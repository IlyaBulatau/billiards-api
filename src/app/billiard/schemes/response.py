from datetime import datetime, time
from decimal import Decimal
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ValidationInfo, model_validator

from core.enums import BookingStatus, DayOfWeek, TableType
from core.use_cases.club_closing_time import get_closing_time
from core.use_cases.club_opening_time import get_nearest_opening_time
from core.use_cases.is_work_billiard_club_now import is_work_billiard_club_now
from infrastructure.database.models import BilliardClub
from settings import TIMEZONE


class BilliardClubAddressScheme(BaseModel):
    """Адрес биллиардного клуба"""

    id: UUID
    city: str
    street: str
    building: str
    apartment: str | None
    latitude: float | None
    longitude: float | None

    class Config:
        from_attributes = True


class BilliardClubScheduleScheme(BaseModel):
    """Расписание биллиардного клуба"""

    day_of_week: DayOfWeek
    opening_time: time
    closing_time: time
    is_overnight: bool
    is_closed: bool

    class Config:
        from_attributes = True


class BilliardClubAllItemScheme(BaseModel):
    """Бильярдный клуб в списке"""

    id: UUID
    name: str
    is_work_now: bool
    phone: str | None
    email: str | None
    photo: str | None
    address: BilliardClubAddressScheme | None
    schedules: list[BilliardClubScheduleScheme]
    tables_count: int
    has_russian: bool
    has_pool: bool
    has_snooker: bool
    closing_time: time | None = None
    opening_dt: datetime | None = None

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    def set_dynamic_fields(self, info: ValidationInfo) -> Self:
        context = info.context
        billiard_club: BilliardClub = context["instance"]

        self.is_work_now = is_work_billiard_club_now(billiard_club, datetime.now(tz=TIMEZONE))

        if self.is_work_now:
            self.closing_time = get_closing_time(billiard_club)
        else:
            self.opening_dt = get_nearest_opening_time(billiard_club)

        return self


class BilliardTableBookingScheme(BaseModel):
    """Бронь стола"""

    id: UUID
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True


class BilliardClubTableScheme(BaseModel):
    """Биллиардный стол клуба"""

    id: UUID
    table_type: TableType
    price_per_hour: Decimal
    bookings: list[BilliardTableBookingScheme]

    class Config:
        from_attributes = True


class BilliardClubDetailScheme(BilliardClubAllItemScheme):
    """Бильярдный клуб детально"""

    billiard_tables: list[BilliardClubTableScheme]

    class Config:
        from_attributes = True
