from datetime import datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/api/events', tags=['analytics'])


class EventItem(BaseModel):
    event: str = Field(..., description="Nombre del evento (ej. session_start, poi_visit)")
    payload: dict[str, Any] = Field(..., description="Datos del evento")


class EventsRequest(BaseModel):
    events: list[EventItem] = Field(..., min_length=1, max_length=100)


class EventsResponse(BaseModel):
    received: int
    stored: bool


@router.post('', response_model=EventsResponse)
async def ingest_events(
    req: EventsRequest,
    db: AsyncSession = Depends(get_db),
) -> EventsResponse:
    for ev in req.events:
        if not ev.payload.get('timestamp'):
            ev.payload['timestamp'] = datetime.utcnow().isoformat()

    await db.execute(
        text("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                id BIGSERIAL PRIMARY KEY,
                event_name TEXT NOT NULL,
                user_id TEXT,
                payload JSONB NOT NULL,
                received_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
    )

    for ev in req.events:
        user_id = ev.payload.get('user_id', '')
        await db.execute(
            text("""
                INSERT INTO analytics_events (event_name, user_id, payload)
                VALUES (:event_name, :user_id, :payload::jsonb)
            """),
            {
                'event_name': ev.event,
                'user_id': user_id,
                'payload': ev.payload,
            },
        )

    await db.commit()
    return EventsResponse(received=len(req.events), stored=True)


@router.get('/stats')
async def events_stats(
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    await db.execute(
        text("""
            CREATE TABLE IF NOT EXISTS analytics_events (
                id BIGSERIAL PRIMARY KEY,
                event_name TEXT NOT NULL,
                user_id TEXT,
                payload JSONB NOT NULL,
                received_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
    )
    await db.commit()

    rows = await db.execute(
        text("""
            SELECT
                event_name,
                COUNT(*) as total,
                COUNT(DISTINCT user_id) as unique_users
            FROM analytics_events
            GROUP BY event_name
            ORDER BY total DESC
        """)
    )
    stats = [dict(row._mapping) for row in rows]
    total = await db.execute(text('SELECT COUNT(*) as total FROM analytics_events'))
    total_row = dict((await total.all())[0]._mapping)
    return {
        'total_events': total_row['total'],
        'by_event': stats,
    }
