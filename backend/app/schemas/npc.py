"""Schemas Pydantic para la API de NPCs."""
from pydantic import BaseModel, ConfigDict


class NpcOut(BaseModel):
    """Representación de un NPC."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    zona_id: int
    fsm_state: str
    lat: float
    lon: float
    mission_id: int
    active: bool


class InteractRequest(BaseModel):
    """Request para POST /api/npcs/interact."""

    npc_id: int
    user_id: str
    action: str


class InteractResponse(BaseModel):
    """Response para POST /api/npcs/interact."""

    npc_id: int
    accepted: bool
    state: str
    message: str
