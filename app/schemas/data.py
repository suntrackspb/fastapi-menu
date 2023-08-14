from uuid import UUID

from pydantic import BaseModel

from app.schemas.dish import DishGet
from app.schemas.menu import MenuGet
from app.schemas.submenu import SubmenuGet


class DishesFull(list[DishGet]):
    submenu_id: UUID


class SubmenusFull(list[SubmenuGet]):
    menu_id: UUID
    dishes: list[DishesFull]


class MenusFull(MenuGet):
    submenus: list[SubmenuGet]


class MessageStatus(BaseModel):
    status: str
    message: str
