"""
Документация к сваггеру для ендпоинтов
"""

from blacksheep.server.openapi.common import EndpointDocs

from app.billiard.schemes.response import BilliardClubAllItemScheme


get_billiard_clubs = EndpointDocs(tags=["Бильярный клуб"])
