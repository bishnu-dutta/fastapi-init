
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.repository import find_by_username
from app.core.config import settings
from app.core.database import async_session_dep
from app.users import model


from .response import Token

password_hash = PasswordHash.recommended()

# tokenURL has to match login endpoint, OAuth2PasswordBearer extract token from header. Also enable authorization block in docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def hash_password(password:str) -> str:
    return password_hash.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(data:dict, expire_delta:timedelta | None = None) -> str:
    to_encode = data.copy()
    if expire_delta:
        expire_time = datetime.now(UTC) + expire_delta
    else:
        expire_time = datetime.now(UTC) + timedelta(minutes = settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key.get_secret_value(), 
        algorithm=settings.algorithm
        )   
    return encoded_jwt
    
# verify userID in sub field 
def verify_access_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key.get_secret_value(), 
            algorithms=[settings.algorithm],
            options = {"require": ["exp", "sub"]}
        )
    except jwt.InvalidTokenError:
        return None
    else:
        return payload.get("sub")

async def get_current_user(
    token:str = Depends(oauth2_scheme), 
    session: AsyncSession = async_session_dep):
    
    # decode and returns 
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id_int = int(user_id)
    except(TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = await session.execute(
        select(model.User).where(model.User.id == user_id_int)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_token(
    form_data,
    session: AsyncSession = async_session_dep
    ):
    user = await find_by_username(form_data.username, session)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please verify your email before logging in.",
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expire_delta=access_token_expires,
    )

    # saving the token so created in Token schema
    return Token(
        access_token=access_token,
        token_type="bearer",
    ) 


async def get_current_auth_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = async_session_dep
    ):
    
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )   
    try:
        # from verify_access_token it returns "sub" payload i.e user_id in string format 
        # But sub is conventionally treated as a string identifier. Some JWT/auth libraries or integrations may expect it to be a string.
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )   

    # db query need to resolve it later
    result = await session.execute(
        select(model.User).where(model.User.id == user_id_int)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )   
    
    return user
    




