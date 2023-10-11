from api_singleton import ApiSingleton
from utils import auth_utils

from fastapi.responses import Response, JSONResponse

from fastapi import Request


class UsersRoutes:
    @staticmethod
    def __user_at_method(user_id: int):
        user = auth_utils.get_user_by_id(user_id)

        if user is None:
            return Response(status_code=404)

        return JSONResponse({"user_id": user.id,
                             "login": user.login,
                             "email": user.email,
                             "role_id": user.role_id,
                             "is_verified": user.is_verified,
                             "is_active": user.is_active})

    @staticmethod
    def __me_method(request: Request):
        user_id = auth_utils.get_user_id_by_request(request)
        user = auth_utils.get_user_by_id(user_id)

        response = JSONResponse({"user_id": user.id,
                                 "login": user.login,
                                 "email": user.email,
                                 "role_id": user.role_id,
                                 "is_verified": user.is_verified,
                                 "is_active": user.is_active})

        return response

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/users/", self.__user_at_method, methods=["GET"], tags=["users"])
        api.register_route("/users/me", self.__me_method, methods=["GET"], tags=["users"])
