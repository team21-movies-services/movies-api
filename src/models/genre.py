from pydantic import UUID4

from .common import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    uuid: UUID4
    name: str
