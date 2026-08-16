from app.posts.response import UpdatePrivatePostResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .request import CreatePostRequest, UpdatePostRequest
from .response import PrivatePostResponse, PublicPostResponse
from .service import (
    create_post,
    get_all_posts,
    get_all_posts_of_user,
    get_post_by_id,
    update_post_by_id,
    delete_post_by_id
)

from app.users.helpers import async_session_dep
from app.auth.helpers import CurrentUser


router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/create", response_model=PrivatePostResponse)
async def create_post_api(
    data: CreatePostRequest,
    current_user: CurrentUser,
    session: AsyncSession = async_session_dep
):
    return await create_post(data, current_user, session)

@router.get("/all", response_model=list[PublicPostResponse])
async def get_all_posts_api(
    session: AsyncSession = async_session_dep
):
    return await get_all_posts(session)

@router.get("/{id}", response_model=PrivatePostResponse)
async def get_post_by_id_api(
    id: int,
    current_user: CurrentUser,
    session: AsyncSession = async_session_dep
):
    return await get_post_by_id(id, current_user, session)

@router.get("/user/all", response_model=list[PrivatePostResponse])
async def get_all_posts_of_user_api(
    current_user: CurrentUser,
    session: AsyncSession = async_session_dep
):
    return await get_all_posts_of_user(current_user, session)

@router.put("/{id}", response_model=UpdatePrivatePostResponse)
async def update_post_by_id_api(
    id: int,
    data: UpdatePostRequest,
    current_user: CurrentUser,
    session: AsyncSession = async_session_dep
):
    return await update_post_by_id(id, current_user, data, session)

@router.delete("/{id}", response_model=PrivatePostResponse)
async def delete_post_by_id_api(
    id: int,
    current_user: CurrentUser,
    session: AsyncSession = async_session_dep
):
    return await delete_post_by_id(id, current_user, session)
