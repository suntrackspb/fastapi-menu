from typing import Annotated

from fastapi import APIRouter, Body, Depends

from app.depend import get_dish_service
from app.schemas.dish import DishCreate, DishGet, DishUpdate
from app.schemas.errors import Message404, MessageDeleted
from app.services.dish_service import DishService

router = APIRouter()


@router.get(
    '/dishes',
    response_model=list[DishGet],
    summary='Получить список блюд',
    response_description='Список всех блюд',
)
async def read_dishes(
        dish_service: Annotated[DishService, Depends(get_dish_service)],
):
    """Получить список всех блюд"""
    return await dish_service.get_dishes()


@router.get(
    '/dishes/{dish_id}',
    response_model=DishGet,
    responses={404: {'model': Message404}},
    summary='Получить детальную информацию o блюде',
    response_description='Список всех блюд',
)
async def read_dish(
        dish_id: str,
        dish_service: Annotated[DishService, Depends(get_dish_service)],
):
    """Получить детальную информацию o блюде"""
    return await dish_service.get_dish(
        dish_id=dish_id,
    )


@router.post(
    '/dishes',
    response_model=DishGet,
    summary='Создать блюдо',
    response_description='Созданное блюдо',
    status_code=201,
)
async def create_dish(
        menu_id: str,
        submenu_id: str,
        dish: Annotated[
            DishCreate, Body(
                example={
                    'title': 'Dish 1',
                    'description': 'Dish 1 description',
                },
            ),
        ],
        dish_service: Annotated[DishService, Depends(get_dish_service)],
):
    """Создать блюдо"""
    return await dish_service.create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish=dish,
    )


@router.patch(
    '/dishes/{dish_id}',
    responses={404: {'model': Message404}},
    summary='Изменить блюдо',
    response_description='Измененное блюдо',
    response_model=DishGet,
)
async def update_dish(
        dish_id: str,
        dish: DishUpdate = Body(
            example={
                'title': 'Dish 1 updated',
                'description': 'Dish 1 description updated',
            },
        ),
        dish_service: DishService = Depends(get_dish_service),
):
    """Изменить блюдо"""
    return await dish_service.update_dish(
        dish_id=dish_id,
        dish=dish,
    )


@router.delete(
    '/dishes/{dish_id}',
    responses={404: {'model': Message404}, 200: {'model': MessageDeleted}},
    summary='Удалить блюдо',
)
async def delete_dish(
        menu_id: str,
        submenu_id: str,
        dish_id: str,
        dish_service: DishService = Depends(get_dish_service),
):
    """Удалить блюдо"""
    return await dish_service.delete_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
