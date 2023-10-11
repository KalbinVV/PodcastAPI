from sqlalchemy import create_engine, Column, Text, BigInteger
from sqlalchemy.orm import declarative_base

import config

Engine = create_engine(config.DB_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    login = Column(Text, unique=True)
    hashed_password = Column(Text)
    email = Column(Text, nullable=True)


def init_tables():
    Base.metadata.create_all(Engine)

