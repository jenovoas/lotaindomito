// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # Máquina de estados finita (FSM) de un NPC.

use serde::{Deserialize, Serialize};

/// Escala S60 usada para lat/lon (1 unidad = 1/SCALE_0 de grado).
pub const S60_SCALE: i64 = 12_960_000;

/// Estados de la FSM de un NPC.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[repr(u8)]
pub enum NpcState {
    Idle = 0,
    Wander = 1,
    Approach = 2,
    Deliver = 3,
}

impl NpcState {
    /// Verifica si una transición desde el estado actual a `next` es válida.
    pub fn can_transition(self, next: NpcState) -> bool {
        match (self, next) {
            (NpcState::Idle, NpcState::Wander)
            | (NpcState::Idle, NpcState::Approach)
            | (NpcState::Wander, NpcState::Approach)
            | (NpcState::Approach, NpcState::Deliver)
            | (NpcState::Deliver, NpcState::Idle)
            | (NpcState::Wander, NpcState::Idle)
            | (NpcState::Approach, NpcState::Idle) => true,
            _ => false,
        }
    }
}

/// Acciones que un jugador puede solicitarle a un NPC.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum InteractionAction {
    Approach,
    Deliver,
    Dismiss,
}

impl InteractionAction {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "approach" => Some(InteractionAction::Approach),
            "deliver" => Some(InteractionAction::Deliver),
            "dismiss" => Some(InteractionAction::Dismiss),
            _ => None,
        }
    }
}

/// Resultado de una interacción jugador↔NPC.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct NpcInteractionResult {
    pub npc_id: u32,
    pub prev_state: NpcState,
    pub new_state: NpcState,
    pub accepted: bool,
    pub message: String,
}

/// Un NPC del enjambre SOMA.
///
/// `lat` y `lon` están en grados S60 escalados por `S60_SCALE`.
/// La estructura es `#[repr(C)]` para poder cruzar a VRAM/SHM si se requiere.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[repr(C)]
pub struct Npc {
    pub id: u32,
    pub name: String,
    pub state: NpcState,
    pub lat: i64,
    pub lon: i64,
    pub zona_id: u64,
    pub mission_id: u32,
    pub waypoints: Vec<(i64, i64)>,
    pub waypoint_idx: usize,
    pub active: bool,
    /// Velocidad de movimiento en unidades S60 por tick.
    pub speed: i64,
    /// Contador de ticks acumulados (determinista).
    pub tick_counter: u64,
}

impl Npc {
    /// Crea un nuevo NPC en estado `Idle`.
    pub fn new(id: u32, name: &str, lat: i64, lon: i64, zona_id: u64, mission_id: u32) -> Self {
        Self {
            id,
            name: name.to_string(),
            state: NpcState::Idle,
            lat,
            lon,
            zona_id,
            mission_id,
            waypoints: Vec::new(),
            waypoint_idx: 0,
            active: true,
            speed: S60_SCALE / 3600, // 1 arcsec/tick determinista
            tick_counter: 0,
        }
    }

    /// Asigna una ruta fija de waypoints S60.
    pub fn with_waypoints(mut self, waypoints: Vec<(i64, i64)>) -> Self {
        self.waypoints = waypoints;
        self
    }

    /// Intenta transicionar la FSM a `new_state`.
    /// Devuelve `true` si la transición fue aceptada.
    pub fn transition(&mut self, new_state: NpcState) -> bool {
        if self.state.can_transition(new_state) {
            self.state = new_state;
            true
        } else {
            false
        }
    }

    /// Procesa una acción del jugador y muta el estado de la FSM.
    pub fn interact(&mut self, action: InteractionAction) -> NpcInteractionResult {
        let prev = self.state;
        let (new_state, accepted, message) = match (prev, action) {
            (NpcState::Idle, InteractionAction::Approach) => {
                (NpcState::Approach, true, "Isidora te observa y se acerca.".to_string())
            }
            (NpcState::Approach, InteractionAction::Deliver) => {
                (NpcState::Deliver, true, "Entregas el mensaje del Carbón.".to_string())
            }
            (NpcState::Deliver, InteractionAction::Dismiss) => {
                (NpcState::Idle, true, "Isidora asiente y vuelve a su guardia.".to_string())
            }
            (NpcState::Wander, InteractionAction::Approach) => {
                (NpcState::Approach, true, "Isidora deja de vagar y se acerca.".to_string())
            }
            _ => (prev, false, "Acción no válida para estado actual".to_string()),
        };

        if accepted {
            self.state = new_state;
        }

        NpcInteractionResult {
            npc_id: self.id,
            prev_state: prev,
            new_state: self.state,
            accepted,
            message,
        }
    }

    /// Avanza la FSM un tick determinista.
    /// - Idle → Wander cuando el contador alcanza un umbral determinista.
    /// - Wander mueve el NPC hacia el siguiente waypoint.
    /// - Approach/Idle/Deliver no modifican posición.
    pub fn tick(&mut self) {
        self.tick_counter += 1;
        match self.state {
            NpcState::Idle => {
                // Transición determinista a Wander cada 120 ticks.
                if self.tick_counter % 120 == 0 {
                    self.state = NpcState::Wander;
                }
            }
            NpcState::Wander => {
                self.step_toward_next_waypoint();
                // Si alcanza el waypoint, vuelve a Idle.
                if self.waypoints.is_empty() {
                    self.state = NpcState::Idle;
                }
            }
            NpcState::Approach | NpcState::Deliver => {
                // Mantener estado hasta interacción explícita.
            }
        }
    }

    /// Avanza un paso determinista hacia el waypoint actual usando solo i64.
    fn step_toward_next_waypoint(&mut self) {
        if self.waypoints.is_empty() {
            return;
        }

        let (target_lat, target_lon) = self.waypoints[self.waypoint_idx];
        let dlat = target_lat - self.lat;
        let dlon = target_lon - self.lon;

        // Si estamos suficientemente cerca, avanzar al siguiente waypoint.
        let threshold = S60_SCALE / 3600; // 1 arcsec
        if dlat.abs() <= threshold && dlon.abs() <= threshold {
            self.waypoint_idx = (self.waypoint_idx + 1) % self.waypoints.len();
            return;
        }

        // Normalización aproximada determinista (longitud L1 escalada).
        let manhattan = dlat.abs() + dlon.abs();
        if manhattan == 0 {
            return;
        }

        let step_lat = (dlat * self.speed) / manhattan;
        let step_lon = (dlon * self.speed) / manhattan;

        // Aplicar paso mínimo 1 unidad para garantizar progreso.
        self.lat += if dlat > 0 { step_lat.max(1) } else { step_lat.min(-1) };
        self.lon += if dlon > 0 { step_lon.max(1) } else { step_lon.min(-1) };
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_npc_starts_idle() {
        let npc = Npc::new(1, "Isidora", 0, 0, 89121388, 0);
        assert_eq!(npc.state, NpcState::Idle);
    }

    #[test]
    fn test_state_transitions() {
        assert!(NpcState::Idle.can_transition(NpcState::Wander));
        assert!(NpcState::Wander.can_transition(NpcState::Approach));
        assert!(NpcState::Approach.can_transition(NpcState::Deliver));
        assert!(NpcState::Deliver.can_transition(NpcState::Idle));
        assert!(!NpcState::Idle.can_transition(NpcState::Deliver));
    }

    #[test]
    fn test_interact_approach_from_idle() {
        let mut npc = Npc::new(1, "Isidora", 0, 0, 89121388, 0);
        let result = npc.interact(InteractionAction::Approach);
        assert!(result.accepted);
        assert_eq!(result.new_state, NpcState::Approach);
        assert_eq!(npc.state, NpcState::Approach);
    }

    #[test]
    fn test_interact_deliver_from_approach() {
        let mut npc = Npc::new(1, "Isidora", 0, 0, 89121388, 0);
        npc.transition(NpcState::Approach);
        let result = npc.interact(InteractionAction::Deliver);
        assert!(result.accepted);
        assert_eq!(result.new_state, NpcState::Deliver);
    }

    #[test]
    fn test_invalid_interaction() {
        let mut npc = Npc::new(1, "Isidora", 0, 0, 89121388, 0);
        let result = npc.interact(InteractionAction::Deliver);
        assert!(!result.accepted);
        assert_eq!(npc.state, NpcState::Idle);
    }

    #[test]
    fn test_tick_idle_to_wander() {
        let mut npc = Npc::new(1, "Isidora", 0, 0, 89121388, 0);
        for _ in 0..119 {
            npc.tick();
        }
        assert_eq!(npc.state, NpcState::Idle);
        npc.tick();
        assert_eq!(npc.state, NpcState::Wander);
    }

    #[test]
    fn test_wander_moves_toward_waypoint() {
        let waypoints = vec![(S60_SCALE, S60_SCALE)];
        let mut npc = Npc::new(1, "Isidora", 0, 0, 89121388, 0)
            .with_waypoints(waypoints);
        npc.state = NpcState::Wander;
        let prev_lat = npc.lat;
        let prev_lon = npc.lon;
        npc.tick();
        assert!(npc.lat > prev_lat || npc.lon > prev_lon);
    }
}
