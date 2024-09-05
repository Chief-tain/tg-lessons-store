import json
import pickle
from typing import Optional

from aiogram.fsm.storage.base import StorageKey, DEFAULT_DESTINY
from aiogram.fsm.storage.redis import (
    RedisStorage,
    DefaultKeyBuilder,
    _JsonLoads,
    _JsonDumps,
    KeyBuilder,
)  # NOQA
from redis.asyncio.client import Redis
from redis.typing import ExpiryT

from bot_app.modules.types import Pickleable


class DefaultKeyBuilderCustomKeys(DefaultKeyBuilder):
    # fixed type annotations
    def build(self, key: StorageKey, part: str) -> str:
        parts = [self.prefix]  # NOQA

        if self.with_bot_id:
            parts.append(str(key.bot_id))
        parts.append(str(key.chat_id))

        if key.thread_id:
            parts.append(str(key.thread_id))
        parts.append(str(key.user_id))

        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(
                "Redis key builder is not configured to use key destiny other the default.\n"
                "\n"
                "Probably, you should set `with_destiny=True` in for DefaultKeyBuilder.\n"
                "E.g: `RedisStorage(redis, key_builder=DefaultKeyBuilder(with_destiny=True))`"
            )

        parts.append(part)

        return self.separator.join(parts)


class RedisStorageCustomKeys(RedisStorage):
    def __init__(
        self,
        redis: Redis,
        key_builder: Optional[KeyBuilder] = None,
        state_ttl: Optional[ExpiryT] = None,
        data_ttl: Optional[ExpiryT] = None,
        json_loads: _JsonLoads = json.loads,
        json_dumps: _JsonDumps = json.dumps,
    ) -> None:
        if key_builder is None:
            key_builder = DefaultKeyBuilderCustomKeys()

        super().__init__(
            redis, key_builder, state_ttl, data_ttl, json_loads, json_dumps
        )

    async def set_custom_key(
        self,
        key: StorageKey,
        custom_key: str,
        data: Pickleable = None,
    ) -> None:
        redis_key = self.key_builder.build(key, custom_key)  # NOQA

        if data is None:
            await self.redis.delete(redis_key)
            return

        try:
            data = pickle.dumps(data)
        except pickle.PicklingError as e:
            raise ValueError("This data is not pickleable") from e

        await self.redis.set(
            redis_key,
            data,
            ex=self.data_ttl,
        )

    async def get_custom_key(
        self,
        key: StorageKey,
        custom_key: str,
    ) -> Pickleable:
        data = await self.redis.get(self.key_builder.build(key, custom_key))  # NOQA

        if data is None:
            return None

        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            raise pickle.UnpicklingError(
                f"Can not unpickle data from FSM\nKey: {key}\nCustom key: {custom_key}"
            ) from e
