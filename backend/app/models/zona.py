"""
Modelo Zona — polígono PostGIS con GeoAlchemy2.

El campo `geom` se almacena como WKB en PostGIS (SRID 4326 = WGS84).
Se usa Geometry(geometry_type='Polygon', srid=4326, spatial_index=True)
para que Alembic genere la columna correctamente y para queries ST_Contains.
"""
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base

# GeoAlchemy2 — Geometry type para PostGIS
from geoalchemy2 import Geometry


class Zona(Base):
    """
    Zona geográfica — parque, plaza, museo, ruina de Lota.

    Attributes:
        id: OSM id (PK) — viene de zonas-lota.json.
        name: Nombre legible.
        tags: Tags OSM como dict (ej: {"leisure": "park"}).
        geom: Polígono en WGS84 (SRID 4326).
    """

    __tablename__ = "zonas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    tags: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # PostGIS Polygon, SRID 4326 (WGS84)
    geom: Mapped[bytes] = mapped_column(
        Geometry(geometry_type="Polygon", srid=4326, spatial_index=True),
        nullable=False,
    )
