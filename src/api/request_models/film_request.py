from pydantic import UUID4

from .common.list_iteration import ElasticsearchIteration, PageBasedIteration


class FilmsListQueryParams(PageBasedIteration, ElasticsearchIteration):
    sort: str | None = None
    genre: UUID4 | None = None


class FilmsSearchQueryParams(PageBasedIteration, ElasticsearchIteration):
    query: str | None = None
