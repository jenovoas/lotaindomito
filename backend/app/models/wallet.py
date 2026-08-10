"""Modelo WalletTransaction — transacciones inmutables multi-moneda."""
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Enum, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class WalletTransaction(Base):
    """Transacción inmutable de una moneda del piloto.

    Los montos son enteros (BigInteger). Un monto positivo representa una
    ganancia (earn) y uno negativo un gasto (spend). Las transferencias
    generan dos filas: un gasto para el emisor y una ganancia para el
    receptor.

    Relación de cambio fija para el piloto:
        1 Sn (estanio) = 100 Au (oro) = 10.000 Cu (cobre)

    Attributes:
        id: UUID de la transacción.
        user_id: Identificador del usuario como string.
        currency: Moneda (cobre, oro, estanio).
        amount: Monto entero (positivo para earn, negativo para spend).
        tx_type: Tipo de transacción (earn, spend, transfer).
        counterparty_id: Usuario contraparte (opcional).
        reason: Motivo o descripción de la transacción.
        idempotency_key: Clave de idempotencia única.
        created_at: Fecha de creación del registro.
    """

    __tablename__ = "wallet_transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    currency: Mapped[str] = mapped_column(
        Enum("cobre", "oro", "estanio", name="currency_enum"),
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tx_type: Mapped[str] = mapped_column(
        Enum("earn", "spend", "transfer", name="tx_type_enum"),
        nullable=False,
    )
    counterparty_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reason: Mapped[str] = mapped_column(String(256), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=text("NOW()"))

    __table_args__ = (
        Index("ix_wallet_user_currency", "user_id", "currency"),
    )
