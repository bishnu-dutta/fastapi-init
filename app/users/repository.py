
import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.service import hash_password

from .model import User
from .request import CreateUserRequest, UpdateUserRequest


async def save_user_to_database(data: CreateUserRequest, otp_hash: str, otp_expiry: datetime, session: AsyncSession) -> User:
    user = User(
        username=data.username,
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
        otp_hash=otp_hash,
        otp_expiry=otp_expiry,
        otp_attempts=0,
        is_verified=False,
        organization_id=data.organization_id,
        role=data.role
    )
    session.add(user)
    await session.commit()
    await session.refresh(user, attribute_names=["organization", "posts"])

    return user

    
async def update_user_otp(user: User,otp_hash: str,otp_expiry: datetime,session: AsyncSession,) -> User:
    user.otp_hash = otp_hash
    user.otp_expiry = otp_expiry
    user.otp_attempts = 0
    await session.commit()
    await session.refresh(user, attribute_names=["organization", "posts"])
    return user


async def find_user_by_email(email:EmailStr , session: AsyncSession) -> User | None:
    query = select(User).where(func.lower(User.email) == email.lower())
    result = await session.execute(query)
    return result.scalars().first()


async def all_users(session: AsyncSession, org_id: uuid.UUID | None = None) -> list[User]:
    query = select(User)
    if org_id:
        query = query.where(User.organization_id == org_id)
    result = await session.execute(query)
    return list(result.scalars().all())


async def find_user_by_id(id: int, session: AsyncSession, org_id:uuid.UUID | None = None) -> User | None:
    query = select(User).where(User.id == id)
    if org_id:
        query = query.where(User.organization_id == org_id)
    result = await session.execute(query)
    return result.scalars().first()


async def delete_user_by_id(id: int, session: AsyncSession, org_id:uuid.UUID | None = None) -> User | None:
    user = await find_user_by_id(id, session, org_id)
    if user:
        await session.delete(user)
        await session.commit()
    return user


async def update_user_by_id(id: int, data: UpdateUserRequest, session: AsyncSession, org_id:uuid.UUID | None = None) -> User | None:
    user = await find_user_by_id(id, session, org_id)
    if user:
        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            ''' if find_user_by_email(): return email already used  '''
            user.email = data.email.lower()
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        await session.commit()
        await session.refresh(user, attribute_names=["organization", "posts"])
    return user

async def update_password_by_email(user_mail: EmailStr, password: str, session: AsyncSession) -> User | None:
    user_mail.hashed_password = hash_password(password)
    await session.commit()
    await session.refresh(user_mail, attribute_names=["organization", "posts"])
    return user_mail


    
