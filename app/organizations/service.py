from app.organizations.repository import admin_save_post_for_user_to_database
from app.users.repository import find_user_by_id
from app.posts.request import CreatePostRequest
from app.organizations.repository import admin_delete_post_by_id_from_database
from app.organizations.repository import admin_update_post_by_id_in_database
from app.posts.request import UpdatePostRequest
from .repository import admin_get_user_post_by_id_from_database
from app.posts.repository import get_all_post_by_user_id_from_database

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import User
from app.users.repository import delete_user_by_id, update_user_by_id
from app.users.request import (
    CreateUserRequest,
    UpdateUserRequest,
)

from app.organizations.request import AdminCreateUserRequest
from app.users.service import create_user

# ------ USER ------

async def admin_add_user(data: AdminCreateUserRequest, session: AsyncSession, admin_user: User):
    user_data = CreateUserRequest(
        username=data.username,
        email=data.email,
        password=data.password,
        organization_id=admin_user.organization_id,
        role=data.role
    )
    return await create_user(user_data, session)

async def admin_update_user_by_id(id: int, data: UpdateUserRequest, admin_user: User, session: AsyncSession):
    user = await update_user_by_id(id, data, session, admin_user.organization_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def admin_delete_user_by_id(id: int, admin_user: User, session: AsyncSession):
    if admin_user.id == id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Use self-delete endpoint to delete your own account")
        
    user = await delete_user_by_id(id, session, org_id=admin_user.organization_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in your organization")
    return user


# ------ POST ------
async def admin_get_all_posts_of_user(owner_id:int, current_user: User, session: AsyncSession):
    posts = await get_all_post_by_user_id_from_database(user_id=owner_id, session=session, org_id=current_user.organization_id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found in your organization")
    return posts

async def admin_create_post_for_user(user_id: int,data: CreatePostRequest,admin_user: User,session: AsyncSession):
    user = await find_user_by_id(user_id, session, org_id=admin_user.organization_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in your organization"
        )
    return await admin_save_post_for_user_to_database(data, user_id=user.id, session=session)


async def admin_get_posts_by_id_of_user(owner_id:int,post_id:int,current_user: User, session: AsyncSession):
    posts = await admin_get_user_post_by_id_from_database(user_id=owner_id,post_id=post_id, session=session, org_id=current_user.organization_id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found in your organization")
    return posts

async def admin_update_post_by_id_of_user(owner_id:int, post_id:int, data: UpdatePostRequest, current_user: User, session: AsyncSession):
    posts = await admin_update_post_by_id_in_database(user_id=owner_id,post_id=post_id, data=data, session=session, org_id=current_user.organization_id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found in your organization")
    return posts

async def admin_delete_post_by_id_of_user(owner_id:int,post_id:int,current_user: User, session: AsyncSession):
    posts = await admin_delete_post_by_id_from_database(user_id=owner_id,post_id=post_id, session=session, org_id=current_user.organization_id)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts not found in your organization")
    return posts

