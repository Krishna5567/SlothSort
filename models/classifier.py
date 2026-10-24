"""
File Classifier & Inspector for SlothSort
Extracts metadata, content snippets, transcripts, and classifies files.
"""

import os
import re
from .whisper_engine import transcribe_audio
from .llm_engine import generate_smart_rename, summarize_snippet

# Extension mappings
AUDIO_EXTS = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.aac'}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'}
CODE_EXTS = {'.py', '.js', '.ts', '.html', '.css', '.java', '.cpp', '.c', '.sh', '.bat', '.ps1'}
DOC_EXTS = {'.txt', '.md', '.pdf', '.docx', '.doc', '.rtf'}
DATA_EXTS = {'.csv', '.xlsx', '.xls', '.json', '.xml', '.parquet'}
ARCHIVE_EXTS = {'.zip', '.tar', '.gz', '.7z', '.rar'}

def extract_file_content_snippet(file_path: str, max_chars: int = 1500) -> str:
    """Extracts a readable text snippet from various file types."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext in {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.bat', '.sh'}:
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                    return f.read(max_chars).strip()
            except Exception:
                continue
    elif ext == '.pdf':
        try:
            import fitz # PyMuPDF
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
                if len(text) >= max_chars:
                    break
            return text[:max_chars].strip()
        except Exception:
            pass
    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])[:max_chars].strip()
        except Exception:
            pass
            
    return ""

def determine_category_and_metadata(file_path: str, enable_llm: bool = True) -> dict:
    """
    Analyzes a file, transcribes if audio, extracts text snippet,
    determines category, proposes clean name, and produces a summary.
    """
    filename = os.path.basename(file_path)
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    size_bytes = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    
    category = "Documents & Notes"
    snippet = ""
    is_audio = False
    transcript = ""
    
    # Check Audio
    if ext in AUDIO_EXTS:
        category = "Voice Memos & Audio"
        is_audio = True
        # Transcribe offline with Whisper
        whisper_res = transcribe_audio(file_path, model_name="base")
        if whisper_res["success"] and whisper_res["text"]:
            transcript = whisper_res["text"]
            snippet = f"Audio transcript: {transcript[:300]}"
        else:
            snippet = f"Voice recording ({ext[1:].upper()})"
    
    # Check Image
    elif ext in IMAGE_EXTS:
        category = "Media & Graphics"
        snippet = f"Image file ({ext[1:].upper()})"
        if any(term in filename.lower() for term in ["receipt", "invoice", "bill", "scan"]):
            category = "Receipts & Finance"
            
    # Check Code
    elif ext in CODE_EXTS:
        category = "Code & Scripts"
        snippet = extract_file_content_snippet(file_path)
        
    # Check Data
    elif ext in DATA_EXTS:
        category = "Spreadsheets & Data"
        snippet = extract_file_content_snippet(file_path)
        
    # Check Archives
    elif ext in ARCHIVE_EXTS:
        category = "Archives & Backups"
        snippet = "Compressed archive file"
        
    # Documents / Notes
    elif ext in DOC_EXTS:
        category = "Documents & Notes"
        snippet = extract_file_content_snippet(file_path)
        # Check financial keywords in text
        if any(kw in snippet.lower() for kw in ["invoice", "total:", "amount due", "receipt", "tax invoice", "subtotal"]):
            category = "Receipts & Finance"
    else:
        category = "Miscellaneous"
        snippet = f"File type: {ext}"

    # LLM-enhanced renaming and summarizing
    new_name = filename
    summary = ""
    
    if enable_llm:
        new_name = generate_smart_rename(filename, snippet or transcript, category)
        summary = summarize_snippet(transcript if is_audio else snippet, max_words=25)
    else:
        summary = (snippet[:100] + "...") if len(snippet) > 100 else (snippet or "No preview available")
        
    return {
        "original_name": filename,
        "new_name": new_name,
        "category": category,
        "extension": ext,
        "size_bytes": size_bytes,
        "is_audio": is_audio,
        "transcript": transcript,
        "summary": summary,
        "original_path": file_path
    }
