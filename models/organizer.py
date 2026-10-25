"""
Organizer and Rollback Engine for SlothSort
Handles safe moving, renaming, transcript output, and 1-click Undo operations.
"""

import os
import shutil
import json
import time
import tempfile

if os.environ.get("VERCEL"):
    STORAGE_DIR = os.path.join(tempfile.gettempdir(), "slothsort_storage")
else:
    STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage"))

MANIFEST_DIR = os.path.join(STORAGE_DIR, "manifests")

def ensure_manifest_dir():
    os.makedirs(MANIFEST_DIR, exist_ok=True)

def sanitize_folder_name(name: str) -> str:
    return name.replace("&", "and").replace(" ", "_").replace("/", "_")

def execute_organization(target_dir: str, analysis_results: list) -> dict:
    """
    Moves and renames files according to analysis.
    Creates audio transcript text files next to voice memos.
    Saves a rollback manifest.
    """
    ensure_manifest_dir()
    run_id = f"run_{int(time.time())}"
    manifest = {
        "run_id": run_id,
        "target_dir": target_dir,
        "timestamp": time.time(),
        "operations": []
    }
    
    for item in analysis_results:
        orig_path = item["original_path"]
        if not os.path.exists(orig_path):
            continue
            
        category_dir_name = sanitize_folder_name(item["category"])
        dest_folder = os.path.join(target_dir, category_dir_name)
        os.makedirs(dest_folder, exist_ok=True)
        
        # New filename
        clean_new_name = item.get("new_name") or item["original_name"]
        dest_path = os.path.join(dest_folder, clean_new_name)
        
        # Avoid collision
        counter = 1
        base, ext = os.path.splitext(clean_new_name)
        while os.path.exists(dest_path) and dest_path != orig_path:
            dest_path = os.path.join(dest_folder, f"{base}_{counter}{ext}")
            counter += 1
            
        # Move file
        shutil.move(orig_path, dest_path)
        
        # If audio and transcript exists, write a companion transcript text file!
        transcript_path = None
        if item.get("is_audio") and item.get("transcript"):
            transcript_filename = f"{os.path.splitext(os.path.basename(dest_path))[0]}_transcript.txt"
            transcript_path = os.path.join(dest_folder, transcript_filename)
            with open(transcript_path, "w", encoding="utf-8") as tf:
                tf.write(f"Audio Transcript for: {os.path.basename(dest_path)}\n")
                tf.write("=" * 50 + "\n\n")
                tf.write(item["transcript"])
                tf.write("\n\n" + "=" * 50 + "\n")
                tf.write(f"Summary: {item.get('summary', '')}\n")
        
        manifest["operations"].append({
            "original_path": orig_path,
            "destination_path": dest_path,
            "original_name": item["original_name"],
            "new_name": os.path.basename(dest_path),
            "transcript_path": transcript_path,
            "category": item["category"]
        })
        
    # Save manifest
    manifest_file = os.path.join(MANIFEST_DIR, f"{run_id}.json")
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    return {
        "run_id": run_id,
        "manifest_file": manifest_file,
        "moved_count": len(manifest["operations"])
    }

def undo_run(run_id: str = None) -> dict:
    """
    Rolls back an organizing operation by moving files back to their original locations.
    If run_id is None, undos the most recent run.
    """
    ensure_manifest_dir()
    manifests = sorted([f for f in os.listdir(MANIFEST_DIR) if f.endswith(".json") and not f.endswith(".undone.json")], reverse=True)
    if not manifests:
        return {"success": False, "error": "No organizing history found to undo."}
        
    selected_manifest_file = None
    if run_id:
        selected_manifest_file = os.path.join(MANIFEST_DIR, f"{run_id}.json")
    else:
        selected_manifest_file = os.path.join(MANIFEST_DIR, manifests[0])
        
    if not os.path.exists(selected_manifest_file):
        return {"success": False, "error": f"Manifest file not found: {selected_manifest_file}"}
        
    with open(selected_manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    restored = 0
    errors = []
    for op in manifest["operations"]:
        dest = op["destination_path"]
        orig = op["original_path"]
        transcript_path = op.get("transcript_path")
        
        if transcript_path and os.path.exists(transcript_path):
            try:
                os.remove(transcript_path)
            except Exception:
                pass
                
        if os.path.exists(dest):
            try:
                os.makedirs(os.path.dirname(orig), exist_ok=True)
                shutil.move(dest, orig)
                restored += 1
            except Exception as e:
                errors.append(f"Could not restore {dest} -> {orig}: {e}")
                
    undone_path = selected_manifest_file.replace(".json", ".undone.json")
    try:
        os.rename(selected_manifest_file, undone_path)
    except Exception:
        pass
        
    return {
        "success": True,
        "restored_count": restored,
        "run_id": manifest["run_id"],
        "errors": errors
    }

def list_history() -> list:
    """Lists past runs with counts and status."""
    ensure_manifest_dir()
    files = sorted([f for f in os.listdir(MANIFEST_DIR) if f.endswith(".json")], reverse=True)
    history = []
    for f in files:
        path = os.path.join(MANIFEST_DIR, f)
        is_undone = f.endswith(".undone.json")
        try:
            with open(path, "r", encoding="utf-8") as mf:
                data = json.load(mf)
                history.append({
                    "run_id": data.get("run_id"),
                    "timestamp": data.get("timestamp"),
                    "target_dir": data.get("target_dir"),
                    "file_count": len(data.get("operations", [])),
                    "is_undone": is_undone
                })
        except Exception:
            continue
    return history
