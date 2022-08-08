from httpx import AsyncClient
import pytest


pytestmark = pytest.mark.anyio


async def test_sanity(app):
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.get("/cards/")
    assert resp.status_code == 200


async def test_app_name(app):
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.get("/settings/")
    assert resp.status_code == 200
    assert resp.json()["app_name"] == "TestCards"


async def test_create_card(app):
    data = {"front": "Testy", "back": "Test"}
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.post("/cards/", json=data)
    assert resp.status_code == 201, resp.json()
    assert resp.json()["front"] == "Testy", resp.json()
    assert "id" in resp.json(), resp.json()
    assert "groups" in resp.json(), resp.json()


@pytest.mark.num_cards(3)
async def test_get_cards(app, non_empty_db):
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.get("/cards/")
    assert resp.status_code == 200, resp.json()
    assert len(resp.json()) == 3, resp.json()


@pytest.mark.num_cards(3)
async def test_filter_cards(app, non_empty_db):
    data = {"front": "1"}
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.request("GET", "/cards/", params=data)
    assert resp.status_code == 200
    assert len(resp.json()) == 1, resp.json()
