from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.users.model import User



async def find_by_username(username: str, session: AsyncSession) -> User | None:
    results = await session.execute(
        select(User).where(
            func.lower(User.username) == func.lower(username)
        )
    )
    return results.scalars().first()