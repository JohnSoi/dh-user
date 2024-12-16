"""Репозиторий пользователя"""

__author__: str = "Старков Е.П."


from typing import Type, Any

from dh_auth.repository import AccessDataRepository
from dh_base.repositories import BaseRepository
from dh_base.schemas import NavigationSchema
from sqlalchemy import Select
from sqlalchemy.orm import DeclarativeMeta

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

    async def list(
        self, filters: dict[str, Any], navigation: NavigationSchema | None = None
    ) -> list[DeclarativeMeta]:
        if filters and filters.get("role_id"):
            access_data = await AccessDataRepository().list({"role_id": filters.get("role_id")})
            del filters["role_id"]
            filters["user_ids"] = [data.user_id for data in (access_data or [])]

        return super().list(filters, navigation)

    @staticmethod
    def _before_list(query: Select, filters: dict[str, Any]) -> Select:
        if not filters:
            return query

        if filters.get("user_ids"):
            query = query.where(UserModel.id in filters.get("user_ids"))

        return query
