
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserModel
from dependencies.auth import get_current_user, get_admin_user

from schemas.history import (
    QuoteHistoryResponse,
    UserHistoryResponse,
    LastViewedQuote,
    HistoryStatistics,
    ClearHistoryResponse
)

from services.history_service import (
    get_recent_history,
    get_user_history,
    get_last_viewed,
    clear_user_history,
    get_most_viewed,
    get_history_statistics
)

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get(
    "/recent",
    response_model=list[QuoteHistoryResponse]
)
def recent_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return get_recent_history(db, limit)


@router.get(
    "/user/{user_id}",
    response_model=UserHistoryResponse
)
def user_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot view another user's history."
        )

    return get_user_history(db, user_id)


@router.get(
    "/last",
    response_model=LastViewedQuote
)
def last_viewed(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    history = get_last_viewed(db, current_user.id)

    if history is None:
        raise HTTPException(
            status_code=404,
            detail="History is empty."
        )

    return history


@router.delete(
    "/user/{user_id}",
    response_model=ClearHistoryResponse
)
def clear_history(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot clear another user's history."
        )

    return clear_user_history(db, user_id)


@router.get(
    "/most-viewed"
)
def most_viewed(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return get_most_viewed(db, limit)


@router.get(
    "/statistics",
    response_model=HistoryStatistics
)
def statistics(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return get_history_statistics(db)
