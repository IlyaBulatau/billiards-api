"""
Содержит обработку ошибок приложения.
"""

from typing import Any

from blacksheep import Request, Response
from blacksheep.server import Application
from blacksheep.server.responses import json
from essentials.exceptions import (
    AcceptedException,
    ForbiddenException,
    NotImplementedException,
    ObjectNotFound,
    UnauthorizedException,
)


def configure_error_handlers(app: Application) -> None:
    async def not_found_handler(
        app: Application, request: Request, exception: Exception
    ) -> Response:
        return json({"error": "NotFound"}, status=404)

    async def not_implemented(*args: Any) -> Response:
        return json({"error": "NotImplemented"}, status=500)

    async def unauthorized(*args: Any) -> Response:
        return json({"error": "Unauthorized"}, status=401)

    async def forbidden(*args: Any) -> Response:
        return json({"error": "Forbidden"}, status=403)

    async def accepted(*args: Any) -> Response:
        return json({"error": "Accepted"}, status=202)

    app.exceptions_handlers.update(
        {
            ObjectNotFound: not_found_handler,
            NotImplementedException: not_implemented,
            UnauthorizedException: unauthorized,
            ForbiddenException: forbidden,
            AcceptedException: accepted,
        }
    )
