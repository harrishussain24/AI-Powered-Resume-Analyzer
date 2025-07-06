import json
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.resume_parser import extract_text_from_pdf, analyze_resume_text
from models.session import get_db
from models.db import Resume
from services.job_description_analyzer import analyze_job_description
from fastapi import Body

router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    text = extract_text_from_pdf(file)
    if not text:
        return {"error": "No text found in the PDF file."}
    text = text.strip()
    if not text:
        return {"error": "The PDF file is empty or contains no readable text."}
    analysis = analyze_resume_text(text)
    if not analysis:
        return {"error": "Failed to analyze the resume text."}

    # Convert analysis dict to JSON string
    parsed_json = json.dumps(analysis)

    # Create Resume DB instance
    new_resume = Resume(
        filename=file.filename,
        content=text,
        parsed_data=parsed_json
    )

    # Add and commit the new resume to the DB
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)  # to get the auto-generated id

    file.file.close()

    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "analysis": analysis
    }



@router.post("/analyze-job/")
async def analyze_job(description: str = Body(..., embed=True)):
    result = analyze_job_description(description)
    return result