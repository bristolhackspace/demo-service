from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from demo_service.models.base import Base, PkModel, UTCDateTime

from sqlalchemy import ForeignKey


class Member(Base):
    __tablename__ = "member"

    ext_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[Optional[str]]
    email: Mapped[str]

    sessions: Mapped[list["Session"]] = relationship(back_populates="member")


class Session(Base):
    __tablename__ = "session"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    secret_hash: Mapped[str]
    member_id: Mapped[int] = mapped_column(ForeignKey("member.ext_id"))
    created: Mapped[datetime] = mapped_column(UTCDateTime())
    last_active: Mapped[datetime] = mapped_column(UTCDateTime())

    member: Mapped[Member] = relationship(back_populates="sessions")