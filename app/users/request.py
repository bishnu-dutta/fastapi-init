
from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str 

class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")

class ResendOTPRequest(BaseModel):
    email: EmailStr