from typing import Any

from pydantic import UUID4, BaseModel

from .common import BaseOrjsonModel
from .genre_response import GenreResponse
from .person_response import PersonResponse


class FilmResponse(BaseOrjsonModel):
    uuid: UUID4
    title: str
    imdb_rating: float


class FilmsSearchResponse(BaseModel):
    pages: int
    search_after: list[Any] | None
    items: list[FilmResponse]


class FilmDetailResponse(FilmResponse):
    description: str | None
    genre: list[GenreResponse]
    actors: list[PersonResponse]
    writers: list[PersonResponse]
    directors: list[PersonResponse]
