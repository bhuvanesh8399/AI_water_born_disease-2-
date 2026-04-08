from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_write_access
from app.db.session import get_db
from app.services.ingest_service import reload_dataset

router = APIRouter()


@router.post("/ingest/reload")
def reload_ingest(
    db: Session = Depends(get_db),
    _: dict = Depends(require_write_access),
):
    return reload_dataset(db)
