import uvicorn

from api_singleton import ApiSingleton
from db import init_tables
from routes.admin_routes import AdminRoutes
from routes.auth_routes import AuthRoutes
from routes.categories_routes import CategoriesRoutes
from routes.podcasts_routes import PodcastsRoutes
from routes.secure_rotes import SecureRoutes
from routes.users_routes import UsersRoutes

# For Uvicorn
app = ApiSingleton.instance().get_api()


def main() -> None:
    init_tables()

    auth_routes = AuthRoutes()
    secure_routes = SecureRoutes()
    admin_rotes = AdminRoutes()
    categories_routes = CategoriesRoutes()
    users_routes = UsersRoutes()
    podcasts_routes = PodcastsRoutes()

    auth_routes.register_routes()
    secure_routes.register_routes()
    admin_rotes.register_routes()
    categories_routes.register_routes()
    users_routes.register_routes()
    podcasts_routes.register_routes()

    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info")


if __name__ == '__main__':
    main()
