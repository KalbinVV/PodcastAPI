import uvicorn

from api_singleton import ApiSingleton
from db import init_tables
from routes.auth_routes import AuthRoutes

# For Uvicorn
app = ApiSingleton.instance().get_api()


def main() -> None:
    init_tables()

    auth_routes = AuthRoutes()

    auth_routes.register_routes()

    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info")


if __name__ == '__main__':
    main()
