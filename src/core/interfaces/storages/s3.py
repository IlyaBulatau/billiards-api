from abc import abstractmethod

from aioboto3 import Session

from core.interfaces.storages.abstract import IStorage
from settings import Settings


class IS3Storage(IStorage):
    def __init__(self, s3_session: Session, settings: Settings) -> None:
        self._s3_session = s3_session
        self._settings = settings

    @abstractmethod
    async def get_url(self, path: str, expiration: int = 3600) -> str: ...
