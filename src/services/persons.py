from fastapi import Depends
from pydantic import UUID4

from src.db.abstract import AbstractPersonRepository, SearchAfterType
from src.db.elastic.repositories import get_person_repository
from src.models.person import Person
from src.models.search import PersonSearchParams


class PersonService:
    def __init__(self, person_repository: AbstractPersonRepository):
        self._person_repository = person_repository

    async def get_by_id(self, person_id: UUID4) -> Person | None:
        return await self._person_repository.get_by_id(person_id)

    async def query_with_pagination(
        self,
        person_search_params: PersonSearchParams,
    ) -> tuple[int, SearchAfterType, list[Person]]:
        return await self._person_repository.query_with_pagination(person_search_params)


def get_person_service(
    person_repository: AbstractPersonRepository = Depends(get_person_repository),
) -> PersonService:
    return PersonService(person_repository)
