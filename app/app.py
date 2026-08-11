from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.users.repository import create_user_db_and_tables
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_user_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)