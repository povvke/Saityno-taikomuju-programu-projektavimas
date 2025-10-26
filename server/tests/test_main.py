import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from sqlmodel import SQLModel, Session, create_engine

from ..main import app, lifespan
from ..models import get_session


@pytest.fixture(name="engine")
def engine_fixture(tmp_path):
    """Create an isolated SQLite DB per test run."""
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Yield a SQLModel session bound to our temporary engine."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_app")
def test_app_fixture(session):
    """Create test app with DB override."""

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    yield app
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_lifespan_creates_db():
    """Test that lifespan context manager creates database tables."""
    with patch("server.main.create_db_and_tables") as mock_create_db:
        async with lifespan(app):
            pass
        mock_create_db.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_app_has_categories_router(test_app):
    """Test that categories router is included."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/categories/")
    assert resp.status_code == 200


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_app_has_recipes_router(test_app):
    """Test that recipes router is included."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/recipes/")
    assert resp.status_code == 200


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_app_has_comments_router(test_app):
    """Test that comments router is included."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/comments/")
    assert resp.status_code == 200


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_categories_router_prefix(test_app):
    """Test that categories router uses correct prefix."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Try without prefix - should fail
        resp_wrong = await ac.get("/")
        # Try with prefix - should work
        resp_correct = await ac.get("/categories/")
    assert resp_wrong.status_code == 404
    assert resp_correct.status_code == 200


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_recipes_router_prefix(test_app):
    """Test that recipes router uses correct prefix."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/recipes/")
    assert resp.status_code == 200


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_comments_router_prefix(test_app):
    """Test that comments router uses correct prefix."""
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/comments/")
    assert resp.status_code == 200


def test_app_is_fastapi_instance():
    """Test that app is a FastAPI instance."""
    from fastapi import FastAPI

    assert isinstance(app, FastAPI)


def test_app_has_lifespan():
    """Test that app has lifespan configured."""
    assert app.router.lifespan_context is not None
