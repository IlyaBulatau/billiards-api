from datetime import datetime
from uuid import UUID

from core.interfaces.repositories.abstract import IRepository
from infrastructure.database.models.bookings import BookingTable


class IBookingTableRepository(IRepository[BookingTable]):
    async def get_booking_table_by_range(
        self, billiard_table_id: UUID, start_time: datetime, end_time: datetime
    ) -> BookingTable | None:
        """Получить брони в диапазоне дат"""
