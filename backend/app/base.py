from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.main.db.base import SQLALCHEMY_DATABASE_URL
from backend.app.main.models import db as gino_db


@asynccontextmanager
async def lifespan(app):
    await gino_db.set_bind(SQLALCHEMY_DATABASE_URL)
    yield
    await gino_db.pop_bind().close()


app = FastAPI(lifespan=lifespan)


from backend.app.main.routers import auth, users, photoshoots, reviews, photos, photographers, messages, comments

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(photoshoots.router, prefix="/photoshoots", tags=["photoshoots"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(photos.router, prefix="/photos", tags=["photos"])
app.include_router(photographers.router, prefix="/photographers", tags=["photographers"])
app.include_router(messages.router, prefix="/messages", tags=["messages"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn

    lifespan(app=app)
    uvicorn.run("base:app", host="127.0.0.1", port=8000, reload=True)