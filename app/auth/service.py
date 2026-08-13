
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import model
from app.users.router import async_session_dep

from .model import Settings

settings = Settings()

password_hash = PasswordHash.recommend()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/token')

def hash_password(password:str) -> str:
    return password_hash.hash(password)

def verify_password(password:str, hashed_password:str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_data(data:dict, expire_delta:timedelta | None = None) -> str:
    to_encode = data.copy()
    if expire_delta:
        expire_time = datetime.now(timezone.utc) + expire_delta
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes = settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm)
    return encoded_jwt
    
def verify_access_token(token: str) -> bool:
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
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
        Select(model.User).where(model.User.id == user_id_int)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

