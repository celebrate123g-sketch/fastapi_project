
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import UserModel
from dependencies.auth import get_current_user, get_admin_user

from schemas.notification import (
    NotificationCreate,
    NotificationResponse
)

from services.notification_service import (
    create_notification,
    get_notifications,
    get_recent_notifications,
    get_unread_notifications,
    get_unread_count,
    mark_as_read,
    mark_all_as_read,
    delete_notification,
    delete_all_notifications
)


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@router.post(
    "",
    response_model=NotificationResponse
)
def add_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return create_notification(
        db,
        notification
    )


@router.get(
    "",
    response_model=list[NotificationResponse]
)
def notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_notifications(
        db,
        current_user.id,
        skip,
        limit
    )


@router.get(
    "/recent",
    response_model=list[NotificationResponse]
)
def recent_notifications(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_recent_notifications(
        db,
        current_user.id,
        limit
    )


@router.get(
    "/unread",
    response_model=list[NotificationResponse]
)
def unread_notifications(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return get_unread_notifications(
        db,
        current_user.id
    )


@router.get(
    "/unread/count"
)
def unread_notifications_count(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return {
        "count": get_unread_count(
            db,
            current_user.id
        )
    }


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return mark_as_read(
        db,
        current_user.id,
        notification_id
    )


@router.put(
    "/read-all"
)
def read_all_notifications(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return mark_all_as_read(
        db,
        current_user.id
    )


@router.delete(
    "/{notification_id}"
)
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return delete_notification(
        db,
        current_user.id,
        notification_id
    )


@router.delete(
    ""
)
def remove_all_notifications(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return delete_all_notifications(
        db,
        current_user.id
    )
