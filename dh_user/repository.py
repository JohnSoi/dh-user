"""Репозиторий пользователя"""

__author__: str = "Старков Е.П."


from typing import Type

from dh_base.repositories import BaseRepository

from .model import UserModel


class UserRepository(BaseRepository):
    """Репозиторий пользователя"""

    @property
    def model(self) -> Type[UserModel]:
        """Модель пользователей"""
        return UserModel

    @property
    def ordering_field_name(self) -> str:
        """Поле сортировки"""
        return UserModel.__table__.c.name
