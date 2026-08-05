from fastapi import Query
from sqlalchemy import select
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, get_async_session, create_db_and_tables, User
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import shutil
import os 
import uuid 
import tempfile
from app.users import auth_backend, current_active_user, fastapi_users




@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),prefix="/auth",tags=["auth"]) 
app.include_router(fastapi_users.get_reset_password_router(),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead),prefix="/auth",tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),prefix="/users",tags=["users"])


@app.post("/uploadposts")
async def upload_posts(
    title: str = Form(...), 
    content: str = Form(...), 
    user: User = Depends(current_active_user),
    session:AsyncSession = Depends(get_async_session),
    ):
    post = Post(
    user_id = user.id,
    title= title, 
    content= content,
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post
    
@app.get("/feed")
async def get_feed(
    session:AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
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
                "is_owner": i.user_id == user.id
            }
        )
    return {"posts": posts_data}

@app.delete("/posts/{id}")
async def delete_post(
    id: int, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user)
    ):
    result = await session.execute(select(Post).where(Post.id == id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this post")
    await session.delete(post)
    await session.commit()
    return {"detail": "Post deleted"}
 

