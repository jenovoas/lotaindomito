"""
Base declarativa — todas las tablas heredan de esta.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base para modelos SQLAlchemy — metadata se registra en models/__init__."""

    pass


# Importar modelos para que Alembic los detecte en autogenerate
from app.models.zona import Zona  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.wallet import WalletTransaction  # noqa: E402
from app.models.user_location import UserLocation  # noqa: E402
from app.models.npc import NPC  # noqa: E402
