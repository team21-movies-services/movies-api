from enum import StrEnum
from http import HTTPStatus

from elasticsearch.exceptions import RequestError
from fastapi import Request, Response
from fastapi.responses import ORJSONResponse


class APIErrorDetail(StrEnum):
    FILM_NOT_FOUND = "film not found"
    GENRE_NOT_FOUND = "genre not found"
    PERSON_NOT_FOUND = "person not found"
    ELASTIC_SEARCH_AFTER = "incorrect value for search_after field"

    TOKEN_EXPIRED = "Error validating access token: Session has expired"


async def elasticsearch_handler(request: Request, exc: RequestError) -> Response:
    """Обработчик ошибок elasticsearch."""

    if exc.error == "search_phase_execution_exception":
        response = ORJSONResponse(
            {
                "detail": APIErrorDetail.ELASTIC_SEARCH_AFTER,
            },
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        )
    else:
        response = ORJSONResponse(
            {
                "detail": HTTPStatus.BAD_REQUEST.description,
            },
            status_code=HTTPStatus.BAD_REQUEST,
        )
    return response
