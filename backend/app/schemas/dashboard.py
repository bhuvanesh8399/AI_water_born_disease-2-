from pydantic import BaseModel


class KpiItem(BaseModel):
    label: str
    value: str
    trend: str


class DashboardAlertItem(BaseModel):
    id: int
    title: str
    severity: str
    status: str
    district_code: str
    created_at: str


class DashboardSummaryResponse(BaseModel):
    generated_at: str
    kpis: list[KpiItem]
    top_hotspots: list[dict]
    recent_alerts: list[DashboardAlertItem]
    decision_summary: str
    contributing_factors: list[str]
