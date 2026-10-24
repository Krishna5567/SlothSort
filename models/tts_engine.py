"""
TTS Engine for SlothSort
Generates offline voice briefings using native pyttsx3.
Zero cloud requests, instant execution, completely private.
"""

import os
import pyttsx3

AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "audio_output"))

def ensure_audio_dir():
    os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_speech_file(text: str, filename: str = "morning_digest.wav") -> str:
    """
    Renders text to an offline audio WAV file.
    Returns the absolute file path.
    """
    ensure_audio_dir()
    output_path = os.path.join(AUDIO_DIR, filename)
    
    try:
        # Reinitialize engine per request to avoid comtypes thread issues on Windows
        engine = pyttsx3.init()
        # Set relaxed, steady speaking rate for Sloth theme (default is ~200, we use 155)
        engine.setProperty('rate', 155)
        # Select voice if available
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
            
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return output_path
    except Exception as e:
        print(f"[SlothTTS Error] Failed to generate speech: {e}")
        return ""
