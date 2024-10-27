"""Модели пользователя"""

__author__: str = 'Старков Е.П.'

from datetime import date
from typing import List

from sqlalchemy import String, Date, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from step_vpn_service.contacts.model import ContactModel
from step_vpn_service.contacts.consts import ContactType
from step_vpn_service.contacts.repository import ContactRepository

from dh_base.columns import IdColumns, DateEditColumns
from dh_base.database import Base


class UserModel(IdColumns, DateEditColumns, Base):
    """Модель пользователя"""
    __tablename__: str = 'users'

    name: Mapped[str] = mapped_column(String(40), index=True)
    surname: Mapped[str] = mapped_column(String(40), index=True)
    second_name: Mapped[str] = mapped_column(String(40), nullable=True)

    date_birthday: Mapped[date] = mapped_column(Date)
    gender: Mapped[int] = mapped_column(SmallInteger)

    access_data: Mapped['AccessDataModel'] = relationship(back_populates='user', lazy=False)
    session: Mapped['SessionModel'] = relationship(back_populates='user', lazy=False)
    contacts: Mapped[List['ContactModel']] = relationship(back_populates='user', lazy=False)

    @property
    def full_name(self) -> str:
        """ФИО пользователя"""
        result: str = f'{self.surname} {self.name}'

        if self.second_name:
            result += f' {self.second_name}'

        return result

    @property
    async def email_value(self) -> str:
        """Основная почта"""
        contact_data: ContactModel = await ContactRepository().find_one_or_none(
            user_id=self.id, type=ContactType.EMAIL, is_main=True
        )

        return contact_data.value
