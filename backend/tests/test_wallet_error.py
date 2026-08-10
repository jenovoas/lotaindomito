"""Tests failure path para la API de wallet.

Cubre:
    - Gasto sin saldo suficiente → HTTP 422
    - Transferencia a usuario inexistente → HTTP 404
    - Montos negativos → HTTP 422
    - Monedas inválidas → HTTP 422
"""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Client async para testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestSpendInsufficientBalance:
    """Tests para gastos sin saldo suficiente."""

    @pytest.mark.asyncio
    async def test_spend_insufficient_balance(self, client: AsyncClient) -> None:
        """Gastar más de lo disponible devuelve 422 (o 503 si la DB no está)."""
        payload = {
            "user_id": "test-1",
            "currency": "cobre",
            "amount": 999999999,
            "reason": "gasto imposible",
        }
        response = await client.post("/api/wallet/spend", json=payload)
        assert response.status_code in (422, 503)
        if response.status_code == 422:
            assert "Saldo insuficiente" in response.json()["detail"]


class TestTransferToNonexistentUser:
    """Tests para transferencias a usuarios inexistentes."""

    @pytest.mark.asyncio
    async def test_transfer_to_nonexistent_user(self, client: AsyncClient) -> None:
        """Transferir a un usuario inexistente devuelve 404 (o 503 si la DB no está)."""
        payload = {
            "from_id": "test-1",
            "to_id": "no-existe-123",
            "currency": "oro",
            "amount": 10,
        }
        response = await client.post("/api/wallet/transfer", json=payload)
        assert response.status_code in (404, 503)
        if response.status_code == 404:
            assert "Usuario no encontrado" in response.json()["detail"]


class TestNegativeAmount:
    """Tests para montos negativos."""

    @pytest.mark.asyncio
    async def test_earn_with_negative_amount(self, client: AsyncClient) -> None:
        """amount negativo en earn devuelve 422."""
        payload = {
            "user_id": "test-1",
            "currency": "cobre",
            "amount": -5,
            "reason": "recompensa",
        }
        response = await client.post("/api/wallet/earn", json=payload)
        assert response.status_code == 422


class TestInvalidCurrency:
    """Tests para monedas inválidas."""

    @pytest.mark.asyncio
    async def test_invalid_currency(self, client: AsyncClient) -> None:
        """currency no válida devuelve 422."""
        payload = {
            "user_id": "test-1",
            "currency": "dolar",
            "amount": 100,
            "reason": "recompensa",
        }
        response = await client.post("/api/wallet/earn", json=payload)
        assert response.status_code == 422
