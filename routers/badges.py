
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserModel
from dependencies.auth import get_current_user, get_admin_user

from schemas.badge import (
    BadgeResponse,
    BadgeStatistics
)

from services.badge_service import (
    get_all_badges,
    get_user_badges,
    get_quote_badges,
    get_badge_statistics
)

router = APIRouter(
    prefix="/badges",
    tags=["Badges"]
)


@router.get(
    "",
    response_model=list[BadgeResponse]
)
def badges():
    badges = get_all_badges()

    return [
        {
            **badge,
            "unlocked": False
        }
        for badge in badges
    ]


@router.get(
    "/user/{user_id}",
    response_model=list[BadgeResponse]
)
def user_badges(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own badges."
        )

    return get_user_badges(
        db,
        user_id
    )


@router.get(
    "/quote/{quote_id}",
    response_model=list[BadgeResponse]
)
def quote_badges(
    quote_id: int,
    db: Session = Depends(get_db)
):
    badges = get_quote_badges(
        db,
        quote_id
    )

    if badges is None:
        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    return badges


@router.get(
    "/statistics/{user_id}",
    response_model=BadgeStatistics
)
def badge_statistics(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view your own badge statistics."
        )

    return get_badge_statistics(
        db,
        user_id
    )
