"""
Содержит генерацию документации в сваггере.
"""

from typing import Any, Generic, TypeVar

from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info, MediaType, Parameter, ParameterLocation, Response, Schema
from pydantic import BaseModel

from app.billiard.binders import BilliardClubFilterBinder
from core.binders import PaginationBinder
from settings import settings


R = TypeVar("R")


class SuccessResponse(BaseModel, Generic[R]):
    success: bool = True
    result: R


class ErrorInfo(BaseModel):
    error: str
    detail: dict[str, Any]


open_api = OpenAPIHandler(
    info=Info(title="API", version="0.1.0"),
    ui_path="/docs",
    anonymous_access=True,
)


def configure_open_api(app: Application) -> None:
    """
    Сюда нужно добавлять все биндеры зависимости которых должны быть в сваггере.
    Ксожаления, сваггер не генерируется на основании биндеров автоматически, неприятно.
    """
    open_api.bind_app(app)

    error_info = open_api.register_schema_for_type(ErrorInfo)

    open_api.common_responses = {
        400: Response(
            "Bad Request",
            content={
                "application/json": MediaType(schema=Schema(type="object", any_of=[error_info]))
            },
        ),
        401: Response(
            "Unauthorized",
            content={
                "application/json": MediaType(schema=Schema(type="object", any_of=[error_info]))
            },
        ),
        403: Response(
            "Forbidden",
            content={
                "application/json": MediaType(schema=Schema(type="object", any_of=[error_info]))
            },
        ),
    }

    open_api.set_binder_docs(
        PaginationBinder,
        [
            Parameter(
                "offset",
                ParameterLocation.QUERY,
                required=False,
                schema=Schema(type="integer", minimum=0),
            ),
            Parameter(
                "limit",
                ParameterLocation.QUERY,
                required=False,
                schema=Schema(type="integer", minimum=0, maximum=settings.api_max_page_size),
            ),
        ],
    )
    open_api.set_binder_docs(
        BilliardClubFilterBinder,
        [
            Parameter("name", ParameterLocation.QUERY, required=False),
            Parameter("name__ilike", ParameterLocation.QUERY, required=False),
        ],
    )
