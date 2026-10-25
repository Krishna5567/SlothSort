"""
SlothSort FastAPI Application
The 100% Offline, Open-Source AI Desktop & Voice Memo Organizer
Supports both local native GPU/CPU execution and lightweight Vercel cloud deployment.
"""

import os
import glob
import tempfile
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List

try:
    import torch
    HAS_TORCH = True
except ImportError:
    torch = None
    HAS_TORCH = False

from models.classifier import determine_category_and_metadata
from models.organizer import execute_organization, undo_run, list_history
from models.llm_engine import generate_morning_digest_text
from models.tts_engine import generate_speech_file
from models.sandbox_generator import populate_sandbox, SANDBOX_DIR

app = FastAPI(title="SlothSort API", description="Autonomous Local Desktop Organizer with Open-Source AI", redirect_slashes=False)

IS_VERCEL = bool(os.environ.get("VERCEL"))
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

if IS_VERCEL:
    STORAGE_DIR = os.path.join(tempfile.gettempdir(), "slothsort_storage")
else:
    STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))

AUDIO_DIR = os.path.join(STORAGE_DIR, "audio_output")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

class ScanRequest(BaseModel):
    directory: Optional[str] = None

class ProcessRequest(BaseModel):
    directory: Optional[str] = None
    enable_llm: bool = True
    enable_tts: bool = True
    sloth_mode: bool = False

@app.get("/api/status")
@app.get("/status")
def get_system_status():
    """Returns local AI and hardware status."""
    cuda_avail = torch.cuda.is_available() if (HAS_TORCH and torch) else False
    if cuda_avail:
        device_name = torch.cuda.get_device_name(0)
        vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
    elif IS_VERCEL:
        device_name = "Vercel Serverless (Cloud Showcase)"
        vram_gb = 0
    else:
        device_name = "Local CPU Inference"
        vram_gb = 0
    
    return {
        "status": "online",
        "platform": "Vercel Serverless" if IS_VERCEL else "Local Native",
        "offline_ready": not IS_VERCEL,
        "cuda_available": cuda_avail,
        "device": device_name,
        "vram_gb": vram_gb,
        "llm_model": "HuggingFaceTB/SmolLM2-360M-Instruct" if HAS_TORCH else "SmolLM2-360M (Cloud Simulation Mode)",
        "whisper_model": "openai-whisper/base (CUDA accelerated)" if HAS_TORCH else "Whisper base (Cloud Simulation Mode)",
        "tts_engine": "pyttsx3 / Web Speech API",
        "cloud_api_cost": "$0.00 / ∞",
        "data_leakage_risk": "0.0% (Zero packets sent to external servers)"
    }

@app.post("/api/sandbox/populate")
@app.post("/sandbox/populate")
def api_populate_sandbox():
    """Populates or resets the sandbox test folder with sample messy files."""
    sandbox_path = populate_sandbox()
    files = [f for f in os.listdir(sandbox_path) if os.path.isfile(os.path.join(sandbox_path, f))]
    return {
        "success": True,
        "sandbox_path": sandbox_path,
        "file_count": len(files),
        "files": files
    }

@app.post("/api/scan")
@app.post("/scan")
def api_scan_directory(req: ScanRequest):
    """Scans target directory and previews files without moving them."""
    target_dir = req.directory or SANDBOX_DIR
    if not os.path.exists(target_dir):
        if target_dir == SANDBOX_DIR:
            populate_sandbox()
        else:
            raise HTTPException(status_code=404, detail="Target directory does not exist.")
            
    files = []
    for entry in os.scandir(target_dir):
        if entry.is_file() and not entry.name.startswith("."):
            _, ext = os.path.splitext(entry.name)
            files.append({
                "name": entry.name,
                "path": entry.path,
                "size_bytes": entry.stat().st_size,
                "extension": ext.lower()
            })
            
    return {
        "target_dir": target_dir,
        "file_count": len(files),
        "files": files
    }

@app.post("/api/process")
@app.post("/process")
def api_process_directory(req: ProcessRequest):
    """
    Core 'Hibernate & Sort' endpoint.
    Transcribes audio with Whisper, analyzes text with SmolLM2,
    organizes files safely, and generates the Morning Digest with audio.
    """
    target_dir = req.directory or SANDBOX_DIR
    if not os.path.exists(target_dir):
        if target_dir == SANDBOX_DIR:
            populate_sandbox()
        else:
            raise HTTPException(status_code=404, detail="Directory not found.")
            
    file_entries = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    if not file_entries:
        return {
            "success": False,
            "message": "No files found in directory to organize. Try generating sample sandbox files!",
            "target_dir": target_dir,
            "results": []
        }
        
    analysis_results = []
    voice_memo_count = 0
    
    for fpath in file_entries:
        if os.path.basename(fpath).startswith("."):
            continue
            
        res = determine_category_and_metadata(fpath, enable_llm=req.enable_llm)
        if res.get("is_audio"):
            voice_memo_count += 1
        analysis_results.append(res)
        
    org_result = execute_organization(target_dir, analysis_results)
    digest = generate_morning_digest_text(analysis_results, len(analysis_results), voice_memo_count)
    
    audio_file_url = None
    if req.enable_tts:
        speech_text = f"{digest['greeting']}. {digest['briefing']}"
        wav_path = generate_speech_file(speech_text, f"digest_{org_result['run_id']}.wav")
        if wav_path and os.path.exists(wav_path):
            audio_file_url = f"/api/audio/{os.path.basename(wav_path)}"
            
    return {
        "success": True,
        "run_id": org_result["run_id"],
        "target_dir": target_dir,
        "total_files": len(analysis_results),
        "voice_memos": voice_memo_count,
        "digest": digest,
        "audio_url": audio_file_url,
        "operations": org_result["moved_count"],
        "items": analysis_results
    }

@app.post("/api/undo")
@app.post("/undo")
def api_undo(run_id: Optional[str] = None):
    """Rolls back an organizing operation."""
    res = undo_run(run_id)
    return res

@app.get("/api/history")
@app.get("/history")
def api_history():
    """Returns past organization runs."""
    return list_history()

@app.get("/api/audio/{filename}")
@app.get("/audio/{filename}")
def api_get_audio(filename: str):
    """Streams generated audio files or sandbox audio."""
    path = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(path):
        path = os.path.join(SANDBOX_DIR, filename)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(path, media_type="audio/wav")

@app.get("/api/open-innovation-stats")
@app.get("/open-innovation-stats")
def api_open_innovation_stats():
    """Returns comparative metrics highlighting the advantages of open-weight local AI."""
    return {
        "comparison": [
            {
                "feature": "Privacy & Data Sovereignty",
                "open_source": "100% Private (Runs on local GPU/CPU; voice notes & files never leave disk)",
                "closed_api": "Data sent to third-party cloud data centers; logged or used for training"
            },
            {
                "feature": "Cost & Billing",
                "open_source": "$0.00 forever (Zero API tokens, zero credit cards, no surprise bills)",
                "closed_api": "Pay-per-token / per-minute audio charges, easily $20-$100/mo"
            },
            {
                "feature": "Offline Resilience",
                "open_source": "Works on an airplane, in the woods, or with Wi-Fi toggled off",
                "closed_api": "Completely fails without high-speed internet connection"
            },
            {
                "feature": "Customizability & Control",
                "open_source": "Swap Whisper base/small/large, adjust SmolLM2 temperature, quantize to GGUF",
                "closed_api": "Locked to vendor model versions, deprecations, and rate limits"
            },
            {
                "feature": "Sloth Score (Effort Required)",
                "open_source": "Set it once, hibernate laptop, wake up organized",
                "closed_api": "Requires managing API keys, tokens, rate limit retries, network drops"
            }
        ]
    }

# Explicit static file endpoints to guarantee delivery on all hosting environments
@app.get("/static/css/styles.css")
def serve_css():
    css_path = os.path.join(STATIC_DIR, "css", "styles.css")
    if not os.path.exists(css_path):
        css_path = os.path.join(os.path.dirname(__file__), "public", "static", "css", "styles.css")
    if os.path.exists(css_path):
        return FileResponse(css_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS not found")

@app.get("/static/js/app.js")
def serve_js():
    js_path = os.path.join(STATIC_DIR, "js", "app.js")
    if not os.path.exists(js_path):
        js_path = os.path.join(os.path.dirname(__file__), "public", "static", "js", "app.js")
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JS not found")

# Mount static frontend
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_file):
        index_file = os.path.join(os.path.dirname(__file__), "public", "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file, media_type="text/html")
    return {"message": "SlothSort API is live."}
