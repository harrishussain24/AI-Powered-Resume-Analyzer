from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(SUPABASE_URL)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_resume_to_supabase(file):
    contents = await file.read()
    file_name = file.filename

    # Upload to Supabase Storage (bucket name: "resumes")
    response = supabase.storage.from_("resumes").upload(file_name, contents, {"content-type": file.content_type})

    if response.error:
        raise Exception(str(response.error))

    # Get the public URL
    public_url = supabase.storage.from_("resumes").get_public_url(file_name)
    return public_url