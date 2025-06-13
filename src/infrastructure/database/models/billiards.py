from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression
from sqlalchemy_utils import EmailType, PhoneNumberType

from core.enums import TableType
from infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from infrastructure.database.models.addresses import Address
    from infrastructure.database.models.bookings import BookingTable
    from infrastructure.database.models.schedules import ClubSchedule


class BilliardClub(Base):
    __tablename__ = "billiard_clubs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    address_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("addresses.id"),
        unique=True,
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=False)
    phone: Mapped[PhoneNumberType] = mapped_column(PhoneNumberType(region="BY"), nullable=True)
    email: Mapped[EmailType] = mapped_column(EmailType, nullable=True)
    photo: Mapped[str] = mapped_column(String, nullable=True)

    billiard_tables: Mapped[list["BilliardTable"]] = relationship(back_populates="billibard_club")
    schedules: Mapped[list["ClubSchedule"]] = relationship(
        "ClubSchedule", back_populates="billiard_club", cascade="all, delete-orphan"
    )
    address: Mapped["Address"] = relationship(back_populates="billiard_clubs")


class BilliardTable(Base):
    __tablename__ = "billiard_tables"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    billiard_club_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("billiard_clubs.id"), nullable=False
    )
    table_type: Mapped[TableType] = mapped_column(
        PgEnum(TableType), nullable=False, comment="Тип стола"
    )
    price_per_hour: Mapped[Numeric] = mapped_column(
        Numeric(precision=5, scale=2, decimal_return_scale=2), nullable=True, comment="Цена в час"
    )
    in_service: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=expression.false(),
        nullable=False,
        comment="Находится ли стол в техническом обслуживании",
    )

    billibard_club: Mapped[BilliardClub] = relationship(back_populates="billiard_tables")
    bookings: Mapped[list["BookingTable"]] = relationship(back_populates="billiard_table")
