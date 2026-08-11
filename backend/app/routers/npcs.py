"""Router /api/npcs — CRUD de NPCs del backend."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas.npc import InteractRequest, InteractResponse, NpcOut

router = APIRouter(prefix="/api/npcs", tags=["npcs"])

# Transiciones válidas de la máquina de estados del NPC.
# idle → approach → deliver → idle
_VALID_TRANSITIONS: dict[str, dict[str, str]] = {
    "idle": {"approach": "approach"},
    "wander": {"approach": "approach"},
    "approach": {"deliver": "deliver"},
    "deliver": {"dismiss": "idle"},
}


@router.get("", response_model=list[NpcOut])
async def list_npcs(
    zona_id: int,
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> list[NpcOut]:
    """Lista NPCs activos de una zona."""
    try:
        result = await db.execute(
            text(
                """
                SELECT id, name, zona_id, fsm_state, lat, lon, mission_id, active
                FROM npcs
                WHERE zona_id = :zona_id AND active = true
                ORDER BY id
                """
            ),
            {"zona_id": zona_id},
        )
        rows = result.fetchall()
        return [
            NpcOut(
                id=row.id,
                name=row.name,
                zona_id=row.zona_id,
                fsm_state=row.fsm_state,
                lat=row.lat,
                lon=row.lon,
                mission_id=row.mission_id,
                active=row.active,
            )
            for row in rows
        ]
    except Exception:  # noqa: BLE001
        return []


@router.post("/interact", response_model=InteractResponse)
async def interact(
    payload: InteractRequest,
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> InteractResponse:
    """Procesa una interacción con un NPC y actualiza su FSM."""
    action = payload.action
    valid_actions = {"approach", "deliver", "dismiss"}
    if action not in valid_actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Acción inválida: {action}",
        )

    try:
        result = await db.execute(
            text(
                """
                SELECT id, name, fsm_state
                FROM npcs
                WHERE id = :npc_id
                """
            ),
            {"npc_id": payload.npc_id},
        )
        row = result.fetchone()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available",
        ) from exc

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"NPC {payload.npc_id} no encontrado",
        )

    current_state = row.fsm_state
    transitions = _VALID_TRANSITIONS.get(current_state, {})
    new_state = transitions.get(action)

    if new_state is None:
        return InteractResponse(
            npc_id=row.id,
            accepted=False,
            state=current_state,
            message=f"Acción '{action}' no aplica en estado '{current_state}'",
        )

    try:
        await db.execute(
            text("UPDATE npcs SET fsm_state = :state WHERE id = :npc_id"),
            {"state": new_state, "npc_id": row.id},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available",
        ) from exc

    messages = {
        "approach": "El NPC se acerca al jugador.",
        "deliver": "El NPC entrega el objeto de la misión.",
        "dismiss": "El NPC se despide y vuelve a su rutina.",
    }

    return InteractResponse(
        npc_id=row.id,
        accepted=True,
        state=new_state,
        message=messages.get(action, "Interacción procesada."),
    )
