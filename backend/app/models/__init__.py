"""
Base declarativa — todas las tablas heredan de esta.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base para modelos SQLAlchemy — metadata se registra en models/__init__."""

    pass
