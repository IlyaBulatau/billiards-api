import uuid

from sqlalchemy import Boolean, ForeignKey, Time
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from core.enums import DayOfWeek
from infrastructure.database.models.base import Base
from infrastructure.database.models.billiards import BilliardClub


class ClubSchedule(Base):
    __tablename__ = "club_schedules"
    __table_args__ = (
        UniqueConstraint("billiard_club_id", "day_of_week", name="unique_club_schedule"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    billiard_club_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("billiard_clubs.id"), nullable=False
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(PgEnum(DayOfWeek), nullable=False)
    opening_time: Mapped[Time] = mapped_column(Time, nullable=False)
    closing_time: Mapped[Time] = mapped_column(Time, nullable=False)
    is_overnight: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    billiard_club: Mapped[BilliardClub] = relationship(
        back_populates="schedules", single_parent=True
    )
