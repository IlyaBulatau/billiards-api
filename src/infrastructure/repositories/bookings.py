from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from core.enums import BookingStatus
from core.filters.filter_model import FilterModel
from core.interfaces.repositories.bookings import IBookingTableRepository
from core.schemes.paginations import Pagination
from infrastructure.database.models.bookings import BookingTable


class BookingTableRepository(IBookingTableRepository):
    async def get_all(
        self, filters: FilterModel[BookingTable], pagination: Pagination
    ) -> list[BookingTable]: ...

    async def create(self, instance: BookingTable) -> BookingTable:
        self._async_session.add(instance)

        await self._async_session.commit()

        return instance

    async def update(self, instance: BookingTable) -> BookingTable: ...

    async def delete(self, instance: BookingTable) -> None: ...

    async def get_booking_table_by_range(
        self, billiard_table_id: UUID, start_time: datetime, end_time: datetime
    ) -> BookingTable | None:
        """
        Получить брони стола которые попадают в диапазон,
        может быть только 1 такая бронь в статусе CONFIRMED
        """

        stmt = select(BookingTable).where(
            BookingTable.billiard_table_id == billiard_table_id,
            BookingTable.start_time < end_time,
            BookingTable.end_time > start_time,
            BookingTable.status.in_([BookingStatus.CONFIRMED]),
        )

        result = await self._async_session.execute(stmt)

        return result.scalar()
