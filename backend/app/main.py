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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://ai-powered-resume-analyzer-u0hx.onrender.com",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/init")
async def manual_init():
    try:
        await init_db()
        return {"message": "DB initialized"}
    except Exception as e:
        return {"message": f"DB init failed: {str(e)}"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/test")
async def test_endpoint():
    return {"message": "Backend is working!", "timestamp": "2024-01-01"}

app.include_router(router)
