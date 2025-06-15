"""
Содержит регистрацию всех контроллеров в приложении.
"""

from blacksheep import Application

from presentation.html.billiards.views import BilliardClubView
from presentation.rest import BilliardClubAPIController, BookingController


CONTROLLERS = [BilliardClubAPIController, BookingController, BilliardClubView]


def configure_controllers(app: Application) -> None:
    app.register_controllers(CONTROLLERS)
