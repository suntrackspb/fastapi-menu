from fastapi import APIRouter

from app.google_sheets.google_sheet import auth

router = APIRouter()


@router.get(
    "/google_auth",
    summary="Запрос разрешений от Google Api",
    response_description="Запрос разрешений от Google Api",
)
async def read_menus():
    """Запросить разрешения googleAPi"""
    return auth()
