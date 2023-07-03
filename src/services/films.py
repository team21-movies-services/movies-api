from fastapi import Depends
from pydantic import UUID4

from src.db.abstract import AbstractFilmRepository, SearchAfterType
from src.db.elastic.repositories import get_film_repository
from src.models.film import FilmDetail
from src.models.search import FilmsSearchParams


class FilmsService:
    def __init__(self, film_repository: AbstractFilmRepository):
        self._film_repository = film_repository

    async def get_by_id(self, film_id: UUID4) -> FilmDetail | None:
        return await self._film_repository.get_by_id(film_id)

    async def query(self, films_search_params: FilmsSearchParams) -> list[FilmDetail]:
        return await self._film_repository.query(films_search_params)

    async def query_with_pagination(
        self,
        films_search_params: FilmsSearchParams,
    ) -> tuple[int, SearchAfterType, list[FilmDetail]]:
        return await self._film_repository.query_with_pagination(films_search_params)


def get_films_service(
    film_repository: AbstractFilmRepository = Depends(get_film_repository),
) -> FilmsService:
    return FilmsService(film_repository)
