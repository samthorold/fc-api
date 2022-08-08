from fastapi import APIRouter, Query

from app import db
from app.models import CardCreate, CardInDB, Group
from app.repository import CardsListRepository, CardsRepository


router = APIRouter()


@router.get("/cards/")
async def cards(
    front: str | None = None,
    back: str | None = None,
    groups: list[str] | None = Query(default=None),
):
    repo: CardsRepository = CardsListRepository(db)
    return repo.list_cards(front=front, back=back, groups=groups)


@router.post("/cards/", status_code=201)
async def create_card(card: CardCreate) -> CardInDB:
    repo: CardsRepository = CardsListRepository(db)
    return repo.add_card(card)


@router.get("/cards/{card_id}")
async def read_card(card_id: int):
    return {"card_id": card_id}


@router.get("/groups/")
async def groups():
    return db.GROUPSDB


@router.post("/groups/", status_code=201)
def create_group(group: Group):
    db.GROUPSDB.append(group)
    return group
