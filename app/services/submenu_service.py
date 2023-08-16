from fastapi import BackgroundTasks, HTTPException

from app.crud.submenu import SubmenuCrud
from app.schemas.submenu import SubmenuCreate, SubmenuUpdate
from app.services.cache_service import CacheService


class SubmenuService:
    def __init__(self, crud: SubmenuCrud, cache: CacheService):
        self.crud = crud
        self.cache = cache

    async def get_submenus(self, menu_id: str):
        cached_data = await self.cache.get("submenu_list")
        if cached_data:
            db_submenus = cached_data
        else:
            db_submenus = await self.crud.get_list(menu_id)
            cached_data = await self.cache.set_all("submenu_list", db_submenus)
        return db_submenus

    async def get_submenu(self, submenu_id: str):
        cached_data = await self.cache.get(f"submenu_{submenu_id}")
        if cached_data:
            db_submenu = cached_data
        else:
            db_submenu = await self.crud.get(submenu_id)
            if db_submenu is None:
                raise HTTPException(
                    status_code=404,
                    detail="submenu not found",
                )
            await self.cache.set(
                f"submenu_{submenu_id}",
                db_submenu,
            )
        return db_submenu

    async def create_submenu(
        self,
        menu_id: str,
        submenu: SubmenuCreate,
        background_tasks: BackgroundTasks,
    ):
        db_submenu = await self.crud.get_by_title(title=submenu.title)
        if db_submenu:
            raise HTTPException(
                status_code=400,
                detail="submenu with this title already exist",
            )
        background_tasks.add_task(self.cache.delete, f"menu_{menu_id}")
        background_tasks.add_task(self.cache.delete, "submenu_list")
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return await self.crud.create(
            submenu=submenu,
            menu_id=menu_id,
        )

    async def update_submenu(
        self,
        submenu_id: str,
        submenu: SubmenuUpdate,
        background_tasks: BackgroundTasks,
    ):
        db_submenu = await self.crud.get(submenu_id=submenu_id)
        if db_submenu is None:
            raise HTTPException(status_code=404, detail="submenu not found")
        updated_submenu = await self.crud.update(
            submenu=submenu,
            submenu_id=submenu_id,
        )
        await self.cache.set(f"submenu_{submenu_id}", updated_submenu)
        background_tasks.add_task(self.cache.delete, "submenu_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return updated_submenu

    async def delete_submenu(
        self,
        menu_id: str,
        submenu_id: str,
        background_tasks: BackgroundTasks,
    ):
        db_submenu = await self.crud.get(submenu_id=submenu_id)
        if db_submenu is None:
            raise HTTPException(status_code=404, detail="submenu not found")

        await self.crud.delete(submenu_id=submenu_id)
        background_tasks.add_task(self.cache.delete, f"menu_{menu_id}")
        background_tasks.add_task(self.cache.delete, f"submenu_{submenu_id}")
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "submenu_list")
        background_tasks.add_task(self.cache.delete, "dish_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")

        return {"status": "true", "message": "The menu has been deleted"}
