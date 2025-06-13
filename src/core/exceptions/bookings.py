from core.exceptions.base import BadRequestError


class BookingTimeAlreadyBookedError(BadRequestError):
    msg = "Время уже забронировано"
