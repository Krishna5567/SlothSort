import os
import sys

# Configure UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import webbrowser
import threading
import time
import uvicorn
import torch

def open_browser():
    time.sleep(1.5)
    print("\n[SlothSort] Opening browser at http://localhost:8000 ...\n")
    webbrowser.open("http://localhost:8000")

def main():
    print("=" * 60)
    print("         [SlothSort] - Slow & Steady Local AI Agent")
    print("      International Sloth Day Edition | 100% Offline")
    print("=" * 60)
    
    device = "CUDA GPU (" + torch.cuda.get_device_name(0) + ")" if torch.cuda.is_available() else "CPU"
    print(f"[*] Compute Device: {device}")
    print("[*] Open Models: SmolLM2-360M (HF) + OpenAI Whisper (base) + pyttsx3")
    print("[*] Cloud Calls: None (0.00% external network traffic)")
    print("[*] Server Address: http://localhost:8000")
    print("=" * 60)

    # Start browser opener in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Run uvicorn server
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False, log_level="info")

if __name__ == "__main__":
    main()
