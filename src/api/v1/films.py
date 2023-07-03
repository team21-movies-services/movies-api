from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import UUID4

from src.api.errors import APIErrorDetail
from src.api.request_models.film_request import FilmsListQueryParams, FilmsSearchQueryParams
from src.api.response_models.film_response import Film, FilmsSearchResponse
from src.models.search import FilmsSearchParams
from src.services.films import FilmsService, get_films_service

router = APIRouter(tags=["Films"])


@router.get(
    "/search",
    status_code=HTTPStatus.OK,
    summary="performs search for the most relevant films",
)
@cache()
async def films_search(
    query_params: FilmsSearchQueryParams = Depends(),
    films_service: FilmsService = Depends(get_films_service),
) -> FilmsSearchResponse:
    films_search_params = FilmsSearchParams(
        query=query_params.query,
        page_number=query_params.page_number,
        page_size=query_params.page_size,
        search_after=query_params.search_after,
    )

    pages, search_after, items = await films_service.query_with_pagination(films_search_params)

    return FilmsSearchResponse(pages=pages, search_after=search_after, items=items)


@router.get(
    "/{film_uuid}",
    status_code=HTTPStatus.OK,
    summary="returns detailed information about film",
)
@cache()
async def film_details(
    film_uuid: UUID4,
    films_service: FilmsService = Depends(get_films_service),
) -> Film:
    film = await films_service.get_by_id(film_uuid)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=APIErrorDetail.FILM_NOT_FOUND)

    return film


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    summary="returns films list according to provided filters",
)
@cache()
async def films_list(
    query_params: FilmsListQueryParams = Depends(),
    films_service: FilmsService = Depends(get_films_service),
) -> FilmsSearchResponse:
    films_search_params = FilmsSearchParams(
        sort=query_params.sort,
        genre=query_params.genre,
        page_number=query_params.page_number,
        page_size=query_params.page_size,
        search_after=query_params.search_after,
    )

    pages, search_after, items = await films_service.query_with_pagination(films_search_params)

    return FilmsSearchResponse(pages=pages, search_after=search_after, items=items)
