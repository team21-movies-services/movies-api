from http import HTTPStatus

from fastapi import APIRouter

from src.api.response_models.status_response import StatusResponse
from src.services.status import statusService

router = APIRouter(tags=["Status"])


@router.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=StatusResponse,
    summary="Проверить статус сервисов",
)
async def check_status_request(status_service: statusService) -> StatusResponse:
    return await status_service.get_status_of_services()
