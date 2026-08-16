from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.users.router import router as users_router
from app.users.helpers import create_tables
from app.auth.router import router as auth_router
from app.posts.router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(posts_router)

