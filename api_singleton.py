import json
from typing import Optional, Self, Callable
from fastapi import FastAPI

tags_metadata = [
    {
        "name": "auth",
        "description": "Авторизация/регистрация пользователей.",
    },
    {
        "name": "admin",
        "description": "Администрирование ресурса"
    },
    {
        "name": "categories",
        "description": "Доступ к категориям"
    },
    {
        "name": "secure",
        "description": "Методы для аутентификации"
    },
    {
        "name": "users",
        "description": "Доступ к пользователям"
    },
    {
        "name": "podcasts",
        "description": "Доступ к подкастам"
    }
]


class ApiSingleton:
    __instance_ptr: Optional[Self] = None

    @classmethod
    def instance(cls) -> Self:
        if cls.__instance_ptr is None:
            cls.__instance_ptr = ApiSingleton()

        return cls.__instance_ptr

    def __init__(self):
        self.__api = FastAPI(openapi_tags=tags_metadata)

    def register_route(self, path: str, endpoint: Callable, methods: list[str],
                       tags: Optional[list[str]] = None) -> None:
        if tags is None:
            tags = []

        self.__api.add_api_route(path, endpoint, methods=methods, tags=tags)

    def get_api(self) -> FastAPI:
        return self.__api
