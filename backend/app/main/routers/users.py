from fastapi import Depends, HTTPException
from gino import Gino
from sqlalchemy.orm import Session

from backend.app.main.db.base import get_db
from backend.app.main.models import User as UserModel, db as gino_db
from backend.app.main.schemas import User, UserCreate
from fastapi import APIRouter

router = APIRouter()


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: gino_db = Depends(get_db)):
    if await UserModel.query.where(UserModel.username == user.username).gino.first():
        raise HTTPException(status_code=400, detail="User already exists")
    async with db.transaction():
        new_user = await UserModel.create(username=user.username, phone=user.phone, password=user.password)
    return new_user


@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_in.dict().items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user
