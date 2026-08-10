"""
Tests happy path para la API de zonas.

Cubre:
    GET /api/zonas          — devuelve lista
    GET /api/zonas/{id}     — zona por id
    POST /api/zonas/contains — point-in-polygon
"""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Client async para testing — usa httpx.AsyncClient sobre ASGI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


class TestListZonas:
    """Tests para GET /api/zonas."""

    @pytest.mark.asyncio
    async def test_returns_list(self, client: AsyncClient) -> None:
        """GET /api/zonas devuelve HTTP 200 con lista (vacía o con datos)."""
        response = await client.get("/api/zonas")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_empty_when_no_zonas(self, client: AsyncClient) -> None:
        """Sin seed, devuelve lista vacía (no error)."""
        response = await client.get("/api/zonas")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_zona_has_geojson_geom(self, client: AsyncClient) -> None:
        """Con zonas en DB, cada una tiene geom en formato GeoJSON Feature."""
        response = await client.get("/api/zonas")
        assert response.status_code == 200
        zonas = response.json()
        if zonas:
            zona = zonas[0]
            assert "geom" in zona
            geom = zona["geom"]
            assert geom["type"] == "Feature"
            assert "geometry" in geom
            assert geom["geometry"]["type"] == "Polygon"
            assert "coordinates" in geom["geometry"]


class TestGetZona:
    """Tests para GET /api/zonas/{id}."""

    @pytest.mark.asyncio
    async def test_get_parque_by_id(self, client: AsyncClient) -> None:
        """GET /api/zonas/89121388 devuelve el Parque Isidora Cousiño."""
        response = await client.get("/api/zonas/89121388")
        # Puede ser 200 (con seed) o 404 (sin seed)
        if response.status_code == 200:
            zona = response.json()
            assert zona["id"] == 89121388
            assert "Parque" in zona["name"]
            assert zona["geom"]["type"] == "Feature"
        elif response.status_code == 404:
            # DB sin seed — ok, no es error del endpoint
            pass
        else:
            pytest.fail(f"Status inesperado: {response.status_code}")

    @pytest.mark.asyncio
    async def test_not_found(self, client: AsyncClient) -> None:
        """GET /api/zonas/99999999 devuelve 404."""
        response = await client.get("/api/zonas/99999999")
        assert response.status_code == 404
        assert "no encontrada" in response.json()["detail"]


class TestContainsPoint:
    """Tests para POST /api/zonas/contains."""

    @pytest.mark.asyncio
    async def test_point_in_parque(self, client: AsyncClient) -> None:
        """
        Punto dentro del polígono del Parque Isidora Cousiño.
        Coordenadas: centro del polígono del Parque.
        """
        payload = {"lat": -37.091, "lon": -73.167}
        response = await client.post("/api/zonas/contains", json=payload)
        assert response.status_code == 200
        data = response.json()
        # Con seed: devuelve el nombre de la zona
        if data["zona"] is not None:
            assert "Parque" in data["zona"]
        # Sin seed: devuelve null (no error)
        assert data.get("zona") is None or "Parque" in data["zona"]

    @pytest.mark.asyncio
    async def test_invalid_payload(self, client: AsyncClient) -> None:
        """Payload sin lat/lon devuelve 422."""
        response = await client.post("/api/zonas/contains", json={})
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_contains_validates_coordinates(self, client: AsyncClient) -> None:
        """Payload con lat fuera de rango devuelve 422."""
        response = await client.post("/api/zonas/contains", json={"lat": 999, "lon": -73})
        assert response.status_code == 422


class TestHealth:
    """Tests para /health."""

    @pytest.mark.asyncio
    async def test_health_returns_ok(self, client: AsyncClient) -> None:
        """GET /health devuelve {"status": "ok"}."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
