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

    # Upload to Supabase Storage (bucket name: "resumes")
    response = supabase.storage.from_("resumes").upload(
        file_name, contents, {"content-type": file.content_type}
    )

    # Check for failure
    if response.get("error"):
        raise Exception(f"Upload failed: {response['error']['message']}")

    # Get the public URL
    public_url_response = supabase.storage.from_("resumes").get_public_url(file_name)
    if public_url_response.get("error"):
        raise Exception(f"Failed to get public URL: {public_url_response['error']['message']}")

    return public_url_response["data"]["publicUrl"]
