from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    district_id: int
    title: str
    message: str
    severity: str
    status: str
    source: str
    created_at: datetime
    updated_at: datetime


class AlertListResponse(BaseModel):
    items: list[AlertOut]
    total: int


class AlertUpdateRequest(BaseModel):
    status: str
