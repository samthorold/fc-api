from app import models


GROUPSDB = [
    models.Group(name="g1"),
    models.Group(name="g2"),
]


CARDSDB = [
    models.Card(front="Front", back="Back", groups=[GROUPSDB[0], GROUPSDB[-1]]),
    models.Card(front="Question", back="Answer", groups=[GROUPSDB[-1]]),
    models.Card(front="Query", back="Knowledge"),
]
