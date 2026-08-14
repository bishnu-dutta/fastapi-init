
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import User
from .request import CreateUserRequest, UpdateUserRequest
from app.auth.service import hash_password
from app.auth.helpers import CurrentUser



async def save_user_to_database(data: CreateUserRequest, session: AsyncSession) -> User:
    user = User(
        username=data.username,
        email=data.email.lower(),
        hashed_password=hash_password(data.password),
    )
    session.add(user)
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
            user.email = data.email
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        await session.commit()
        await session.refresh(user)
    return user
