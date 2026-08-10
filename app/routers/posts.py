import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Post, User, get_async_session
from app.schemas import FeedResponse, MessageResponse, PostResponse
from app.users import current_active_user

router = APIRouter(tags=["posts"])

async_session_dep = Depends(get_async_session)
current_user_dep = Depends(current_active_user)

# Module-level constant for path parameter to avoid function call in default
POST_DELETE_ID = Path(
    ..., 
    description="The unique UUID of the post to delete"
)




@router.post(
    "/uploadposts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new post",
    description="Creates and saves a new post authored by the currently authenticated user.",
)
async def upload_posts(
    title: str = Form(
        ...,
        description="The title of the post to upload",
        examples=["My First Post"],
    ),
    content: str = Form(
        ...,
        description="The text content body of the post",
        examples=["Hello world! This is my post content."],
    ),
    user: User = current_user_dep,
    session: AsyncSession = async_session_dep,
):
    post = Post(
        user_id=user.id,
        title=title,
        content=content,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.get(
    "/feed",
    response_model=FeedResponse,
    summary="Get user posts feed",
    description="Retrieves all posts sorted by creation date in descending order, marked with ownership flags for the requesting user.",
)
async def get_feed(
    session: AsyncSession = async_session_dep,
    user: User = current_user_dep,
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for i in posts:
        posts_data.append(
            {
                "id": i.id,
                "user_id": i.user_id,
                "title": i.title,
                "content": i.content,
                "created_at": i.created_at,
                "is_owner": i.user_id == user.id,
            }
        )
    return {"posts": posts_data}


@router.delete(
    "/posts/{id}",
    response_model=MessageResponse,
    summary="Delete a post",
    description="Deletes a post by its unique UUID. Only the author of the post is permitted to delete it.",
    responses={
        404: {"model": MessageResponse, "description": "Post not found"},
        403: {"model": MessageResponse, "description": "Permission denied - post belongs to another user"},
    },
)


async def delete_post(
    id: uuid.UUID = POST_DELETE_ID,
    session: AsyncSession = async_session_dep,
    user: User = current_user_dep,
):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this post"
        )
    await session.delete(post)
    await session.commit()
    return {"detail": "Post deleted"}
