from abc import ABC, abstractmethod
from typing import Generic, NoReturn, Sequence, TypeVar
from uuid import UUID

from pydantic import BaseModel

from core.interfaces.repositories import IBilliardClubRepository
from core.interfaces.storages.s3 import IS3Storage
from core.schemes.paginations import Pagination


T = TypeVar("T")
F = TypeVar("F")


class IBilliardClubService(ABC, Generic[T, F]):
    def __init__(self, billiard_club_repository: IBilliardClubRepository, s3_storage: IS3Storage):
        self._billiard_club_repository = billiard_club_repository
        self._s3_storage = s3_storage

    @abstractmethod
    async def get_all(self, filters: F, paginaton: Pagination) -> Sequence[BaseModel]: ...

    @abstractmethod
    async def get_detail(self, billiard_club_id: UUID) -> BaseModel | NoReturn: ...
