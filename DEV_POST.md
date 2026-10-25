*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

# 🦥 SlothSort: Channeling Our Inner Sloth with 100% Offline Open-Source AI

## What I Built

Sloths move at their own unhurried pace, conserve their energy, and never expend calories when they don't have to. Human developers and knowledge workers, on the other hand, spend hours:
- Drowning in chaotic `Downloads` and `Desktop` folders filled with cryptic files (`scan_p10.png`, `step_576.txt`, `temp_scratch_v2.py`).
- Dreading listening to rambling 4-minute voice notes from colleagues.
- Procrastinating on digital housekeeping because manual sorting and renaming is exhausting.
- Hesitating to use cloud AI tools because they demand recurring subscriptions and upload private bank receipts, personal notes, and voice recordings to remote servers.

To celebrate **International Sloth Day (October 20)** and reward peak laziness, I built **SlothSort**—an autonomous local desktop and voice memo organizer powered 100% by open-weight models.

### How It Rewards Peak Laziness:
1. **Drop & Sleep:** Dump your cluttered downloads, invoices, code snippets, and voice memos into a folder (or use the built-in Lazy Sandbox).
2. **Hit "Hibernate & Sort (Lazy Mode)":** The sleepy sloth agent takes over. It transcribes audio recordings using local **OpenAI Whisper**, parses documents and code using Hugging Face's open-weight **SmolLM2-360M-Instruct**, sorts files into categorized folders, and creates companion `.txt` transcripts for every audio file.
3. **Wake Up to a Morning Digest:** When you wake up, your clutter is organized, cryptic filenames are cleanly renamed in snake_case, and you get an executive **Morning Digest** with a spoken audio briefing.
4. **Zero-Stress Undo:** If you ever change your mind, a 1-click rollback engine restores every single file to its exact original location.

---

## Demo

- 🌐 **Live Cloud Interactive Showcase:** **[https://slothsort.vercel.app](https://slothsort.vercel.app)**
- 💻 **Local Hardware Mode:** Runs 100% offline with CUDA acceleration on an NVIDIA RTX 3050 Laptop GPU (or CPU) taking under 1.8 GB VRAM.

### Quick Tour of the Web UI:
- **🗂️ File Organizer:** Live before/after inspection table showing smart renaming, categorization pills (`Receipts & Finance`, `Voice Memos`, `Code & Scripts`), and AI summaries.
- **☕ Morning Digest:** Personalized sloth greeting, task statistics, energy conserved percentage, and audio playback with browser speech synthesis.
- **🎙️ Voice Memos & Whisper:** Side-by-side audio playback and synchronized Whisper transcripts.
- **↩️ Rollback History:** Transaction-level rollback manifests with 1-click undo.
- **🌱 Open Innovation Manifesto:** Real-time hardware specs, zero cloud cost badges, and offline architecture proof.

---

## Code

{% github Krishna5567/SlothSort %}

👉 **GitHub Repository:** **[https://github.com/Krishna5567/SlothSort](https://github.com/Krishna5567/SlothSort)**

---

## How I Built It

SlothSort is designed as a modular, local-first agent harness:

```
[ Messy Clutter / Voice Memos / Invoices ]
                   │
                   ▼
     ┌─────────────────────────────────────────────────────────┐
     │                  SlothSort Local Agent                  │
     │                                                         │
     │  🎙️ OpenAI Whisper (CUDA FP16 / CPU)                    │
     │     └── Offline speech-to-text -> generates transcript  │
     │                                                         │
     │  🧠 SmolLM2-360M-Instruct (Hugging Face Transformers)   │
     │     └── Content inspection -> semantic categorization   │
     │     └── Intelligent snake_case file renaming            │
     │     └── 2-sentence file summarization                   │
     │                                                         │
     │  🗂️ Transactional Safe Organizer                        │
     │     └── Moves to /Voice_Memos, /Receipts, /Code, etc.   │
     │     └── Generates rollback manifest for 1-click Undo    │
     │                                                         │
     │  ☕ Morning Digest Generator                            │
     │     └── SmolLM2 creates relaxed, humorous recap         │
     │     └── pyttsx3 / Web Speech API synthesizes audio      │
     └─────────────────────────────────────────────────────────┘
                   │
                   ▼
  [ Clean Organized Folders + Companion Transcripts + Audio Digest ]
```

### The Open-Source AI Stack:
- **`openai-whisper` (`base` model, MIT License):** Performs on-device automatic speech recognition. Transcribes voice notes directly on GPU in seconds without sending a single byte to the cloud.
- **`HuggingFaceTB/SmolLM2-360M-Instruct` (Apache 2.0 License):** A lightweight 360M parameter open-weight model that runs in FP16 on consumer laptop GPUs (under 1 GB VRAM). Handles semantic document categorization, smart snake_case renaming, and generates the Morning Digest.
- **`pyttsx3` & Web Speech API:** Generates native offline audio briefings (`morning_digest.wav`) with zero external API calls.
- **`FastAPI` & `Uvicorn`:** High-performance asynchronous backend with structured Pydantic schemas and Server-Sent Event support.
- **Vercel Edge & Serverless Architecture:** Optimized with a lightweight serverless profile (< 20 MB bundle size) and inlined glassmorphic styling for instant web deployment.

---

## Why Does Open Innovation Matter?

The prompt asked: *“In your post, tell us why open innovation matters for what you built. Does it run on a laptop with no internet? Keep someone's data off a server they don't control? Cost nothing to run? Tell us where your open-based approach worked better than a closed one.”*

Here is why open-source AI is the foundational piece that makes SlothSort possible:

### 1. Absolute Data Sovereignty (Keeping Personal Files Off Remote Servers)
A desktop organizer handles the most intimate data in your digital life: bank statements, tax invoices, medical notes, private voice memos, and proprietary code. Sending these files to a closed cloud API (OpenAI, Anthropic, or Google) creates severe privacy and security risks. With local open-weight models:
- **0 bytes of user data ever leave the machine.**
- Network calls to external servers: **0.00%**.
- Sensitive receipts and personal audio diaries stay on your own SSD.

### 2. 100% Offline Capability (Airplane & Cabin Friendly)
Closed APIs completely brick the moment your Wi-Fi drops. SlothSort runs on a laptop GPU (taking under 1.8 GB VRAM) or on standard CPU. You can be on an airplane, in a remote cabin, or in power-saving mode with Wi-Fi toggled off—SlothSort works flawlessly.

### 3. $0.00 Marginal Cost Forever
Closed LLM and Speech APIs charge per input token, output token, and audio minute. Running a continuous background organizing agent with cloud APIs would easily cost $30–$80 every month. SlothSort costs **$0.00 forever**. You set it up once, and it serves you for years with zero subscriptions, zero API keys, and zero credit cards.

### 4. Zero Vendor Lock-in & Model Freedom
Because SlothSort is built on open standards (Hugging Face Transformers and PyTorch), you are never locked into vendor deprecation schedules or sudden price hikes. You can swap Whisper `base` for Whisper `large-v3`, quantize SmolLM2 with GGUF or AWQ for ultra-low memory laptops, or swap in Qwen2.5 with a single configuration change.

---

## My Agent Session

This project was architected, implemented, and deployed using autonomous agent pair-programming:
- **Complete Project Workspace & Code:** [`https://github.com/Krishna5567/SlothSort`](https://github.com/Krishna5567/SlothSort)
- **Local Hardware Verified:** NVIDIA GeForce RTX 3050 Laptop GPU (CUDA 12.4 + PyTorch 2.6.0)

---

## The Lazy Payoff

### Real-World Testing & Time Saved:
During testing this week, I dumped a cluttered directory containing messy receipts (`scan_p10.txt`), raw group chat exports, python benchmark scripts, and voice memos:
- **Manual Sorting Time Avoided:** ~35 to 45 minutes of dragging, reading, listening, and renaming files.
- **Audio Friction Eliminated:** Rather than sitting through audio recordings, SlothSort generated a clean companion `.txt` transcript right beside each audio file in seconds.
- **Effort Expended:** Exactly **1 click** on *"Hibernate & Sort (Lazy Mode)"*.
- **Human Energy Conserved:** **100%**.

---

## Prize Categories

- **Primary Challenge:** Open-Source AI Challenge Week 3: *Slow and Steady* (International Sloth Day Edition)
- **Sub-themes addressed:** Rewarding laziness, running open-weight models locally, keeping personal data off cloud servers, and automating everyday clutter with zero running cost.
