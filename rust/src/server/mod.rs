// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # Servidor HTTP Axum para lota-server.
//!
//! Expone endpoints REST y WebSockets para NPCs, reportes de la rejilla
//! y eventos del dispatch GPU.
//! El estado se mantiene en `AppState` compartido entre handlers.

use std::sync::{Arc, RwLock};

use axum::{
    extract::{
        ws::{Message, WebSocket, WebSocketUpgrade},
        Query, State,
    },
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use me60os_core::resonant_matrix::ResonantMatrix;
use serde::{Deserialize, Serialize};
use tokio::sync::broadcast;

use crate::gpu::pipeline::DispatchResult;
use crate::npc::fsm::{InteractionAction, Npc, NpcState};
use crate::npc::orchestrator::NpcOrchestrator;

/// Representación explicita sexagesimal de 5 componentes: [d, m, s, t, q].
/// 0 <= m,s,t,q < 60. Aritmética entera pura.
#[derive(Debug, Serialize, Deserialize, Clone, Copy, PartialEq, Eq)]
pub struct S60Components {
    pub d: i64,
    pub m: i64,
    pub s: i64,
    pub t: i64,
    pub q: i64,
}

/// Convierte un entero raw i64 escalado por 12_960_000 a 5 componentes sexagesimales.
pub fn i64_to_s60_components(raw: i64) -> S60Components {
    let is_neg = raw < 0;
    let abs_raw = raw.abs();
    let mut d = abs_raw / 12_960_000;
    let mut rem = abs_raw % 12_960_000;
    let m = rem / 216_000;
    rem %= 216_000;
    let s = rem / 3_600;
    rem %= 3_600;
    let t = rem / 60;
    let q = rem % 60;

    if is_neg {
        d = -d;
    }

    S60Components { d, m, s, t, q }
}

/// Eventos transmitidos por WebSocket a los clientes.
#[derive(Debug, Clone, Serialize)]
#[serde(tag = "event", rename_all = "snake_case")]
pub enum ServerEvent {
    LatticeTick {
        tick: u32,
        node_count: u32,
        wave_value_sample: Vec<f32>,
    },
    PortalOpened {
        indices: Vec<u32>,
        count: u32,
        tick: u32,
    },
}

/// Representación serializable de un NPC para la API (con coords S60 compuestas).
#[derive(Debug, Serialize)]
pub struct NpcWire {
    pub id: u32,
    pub name: String,
    pub state: NpcState,
    pub lat_s60: S60Components,
    pub lon_s60: S60Components,
    pub zona_id: u64,
    pub mission_id: u32,
    pub active: bool,
}

impl From<&Npc> for NpcWire {
    fn from(npc: &Npc) -> Self {
        Self {
            id: npc.id,
            name: npc.name.clone(),
            state: npc.state,
            lat_s60: i64_to_s60_components(npc.lat),
            lon_s60: i64_to_s60_components(npc.lon),
            zona_id: npc.zona_id,
            mission_id: npc.mission_id,
            active: npc.active,
        }
    }
}

/// Estado global compartido del servidor.
pub struct AppState {
    pub orchestrator: RwLock<NpcOrchestrator>,
    pub last_dispatch: RwLock<Option<DispatchResult>>,
    pub tx_events: broadcast::Sender<ServerEvent>,
}

impl AppState {
    pub fn new(orchestrator: NpcOrchestrator) -> Arc<Self> {
        let (tx_events, _rx) = broadcast::channel(100);
        Arc::new(Self {
            orchestrator: RwLock::new(orchestrator),
            last_dispatch: RwLock::new(None),
            tx_events,
        })
    }
}

/// Respuesta JSON para /npcs.
#[derive(Debug, Serialize)]
struct NpcsResponse {
    zona_id: u64,
    count: usize,
    npcs: Vec<NpcWire>,
}

/// Query params para /npcs.
#[derive(Debug, Deserialize)]
struct NpcsQuery {
    zona_id: u64,
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
    let wire_npcs: Vec<NpcWire> = npcs.iter().map(|npc| NpcWire::from(*npc)).collect();
    Json(NpcsResponse {
        zona_id: query.zona_id,
        count: wire_npcs.len(),
        npcs: wire_npcs,
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

async fn ws_handler(
    ws: WebSocketUpgrade,
    State(state): State<Arc<AppState>>,
) -> impl axum::response::IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(mut socket: WebSocket, state: Arc<AppState>) {
    let mut rx = state.tx_events.subscribe();
    while let Ok(event) = rx.recv().await {
        if let Ok(json) = serde_json::to_string(&event) {
            if socket.send(Message::Text(json)).await.is_err() {
                break;
            }
        }
    }
}

/// Crea el router Axum con el estado compartido.
pub fn create_app(state: Arc<AppState>) -> axum::Router {
    Router::new()
        .route("/npcs", get(get_npcs))
        .route("/npcs/interact", post(post_interact))
        .route("/dispatch", get(get_dispatch))
        .route("/portales", get(get_portales))
        .route("/ws/events", get(ws_handler))
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

    #[test]
    fn test_i64_to_s60_components() {
        // -37.089° * 12_960_000 = -480_673_440
        let raw = -480_673_440;
        let comps = i64_to_s60_components(raw);
        assert_eq!(comps.d, -37);
        assert!(comps.m >= 0 && comps.m < 60);
        assert!(comps.s >= 0 && comps.s < 60);
        assert!(comps.t >= 0 && comps.t < 60);
        assert!(comps.q >= 0 && comps.q < 60);
    }
}
