import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql.annotation import Annotated

from app.auth.service import get_current_user
from app.users.model import Base, User

from .repository import (
    all_users,
    delete_user_by_id,
    find_user_by_email,
    find_user_by_id,
    save_user_to_database,
    update_user_by_id,
)
from .request import CreateUserRequest, UpdateUserRequest


currentUser = Annotated[User, Depends(get_current_user)]


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


async def create_user(data: CreateUserRequest, session: AsyncSession = async_session_dep):
    existing_user = await find_user_by_email(data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return await save_user_to_database(data, session)


async def get_all_users(session: AsyncSession = async_session_dep):
    users = await all_users(session)
    return users


async def get_user_by_id(id: int, 
current_user : currentUser,
session: AsyncSession = async_session_dep):
    user = await find_user_by_id(id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this user",
        )
    return user


async def delete_user(id: int, 
current_user : currentUser,
session: AsyncSession = async_session_dep):
    user = await delete_user_by_id(id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user",
        )

    return user


async def update_user(id: int, 
data: UpdateUserRequest, 
current_user : currentUser,
session: AsyncSession = async_session_dep):
    user = await update_user_by_id(id, data, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user",
        )
    return user

