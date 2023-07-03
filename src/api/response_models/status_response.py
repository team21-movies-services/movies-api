from pydantic import BaseModel


class StatusResponse(BaseModel):
    api: bool
    cache_repository: bool
    elastic: bool


class StatusCacheResponse(BaseModel):
    message: str
