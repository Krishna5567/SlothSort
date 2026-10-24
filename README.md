# 🦥 SlothSort: Slow & Steady Autonomous Local AI Desktop Tidier

> **Built for the "Slow and Steady" Hackathon Challenge (International Sloth Day Edition)**  
> *Channeling our inner sloth to automate digital clutter with 100% open-source AI, zero cloud dependencies, and zero cost.*

---

## 🍃 Overview

Sloths don't stress, they don't rush, and they conserve their energy. Human developers, on the other hand, spend hours:
- Digging through chaotic `Downloads/` and `Desktop/` folders.
- Listening to rambling 5-minute voice memos from colleagues.
- Renaming cryptic files like `scan_p10.png` or `IMG_2984.PNG`.
- Dealing with paid cloud AI subscriptions that fail as soon as the Wi-Fi drops.

**SlothSort** is an autonomous desktop and voice note organizer powered entirely by **open-weight and open-source AI models running locally on your machine**. 

You dump your cluttered files into a folder, hit **"Hibernate & Sort (Lazy Mode)"**, and go to sleep. SlothSort steadily transcribes audio recordings using local **OpenAI Whisper**, understands and summarizes documents using Hugging Face's open-weight **SmolLM2-360M-Instruct**, sorts everything into clean directories, generates companion transcript files, and serves a soothing **Morning Digest** with offline synthesized speech via **pyttsx3**.

---

## 🌟 Key Features

1. **🎙️ Offline Voice Note Transcription (OpenAI Whisper)**
   - Transcribes voice memos, audio recordings, and meeting notes locally on GPU/CPU.
   - Automatically writes companion `.txt` transcripts right next to the audio files so you never have to re-listen to voice messages.
2. **🧠 Open-Weight Content Understanding (SmolLM2-360M-Instruct)**
   - Reads text, invoices, receipts, code files, and notes.
   - Generates concise 2-sentence summaries and proposes neat, descriptive snake_case names for cryptic files.
3. **☕ The Sloth Morning Digest & Offline Voice Briefing**
   - Hands you an executive morning recap of everything sorted while you rested.
   - Includes an inline offline voice player synthesized via `pyttsx3` (zero cloud TTS).
4. **↩️ 1-Click Undo / Rollback Engine**
   - Every file move and rename is logged in an encrypted transaction manifest (`storage/manifests/`).
   - If you ever change your mind, hit **"Undo Last Run"** to restore files to their exact original locations.
5. **🎲 Built-in Lazy Sandbox**
   - Click "Populate Sample Clutter" to instantly test voice memos, mock tax invoices, Python scripts, and chat logs without touching your personal files.

---

## 🌿 Why Open Innovation Matters (The Core Hackathon Question)

| Dimension | 🌿 Open-Source AI (SlothSort) | ☁️ Closed Proprietary APIs (OpenAI / Claude) |
|---|---|---|
| **Privacy & Sovereignty** | **100% On-Device:** Bank receipts, private voice memos, and personal code never leave your SSD. | Files and audio uploaded to remote data centers; logged or used for telemetry. |
| **Running Cost** | **$0.00 Forever:** No API tokens, no monthly subscriptions, no credit card required. | Pay-per-token and per-minute audio charges ($20–$100+/mo). |
| **Offline Resilience** | **Zero Internet Required:** Works in an airplane, in the woods, or with Wi-Fi toggled off. | Completely fails without high-speed internet connection. |
| **Model Freedom** | Swap Whisper `base`/`small`/`large`, quantize SmolLM2 with GGUF, or fine-tune locally. | Locked to vendor pricing, rate limits, and model deprecation cycles. |
| **Sloth Factor** | Set it up once, hibernate your laptop, wake up organized. | Constant worry about token quotas, API error retries, and network latency. |

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+
- PyTorch (CUDA optional for GPU acceleration, CPU supported out-of-the-box)

### 2. Launch
```bash
cd slothsort
python run.py
```
This will automatically launch the server and open your browser at `http://localhost:8000`.

### 3. Usage in 3 Steps
1. Click **"🎲 Populate Sample Clutter"** to load the safe sandbox test files.
2. Click **"💤 Hibernate & Sort (Lazy Mode)"**. Watch the sloth mascot steadily process files locally.
3. Switch to the **"☕ Morning Digest"** tab to read your summary and listen to the offline voice briefing!

---

## 🛠️ Tech Stack & Open-Source Components

- **Speech-to-Text**: `openai-whisper` (`base` model, MIT License)
- **Language Model**: `HuggingFaceTB/SmolLM2-360M-Instruct` (Apache 2.0 License)
- **Offline TTS**: `pyttsx3` (Native SAPI5 / NSSpeechSynthesizer)
- **Backend**: FastAPI + Uvicorn + Pydantic
- **Frontend**: Vanilla HTML5, CSS3 Glassmorphism, Modern Async JavaScript
- **Safety**: Manifest-based transactional rollback engine
