from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db

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
    db: Session = Depends(get_db)
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
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return get_notifications(
        db,
        user_id,
        skip,
        limit
    )


@router.get(
    "/recent",
    response_model=list[NotificationResponse]
)
def recent_notifications(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_recent_notifications(
        db,
        user_id,
        limit
    )


@router.get(
    "/unread",
    response_model=list[NotificationResponse]
)
def unread_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_unread_notifications(
        db,
        user_id
    )


@router.get(
    "/unread/count"
)
def unread_notifications_count(
    user_id: int,
    db: Session = Depends(get_db)
):
    return {
        "count": get_unread_count(
            db,
            user_id
        )
    }


@router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def read_notification(
    notification_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return mark_as_read(
        db,
        user_id,
        notification_id
    )


@router.put(
    "/read-all"
)
def read_all_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):
    return mark_all_as_read(
        db,
        user_id
    )


@router.delete(
    "/{notification_id}"
)
def remove_notification(
    notification_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    return delete_notification(
        db,
        user_id,
        notification_id
    )


@router.delete(
    ""
)
def remove_all_notifications(
    user_id: int,
    db: Session = Depends(get_db)
):
    return delete_all_notifications(
        db,
        user_id
    )