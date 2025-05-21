from uuid import UUID

from pydantic import BaseModel


class BilliardClubAddressScheme(BaseModel):
    id: UUID
    city: str
    street: str
    building: str
    apartment: str | None
    latitude: float | None
    longitude: float | None

    class Config:
        from_attributes = True


class BilliardClubAllItemScheme(BaseModel):
    id: UUID
    name: str
    phone: str | None
    email: str | None
    photo: str | None
    address: BilliardClubAddressScheme | None

    class Config:
        from_attributes = True
