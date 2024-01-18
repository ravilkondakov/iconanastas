from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.main.db.base import get_db
from backend.app.main.models import Message as MessageModel
from backend.app.main.schemas import MessageCreate, Message
from fastapi import APIRouter

router = APIRouter()


@router.post("/messages/", response_model=Message)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = MessageModel(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.get("/messages/{message_id}", response_model=Message)
async def read_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message


@router.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, message_in: MessageCreate, db: Session = Depends(get_db)):
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    for field, value in message_in.dict().items():
        setattr(message, field, value)

    db.commit()
    db.refresh(message)
    return message


@router.delete("/messages/{message_id}", response_model=Message)
async def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.query(MessageModel).filter(MessageModel.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(message)
    db.commit()
    return message
