"""Router /api/wallet — wallet multi-moneda del piloto.

Endpoints:
    GET  /api/wallet/{user_id}  — consulta de saldos
    POST /api/wallet/earn      — ganar moneda
    POST /api/wallet/spend     — gastar moneda
    POST /api/wallet/transfer  — transferir moneda entre usuarios
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.user import User
from app.models.wallet import WalletTransaction
from app.schemas.wallet import (
    BalanceResponse,
    EarnRequest,
    SpendRequest,
    TransferRequest,
)

router = APIRouter(prefix="/api/wallet", tags=["wallet"])

# Relación de cambio fija (informativa para el piloto):
# 1 Sn (estanio) = 100 Au (oro) = 10.000 Cu (cobre)


async def _user_exists(db: AsyncSession, user_id: str) -> bool:
    """Verifica si un usuario existe buscando por UUID o nickname."""
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        user_uuid = None

    if user_uuid is not None:
        condition = or_(User.id == user_uuid, User.nickname == user_id)
    else:
        condition = User.nickname == user_id

    result = await db.execute(select(User).where(condition))
    return result.scalar_one_or_none() is not None


async def _get_balance(
    db: AsyncSession,
    user_id: str,
) -> BalanceResponse:
    """Calcula el saldo agrupado por moneda para un usuario."""
    result = await db.execute(
        select(
            WalletTransaction.currency,
            func.coalesce(func.sum(WalletTransaction.amount), 0),
        )
        .where(WalletTransaction.user_id == user_id)
        .group_by(WalletTransaction.currency)
    )
    rows = result.all()
    balances = {currency: int(total) for currency, total in rows}
    return BalanceResponse(
        cobre=balances.get("cobre", 0),
        oro=balances.get("oro", 0),
        estanio=balances.get("estanio", 0),
    )


@router.get("/{user_id}", response_model=BalanceResponse)
async def get_balance(
    user_id: str,
    db: AsyncSession = Depends(get_db),
) -> BalanceResponse:
    """Devuelve el saldo de un usuario agrupado por moneda.

    Si la base de datos no está disponible, retorna saldos en cero para
    no romper el cliente durante el piloto.
    """
    try:
        return await _get_balance(db, user_id)
    except Exception:
        return BalanceResponse()


@router.post("/earn", response_model=BalanceResponse)
async def earn(
    payload: EarnRequest,
    db: AsyncSession = Depends(get_db),
) -> BalanceResponse:
    """Registra una ganancia de moneda para un usuario."""
    try:
        tx = WalletTransaction(
            user_id=payload.user_id,
            currency=payload.currency,
            amount=payload.amount,
            tx_type="earn",
            reason=payload.reason,
            idempotency_key=str(uuid.uuid4()),
        )
        db.add(tx)
        await db.flush()
        return await _get_balance(db, payload.user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available",
        ) from None


@router.post("/spend", response_model=BalanceResponse)
async def spend(
    payload: SpendRequest,
    db: AsyncSession = Depends(get_db),
) -> BalanceResponse:
    """Registra un gasto de moneda para un usuario si tiene saldo suficiente."""
    try:
        balance_result = await db.execute(
            select(func.coalesce(func.sum(WalletTransaction.amount), 0)).where(
                WalletTransaction.user_id == payload.user_id,
                WalletTransaction.currency == payload.currency,
            )
        )
        balance = int(balance_result.scalar_one() or 0)
        if balance < payload.amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Saldo insuficiente",
            )

        tx = WalletTransaction(
            user_id=payload.user_id,
            currency=payload.currency,
            amount=-payload.amount,
            tx_type="spend",
            reason=payload.reason,
            idempotency_key=str(uuid.uuid4()),
        )
        db.add(tx)
        await db.flush()
        return await _get_balance(db, payload.user_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available",
        ) from None


@router.post("/transfer", response_model=BalanceResponse)
async def transfer(
    payload: TransferRequest,
    db: AsyncSession = Depends(get_db),
) -> BalanceResponse:
    """Transfiere moneda de un usuario a otro de forma atómica."""
    try:
        # Verificar saldo del emisor
        balance_result = await db.execute(
            select(func.coalesce(func.sum(WalletTransaction.amount), 0)).where(
                WalletTransaction.user_id == payload.from_id,
                WalletTransaction.currency == payload.currency,
            )
        )
        balance = int(balance_result.scalar_one() or 0)
        if balance < payload.amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Saldo insuficiente",
            )

        # Verificar que el receptor existe
        if not await _user_exists(db, payload.to_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado",
            )

        spend_tx = WalletTransaction(
            user_id=payload.from_id,
            currency=payload.currency,
            amount=-payload.amount,
            tx_type="transfer",
            counterparty_id=payload.to_id,
            reason=f"Transferencia a {payload.to_id}",
            idempotency_key=str(uuid.uuid4()),
        )
        earn_tx = WalletTransaction(
            user_id=payload.to_id,
            currency=payload.currency,
            amount=payload.amount,
            tx_type="transfer",
            counterparty_id=payload.from_id,
            reason=f"Transferencia desde {payload.from_id}",
            idempotency_key=str(uuid.uuid4()),
        )
        db.add(spend_tx)
        db.add(earn_tx)
        await db.flush()
        return await _get_balance(db, payload.from_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available",
        ) from None
