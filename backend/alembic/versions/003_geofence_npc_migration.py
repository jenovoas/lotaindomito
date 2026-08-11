"""Migración geofence + NPCs — tablas user_locations y npcs.

Revision ID: 003
Revises: 002
Create Date: 2026-08-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tabla de ubicaciones conocidas de los jugadores
    op.create_table(
        "user_locations",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("user_id", sa.String(64), nullable=False, index=True),
        sa.Column("zona_id", sa.Integer(), nullable=True),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
        ),
    )

    # Tabla de NPCs del piloto
    op.create_table(
        "npcs",
        sa.Column("id", sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("zona_id", sa.Integer(), nullable=False, index=True),
        sa.Column(
            "fsm_state",
            sa.Enum(
                "idle",
                "wander",
                "approach",
                "deliver",
                name="npc_state_enum",
            ),
            nullable=False,
            server_default="idle",
        ),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lon", sa.Float(), nullable=False),
        sa.Column("mission_id", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("active", sa.Boolean(), nullable=False, server_default="true"),
    )

    # NPC semilla del piloto: Isidora Goyenechea
    op.execute(
        sa.text(
            """
            INSERT INTO npcs (id, name, zona_id, fsm_state, lat, lon, mission_id, active)
            VALUES (:id, :name, :zona_id, :fsm_state, :lat, :lon, :mission_id, :active)
            """
        ).bindparams(
            id=1,
            name="Isidora Goyenechea",
            zona_id=89121388,
            fsm_state="idle",
            lat=-37.089,
            lon=-73.165,
            mission_id=1,
            active=True,
        )
    )


def downgrade() -> None:
    op.drop_table("npcs")
    op.drop_table("user_locations")
    op.execute("DROP TYPE IF EXISTS npc_state_enum")
