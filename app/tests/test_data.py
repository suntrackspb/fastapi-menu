from httpx import AsyncClient

from app.tests.schemas import Menu


async def test_get_exact_full_with_id_after_post(ac: AsyncClient):
    response_get_by_id = await ac.get("/api/v1/load_from_excel")
    response_data = response_get_by_id.json()

    assert response_get_by_id.status_code == 200
    assert response_data["id"] == Menu.id
    assert response_data["title"] == Menu.title
    assert response_data["description"] == Menu.description


async def test_get_exact_full_without_id_after_post(ac: AsyncClient):
    response_get_by_id = await ac.get("/api/v1/load_from_excel")
    response_data = response_get_by_id.json()

    assert response_get_by_id.status_code == 200
    assert response_data["id"] == Menu.id
    assert response_data["title"] == Menu.title
    assert response_data["description"] == Menu.description
