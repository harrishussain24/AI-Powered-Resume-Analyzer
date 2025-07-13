from fastapi import FastAPI
from app.api.routes import router
from app.models.session import init_db
from fastapi.middleware.cors import CORSMiddleware
import os

# Only load dotenv locally
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/init")
async def manual_init():
    await init_db()
    return {"message": "DB initialized"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(router)
