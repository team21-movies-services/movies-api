from typing import Any

from pydantic import BaseModel

from src.models.person import Person


class PersonsSearchResponse(BaseModel):
    pages: int
    search_after: list[Any] | None
    items: list[Person]
