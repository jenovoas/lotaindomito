"""Migración inicial — PostGIS + tabla zonas.

Revision ID: 001
Revises:
Create Date: 2026-08-10

"""
from typing import Sequence, Union

from alembic import op
import geoalchemy2
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Habilitar extensión PostGIS en la DB
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Crear tabla zonas
    op.create_table(
        "zonas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column(
            "tags",
            sa.JSON().with_variant(sa.JSON(), "postgresql"),
            nullable=False,
            server_default="{}",
        ),
        # Geometría PostGIS — Polygon SRID 4326 (WGS84)
        sa.Column(
            "geom",
            geoalchemy2.Geometry(
                geometry_type="Polygon",
                srid=4326,
                spatial_index=True,
            ),
            nullable=False,
        ),
    )

    # Comentario en tabla
    op.execute("COMMENT ON TABLE zonas IS 'Zonas geográficas de Lota — OSM polygons'")


def downgrade() -> None:
    op.drop_table("zonas")
    op.execute("DROP EXTENSION IF EXISTS postgis")
