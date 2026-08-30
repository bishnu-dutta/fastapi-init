from pydantic import BaseModel

from app.users.model import UserRole


class AdminCreateUserRequest(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.USER
