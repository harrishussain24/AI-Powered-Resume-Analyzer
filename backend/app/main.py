from fastapi import FastAPI
from api.routes import router
from models.session import init_db
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(router)
