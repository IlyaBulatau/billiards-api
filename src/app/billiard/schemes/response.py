from pydantic import BaseModel


class BilliardClubAllItemScheme(BaseModel):
    name: str

    class Config:
        from_attributes = True
