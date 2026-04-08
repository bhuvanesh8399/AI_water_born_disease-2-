from pydantic import BaseModel


class HeatPoint(BaseModel):
    district_code: str
    district_name: str
    latitude: float
    longitude: float
    risk_score: float
    risk_level: str
    confidence_score: float


class HeatmapResponse(BaseModel):
    items: list[HeatPoint]
