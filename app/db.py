from app import models


GROUPSDB = [
    models.GroupInDB(id=1, name="g1"),
    models.GroupInDB(id=2, name="g2"),
]


CARDSDB = [
    models.CardInDB(id=1, front="Front", back="Back", groups=[GROUPSDB[0], GROUPSDB[-1]]),
    models.CardInDB(id=2, front="Question", back="Answer", groups=[GROUPSDB[-1]]),
    models.CardInDB(id=3, front="Query", back="Knowledge"),
]
