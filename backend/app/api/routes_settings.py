from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.core.security import require_write_access
from app.db.models import Setting
from app.db.session import get_db

router = APIRouter()


@router.get("/settings")
def read_settings(db: Session = Depends(get_db)):
    values = {item.key: item.value for item in db.query(Setting).order_by(Setting.key.asc()).all()}
    return {"values": values}


@router.put("/settings")
def update_settings(
    payload: dict = Body(default={}),
    _: dict = Depends(require_write_access),
    db: Session = Depends(get_db),
):
    updated: dict[str, str] = {}
    for key, value in payload.items():
        item = db.query(Setting).filter(Setting.key == str(key)).first()
        if item is None:
            item = Setting(key=str(key), value=str(value))
            db.add(item)
        else:
            item.value = str(value)
        updated[str(key)] = str(value)
    db.commit()
    return {"detail": "Settings updated", "values": updated}
