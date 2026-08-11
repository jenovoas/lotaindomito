"""Schemas Pydantic para la API de geofence."""
from pydantic import BaseModel, ConfigDict, Field


class GeofenceCheckIn(BaseModel):
    """Request para POST /api/geofence/check."""

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    user_id: str


class GeofenceCheckOut(BaseModel):
    """Response para POST /api/geofence/check."""

    model_config = ConfigDict(from_attributes=True)

    zona_id: int | None = None
    zona_name: str | None = None
    entered: bool = False
