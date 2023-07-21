from enum import StrEnum
from typing import Any

from pydantic import UUID4

from .common import BaseOrjsonModel


class RoleEnum(StrEnum):
    WRITER = "writer"
    DIRECTOR = "director"
    ACTOR = "actor"


class PersonResponse(BaseOrjsonModel):
    uuid: UUID4
    full_name: str


class RoleFilmResponse(BaseOrjsonModel):
    uuid: UUID4
    roles: list[RoleEnum]


class PersonFilmResponse(PersonResponse):
    films: list[RoleFilmResponse]


class PersonsSearchResponse(BaseOrjsonModel):
    pages: int
    search_after: list[Any] | None
    items: list[PersonFilmResponse]
