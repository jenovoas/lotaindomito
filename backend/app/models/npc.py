"""Modelo NPC — personaje no jugable del piloto."""
from sqlalchemy import Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class NPC(Base):
    __tablename__ = "npcs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    zona_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    fsm_state: Mapped[str] = mapped_column(
        Enum("idle", "wander", "approach", "deliver", name="npc_state_enum"),
        nullable=False,
        default="idle",
    )
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    mission_id: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
