import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ingest_events_payload_too_large(client: AsyncClient):
    # Create a payload > 8KB
    large_payload = {"data": "A" * 9000}

    payload = {
        "events": [
            {
                "event": "session_start",
                "payload": large_payload
            }
        ]
    }

    response = await client.post("/api/events", json=payload)

    # Should be rejected with HTTP 422 Unprocessable Entity due to validation failure
    assert response.status_code == 422
    assert "El tamaño del payload excede el límite de 8KB" in response.text
