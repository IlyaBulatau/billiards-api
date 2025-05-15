from blacksheep import Application
from blacksheep.server.diagnostics import get_diagnostic_app

from core.controllers import configure_controllers
from core.di import configure_di
from core.docs import configure_open_api
from core.errors import configure_error_handlers
from settings import Settings, settings


def configure_application(settings: Settings) -> Application:
    """Настройка конфигурации приложения"""

    app = Application(
        show_error_details=settings.show_error_details,
    )

    configure_di(app, settings)
    configure_error_handlers(app)
    configure_controllers(app)
    configure_open_api(app)

    return app


def get_app() -> Application:
    try:
        return configure_application(settings)
    except Exception as exc:
        return get_diagnostic_app(exc)


app = get_app()
