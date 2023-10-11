import hashlib
from typing import Type

from fastapi.responses import JSONResponse
from fastapi import Request

import jwt
from sqlalchemy.orm import Session

import config
import db
from api_singleton import ApiSingleton


class AuthRoutes:
    @staticmethod
    def __auth_method(login: str, password: str):
        session = Session(bind=db.Engine)

        hashed_password = hashlib.sha3_256(password.encode()).hexdigest()

        user = session.query(db.User).filter(db.User.login == login
                                             and db.User.hashed_password == hashed_password).first()

        if user is None:
            return JSONResponse({"successful": False, "reason": "Неверные данные для входа"})

        encoded = jwt.encode({"user_id": str(user.id)}, config.SECRET, algorithm="HS256")

        response = JSONResponse({"user_id": user.id, "login": user.login, "email": user.email})
        response.set_cookie(key="token", value=encoded)

        session.close()

        return response

    @staticmethod
    def __register_method(login: str, password: str):
        session = Session(bind=db.Engine)

        user = db.User(login=login,
                       hashed_password=hashlib.sha3_256(password.encode()).hexdigest())

        session.add(user)
        session.commit()

        encoded = jwt.encode({"user_id": str(user.id)}, config.SECRET, algorithm="HS256")

        session.close()

        response = JSONResponse({"successful": True, "user_id": user.id})

        response.set_cookie(key="token", value=encoded)

        return response

    @staticmethod
    def __me_method(request: Request):
        token = request.cookies.get("token")

        if token is None:
            return JSONResponse({"successful": False, "reason": "Пользователь не авторизирован"})

        decoded = jwt.decode(token, config.SECRET, algorithms=["HS256"])

        user_id = decoded['user_id']

        session = Session(bind=db.Engine)

        user: Type[db.User] = session.query(db.User).filter(db.User.id == int(user_id)).one()

        response = JSONResponse({"user_id": user.id, "login": user.login, "email": user.email})

        session.close()

        return response

    @staticmethod
    def __logout_method():
        response = JSONResponse({"successful": True})

        response.delete_cookie(key="token")

        return response

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/auth/login", self.__auth_method, methods=["GET"])
        api.register_route("/auth/logout", self.__logout_method, methods=["GET"])
        api.register_route("/auth/register", self.__register_method, methods=["GET"])
        api.register_route("/auth/me", self.__me_method, methods=["GET"])
