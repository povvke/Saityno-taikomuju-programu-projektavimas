SECRET = "243a4c253de2af5447ae4abfe707dbb5a4b3080a59bcd8dd8ec459f493dfadad"
ALGORITHM = "HS256"

import time
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyCookie
import jwt

import bcrypt
from sqlmodel import select

from ..models import Message, SessionDep, User, UserBase, UserLoginSchema


import re

email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

access_token_cookie = APIKeyCookie(name="access_token", auto_error=True)


def is_valid_email(email: str):
    return bool(email_regex.match(email))


def sign_jwt(user_id: int) -> str:
    payload = {"sub": str(user_id), "expires": time.time() + 600}
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return token


def decode_jwt(token: str) -> dict | None:
    decoded_token = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
    return decoded_token if decoded_token["expires"] >= time.time() else None


router = APIRouter()


@router.post(
    "/register",
    responses={
        409: {"model": Message, "description": "Conflict Error"},
        400: {"model": Message, "description": "Bad Request Error"},
    },
)
async def create_user(user: UserBase, session: SessionDep, response: Response):
    if not is_valid_email(user.email):
        return JSONResponse(
            status_code=400,
            content={"message": "Invalid email address"},
        )

    existing_user = session.exec(
        select(User).where(User.email == user.email or User.username == user.username)
    ).first()

    if existing_user:
        return JSONResponse(
            status_code=409,
            content={"message": "User with this email or username already exists"},
        )

    s = bcrypt.gensalt()
    h = bcrypt.hashpw(bytes(user.password, "UTF-8"), s)

    user_in_db = User(
        username=user.username,
        email=user.email,
        password=h.decode("UTF-8"),
        role="USER",
    )
    session.add(user_in_db)
    session.commit()
    session.refresh(user_in_db)
    token = sign_jwt(user_in_db.id)
    response.set_cookie(key="access_token", value=token)
    return {"message": "User created successfully"}


@router.post(
    "/login",
    responses={
        401: {"model": Message, "description": "Authorization Error"},
    },
)
async def login_user(user: UserLoginSchema, session: SessionDep, response: Response):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if not existing_user:
        return JSONResponse(
            status_code=401,
            content={"message": "Incorrect email or password"},
        )

    if bcrypt.checkpw(
        bytes(user.password, "UTF-8"), bytes(existing_user.password, "UTF-8")
    ):
        token = sign_jwt(existing_user.id)
        response.set_cookie(key="access_token", value=token)
        return {"message": "Logged in successfully"}
    else:
        return JSONResponse(
            status_code=401,
            content={"message": "Incorrect email or password"},
        )


async def get_current_user(
    session: SessionDep, api_key: str = Depends(access_token_cookie)
) -> User | JSONResponse:
    access = api_key
    if not access:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization tokens",
        )

    payload = decode_jwt(access)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        )

    user_id = payload["sub"]

    if payload == {}:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        )

    # Fetch from DB
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Failed to login",
        )

    return user
