from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi import APIRouter

from backend.app.main.db.base import get_db
from backend.app.main.schemas import Photographer, PhotographerCreate
from backend.app.main.models import Photographer as PhotographerModel

router = APIRouter()

@router.post("/photographers/", response_model=Photographer)
async def create_photographer(photographer: PhotographerCreate, db: Session = Depends(get_db)):
    db_photographer = PhotographerModel(**photographer.dict())
    db.add(db_photographer)
    db.commit()
    db.refresh(db_photographer)
    return db_photographer


@router.get("/photographers/{photographer_id}", response_model=Photographer)
async def read_photographer(photographer_id: int, db: Session = Depends(get_db)):
    photographer = db.query(PhotographerModel).filter(PhotographerModel.id == photographer_id).first()
    if not photographer:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return photographer


@router.put("/photographers/{photographer_id}", response_model=Photographer)
async def update_photographer(photographer_id: int, photographer_in: PhotographerCreate, db: Session = Depends(get_db)):
    photographer = db.query(PhotographerModel).filter(PhotographerModel.id == photographer_id).first()
    if not photographer:
        raise HTTPException(status_code=404, detail="Photographer not found")

    for field, value in photographer_in.dict().items():
        setattr(photographer, field, value)

    db.commit()
    db.refresh(photographer)
    return photographer


@router.delete("/photographers/{photographer_id}", response_model=Photographer)
async def delete_photographer(photographer_id: int, db: Session = Depends(get_db)):
    photographer = db.query(PhotographerModel).filter(PhotographerModel.id == photographer_id).first()
    if not photographer:
        raise HTTPException(status_code=404, detail="Photographer not found")

    db.delete(photographer)
    db.commit()
    return photographer
