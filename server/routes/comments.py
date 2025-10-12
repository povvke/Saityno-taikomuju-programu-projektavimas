from typing import Annotated
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from sqlmodel import select

from ..models import (
    Comment,
    CommentBase,
    CommentPublic,
    CommentUpdate,
    Message,
    Recipe,
    SessionDep,
)


router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=CommentPublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
        400: {"model": Message, "description": "Bad Request Error"},
    },
)
async def create_comment(comment: CommentBase, session: SessionDep):
    recipe = session.get(Recipe, comment.recipe_id)
    if not recipe:
        return JSONResponse(status_code=404, content={"message": "Recipe not found"})

    if comment.rating < 0.0 or comment.rating > 5.0:
        return JSONResponse(
            status_code=400, content={"message": "Rating must be between 0.0 and 5.0"}
        )

    db_comment = Comment.model_validate(comment)
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    return db_comment


@router.get(
    "/{id}",
    response_model=CommentPublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
    },
)
async def read_comment(id: int, session: SessionDep):
    comment = session.get(Comment, id)
    if not comment:
        return JSONResponse(status_code=404, content={"message": "Comment not found"})
    return comment


@router.get("/", response_model=list[CommentPublic])
async def read_comments(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    comments = session.exec(select(Comment).offset(offset).limit(limit)).all()
    return comments


@router.patch(
    "/{id}",
    response_model=CommentPublic,
    responses={
        404: {"model": Message, "description": "Not Found Error"},
        400: {"model": Message, "description": "Bad Request Error"},
    },
)
async def update_comment(id: int, comment: CommentUpdate, session: SessionDep):
    comment_db = session.get(Comment, id)
    if not comment_db:
        return JSONResponse(status_code=404, content={"message": "Comment not found"})

    if comment.rating:
        if comment.rating < 0.0 or comment.rating > 5.0:
            return JSONResponse(
                status_code=400,
                content={"message": "Rating must be between 0.0 and 5.0"},
            )

    comment_data = comment.model_dump(exclude_unset=True)
    _ = comment_db.sqlmodel_update(comment_data)
    session.add(comment_db)
    session.commit()
    session.refresh(comment_db)
    return comment_db


@router.delete(
    "/{id}",
    responses={
        404: {"model": Message, "description": "Not Found Error"},
    },
)
async def delete_comment(
    id: int,
    session: SessionDep,
):
    comment = session.get(Comment, id)
    if not comment:
        return JSONResponse(status_code=404, content={"message": "Comment not found"})

    session.delete(comment)
    session.commit()
    return {"ok": True}
