from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .request import CreateUserRequest, UpdateUserRequest
from .response import UserResponse
from .service import (
    create_user,
    delete_user,
    get_all_users,
    get_async_session,
    get_user_by_id,
    update_user,
)

# creating a dependency for the session
async_session_dep = Depends(get_async_session)


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", response_model=UserResponse)
async def create_user_api(
    data: CreateUserRequest,
    session: AsyncSession = async_session_dep,
):
    return await create_user(data, session)


@router.get("/all", response_model=list[UserResponse])
async def get_all_users_api(
    session: AsyncSession = async_session_dep,
):
    return await get_all_users(session)


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id_api(
    id: int,
    session: AsyncSession = async_session_dep,
):
    return await get_user_by_id(id, session)


@router.delete("/{id}", response_model=UserResponse)
async def delete_user_api(
    id: int,
    session: AsyncSession = async_session_dep,
):
    return await delete_user(id, session)


@router.put("/{id}", response_model=UserResponse)
async def update_user_api(
    id: int,
    data: UpdateUserRequest,
    session: AsyncSession = async_session_dep,
):
    return await update_user(id, data, session)