"""
Содержит регистрацию всех контроллеров в приложении.
"""

from blacksheep import Application

from presentation.rest import BilliardClubAPIController, BookingController


CONTROLLERS = [BilliardClubAPIController, BookingController]


def configure_controllers(app: Application) -> None:
    app.register_controllers(CONTROLLERS)
