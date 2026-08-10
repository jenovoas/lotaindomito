"""Tests happy path para la API de wallet.

Cubre:
    GET /api/wallet/{user_id}  — saldo vacío
    POST /api/wallet/earn     — validaciones de request
    POST /api/wallet/spend    — validaciones de request
    POST /api/wallet/transfer — validaciones de request
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


class TestGetBalance:
    """Tests para GET /api/wallet/{user_id}."""

    @pytest.mark.asyncio
    async def test_get_balance_empty(self, client: AsyncClient) -> None:
        """Un usuario sin transacciones debe tener saldo cero."""
        response = await client.get("/api/wallet/test-1")
        # Sin DB puede devolver 503; con DB debe devolver 200 y saldos en cero
        assert response.status_code in (200, 503)
        if response.status_code == 200:
            data = response.json()
            assert data == {"cobre": 0, "oro": 0, "estanio": 0}


class TestEarnValidation:
    """Tests de validación para POST /api/wallet/earn."""

    @pytest.mark.asyncio
    async def test_earn_validation(self, client: AsyncClient) -> None:
        """amount=0 debe devolver 422."""
        payload = {
            "user_id": "test-1",
            "currency": "cobre",
            "amount": 0,
            "reason": "recompensa piloto",
        }
        response = await client.post("/api/wallet/earn", json=payload)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_earn_with_negative_amount(self, client: AsyncClient) -> None:
        """amount negativo debe devolver 422."""
        payload = {
            "user_id": "test-1",
            "currency": "cobre",
            "amount": -5,
            "reason": "recompensa piloto",
        }
        response = await client.post("/api/wallet/earn", json=payload)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_earn_invalid_currency(self, client: AsyncClient) -> None:
        """currency inválida debe devolver 422."""
        payload = {
            "user_id": "test-1",
            "currency": "plata",
            "amount": 100,
            "reason": "recompensa piloto",
        }
        response = await client.post("/api/wallet/earn", json=payload)
        assert response.status_code == 422


class TestSpendValidation:
    """Tests de validación para POST /api/wallet/spend."""

    @pytest.mark.asyncio
    async def test_spend_validation(self, client: AsyncClient) -> None:
        """Falta user_id debe devolver 422."""
        payload = {
            "currency": "oro",
            "amount": 10,
            "reason": "compra piloto",
        }
        response = await client.post("/api/wallet/spend", json=payload)
        assert response.status_code == 422


class TestTransferValidation:
    """Tests de validación para POST /api/wallet/transfer."""

    @pytest.mark.asyncio
    async def test_transfer_validation(self, client: AsyncClient) -> None:
        """Falta to_id debe devolver 422."""
        payload = {
            "from_id": "test-1",
            "currency": "estanio",
            "amount": 1,
        }
        response = await client.post("/api/wallet/transfer", json=payload)
        assert response.status_code == 422
