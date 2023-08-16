from httpx import AsyncClient

from app.tests.schemas import Dish, Menu, Submenu


async def test_get_empty_menu_with_id(ac: AsyncClient):
    response_get_all_menus = await ac.get("/api/v1/full_menu_with_id")
    assert response_get_all_menus.status_code == 200
    assert response_get_all_menus.json() == []


async def test_post_menu(ac: AsyncClient):
    response_post = await ac.post("/api/v1/menus", json={
        "title": "My menu 1",
        "description": "My menu description 1",
    })

    assert response_post.status_code == 201
    Menu.id = response_post.json()["id"]


async def test_post_submenu(ac: AsyncClient):
    response_post_submenu = await ac.post(
        f"/api/v1/menus/{Menu.id}/submenus",
        json={
            "title": "My submenu 1",
            "description": "My submenu description 1",
        },
    )
    assert response_post_submenu.status_code == 201
    Submenu.id = response_post_submenu.json()["id"]


async def test_get_all_dishes_is_empty(ac: AsyncClient):
    response_get_all_dishes = await ac.get(
        f"/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes",
    )
    assert response_get_all_dishes.status_code == 200
    assert response_get_all_dishes.json() == []


async def test_post_dishes(ac: AsyncClient):
    response_post_dishes = await ac.post(
        f"/api/v1/menus/{Menu.id}/submenus/{Submenu.id}/dishes",
        json={
            "title": "My dish 1",
            "description": "My dish description 1",
            "price": "12.50",
        },
    )

    response_data = response_post_dishes.json()
    assert response_post_dishes.status_code == 201
    assert response_data["id"]
    assert response_data["title"]
    assert response_data["description"]
    assert response_data["price"]

    Dish.id, Dish.title, Dish.description, Dish.price = response_data[
        "id"], response_data["title"], response_data["description"], response_data["price"]


async def test_get_full_menu_with_id(ac: AsyncClient):
    response_get_all_menus = await ac.get("/api/v1/full_menu_with_id")
    assert response_get_all_menus.status_code == 200
    assert response_get_all_menus.json() != []


async def test_delete_menu(ac: AsyncClient):
    response_delete_menu = await ac.delete(
        f"/api/v1/menus/{Menu.id}",
    )
    assert response_delete_menu.status_code == 200
