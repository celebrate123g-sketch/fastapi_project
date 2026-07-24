from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models import (
    QuoteModel,
    ReportModel
)

from schemas.report import (
    ReportCreate,
    ReportStatus
)


def create_report(
    db: Session,
    data: ReportCreate
):

    quote = (
        db.query(QuoteModel)
        .filter(
            QuoteModel.id == data.quote_id
        )
        .first()
    )

    if quote is None:
        return None

    report = ReportModel(
        quote_id=data.quote_id,
        user_id=data.user_id,
        reason=data.reason.value,
        description=data.description,
        status=ReportStatus.pending.value
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def get_report(
    db: Session,
    report_id: int
):

    return (
        db.query(ReportModel)
        .filter(
            ReportModel.id == report_id
        )
        .first()
    )


def get_all_reports(
    db: Session
):

    return (
        db.query(ReportModel)
        .order_by(
            ReportModel.created_at.desc()
        )
        .all()
    )


def get_reports_by_quote(
    db: Session,
    quote_id: int
):

    return (
        db.query(ReportModel)
        .filter(
            ReportModel.quote_id == quote_id
        )
        .order_by(
            ReportModel.created_at.desc()
        )
        .all()
    )


def get_reports_by_user(
    db: Session,
    user_id: int
):

    return (
        db.query(ReportModel)
        .filter(
            ReportModel.user_id == user_id
        )
        .order_by(
            ReportModel.created_at.desc()
        )
        .all()
    )


def approve_report(
    db: Session,
    report_id: int
):

    report = get_report(
        db,
        report_id
    )

    if report is None:
        return None

    report.status = ReportStatus.approved.value

    db.commit()
    db.refresh(report)

    return report


def reject_report(
    db: Session,
    report_id: int
):

    report = get_report(
        db,
        report_id
    )

    if report is None:
        return None

    report.status = ReportStatus.rejected.value

    db.commit()
    db.refresh(report)

    return report


def delete_report(
    db: Session,
    report_id: int
):

    report = get_report(
        db,
        report_id
    )

    if report is None:
        return False

    db.delete(report)
    db.commit()

    return True


def get_report_statistics(
    db: Session
):

    total_reports = (
        db.query(
            func.count(
                ReportModel.id
            )
        )
        .scalar()
    )

    pending = (
        db.query(
            func.count(
                ReportModel.id
            )
        )
        .filter(
            ReportModel.status == ReportStatus.pending.value
        )
        .scalar()
    )

    approved = (
        db.query(
            func.count(
                ReportModel.id
            )
        )
        .filter(
            ReportModel.status == ReportStatus.approved.value
        )
        .scalar()
    )

    rejected = (
        db.query(
            func.count(
                ReportModel.id
            )
        )
        .filter(
            ReportModel.status == ReportStatus.rejected.value
        )
        .scalar()
    )

    return {
        "total_reports": total_reports,
        "pending": pending,
        "approved": approved,
        "rejected": rejected
    }