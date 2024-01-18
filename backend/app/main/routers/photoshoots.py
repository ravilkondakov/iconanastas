from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.main.db.base import get_db
from backend.app.main.models import Photoshoot as PhotoshootModel
from backend.app.main.schemas import PhotoshootCreate, Photoshoot
from fastapi import APIRouter

router = APIRouter()


@router.post("/photoshoots/", response_model=Photoshoot)
async def create_photoshoot(photoshoot: PhotoshootCreate, db: Session = Depends(get_db)):
    db_photoshoot = PhotoshootModel(**photoshoot.dict())
    db.add(db_photoshoot)
    db.commit()
    db.refresh(db_photoshoot)
    return db_photoshoot


@router.get("/photoshoots/{photoshoot_id}", response_model=Photoshoot)
async def read_photoshoot(photoshoot_id: int, db: Session = Depends(get_db)):
    photoshoot = db.query(PhotoshootModel).filter(PhotoshootModel.id == photoshoot_id).first()
    if not photoshoot:
        raise HTTPException(status_code=404, detail="Photoshoot not found")
    return photoshoot


@router.put("/photoshoots/{photoshoot_id}", response_model=Photoshoot)
async def update_photoshoot(photoshoot_id: int, photoshoot_in: PhotoshootCreate, db: Session = Depends(get_db)):
    photoshoot = db.query(PhotoshootModel).filter(PhotoshootModel.id == photoshoot_id).first()
    if not photoshoot:
        raise HTTPException(status_code=404, detail="Photoshoot not found")

    for field, value in photoshoot_in.dict().items():
        setattr(photoshoot, field, value)

    db.commit()
    db.refresh(photoshoot)
    return photoshoot


@router.delete("/photoshoots/{photoshoot_id}", response_model=Photoshoot)
async def delete_photoshoot(photoshoot_id: int, db: Session = Depends(get_db)):
    photoshoot = db.query(PhotoshootModel).filter(PhotoshootModel.id == photoshoot_id).first()
    if not photoshoot:
        raise HTTPException(status_code=404, detail="Photoshoot not found")

    db.delete(photoshoot)
    db.commit()
    return photoshoot
