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

        # TODO: проверка что время бронирования попадает под время работы клуба
        # получить расписание за прошлый день и если по расписанию прошлого дня клуб работает
        # проверить затрагивает ли время брони этот день по времени
        # если да то проверить попадает ли время работы под бронирование
        # иначе взять расписание на сегодня и проверить то же самое
