from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.sql.annotation import Annotated

from .repository import (
    all_users,
    delete_user_by_id,
    find_user_by_email,
    find_user_by_id,
    save_user_to_database,
    update_user_by_id,
)
from .request import CreateUserRequest, UpdateUserRequest

from .helpers import async_session_dep
from app.auth.helpers import CurrentUser





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


async def get_user_by_id(id: int, session: AsyncSession = async_session_dep):
    user = await find_user_by_id(id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def delete_user(id: int, current_user: CurrentUser,session: AsyncSession = async_session_dep):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user",
        )
    user = await delete_user_by_id(id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def update_user(id: int, current_user: CurrentUser, data: UpdateUserRequest, session: AsyncSession = async_session_dep):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user",
        )
    user = await update_user_by_id(id, data, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

