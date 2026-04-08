import csv
from io import BytesIO, StringIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session

from app.db.models import Alert, District


def alerts_csv_report(db: Session) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "district_code", "title", "severity", "status", "created_at"])

    alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()
    for alert in alerts:
        district = db.get(District, alert.district_id)
        writer.writerow([
            alert.id,
            district.code,
            alert.title,
            alert.severity,
            alert.status,
            alert.created_at.isoformat(),
        ])

    return output.getvalue()


def alerts_pdf_report(db: Session) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("Alerts Report")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "AI-Based Early Warning System — Alerts Report")
    pdf.setFont("Helvetica", 10)

    y = 770
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(25).all()
    for alert in alerts:
        district = db.get(District, alert.district_id)
        line = f"#{alert.id} | {district.code} | {alert.title} | {alert.severity.upper()} | {alert.status}"
        pdf.drawString(50, y, line[:100])
        y -= 18
        if y < 60:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = 800

    pdf.save()
    return buffer.getvalue()
