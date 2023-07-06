from src.exceptions.base import AppException


class AuthException(AppException):
    """Base Token Exception"""


class TokenException(AuthException):
    """Base Token Exception"""


class TokenDecodeException(TokenException):
    """Token Decode Exception"""


class TokenExpiredException(AuthException):
    """Token Expired Exception"""
