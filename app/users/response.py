from pydantic import BaseModel, ConfigDict, EmailStr


class PublicUserResponse(BaseModel):
    id: int
    username: str
    

    model_config = ConfigDict(from_attributes=True)

class PrivateUserResponse(PublicUserResponse):
    email: EmailStr
    