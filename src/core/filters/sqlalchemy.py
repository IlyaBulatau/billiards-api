"""
Содержит реализацию фильтрации для SQLAlchemy.
Код отсюда https://github.com/arthurio/fastapi-filter, так как не удалось прикрутить библиотеку целиком.
"""

from typing import Any, Union
from warnings import warn

from sqlalchemy import Select
from sqlalchemy.orm import Query

from core.filters.filter_model import FilterModel


def _backward_compatible_value_for_like_and_ilike(value: str) -> str:
    """Add % if not in value to be backward compatible.

    Args:
        value (str): The value to filter.

    Returns:
        Either the unmodified value if a percent sign is present, the value wrapped in % otherwise to preserve
        current behavior.
    """
    if "%" not in value:
        warn(
            "You must pass the % character explicitly to use the like and ilike operators.",
            DeprecationWarning,
            stacklevel=2,
        )
        value = f"%{value}%"
    return value


_orm_operator_transformer = {
    "neq": lambda value: ("__ne__", value),
    "gt": lambda value: ("__gt__", value),
    "gte": lambda value: ("__ge__", value),
    "in": lambda value: ("in_", value),
    "isnull": lambda value: ("is_", None) if value is True else ("is_not", None),
    "lt": lambda value: ("__lt__", value),
    "lte": lambda value: ("__le__", value),
    "like": lambda value: ("like", _backward_compatible_value_for_like_and_ilike(value)),
    "ilike": lambda value: ("ilike", _backward_compatible_value_for_like_and_ilike(value)),
    # XXX(arthurio): Mysql excludes None values when using `in` or `not in` filters.
    "not": lambda value: ("is_not", value),
    "not_in": lambda value: ("not_in", value),
}


def orm_filter(pydantic_filter_model: FilterModel | None, query: Union[Query, Select]) -> Any:
    """Реализация добавления фильтров к orm запросу."""

    if not pydantic_filter_model:
        return query

    filtering_fields = pydantic_filter_model.model_dump(
        exclude_none=True, exclude_unset=True
    ).items()

    for field_name, value in filtering_fields:
        if "__" in field_name:
            field_name, operator = field_name.split("__")
            operator, value = _orm_operator_transformer[operator](value)
        else:
            operator = "__eq__"

        model_field = getattr(pydantic_filter_model.Model.target, field_name)
        query = query.filter(getattr(model_field, operator)(value))

    return query
