from sqlalchemy.orm import Mapped
from typing import TYPE_CHECKING
from typing import List
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from app.posts.model import Post
    

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    posts : Mapped[List["Post"]] = relationship("Post", back_populates="owner")
    