from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Form, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Post, User, create_db_and_tables, get_async_session
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users

# Module-level dependencies to avoid calling Depends in default arguments
async_session_dep = Depends(get_async_session)
current_user_dep = Depends(current_active_user)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.post("/uploadposts")
async def upload_posts(
    title: str = Form(...),
    content: str = Form(...),
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


@app.get("/feed")
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


@app.delete("/posts/{id}")
async def delete_post(
    id: int,
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
