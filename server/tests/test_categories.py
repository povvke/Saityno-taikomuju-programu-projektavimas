import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

from ..models import get_session
from ..routes import categories as categories_router


@pytest.fixture(name="engine")
def engine_fixture(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="app")
def app_fixture(session):
    app = FastAPI()

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    app.include_router(categories_router.router, prefix="/categories")
    return app


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_category_success(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/categories/",
            json={
                "name": "Desserts",
                "description": "Sweet stuff",
                "parent_category": None,
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["slug"] == "desserts"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_category_conflict(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # create once
        await ac.post(
            "/categories/",
            json={"name": "Drinks", "description": None, "parent_category": None},
        )
        # duplicate slug
        resp = await ac.post(
            "/categories/",
            json={"name": "Drinks", "description": None, "parent_category": None},
        )
    assert resp.status_code == 409
    assert "already exists" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_category_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/categories/",
            json={"name": "Snacks", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]
        resp = await ac.get(f"/categories/{cid}")
    assert resp.status_code == 200
    assert resp.json()["slug"] == "snacks"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_category_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/categories/999")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Category not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_categories_list(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/categories/",
            json={"name": "Breakfast", "description": None, "parent_category": None},
        )
        await ac.post(
            "/categories/",
            json={"name": "Lunch", "description": None, "parent_category": None},
        )
        resp = await ac.get("/categories/")
    assert resp.status_code == 200
    names = {c["name"] for c in resp.json()}
    assert {"Breakfast", "Lunch"}.issubset(names)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_category_success(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/categories/",
            json={"name": "Dinner", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]
        resp = await ac.patch(f"/categories/{cid}", json={"name": "Evening"})
    assert resp.status_code == 200
    assert resp.json()["slug"] == "evening"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_delete_category_success(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/categories/",
            json={"name": "Temp", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]
        resp = await ac.delete(f"/categories/{cid}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipes_empty(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/categories/1/recipes")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_category_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.patch("/categories/999", json={"name": "Test"})
    assert resp.status_code == 404
    assert resp.json()["message"] == "Category not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_update_category_conflict(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create first category
        await ac.post(
            "/categories/",
            json={"name": "Category A", "description": None, "parent_category": None},
        )
        # Create second category
        post = await ac.post(
            "/categories/",
            json={"name": "Category B", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]
        # Try to update to duplicate name
        resp = await ac.patch(f"/categories/{cid}", json={"name": "Category A"})
    assert resp.status_code == 409
    assert "already exists" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_delete_category_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.delete("/categories/999")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Category not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_categories_pagination(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create multiple categories
        for i in range(5):
            await ac.post(
                "/categories/",
                json={
                    "name": f"Category {i}",
                    "description": None,
                    "parent_category": None,
                },
            )
        resp = await ac.get("/categories/?offset=2&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipes_empty(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/categories/",
            json={"name": "Empty Cat", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]
        resp = await ac.get(f"/categories/{cid}/recipes")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipes_with_data(app, session):
    from ..models import Recipe

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create category
        post = await ac.post(
            "/categories/",
            json={"name": "Test Cat", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]

        # Create recipes directly in DB
        recipe1 = Recipe(
            name="Recipe 1",
            slug="recipe-1",
            description="Test",
            instructions="Test",
            ingredients="Test",
            calories=100,
            prep_time=10,
            servings=2,
            category_id=cid,
        )
        recipe2 = Recipe(
            name="Recipe 2",
            slug="recipe-2",
            description="Test",
            instructions="Test",
            ingredients="Test",
            calories=200,
            prep_time=20,
            servings=4,
            category_id=cid,
        )
        session.add(recipe1)
        session.add(recipe2)
        session.commit()

        resp = await ac.get(f"/categories/{cid}/recipes")
    assert resp.status_code == 200
    names = {r["name"] for r in resp.json()}
    assert {"Recipe 1", "Recipe 2"}.issubset(names)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipes_pagination(app, session):
    from ..models import Recipe

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create category
        post = await ac.post(
            "/categories/",
            json={"name": "Test Cat", "description": None, "parent_category": None},
        )
        cid = post.json()["id"]

        # Create multiple recipes
        for i in range(5):
            recipe = Recipe(
                name=f"Recipe {i}",
                slug=f"recipe-{i}",
                description="Test",
                instructions="Test",
                ingredients="Test",
                calories=100,
                prep_time=10,
                servings=2,
                category_id=cid,
            )
            session.add(recipe)
        session.commit()

        resp = await ac.get(f"/categories/{cid}/recipes?offset=2&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 2
