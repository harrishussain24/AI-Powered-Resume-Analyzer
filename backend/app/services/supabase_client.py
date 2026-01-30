from supabase import create_client
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def upload_resume_to_supabase(file):
    contents = await file.read()
    unique_id = str(uuid.uuid4())
    file_name = f"{unique_id}_{file.filename}"

    response = supabase.storage.from_('resumes').upload(
        file_name,
        contents,
        {"content-type": file.content_type},
    )

    # ✅ CORRECT check (Supabase SDK v2)
    if response.error:
        raise Exception(f"Supabase upload error: {response.error}")

    public_url = supabase.storage.from_('resumes').get_public_url(file_name)
    return public_url
