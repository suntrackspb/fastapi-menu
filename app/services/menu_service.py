from fastapi import BackgroundTasks, HTTPException

from app.crud.menu import MenuCrud
from app.schemas.menu import MenuCreate, MenuUpdate
from app.services.cache_service import CacheService


class MenuService:
    def __init__(self, crud: MenuCrud, cache: CacheService):
        self.crud = crud
        self.cache = cache

    async def get_menus(self):
        cached_data = await self.cache.get("menu_list")
        if cached_data:
            db_menus = cached_data
        else:
            db_menus = await self.crud.get_list()
            await self.cache.set_all("menu_list", db_menus)
        return db_menus

    async def get_menu(self, menu_id: str):
        cached_data = await self.cache.get(f"menu_{menu_id}")
        if cached_data:
            db_menu = cached_data
        else:
            db_menu = await self.crud.get(menu_id)
            if db_menu is None:
                raise HTTPException(status_code=404, detail="menu not found")
            await self.cache.set(f"menu_{menu_id}", db_menu)
        return db_menu

    async def create_menu(self, menu: MenuCreate, background_tasks: BackgroundTasks):
        db_menu = await self.crud.get_by_title(title=menu.title)
        if db_menu:
            raise HTTPException(
                status_code=400,
                detail="menu with this title already exist",
            )
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return await self.crud.create(menu=menu)

    async def update_menu(self, menu_id: str, menu: MenuUpdate, background_tasks: BackgroundTasks):
        db_menu = await self.crud.get(menu_id=menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail="menu not found")
        updated_menu = await self.crud.update(menu=menu, menu_id=menu_id)
        await self.cache.set(f"menu_{menu_id}", updated_menu)
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return updated_menu

    async def delete_menu(self, menu_id: str, background_tasks: BackgroundTasks):
        db_menu = await self.crud.get(menu_id=menu_id)
        if db_menu is None:
            raise HTTPException(status_code=404, detail="menu not found")
        await self.crud.delete(menu_id=menu_id)
        background_tasks.add_task(self.cache.delete, f"menu_{menu_id}")
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return {"status": "true", "message": "The menu has been deleted"}
