from typing import Optional, Type

from sqlalchemy.orm import Session

import db
from fastapi import Request
from fastapi.responses import JSONResponse

from api_singleton import ApiSingleton
from decorators.auth_decorators import auth_required
from decorators.secure_decorators import verify_required
from utils import auth_utils


class PodcastsRoutes:
    @staticmethod
    @verify_required
    def __create_method(request: Request, name: str, description: str, category_id: Optional[int] = None):
        session = db.Session(bind=db.Engine)

        podcast_with_name_already_exists = session.query(db.Podcast).filter(db.Podcast.name == name).scalar()

        if podcast_with_name_already_exists:
            return JSONResponse({"successful": False,
                                 "error_code": 1,
                                 "reason": "Подкаст с данным именем уже существует!"})

        if category_id is not None:
            category_exists = session.query(db.Category).filter(db.Category.id == category_id).scalar()

            if not category_exists:
                return JSONResponse({"successful": False,
                                     "error_code": 2,
                                     "reason": "Неверная категория!"})

        user = auth_utils.get_user_by_request(request)

        podcast = db.Podcast(name=name,
                             description=description,
                             category_id=category_id,
                             owner_id=user.id)

        session.add(podcast)
        session.commit()

        response = JSONResponse({"id": podcast.id,
                                 "name": podcast.name,
                                 "description": podcast.description,
                                 "owner_id": podcast.owner_id})

        session.close()

        return response

    @staticmethod
    @auth_required
    def __my_podcasts_list_method(request: Request):
        session = Session(bind=db.Engine)

        user = auth_utils.get_user_by_request(request)

        podcasts: list[Type[db.Podcast]] = session.query(db.Podcast).filter_by(owner_id=user.id).all()

        podcasts_list = []

        for podcast in podcasts:
            podcasts_list.append({"id": podcast.id,
                                  "name": podcast.name,
                                  "description": podcast.description,
                                  "owner_id": podcast.owner_id})

        session.close()

        return JSONResponse(podcasts_list)

    @staticmethod
    def __all_podcasts_list_method():
        session = Session(bind=db.Engine)

        podcasts: list[Type[db.Podcast]] = session.query(db.Podcast).all()

        podcasts_list = []

        for podcast in podcasts:
            podcasts_list.append({"id": podcast.id,
                                  "name": podcast.name,
                                  "description": podcast.description,
                                  "owner_id": podcast.owner_id})

        session.close()

        return JSONResponse(podcasts_list)

    @staticmethod
    def __podcasts_with_category_method(category_id: int):
        session = Session(bind=db.Engine)

        podcasts: list[Type[db.Podcast]] = session.query(db.Podcast).filter_by(category_id=category_id).all()

        podcasts_list = []

        for podcast in podcasts:
            podcasts_list.append({"id": podcast.id,
                                  "name": podcast.name,
                                  "description": podcast.description,
                                  "owner_id": podcast.owner_id})

        session.close()

        return JSONResponse(podcasts_list)

    @staticmethod
    @auth_required
    def __follow_podcast_method(request: Request, podcast_id: int):
        session = Session(bind=db.Engine)

        user = auth_utils.get_user_by_request(request)

        is_already_follow = session.query(db.FollowingPodcast)\
            .filter(db.FollowingPodcast.user_id == user.id and db.FollowingPodcast.podcast_id == podcast_id).scalar()

        if is_already_follow:
            return JSONResponse({"successful": False,
                                 "error_code": 1,
                                 "reason": "Вы уже следите за данным подкастом!"})

        following_podcast = db.FollowingPodcast(user_id=user.id,
                                                podcast_id=podcast_id)

        session.add(following_podcast)
        session.commit()

        response = JSONResponse({"successful": True,
                                 "following_id": following_podcast.id})

        session.close()

        return response

    @staticmethod
    @auth_required
    def __unfollow_podcast_method(request: Request, podcast_id: int):
        session = Session(bind=db.Engine)

        user = auth_utils.get_user_by_request(request)

        session.query(db.FollowingPodcast)\
            .filter(db.FollowingPodcast.user_id == user.id
                    and db.FollowingPodcast.podcast_id == podcast_id).delete(synchronize_session='fetch')

        session.commit()

        return JSONResponse({"successful": True})

    @staticmethod
    @auth_required
    def __followed_podcasts_list_method(request: Request):
        session = Session(bind=db.Engine)

        user = auth_utils.get_user_by_request(request)

        # TODO: Refactor this
        podcasts = session.query(db.Podcast).join(db.FollowingPodcast)\
            .filter(db.FollowingPodcast.user_id == user.id).all()

        podcasts_list = []

        for podcast in podcasts:
            podcasts_list.append({"id": podcast.id,
                                  "name": podcast.name,
                                  "description": podcast.description,
                                  "owner_id": podcast.owner_id,
                                  "category_id": podcast.category_id})

        session.close()

        return JSONResponse(podcasts_list)

    def register_routes(self):
        api = ApiSingleton.instance()

        api.register_route("/podcasts/create", self.__create_method, methods=["POST"], tags=["podcasts"])

        api.register_route("/podcasts/my", self.__my_podcasts_list_method, methods=["GET"], tags=["podcasts"])
        api.register_route("/podcasts/followed", self.__followed_podcasts_list_method, methods=["GET"], tags=["podcasts"])

        api.register_route("/podcasts/all", self.__all_podcasts_list_method, methods=["GET"], tags=["podcasts"])
        api.register_route("/podcasts/with_category", self.__podcasts_with_category_method, methods=["GET"], tags=["podcasts"])

        api.register_route("/podcasts/follow", self.__follow_podcast_method, methods=["POST"], tags=["podcasts"])
        api.register_route("/podcasts/unfollow", self.__unfollow_podcast_method, methods=["POST"], tags=["podcasts"])