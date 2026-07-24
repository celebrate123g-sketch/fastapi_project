from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.report import (
    ReportCreate,
    ReportResponse,
    ReportStats
)

from services.report_service import (
    create_report,
    get_report,
    get_all_reports,
    get_reports_by_quote,
    get_reports_by_user,
    approve_report,
    reject_report,
    delete_report,
    get_report_statistics
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post(
    "",
    response_model=ReportResponse
)
def report(
    data: ReportCreate,
    db: Session = Depends(get_db)
):

    result = create_report(
        db,
        data
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Quote not found."
        )

    return result


@router.get(
    "",
    response_model=list[ReportResponse]
)
def reports(
    db: Session = Depends(get_db)
):

    return get_all_reports(db)


@router.get(
    "/statistics",
    response_model=ReportStats
)
def statistics(
    db: Session = Depends(get_db)
):

    return get_report_statistics(db)


@router.get(
    "/{report_id}",
    response_model=ReportResponse
)
def report_by_id(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = get_report(
        db,
        report_id
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return report


@router.get(
    "/quote/{quote_id}",
    response_model=list[ReportResponse]
)
def reports_by_quote(
    quote_id: int,
    db: Session = Depends(get_db)
):

    return get_reports_by_quote(
        db,
        quote_id
    )


@router.get(
    "/user/{user_id}",
    response_model=list[ReportResponse]
)
def reports_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return get_reports_by_user(
        db,
        user_id
    )


@router.put(
    "/{report_id}/approve",
    response_model=ReportResponse
)
def approve(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = approve_report(
        db,
        report_id
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return report


@router.put(
    "/{report_id}/reject",
    response_model=ReportResponse
)
def reject(
    report_id: int,
    db: Session = Depends(get_db)
):

    report = reject_report(
        db,
        report_id
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return report


@router.delete(
    "/{report_id}"
)
def delete(
    report_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_report(
        db,
        report_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Report not found."
        )

    return {
        "message": "Report deleted successfully."
    }