from typing import Annotated

from fastapi import Depends

from src.db.abstract import AbstractCacheRepository
from src.db.redis.repository import get_redis_repository

cacheRepository = Annotated[AbstractCacheRepository, Depends(get_redis_repository)]
