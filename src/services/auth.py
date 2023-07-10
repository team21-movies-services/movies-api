import jwt

import logging
from uuid import UUID
from abc import ABC, abstractmethod
import src.exceptions.auth as auth_exceptions
from src.core.config import config

from src.models.auth import AuthData

logger = logging.getLogger(__name__)


class AuthServiceABC(ABC):

    @abstractmethod
    async def validate_access_token(self, access_token: str) -> AuthData:
        ...


class AuthService(AuthServiceABC):
    encode_algorithm: str = "HS256"

    def __init__(self, jwt_secret_key: str) -> None:
        self.jwt_secret_key = jwt_secret_key

    def _validate_token(self, token: str) -> dict:

        try:
            payload: dict = jwt.decode(token, self.jwt_secret_key, algorithms=[self.encode_algorithm])
        except (
                jwt.DecodeError,
                jwt.InvalidKeyError,
                jwt.InvalidIssuerError,
                jwt.InvalidSignatureError,
        ):
            logger.error(f"Can't decode jwt token! See {token}")
            raise auth_exceptions.TokenDecodeException()

        except jwt.exceptions.ExpiredSignatureError as error:
            logger.warning(f"Token is expired! error = {error}")
            raise auth_exceptions.TokenExpiredException()

        logger.info(">>> Payload %s", payload)

        return payload

    async def validate_access_token(self, access_token: str) -> AuthData:
        """Валидация access токена."""
        payload = self._validate_token(access_token)
        user_id = payload.get('user_id')
        is_superuser = payload.get('is_superuser', False)
        if not user_id:
            logger.error(f"Can't get user_id from access token! {access_token}")
            raise auth_exceptions.TokenDecodeException()

        return AuthData(user_id=UUID(user_id), is_superuser=is_superuser)


def get_auth_service() -> AuthServiceABC:
    return AuthService(config.jwt_secret_key)
