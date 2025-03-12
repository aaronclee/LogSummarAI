from fastapi import APIRouter, UploadFile, File, HTTPException

from src.log_parser import parse_log_line
from src.obfuscator import obfuscate, deobfuscate, email_mapping, ip_mapping
from src.summarizer import summarize_logs

router = APIRouter()

@router.post("/upload")
async def upload_logs(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are accepted.")
    content = await file.read()
    text = content.decode("utf-8")
    lines = text.splitlines()
    
    parsed_logs = []
    for line in lines:
        # Obfuscate sensitive data in each line.
        obfuscated_line = obfuscate(line)
        parsed = parse_log_line(obfuscated_line)
        if parsed:
            parsed_logs.append(parsed)
    
    # Deduplicate logs (using log level and message as the key).
    seen = set()
    unique_logs = []
    for log in parsed_logs:
        key = (log["level"], log["message"])
        if key not in seen:
            seen.add(key)
            unique_logs.append(log)
    
    summary = summarize_logs(unique_logs, email_mapping, ip_mapping)
    # Recompose sensitive information for internal review.
    final_summary = deobfuscate(summary)
    
    return {"summary": final_summary}