from fastapi import FastAPI
from api.routes import router
from models.session import init_db
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)
