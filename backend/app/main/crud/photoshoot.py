from fastapi import HTTPException

from backend.app.main.models import Photoshoot as PhotoshootModel
from backend.app.main.models import db as gino_db


class PhotoshootCRUD:
    @staticmethod
    async def is_photoshoot(title: str):
        if await PhotoshootModel.query.where(PhotoshootModel.title == title).gino.first():
            raise HTTPException(status_code=400, detail="Photoshoot already exists")
        photoshoot = PhotoshootModel.query.where(PhotoshootModel.id == id).gino.first()
        return photoshoot

    @staticmethod
    async def get_photoshoot(photoshoot_id: int = None):
        photoshoot = await PhotoshootModel.query.where(PhotoshootModel.id == photoshoot_id).gino.first()
        if not photoshoot:
            raise HTTPException(status_code=404, detail="photoshoot not found")
        return photoshoot

    @staticmethod
    async def create_photoshoot(photographer_id: int, title: str, description: str, limit: int):
        new_photoshoot = await PhotoshootModel.create(photographer_id=photographer_id,
                                                      title=title, description=description, limit=limit)
        return new_photoshoot

    async def update(self, db: gino_db, db_obj: PhotoshootModel, obj_in: dict):
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"photoshoot not found")
        return super().update(db, db_obj, obj_in)
