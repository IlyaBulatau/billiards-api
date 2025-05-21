import uuid

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base
from infrastructure.database.models.billiards import BilliardClub


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="Минск")
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    building: Mapped[str] = mapped_column(String(20), nullable=False)
    apartment: Mapped[str] = mapped_column(String(20), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)

    billiard_clubs: Mapped["BilliardClub"] = relationship(back_populates="address")
