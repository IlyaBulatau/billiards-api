from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel

from core.interfaces.repositories.billiards import IBilliardTableRepository
from core.interfaces.repositories.bookings import IBookingTableRepository
from core.validators.bookngs import BookingTableIsFreeValidator


T = TypeVar("T")


class IReservationTableCommand(ABC, Generic[T]):
    """Бронирование времени стола"""

    def __init__(
        self,
        booking_table_repository: IBookingTableRepository,
        billiard_table_repository: IBilliardTableRepository,
        booking_table_is_free_validator: BookingTableIsFreeValidator,
    ):
        self._booking_table_repository = booking_table_repository
        self._billiard_table_repository = billiard_table_repository
        self._booking_table_is_free_validator = booking_table_is_free_validator

    @abstractmethod
    async def execute(
        self, billiard_table_id: UUID, phone: str, start_time: datetime, end_time: datetime
    ) -> BaseModel:
        """Создание брони на стол

        Стол можно забронировать при условии соблюдения следующих правил: время бронирования стола
        не затрагивает существующие брони на этот стол; время бронирования попадает в промежуток
        времени работы клуба; соблюдение максимального и минимального времени бронирования;
        минимальное время бронирования до начала брони.
        """
