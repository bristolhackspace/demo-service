from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from demo_service.models.base import Base, PkModel, LocalDateTime

from sqlalchemy import ForeignKey

class Onboarding(Base):
    __tablename__ = "onboarding"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(LocalDateTime())
    terms_agreed: Mapped[Optional[datetime]] = mapped_column(LocalDateTime())

    # Legal stuff (Based on GoCardless fields)
    given_name: Mapped[Optional[str]]
    family_name: Mapped[Optional[str]]
    address_line1: Mapped[Optional[str]]
    address_line2: Mapped[Optional[str]]
    address_town_city: Mapped[Optional[str]]
    address_country_code: Mapped[Optional[str]]
    address_postcode: Mapped[Optional[str]]
    address_state: Mapped[Optional[str]] # for US addresses

    # Account stuff
    display_name: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    username: Mapped[Optional[str]]


    gocardless_subscription_id: Mapped[Optional[str]]