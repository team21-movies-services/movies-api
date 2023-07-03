from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from src.api.response_models.status_response import StatusResponse
from src.db.elastic.adapter import get_elastic
from src.db.repositories import cacheRepository


class StatusService:
    def __init__(
        self,
        cache_repository: cacheRepository,
        elastic: AsyncElasticsearch = Depends(get_elastic),
    ) -> None:
        self._cache_repository = cache_repository
        self._elastic = elastic

    async def get_status_of_services(self) -> StatusResponse:
        status = StatusResponse(
            api=True,
            cache_repository=await self._cache_repository.ping(),
            elastic=await self._elastic.ping(),
        )

        return status


statusService = Annotated[StatusService, Depends(StatusService)]
