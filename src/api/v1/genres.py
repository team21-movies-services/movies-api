from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from pydantic import UUID4

from src.api.errors import APIErrorDetail
from src.models.genre import Genre
from src.services.genres import GenreService, get_genre_service

router = APIRouter(tags=["Genres"])


@router.get(
    "/{genre_uuid}",
    status_code=HTTPStatus.OK,
    summary="returns information about genre",
)
@cache()
async def genre_details(
    genre_uuid: UUID4,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_id(genre_uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=APIErrorDetail.GENRE_NOT_FOUND)
    return genre


@router.get(
    "/",
    status_code=HTTPStatus.OK,
    summary="returns genres list",
)
@cache()
async def genres_list(genre_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    return await genre_service.query()
