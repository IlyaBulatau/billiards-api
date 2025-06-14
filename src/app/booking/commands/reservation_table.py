import asyncio
from datetime import datetime
from uuid import UUID

from app.booking.schemes.response import BookingCreateScheme
from core.exceptions.billiards import BilliardTableNotExistsError
from core.interfaces.commands.bookings import IReservationTableCommand
from infrastructure.database.models.billiards import BilliardClub
from infrastructure.database.models.bookings import BookingTable


class ReservationTableCommand(IReservationTableCommand[BilliardClub]):
    async def execute(
        self, billiard_table_id: UUID, phone: str, start_time: datetime, end_time: datetime
    ) -> BookingCreateScheme:
        billiard_table = await self._billiard_table_repository.get_by_id_with_club_and_schedules(
            billiard_table_id
        )

        if not billiard_table:
            raise BilliardTableNotExistsError

        validate_tasks = [
            asyncio.create_task(
                self._booking_table_is_free_validator.validate(
                    billiard_table_id, start_time, end_time
                )
            ),
            asyncio.create_task(
                self._club_schedule_available_validator.validate(
                    billiard_table.billibard_club, start_time
                )
            ),
        ]

        done, _ = await asyncio.wait(validate_tasks, return_when=asyncio.FIRST_EXCEPTION)

        for future in done:
            await future

        instance = BookingTable(
            billiard_table_id=billiard_table_id,
            phone=phone,
            start_time=start_time,
            end_time=end_time,
        )

        booking = await self._booking_table_repository.create(instance)

        return BookingCreateScheme.model_validate(booking)
