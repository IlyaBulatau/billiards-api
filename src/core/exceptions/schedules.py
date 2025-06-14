from core.exceptions.base import BadRequestError


class ClubDoesNotWorkError(BadRequestError):
    msg = "Клуб не работает в это время"
