import pytest

from app.app import get_app


@pytest.fixture
def app():
    return get_app(".test.env")
