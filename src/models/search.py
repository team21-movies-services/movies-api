from pydantic import UUID4, BaseModel

DEFAULT_PAGE_NUMBER = 0
MIN_PAGE_NUMBER = 0

DEFAULT_PAGE_SIZE = 20
MIN_PAGE_SIZE = 1


class BaseSearchParams(BaseModel):
    query: str | None = None
    sort: str | None = None
    page_number: int = DEFAULT_PAGE_NUMBER
    page_size: int = DEFAULT_PAGE_SIZE
    search_after: str | None = None


class FilmsSearchParams(BaseSearchParams):
    genre: UUID4 | None = None
    person: UUID4 | None = None


class PersonSearchParams(BaseSearchParams):
    ...
