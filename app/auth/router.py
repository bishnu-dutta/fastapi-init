from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.users.response import PrivateUserResponse
from .model import Token
from .service import create_token, oauth2_scheme, get_current_auth_user
from app.core.database import async_session_dep


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    # OAuth2PasswordRequstForm -> parses login form data and requires username.
    # oauth2_scheme use this POST /token to return token value from token db
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = async_session_dep,
):
    return await create_token(form_data, session)


@router.get("/me", response_model=PrivateUserResponse)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = async_session_dep,
):  
    return await get_current_auth_user(token, session)

