from typing import Any, List, Union, Dict

import aiohttp
from miniopy_async import Minio


class OrderMediaRepository:
    def __init__(self, client: Minio):
        self.client = client

    async def bucket_exist(self, bucket_id: str) -> bool:
        return await self.client.bucket_exists(bucket_id)

    async def create_bucket(self, bucket_id: str) -> None:
        return await self.client.make_bucket(bucket_id)

    async def put_object(
        self,
        bucket_id: str,
        object_name: str,
        object: Any,
        object_len: int,
        metadata: Dict[str, str] | None = None,
    ) -> None:
        await self.client.put_object(
            bucket_id,
            object_name,
            object,
            object_len,
            metadata=metadata,
        )

    async def put_objects(
        self,
        bucket_id: str,
        object_names: List[str],
        objects: List[Any],
        object_lens: List[int],
        metadata: Dict[str, str] | None = None,
    ) -> None:
        if len(object_names) != len(objects) or len(objects) != len(object_lens):
            raise ValueError(
                "object_names, objects and object_lens must have the same length"
            )

        for object_name, object, object_len in zip(object_names, objects, object_lens):
            await self.client.put_object(
                bucket_id, object_name, object, object_len, metadata=metadata
            )

    async def get_objects_by_name(
        self, bucket_id: str, object_name: str
    ) -> Union[Any, str]:

        async with aiohttp.ClientSession() as session:
            current_object = await self.client.get_object(
                bucket_id, object_name, session
            )

            metadata: Dict[str, str] = (
                await self.client.stat_object(bucket_id, object_name)
            ).metadata

            return await current_object.read(), metadata

    async def get_safe_objects_by_name(
        self, bucket_id: str, object_name: str
    ) -> Union[Any, str]:
        try:
            return await self.get_objects_by_name(bucket_id, object_name)
        except Exception as e:
            return None, None

    async def remove_object_by_name(self, bucket_id: str, object_name: str) -> None:
        await self.client.remove_object(bucket_id, object_name)

    async def safe_remove_object_by_name(
        self, bucket_id: str, object_name: str
    ) -> bool:
        try:
            await self.remove_object_by_name(bucket_id, object_name)
        except Exception as e:
            return False

        return True
