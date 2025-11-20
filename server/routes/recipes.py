from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from .auth import get_current_user

from ..models import (
    Category,
    Comment,
    CommentPublic,
    Message,
    Recipe,
    RecipeBase,
    RecipePublic,
    RecipeUpdate,
    SessionDep,
    User,
)

from ..utils import slugify


router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=RecipePublic,
    responses={
        409: {"model": Message, "description": "Conflict Error"},
        404: {"model": Message, "description": "Not Found Error"},
        403: {"model": Message, "description": "Forbidden Error"},
    },
)
async def create_recipe(
    recipe: RecipeBase,
    session: SessionDep,
    response: Response,
    user: User = Depends(get_current_user),
):
    try:
        category = session.get(Category, recipe.category_id)
        if not category:
            return JSONResponse(
                status_code=404,
                content={"message": "Category not found"},
                headers=response.headers,
            )

        slug = slugify(recipe.name)
        recipe_db = Recipe(
            name=recipe.name,
            slug=slug,
            description=recipe.description,
            instructions=recipe.instructions,
            ingredients=recipe.ingredients,
            calories=recipe.calories,
            prep_time=recipe.prep_time,
            servings=recipe.servings,
            category_id=recipe.category_id,
            author_id=user.id,
        )
        session.add(recipe_db)
        session.commit()
        session.refresh(recipe_db)
        return recipe_db
    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            return JSONResponse(
                status_code=409,
                content={"message": "Recipe with this slug already exists"},
                headers=response.headers,
            )


@router.get(
    "/{id}",
    response_model=RecipePublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
    },
)
async def read_recipe(id: int, session: SessionDep):
    recipe = session.get(Recipe, id)
    if not recipe:
        return JSONResponse(status_code=404, content={"message": "Recipe not found"})
    return recipe


@router.get("/", response_model=list[RecipePublic])
async def read_recipes(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    recipes = session.exec(select(Recipe).offset(offset).limit(limit)).all()
    return recipes


@router.patch(
    "/{id}",
    response_model=RecipePublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
        409: {"model": Message, "description": "Conflict Error"},
        403: {"model": Message, "description": "Forbidden Error"},
    },
)
async def update_recipe(
    id: int,
    recipe: RecipeUpdate,
    session: SessionDep,
    response: Response,
    user: User = Depends(get_current_user),
):
    try:
        recipe_db = session.get(Recipe, id)
        if not recipe_db:
            return JSONResponse(
                status_code=404,
                content={"message": "Recipe not found"},
                headers=response.headers,
            )

        if recipe_db.author_id is not user.id:
            return JSONResponse(
                status_code=403,
                content={"message": "You do not have rights to this resource"},
                headers=response.headers,
            )

        category = session.get(Category, recipe.category_id)
        if not category:
            return JSONResponse(
                status_code=404,
                content={"message": "Category not found"},
                headers=response.headers,
            )

        recipe_data = recipe.model_dump(exclude_unset=True)
        if recipe.name:
            recipe_data["slug"] = slugify(recipe.name)

        _ = recipe_db.sqlmodel_update(recipe_data)
        session.add(recipe_db)
        session.commit()
        session.refresh(recipe_db)
        return recipe_db

    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint failed" in str(e.orig):
            return JSONResponse(
                status_code=409,
                content={"message": "Recipe with this slug already exists"},
                headers=response.headers,
            )


@router.delete(
    "/{id}",
    responses={
        404: {"model": Message, "description": "Not Found Error"},
        403: {"model": Message, "description": "Forbidden Error"},
    },
)
async def delete_recipe(
    id: int,
    session: SessionDep,
    response: Response,
    user: User = Depends(get_current_user),
):
    recipe = session.get(Recipe, id)
    if not recipe:
        return JSONResponse(
            status_code=404,
            content={"message": "Recipe not found"},
            headers=response.headers,
        )

    if recipe.author_id is not user.id and user.role is not "ADMIN":
        return JSONResponse(
            status_code=403,
            content={"message": "You do not have rights to this resource"},
            headers=response.headers,
        )

    session.delete(recipe)
    session.commit()
    return {"ok": True}


@router.get("/{id}/comments", response_model=list[CommentPublic])
async def read_comments(
    id: int,
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    comments = session.exec(
        select(Comment).where(Comment.recipe_id == id).offset(offset).limit(limit)
    ).all()
    return comments
