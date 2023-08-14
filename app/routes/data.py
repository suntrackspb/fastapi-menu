from typing import Annotated

from fastapi import APIRouter, Depends

from app.depend import get_data_service
from app.schemas.data import MenuSchema
from app.services.data_service import DataService

router = APIRouter()


@router.get(
    "/full_menu_with_id",
    summary="Список всех меню, подменю, блюд c UUID",
    response_description="Список всех меню, подменю, блюд c UUID",
    response_model=list[MenuSchema],
)
async def full_menu_with_id(
        datas_service: Annotated[DataService, Depends(get_data_service)],
):
    """Список всех меню, подменю, блюд c UUID"""
    return await datas_service.get_full_with_id()


@router.get(
    "/full_menu_without_id",
    summary="Список всех меню, подменю, блюд БЕЗ UUID",
    response_description="Список всех меню, подменю, блюд БЕЗ UUID",
    response_model=list[MenuSchema],
)
async def full_menu_without_id(
        datas_service: Annotated[DataService, Depends(get_data_service)],
):
    """Список всех меню, подменю, блюд БЕЗ UUID"""
    return await datas_service.get_full_without_id()
