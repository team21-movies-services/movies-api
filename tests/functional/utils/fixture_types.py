from typing import Any, Protocol

from pydantic import BaseModel


class HTTPResponse(BaseModel):
    body: Any
    status: int


class MakeHTTPGetRequest(Protocol):
    async def __call__(self, endpoint: str, params: dict | None = None) -> HTTPResponse:
        ...


class EsWriteData(Protocol):
    async def __call__(self, data: list[dict], es_index: str) -> None:
        ...


class EsDeleteData(Protocol):
    async def __call__(self, es_index: str) -> None:
        ...
