from blacksheep import Request
from blacksheep.server.bindings import Binder

from core.schemes import Pagination
from settings import settings


class PaginationBinder(Binder):
    handle = Pagination

    async def get_value(self, request: Request) -> Pagination:
        offset = request.query.get("offset", [0])
        limit = request.query.get("limit", [settings.api_default_page_size])

        limit = min(int(limit[0]), settings.api_max_page_size)
        offset = int(offset[0])

        return Pagination(offset=offset, limit=limit)
