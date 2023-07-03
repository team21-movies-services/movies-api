from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import UUID4

from src.api.errors import APIErrorDetail
from src.api.request_models.person_request import PersonSearchQueryParams
from src.api.response_models.film_response import FilmListItem
from src.api.response_models.person_response import PersonsSearchResponse
from src.models.person import Person
from src.models.search import FilmsSearchParams, PersonSearchParams
from src.services.films import FilmsService, get_films_service
from src.services.persons import PersonService, get_person_service

router = APIRouter(tags=["Persons"])


@router.get(
    "/search",
    status_code=HTTPStatus.OK,
    summary="performs search for the most relevant persons",
)
@cache()
async def persons_search(
    query_params: PersonSearchQueryParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> PersonsSearchResponse:
    person_search_params = PersonSearchParams(
        query=query_params.query,
        page_number=query_params.page_number,
        page_size=query_params.page_size,
        sort=query_params.sort,
        search_after=query_params.search_after,
    )

    pages, search_after, items = await person_service.query_with_pagination(person_search_params)

    return PersonsSearchResponse(pages=pages, search_after=search_after, items=items)


@router.get(
    "/{person_uuid}",
    status_code=HTTPStatus.OK,
    summary="returns information about person",
)
@cache()
async def person_details(
    person_uuid: UUID4,
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_id(person_uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=APIErrorDetail.PERSON_NOT_FOUND)
    return person


@router.get(
    "/{person_uuid}/film",
    status_code=HTTPStatus.OK,
    summary="returns films person",
)
@cache()
async def person_films(
    person_uuid: UUID4,
    films_service: FilmsService = Depends(get_films_service),
) -> list[FilmListItem]:
    film_search_params = FilmsSearchParams(person=person_uuid)
    film_details = await films_service.query(film_search_params)
    return film_details
