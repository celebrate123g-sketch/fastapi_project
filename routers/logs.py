
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from dependencies.auth import get_admin_user
from database.models import UserModel
from services.log_service import get_logs

router = APIRouter(
    tags=["Logs"]
)


@router.get("/logs")
def read_logs(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_admin_user)
):
    return get_logs(db)
