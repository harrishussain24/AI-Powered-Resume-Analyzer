from fastapi import FastAPI
from app.api.routes import router
from app.models.session import init_db
from fastapi.middleware.cors import CORSMiddleware
import os

# Only load dotenv locally if you want
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

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)
