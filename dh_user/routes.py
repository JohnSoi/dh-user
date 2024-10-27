"""Конечные точки пользователей"""

__author__: str = "Старков Е.П."

from typing import Any

from fastapi import Depends, APIRouter
from dh_base.schemas import SimpleOperationResult

from .model import UserModel
from .helpers import get_current_user
from .schemas import UserData, RegisterData, DeleteOrBlockUserIn
from .service import UserService

router: APIRouter = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", description="Регистрирует пользователя", response_model=UserData)
async def register(payload: RegisterData) -> dict[str, Any]:
    """Регистрация"""
    return await UserService.register_user(payload)


@router.post("/block", description="Блокирует пользователя", response_model=SimpleOperationResult)
async def block(payload: DeleteOrBlockUserIn, user: UserModel = Depends(get_current_user)) -> dict[str, bool]:
    """Блокировка"""
    await UserService.block_user(payload.id, user)
    return {"success": True}


@router.post(
    "/delete",
    description="Помечает пользователя на удаление",
    response_model=SimpleOperationResult,
)
async def mark_for_delete(payload: DeleteOrBlockUserIn, user: UserModel = Depends(get_current_user)) -> dict[str, bool]:
    """Пометка на удаление"""
    await UserService.delete_user(payload.id, user)
    return {"success": True}


@router.post("/me", description="Данные текущего пользователя", response_model=UserData)
def get_me(user: UserModel = Depends(get_current_user)):
    """Данные о текущем пользователе"""
    return user
