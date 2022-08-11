from faker import Faker
import pytest


from app import db, models
from app.app import get_app

fake = Faker()


@pytest.fixture
def app():
    return get_app(".test.env")


@pytest.fixture
def new_db():
    db.CARDSDB = []
    db.GROUPSDB = []
    return db


def n_fake_cards(n: int = 10):
    return [
        models.CardInDB(id=(i + 1), front=f"{i+1}", back=fake.sentence())
        for i in range(n)
    ]


def n_fake_groups(n: int = 10):
    return [models.GroupInDB(id=(i + 1), name=str(i)) for i in range(n)]


@pytest.fixture
def non_empty_db(new_db, request):
    m = request.node.get_closest_marker("num_cards")
    if m and len(m.args) > 0:
        for card in n_fake_cards(m.args[0]):
            new_db.CARDSDB.append(card)
    m = request.node.get_closest_marker("num_groups")
    if m and len(m.args) > 0:
        for group in n_fake_groups(m.args[0]):
            new_db.GROUPSDB.append(group)
    return new_db
