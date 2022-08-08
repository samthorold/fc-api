from typing import Protocol


from app.models import CardCreate, CardInDB, GroupInDB


class CardsRepository(Protocol):
    def get_card(self, id: int) -> CardInDB:
        ...

    def list_cards(
        self,
        front: str | None = None,
        back: str | None = None,
        group: str | None = None,
    ) -> list[CardInDB]:
        ...

    def get_group(self, id: int) -> GroupInDB:
        ...

    def list_groups(self, name: str | None = None) -> list[GroupInDB]:
        ...

    def add_card_to_group(card: CardInDB, group: GroupInDB) -> CardInDB:
        ...


class CardsListRepository:
    def __init__(self, lst: list[CardInDB]):
        self.db = lst

    def add_card(self, card: CardCreate) -> CardInDB:
        max_id = max(int(c.id) for c in self.list_cards())
        card_in_db = CardInDB(**{**{"id": max_id + 1}, **card.dict()})
        self.db.CARDSDB.append(card_in_db)
        return card_in_db

    def get_card(self, id: int) -> CardInDB:
        return next(c for c in self.db if c.id == id)

    def list_cards(
        self,
        front: str | None = None,
        back: str | None = None,
        groups: list[str] | None = None,
    ) -> list[CardInDB]:
        groups = [] if groups is None else groups
        cards = [card.copy() for card in self.db.CARDSDB]
        if front is not None:
            cards = [
                card for card in cards if front.lower() in card.front.lower()
            ]
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
