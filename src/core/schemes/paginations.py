from pydantic import BaseModel, Field

from settings import settings


class Pagination(BaseModel):
    offset: int = Field(1, ge=0)
    limit: int = Field(settings.api_default_page_size, ge=0, le=settings.api_max_page_size)
