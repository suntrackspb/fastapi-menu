from typing import Annotated

from fastapi import APIRouter, Depends

from app.depend import get_data_service
from app.schemas.data import MessageStatus
from app.services.data_service import DataService

router = APIRouter()


@router.get(
    "/load_from_excel",
    summary="Загрузить все данные из Menu.xlsx в пустую БД",
    response_description="Загрузить все данные из Menu.xlsx в пустую БД",
    responses={200: {"model": MessageStatus}},
)
async def load_menus_from_xls(
        datas_service: Annotated[DataService, Depends(get_data_service)],
):
    """Загружает все данные из Menu.xlsx в базу данных, использовать при пустой таблице"""
    return await datas_service.load_to_database()


@router.get(
    "/unload_from_database",
    summary="Выгрузить всё из базы данных в Database.xlsx",
    response_description="Выгрузить всё из базы данных в Database.xlsx",
    responses={200: {"model": MessageStatus}},
)
async def unload_from_database(
        datas_service: Annotated[DataService, Depends(get_data_service)],
):
    """Выгружает данные из базы данных в excel таблицу и сохраняет в файл Database.xlsx"""
    return await datas_service.unload_to_excel()
