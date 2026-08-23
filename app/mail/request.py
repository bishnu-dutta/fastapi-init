from pydantic import EmailStr, BaseModel, Field

class EmailModel(BaseModel):
    addresses: list[EmailStr]

