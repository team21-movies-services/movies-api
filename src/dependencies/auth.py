import logging
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

import src.exceptions.auth as auth_exceptions
from src.api.errors import APIErrorDetail
from src.models.auth import AuthData
from src.services.auth import AuthServiceABC, get_auth_service

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

logger = logging.getLogger(__name__)


async def get_auth_user(
    auth_service: AuthServiceABC = Depends(get_auth_service),
    access_token: Optional[str] = Security(api_key_header),
):
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        auth_data: AuthData = await auth_service.validate_access_token(access_token)
    except auth_exceptions.TokenException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    except auth_exceptions.TokenExpiredException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": {"message": APIErrorDetail.TOKEN_EXPIRED}},
        )
    logger.debug(f"User request: user_id - {auth_data.user_id}")
    return auth_data


async def get_auth_admin(
    auth_data: AuthData = Depends(get_auth_user),
):
    if not auth_data.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return auth_data
