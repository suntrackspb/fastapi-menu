from fastapi import HTTPException

from app.crud.menu import MenuCrud
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuService:
    def __init__(self, crud: MenuCrud):
        self.crud = crud

    async def get_menus(self):
        db_menus = await self.crud.get_list()
        return db_menus

    async def get_menu(self, menu_id: str):
        db_menu = await self.crud.get(menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')
        return db_menu

    async def create_menu(self, menu: MenuCreate):
        db_menu = await self.crud.get_by_title(title=menu.title)
        if db_menu:
            raise HTTPException(
                status_code=400,
                detail='menu with this title already exist',
            )
        return await self.crud.create(menu=menu)

    async def update_menu(self, menu_id: str, menu: MenuUpdate):
        db_menu = await self.crud.get(menu_id=menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')
        updated_menu = await self.crud.update(menu=menu, menu_id=menu_id)
        return updated_menu

    async def delete_menu(self, menu_id: str):
        db_menu = await self.crud.get(menu_id=menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail='menu not found')
        await self.crud.delete(menu_id=menu_id)
        return {'status': 'true', 'message': 'The menu has been deleted'}
