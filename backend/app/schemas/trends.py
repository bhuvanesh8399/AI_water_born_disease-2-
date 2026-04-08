from pydantic import BaseModel


class TrendPoint(BaseModel):
    date: str
    risk_score: float
    risk_level: str
    confidence_score: float


class TrendsResponse(BaseModel):
    district_code: str
    district_name: str
    points: list[TrendPoint]
    summary: str
