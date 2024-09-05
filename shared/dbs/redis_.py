from urllib.parse import urlunsplit
from redis import Redis
from redis.asyncio import Redis as RedisAsync

from shared import settings


def get_redis_uri(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        protocol=settings.REDIS_PROTOCOL,
) -> str:
    return urlunsplit((protocol, f'{host}:{port}', db, str(), str()))


redis = Redis.from_url(get_redis_uri())
redis_async = RedisAsync.from_url(get_redis_uri())
