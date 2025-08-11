from fastapi import FastAPI
from app.api.routes import router as core_router
from app.models.session import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.api.authroutes import router as auth_router
import os

# Only load dotenv locally
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv

    load_dotenv()
    print("SUPABASE_URL env var is:", os.getenv("SUPABASE_URL"))
    print("SUPABASE_KEY env var is:", os.getenv("SUPABASE_KEY"))
    print("DATABASE_URL env var is:", os.getenv("DATABASE_URL"))

app = FastAPI()

app.include_router(core_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://ai-powered-resume-analyzer-u0hx.onrender.com",
        "*",
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


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    return {"status": "ok"}


@app.get("/test")
async def test_endpoint():
    return {"message": "Backend is working!", "timestamp": "2024-01-01"}
