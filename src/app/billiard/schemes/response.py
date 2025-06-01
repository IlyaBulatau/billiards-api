from datetime import time
from uuid import UUID

from pydantic import BaseModel

from core.enums import DayOfWeek


class BilliardClubAddressScheme(BaseModel):
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
    day_of_week: DayOfWeek
    opening_time: time
    closing_time: time
    is_overnight: bool
    is_closed: bool

    class Config:
        from_attributes = True


class BilliardClubAllItemScheme(BaseModel):
    id: UUID
    name: str
    phone: str | None
    email: str | None
    photo: str | None
    address: BilliardClubAddressScheme | None
    schedules: list[BilliardClubScheduleScheme]

    class Config:
        from_attributes = True
