from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from demo_service.models.base import Base, PkModel, UTCDateTime

from sqlalchemy import ForeignKey


class User(PkModel):
    __tablename__ = "user"

    external_id: Mapped[str] = mapped_column(index=True, unique=True)
    name: Mapped[Optional[str]]
    email: Mapped[str]

    sessions: Mapped[list["Session"]] = relationship(back_populates="user")


class Session(Base):
    __tablename__ = "session"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    secret_hash: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created: Mapped[datetime] = mapped_column(UTCDateTime())
    last_active: Mapped[datetime] = mapped_column(UTCDateTime())

    user: Mapped[User] = relationship(back_populates="sessions")