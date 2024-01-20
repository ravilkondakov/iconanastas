from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.app.main.models import User as UserModel
from backend.app.main.schemas import UserCreate


class UserCRUD:
    @staticmethod
    async def is_username(username: str):
        if await UserModel.query.where(UserModel.username == username).gino.first():
            raise HTTPException(status_code=400, detail="User already exists")
        user = UserModel.query.where(UserModel.username == username).gino.first()
        return user

    @staticmethod
    async def get_user(user_id: int = None, username: str = None):
        if user_id:
            user = await UserModel.query.where(UserModel.id == user_id).gino.first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            user = await UserModel.query.where(UserModel.username == username).gino.first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def create_user(user: UserCreate):
        new_user = await UserModel.create(username=user.username, phone=user.phone, password=user.password)
        return new_user

    async def update(self, db: Session, db_obj: UserModel, obj_in: dict):
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"User not found")
        return super().update(db, db_obj, obj_in)
