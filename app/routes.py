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
    repo: CardsRepository = CardsListRepository(db)
    return repo.get_card(id)


@router.get("/groups/")
async def groups(name: str | None = None):
    repo: CardsRepository = CardsListRepository(db)
    return repo.list_groups(name)


@router.post("/groups/", status_code=201)
def create_group(group: Group):
    repo: CardsRepository = CardsListRepository(db)
    return repo.add_group(group)


@router.post("/add-card-to-group/", status_code=201)
async def add_card_to_group(card_id: int, group_id: int) -> CardInDB:
    repo: CardsRepository = CardsListRepository(db)
    card = repo.get_card(card_id)
    group = repo.get_group(group_id)
    return repo.add_card_to_group(card, group)
