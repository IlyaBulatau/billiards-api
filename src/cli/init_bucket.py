import logging

from aioboto3 import Session
from botocore.exceptions import ClientError
import fire

from infrastructure.storages.s3.s3_session import get_s3_session
from settings import settings


logger = logging.getLogger()
logger.setLevel(logging.INFO)


async def init_s3_bucket() -> None:
    session: Session = get_s3_session(settings)

    async with session.resource(service_name="s3", endpoint_url=settings.s3.endpoint) as client:
        try:
            await client.create_bucket(Bucket=settings.s3.bucket)
        except ClientError:
            logger.error(f"Bucket `{settings.s3.bucket}` already exists")


if __name__ == "__main__":
    fire.Fire(init_s3_bucket)
