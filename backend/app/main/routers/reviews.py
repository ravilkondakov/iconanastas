from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.main.db.base import get_db
from backend.app.main.models import Review as ReviewModel
from backend.app.main.schemas import ReviewCreate, Review
from fastapi import APIRouter

router = APIRouter()


@router.post("/reviews/", response_model=Review)
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = ReviewModel(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/reviews/{review_id}", response_model=Review)
async def read_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/reviews/{review_id}", response_model=Review)
async def update_review(review_id: int, review_in: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    for field, value in review_in.dict().items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


@router.delete("/reviews/{review_id}", response_model=Review)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return review
