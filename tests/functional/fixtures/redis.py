import pytest
from redis.asyncio import Redis

from tests.functional.settings import test_settings


@pytest.fixture
async def redis_client():
    redis = Redis(host=test_settings.redis_host, port=test_settings.redis_port)
    async for key in redis.scan_iter("*"):
        await redis.delete(key)
    yield redis
    await redis.close()
