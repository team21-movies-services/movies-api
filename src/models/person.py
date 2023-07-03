from enum import StrEnum

from pydantic import UUID4

from .common import BaseOrjsonModel


class RoleEnum(StrEnum):
    WRITER = "writer"
    DIRECTOR = "director"
    ACTOR = "actor"


class RoleFilm(BaseOrjsonModel):
    uuid: UUID4
    roles: list[RoleEnum]


class Person(BaseOrjsonModel):
    uuid: UUID4
    full_name: str
    films: list[RoleFilm]
