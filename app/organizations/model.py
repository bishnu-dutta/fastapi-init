
import uuid
from sqlalchemy import Uuid, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.users.model import User

from app.core.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    uid:Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, index=True, default = uuid.uuid4)
    name:Mapped[str] = mapped_column(String, index=True)

    user_org: Mapped[list[User]] = relationship("User", back_populates="organization")
