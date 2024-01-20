from fastapi import HTTPException

from backend.app.main.models import Photographer as PhotographerModel
from backend.app.main.schemas import PhotographerBase
from backend.app.main.models import db as gino_db


class PhotographerCRUD:
    @staticmethod
    async def is_photographer(insta_name: str):
        if await PhotographerModel.query.where(PhotographerModel.insta_name == insta_name).gino.first():
            raise HTTPException(status_code=400, detail="Photographer already exists")
        photographer = PhotographerModel.query.where(PhotographerModel.insta_name == insta_name).gino.first()
        return photographer

    @staticmethod
    async def get_photographer(photographer_id: int = None, insta_name: str = None):
        if photographer_id:
            photographer = await PhotographerModel.query.where(PhotographerModel.id == photographer_id).gino.first()
            if not photographer:
                raise HTTPException(status_code=404, detail="photographer not found")
        else:
            photographer = await PhotographerModel.query.where(PhotographerModel.insta_name == insta_name).gino.first()
            if not photographer:
                raise HTTPException(status_code=404, detail="photographer not found")
        return photographer

    @staticmethod
    async def create_photographer(photographer: PhotographerBase):
        new_photographer = await PhotographerModel.create(user_id=photographer.user_id,
                                                          insta_name=photographer.insta_name,
                                                          title=photographer.title)
        return new_photographer

    async def update(self, db: gino_db, db_obj: PhotographerModel, obj_in: dict):
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"photographer not found")
        return super().update(db, db_obj, obj_in)
