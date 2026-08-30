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