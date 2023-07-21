from typing import Any, Protocol

from pydantic import UUID4

from src.api.response_models.film_response import FilmDetailResponse, FilmResponse
from src.api.response_models.genre_response import GenreResponse
from src.api.response_models.person_response import PersonFilmResponse
from src.models.search import FilmsSearchParams, PersonSearchParams

SearchAfterType = list[Any] | None


class AbstractFilmRepository(Protocol):
    async def get_by_id(self, film_id: UUID4) -> FilmDetailResponse | None:
        ...

    async def query(self, search_query_params: FilmsSearchParams) -> list[FilmDetailResponse]:
        ...

    async def query_with_pagination(
        self,
        search_query_params: FilmsSearchParams,
    ) -> tuple[int, SearchAfterType, list[FilmResponse]]:
        ...


class AbstractPersonRepository(Protocol):
    async def get_by_id(self, person_id: UUID4) -> PersonFilmResponse | None:
        ...

    async def query_with_pagination(
        self,
        search_query_params: PersonSearchParams,
    ) -> tuple[int, SearchAfterType, list[PersonFilmResponse]]:
        ...


class AbstractGenreRepository(Protocol):
    async def get_by_id(self, genre_id: UUID4) -> GenreResponse | None:
        ...

    async def query(self) -> list[GenreResponse]:
        ...


class AbstractCacheRepository(Protocol):
    async def get(self, key: str) -> Any | None:
        ...

    async def set(self, name: str, value: Any) -> None:
        ...

    async def clear(self) -> None:
        ...

    async def ping(self) -> bool:
        ...
