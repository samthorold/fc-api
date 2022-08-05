from fastapi import FastAPI, Query
from pydantic import BaseModel, constr


class Group(BaseModel):
    name: constr(min_length=1)


class Card(BaseModel):
    front: constr(min_length=1)
    back: constr(min_length=1)
    groups: list[Group] | None = None

    class Config:
        schema_extra = {"example": {"front": "Question", "back": "Answer"}}


GROUPSDB = [
    Group(name="g1"),
    Group(name="g2"),
]

CARDSDB = [
    Card(front="Front", back="Back", groups=[GROUPSDB[0], GROUPSDB[-1]]),
    Card(front="Question", back="Answer", groups=[GROUPSDB[-1]]),
    Card(front="Query", back="Knowledge"),
]


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hi hi"}


@app.get("/cards/")
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


@app.post("/cards/")
async def create_card(card: Card):
    CARDSDB.append(card)
    return card


@app.get("/cards/{card_id}")
async def read_card(card_id: int):
    return {"card_id": card_id}


@app.get("/groups/")
async def groups():
    return GROUPSDB


@app.post("/groups/")
def create_group(group: Group):
    GROUPSDB.append(group)
    return group
