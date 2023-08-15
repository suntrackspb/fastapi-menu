from sqlalchemy.future import select
from sqlalchemy.orm import Session, subqueryload

from app.models.models import Dish, Menu, Submenu


class DataCrud:
    def __init__(self, db: Session):
        self.db = db

    async def get_submenu(self, submenu_id: str):
        db_submenu = await self.db.get(Submenu, submenu_id)
        if db_submenu is None:
            return None
        return db_submenu

    async def get_dish_by_title(self, key: str, value: str) -> Dish | None:
        result = await self.db.execute(
            select(Dish).where(getattr(Dish, key) == value),
        )
        dish = result.scalars().first()
        if dish:
            return dish
        return None

    async def get_submenu_by_title(self, key: str, value: str) -> Submenu | None:
        result = await self.db.execute(
            select(Submenu).where(getattr(Submenu, key) == value),
        )
        submenu = result.scalars().first()
        if submenu:
            return submenu
        return None

    async def get_menu_by_title(self, key: str, value: str) -> Menu | None:
        result = await self.db.execute(
            select(Menu).where(getattr(Menu, key) == value),
        )
        menu = result.scalars().first()
        if menu:
            return menu
        return None

    async def get_list_with_id(self) -> list[dict]:
        return (
            await self.db.execute(
                select(Menu).options(subqueryload(Menu.submenus).subqueryload(Submenu.dishes)),
            )
        ).scalars().fetchall()
