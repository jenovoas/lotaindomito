// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # Servidor HTTP Axum para lota-server.
//!
//! Expone endpoints REST para NPCs y reportes del dispatch GPU.
//! El estado se mantiene en `AppState` compartido entre handlers.

use std::sync::{Arc, RwLock};

use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use me60os_core::resonant_matrix::ResonantMatrix;
use serde::{Deserialize, Serialize};

use crate::gpu::pipeline::DispatchResult;
use crate::npc::fsm::{InteractionAction, Npc};
use crate::npc::orchestrator::NpcOrchestrator;

/// Estado global compartido del servidor.
pub struct AppState {
    pub orchestrator: RwLock<NpcOrchestrator>,
    pub last_dispatch: RwLock<Option<DispatchResult>>,
}

impl AppState {
    pub fn new(orchestrator: NpcOrchestrator) -> Arc<Self> {
        Arc::new(Self {
            orchestrator: RwLock::new(orchestrator),
            last_dispatch: RwLock::new(None),
        })
    }
}

/// Respuesta JSON para /npcs.
#[derive(Debug, Serialize)]
struct NpcsResponse {
    zona_id: u32,
    count: usize,
    npcs: Vec<Npc>,
}

/// Query params para /npcs.
#[derive(Debug, Deserialize)]
struct NpcsQuery {
    zona_id: u32,
}

/// Body para POST /npcs/interact.
#[derive(Debug, Deserialize)]
struct InteractRequest {
    npc_id: u32,
    user_id: String,
    action: String,
}


async fn get_npcs(State(state): State<Arc<AppState>>, Query(query): Query<NpcsQuery>) -> Json<NpcsResponse> {
    let orchestrator = state.orchestrator.read().unwrap();
    let npcs = orchestrator.get_active_npcs(query.zona_id);
    let cloned: Vec<Npc> = npcs.iter().map(|npc| (*npc).clone()).collect();
    Json(NpcsResponse {
        zona_id: query.zona_id,
        count: cloned.len(),
        npcs: cloned,
    })
}

async fn post_interact(
    State(state): State<Arc<AppState>>,
    Json(payload): Json<InteractRequest>,
) -> Result<Json<serde_json::Value>, (StatusCode, String)> {
    let action = match InteractionAction::from_str(&payload.action) {
        Some(a) => a,
        None => {
            return Err((
                StatusCode::BAD_REQUEST,
                "Acción no válida para estado actual".to_string(),
            ))
        }
    };

    let mut orchestrator = state.orchestrator.write().unwrap();
    match orchestrator.interact(payload.npc_id, &payload.user_id, action) {
        Some(result) => {
            if result.accepted {
                Ok(Json(serde_json::json!({
                    "npc_id": result.npc_id,
                    "accepted": true,
                    "state": format!("{:?}", result.new_state).to_lowercase(),
                    "message": result.message,
                })))
            } else {
                Ok(Json(serde_json::json!({
                    "npc_id": result.npc_id,
                    "accepted": false,
                    "state": format!("{:?}", result.prev_state).to_lowercase(),
                    "message": result.message,
                })))
            }
        }
        None => Err((StatusCode::NOT_FOUND, "NPC no encontrado".to_string())),
    }
}

async fn get_dispatch(State(state): State<Arc<AppState>>) -> Json<serde_json::Value> {
    let dispatch = state.last_dispatch.read().unwrap();
    match dispatch.as_ref() {
        Some(result) => Json(serde_json::json!({
            "portal_count": result.portal_count,
            "portal_indices": result.portal_indices,
            "wave_values_sample": result.wave_values.iter().take(10).copied().collect::<Vec<f32>>(),
        })),
        None => Json(serde_json::json!({
            "portal_count": 0,
            "portal_indices": [],
            "wave_values_sample": [],
        })),
    }
}

async fn get_portales(State(state): State<Arc<AppState>>) -> Json<serde_json::Value> {
    let dispatch = state.last_dispatch.read().unwrap();
    match dispatch.as_ref() {
        Some(result) => Json(serde_json::json!({
            "portales": result.portal_indices.clone(),
            "count": result.portal_count,
        })),
        None => Json(serde_json::json!({
            "portales": [],
            "count": 0,
        })),
    }
}

/// Crea el router Axum con el estado compartido.
pub fn create_app(state: Arc<AppState>) -> axum::Router {
    Router::new()
        .route("/npcs", get(get_npcs))
        .route("/npcs/interact", post(post_interact))
        .route("/dispatch", get(get_dispatch))
        .route("/portales", get(get_portales))
        .with_state(state)
}

/// Inicializa las dos mallas resonantes duales usadas por el dispatch GPU.
pub fn initialize_resonant_lattices() -> (ResonantMatrix, ResonantMatrix) {
    let mut lane_a = ResonantMatrix::new(91);
    let mut lane_b = ResonantMatrix::new(91);
    for i in 0..5 {
        lane_a.inject(i * 18, 5_000_000);
        lane_b.inject(i * 18 + 9, 3_000_000);
    }
    for _ in 0..68 {
        lane_a.step();
        lane_b.step();
    }
    (lane_a, lane_b)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::npc::orchestrator::NpcOrchestrator;

    #[test]
    fn test_app_state_creation() {
        let state = AppState::new(NpcOrchestrator::new());
        let guard = state.orchestrator.read().unwrap();
        let npcs = guard.get_active_npcs(89121388);
        assert_eq!(npcs.len(), 1);
    }
}
