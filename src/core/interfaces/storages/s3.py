from abc import abstractmethod

from aioboto3 import Session

from core.interfaces.storages.abstract import IStorage
from settings import Settings


class IS3Storage(IStorage):
    settings: Settings

    def __init__(self, s3_session: Session) -> None:
        self._s3_session = s3_session

    @abstractmethod
    async def get_url(self, path: str, expiration: int) -> str: ...
