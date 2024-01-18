from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.main.db.base import get_db
from backend.app.main.models import Photo as PhotoModel
from backend.app.main.schemas import PhotoCreate, Photo
from fastapi import APIRouter

router = APIRouter()


@router.post("/photos/", response_model=Photo)
async def create_photo(photo: PhotoCreate, db: Session = Depends(get_db)):
    db_photo = PhotoModel(**photo.dict())
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


@router.get("/photos/{photo_id}", response_model=Photo)
async def read_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(PhotoModel).filter(PhotoModel.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo


@router.put("/photos/{photo_id}", response_model=Photo)
async def update_photo(photo_id: int, photo_in: PhotoCreate, db: Session = Depends(get_db)):
    photo = db.query(PhotoModel).filter(PhotoModel.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    for field, value in photo_in.dict().items():
        setattr(photo, field, value)

    db.commit()
    db.refresh(photo)
    return photo


@router.delete("/photos/{photo_id}", response_model=Photo)
async def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    photo = db.query(PhotoModel).filter(PhotoModel.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    db.delete(photo)
    db.commit()
    return photo
