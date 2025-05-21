from typing import Any

from aiobotocore.config import AioConfig

from core.interfaces.storages.s3 import IS3Storage


class S3Storage(IS3Storage):
    async def get_url(self, path: str, expiration: int = 3600) -> str:
        async with self._s3_session.client(
            "s3",
            endpoint_url=self._settings.s3.endpoint,
            config=AioConfig({"keepalive_timeout": 5}),
        ) as client:
            url: str = await client.generate_presigned_url(
                "get_object",
                Params={"Key": path, "Bucket": self._settings.s3.bucket},
                ExpiresIn=expiration,
            )
            return url

    async def upload(self, file: bytes, path: str, **kwargs: Any) -> None:
        async with self._s3_session.client(
            service_name="s3", endpoint_url=self._settings.s3.endpoint
        ) as client:
            await client.put_object(Body=file, Bucket=self._settings.s3.bucket, Key=path, **kwargs)

    async def delete(self, path: str) -> None:
        async with self._s3_session.client(
            service_name="s3", endpoint_url=self._settings.s3.endpoint
        ) as client:
            await client.delete_object(Bucket=self._settings.s3.bucket, Key=path)
