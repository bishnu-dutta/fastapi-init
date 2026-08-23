from sqlalchemy.orm import mapped_column
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import Mapped, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.posts.model import Post
    

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    otp_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    otp_expiry: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    otp_attempts: Mapped[int] = mapped_column(Integer, default=0)  # for rate limiting

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    posts : Mapped[list[Post]] = relationship("Post", back_populates="owner_id", cascade="all, delete-orphan")
    