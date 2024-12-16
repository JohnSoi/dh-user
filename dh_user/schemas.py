# pylint: disable=unnecessary-pass
"""Схемы данных для работы с пользователем"""

__author__: str = "Старков Е.П."


from uuid import UUID
from typing import List
from datetime import date

from pydantic import BaseModel
from dh_auth.schemas import AuthData, RoleAuth, AccessDataPublic, SessionPublicData
from dh_contact.schemas import ContactPublicData, ContactRegisterData


class UserMainInfo(BaseModel):
    """Основная информация"""

    name: str
    surname: str
    second_name: str


class UserExtraInfo(BaseModel):
    """Дополнительная информация"""

    date_birthday: date
    gender: int


class UserInfo(UserMainInfo, UserExtraInfo):
    id: int
    uuid: UUID
    full_name: str


class UserData(UserInfo):
    """Публичные данные пользователя"""

    access_data: AccessDataPublic
    session: SessionPublicData
    contacts: List[ContactPublicData]


class RegisterData(UserMainInfo, UserExtraInfo, ContactRegisterData, AuthData, RoleAuth):
    """Данные для регистрации"""

    pass


class DeleteOrBlockUserIn(BaseModel):
    """Данные бля блокировки или удаления пользователя"""

    id: int
