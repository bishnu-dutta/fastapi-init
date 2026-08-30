import uuid
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.organizations.model import Organization
    from app.posts.model import Post
    


class UserRole(StrEnum):
    SUPER_ADMIN = "super_admin"
    ORG_ADMIN = "org_admin"
    USER = "user"



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

    role: Mapped[UserRole] = mapped_column(String, index=True, default=UserRole.USER, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.uid"), nullable=False)

    organization: Mapped[Organization] = relationship("Organization", back_populates="user_org", lazy ="selectin")
    
    posts : Mapped[list[Post]] = relationship("Post", back_populates="owner_id", cascade="all, delete-orphan", lazy ="selectin")
    
    @property
    def organization_name(self) -> str | None:
        return self.organization.name if self.organization else None
    
    @property
    def all_posts(self) -> list[Post]:
        return self.posts