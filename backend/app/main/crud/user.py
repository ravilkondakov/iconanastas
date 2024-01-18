from sqlalchemy.orm import Session
from backend.app.main.models import User
from fastapi import HTTPException


class UserCRUD:
    def create_user(self, db: Session, username: str, phone: str, password: str):
        db_user = User(username=username, phone=phone, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_obj: User, obj_in: dict):
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"User not found")
        return super().update(db, db_obj, obj_in)
