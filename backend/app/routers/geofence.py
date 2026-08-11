"""Router /api/geofence — point-in-polygon y zonas GeoJSON."""
from typing import Any

from fastapi import APIRouter, Depends
from geoalchemy2.shape import to_shape
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.geofence import GeofenceCheckIn, GeofenceCheckOut

router = APIRouter(prefix="/api/geofence", tags=["geofence"])


@router.post("/check", response_model=GeofenceCheckOut)
async def check_geofence(
    payload: GeofenceCheckIn,
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> GeofenceCheckOut:
    """
    Verifica en qué zona cae un punto y si el usuario acaba de entrar.

    Usa ST_Contains de PostGIS. Si la DB no está disponible, devuelve
    zona nula y `entered=false` para no romper el cliente del piloto.
    """
    try:
        # Buscar la zona que contiene el punto
        result = await db.execute(
            text(
                """
                SELECT id, name
                FROM zonas
                WHERE ST_Contains(
                    geom,
                    ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
                )
                LIMIT 1
                """
            ),
            {"lat": payload.lat, "lon": payload.lon},
        )
        row = result.fetchone()
        current_zona_id = row.id if row else None
        current_zona_name = row.name if row else None

        # Última zona conocida del usuario
        last_result = await db.execute(
            text(
                """
                SELECT zona_id
                FROM user_locations
                WHERE user_id = :user_id
                ORDER BY updated_at DESC
                LIMIT 1
                """
            ),
            {"user_id": payload.user_id},
        )
        last_row = last_result.fetchone()
        last_zona_id = last_row.zona_id if last_row else None

        # Registrar ubicación actual
        await db.execute(
            text(
                """
                INSERT INTO user_locations (user_id, zona_id, lat, lon)
                VALUES (:user_id, :zona_id, :lat, :lon)
                """
            ),
            {
                "user_id": payload.user_id,
                "zona_id": current_zona_id,
                "lat": payload.lat,
                "lon": payload.lon,
            },
        )

        entered = (
            current_zona_id is not None
            and current_zona_id != last_zona_id
        )

        return GeofenceCheckOut(
            zona_id=current_zona_id,
            zona_name=current_zona_name,
            entered=entered,
        )
    except Exception:  # noqa: BLE001
        return GeofenceCheckOut(zona_id=None, zona_name=None, entered=False)


@router.get("/zonas")
async def list_zonas_geojson(
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> dict[str, Any]:
    """
    Devuelve todas las zonas como GeoJSON FeatureCollection.

    Si la DB no está disponible, retorna una colección vacía.
    """
    try:
        result = await db.execute(
            text("SELECT id, name, tags, geom FROM zonas ORDER BY id")
        )
        rows = result.fetchall()
    except Exception:  # noqa: BLE001
        return {"type": "FeatureCollection", "features": []}

    features: list[dict[str, Any]] = []
    for row in rows:
        if row.geom is None:
            continue
        shape = to_shape(row.geom)
        features.append(
            {
                "type": "Feature",
                "geometry": shape.__geo_interface__,
                "properties": {
                    "id": row.id,
                    "name": row.name,
                    "tags": row.tags or {},
                },
            }
        )

    return {"type": "FeatureCollection", "features": features}
