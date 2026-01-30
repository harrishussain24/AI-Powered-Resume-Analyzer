from supabase import create_client
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def upload_resume_to_supabase(file):
    try:
        contents = await file.read()
        unique_id = str(uuid.uuid4())
        file_name = f"{unique_id}_{file.filename}"

        # Upload (will raise exception if RLS or auth fails)
        upload_response = supabase.storage.from_(SUPABASE_BUCKET).upload(
            file_name,
            contents,
            file_options={"content-type": file.content_type},
        )

        # Build public URL (bucket must be public)
        public_url = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(file_name)

        return public_url

    except Exception as e:
        print("❌ Supabase upload error:", str(e))
        raise
