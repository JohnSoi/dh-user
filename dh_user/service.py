"""Работа с пользователями"""

__author__: str = 'Старков Е.П.'


from typing import Any, NoReturn
from uuid import uuid4, UUID

from dh_auth.consts import ADMIN_ROLE_KEY
from dh_auth.exceptions import LoginExist, NotAccessOperation
from dh_auth.celery_tasks.email_sender import send_confirm_email
from step_vpn_service.contacts.consts import ContactType
from step_vpn_service.contacts.model import ContactModel
from step_vpn_service.contacts.repository import ContactRepository
from .exceptions import UserNotFound
from .model import UserModel
from .schemas import RegisterData
from .repository import UserRepository
from dh_auth.helpers.auth import get_password_hash
from dh_auth.repository import AccessDataRepository, ConfirmEmailRepository
from dh_base.database import Base


class UserService:
    """Сервис для работы с пользователями"""
    @classmethod
    async def register_user(cls, payload: RegisterData) -> dict[str, Any]:
        """
        Регистрация пользователей

        @param payload: данные для регистрации
        @return: информация о пользователе
        """
        await cls._check_contacts(payload.email, payload.phone)
        await cls._check_login(payload.login)

        user_data: Base = await UserRepository().create(payload.dict())
        contact_id: int = await cls._create_additional_data(payload, user_data.id)

        email: str = await user_data.email_value
        await cls._send_confirm_email(email, user_data.id, contact_id)

        return user_data

    @classmethod
    async def block_user(cls, user_id: int, user: UserModel) -> None:
        """Блокировка пользователя"""
        access_data: UserModel = await AccessDataRepository().get_data_with_permission(
            user_id, user
        )

        await AccessDataRepository().update(access_data.id, {'is_active': False})

    @classmethod
    async def delete_user(cls, user_id: int, user: UserModel) -> None:
        """Удаление пользователя"""
        user_repository: UserRepository = UserRepository()
        user_data: UserModel = await user_repository.get(user_id)

        if not user_data:
            raise UserNotFound()

        if user_id != user.id and user.access_data.role.key != ADMIN_ROLE_KEY:
            raise NotAccessOperation()

        await user_repository.delete(user_id)

    @classmethod
    async def _send_confirm_email(cls, email: str, user_id: int, contact_id: int) -> None:
        """
        Отправка письма о подтверждении почты

        @param email: почта
        @param user_id: идентификатор пользователя
        @param contact_id: идентификатор контакта
        """
        token: UUID = uuid4()
        await ConfirmEmailRepository().create({
            'user_id': user_id,
            'contact_id': contact_id,
            'token': token
        })
        send_confirm_email.delay(f'/auth/confirm_email/{token}', email)

    @classmethod
    async def _check_contacts(cls, email: str, phone: str | None) -> NoReturn:
        """
        Проверяет контакты, что они не существуют

        @param email:
        @param phone:
        @return:
        """
        contact_repository: ContactRepository = ContactRepository()
        await contact_repository.check_email_exist(email)

        if phone:
            await contact_repository.check_phone_exist(phone)

    @classmethod
    async def _check_login(cls, login: str) -> NoReturn:
        """
        Проверяет, что логин не занят

        @param login: логин
        """
        login_already_exist: bool = await AccessDataRepository().find_one_or_none(login=login)

        if login_already_exist:
            raise LoginExist()

    @classmethod
    async def _create_additional_data(cls, payload: RegisterData, user_id: int) -> int:
        """
        Создание дополнительных данных при регистрации:
        1. Данные для входа
        2. Почту в контакты
        3. Телефон, если есть

        @param payload: данные о регистрации
        @param user_id: идентификатор пользователя
        @return: идентификатор добавленной почты
        """
        contact_repository: ContactRepository = ContactRepository()
        await AccessDataRepository().create({
            'login': payload.login,
            'password': get_password_hash(payload.password),
            'user_id': user_id,
            'role_id': payload.role_id
        })

        contact_data: ContactModel = await contact_repository.create({
            'value': payload.email,
            'type': ContactType.EMAIL,
            'user_id': user_id,
            'is_main': True
        })

        if payload.phone:
            await contact_repository.create({
                'value': payload.phone,
                'type': ContactType.PHONE,
                'user_id': user_id,
                'is_main': True
            })

        return contact_data.id
