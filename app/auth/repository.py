from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.model import User


async def find_by_username(username: str, session: AsyncSession) -> User | None:
    results = await session.execute(
        select(User).where(
            func.lower(User.username) == func.lower(username)
        )
    )
    return results.scalars().first()


async def find_by_email(email:str, session:AsyncSession) -> User | None:
    result = await session.execute(
        select(User).where(User.email == email)
    )
    return result.scalars().first()