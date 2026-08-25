import pytest
import time
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.fixture
async def client() -> AsyncClient:
    """Client async para testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_events_perf(client: AsyncClient) -> None:
    events = [
        {
            "event": f"test_event_{i}",
            "payload": {"user_id": f"test_user_{i}"}
        }
        for i in range(100)
    ]

    start = time.time()
    response = await client.post("/api/events", json={"events": events})
    end = time.time()

    assert response.status_code == 200
    print(f"Time taken to ingest 100 events: {end - start:.4f} seconds")
