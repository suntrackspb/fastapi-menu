from sqlalchemy import func
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

    async def get_list_without_id(self) -> list[dict] | None:
        dish_subquery = (
            select(
                Dish.submenu_id,
                func.json_agg(
                    func.json_build_object(
                        "title", Dish.title,
                        "description", Dish.description,
                        "price", Dish.price,
                    ),
                ).label("dishes"),
            )
            .select_from(Dish)
            .group_by(Dish.submenu_id)
            .subquery()
        )

        submenu_subquery = (
            select(
                Submenu.menu_id,
                func.json_agg(
                    func.json_build_object(
                        "title", Submenu.title,
                        "description", Submenu.description,
                        "dishes", dish_subquery.c.dishes,
                    ),
                ).label("submenus"),
            )
            .select_from(Submenu)
            .group_by(Submenu.menu_id)
            .join(dish_subquery, dish_subquery.c.submenu_id == Submenu.id)
            .subquery()
        )

        query = (
            select(
                Menu.title,
                Menu.description,
                submenu_subquery.c.submenus,
            )
            .select_from(Menu)
            .join(submenu_subquery, submenu_subquery.c.menu_id == Menu.id)
        )

        db_response = await self.db.execute(query)
        return [dict(data) for data in db_response]
