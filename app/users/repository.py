import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .model import Base, User
from .request import CreateUserRequest, UpdateUserRequest

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set in .env")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_user_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session

async_session_dep = Depends(get_async_session)


async def find_user_by_email(email: str, session:AsyncSession=async_session_dep):
    
    user = session.execute(select(User).where(User.email == email)).scalars().first()
    await session.close()
    return user

async def save_user_to_database(data: CreateUserRequest,session:AsyncSession=async_session_dep):
    user = User(
        username=data.username,
        email=data.email,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    await session.close()
    return user

async def all_users(session:AsyncSession=async_session_dep):
    users = session.execute(select(User)).scalars().all()
    await session.close()
    return users

async def find_user_by_id(id: int, session:AsyncSession=async_session_dep):
    user = session.execute(select(User).where(User.id == id)).scalars().first()
    await session.close()
    return user 


async def delete_user_by_id(id: int, session:AsyncSession=async_session_dep):
    user = session.execute(select(User).where(User.id == id)).scalars().first()
    await session.delete(user)
    await session.commit()
    await session.close()
    return user

async def update_user_by_id(id: int, data: UpdateUserRequest, session:AsyncSession=async_session_dep):
    user = session.execute(select(User).where(User.id == id)).scalars().first()
    if user:
        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            user.email = data.email
    await session.close()
    return user