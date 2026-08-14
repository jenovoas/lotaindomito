// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # Orquestador del enjambre SOMA de NPCs.

use std::collections::HashMap;

use super::fsm::{InteractionAction, Npc, NpcInteractionResult, NpcState};
use super::spawn::spawn_initial_npcs;

/// Orquesta todos los NPCs del servidor.
///
/// Server-authoritative: las transiciones de estado y posiciones ocurren aquí,
/// no en el cliente.
pub struct NpcOrchestrator {
    npcs: HashMap<u32, Npc>,
    next_id: u32,
}

impl NpcOrchestrator {
    /// Crea el orquestador con los NPCs piloto iniciales.
    pub fn new() -> Self {
        let mut npcs = HashMap::new();
        let initial = spawn_initial_npcs();
        let mut max_id = 0;
        for npc in initial {
            if npc.id > max_id {
                max_id = npc.id;
            }
            npcs.insert(npc.id, npc);
        }
        Self {
            npcs,
            next_id: max_id + 1,
        }
    }

    /// Avanza la FSM de cada NPC un tick determinista.
    pub fn tick(&mut self) {
        for npc in self.npcs.values_mut() {
            npc.tick();
        }
    }

    /// Devuelve los NPCs activos en una zona.
    pub fn get_active_npcs(&self, zona_id: u64) -> Vec<&Npc> {
        self.npcs
            .values()
            .filter(|npc| npc.zona_id == zona_id && npc.active)
            .collect()
    }

    /// Procesa una interacción jugador↔NPC.
    pub fn interact(
        &mut self,
        npc_id: u32,
        _user_id: &str,
        action: InteractionAction,
    ) -> Option<NpcInteractionResult> {
        self.npcs.get_mut(&npc_id).map(|npc| npc.interact(action))
    }

    /// Fuerza un estado para testing o eventos del mundo.
    pub fn set_state(&mut self, npc_id: u32, state: NpcState) -> bool {
        if let Some(npc) = self.npcs.get_mut(&npc_id) {
            npc.state = state;
            true
        } else {
            false
        }
    }

    /// Inserta un NPC nuevo en el orquestador.
    pub fn insert(&mut self, mut npc: Npc) -> u32 {
        let id = self.next_id.max(npc.id);
        npc.id = id;
        self.next_id = id + 1;
        self.npcs.insert(id, npc);
        id
    }

    /// Devuelve una referencia a un NPC por ID.
    pub fn get(&self, npc_id: u32) -> Option<&Npc> {
        self.npcs.get(&npc_id)
    }
}

impl Default for NpcOrchestrator {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_orchestrator_has_default_npcs() {
        let orchestrator = NpcOrchestrator::new();
        let isidora = orchestrator.get_active_npcs(89121388);
        assert_eq!(isidora.len(), 1);
        assert_eq!(isidora[0].name, "Isidora Goyenechea");

        let palanquero = orchestrator.get_active_npcs(12557447365);
        assert_eq!(palanquero.len(), 1);
        assert_eq!(palanquero[0].name, "El Palanquero");

        let ciego = orchestrator.get_active_npcs(480338029);
        assert_eq!(ciego.len(), 1);
        assert_eq!(ciego[0].name, "El Ciego de la Mina");
    }

    #[test]
    fn test_orchestrator_empty_for_unknown_zone() {
        let orchestrator = NpcOrchestrator::new();
        let npcs = orchestrator.get_active_npcs(999);
        assert!(npcs.is_empty());
    }

    #[test]
    fn test_orchestrator_interact() {
        let mut orchestrator = NpcOrchestrator::new();
        let result = orchestrator.interact(1, "test", InteractionAction::Approach);
        assert!(result.is_some());
        let result = result.unwrap();
        assert!(result.accepted);
        assert_eq!(result.new_state, NpcState::Approach);
    }

    #[test]
    fn test_orchestrator_interact_unknown_npc() {
        let mut orchestrator = NpcOrchestrator::new();
        let result = orchestrator.interact(999, "test", InteractionAction::Approach);
        assert!(result.is_none());
    }

    #[test]
    fn test_orchestrator_tick() {
        let mut orchestrator = NpcOrchestrator::new();
        orchestrator.tick();
        let npcs = orchestrator.get_active_npcs(89121388);
        assert_eq!(npcs.len(), 1);
    }
}
