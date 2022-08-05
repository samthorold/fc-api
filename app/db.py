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


GROUPSDB = [
    Group(name="g1"),
    Group(name="g2"),
]


CARDSDB = [
    Card(front="Front", back="Back", groups=[GROUPSDB[0], GROUPSDB[-1]]),
    Card(front="Question", back="Answer", groups=[GROUPSDB[-1]]),
    Card(front="Query", back="Knowledge"),
]
