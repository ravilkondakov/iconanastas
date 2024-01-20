from typing import List, Dict

from fastapi import Depends
from sqlalchemy.orm import Session

from fastapi import APIRouter

from backend.app.main.crud.photographer import PhotographerCRUD
from backend.app.main.db.base import get_db
from backend.app.main.schemas import Photographer, PhotographerCreate, UserBase

from backend.app.main.models import db as gino_db

router = APIRouter()


@router.post("/photographers/", response_model=Photographer)
async def create_photographer(photographer: PhotographerCreate, db: gino_db = Depends(get_db)):
    await PhotographerCRUD.is_photographer(photographer.insta_name)
    async with db.transaction():
        new_photographer = await PhotographerCRUD.create_photographer(photographer)
    return new_photographer


@router.get("/photographers/{photographer_id}", response_model=PhotographerCreate)
async def read_photographer(photographer_id: int):
    photographer = await PhotographerCRUD.get_photographer(photographer_id)
    return photographer


@router.put("/photographers/{photographer_id}", response_model=Photographer)
async def update_photographer(photographer_id: int, photographer_in: PhotographerCreate):
    photographer = await PhotographerCRUD.get_photographer(photographer_id)
    await photographer.update(**photographer_in.dict(exclude_unset=True)).apply()
    return photographer


@router.delete("/photographers/{photographer_id}", response_model=Photographer)
async def delete_photographer(photographer_id: int, db: Session = Depends(get_db)):
    photographer = await PhotographerCRUD.get_photographer(photographer_id)
    await photographer.delete()
    return {"message": "Photographer deleted successfully"}
