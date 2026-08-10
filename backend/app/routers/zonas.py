"""
Router /api/zonas — CRUD + point-in-polygon.

Endpoints:
    GET  /api/zonas          — lista todas las zonas
    GET  /api/zonas/{id}     — zona por id
    POST /api/zonas/contains  — point-in-polygon (¿en qué zona está un punto?)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.zona import Zona
from app.schemas.zona import ContainsIn, ContainsOut, ZonaOut

router = APIRouter(prefix="/api/zonas", tags=["zonas"])


@router.get("", response_model=list[ZonaOut])
async def list_zonas(db: AsyncSession = Depends(get_db)) -> list[ZonaOut]:
    """
    Lista todas las zonas — GET /api/zonas.

    Returns:
        Lista de zonas con geometría GeoJSON.

    Raises:
        HTTP 500 si la DB no está disponible.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        result.release()
        result = await db.execute(text("SELECT COUNT(*) FROM zonas"))
        count = result.scalar() or 0
        if count == 0:
            return []

        stmt = text("SELECT id, name, tags, geom FROM zonas ORDER BY id")
        result = await db.execute(stmt)
        rows = result.fetchall()

        return [
            ZonaOut(
                id=row.id,
                name=row.name,
                tags=row.tags or {},
                geom=row.geom,
            )
            for row in rows
        ]
    except Exception:
        return []


@router.get("/{zona_id}", response_model=ZonaOut)
async def get_zona(zona_id: int, db: AsyncSession = Depends(get_db)) -> ZonaOut:
    """
    Obtiene una zona por id — GET /api/zonas/{id}.

    Returns:
        Zona con geometría GeoJSON.

    Raises:
        HTTP 404 si no existe.
    """
    try:
        stmt = text("SELECT id, name, tags, geom FROM zonas WHERE id = :id")
        result = await db.execute(stmt, {"id": zona_id})
        row = result.fetchone()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zona {zona_id} no encontrada",
        ) from None

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zona {zona_id} no encontrada",
        )

    return ZonaOut(
        id=row.id,
        name=row.name,
        tags=row.tags or {},
        geom=row.geom,
    )


@router.post("/contains", response_model=ContainsOut)
async def contains_point(
    payload: ContainsIn, db: AsyncSession = Depends(get_db)
) -> ContainsOut:
    """
    Point-in-polygon — POST /api/zonas/contains.

    Usa ST_Contains de PostGIS para determinar en qué zona cae un punto.

    Args:
        payload: {"lat": float, "lon": float}.

    Returns:
        {"zona": "Nombre de la zona"} o {"zona": null} si no hay zona.
    """
    query = text("""
        SELECT name
        FROM zonas
        WHERE ST_Contains(
            geom,
            ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)
        )
        LIMIT 1
    """)
    try:
        result = await db.execute(query, {"lat": payload.lat, "lon": payload.lon})
        row = result.fetchone()
    except Exception:
        return ContainsOut(zona=None)

    return ContainsOut(zona=row.name if row else None)
