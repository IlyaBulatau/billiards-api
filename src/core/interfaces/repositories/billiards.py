from core.interfaces.repositories.abstract import IRepository
from infrastructure.database.models import BilliardClub, BilliardTable


class IBilliardClubRepository(IRepository[BilliardClub]):
    pass


class IBilliardTableRepository(IRepository[BilliardTable]):
    pass
