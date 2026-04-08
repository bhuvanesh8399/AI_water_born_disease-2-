import csv
import io

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.models import Alert
from app.db.session import get_db

router = APIRouter()


def _alerts_csv_bytes(db: Session) -> bytes:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "id",
            "district_id",
            "district_name",
            "title",
            "score",
            "severity",
            "status",
            "snapshot_date",
            "created_at",
            "updated_at",
        ]
    )
    alerts = db.query(Alert).order_by(Alert.score.desc(), Alert.created_at.desc()).all()
    for item in alerts:
        writer.writerow(
            [
                item.id,
                item.district_id,
                item.district.district_name,
                item.title,
                item.score,
                item.severity,
                item.status,
                item.snapshot_date.isoformat(),
                item.created_at.isoformat(),
                item.updated_at.isoformat(),
            ]
        )
    return output.getvalue().encode("utf-8")


@router.get("/reports/alerts.csv")
def report_alerts_csv(db: Session = Depends(get_db)):
    data = _alerts_csv_bytes(db)
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=alerts-report.csv"},
    )


@router.get("/reports/alerts.pdf")
def report_alerts_pdf(db: Session = Depends(get_db)):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="PDF report generation is not implemented yet; use /api/reports/alerts.csv for now.",
    )
