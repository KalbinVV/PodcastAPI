import datetime
import hashlib
from typing import Type

from fastapi.responses import JSONResponse
from fastapi import Request

import jwt
from sqlalchemy.orm import Session

import config
import db
from api_singleton import ApiSingleton
from decorators.auth_decorators import not_auth_required
from utils import auth_utils


class AuthRoutes:
    @staticmethod
    @not_auth_required
    def __auth_method(_request: Request, login: str, password: str, remember_me: bool = False):
        session = Session(bind=db.Engine)

        hashed_password = hashlib.sha3_256(password.encode()).hexdigest()

        user: Type[db.User] = session.query(db.User).filter(db.User.login == login
                                                            and db.User.hashed_password == hashed_password).first()

        if user is None:
            return JSONResponse({"successful": False, "error_code": 1,
                                 "reason": "Неверные данные для входа!"})

        if not user.is_active:
            return JSONResponse({"successful": False, "error_code": 2,
                                 "reason": "Ваша учетная запись заблокирована!"})

        jwt_dict = {"user_id": str(user.id)}

        if not remember_me:
            jwt_dict["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1)

        encoded = jwt.encode(jwt_dict, config.SECRET, algorithm="HS256")

        response = JSONResponse({"user_id": user.id,
                                 "login": user.login,
                                 "email": user.email,
                                 "role_id": user.role_id})
        response.set_cookie(key="token", value=encoded)

        session.close()

        return response

    @staticmethod
    @not_auth_required
    def __register_method(_request: Request,
                          login: str,
                          password: str,
                          email: str = None,
                          remember_me: bool = False):
        session = Session(bind=db.Engine)

        user_with_this_login_already_exists = session.query(db.User) \
            .filter(db.User.login == login).scalar()

        if user_with_this_login_already_exists:
            return JSONResponse({"successful": False,
                                 "error_code": 1,
                                 "reason": "Пользователь с таким именем уже существует!"})

        if email is not None:
            user_with_this_mail_already_exists = session.query(db.User) \
                .filter(db.User.email == email).scalar()

            if user_with_this_mail_already_exists:
                return JSONResponse({"successful": False,
                                     "error_code": 2,
                                     "reason": "Данная почта уже занята!"})

        user = db.User(login=login,
                       hashed_password=hashlib.sha3_256(password.encode()).hexdigest(),
                       email=email)

        session.add(user)
        session.commit()

        jwt_dict = {"user_id": str(user.id)}

        if not remember_me:
            jwt_dict["exp"] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1)

        encoded = jwt.encode(jwt_dict, config.SECRET, algorithm="HS256")

        session.close()

        response = JSONResponse({"successful": True,
                                 "user_id": user.id,
                                 "login": user.login,
                                 "email": user.email,
                                 "role_id": user.role_id
                                 })

        response.set_cookie(key="token", value=encoded)

        return response

    @staticmethod
    def __logout_method(_request: Request):
        response = JSONResponse({"successful": True})

        response.delete_cookie(key="token")

        return response

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/auth/login", self.__auth_method, methods=["GET"], tags=["auth"])
        api.register_route("/auth/logout", self.__logout_method, methods=["GET"], tags=["auth"])
        api.register_route("/auth/register", self.__register_method, methods=["POST"], tags=["auth"])
