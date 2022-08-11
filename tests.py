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


async def test_create_group(app):
    data = {"name": "Group"}
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.post("/groups/", json=data)
    assert resp.status_code == 201, resp.json()
    assert resp.json()["name"] == "Group", resp.json()
    assert "id" in resp.json(), resp.json()


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


@pytest.mark.num_groups(3)
async def test_get_groups(app, non_empty_db):
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.get("/groups/")
    assert resp.status_code == 200, resp.json()
    assert len(resp.json()) == 3, resp.json()


@pytest.mark.num_groups(3)
async def test_filter_groups(app, non_empty_db):
    data = {"name": "0"}
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.get("/groups/", params=data)
    assert resp.status_code == 200, resp.json()
    assert len(resp.json()) == 1, resp.json()


@pytest.mark.num_cards(1)
@pytest.mark.num_groups(1)
async def test_add_card_to_group(app, non_empty_db):
    data = {"card_id": 1, "group_id": 1}
    async with AsyncClient(app=app, base_url="http://test") as cl:
        resp = await cl.post("/add-card-to-group/", params=data)
    assert resp.status_code == 201, resp.json()
    assert "groups" in resp.json(), resp.json()
    assert resp.json()["groups"] is not None
