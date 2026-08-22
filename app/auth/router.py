from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_dep
from app.users.response import PrivateUserResponse

from .response import Token
from .service import create_token, get_current_auth_user, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token, include_in_schema=False)
async def login_for_access_token(
    # OAuth2PasswordRequstForm -> parses login form data and requires username.
    # oauth2_scheme use this POST /token to return token value from token model
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = async_session_dep,
):
    return await create_token(form_data, session)


@router.get("/me", 
            response_model=PrivateUserResponse, 
            status_code=status.HTTP_200_OK, 
            summary="Get current user", 
            description="Need user authentication to get current user data"
            )
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = async_session_dep,
):  
    return await get_current_auth_user(token, session)

