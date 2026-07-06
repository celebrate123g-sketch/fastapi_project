from sqlalchemy.orm import Session

from database.models import LogModel


def create_log(
    db: Session,
    action: str,
    quote_id: int | None = None
):
    log = LogModel(
        action=action,
        quote_id=quote_id
    )

    db.add(log)
    db.commit()


def get_logs(
    db: Session
):
    return (
        db.query(LogModel)
        .order_by(LogModel.created_at.desc())
        .all()
    )