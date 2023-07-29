import pytest


@pytest.fixture(scope='session')
def api_url():
    yield 'https://localhost:8000'
