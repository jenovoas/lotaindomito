"""Migración wallet — usuarios y transacciones multi-moneda.

Revision ID: 002
Revises: 001
Create Date: 2026-08-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tabla de usuarios/jugadores del piloto
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("nickname", sa.String(128), nullable=False),
        sa.Column("is_test", sa.Boolean(), nullable=False, server_default="true"),
    )

    # Tabla inmutable de transacciones multi-moneda
    op.create_table(
        "wallet_transactions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.String(64), nullable=False, index=True),
        sa.Column(
            "currency",
            sa.Enum("cobre", "oro", "estanio", name="currency_enum"),
            nullable=False,
        ),
        sa.Column("amount", sa.BigInteger(), nullable=False),
        sa.Column(
            "tx_type",
            sa.Enum("earn", "spend", "transfer", name="tx_type_enum"),
            nullable=False,
        ),
        sa.Column("counterparty_id", sa.String(64), nullable=True),
        sa.Column("reason", sa.String(256), nullable=False),
        sa.Column("idempotency_key", sa.String(128), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()")),
    )

    # Índice para consultas de saldo por usuario/moneda
    op.create_index(
        "ix_wallet_user_currency",
        "wallet_transactions",
        ["user_id", "currency"],
    )


def downgrade() -> None:
    op.drop_index("ix_wallet_user_currency", table_name="wallet_transactions")
    op.drop_table("wallet_transactions")
    op.execute("DROP TYPE IF EXISTS tx_type_enum")
    op.execute("DROP TYPE IF EXISTS currency_enum")
    op.drop_table("users")
