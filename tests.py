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


@pytest.mark.num_cards(3)
async def test_get_cards(app, non_empty_db):
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.get("/cards/")
    assert resp.status_code == 200
    assert len(resp.json()) == 3, resp.json()
