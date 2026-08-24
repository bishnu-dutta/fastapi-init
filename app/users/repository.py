
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from app.auth.service import hash_password
from app.utils.mail import get_otp_expiry, generate_otp

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
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

    
async def update_user_otp(user: User,otp_hash: str,otp_expiry: datetime,session: AsyncSession,) -> User:
    user.otp_hash = otp_hash
    user.otp_expiry = otp_expiry
    user.otp_attempts = 0
    await session.commit()
    await session.refresh(user)
    return user


async def find_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(func.lower(User.email) == email.lower()))
    return result.scalars().first()


async def all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())


async def find_user_by_id(id: int, session: AsyncSession) -> User | None:
    result = await session.execute(select(User).where(User.id == id))
    return result.scalars().first()


async def delete_user_by_id(id: int, session: AsyncSession) -> User | None:
    user = await find_user_by_id(id, session)
    if user:
        await session.delete(user)
        await session.commit()
    return user


async def update_user_by_id(id: int, data: UpdateUserRequest, session: AsyncSession) -> User | None:
    user = await find_user_by_id(id, session)
    if user:
        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            ''' if find_user_by_email(): return email already used  '''
            user.email = data.email.lower()
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        await session.commit()
        await session.refresh(user)
    return user
