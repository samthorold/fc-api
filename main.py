from fastapi import FastAPI, Query


CARDSDB = [
    {"front": "Front", "back": "Back", "groups": ["g1", "g2"]},
    {"front": "Question", "back": "Answer", "groups": ["g2"]},
    {"front": "Query", "back": "Knowledge", "groups": None},
]


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hi hi"}


@app.get("/cards/")
async def cards(
    front: str = None,
    back: str = None,
    groups: list[str] = Query(default=None)
):
    cards = [{k: v for k, v in card.items()} for card in CARDSDB]
    if front is not None:
        cards = [card for card in cards if front.lower() in card["front"].lower()]
    if back is not None:
        cards = [card for card in cards if back.lower() in card["back"].lower()]
    if groups is not None:
        for group in groups:
            cards = [card for card in cards if group.lower() in [g.lower() for g in (card["groups"] or [])]]
    return cards


@app.get("/cards/{card_id}")
async def read_card(card_id: int):
    return {"card_id": card_id}

