from typing import TypeVar


T = TypeVar("T")


def cyclic_iteration(lst: list[T], start_index: int) -> list[T]:
    """
    Отсортировать список начиная с заданного индекса,
    используется для сортировки расписания по дням недели в зависимости от текущего дня.
    Индекс не должен превышать длинну списка.
    """

    n = len(lst)

    if n == 0:
        return []

    return lst[start_index:] + lst[:start_index]
