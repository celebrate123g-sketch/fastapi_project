from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.models import NotificationModel

from schemas.notification import NotificationCreate


def create_notification(
    db: Session,
    notification: NotificationCreate
):

    new_notification = NotificationModel(
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        notification_type=notification.notification_type
    )

    db.add(
        new_notification
    )

    db.commit()

    db.refresh(
        new_notification
    )

    return new_notification


def notify_user(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str
):

    notification = NotificationCreate(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type
    )

    return create_notification(
        db,
        notification
    )


def get_notifications(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 20
):

    return (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.user_id == user_id
        )
        .order_by(
            NotificationModel.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_recent_notifications(
    db: Session,
    user_id: int,
    limit: int = 10
):

    return (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.user_id == user_id
        )
        .order_by(
            NotificationModel.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def get_unread_notifications(
    db: Session,
    user_id: int
):

    return (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        )
        .order_by(
            NotificationModel.created_at.desc()
        )
        .all()
    )


def get_unread_count(
    db: Session,
    user_id: int
):

    return (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        )
        .count()
    )


def mark_as_read(
    db: Session,
    user_id: int,
    notification_id: int
):

    notification = (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == user_id
        )
        .first()
    )

    if notification is None:

        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    notification.is_read = True

    db.commit()

    db.refresh(
        notification
    )

    return notification


def mark_all_as_read(
    db: Session,
    user_id: int
):

    notifications = (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        )
        .all()
    )

    count = len(
        notifications
    )

    for notification in notifications:

        notification.is_read = True

    db.commit()

    return {
        "message": "All notifications marked as read.",
        "count": count
    }


def delete_notification(
    db: Session,
    user_id: int,
    notification_id: int
):

    notification = (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.id == notification_id,
            NotificationModel.user_id == user_id
        )
        .first()
    )

    if notification is None:

        raise HTTPException(
            status_code=404,
            detail="Notification not found."
        )

    db.delete(
        notification
    )

    db.commit()

    return {
        "message": "Notification deleted successfully."
    }


def delete_all_notifications(
    db: Session,
    user_id: int
):

    notifications = (
        db.query(
            NotificationModel
        )
        .filter(
            NotificationModel.user_id == user_id
        )
        .all()
    )

    count = len(
        notifications
    )

    for notification in notifications:

        db.delete(
            notification
        )

    db.commit()

    return {
        "message": "All notifications deleted successfully.",
        "count": count
    }