from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import RequestError
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis

from src.api.errors import elasticsearch_handler
from src.api.v1 import api_v1_router
from src.core.config import config
from src.db.elastic import adapter as es_adapter
from src.db.redis import adapter as redis_adapter


def create_app():
    app = FastAPI(
        title=config.project_name,
        docs_url="/api/openapi",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )

    @app.on_event("startup")
    async def startup():
        redis_adapter.redis = Redis(host=config.redis_host, port=config.redis_port)
        FastAPICache.init(RedisBackend(redis_adapter.redis), prefix=config.project_name, expire=config.cache_expire)
        es_adapter.es = AsyncElasticsearch(hosts=[f"{config.elastic_host}:{config.elastic_port}"])

    @app.on_event("shutdown")
    async def shutdown():
        if redis_adapter.redis:
            await redis_adapter.redis.close()
        if es_adapter.es:
            await es_adapter.es.close()

    app.include_router(api_v1_router, prefix="/api/v1")

    app.add_exception_handler(RequestError, elasticsearch_handler)

    return app
