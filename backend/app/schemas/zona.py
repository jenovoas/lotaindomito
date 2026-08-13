"""
Schemas Pydantic para la API de zonas.

Usa Pydantic v2 con @field_serializer para convertir WKB → GeoJSON.
"""
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from geoalchemy2.shape import to_shape
from geoalchemy2.elements import WKBElement


class ZonaIn(BaseModel):
    """Input — no se usa en este piloto (el seed viene del JSON)."""

    pass


class ZonaOut(BaseModel):
    """
    Output — zona con geometría en GeoJSON.

    El campo `geom` se serializa de WKB a GeoJSON Feature.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    tags: dict[str, Any]
    geom: bytes  # raw WKB del modelo

    @field_serializer("geom")
    def serialize_geom(self, geom: bytes) -> dict[str, Any]:
        if isinstance(geom, WKBElement):
            shape = to_shape(geom)
        else:
            shape = to_shape(WKBElement(geom))
        return {
            "type": "Feature",
            "geometry": shape.__geo_interface__,
            "properties": {},
        }


class ContainsIn(BaseModel):
    """Request para POST /api/zonas/contains."""

    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)


class ContainsOut(BaseModel):
    """Response para POST /api/zonas/contains."""

    zona: str | None = None
