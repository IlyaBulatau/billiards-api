from abc import ABC, abstractmethod
from typing import Generic, NoReturn, Sequence, TypeVar
from uuid import UUID

from pydantic import BaseModel

from core.interfaces.repositories import IBilliardClubRepository
from core.interfaces.storages.s3 import IS3Storage
from core.schemes.paginations import Pagination


T = TypeVar("T")
F = TypeVar("F")


class IBilliardClubListQuery(ABC, Generic[T, F]):
    """Получение списка бильярдных клубов"""

    def __init__(self, billiard_club_repository: IBilliardClubRepository, s3_storage: IS3Storage):
        self._billiard_club_repository = billiard_club_repository
        self._s3_storage = s3_storage

    @abstractmethod
    async def query(self, filters: F, pagination: Pagination) -> Sequence[BaseModel]: ...


class IBilliardClubDetailQuery(ABC, Generic[T]):
    """Получение данных бильярдного клуба по ID"""

    def __init__(self, billiard_club_repository: IBilliardClubRepository, s3_storage: IS3Storage):
        self._billiard_club_repository = billiard_club_repository
        self._s3_storage = s3_storage

    @abstractmethod
    async def query(self, billiard_club_id: UUID) -> BaseModel | NoReturn: ...


class IBilliardClubCountQuery(ABC, Generic[T, F]):
    """Получение количества бильярдныз клубов"""

    def __init__(self, billiard_club_repository: IBilliardClubRepository):
        self._billiard_club_repository = billiard_club_repository

    @abstractmethod
    async def query(self, filters: F) -> int: ...
