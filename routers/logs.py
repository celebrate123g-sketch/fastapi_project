from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from services.log_service import get_logs

router = APIRouter(
    tags=["Logs"]
)


@router.get("/logs")
def read_logs(
    db: Session = Depends(get_db)
):
    return get_logs(db)