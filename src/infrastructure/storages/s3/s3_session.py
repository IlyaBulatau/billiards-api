from aioboto3 import Session
from rodi import ActivationScope

from settings import Settings


def get_s3_session(settings: Settings | ActivationScope) -> Session | ActivationScope:
    if isinstance(settings, ActivationScope):
        settings = settings.provider.get("settings")

    return Session(
        aws_access_key_id=settings.s3.access_key,
        aws_secret_access_key=settings.s3.secret_key,
        region_name="by",
    )
