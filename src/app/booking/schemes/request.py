from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber


class BookingCreateScheme(BaseModel):
    billiard_table_id: UUID
    phone: PhoneNumber
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True
