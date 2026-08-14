import os
from collections.abc import AsyncGenerator
from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from .model import Base


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set in .env")


# creating async engine
async_engine = create_async_engine(DATABASE_URL, echo=False)

# creating session factory
async_session = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession, autocommit=False, autoflush=False)

# creating actual tables, base
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# creating a local session for each request
async def async_session_local() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async_session_dep = Depends(async_session_local)