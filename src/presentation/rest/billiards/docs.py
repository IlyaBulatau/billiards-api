"""
Документация к сваггеру для ендпоинтов
"""

from blacksheep.server.openapi.common import ContentInfo, EndpointDocs, ResponseInfo

from app.billiard.schemes.response import BilliardClubAllItemScheme, BilliardClubDetailScheme
from core.docs import SuccessResponse


get_billiard_clubs = EndpointDocs(
    tags=["Бильярный клуб"],
    responses={
        200: ResponseInfo(
            description="Получить список всех бильярных клубов",
            content=[ContentInfo(SuccessResponse[list[BilliardClubAllItemScheme]])],
        )
    },
)


get_billiard_club_detail = EndpointDocs(
    tags=["Бильярный клуб"],
    responses={
        200: ResponseInfo(
            description="Получить детальную информацию о клубе",
            content=[ContentInfo(SuccessResponse[BilliardClubDetailScheme])],
        )
    },
)
