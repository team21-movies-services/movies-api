from typing import Any, Protocol

from pydantic import UUID4

from src.models.film import FilmDetail
from src.models.genre import Genre
from src.models.person import Person
from src.models.search import FilmsSearchParams, PersonSearchParams

SearchAfterType = list[Any] | None


class AbstractFilmRepository(Protocol):
    async def get_by_id(self, film_id: UUID4) -> FilmDetail | None:
        pass

    async def query(self, search_query_params: FilmsSearchParams) -> list[FilmDetail]:
        pass

    async def query_with_pagination(
        self,
        search_query_params: FilmsSearchParams,
    ) -> tuple[int, SearchAfterType, list[FilmDetail]]:
        pass


class AbstractPersonRepository(Protocol):
    async def get_by_id(self, person_id: UUID4) -> Person | None:
        pass

    async def query_with_pagination(
        self,
        search_query_params: PersonSearchParams,
    ) -> tuple[int, SearchAfterType, list[Person]]:
        pass


class AbstractGenreRepository(Protocol):
    async def get_by_id(self, genre_id: UUID4) -> Genre | None:
        pass

    async def query(self) -> list[Genre]:
        pass


class AbstractCacheRepository(Protocol):
    async def get(self, key: str) -> Any | None:
        pass

    async def set(self, name: str, value: Any) -> None:
        pass

    async def clear(self) -> None:
        pass

    async def ping(self) -> bool:
        pass
