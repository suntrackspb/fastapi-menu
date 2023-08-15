from sqlalchemy.future import select
from sqlalchemy.orm import Session, subqueryload

from app.models.models import Menu, Submenu


class DataCrud:
    def __init__(self, db: Session):
        self.db = db

    async def get_list_with_id(self) -> list[dict]:
        return (
            await self.db.execute(
                select(Menu).options(subqueryload(Menu.submenus).subqueryload(Submenu.dishes)),
            )
        ).scalars().fetchall()
