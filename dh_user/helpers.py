"""Хелперы пользователей"""

__author__: str = 'Старков Е.П.'


from fastapi import Depends
from dh_auth.helpers import get_token, get_user_id_from_token
from dh_auth.exceptions.access_data import NoActiveAccessData

from .model import UserModel
from .repository import UserRepository


async def get_current_user(access_token: str = Depends(get_token)) -> UserModel:
    """
    Получение текущего пользователя с проверкой

    @param access_token: токен доступа
    @return: данные о пользователе
    """
    user_id: int = await get_user_id_from_token(access_token)
    user: UserModel = await UserRepository().get(user_id)

    if not user.access_data or not user.access_data.is_active:
        raise NoActiveAccessData()

    return user
