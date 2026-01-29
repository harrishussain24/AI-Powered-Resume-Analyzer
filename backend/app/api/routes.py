import json
from fastapi import APIRouter, UploadFile, File, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.resume_parser import extract_text_from_pdf, analyze_resume_text
from app.models.session import get_db
from app.models.db import Resume, JobDescription
from app.services.job_description_analyzer import analyze_job_description
from app.services.matcher import match_resume_to_job
from app.services.supabase_client import upload_resume_to_supabase
from pydantic import BaseModel
from pdfminer.pdfparser import PDFSyntaxError

router = APIRouter()


@router.post("/upload-resume/")
async def upload_resume(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
):
    print(f"🔹 Received file: {file.filename}")
    try:
        text = extract_text_from_pdf(file)
        print(f"🔹 Extracted text length: {len(text) if text else 0}")
    except PDFSyntaxError:
        raise HTTPException(
            status_code=400, detail="Invalid PDF file format."
        )
    except Exception as e:
        print(f"❌ PDF extraction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to read PDF file: {str(e)}")

    if not text or "No text found" in text:
        raise HTTPException(status_code=422, detail="No text found in PDF.")

    text = text.strip()
    if not text:
        raise HTTPException(status_code=422, detail="PDF contains no readable text.")

    analysis = analyze_resume_text(text)
    if not analysis:
        raise HTTPException(status_code=500, detail="Failed to analyze resume text.")

    # Upload to Supabase
    try:
        file_url = await upload_resume_to_supabase(file)
        print(f"🔹 Supabase file URL: {file_url}")
    except Exception as e:
        print(f"❌ Supabase upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload to Supabase: {str(e)}")

    parsed_json = json.dumps(analysis)

    try:
        new_resume = Resume(
            filename=file.filename,
            content=text,
            parsed_data=parsed_json,
            file_url=file_url,
        )
        db.add(new_resume)
        await db.commit()
        await db.refresh(new_resume)
        print(f"🔹 Resume saved to DB with ID: {new_resume.id}")
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    file.file.close()

    return {
        "id": new_resume.id,
        "filename": new_resume.filename,
        "file_url": file_url,
        "analysis": analysis,
    }


@router.post("/analyze-job/")
async def analyze_job(
    description: str = Body(..., embed=True), db: AsyncSession = Depends(get_db)
):
    if not description or not description.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Job description must not be empty.",
        )

    try:
        result = analyze_job_description(description)
        parsed_json = json.dumps(result)

        new_job_description = JobDescription(
            title=result.get("title", ""),
            content=description,
            parsed_data=parsed_json,
        )

        db.add(new_job_description)
        await db.commit()
        await db.refresh(new_job_description)

        return {
            "id": new_job_description.id,
            "title": new_job_description.title,
            "analysis": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze job description: {str(e)}",
        )


class MatchRequest(BaseModel):
    resume: dict
    job: dict


@router.get("/test-match")
async def test_match():
    """Simple test endpoint to check if matching service is working"""
    try:
        test_resume = {
            "skills": ["Python", "JavaScript"],
            "experience": [{"bullets": ["Developed web applications"]}],
        }
        test_job = {
            "skills": ["Python", "React"],
            "description": "Software developer position",
        }

        result = match_resume_to_job(test_resume, test_job)
        return {"status": "success", "test_result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@router.post("/match")
async def match_resume_job(data: MatchRequest):
    if not data.resume or not data.job:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Resume and job data must be provided.",
        )

    print(
        f"🔍 Received match request - Resume keys: "
        f"{list(data.resume.keys()) if data.resume else 'None'}"
    )
    print(
        f"🔍 Received match request - Job keys: "
        f"{list(data.job.keys()) if data.job else 'None'}"
    )

    try:
        result = match_resume_to_job(data.resume, data.job)
        print(f"✅ Match result: {result}")
        return {"status": "success", "match": result}
    except Exception as e:
        print(f"❌ Match error: {str(e)}")
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to match resume to job: {str(e)}",
        )
