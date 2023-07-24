from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud.menu import MenuCrud
from app.crud.submenu import SubmenuCrud
from app.crud.dish import DishCrud
from app.services.menu_service import MenuService
from app.services.submenu_service import SubmenuService
from app.services.dish_service import DishService


###
# MENU
###
def get_menu_crud(db: Session = Depends(get_db)):
    return MenuCrud(db)


def get_menu_service(crud: MenuCrud = Depends(get_menu_crud)):
    return MenuService(crud)


###
# SUBMENU
###
def get_submenu_crud(db: Session = Depends(get_db)):
    return SubmenuCrud(db)


def get_submenu_service(crud: SubmenuCrud = Depends(get_submenu_crud)):
    return SubmenuService(crud)


###
# DISHES
###
async def get_dish_crud(db: Session = Depends(get_db)):
    return DishCrud(db)


async def get_dish_service(crud: DishCrud = Depends(get_dish_crud)):
    return DishService(crud)
