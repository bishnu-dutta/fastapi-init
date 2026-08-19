from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.posts.model import Post
    

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    posts : Mapped[list[Post]] = relationship("Post", back_populates="owner_id", cascade="all, delete-orphan")
    