from typing import Any

from blacksheep import Content, Response
from blacksheep.server.controllers import APIController as BlacksheepAPIController
from blacksheep.settings.json import json_settings

from core.docs import SuccessResponse


class APIController(BlacksheepAPIController):
    def json(self, data: list[Any] | dict[str, Any], status: int = 200) -> Response:
        return Response(
            status,
            None,
            Content(
                b"application/json",
                json_settings.dumps(SuccessResponse(result=data).model_dump()).encode("utf8"),
            ),
        )
