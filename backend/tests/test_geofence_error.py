"""Tests failure path para la API de geofence y NPCs."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Client async para testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestGeofenceValidationErrors:
    """Errores de validación en /api/geofence/check."""

    @pytest.mark.asyncio
    async def test_check_missing_lat(self, client: AsyncClient) -> None:
        """Falta lat → 422."""
        response = await client.post(
            "/api/geofence/check",
            json={"lon": -73.165, "user_id": "user-1"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_check_missing_lon(self, client: AsyncClient) -> None:
        """Falta lon → 422."""
        response = await client.post(
            "/api/geofence/check",
            json={"lat": -37.089, "user_id": "user-1"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_check_invalid_lat_range(self, client: AsyncClient) -> None:
        """lat fuera de rango → 422."""
        response = await client.post(
            "/api/geofence/check",
            json={"lat": 999, "lon": -73.165, "user_id": "user-1"},
        )
        assert response.status_code == 422


class TestNpcsErrors:
    """Errores en /api/npcs."""

    @pytest.mark.asyncio
    async def test_npcs_empty_for_unknown_zone(self, client: AsyncClient) -> None:
        """GET /api/npcs?zona_id=999 debe devolver lista vacía."""
        response = await client.get("/api/npcs?zona_id=999")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_npcs_interact_not_found(self, client: AsyncClient) -> None:
        """POST con npc_id inexistente → 404 (o 503 sin DB)."""
        response = await client.post(
            "/api/npcs/interact",
            json={"npc_id": 999, "user_id": "user-1", "action": "approach"},
        )
        assert response.status_code in (404, 503)

    @pytest.mark.asyncio
    async def test_npcs_interact_invalid_action(self, client: AsyncClient) -> None:
        """POST con acción inválida → 400 (o 503 sin DB)."""
        response = await client.post(
            "/api/npcs/interact",
            json={"npc_id": 1, "user_id": "user-1", "action": "invalid"},
        )
        assert response.status_code in (400, 503)
