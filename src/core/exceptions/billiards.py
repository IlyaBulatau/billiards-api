from core.exceptions.base import BadRequestError


class BilliardTableNotExistsError(BadRequestError):
    msg = "Биллиардный стол не найден"
