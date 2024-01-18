from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.main.db.base import get_db
from backend.app.main.models import Comment as CommentModel
from backend.app.main.schemas import CommentCreate, Comment
from fastapi import APIRouter

router = APIRouter()


@router.post("/comments/", response_model=Comment)
async def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = CommentModel(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@router.get("/comments/{comment_id}", response_model=Comment)
async def read_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(comment_id: int, comment_in: CommentCreate, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    for field, value in comment_in.dict().items():
        setattr(comment, field, value)

    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/comments/{comment_id}", response_model=Comment)
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(CommentModel).filter(CommentModel.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    db.delete(comment)
    db.commit()
    return comment
