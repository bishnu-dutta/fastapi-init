from email_validator import deliverability
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .request import CreatePostRequest, UpdatePostRequest
from .model import Post
from .repository import (
    save_post_to_database,
    get_all_posts_from_database,
    get_post_by_id_from_database,
    update_post_by_id_in_database,
    delete_post_by_id_from_database,
    get_all_post_by_user_id_from_database
)

from app.auth.helpers import CurrentUser

async def create_post(data: CreatePostRequest, current_user: CurrentUser, session: AsyncSession):
    return await save_post_to_database(data, current_user.id, session)
    

async def get_all_posts(session: AsyncSession):
    posts = await get_all_posts_from_database(session)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
        )
    return posts

async def get_all_posts_of_user(current_user: CurrentUser, session: AsyncSession):
    posts = await get_all_post_by_user_id_from_database(current_user.id, session)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found",
        )
    return posts

async def get_post_by_id(id: int, current_user: CurrentUser, session: AsyncSession):
    post = await get_post_by_id_from_database(id, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to get this post",
        )
    return post

async def update_post_by_id(id: int, current_user: CurrentUser, data: UpdatePostRequest, session: AsyncSession):
    post = await get_post_by_id_from_database(id, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this post",
        )
    post = await update_post_by_id_in_database(id, data, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post

async def delete_post_by_id(id: int, current_user: CurrentUser, session: AsyncSession):
    post = await get_post_by_id_from_database(id, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post",
        )
    post = await delete_post_by_id_from_database(id, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    return post