from datetime import datetime
import uuid

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import PhoneNumberType

from core.enums import BookingStatus
from infrastructure.database.models.base import Base
from infrastructure.database.models.billiards import BilliardTable


class BookingTable(Base):
    __tablename__ = "booking_tables"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    billiard_table_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("billiard_tables.id"), nullable=False
    )
    start_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        PgEnum(BookingStatus), nullable=False, default=BookingStatus.PENDING.name
    )
    phone: Mapped[PhoneNumberType] = mapped_column(PhoneNumberType(region="BY"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now(), onupdate=datetime.now()
    )

    billiard_table: Mapped[BilliardTable] = relationship(back_populates="bookings")
