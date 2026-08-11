"""Tests happy path para la API de geofence y NPCs."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Client async para testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestGeofenceCheck:
    """Tests para POST /api/geofence/check."""

    @pytest.mark.asyncio
    async def test_check_returns_null_when_no_db(self, client: AsyncClient) -> None:
        """Sin DB debe responder graceful con zona nula y entered=false."""
        payload = {"lat": -37.089, "lon": -73.165, "user_id": "user-1"}
        response = await client.post("/api/geofence/check", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["zona_id"] is None
        assert data["zona_name"] is None
        assert data["entered"] is False

    @pytest.mark.asyncio
    async def test_geofence_validation(self, client: AsyncClient) -> None:
        """POST sin lat debe devolver 422."""
        response = await client.post(
            "/api/geofence/check",
            json={"lon": -73.165, "user_id": "user-1"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_geofence_lon_required(self, client: AsyncClient) -> None:
        """POST sin lon debe devolver 422."""
        response = await client.post(
            "/api/geofence/check",
            json={"lat": -37.089, "user_id": "user-1"},
        )
        assert response.status_code == 422


class TestGeofenceZonas:
    """Tests para GET /api/geofence/zonas."""

    @pytest.mark.asyncio
    async def test_get_zonas_geojson(self, client: AsyncClient) -> None:
        """GET /api/geofence/zonas debe devolver FeatureCollection."""
        response = await client.get("/api/geofence/zonas")
        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "FeatureCollection"
        assert "features" in data
        assert isinstance(data["features"], list)
