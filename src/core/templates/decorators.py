from typing import Callable

from blacksheep.server.rendering.jinja2 import JinjaRenderer
from blacksheep.settings.html import html_settings


def template_filter(name: str) -> Callable[..., None]:
    renderer = html_settings.renderer

    assert isinstance(renderer, JinjaRenderer)

    env = renderer.env

    def wrapper(filter_class: Callable) -> None:
        env.filters.update({name: filter_class()})

    return wrapper
