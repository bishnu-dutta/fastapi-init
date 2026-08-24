from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.helpers import CurrentUser

from datetime import datetime, UTC, timedelta

from app.auth.service import verify_password
from app.utils.mail import generate_otp, get_otp_expiry, mail

from fastapi_mail import MessageSchema, MessageType


from .repository import (
    all_users,
    delete_user_by_id,
    find_user_by_email,
    find_user_by_id,
    save_user_to_database,
    update_user_by_id,
    update_user_otp
)
from .request import CreateUserRequest, UpdateUserRequest


async def create_user(data: CreateUserRequest, session: AsyncSession):
    existing_user = await find_user_by_email(data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    p_otp, h_otp = generate_otp()
    otp_expiry = get_otp_expiry(minutes=10)
    user = await save_user_to_database(data, h_otp, otp_expiry, session)
    await send_otp_email(user.email, p_otp)
    return user


async def send_otp_email(recipient_email: str, otp: str, subject: str = "Verify your account"):
    
    html_content = f"""
    <h2>Account Verification</h2>
    <p>Your 6-digit verification code is:</p>
    <h1 style="letter-spacing: 4px; color: #2563eb;">{otp}</h1>
    <p>This code will expire in 10 minutes.</p>
    """
    message = MessageSchema(
        subject=subject,
        recipients=[recipient_email],
        body=html_content,
        subtype=MessageType.html,
    )
    await mail.send_message(message)

async def verify_otp(email:str,otp:str,session:AsyncSession):
    user = await find_user_by_email(email, session)
    if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
    if user.is_verified:
        return {"message": "Account is already verified"}

    if user.otp_attempts >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Please request a new OTP.",
        )

    if not user.otp_expiry or datetime.now(UTC) > user.otp_expiry.replace(tzinfo=UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new one.",
        )

    if not user.otp_hash or not verify_password(otp, user.otp_hash):
        user.otp_attempts += 1
        await session.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid OTP code. Remaining attempts: {5 - user.otp_attempts}",
        )

    user.is_verified = True
    user.otp_hash = None
    user.otp_expiry = None
    user.otp_attempts = 0
    await session.commit()
    return {"message": "Account verified successfully. You can now log in."}

async def resend_otp(email:str, session: AsyncSession):
    user = await find_user_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is already verified",
        )

    if user.otp_expiry:
        last_sent = user.otp_expiry.replace(tzinfo=UTC) - timedelta(minutes=10)
        if (datetime.now(UTC) - last_sent).total_seconds() < 60:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Please wait at least 60 seconds before requesting another OTP.",
            )
    # Generate new OTP & hash
    p_otp, h_otp = generate_otp()
    otp_expiry = get_otp_expiry(minutes=10)
    await update_user_otp(user,h_otp,otp_expiry,session)
    await send_otp_email(user.email,p_otp,"Your new verification code")
    return {"message": "A new verification code has been sent to your email."}



async def get_all_users(session: AsyncSession):
    users = await all_users(session)
    return users


async def get_user_by_id(id: int, session: AsyncSession):
    user = await find_user_by_id(id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def delete_user(current_user: CurrentUser,session: AsyncSession):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this user",
        )
    user = await delete_user_by_id(current_user.id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


async def update_user(current_user: CurrentUser, data: UpdateUserRequest, session: AsyncSession):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this user",
        )
    user = await update_user_by_id(current_user.id, data, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


