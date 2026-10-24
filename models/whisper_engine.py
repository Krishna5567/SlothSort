"""
Whisper Engine for SlothSort
Loads open-weight OpenAI Whisper locally with GPU/CPU acceleration.
Transcribes voice memos, audio recordings, and meeting notes with 100% offline privacy.
"""

import os
import torch
import whisper

_whisper_model = None

def get_whisper_model(model_name: str = "base"):
    global _whisper_model
    if _whisper_model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[SlothWhisper] Loading Whisper '{model_name}' on {device}...")
        _whisper_model = whisper.load_model(model_name, device=device)
        print(f"[SlothWhisper] Whisper '{model_name}' loaded successfully!")
    return _whisper_model

def transcribe_audio(audio_path: str, model_name: str = "base") -> dict:
    """
    Transcribes an audio file offline using local Whisper model.
    Returns:
        dict: {
            "text": str,
            "language": str,
            "duration": float,
            "success": bool,
            "error": str or None
        }
    """
    if not os.path.exists(audio_path):
        return {"text": "", "language": "unknown", "duration": 0, "success": False, "error": "File not found"}
    
    try:
        model = get_whisper_model(model_name)
        result = model.transcribe(audio_path, fp16=(torch.cuda.is_available()))
        text = result.get("text", "").strip()
        language = result.get("language", "en")
        
        return {
            "text": text,
            "language": language,
            "success": True,
            "error": None
        }
    except Exception as e:
        print(f"[SlothWhisper Error] Failed to transcribe {audio_path}: {e}")
        return {
            "text": "",
            "language": "unknown",
            "success": False,
            "error": str(e)
        }
