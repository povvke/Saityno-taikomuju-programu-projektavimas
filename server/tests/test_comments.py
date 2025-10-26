import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine

from ..models import get_session, Category, Recipe, User
from ..routes import comments as comments_router


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

    # Čia įvyksta "mockinimas"
    app.dependency_overrides[get_session] = get_session_override
    app.include_router(comments_router.router, prefix="/comments")
    return app


@pytest.fixture(name="user")
def user_fixture(session):
    """Create a test user."""
    user = User(
        username="testuser",
        password="testpass",
        role="user",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="recipe")
def recipe_fixture(session):
    category = Category(
        name="Test Category",
        slug="test-category",
        description="Test description",
        parent_category=None,
    )
    session.add(category)
    session.commit()
    session.refresh(category)

    recipe = Recipe(
        name="Test Recipe",
        slug="test-recipe",
        description="Test description",
        instructions="Test instructions",
        ingredients="Test ingredients",
        calories=100,
        prep_time=10,
        servings=2,
        category_id=category.id,
    )
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_comment_success(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/comments/",
            json={
                "title": "Great Recipe",
                "text": "This was delicious!",
                "rating": 4.5,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Great Recipe"
    assert data["text"] == "This was delicious!"
    assert float(data["rating"]) == 4.5


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_comment_recipe_not_found(app, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 4.0,
                "user_id": user.id,
                "recipe_id": 999,
            },
        )
    assert resp.status_code == 404
    assert resp.json()["message"] == "Recipe not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_comment_rating_too_low(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": -0.1,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
    assert resp.status_code == 400
    assert "between 0.0 and 5.0" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_comment_rating_too_high(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 5.1,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
    assert resp.status_code == 400
    assert "between 0.0 and 5.0" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_comment_rating_boundary_min(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 0.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
    assert resp.status_code == 201
    assert float(resp.json()["rating"]) == 0.0


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_create_comment_rating_boundary_max(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 5.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
    assert resp.status_code == 201
    assert float(resp.json()["rating"]) == 5.0


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_comment_found(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/comments/",
            json={
                "title": "Nice Recipe",
                "text": "Really good!",
                "rating": 4.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        comment_id = post.json()["id"]
        resp = await ac.get(f"/comments/{comment_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Nice Recipe"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_comment_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/comments/999")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Comment not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_comments_list(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/comments/",
            json={
                "title": "Comment 1",
                "text": "Text 1",
                "rating": 4.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        await ac.post(
            "/comments/",
            json={
                "title": "Comment 2",
                "text": "Text 2",
                "rating": 5.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        resp = await ac.get("/comments/")
    assert resp.status_code == 200
    titles = {c["title"] for c in resp.json()}
    assert {"Comment 1", "Comment 2"}.issubset(titles)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_read_comments_pagination(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        for i in range(5):
            await ac.post(
                "/comments/",
                json={
                    "title": f"Comment {i}",
                    "text": f"Text {i}",
                    "rating": 4.0,
                    "user_id": user.id,
                    "recipe_id": recipe.id,
                },
            )
        resp = await ac.get("/comments/?offset=2&limit=2")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_update_comment_success(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/comments/",
            json={
                "title": "Old Title",
                "text": "Old text",
                "rating": 3.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        comment_id = post.json()["id"]
        resp = await ac.patch(
            f"/comments/{comment_id}",
            json={"title": "New Title", "text": "New text", "rating": 4.5},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New Title"
    assert data["text"] == "New text"
    assert float(data["rating"]) == 4.5


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_comment_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.patch("/comments/999", json={"text": "Test"})
    assert resp.status_code == 404
    assert resp.json()["message"] == "Comment not found"


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_comment_rating_too_low(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 3.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        comment_id = post.json()["id"]
        resp = await ac.patch(f"/comments/{comment_id}", json={"rating": -1.0})
    assert resp.status_code == 400
    assert "between 0.0 and 5.0" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_update_comment_rating_too_high(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 3.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        comment_id = post.json()["id"]
        resp = await ac.patch(f"/comments/{comment_id}", json={"rating": 6.0})
    assert resp.status_code == 400
    assert "between 0.0 and 5.0" in resp.json()["message"]


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
async def test_update_comment_without_rating(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/comments/",
            json={
                "title": "Test",
                "text": "Test",
                "rating": 3.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        comment_id = post.json()["id"]
        resp = await ac.patch(f"/comments/{comment_id}", json={"text": "Updated text"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "Updated text"
    assert float(data["rating"]) == 3.0  # Rating unchanged


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_delete_comment_success(app, recipe, user):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        post = await ac.post(
            "/comments/",
            json={
                "title": "Temp",
                "text": "Temp",
                "rating": 3.0,
                "user_id": user.id,
                "recipe_id": recipe.id,
            },
        )
        comment_id = post.json()["id"]
        resp = await ac.delete(f"/comments/{comment_id}")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_delete_comment_not_found(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.delete("/comments/999")
    assert resp.status_code == 404
    assert resp.json()["message"] == "Comment not found"
