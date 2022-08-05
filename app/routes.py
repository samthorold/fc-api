from fastapi import APIRouter, Query

from app.db import CARDSDB, GROUPSDB, Card, CardCreate, Group


router = APIRouter()


@router.get("/cards/")
async def cards(
    front: str | None = None,
    back: str | None = None,
    groups: list[str] | None = Query(default=None),
):
    cards = [card.copy() for card in CARDSDB]
    if front is not None:
        cards = [card for card in cards if front.lower() in card.front.lower()]
    if back is not None:
        cards = [card for card in cards if back.lower() in card.back.lower()]
    if groups is not None:
        for group in groups:
            cards = [
                card
                for card in cards
                if group.lower() in [g.name.lower() for g in (card.groups or [])]
            ]
    return cards


@router.post("/cards/")
async def create_card(card: CardCreate):
    CARDSDB.append(Card(**card.dict()))
    return CARDSDB[-1]


@router.get("/cards/{card_id}")
async def read_card(card_id: int):
    return {"card_id": card_id}


@router.get("/groups/")
async def groups():
    return GROUPSDB


@router.post("/groups/")
def create_group(group: Group):
    GROUPSDB.append(group)
    return group
