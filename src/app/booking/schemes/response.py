from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from core.enums import BookingStatus


class BookingCreateScheme(BaseModel):
    id: UUID
    billiard_table_id: UUID
    start_time: datetime
    end_time: datetime
    status: BookingStatus
    created_at: datetime

    class Config:
        from_attributes = True
