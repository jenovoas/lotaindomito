#!/usr/bin/env python3
"""
Seed script — carga las 11 zonas desde zonas-lota.json a PostGIS.

Uso:
    cd backend
    python seed.py

Requiere:
    DATABASE_URL apuntando a una DB con PostGIS.
    Tabla `zonas` ya creada (alembic upgrade head).
"""
import json
import sys
from pathlib import Path

import shapely.geometry
from shapely.geometry import Polygon

# Asegurar que app está en el path
sys.path.insert(0, str(Path(__file__).parent))

from geoalchemy2.shape import to_shape
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_context

ZONAS_JSON = Path(__file__).parent.parent / "piloto-a" / "src" / "data" / "zonas-lota.json"


def coords_to_polygon(coords: list[dict]) -> Polygon:
    """
    Convierte lista de {lat, lon} a Shapely Polygon.

    PostGIS espera (lon, lat) en SRID 4326.
    El JSON tiene {lat, lon} — reordenamos.
    """
    ring = [(c["lon"], c["lat"]) for c in coords]
    return Polygon(ring)


def polygon_to_wkb(polygon: Polygon) -> bytes:
    """Shapely Polygon → WKB bytes (little-endian, sin SRID)."""
    return polygon.wkb


def load_zonas() -> list[dict]:
    """Carga las zonas desde zonas-lota.json."""
    if not ZONAS_JSON.exists():
        raise FileNotFoundError(
            f"No se encontró {ZONAS_JSON}. "
            "Ejecutar desde backend/ o verificar ruta."
        )
    with open(ZONAS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return data["zonas"]


async def seed() -> None:
    """Inserta las 11 zonas en la tabla zonas."""
    zonas = load_zonas()
    print(f"[seed] Cargando {len(zonas)} zonas desde {ZONAS_JSON}")

    async with get_db_context() as db:
        # Verificar que la tabla existe
        result = await db.execute(text("SELECT COUNT(*) FROM zonas"))
        count = result.scalar() or 0
        print(f"[seed] Zonas en DB: {count}")

        if count > 0:
            print("[seed] DB ya tiene zonas — omitiendo seed (usar truncate si se quiere re-seed).")
            return

        # Insertar cada zona
        inserted = 0
        for zona in zonas:
            polygon = coords_to_polygon(zona["coords"])
            wkb = polygon_to_wkb(polygon)

            await db.execute(
                text("""
                    INSERT INTO zonas (id, name, tags, geom)
                    VALUES (:id, :name, :tags, ST_GeomFromWKB(:geom, 4326))
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        tags = EXCLUDED.tags,
                        geom = EXCLUDED.geom
                """),
                {
                    "id": zona["id"],
                    "name": zona["name"],
                    "tags": zona["tags"],
                    "geom": wkb,
                },
            )
            inserted += 1
            print(f"  ✓ {zona['id']}: {zona['name']}")

        print(f"[seed] ✓ {inserted} zonas insertadas.")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(seed())
    except Exception as exc:
        print(f"[seed] ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
