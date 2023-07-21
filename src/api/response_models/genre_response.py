from pydantic import UUID4

from .common import BaseOrjsonModel


class GenreResponse(BaseOrjsonModel):
    uuid: UUID4
    name: str
