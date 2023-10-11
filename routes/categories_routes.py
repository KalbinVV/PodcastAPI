from typing import Type

from sqlalchemy.orm import Session

import db

from fastapi.responses import JSONResponse

from api_singleton import ApiSingleton


class CategoriesRoutes:
    @staticmethod
    def __categories_list_method():
        session = Session(bind=db.Engine)

        categories: list[Type[db.Category]] = session.query(db.Category).all()

        categories_list = list()

        for category in categories:
            categories_list.append({"id": category.id,
                                    "name": category.name,
                                    "description": category.description})

        session.close()

        return JSONResponse(categories_list)

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/categories/list", self.__categories_list_method, methods=["GET"], tags=["categories"])
