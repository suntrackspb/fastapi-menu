from fastapi import BackgroundTasks, HTTPException

from app.crud.dish import DishCrud
from app.schemas.dish import DishCreate, DishUpdate
from app.services.cache_service import CacheService


class DishService:
    def __init__(self, crud: DishCrud, cache: CacheService):
        self.crud = crud
        self.cache = cache

    async def get_dishes(self):
        cached_data = await self.cache.get("dish_list")
        if cached_data:
            db_dishes = cached_data
        else:
            db_dishes = await self.crud.get_list()
            await self.cache.set_all("dish_list", db_dishes)
        return db_dishes

    async def get_dish(self, dish_id: str):
        cached_data = await self.cache.get(f"dish_{dish_id}")
        if cached_data:
            db_dish = cached_data
        else:
            db_dish = await self.crud.get(dish_id)
            if db_dish is None:
                raise HTTPException(status_code=404, detail="dish not found")
            await self.cache.set(f"dish_{dish_id}", db_dish)
        return db_dish

    async def create_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish: DishCreate,
        background_tasks: BackgroundTasks,
    ):
        db_dish = await self.crud.get_by_title(title=dish.title)
        if db_dish:
            raise HTTPException(
                status_code=400,
                detail="dish with this title already exist",
            )
        background_tasks.add_task(self.cache.delete, f"menu_{menu_id}")
        background_tasks.add_task(self.cache.delete, f"submenu_{submenu_id}")
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "submenu_list")
        background_tasks.add_task(self.cache.delete, "dish_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return await self.crud.create(
            dish=dish,
            submenu_id=submenu_id,
        )

    async def update_dish(
        self,
        dish_id: str,
        dish: DishUpdate,
        background_tasks: BackgroundTasks,
    ):
        db_dish = await self.crud.get(dish_id=dish_id)
        if db_dish is None:
            raise HTTPException(status_code=404, detail="dish not found")
        updated_dish = await self.crud.update(
            dish=dish,
            dish_id=dish_id,
        )
        await self.cache.set(f"dish_{dish_id}", updated_dish)
        background_tasks.add_task(self.cache.delete, "dish_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return updated_dish

    async def delete_dish(
        self,
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        background_tasks: BackgroundTasks,
    ):
        db_dish = await self.crud.get(dish_id=dish_id)
        if db_dish is None:
            raise HTTPException(status_code=404, detail="dish not found")
        await self.crud.delete(dish_id=dish_id)
        background_tasks.add_task(self.cache.delete, f"menu_{menu_id}")
        background_tasks.add_task(self.cache.delete, f"submenu_{submenu_id}")
        background_tasks.add_task(self.cache.delete, f"dish_{dish_id}")
        background_tasks.add_task(self.cache.delete, "menu_list")
        background_tasks.add_task(self.cache.delete, "submenu_list")
        background_tasks.add_task(self.cache.delete, "dish_list")
        background_tasks.add_task(self.cache.delete, "full_menu_ids")
        return {"status": "true", "message": "The menu has been deleted"}
