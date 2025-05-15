from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from core.filters.filter_model import FilterModel, SQLAlchemyModel
from core.schemes.paginations import Pagination


T = TypeVar("T")


class IRepository(ABC, Generic[T]):
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    @abstractmethod
    async def get_all(
        self, filters: FilterModel[SQLAlchemyModel], pagination: Pagination
    ) -> Sequence[T]: ...

    @abstractmethod
    async def create(self, entity: T) -> T: ...

    @abstractmethod
    async def update(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, entity: T) -> None: ...
