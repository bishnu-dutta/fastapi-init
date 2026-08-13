from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Token(BaseModel):
    access_type: str
    token_type: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int = 60
    
