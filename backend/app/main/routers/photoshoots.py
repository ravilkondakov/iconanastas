from fastapi import Depends, HTTPException
from sqlalchemy import select

from backend.app.main.crud.photoshoot import PhotoshootCRUD
from backend.app.main.db.base import get_db
from backend.app.main.models import Photoshoot as PhotoshootModel, Photographer, db as gino_db
from backend.app.main.routers.auth import get_current_user
from backend.app.main.schemas import PhotoshootCreate, Photoshoot, PhotoshootBase
from fastapi import APIRouter

router = APIRouter()

DEFAULT_PHOTO_LIMIT = 15


@router.post("/create-photoshoot")
async def create_photoshoot(photoshoot: PhotoshootBase, current_user: dict = Depends(get_current_user)):
    photographer = await Photographer.query.where(Photographer.user_id == current_user).gino.first()
    if not photographer:
        raise HTTPException(status_code=404, detail="Photographer not found")
    await PhotoshootCRUD.is_photoshoot(photoshoot.title)
    photoshoot = await PhotoshootCRUD.create_photoshoot(photographer_id=photographer.id, title=photoshoot.title,
                                                        description=photoshoot.description,
                                                        limit=photoshoot.limit, )

    return photoshoot


# Выбор фотографий для фотосессии
@router.post("/select-photos/{photoshoot_id}")
async def select_photos(photoshoot_id: int, selected_photos: list[int], db: gino_db = Depends(get_db)):
    # Проверяем существование фотосессии
    photoshoot = await Photoshoot.get(photoshoot_id)
    if not photoshoot:
        raise HTTPException(status_code=404, detail="Photoshoot not found")

    # Проверяем, что количество выбранных фотографий не превышает лимит
    if len(selected_photos) > photoshoot.limit:
        raise HTTPException(status_code=400, detail="Exceeded photo selection limit")

    # Дополнительная логика для обработки выбранных фотографий
    # ...

    return {"message": "Photos selected successfully"}
