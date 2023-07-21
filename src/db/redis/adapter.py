from redis.asyncio import Redis

from src.exceptions.redis import RedisNotInitException

redis: Redis | None = None


async def get_redis() -> Redis:
    if redis:
        return redis
    raise RedisNotInitException
