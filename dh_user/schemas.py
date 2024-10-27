# pylint: disable=unnecessary-pass
"""Схемы данных для работы с пользователем"""

__author__: str = 'Старков Е.П.'


from datetime import date
from typing import List
from uuid import UUID

from pydantic import BaseModel

from dh_auth.schemas import AuthData, RoleAuth, AccessDataPublic, SessionPublicData
from step_vpn_service.contacts.schemas import ContactRegisterData
from step_vpn_service.contacts.schemas import ContactPublicData


class UserMainInfo(BaseModel):
    """Основная информация"""
    name: str
    surname: str
    second_name: str


class UserExtraInfo(BaseModel):
    """Дополнительная информация"""
    date_birthday: date
    gender: int


class UserData(UserMainInfo, UserExtraInfo):
    """Публичные данные пользователя"""
    id: int
    uuid: UUID

    access_data: AccessDataPublic
    session: SessionPublicData
    contacts: List[ContactPublicData]


class RegisterData(UserMainInfo, UserExtraInfo, ContactRegisterData, AuthData, RoleAuth):
    """Данные для регистрации"""
    pass


class DeleteOrBlockUserIn(BaseModel):
    """Данные бля блокировки или удаления пользователя"""
    id: int
