from abc import ABC, abstractmethod
from typing import Any


class IStorage(ABC):
    @abstractmethod
    async def upload(self, file: bytes, path: str, **kwargs: Any) -> None: ...

    @abstractmethod
    async def delete(self, path: str) -> None: ...
