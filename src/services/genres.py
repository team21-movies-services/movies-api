from fastapi import Depends
from pydantic import UUID4

from src.api.response_models.genre_response import GenreResponse
from src.db.abstract import AbstractGenreRepository
from src.db.elastic.repositories import get_genre_repository


class GenreService:
    def __init__(self, genre_repository: AbstractGenreRepository):
        self._genre_repository = genre_repository

    async def get_by_id(self, genre_id: UUID4) -> GenreResponse | None:
        return await self._genre_repository.get_by_id(genre_id)

    async def query(self) -> list[GenreResponse]:
        return await self._genre_repository.query()


def get_genre_service(
    genre_repository: AbstractGenreRepository = Depends(get_genre_repository),
) -> GenreService:
    return GenreService(genre_repository)
