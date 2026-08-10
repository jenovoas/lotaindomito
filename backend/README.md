# Lota Indómito — Backend

FastAPI + PostgreSQL/PostGIS para el piloto de concepto.

## Setup

```bash
cd backend
uv sync --dev
cp .env.example .env  # ajustar DATABASE_URL si es necesario
docker-compose up -d  # levanta PostGIS
alembic upgrade head   # crea tablas
python seed.py        # carga 11 zonas desde piloto-a/src/data/zonas-lota.json
uvicorn app.main:app --reload
```

## API

- `GET /api/zonas` — lista todas las zonas (GeoJSON)
- `GET /api/zonas/{id}` — zona por id
- `POST /api/zonas/contains` — point-in-polygon
- `GET /health` — health check

## Tests

```bash
pytest
```
