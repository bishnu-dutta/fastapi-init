from app.users.service import verify_otp, resend_otp
from .request import OTPVerify, ResendOTPRequest
from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.helpers import CurrentUser
from app.core.database import async_session_dep

from .request import CreateUserRequest, UpdateUserRequest
from .response import PrivateUserResponse, PublicUserResponse
from .service import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/create", 
    response_model=PrivateUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create and saves a new user to database"
)
async def create_user_api(data: CreateUserRequest, session: AsyncSession = async_session_dep
):
    return await create_user(data, session)

@router.post("/mail/verify-otp", 
    status_code=status.HTTP_200_OK,
    summary="Verify OTP",
    description="Verify OTP of a user"
)
async def verify_otp_api(data: OTPVerify, session: AsyncSession = async_session_dep):
    return await verify_otp(data.email, data.otp, session)

@router.post("/mail/resend-otp", 
    status_code=status.HTTP_200_OK, 
    summary="Resend verification OTP",
    description="Resends a new 6-digit OTP to the user's email if not already verified.")
async def resend_otp_api(data: ResendOTPRequest, session: AsyncSession = async_session_dep):
    return await resend_otp(data.email, session)


@router.get("/all", 
    response_model=list[PublicUserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
    description="Get all list of users from database(only public accessible data)"
)
async def get_all_users_api(session: AsyncSession = async_session_dep):
    return await get_all_users(session)


@router.get("/{id}", 
    response_model=PublicUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a user by id",
    description="Get a user by id from database(only public accessible data)"
)
async def get_user_by_id_api(id: int, session: AsyncSession = async_session_dep):
    return await get_user_by_id(id, session)


@router.delete("/delete", 
    response_model=PrivateUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete current user",
    description="Delete current user data from database(only the current authorised user can delete itself)"
)
async def delete_user_api(current_user: CurrentUser, session: AsyncSession = async_session_dep):
    return await delete_user(current_user, session)


@router.put("/update", 
    response_model=PrivateUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update current user",
    description="Update current user data from database(only the current authorised user can update itself)"
)
async def update_user_api(data: UpdateUserRequest, current_user: CurrentUser, session: AsyncSession = async_session_dep):
    return await update_user(current_user, data, session)



