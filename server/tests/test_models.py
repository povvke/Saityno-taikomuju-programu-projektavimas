import pytest
from decimal import Decimal
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, select, SQLModel, create_engine
from sqlalchemy import inspect
from sqlalchemy.orm.session import close_all_sessions
from .. import models


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_category_model_fields():
    c = models.Category(
        name="Main", description="desc", parent_category=None, slug="main"
    )
    assert c.name == "Main"
    assert c.slug == "main"
    assert c.id is None


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_recipe_model_fields():
    r = models.Recipe(
        name="Cake",
        description="Yummy",
        instructions="Mix & bake",
        ingredients='["flour", "sugar"]',
        calories=200,
        prep_time=30,
        servings=4,
        category_id=None,
        author_id=None,
        slug="cake",
    )
    assert r.slug == "cake"
    assert isinstance(r.name, str)
    assert r.id is None


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_comment_model_fields():
    cm = models.Comment(
        title="Great!",
        text="Loved it",
        rating=Decimal("4.5"),
        user_id=1,
        recipe_id=None,
    )
    assert cm.title == "Great!"
    assert cm.user_id == 1
    assert isinstance(cm.rating, Decimal)


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_user_model_fields():
    u = models.User(id=1, username="bob", password="secret", role="admin")
    assert u.username == "bob"
    assert u.role == "admin"


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_create_db_and_tables_creates_tables(tmp_path):
    # Use temp SQLite DB
    db_path = tmp_path / "test.db"
    test_url = f"sqlite:///{db_path}"
    engine = create_engine(test_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected = {"category", "recipe", "comment", "user"}
    for table in expected:
        assert table in tables


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_get_session_yields_session(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)

    def local_get_session():
        with Session(engine) as s:
            yield s

    gen = local_get_session()
    session = next(gen)
    assert isinstance(session, Session)
    gen.close()


@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_insert_and_select_roundtrip(tmp_path):
    db_path = tmp_path / "test_roundtrip.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = models.User(id=1, username="alice", password="123", role="user")
        session.add(user)
        session.commit()

        result = session.exec(select(models.User)).first()
        engine.dispose()
        assert result.username == "alice"
