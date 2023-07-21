from src.exceptions.base import AppException


class RedisException(AppException):
    """Base Redis Exception"""


class RedisNotInitException(RedisException):
    """Redis not initialized"""
