from .common.list_iteration import ElasticsearchIteration, PageBasedIteration


class PersonSearchQueryParams(PageBasedIteration, ElasticsearchIteration):
    sort: str | None = None
    query: str | None = None
