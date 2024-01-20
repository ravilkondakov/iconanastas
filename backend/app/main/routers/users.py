from fastapi import Depends

from backend.app.main.crud.user import UserCRUD
from backend.app.main.db.base import get_db
from backend.app.main.models import db as gino_db
from backend.app.main.schemas import User, UserCreate, UserBase
from fastapi import APIRouter

router = APIRouter()


@router.post("/create", response_model=User)
async def create_user(user: UserCreate, db: gino_db = Depends(get_db)):
    await UserCRUD.is_username(user.username)
    async with db.transaction():
        new_user = await UserCRUD.create_user(user)
    return new_user


@router.get("/get/{user_id}", response_model=UserBase)
async def read_user(user_id: int):
    user = await UserCRUD.get_user(user_id)
    return user


@router.put("/update/{user_id}", response_model=User)
async def update_user(user_id: int, user_in: UserCreate):
    user = await UserCRUD.get_user(user_id)
    await user.update(**user_in.dict(exclude_unset=True)).apply()
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = await UserCRUD.get_user(user_id)
    await user.delete()
    return {"message": "User deleted successfully"}
