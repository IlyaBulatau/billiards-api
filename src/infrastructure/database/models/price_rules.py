from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Time
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enums import TableType
from infrastructure.database.models.base import Base


if TYPE_CHECKING:
    from infrastructure.database.models.billiards import BilliardClub


class PriceRule(Base):
    __tablename__ = "price_rules"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    billiard_club_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("billiard_clubs.id"), nullable=False
    )
    table_type: Mapped[TableType] = mapped_column(
        PgEnum(TableType),
        nullable=True,
        comment="Тип стола по которому действует цена, если null действует для всех столов",
    )
    days_of_week: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        nullable=False,
        default=[],
        comment="Дни недели когда действует цена, если пустой массив - день недели не влияет на цену",
    )
    start_time: Mapped[Time] = mapped_column(Time(timezone=True), nullable=True)
    end_time: Mapped[Time] = mapped_column(Time(timezone=True), nullable=True)
    price_per_hour: Mapped[Numeric] = mapped_column(
        Numeric(precision=5, scale=2, decimal_return_scale=2), nullable=True, comment="Цена в час"
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(), onupdate=datetime.now()
    )

    billibard_club: Mapped["BilliardClub"] = relationship(back_populates="price_rules")
