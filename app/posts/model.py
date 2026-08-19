from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.users.model import User

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    owner_id : Mapped[User] = relationship("User", back_populates="posts")

    @property
    def author(self) -> str | None:
        return self.owner_id.email if self.owner_id else None 
    