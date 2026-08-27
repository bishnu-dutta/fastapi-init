from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.auth.router import router as auth_router
from app.core.database import async_engine
from app.core.exceptions import register_exception_handlers
from app.middleware import register_middleware
from app.posts.router import router as posts_router
from app.users.router import router as users_router
import app.organizations.model 


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(posts_router)

register_middleware(app)
register_exception_handlers(app)
