from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession


CURRENT_ASYNC_SESSION: ContextVar[AsyncSession] = ContextVar("CURRENT_ASYNC_SESSION")
