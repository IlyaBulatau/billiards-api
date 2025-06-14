from datetime import datetime
from uuid import UUID

from core.exceptions.bookings import BookingTimeAlreadyBookedError
from core.interfaces.repositories.bookings import IBookingTableRepository


class BookingTableIsFreeValidator:
    """Проверка что время бронирования стола не затрагивает существующие брони на этот стол"""

    def __init__(self, booking_table_repository: IBookingTableRepository):
        self._booking_table_repository = booking_table_repository

    async def validate(
        self, billiard_table_id: UUID, start_time: datetime, end_time: datetime
    ) -> None:
        existing_booking_by_range = await self._booking_table_repository.get_booking_table_by_range(
            billiard_table_id, start_time, end_time
        )

        if existing_booking_by_range:
            raise BookingTimeAlreadyBookedError


class BookingTableBeforeClubClosing:
    """
    Проверят возможность бронирования стола в зависимости
    от того сколько времени осталось до закрытия клуба
    """

    def validate(self): ...
