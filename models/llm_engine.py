"""
LLM Engine for SlothSort
Loads open-weight HuggingFaceTB/SmolLM2-360M-Instruct locally.
Performs semantic categorization, intelligent renaming, and generates the Morning Digest.
"""

import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

_tokenizer = None
_model = None
MODEL_ID = "HuggingFaceTB/SmolLM2-360M-Instruct"

def get_llm():
    global _tokenizer, _model
    if _model is None or _tokenizer is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        print(f"[SlothLLM] Loading {MODEL_ID} on {device} ({dtype})...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=dtype,
            device_map="auto" if torch.cuda.is_available() else None
        )
        if not torch.cuda.is_available():
            _model.to("cpu")
        print(f"[SlothLLM] {MODEL_ID} ready for local inference.")
    return _tokenizer, _model

def generate_completion(prompt: str, max_new_tokens: int = 120, temperature: float = 0.3) -> str:
    """Generates completion using local SmolLM2 model."""
    try:
        tokenizer, model = get_llm()
        messages = [
            {"role": "system", "content": "You are SlothSort, a concise, highly intelligent desktop organizer assistant. Provide clear, minimal answers."},
            {"role": "user", "content": prompt}
        ]
        text_input = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        device = model.device
        inputs = tokenizer(text_input, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=(temperature > 0),
                temperature=temperature if temperature > 0 else 1.0,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )
        new_tokens = outputs[0][inputs.input_ids.shape[-1]:]
        response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        return response
    except Exception as e:
        print(f"[SlothLLM Error] {e}")
        return ""

def generate_smart_rename(filename: str, snippet: str, category: str) -> str:
    """Proposes a neat, clean, descriptive filename (preserving original extension)."""
    base, ext = os.path.splitext(filename)
    
    # If the filename already looks descriptive (not scan_p10, IMG_1234, Untitled, etc.), keep clean
    cryptic_patterns = [r'^scan_', r'^img_', r'^temp_', r'^untitled', r'^new_file', r'^audio_', r'^step_', r'^qvwr', r'^xkt']
    is_cryptic = any(re.search(pat, base.lower()) for pat in cryptic_patterns) or len(base) <= 4 or base.isdigit()
    
    if not is_cryptic and snippet == "":
        clean_base = re.sub(r'[\s\-]+', '_', base.strip().lower())
        return f"{clean_base}{ext}"
    
    clean_snippet = (snippet[:200] if snippet else base).replace("\n", " ").strip()
    prompt = (
        f"Original filename: '{filename}'\n"
        f"File category: '{category}'\n"
        f"Content preview: '{clean_snippet}'\n\n"
        f"Task: Suggest a concise, descriptive snake_case filename (3 to 5 words max) reflecting what this file is. "
        f"Include the extension '{ext}'. Reply ONLY with the filename, nothing else."
    )
    
    res = generate_completion(prompt, max_new_tokens=25, temperature=0.2)
    # Extract clean filename
    match = re.search(r'([a-zA-Z0-9_\-]+\.[a-zA-Z0-9]+)', res)
    if match:
        suggested = match.group(1).lower()
        # Cap length
        s_base, s_ext = os.path.splitext(suggested)
        if len(s_base) > 35:
            s_base = s_base[:35].rstrip('_')
        suggested = f"{s_base}{ext}"
        return suggested
    
    # Fallback to sanitized existing base
    clean_base = re.sub(r'[^a-zA-Z0-9_]', '_', base.strip().lower()).strip('_')
    return f"{clean_base}{ext}"

def summarize_snippet(text: str, max_words: int = 40) -> str:
    """Summarizes text into 1-2 punchy sentences."""
    if not text or len(text.strip()) == 0:
        return "No text content available."
    
    clean_text = text[:800].replace("\n", " ")
    prompt = f"Summarize this text in 1 or 2 concise, clear sentences (under {max_words} words):\n\n\"{clean_text}\""
    summary = generate_completion(prompt, max_new_tokens=60, temperature=0.3)
    if not summary:
        words = text.strip().split()
        return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")
    return summary

def generate_morning_digest_text(files_summary_list: list, total_files: int, voice_memo_count: int) -> dict:
    """
    Generates a charming Sloth-themed morning digest.
    """
    items_text = "\n".join([f"- {item['new_name']} ({item['category']}): {item['summary']}" for item in files_summary_list[:8]])
    
    prompt = (
        f"You are the SlothSort morning host. Write a brief, relaxing 3-4 sentence morning briefing for the user "
        f"who just woke up after a good sleep. You organized {total_files} messy files (including {voice_memo_count} voice memos). "
        f"Here are the top files processed:\n{items_text}\n\n"
        f"Tone: Relaxed, warm, gently humorous, sloth-themed ('you slept, I sorted'). Keep it under 80 words."
    )
    
    sloth_quote = generate_completion(prompt, max_new_tokens=120, temperature=0.4)
    if not sloth_quote or len(sloth_quote) < 20:
        sloth_quote = (
            f"Good morning! While you were resting peacefully, SlothSort steadily organized {total_files} files "
            f"and transcribed your voice memos. Everything is cataloged and safe. Energy conserved: 100%. "
            f"Go grab your coffee—today's clutter is already handled."
        )
    
    return {
        "greeting": "Good Morning, Master Sloth 🦥",
        "briefing": sloth_quote,
        "total_files": total_files,
        "voice_memos": voice_memo_count,
        "energy_saved_pct": "100%",
        "sloth_zen_rating": "5 / 5 Leaves 🍃"
    }
