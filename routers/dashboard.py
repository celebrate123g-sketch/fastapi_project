
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth import get_admin_user

from schemas.dashboard import DashboardResponse

from services.dashboard_service import (
    get_dashboard
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "",
    response_model=DashboardResponse
)
def dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(get_admin_user)
):
    return get_dashboard(
        db
    )
