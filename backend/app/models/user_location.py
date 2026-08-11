"""Modelo UserLocation — tracking de última zona conocida del jugador."""
from datetime import datetime

from sqlalchemy import Float, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class UserLocation(Base):
    __tablename__ = "user_locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    zona_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    lon: Mapped[float] = mapped_column(Float, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))
