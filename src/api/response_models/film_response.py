from typing import Any

from pydantic import UUID4, BaseModel


class FilmListItem(BaseModel):
    uuid: UUID4
    title: str
    imdb_rating: float


class FilmsSearchResponse(BaseModel):
    pages: int
    search_after: list[Any] | None
    items: list[FilmListItem]


class FilmGenre(BaseModel):
    uuid: UUID4
    name: str


class FilmPerson(BaseModel):
    uuid: UUID4
    full_name: str


class Film(BaseModel):
    uuid: UUID4
    title: str
    imdb_rating: float
    description: str
    genre: list[FilmGenre]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]
