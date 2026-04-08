from sqlalchemy.orm import Session

from app.db.models import Setting


def get_settings_map(db: Session) -> dict[str, str]:
    return {item.key: item.value for item in db.query(Setting).order_by(Setting.key.asc()).all()}
