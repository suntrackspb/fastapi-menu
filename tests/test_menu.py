import pytest
import requests
from requests import Response


@pytest.fixture(scope='function')
def create_test_menu(api_url):
    route = f"{api_url}/api/v1/menus"
    body = {
        "title": "My menu 1",
        "description": "My menu description 1"
    }
    response: Response = requests.post(url=route, json=body)
    yield response.json()
    url = route + '/' + response.json()['id']
    requests.delete(url)

