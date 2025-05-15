"""
Содержит регистрацию всех контроллеров в приложении.
"""

from blacksheep import Application

from presentation.rest import BilliardClubAPIController


CONTROLLERS = [BilliardClubAPIController]


def configure_controllers(app: Application) -> None:
    app.register_controllers(CONTROLLERS)
