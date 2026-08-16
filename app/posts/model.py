from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, DeclarativeBase
from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.users.model import Base    

if TYPE_CHECKING:
    from app.users.model import User

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now())

    owner_id : Mapped["User"] = relationship("User", back_populates="posts")

    @property
    def author(self) -> str | None:
        return self.owner_id.email if self.owner_id else None 
    