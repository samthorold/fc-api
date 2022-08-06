from pydantic import BaseModel, Field


class Group(BaseModel):
    name: str = Field(..., min_length=1)

    class Config:
        frozen = True


class CardCreate(BaseModel):
    front: str = Field(..., min_length=1)
    back: str = Field(..., min_length=1)

    class Config:
        schema_extra = {"example": {"front": "Question", "back": "Answer"}}


class Card(CardCreate):
    groups: list[Group] | None = None
