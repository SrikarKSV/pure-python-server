import os

from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, sessionmaker

from .modelbase import SqlAlchemyBase

__factory = None


def db_init():
    """Initializes database with given URI from .env"""
    global __factory

    if __factory:
        return

    engine = create_engine(
        os.getenv("DATABASE_URI", "sqlite:///posts.db"),
        echo=False,
        connect_args={"check_same_thread": False},
    )
    __factory = sessionmaker(bind=engine)
    print("📈 Successfully connected to DB")

    from ..db import models

    # If table don't exist, Create.
    if not inspect(engine).has_table("posts"):
        SqlAlchemyBase.metadata.tables["posts"].create(engine)


def create_session() -> Session:
    """Returns the database session"""
    global __factory
    return __factory()
