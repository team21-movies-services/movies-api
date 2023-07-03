from pydantic import UUID4

from src.models.genre import Genre

from .common import BaseOrjsonModel


class FilmPerson(BaseOrjsonModel):
    uuid: UUID4
    full_name: str


class Film(BaseOrjsonModel):
    uuid: UUID4
    title: str
    imdb_rating: float


class FilmDetail(Film):
    description: str
    genre: list[Genre]
    actors: list[FilmPerson]
    writers: list[FilmPerson]
    directors: list[FilmPerson]
