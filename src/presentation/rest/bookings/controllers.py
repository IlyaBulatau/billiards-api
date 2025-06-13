from blacksheep import Response
from blacksheep.server.controllers import post

from app.booking.schemes.request import BookingCreateScheme
from core.docs import open_api
from core.interfaces.commands.bookings import IReservationTableCommand
from presentation.rest.api_controller import APIController
from presentation.rest.bookings import docs
from settings import Settings


class BookingController(APIController):
    settings: Settings

    @classmethod
    def version(cls) -> str:
        return cls.settings.api_version

    @classmethod
    def route(cls) -> str | None:
        return "/bookings/"

    @open_api(docs.do_booking_table)
    @post()
    async def booking_table(
        self,
        booking_create_data: BookingCreateScheme,
        reservation_command: IReservationTableCommand,
    ) -> Response:
        booking = await reservation_command.execute(
            booking_create_data.billiard_table_id,
            booking_create_data.phone,
            booking_create_data.start_time,
            booking_create_data.end_time,
        )

        return self.json(data=booking)
