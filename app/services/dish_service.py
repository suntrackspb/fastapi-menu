from fastapi import HTTPException

from app.crud.dish import DishCrud
from app.schemas.dish import DishCreate, DishUpdate


class DishService:
    def __init__(self, crud: DishCrud):
        self.crud = crud

    async def get_dishes(self):
        db_dishes = await self.crud.get_list()
        return db_dishes

    async def get_dish(self, dish_id: str):
        db_dish = await self.crud.get(dish_id)
        if db_dish is None:
            raise HTTPException(status_code=404, detail='dish not found')
        return db_dish

    async def create_dish(
            self,
            menu_id: str,
            submenu_id: str,
            dish: DishCreate,
    ):
        db_dish = await self.crud.get_by_title(title=dish.title)
        if db_dish:
            raise HTTPException(
                status_code=400,
                detail='dish with this title already exist',
            )
        return await self.crud.create(
            dish=dish,
            submenu_id=submenu_id,
        )

    async def update_dish(
            self, dish_id: str,
            submenu_id: str,
            dish: DishUpdate,
    ):
        db_dish = await self.crud.get(dish_id=dish_id)
        if db_dish is None:
            raise HTTPException(status_code=404, detail='dish not found')
        updated_dish = await self.crud.update(
            dish=dish,
            dish_id=dish_id,
            submenu_id=submenu_id,
        )
        return updated_dish

    async def delete_dish(
            self, menu_id: str, submenu_id: str, dish_id: str
    ):
        db_dish = await self.crud.get(dish_id=dish_id)
        if db_dish is None:
            raise HTTPException(status_code=404, detail='dish not found')
        await self.crud.delete(dish_id=dish_id)
        return {'status': 'true', 'message': 'The menu has been deleted'}
