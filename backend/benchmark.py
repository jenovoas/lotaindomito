import asyncio
import time
from httpx import ASGITransport, AsyncClient
from app.main import app

async def benchmark():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # warm up
        for _ in range(10):
            await client.get("/api/zonas")

        start_time = time.perf_counter()
        for _ in range(500):
            await client.get("/api/zonas")
        end_time = time.perf_counter()

        print(f"Time for 500 requests: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(benchmark())
