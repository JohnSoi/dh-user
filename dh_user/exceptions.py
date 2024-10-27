"""Исключения пользователей"""

__author__: str = 'Старков Е.П.'


from fastapi import status

from dh_base.exceptions import BaseAppException


class UserNotFound(BaseAppException):
    """Пользователь не найден"""
    STATUS_CODE: int = status.HTTP_409_CONFLICT
    DETAIL: str = 'Пользователь не найден в системе'
