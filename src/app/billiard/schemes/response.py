from datetime import datetime, time
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from core.enums import BookingStatus, DayOfWeek, TableType


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
    phone: str | None
    email: str | None
    photo: str | None
    address: BilliardClubAddressScheme | None
    schedules: list[BilliardClubScheduleScheme]

    class Config:
        from_attributes = True


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
