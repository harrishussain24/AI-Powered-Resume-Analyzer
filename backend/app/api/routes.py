from fastapi import APIRouter, UploadFile, File
from services.resume_parser import extract_text_from_pdf
from services.resume_parser import analyze_resume_text

router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)
    if not text:
        return {"error": "No text found in the PDF file."}
    text = text.strip()
    if not text:
        return {"error": "The PDF file is empty or contains no readable text."}
    analysis = analyze_resume_text(text)
    if not analysis:
        return {"error": "Failed to analyze the resume text."}
    analysis["filename"] = file.filename
    analysis["content"] = text
    # Close the file after reading
    file.file.close()

    return {"filename": file.filename, "content": text, "analysis": analysis}