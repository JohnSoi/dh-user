"""Репозиторий пользователя"""

__author__: str = "Старков Е.П."


from typing import Type, Any

from dh_auth.repository import AccessDataRepository
from dh_base.repositories import BaseRepository
from sqlalchemy import Select

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
        return "surname"

    @staticmethod
    async def _before_list(query: Select, filters: dict[str, Any]) -> Select:
        if not filters:
            return query

        if filters.get("role_id"):
            access_data = await AccessDataRepository().list({"role_id": filters.get("role_id")})
            query = query.where(UserModel.id in (data.user_id for data in (access_data or [])))

        return query
