from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.helpers import CurrentUser

from .repository import (
    all_users,
    delete_user_by_id,
    find_user_by_email,
    find_user_by_id,
    save_user_to_database,
    update_user_by_id,
)
from .request import CreateUserRequest, UpdateUserRequest


async def create_user(data: CreateUserRequest, session: AsyncSession):
    existing_user = await find_user_by_email(data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return await save_user_to_database(data, session)


async def get_all_users(session: AsyncSession):
    users = await all_users(session)
    return users


async def get_user_by_id(id: int, session: AsyncSession):
    user = await find_user_by_id(id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def delete_user(current_user: CurrentUser,session: AsyncSession):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user",
        )
    user = await delete_user_by_id(current_user.id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def update_user(current_user: CurrentUser, data: UpdateUserRequest, session: AsyncSession):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user",
        )
    user = await update_user_by_id(current_user.id, data, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

