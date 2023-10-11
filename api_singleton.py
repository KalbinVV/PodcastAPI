from typing import Optional, Self, Callable
from fastapi import FastAPI


class ApiSingleton:
    __instance_ptr: Optional[Self] = None

    @classmethod
    def instance(cls) -> Self:
        if cls.__instance_ptr is None:
            cls.__instance_ptr = ApiSingleton()

        return cls.__instance_ptr

    def __init__(self):
        self.__api = FastAPI()

    def register_route(self, path: str, endpoint: Callable, methods: list[str]) -> None:
        self.__api.add_api_route(path, endpoint, methods=methods)

    def get_api(self) -> FastAPI:
        return self.__api

