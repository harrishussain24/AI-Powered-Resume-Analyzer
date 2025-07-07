import json
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.resume_parser import extract_text_from_pdf, analyze_resume_text
from models.session import get_db
from models.db import Resume
from services.job_description_analyzer import analyze_job_description
from fastapi import Body
from services.matcher import match_resume_to_job
from pydantic import BaseModel
from fastapi import HTTPException, status
from pdfminer.pdfparser import PDFSyntaxError

router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    try:
        text = extract_text_from_pdf(file)
    except PDFSyntaxError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PDF file format."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read PDF file: {str(e)}"
        )

    if not text or "No text found" in text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No text found in the PDF file."
        )

    text = text.strip()
    if not text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="The PDF file is empty or contains no readable text."
        )

    analysis = analyze_resume_text(text)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze the resume text."
        )

    parsed_json = json.dumps(analysis)

    new_resume = Resume(
        filename=file.filename,
        content=text,
        parsed_data=parsed_json
    )

    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    file.file.close()

    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "analysis": analysis
    }


@router.post("/analyze-job/")
async def analyze_job(description: str = Body(..., embed=True)):
    if not description or not description.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Job description must not be empty.")
    try:
        result = analyze_job_description(description)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to analyze job description: {str(e)}")


class MatchRequest(BaseModel):
    resume: dict
    job: dict

@router.post("/match")
async def match_resume_job(data: MatchRequest):
    if not data.resume or not data.job:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Resume and job data must be provided.")
    try:
        result = match_resume_to_job(data.resume, data.job)
        return {"status": "success", "match": result}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to match resume to job: {str(e)}")