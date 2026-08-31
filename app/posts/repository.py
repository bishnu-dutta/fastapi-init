import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.users.model import User

from .model import Post
from .request import CreatePostRequest, UpdatePostRequest


async def save_post_to_database(data: CreatePostRequest, current_user_id: int, session: AsyncSession):
    post = Post(
        user_id=current_user_id,
        title=data.title,
        content=data.content,
        created_at=datetime.now(UTC),
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def get_all_posts_from_database(session: AsyncSession, org_id: uuid.UUID | None = None) -> list[Post]:
    result = select(Post).options(joinedload(Post.owner_id))
    if org_id:
        result = result.join(User, Post.user_id == User.id).where(User.organization_id == org_id)
    result = await session.execute(result)
    return list(result.scalars().all())

async def get_all_post_by_user_id_from_database(user_id: int, session: AsyncSession, org_id: uuid.UUID | None = None) -> list[Post]:
    result = select(Post).options(joinedload(Post.owner_id)).where(Post.user_id == user_id)
    if org_id:
        result = result.join(User, Post.user_id == User.id).where(User.organization_id == org_id)
    result = await session.execute(result)
    return list(result.scalars().all())

async def get_post_by_id_from_database(id: int, session: AsyncSession, org_id: uuid.UUID | None = None) -> Post | None:
    result = select(Post).options(joinedload(Post.owner_id)).where(Post.id == id)
    if org_id:
        result = result.join(User, Post.user_id == User.id).where(User.organization_id == org_id)
    result = await session.execute(result)
    return result.scalars().first()

async def update_post_by_id_in_database(id: int, data: UpdatePostRequest, session: AsyncSession, org_id: uuid.UUID | None = None) -> Post | None:
    post = await get_post_by_id_from_database(id, session, org_id)
    if post:
        if data.title is not None:
            post.title = data.title
        if data.content is not None:
            post.content = data.content
        post.updated_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(post, attribute_names=["owner_id"])
    return post

async def delete_post_by_id_from_database(id: int, session: AsyncSession, org_id: uuid.UUID | None = None) -> Post | None:
    post = await get_post_by_id_from_database(id, session, org_id)
    if post:
        await session.delete(post)
        await session.commit()
    return post
