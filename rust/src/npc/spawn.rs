// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # Spawning de NPCs a partir de eventos celestes y de zona.

use super::fsm::{Npc, S60_SCALE};

/// Evento del cielo o de zona que puede activar un NPC.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SkyEvent {
    /// Atardecer del Carbón (≈19:00 en zona horaria de Lota).
    AtardecerDelCarbon,
    /// Evento genérico de portal abierto.
    PortalAbierto,
    /// Evento de prueba.
    TestEvent,
}

/// Crea un NPC a partir de un evento.
///
/// Determinista: el mismo evento siempre genera el mismo NPC y misma posición inicial.
pub fn spawn_npc_from_event(event: SkyEvent) -> Option<Npc> {
    match event {
        SkyEvent::AtardecerDelCarbon | SkyEvent::TestEvent => {
            // Coordenadas fijas S60 dentro del polígono del Parque de Lota.
            // -37.089° → lat = -37 * SCALE - 0.089 * SCALE
            let lat_deg = -37_089 * S60_SCALE / 1000;
            let lon_deg = -73_165 * S60_SCALE / 1000;

            let waypoints = vec![
                (lat_deg, lon_deg),
                (lat_deg + S60_SCALE / 3600, lon_deg),
                (lat_deg + S60_SCALE / 3600, lon_deg + S60_SCALE / 3600),
                (lat_deg, lon_deg + S60_SCALE / 3600),
            ];

            Some(
                Npc::new(1, "Isidora Goyenechea", lat_deg, lon_deg, 89121388, 1)
                    .with_waypoints(waypoints),
            )
        }
        SkyEvent::PortalAbierto => {
            // Por ahora no spawnea NPC nuevo; extensión futura.
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spawn_isidora_from_atardecer() {
        let npc = spawn_npc_from_event(SkyEvent::AtardecerDelCarbon).unwrap();
        assert_eq!(npc.name, "Isidora Goyenechea");
        assert_eq!(npc.zona_id, 89121388);
        assert_eq!(npc.waypoints.len(), 4);
    }

    #[test]
    fn test_spawn_none_on_portal_abierto() {
        assert!(spawn_npc_from_event(SkyEvent::PortalAbierto).is_none());
    }
}
