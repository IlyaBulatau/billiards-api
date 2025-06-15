from blacksheep.server.openapi.common import ContentInfo, EndpointDocs, ResponseInfo

from app.booking.schemes.response import BookingCreateScheme
from core.docs import SuccessResponse


do_booking_table = EndpointDocs(
    tags=["Бронирование"],
    responses={
        201: ResponseInfo(
            description="Забронировать стол",
            content=[ContentInfo(SuccessResponse[BookingCreateScheme])],
        )
    },
)
