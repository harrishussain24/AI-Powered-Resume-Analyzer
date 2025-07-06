import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from models.db import Base
from contextlib import asynccontextmanager

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ✅ KEEP this
@asynccontextmanager
async def get_db_context():
    async with AsyncSessionLocal() as session:
        yield session

# ✅ ADD this: actual FastAPI-compatible dependency
async def get_db():
    async with get_db_context() as session:
        yield session

# ✅ KEEP this too
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
