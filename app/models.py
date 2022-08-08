from pydantic import BaseModel, Field


class FlashCardsError(Exception):
    """FlashCards root error."""


class NoSuchCard(FlashCardsError):
    """Card does not exist."""


class NoSuchGroup(FlashCardsError):
    """Group does not exist."""


class Group(BaseModel):
    name: str = Field(..., min_length=1)


class GroupInDB(Group):
    id: int


class CardCreate(BaseModel):
    front: str = Field(..., min_length=1)
    back: str = Field(..., min_length=1)

    class Config:
        schema_extra = {"example": {"front": "Question", "back": "Answer"}}


class Card(CardCreate):
    groups: list[Group] | None = None


class CardInDB(Card):
    id: int
