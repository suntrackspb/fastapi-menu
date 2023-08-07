from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.depend import get_menu_service
from app.schemas.errors import Message404, MessageDeleted
from app.schemas.menu import MenuCreate, MenuGet, MenuUpdate
from app.services.menu_service import MenuService

router = APIRouter()


@router.get(
    "/menus",
    response_model=list[MenuGet],
    summary="Получить список меню",
    response_description="Список всех меню",
)
async def read_menus(
        menu_service: Annotated[MenuService, Depends(get_menu_service)],
):
    """Получить список всех меню"""
    return await menu_service.get_menus()


@router.get(
    "/menus/{menu_id}", response_model=MenuGet,
    responses={404: {"model": Message404}},
    summary="Получить детальную информацию o меню",
    response_description="Детальная информация o меню",
)
async def read_menu(
        menu_id: str,
        menu_service: Annotated[MenuService, Depends(get_menu_service)],
):
    """Получить детальную информацию o меню"""
    return await menu_service.get_menu(menu_id=menu_id)


@router.post(
    "/menus", response_model=MenuGet,
    summary="Создать меню",
    response_description="Созданное меню",
    status_code=201,
)
async def create_menu(
        menu: Annotated[MenuCreate, Body(
            example={
                "title": "Menu 1",
                "description": "Menu 1 description",
            },
        )],
        menu_service: Annotated[MenuService, Depends(get_menu_service)],
):
    """Создать меню"""
    return await menu_service.create_menu(menu=menu)


@router.patch(
    "/menus/{menu_id}",
    response_model=MenuGet,
    responses={404: {"model": Message404}},
    summary="Изменить меню",
    response_description="Измененное меню",
)
async def update_menu(
        menu_id: str,
        menu: Annotated[MenuUpdate, Body(
            example={
                "title": "Menu 1 updated",
                "description": "Menu 1 description updated",
            },
        )],
        menu_service: Annotated[MenuService, Depends(get_menu_service)],
):
    """Изменить меню"""
    return await menu_service.update_menu(
        menu_id=menu_id,
        menu=menu,
    )


@router.delete(
    "/menus/{menu_id}",
    responses={404: {"model": Message404}, 200: {"model": MessageDeleted}},
    summary="Удалить меню",
)
async def delete_menu(
        menu_id: str,
        menu_service: Annotated[MenuService, Depends(get_menu_service)],
):
    """Удалить меню"""
    return await menu_service.delete_menu(
        menu_id=menu_id,
    )
