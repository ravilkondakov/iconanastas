from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main.crud.user import UserCRUD
from backend.app.main.models import db as gino_db

SQLALCHEMY_DATABASE_URL = 'postgresql://iconanastas:leothebestcat1@localhost/iconanastas'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    try:
        yield gino_db
    finally:
        gino_db.pop_bind().close()


async def init_db():
    await gino_db.gino.create_all()

    async with gino_db.transaction():
        user_crud = UserCRUD()
        user = await user_crud.create_user(username="admin", phone="admin@example.com", password='admin')
