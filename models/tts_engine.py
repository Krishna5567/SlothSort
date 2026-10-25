"""
TTS Engine for SlothSort
Generates offline voice briefings using native pyttsx3 or wave fallback.
Zero cloud requests, instant execution, completely private.
"""

import os
import wave
import struct
import math
import tempfile

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    pyttsx3 = None
    HAS_PYTTSX3 = False

if os.environ.get("VERCEL"):
    AUDIO_DIR = os.path.join(tempfile.gettempdir(), "slothsort_storage", "audio_output")
else:
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
    
    if HAS_PYTTSX3:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 155)
            voices = engine.getProperty('voices')
            if voices:
                engine.setProperty('voice', voices[0].id)
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return output_path
        except Exception as e:
            print(f"[SlothTTS Error] Failed to generate pyttsx3 speech: {e}")
            
    # Pure Python synthetic chime/sound fallback if pyttsx3 is not installed (e.g. Vercel serverless)
    try:
        sample_rate = 22050
        duration = 1.2
        n_samples = int(sample_rate * duration)
        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            for i in range(n_samples):
                t = float(i) / sample_rate
                value = 0.3 * math.sin(2.0 * math.pi * 523.25 * t) + 0.2 * math.sin(2.0 * math.pi * 659.25 * t)
                decay = math.exp(-2.5 * t)
                sample = int(value * decay * 32767.0)
                wav_file.writeframes(struct.pack('<h', sample))
        return output_path
    except Exception as e:
        print(f"[SlothTTS Fallback Error] {e}")
        return ""
