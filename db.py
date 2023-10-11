import hashlib
from typing import Self

from sqlalchemy import create_engine, Column, Text, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, Session

import config

Engine = create_engine(config.DB_URL)

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, unique=True)

    can_modify_users = Column(Boolean, default=False)
    can_modify_roles = Column(Boolean, default=False)
    can_modify_categories = Column(Boolean, default=False)
    can_modify_podcasts = Column(Boolean, default=False)
    can_modify_comments = Column(Boolean, default=False)

    @staticmethod
    def clone(role):
        return Role(id=role.id,
                    name=role.name,
                    can_modify_roles=role.can_modify_roles,
                    can_modify_categories=role.can_modify_categories,
                    can_modify_users=role.can_modify_users,
                    can_modify_podcasts=role.can_modify_podcasts,
                    can_modify_comments=role.can_modify_comments)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    login = Column(Text, unique=True)
    hashed_password = Column(Text)
    email = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=True)

    @staticmethod
    def clone(user):
        return User(id=user.id,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    login=user.login,
                    hashed_password=user.hashed_password,
                    email=user.email,
                    role_id=user.role_id)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, unique=True)
    description = Column(Text, unique=True)


class Podcast(Base):
    __tablename__ = 'podcasts'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text, unique=True)
    description = Column(Text, unique=True)
    category_id = Column(BigInteger, ForeignKey("categories.id"))
    owner_id = Column(BigInteger, ForeignKey("users.id"))


class FollowingPodcast(Base):
    __tablename__ = "followings_podcasts"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    podcast_id = Column(BigInteger, ForeignKey("podcasts.id"), nullable=False)


def init_tables():
    Base.metadata.create_all(Engine)

    init_admin_user()


def init_admin_user():
    session = Session(bind=Engine)

    is_root_role_exists = session.query(Role).filter(Role.name == 'Root').scalar()

    if not is_root_role_exists:
        root_role = Role(name=config.ROOT_ROLE_NAME,
                         can_modify_categories=True,
                         can_modify_users=True,
                         can_modify_roles=True,
                         can_modify_podcasts=True,
                         can_modify_comments=True)

        session.add(root_role)
    else:
        root_role = session.query(Role).filter(Role.name == config.ROOT_ROLE_NAME).one()

    is_admin_user_exists = session.query(User).filter(User.login == config.ROOT_LOGIN).scalar()

    if not is_admin_user_exists:
        admin_user = User(login=config.ROOT_LOGIN,
                          hashed_password=hashlib.sha3_256(config.ROOT_PASSWORD.encode()).hexdigest(),
                          role_id=root_role.id,
                          is_verified=True)

        session.add(admin_user)

    session.commit()
    session.close()
