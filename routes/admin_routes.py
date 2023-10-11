from sqlalchemy.orm import Session

import db
from api_singleton import ApiSingleton
from decorators.secure_decorators import permission_required

from fastapi.responses import JSONResponse
from fastapi import Request

from utils import auth_utils


class AdminRoutes:
    @staticmethod
    @permission_required(permission_name='can_modify_users')
    def __ban_user_method(_request: Request, user_id: int):
        session = Session(bind=db.Engine)

        session.query(db.User).filter(db.User.id == user_id).update({"is_active": False})

        session.commit()
        session.close()

        return JSONResponse({"banned_user_id": user_id})

    @staticmethod
    @permission_required(permission_name='can_modify_users')
    def __unban_user_method(_request: Request, user_id: int):
        session = Session(bind=db.Engine)

        session.query(db.User).filter(db.User.id == user_id).update({"is_active": True})

        session.commit()
        session.close()

        return JSONResponse({"unbanned_user_id": user_id})

    @staticmethod
    @permission_required(permission_name='can_modify_users')
    def __verify_user_method(_request: Request, user_id: int):
        session = Session(bind=db.Engine)

        session.query(db.User).filter(db.User.id == user_id).update({"is_verified": True})

        session.commit()
        session.close()

        return JSONResponse({"verified_user_id": user_id})

    @staticmethod
    @permission_required(permission_name="can_modify_roles")
    def __add_role_method(_request: Request, role_name: str,
                          can_modify_users: bool = False,
                          can_modify_roles: bool = False,
                          can_modify_categories: bool = False,
                          can_modify_podcasts: bool = False,
                          can_modify_comments: bool = False):
        role = db.Role(name=role_name,
                       can_modify_users=can_modify_users,
                       can_modify_roles=can_modify_roles,
                       can_modify_categories=can_modify_categories,
                       can_modify_podcasts=can_modify_podcasts,
                       can_modify_comments=can_modify_comments)

        session = Session(bind=db.Engine)

        session.add(role)
        session.commit()

        response = JSONResponse({"role_id": role.id,
                                 "role_name": role.name,
                                 "can_modify_users": role.can_modify_users,
                                 "can_modify_roles": role.can_modify_roles,
                                 "can_modify_categories": role.can_modify_categories,
                                 "can_modify_podcasts": role.can_modify_podcasts,
                                 "can_modify_comments": role.can_modify_comments
                                 })

        session.close()

        return response

    @staticmethod
    @permission_required(permission_name="can_modify_roles")
    def __set_user_role_method(_request: Request, user_id: int, role_id: int):
        session = db.Session(bind=db.Engine)

        session.query(db.User).filter(db.User.id == user_id).update({"role_id": role_id})

        session.commit()
        session.close()

        user = auth_utils.get_user_by_id(user_id)
        role = auth_utils.get_role_by_id(user.role_id)

        return JSONResponse({"user_id": user.id,
                             "role_id": role.id,
                             "role_name": role.name,
                             "can_modify_users": role.can_modify_users,
                             "can_modify_roles": role.can_modify_roles,
                             "can_modify_categories": role.can_modify_categories,
                             "can_modify_podcasts": role.can_modify_podcasts,
                             "can_modify_comments": role.can_modify_comments
                             })

    @staticmethod
    @permission_required(permission_name="can_modify_roles")
    def __roles_list_method(_request: Request):
        session = db.Session(bind=db.Engine)

        roles = session.query(db.Role).all()

        roles_list = []

        for role in roles:
            roles_list.append({"role_id": role.id,
                               "role_name": role.name,
                               "can_modify_users": role.can_modify_users,
                               "can_modify_roles": role.can_modify_roles,
                               "can_modify_categories": role.can_modify_categories,
                               "can_modify_podcasts": role.can_modify_podcasts,
                               "can_modify_comments": role.can_modify_comments})

        session.close()

        return JSONResponse(roles_list)

    @staticmethod
    @permission_required(permission_name="can_modify_categories")
    def __add_category_method(_request: Request, category_name: str, category_description: str):
        session = Session(bind=db.Engine)

        category = db.Category(name=category_name,
                               description=category_description)

        session.add(category)
        session.commit()

        response = JSONResponse({"category_id": category.id,
                                 "name": category.name,
                                 "description": category.description})

        session.close()

        return response

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/admin/users/ban_user", self.__ban_user_method, methods=["PUT"], tags=["admin"])
        api.register_route("/admin/users/unban_user", self.__unban_user_method, methods=["PUT"], tags=["admin"])
        api.register_route("/admin/users/verify_user", self.__verify_user_method, methods=["PUT"], tags=["admin"])

        api.register_route("/admin/roles/add_role", self.__add_role_method, methods=["POST"], tags=["admin"])
        api.register_route("/admin/roles/set_user_role", self.__set_user_role_method, methods=["PUT"], tags=["admin"])
        api.register_route("/admin/roles/roles_list", self.__roles_list_method, methods=["GET"], tags=["admin"])

        api.register_route("/admin/categories/add_category", self.__add_category_method, methods=["POST"], tags=["admin"])
