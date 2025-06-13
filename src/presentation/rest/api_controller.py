from typing import Any, Sequence

from blacksheep import Content, Response
from blacksheep.server.controllers import APIController as BlacksheepAPIController
from blacksheep.settings.json import json_settings
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.docs import SuccessResponse
from infrastructure.database.context import CURRENT_ASYNC_SESSION


class APIController(BlacksheepAPIController):
    def json(self, data: Sequence[Any] | dict[str, Any] | BaseModel, status: int = 200) -> Response:
        return Response(
            status,
            None,
            Content(
                b"application/json",
                json_settings.dumps(SuccessResponse(result=data).model_dump()).encode("utf8"),
            ),
        )

    async def on_response(self, response: Response) -> None:
        context_async_session: AsyncSession = CURRENT_ASYNC_SESSION.get()

        # TODO: а если ошибка в прилаге сессия не закроется
        # написать uow с контекстным менеджером,
        # тогда можно избавится от контекстной переменной, и в
        # случае ошибки сессия будет закрываться после выхода из контекстного менеджера
        await context_async_session.close()
