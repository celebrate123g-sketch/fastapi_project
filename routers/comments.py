
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import CommentModel, QuoteModel
from dependencies.auth import get_current_user
from schemas.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/{quote_id}", response_model=list[CommentResponse])
def get_comments(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(QuoteModel).filter(
        QuoteModel.id == quote_id,
        QuoteModel.is_deleted.is_(False)
    ).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    return db.query(CommentModel).filter(
        CommentModel.quote_id == quote_id
    ).order_by(CommentModel.created_at.desc()).all()


@router.post("/{quote_id}", response_model=CommentResponse)
def create_comment(
    quote_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    quote = db.query(QuoteModel).filter(
        QuoteModel.id == quote_id,
        QuoteModel.is_deleted.is_(False)
    ).first()

    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    comment = CommentModel(
        quote_id=quote_id,
        user_id=current_user.id,
        author=current_user.username,
        text=data.text
    )

    db.add(comment)
    quote.comments_count += 1
    db.commit()
    db.refresh(comment)

    return comment


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    comment = db.query(CommentModel).filter(
        CommentModel.id == comment_id
    ).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    quote = db.query(QuoteModel).filter(
        QuoteModel.id == comment.quote_id
    ).first()

    db.delete(comment)

    if quote and quote.comments_count > 0:
        quote.comments_count -= 1

    db.commit()

    return {"message": "Comment deleted"}
