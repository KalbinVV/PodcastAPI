
from api_singleton import ApiSingleton

from decorators.auth_decorators import auth_required

from fastapi import Request

from utils import auth_utils

from fastapi.responses import JSONResponse


class SecureRoutes:
    @staticmethod
    @auth_required
    def __get_my_role(request: Request):
        user_id = auth_utils.get_user_id_by_request(request)

        user = auth_utils.get_user_by_id(user_id)

        role = auth_utils.get_role_by_id(user.role_id)

        if role is None:
            return JSONResponse({"has_role": False, "role_name": "Common user"})
        else:
            return JSONResponse({"has_role": True,
                                 "role_id": role.id,
                                 "role_name": role.name,
                                 "can_modify_users": role.can_modify_users,
                                 "can_modify_roles": role.can_modify_roles,
                                 "can_modify_categories": role.can_modify_categories,
                                 "can_modify_podcasts": role.can_modify_podcasts,
                                 "can_modify_comments": role.can_modify_comments})

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/secure/my_role", self.__get_my_role, methods=["GET"], tags=["secure"])
