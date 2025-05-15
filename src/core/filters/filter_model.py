from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict


SQLAlchemyModel = TypeVar("SQLAlchemyModel")


class FilterModel(BaseModel, Generic[SQLAlchemyModel]):
    """Базовай класс для фильтров"""

    model_config = ConfigDict(extra="ignore")

    class Model:
        target = SQLAlchemyModel
