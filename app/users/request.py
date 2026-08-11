
from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr


class UpdateUserRequest(BaseModel):
    username: str | None = None
    email: EmailStr | None = None