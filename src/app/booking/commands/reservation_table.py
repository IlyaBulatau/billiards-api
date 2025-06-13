from datetime import datetime
from uuid import UUID

from app.booking.schemes.response import BookingCreateScheme
from core.exceptions.billiards import BilliardTableNotExistsError
from core.exceptions.bookings import BookingTimeAlreadyBookedError
from core.interfaces.commands.bookings import IReservationTableCommand
from infrastructure.database.models.bookings import BookingTable


class ReservationTableCommand(IReservationTableCommand[BookingTable]):
    async def execute(
        self, billiard_table_id: UUID, phone: str, start_time: datetime, end_time: datetime
    ) -> BookingCreateScheme:
        await self._validation_booking_table(billiard_table_id, start_time, end_time)

        instance = BookingTable(
            billiard_table_id=billiard_table_id,
            phone=phone,
            start_time=start_time,
            end_time=end_time,
        )

        booking = await self._booking_table_repository.create(instance)

        return BookingCreateScheme.model_validate(booking)

    async def _validation_booking_table(
        self, billiard_table_id: UUID, start_time: datetime, end_time: datetime
    ) -> None:
        """Проверка на возможность забронировать стол"""

        billiard_table = await self._billiard_table_repository.get_by_id_with_club_and_schedules(
            billiard_table_id
        )

        if not billiard_table:
            raise BilliardTableNotExistsError

        existing_booking_by_range = await self._booking_table_repository.get_booking_table_by_range(
            billiard_table_id, start_time, end_time
        )

        if existing_booking_by_range:
            raise BookingTimeAlreadyBookedError

        # TODO: проверка что время бронирования попадает под время работы клуба
        # получить расписание за прошлый день и по расписанию прошлого дня ресторан клуб работает
        # проверить затрагивает ли время работы дня если да то проверить попадает ли время работы под бронирование
        # иначе взять расписание на сегодня и проверить то же самое
