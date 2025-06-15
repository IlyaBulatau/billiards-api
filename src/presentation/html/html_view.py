from blacksheep import Response
from blacksheep.server.controllers import Controller
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from infrastructure.database.context import CURRENT_ASYNC_SESSION


class HTMLView(Controller):
    async def on_response(self, response: Response) -> None:
        context_async_session: AsyncSession = CURRENT_ASYNC_SESSION.get()

        # TODO: а если ошибка в прилаге сессия не закроется
        # написать uow с контекстным менеджером,
        # тогда можно избавится от контекстной переменной, и в
        # случае ошибки сессия будет закрываться после выхода из контекстного менеджера
        await context_async_session.close()

    @override
    def full_view_name(self, name: str) -> str:
        """Returns the full view name for this controller."""

        return name
