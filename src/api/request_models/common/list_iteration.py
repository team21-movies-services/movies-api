from fastapi import Query
from pydantic import BaseModel

from src.models.search import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MIN_PAGE_NUMBER,
    MIN_PAGE_SIZE,
)


class PageBasedIteration(BaseModel):
    page_number: int = Query(DEFAULT_PAGE_NUMBER, ge=MIN_PAGE_NUMBER)
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=MIN_PAGE_SIZE)


class ElasticsearchIteration(BaseModel):
    search_after: str | None = None
