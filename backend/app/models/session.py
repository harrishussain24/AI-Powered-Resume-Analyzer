import os
import ssl
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.db import Base
from contextlib import asynccontextmanager
print("DATABASE_URL env var is:", os.getenv("DATABASE_URL"))
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create SSL context for Neon DB connection
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context}  # Pass SSL context here for secure connection
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_db_context():
    async with AsyncSessionLocal() as session:
        yield session

async def get_db():
    async with get_db_context() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
