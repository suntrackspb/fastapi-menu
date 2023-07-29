from fastapi import FastAPI
from app.routes.menu import router as menu_router
from app.routes.submenu import router as submenu_router
from app.routes.dish import router as dish_router
from app.db.database import db_init

app = FastAPI(
    title="Online Menu API"
)


@app.on_event("startup")
async def on_startup():
    await db_init()


app.include_router(
    menu_router,
    prefix='/api/v1',
    tags=['menus'],
)
app.include_router(
    submenu_router,
    prefix='/api/v1/menus/{menu_id}',
    tags=['submenus'],
)
app.include_router(
    dish_router,
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}',
    tags=['dishes'],
)


