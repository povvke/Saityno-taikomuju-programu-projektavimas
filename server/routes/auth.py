SECRET = "243a4c253de2af5447ae4abfe707dbb5a4b3080a59bcd8dd8ec459f493dfadad"
ALGORITHM = "HS256"

import time
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import jwt

import bcrypt
from sqlmodel import select

from ..models import Message, SessionDep, User, UserBase, UserLoginSchema


import re

email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_valid_email(email: str):
    return bool(email_regex.match(email))


def token_response(token: str):
    return {"access_token": token}


def sign_jwt(user_id: int) -> dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}


router = APIRouter()


@router.post(
    "/register",
    responses={
        409: {"model": Message, "description": "Conflict Error"},
        400: {"model": Message, "description": "Bad Request Error"},
    },
)
async def create_user(user: UserBase, session: SessionDep):
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
    return sign_jwt(user_in_db.id)


@router.post(
    "/login",
    responses={
        404: {"model": Message, "description": "Not Found Error"},
    },
)
async def login_user(user: UserLoginSchema, session: SessionDep):
    return "yo"
