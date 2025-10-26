import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

from ..models import get_session, Category
from ..routes import recipes as recipes_router


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


@pytest.fixture(name="app")
def app_fixture(session):
    """Create a FastAPI app with a proper DB dependency override."""
    app = FastAPI()

    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    app.include_router(recipes_router.router, prefix="/recipes")
    return app


@pytest.fixture(name="category")
def category_fixture(session):
    """Create a test category."""
    category = Category(
        name="Test Category",
        slug="test-category",
        description="Test description",
        parent_category=None,
    )
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_recipe_success(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/recipes/",
            json={
                "name": "Chocolate Cake",
                "description": "Delicious chocolate cake",
                "instructions": "Mix and bake",
                "ingredients": "flour, sugar, cocoa",
                "calories": 350,
                "prep_time": 45,
                "servings": 8,
                "category_id": category.id,
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["slug"] == "chocolate-cake"
    assert data["name"] == "Chocolate Cake"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_recipe_category_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/recipes/",
            json={
                "name": "Test Recipe",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": 999,
            },
        )
    assert resp.status_code == 404
    assert resp.json()["message"] == "Category not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_recipe_conflict(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create first recipe
        await ac.post(
            "/recipes/",
            json={
                "name": "Vanilla Cake",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        # Try to create duplicate
        resp = await ac.post(
            "/recipes/",
            json={
                "name": "Vanilla Cake",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
    assert resp.status_code == 409
    assert "already exists" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipe_found(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Pancakes",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        resp = await ac.get(f"/recipes/{recipe_id}")
    assert resp.status_code == 200
    assert resp.json()["slug"] == "pancakes"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipe_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/recipes/999")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Recipe not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipes_list(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/recipes/",
            json={
                "name": "Recipe One",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        await ac.post(
            "/recipes/",
            json={
                "name": "Recipe Two",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        resp = await ac.get("/recipes/")
    assert resp.status_code == 200
    names = {r["name"] for r in resp.json()}
    assert {"Recipe One", "Recipe Two"}.issubset(names)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_recipes_pagination(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create multiple recipes
        for i in range(5):
            await ac.post(
                "/recipes/",
                json={
                    "name": f"Recipe {i}",
                    "description": "Test",
                    "instructions": "Test",
                    "ingredients": "Test",
                    "calories": 100,
                    "prep_time": 10,
                    "servings": 2,
                    "category_id": category.id,
                },
            )
        resp = await ac.get("/recipes/?offset=2&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_update_recipe_success(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Old Name",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        resp = await ac.patch(
            f"/recipes/{recipe_id}",
            json={"name": "New Name", "category_id": category.id},
        )
    assert resp.status_code == 200
    assert resp.json()["slug"] == "new-name"
    assert resp.json()["name"] == "New Name"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_recipe_not_found(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.patch(
            "/recipes/999", json={"name": "Test", "category_id": category.id}
        )
    assert resp.status_code == 404
    assert resp.json()["message"] == "Recipe not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_recipe_category_not_found(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Test Recipe",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        resp = await ac.patch(
            f"/recipes/{recipe_id}", json={"category_id": 999, "name": "Test"}
        )
    assert resp.status_code == 404
    assert resp.json()["message"] == "Category not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_update_recipe_conflict(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create first recipe
        await ac.post(
            "/recipes/",
            json={
                "name": "Recipe A",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        # Create second recipe
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Recipe B",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        # Try to update to duplicate name
        resp = await ac.patch(
            f"/recipes/{recipe_id}",
            json={"name": "Recipe A", "category_id": category.id},
        )
    assert resp.status_code == 409
    assert "already exists" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_delete_recipe_success(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Temp Recipe",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        resp = await ac.delete(f"/recipes/{recipe_id}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_delete_recipe_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.delete("/recipes/999")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Recipe not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_comments_empty(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Test Recipe",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        resp = await ac.get(f"/recipes/{recipe_id}/comments")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_comments_pagination(app, category):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/recipes/",
            json={
                "name": "Test Recipe",
                "description": "Test",
                "instructions": "Test",
                "ingredients": "Test",
                "calories": 100,
                "prep_time": 10,
                "servings": 2,
                "category_id": category.id,
            },
        )
        recipe_id = post.json()["id"]
        resp = await ac.get(f"/recipes/{recipe_id}/comments?offset=0&limit=50")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
