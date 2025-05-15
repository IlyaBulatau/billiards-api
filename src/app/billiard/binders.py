from blacksheep import Request
from blacksheep.server.bindings import Binder

from app.billiard.filters import BilliardClubFilter


class BilliardClubFilterBinder(Binder):
    handle = BilliardClubFilter

    async def get_value(self, request: Request) -> BilliardClubFilter:
        filters = {key: value[0] for key, value in request.query.items()}

        return BilliardClubFilter(**filters)
