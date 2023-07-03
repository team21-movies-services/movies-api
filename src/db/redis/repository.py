from typing import Any

from fastapi import Depends
from redis.asyncio import Redis

from src.core.config import config
from src.db.abstract import AbstractCacheRepository

from .adapter import get_redis


class RedisCacheRepository(AbstractCacheRepository):
    def __init__(self, redis: Redis, expire=config.cache_expire, namespace=config.project_name) -> None:
        self._redis = redis
        self._expire = expire
        self._namespace = namespace

    async def get(self, key: str) -> Any | None:
        return await self._redis.get(key)

    async def set(self, name: str, value: Any) -> None:
        key = f"{self._namespace}:{name}"
        await self._redis.set(key, value, ex=self._expire)

    async def ping(self) -> bool:
        return await self._redis.ping()

    async def clear(self) -> None:
        keys = await self._redis.keys(f"*{self._namespace}*")
        if keys:
            await self._redis.delete(*keys)


def get_redis_repository(store=Depends(get_redis)):
    return RedisCacheRepository(store)
