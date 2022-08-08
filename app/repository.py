from typing import Protocol


from app import models


class CardsRepository(Protocol):

    def add_card(self, card: models.CardCreate) -> models.CardInDB:
        ...

    def get_card(self, id: int) -> models.CardInDB:
        ...

    def list_cards(
        self,
        front: str | None = None,
        back: str | None = None,
        group: str | None = None,
    ) -> list[models.CardInDB]:
        ...

    def add_group(self, group: models.Group) -> models.GroupInDB:
        ...

    def get_group(self, id: int) -> models.GroupInDB:
        ...

    def list_groups(self, name: str | None = None) -> list[models.GroupInDB]:
        ...

    def add_card_to_group(card: models.CardInDB, group: models.GroupInDB) -> models.CardInDB:
        ...


class CardsListRepository:
    def __init__(self, lst: list[models.CardInDB]):
        self.db = lst

    def add_card(self, card: models.CardCreate) -> models.CardInDB:
        max_id = max(int(c.id) for c in self.list_cards())
        card_in_db = models.CardInDB(**{**{"id": max_id + 1}, **card.dict()})
        self.db.CARDSDB.append(card_in_db)
        return card_in_db

    def get_card(self, id: int) -> models.CardInDB:
        try:
            return next(c for c in self.db.CARDSDB if c.id == id)
        except StopIteration:
            raise models.NoSuchCard

    def list_cards(
        self,
        front: str | None = None,
        back: str | None = None,
        groups: list[str] | None = None,
    ) -> list[models.CardInDB]:
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

    def add_group(self, group: models.Group) -> models.GroupInDB:
        max_id = max(int(g.id) for g in self.list_groups())
        group_in_db = models.GroupInDB(**{**{"id": max_id + 1}, **group.dict()})
        self.db.GROUPSDB.append(group_in_db)
        return group_in_db

    def get_group(self, id: int) -> models.GroupInDB:
        return next(g for g in self.list_groups() if g.id == id)

    def list_groups(
        self,
        name: str | None = None,
    ) -> list[models.GroupInDB]:
        groups = [group.copy() for group in self.db.GROUPSDB]
        if name is not None:
            groups = [
                group for group in groups if name.lower() in group.name.lower()
            ]
        return groups

    def add_card_to_group(self, card: models.CardInDB, group: models.GroupInDB) -> models.CardInDB:
        if card.groups is None:
            card.groups = []
        card.groups.append(group)
        return card
