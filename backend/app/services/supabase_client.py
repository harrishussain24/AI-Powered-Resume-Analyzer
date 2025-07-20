from supabase import create_client
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(SUPABASE_URL)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_resume_to_supabase(file):
    contents = await file.read()
    unique_id = str(uuid.uuid4())
    file_name = f"{unique_id}_{file.filename}"

    # Upload to Supabase Storage (bucket name: "resumes")
    response = supabase.storage.from_("resumes").upload(file_name, contents, {"content-type": file.content_type})

    # Check for failure using status_code or raise a generic error if not successful
    if hasattr(response, 'status_code') and response.status_code not in (200, 201):
        raise Exception(f"Upload failed: {getattr(response, 'data', response)}")
    if hasattr(response, 'error_message') and response.error_message:
        raise Exception(f"Upload failed: {response.error_message}")

    # Get the public URL
    public_url = supabase.storage.from_("resumes").get_public_url(file_name)
    return public_url