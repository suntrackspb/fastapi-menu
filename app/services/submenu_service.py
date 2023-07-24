from fastapi import HTTPException

from app.crud.submenu import SubmenuCrud
from app.schemas.submenu import SubmenuCreate, SubmenuUpdate


class SubmenuService:
    def __init__(self, crud: SubmenuCrud):
        self.crud = crud

    async def get_submenus(self):
        db_submenus = await self.crud.get_list()
        return db_submenus

    async def get_submenu(self, submenu_id: str):
        db_submenu = await self.crud.get(submenu_id)
        if db_submenu is None:
            raise HTTPException(
                status_code=404, detail='submenu not found',
            )
        return db_submenu

    async def create_submenu(
            self,
            menu_id: str,
            submenu: SubmenuCreate,
    ):
        db_submenu = await self.crud.get_by_title(title=submenu.title)
        if db_submenu:
            raise HTTPException(
                status_code=400,
                detail='submenu with this title already exist',
            )
        return await self.crud.create(
            submenu=submenu,
            menu_id=menu_id,
        )

    async def update_submenu(
            self, submenu_id: str,
            menu_id: str,
            submenu: SubmenuUpdate,
    ):
        db_submenu = await self.crud.get(submenu_id=submenu_id)
        if db_submenu is None:
            raise HTTPException(status_code=404, detail='submenu not found')
        updated_submenu = await self.crud.update(
            submenu=submenu,
            submenu_id=submenu_id,
            menu_id=menu_id,
        )
        return updated_submenu

    async def delete_submenu(
            self, menu_id: str,
            submenu_id: str,
    ):
        db_submenu = await self.crud.get(submenu_id=submenu_id)
        if db_submenu is None:
            raise HTTPException(status_code=404, detail='submenu not found')
        await self.crud.delete(submenu_id=submenu_id)
        return {'status': 'true', 'message': 'The menu has been deleted'}
