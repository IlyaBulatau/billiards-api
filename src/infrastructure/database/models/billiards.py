import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import Base


class BilliardClub(Base):
    __tablename__ = "billiard_clubs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(length=256), unique=True)

    billiard_tables: Mapped[list["BilliardTable"]] = relationship(back_populates="billibard_club")


class BilliardTable(Base):
    __tablename__ = "billiard_tables"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    billiard_club_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("billiard_clubs.id"))

    billibard_club: Mapped[BilliardClub] = relationship(back_populates="billiard_tables")
