from typing import Optional

import jwt
from fastapi import Request
from sqlalchemy.orm import Session

import config
import db


def get_user_id_by_request(request: Request) -> Optional[int]:
    token = request.cookies.get('token')

    if token is None:
        return None

    try:
        decoded_jwt = jwt.decode(token, config.SECRET, algorithms=["HS256"])

        return decoded_jwt['user_id']
    except jwt.ExpiredSignatureError:
        return None


def get_user_by_id(user_id: Optional[int]) -> Optional[db.User]:
    session = Session(bind=db.Engine)

    if user_id is None:
        return None

    user = session.query(db.User).filter(db.User.id == user_id).first()

    if user is None:
        return None
    else:
        cloned_user = db.User.clone(user)

        session.close()

        return cloned_user


def get_role_by_id(role_id: int) -> Optional[db.Role]:
    session = Session(bind=db.Engine)

    role = session.query(db.Role).filter(db.Role.id == role_id).first()

    if role is None:
        return None
    else:
        cloned_role = db.Role.clone(role)

        session.close()

        return cloned_role


def get_user_by_request(request: Request):
    user_id = get_user_id_by_request(request)

    return get_user_by_id(user_id)
