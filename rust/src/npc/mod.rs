// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # 👥 MÓDULO NPC — ENJAMBRE SOMA 👥
//!
//! Máquinas de estado finito (FSM) deterministas para NPCs server-authoritative.
//! Posiciones en S60 fixed-point (i64, SCALE_0 = 12_960_000). 0 floats en CPU.

pub mod fsm;
pub mod orchestrator;
pub mod spawn;

pub use fsm::{InteractionAction, Npc, NpcInteractionResult, NpcState};
pub use orchestrator::NpcOrchestrator;
pub use spawn::{spawn_npc_from_event, SkyEvent};
