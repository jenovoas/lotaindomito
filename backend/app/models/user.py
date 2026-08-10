"""Modelo User — jugador del piloto."""
import uuid

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class User(Base):
    """Usuario/jugador registrado en el piloto.

    Attributes:
        id: Identificador único (UUID).
        nickname: Apodo o nombre visible del jugador.
        is_test: Bandera para distinguir usuarios de prueba.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nickname: Mapped[str] = mapped_column(String(128), nullable=False)
    is_test: Mapped[bool] = mapped_column(Boolean, default=True)
