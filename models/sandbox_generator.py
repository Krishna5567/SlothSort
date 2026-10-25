"""
Sandbox Generator for SlothSort
Populates sample messy files (text, code, data, and audio voice memos)
so users and judges can test the app with 1 click without touching real folders.
"""

import os
import wave
import struct
import math
import tempfile

if os.environ.get("VERCEL"):
    SANDBOX_DIR = os.path.join(tempfile.gettempdir(), "slothsort_storage", "sandbox")
else:
    SANDBOX_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "storage", "sandbox"))

SAMPLE_FILES = [
    {
        "name": "scan_p10.txt",
        "content": (
            "TAX INVOICE / RECEIPT\n"
            "SuperMarket Organic Groceries\n"
            "Date: 19-Oct-2026  Time: 18:42\n"
            "Item 1: Organic Bananas (2kg) - $4.50\n"
            "Item 2: Almond Milk (1L) - $3.20\n"
            "Item 3: Fresh Bakery Sourdough - $5.00\n"
            "Subtotal: $12.70\n"
            "Tax (8%): $1.02\n"
            "TOTAL PAID: $13.72\n"
            "Payment Method: Apple Pay (Visa ending in 4102)\n"
            "Thank you for shopping local!"
        )
    },
    {
        "name": "group_chat_export_october.txt",
        "content": (
            "[22:15] Alex: Hey everyone, heads up on the hackathon submission deadline!\n"
            "[22:18] Priya: We finalized the open-weight model integration with SmolLM2 and Whisper.\n"
            "[22:20] Dev: Everything runs 100% locally on CUDA with zero external API calls.\n"
            "[22:25] Alex: Awesome, let's prepare the Sloth Day post and celebrate International Sloth Day.\n"
            "[22:30] Maya: Sounds great, going to sleep now. Let the agent do the tidying overnight!"
        )
    },
    {
        "name": "temp_quick_parser_v3.py",
        "content": (
            "import os\nimport csv\n\n# Quick script to analyze local benchmark numbers\ndef compute_metrics(filepath):\n"
            "    with open(filepath, 'r') as f:\n        reader = csv.DictReader(f)\n"
            "        return sum(float(row['latency_ms']) for row in reader)\n\n"
            "if __name__ == '__main__':\n    print('Running offline benchmark parser...')\n"
        )
    },
    {
        "name": "untidy_notes_oct2026.md",
        "content": (
            "# Project Sloth Manifesto\n\n"
            "Sloths move slowly to conserve energy. Human developers spend hours dragging files, "
            "renaming downloads, and catching up on chat messages. "
            "Our goal: build an autonomous, zero-cloud assistant that does the boring digital housekeeping "
            "while you relax. 100% private, 100% open source."
        )
    },
    {
        "name": "weekly_metrics_dump.csv",
        "content": (
            "metric,value,unit\n"
            "vram_usage,1.8,GB\n"
            "offline_privacy_score,100,percent\n"
            "api_bill_usd,0,dollars\n"
            "energy_conserved,99.9,percent\n"
        )
    }
]

def populate_sandbox():
    """Generates the messy test folder."""
    os.makedirs(SANDBOX_DIR, exist_ok=True)
    
    # 1. Create text and code files
    for item in SAMPLE_FILES:
        filepath = os.path.join(SANDBOX_DIR, item["name"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(item["content"])
            
    # 2. Create sample audio voice memo
    audio_path = os.path.join(SANDBOX_DIR, "voice_memo_001.wav")
    if not os.path.exists(audio_path):
        generated = False
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 145)
            engine.save_to_file(
                "Voice memo recorded on October 20. Reminder to finalize the International Sloth Day demo. "
                "The local open weight model runs completely offline with no cloud server. All done, good night.",
                audio_path
            )
            engine.runAndWait()
            generated = True
        except Exception:
            pass
            
        if not generated:
            # Fallback audio generation using standard library wave
            sample_rate = 16000
            duration = 2.0
            n_samples = int(sample_rate * duration)
            with wave.open(audio_path, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                for i in range(n_samples):
                    t = float(i) / sample_rate
                    value = 0.25 * math.sin(2.0 * math.pi * 440.0 * t)
                    sample = int(value * 32767.0)
                    wav_file.writeframes(struct.pack('<h', sample))
            
    return SANDBOX_DIR
