from fastapi import APIRouter, Body, Depends

from app.depend import get_submenu_service
from app.schemas.errors import Message404, MessageDeleted
from app.schemas.submenu import SubmenuCreate, SubmenuGet, SubmenuUpdate
from app.services.submenu_service import SubmenuService

router = APIRouter()


@router.get(
    '/submenus',
    response_model=list[SubmenuGet],
    summary='Получить список подменю',
    response_description='Список всех подменю',
)
async def read_submenus(
    menu_id: str,
    submenu_service: SubmenuService = Depends(
        get_submenu_service,
    ),
):
    """Получить список всех подменю"""
    return await submenu_service.get_submenus(menu_id)


@router.get(
    '/submenus/{submenu_id}',
    responses={404: {'model': Message404}},
    response_model=SubmenuGet,
    summary='Получить детальную информацию о подменю',
    response_description='Детальная информация о подменю',
)
async def read_submenu(
    submenu_id: str,
    submenu_service: SubmenuService = Depends(
        get_submenu_service,
    ),
):
    """Получить детальную информацию о подменю"""
    return await submenu_service.get_submenu(
        submenu_id=submenu_id,
    )


@router.post(
    '/submenus',
    response_model=SubmenuGet,
    summary='Создать подменю',
    response_description='Созданное подменю',
    status_code=201,
)
async def create_submenu(
    menu_id: str,
    submenu: SubmenuCreate = Body(
        example={
            'title': 'Submenu 1',
            'description': 'Submenu 1 description',
        },
    ),
    submenu_service: SubmenuService = Depends(
        get_submenu_service,
    ),
):
    """Создать подменю"""
    return await submenu_service.create_submenu(
        menu_id=menu_id,
        submenu=submenu,
    )


@router.patch(
    '/submenus/{submenu_id}',
    responses={404: {'model': Message404}},
    response_model=SubmenuGet,
    summary='Обновить подменю',
    response_description='Обновленное подменю',
)
async def update_submenu(
    submenu_id: str,
    submenu: SubmenuUpdate = Body(
        example={
            'title': 'Submenu 1 updated',
            'description': 'Submenu 1 description updated',
        },
    ),
    submenu_service: SubmenuService = Depends(
        get_submenu_service,
    ),
):
    """Обновить подменю"""
    return await submenu_service.update_submenu(
        submenu_id=submenu_id,
        submenu=submenu,
    )


@router.delete(
    '/submenus/{submenu_id}',
    responses={404: {'model': Message404}, 200: {'model': MessageDeleted}},
    summary='Удалить подменю',
)
async def delete_submenu(
    menu_id: str,
    submenu_id: str,
    submenu_service: SubmenuService = Depends(
        get_submenu_service,
    ),
):
    """Удалить подменю"""
    return await submenu_service.delete_submenu(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
