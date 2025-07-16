import json
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.resume_parser import extract_text_from_pdf, analyze_resume_text
from app.models.session import get_db
from app.models.db import Resume, JobDescription
from app.services.job_description_analyzer import analyze_job_description
from fastapi import Body
from app.services.matcher import match_resume_to_job
from pydantic import BaseModel
from fastapi import HTTPException, status
from pdfminer.pdfparser import PDFSyntaxError
import uuid
from app.services.supabase_client import supabase

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

    # ⬇️ Upload the original file to Supabase
    try:
        file_url = await upload_resume_to_supabase(file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload to Supabase: {str(e)}"
        )

    parsed_json = json.dumps(analysis)

    new_resume = Resume(
        filename=file.filename,
        content=text,
        parsed_data=parsed_json,
        file_url=file_url  # optional: if you've added this column in your DB
    )

    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)

    file.file.close()

    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "file_url": file_url,  # expose URL to frontend
        "analysis": analysis
    }



@router.post("/analyze-job/")
async def analyze_job(description: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)):
    if not description or not description.strip():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Job description must not be empty.")
    
    try:
        result = analyze_job_description(description)
        
        # Save to database
        parsed_json = json.dumps(result)
        
        new_job_description = JobDescription(
            title=result.get('title', ''),
            content=description,
            parsed_data=parsed_json
        )
        
        db.add(new_job_description)
        await db.commit()
        await db.refresh(new_job_description)
        
        return {
            "id": new_job_description.id,
            "title": new_job_description.title,
            "analysis": result
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to analyze job description: {str(e)}")


class MatchRequest(BaseModel):
    resume: dict
    job: dict

@router.get("/test-match")
async def test_match():
    """Simple test endpoint to check if matching service is working"""
    try:
        # Test with dummy data
        test_resume = {
            "skills": ["Python", "JavaScript"],
            "experience": [{"bullets": ["Developed web applications"]}]
        }
        test_job = {
            "skills": ["Python", "React"],
            "description": "Software developer position"
        }
        
        result = match_resume_to_job(test_resume, test_job)
        return {"status": "success", "test_result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@router.post("/match")
async def match_resume_job(data: MatchRequest):
    if not data.resume or not data.job:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Resume and job data must be provided.")
    
    print(f"🔍 Received match request - Resume keys: {list(data.resume.keys()) if data.resume else 'None'}")
    print(f"🔍 Received match request - Job keys: {list(data.job.keys()) if data.job else 'None'}")
    
    try:
        result = match_resume_to_job(data.resume, data.job)
        print(f"✅ Match result: {result}")
        return {"status": "success", "match": result}
    except Exception as e:
        print(f"❌ Match error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to match resume to job: {str(e)}")