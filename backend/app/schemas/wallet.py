"""Schemas Pydantic para la wallet multi-moneda del piloto."""
from datetime import datetime
from typing import Literal
import uuid

from pydantic import BaseModel, ConfigDict, Field


class EarnRequest(BaseModel):
    """Solicitud para ganar una cantidad de una moneda."""

    user_id: str = Field(..., min_length=1, max_length=64)
    currency: Literal["cobre", "oro", "estanio"]
    amount: int = Field(..., gt=0)
    reason: str = Field(..., min_length=1, max_length=256)


class SpendRequest(BaseModel):
    """Solicitud para gastar una cantidad de una moneda."""

    user_id: str = Field(..., min_length=1, max_length=64)
    currency: Literal["cobre", "oro", "estanio"]
    amount: int = Field(..., gt=0)
    reason: str = Field(..., min_length=1, max_length=256)


class TransferRequest(BaseModel):
    """Solicitud para transferir una cantidad entre dos usuarios."""

    from_id: str = Field(..., min_length=1, max_length=64)
    to_id: str = Field(..., min_length=1, max_length=64)
    currency: Literal["cobre", "oro", "estanio"]
    amount: int = Field(..., gt=0)


class BalanceResponse(BaseModel):
    """Saldo actual desglosado por moneda."""

    model_config = ConfigDict(from_attributes=True)

    cobre: int = 0
    oro: int = 0
    estanio: int = 0


class TransactionResponse(BaseModel):
    """Representación de una transacción de wallet."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: str
    currency: str
    amount: int
    tx_type: str
    reason: str
    created_at: datetime
