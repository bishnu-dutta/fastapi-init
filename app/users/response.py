from pydantic import BaseModel, ConfigDict, EmailStr


class PublicUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    
class PrivateUserResponse(PublicUserResponse):
    email: EmailStr


    