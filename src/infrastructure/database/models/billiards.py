from typing import TYPE_CHECKING
import uuid

from sqlalchemy import Boolean, ForeignKey, Numeric, String, func, select
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship
from sqlalchemy.sql import expression
from sqlalchemy_utils import EmailType, PhoneNumberType

from core.enums import TableType
from infrastructure.database.models.base import Base
from infrastructure.database.models.price_rules import PriceRule


if TYPE_CHECKING:
    from infrastructure.database.models.addresses import Address
    from infrastructure.database.models.bookings import BookingTable
    from infrastructure.database.models.schedules import ClubSchedule


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

    billibard_club: Mapped["BilliardClub"] = relationship(back_populates="billiard_tables")
    bookings: Mapped[list["BookingTable"]] = relationship(back_populates="billiard_table")


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
    price_rules: Mapped[list["PriceRule"]] = relationship(
        back_populates="billibard_club",
        cascade="all, delete-orphan",
        order_by="PriceRule.updated_at",
    )
    schedules: Mapped[list["ClubSchedule"]] = relationship(
        "ClubSchedule",
        back_populates="billiard_club",
        cascade="all, delete-orphan",
        order_by="ClubSchedule.day_of_week",
    )
    address: Mapped["Address"] = relationship(back_populates="billiard_clubs")

    tables_count = column_property(
        select(func.count(BilliardTable.id))
        .where(BilliardTable.billiard_club_id == id)
        .correlate_except(BilliardTable)
        .scalar_subquery()
    )
    min_price_for_table = column_property(
        select(func.min(PriceRule.price_per_hour))
        .where(PriceRule.billiard_club_id == id)
        .correlate_except(PriceRule)
        .scalar_subquery()
    )

    @hybrid_property
    def has_russian(self):
        return any(table.table_type == TableType.RUSSIAN for table in self.billiard_tables)

    @has_russian.expression
    def has_russian(self):
        return (
            select(func.count(BilliardTable.id) > 0)
            .where(
                (BilliardTable.billiard_club_id == self.id)
                & (BilliardTable.table_type == TableType.RUSSIAN)
            )
            .label("has_russian")
        )

    @hybrid_property
    def has_pool(self):
        return any(table.table_type == TableType.POOL for table in self.billiard_tables)

    @has_pool.expression
    def has_pool(self):
        return (
            select(func.count(BilliardTable.id) > 0)
            .where(
                (BilliardTable.billiard_club_id == self.id)
                & (BilliardTable.table_type == TableType.POOL)
            )
            .label("has_pool")
        )

    @hybrid_property
    def has_snooker(self):
        """Свойство которое будет доступно в модели"""

        return any(table.table_type == TableType.SNOOKER for table in self.billiard_tables)

    @has_snooker.expression
    def has_snooker(self):
        """Свойство доступно при фильтрации в ORM"""

        return (
            select(func.count(BilliardTable.id) > 0)
            .where(
                (BilliardTable.billiard_club_id == self.id)
                & (BilliardTable.table_type == TableType.SNOOKER)
            )
            .label("has_snooker")
        )
