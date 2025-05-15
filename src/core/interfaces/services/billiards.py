from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel

from core.interfaces.repositories import IBilliardClubRepository
from core.schemes.paginations import Pagination


T = TypeVar("T")
F = TypeVar("F")


class IBilliardClubService(ABC, Generic[T, F]):
    def __init__(self, billiard_club_repository: IBilliardClubRepository):
        self._billiard_club_repository = billiard_club_repository

    @abstractmethod
    async def get_all(self, filters: F, paginaton: Pagination) -> Sequence[BaseModel]: ...
