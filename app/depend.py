from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.dish import DishCrud
from app.crud.menu import MenuCrud
from app.crud.submenu import SubmenuCrud
from app.db.database import get_db
from app.db.redis import get_cache as get_redis
from app.services.cache_service import CacheService
from app.services.dish_service import DishService
from app.services.menu_service import MenuService
from app.services.submenu_service import SubmenuService


def get_cache(cache: Annotated[Any, Depends(get_redis)]):
    return CacheService(cache)


###
# MENU
###
def get_menu_crud(db: Annotated[Session, Depends(get_db)]):
    return MenuCrud(db)


def get_menu_service(
        crud:  Annotated[MenuCrud, Depends(get_menu_crud)],
        cache:  Annotated[CacheService, Depends(get_cache)],
):
    return MenuService(crud, cache)


###
# SUBMENU
###
def get_submenu_crud(db:  Annotated[Session, Depends(get_db)]):
    return SubmenuCrud(db)


def get_submenu_service(
    crud:  Annotated[SubmenuCrud, Depends(get_submenu_crud)],
    cache:  Annotated[CacheService, Depends(get_cache)],
):
    return SubmenuService(crud, cache)


###
# DISHES
###
async def get_dish_crud(db:  Annotated[Session, Depends(get_db)]):
    return DishCrud(db)


async def get_dish_service(
    crud:  Annotated[DishCrud, Depends(get_dish_crud)],
    cache:  Annotated[CacheService, Depends(get_cache)],
):
    return DishService(crud, cache=cache)
