from pydantic import BaseModel


class SettingsResponse(BaseModel):
    values: dict[str, str]


class SettingsUpdateRequest(BaseModel):
    values: dict[str, str]
