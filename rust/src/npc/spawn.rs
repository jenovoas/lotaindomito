// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # Spawning de NPCs a partir de eventos celestes y de zona.

use super::fsm::{Npc, S60_SCALE};

/// Evento del cielo o de zona que puede activar un NPC.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SkyEvent {
    /// Atardecer del Carbón (≈19:00 en zona horaria de Lota).
    AtardecerDelCarbon,
    /// Turno de la Mina / Amanecer del Minero (≈07:00).
    AmanecerDelMinero,
    /// Turno de Maestranza y Despacho.
    TurnoMaestranza,
    /// Evento genérico de portal abierto.
    PortalAbierto,
    /// Evento de prueba que carga todos los NPCs piloto.
    TestEvent,
}

/// Crea un conjunto de NPCs iniciales para poblar la comuna de Lota.
pub fn spawn_initial_npcs() -> Vec<Npc> {
    vec![
        // 1. Isidora Goyenechea en el Parque de Lota
        {
            let lat_deg = -37_088 * S60_SCALE / 1000;
            let lon_deg = -73_165 * S60_SCALE / 1000;
            let waypoints = vec![
                (lat_deg, lon_deg),
                (lat_deg + S60_SCALE / 3600, lon_deg),
                (lat_deg + S60_SCALE / 3600, lon_deg + S60_SCALE / 3600),
                (lat_deg, lon_deg + S60_SCALE / 3600),
            ];
            Npc::new(1, "Isidora Goyenechea", lat_deg, lon_deg, 89121388, 1)
                .with_waypoints(waypoints)
        },
        // 2. El Palanquero en el Corredor de Pabellones hacia Chiflón
        {
            let lat_deg = -37_094 * S60_SCALE / 1000;
            let lon_deg = -73_161 * S60_SCALE / 1000;
            let waypoints = vec![
                (lat_deg, lon_deg),
                (lat_deg - S60_SCALE / 1800, lon_deg - S60_SCALE / 1800),
                (lat_deg - S60_SCALE / 1200, lon_deg - S60_SCALE / 1200),
                (lat_deg, lon_deg),
            ];
            Npc::new(2, "El Palanquero", lat_deg, lon_deg, 12557447365, 2)
                .with_waypoints(waypoints)
        },
        // 3. El Ciego de la Mina en el Chiflón del Diablo
        {
            let lat_deg = -37_095 * S60_SCALE / 1000;
            let lon_deg = -73_171 * S60_SCALE / 1000;
            let waypoints = vec![
                (lat_deg, lon_deg),
                (lat_deg + S60_SCALE / 3600, lon_deg),
                (lat_deg, lon_deg),
            ];
            Npc::new(3, "El Ciego de la Mina", lat_deg, lon_deg, 480338029, 3)
                .with_waypoints(waypoints)
        },
    ]
}

/// Crea un NPC a partir de un evento específico.
pub fn spawn_npc_from_event(event: SkyEvent) -> Option<Npc> {
    match event {
        SkyEvent::AtardecerDelCarbon => {
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
        SkyEvent::TurnoMaestranza => {
            let lat_deg = -37_094 * S60_SCALE / 1000;
            let lon_deg = -73_161 * S60_SCALE / 1000;
            let waypoints = vec![
                (lat_deg, lon_deg),
                (lat_deg - S60_SCALE / 1800, lon_deg - S60_SCALE / 1800),
                (lat_deg, lon_deg),
            ];
            Some(
                Npc::new(2, "El Palanquero", lat_deg, lon_deg, 12557447365, 2)
                    .with_waypoints(waypoints),
            )
        }
        SkyEvent::AmanecerDelMinero => {
            let lat_deg = -37_095 * S60_SCALE / 1000;
            let lon_deg = -73_171 * S60_SCALE / 1000;
            Some(Npc::new(3, "El Ciego de la Mina", lat_deg, lon_deg, 480338029, 3))
        }
        SkyEvent::TestEvent => spawn_initial_npcs().into_iter().next(),
        SkyEvent::PortalAbierto => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spawn_initial_npcs_has_three_figures() {
        let npcs = spawn_initial_npcs();
        assert_eq!(npcs.len(), 3);
        assert_eq!(npcs[0].name, "Isidora Goyenechea");
        assert_eq!(npcs[1].name, "El Palanquero");
        assert_eq!(npcs[2].name, "El Ciego de la Mina");
    }

    #[test]
    fn test_spawn_isidora_from_atardecer() {
        let npc = spawn_npc_from_event(SkyEvent::AtardecerDelCarbon).unwrap();
        assert_eq!(npc.name, "Isidora Goyenechea");
        assert_eq!(npc.zona_id, 89121388);
        assert_eq!(npc.waypoints.len(), 4);
    }

    #[test]
    fn test_spawn_palanquero_from_turno() {
        let npc = spawn_npc_from_event(SkyEvent::TurnoMaestranza).unwrap();
        assert_eq!(npc.name, "El Palanquero");
        assert_eq!(npc.zona_id, 12557447365);
    }

    #[test]
    fn test_spawn_none_on_portal_abierto() {
        assert!(spawn_npc_from_event(SkyEvent::PortalAbierto).is_none());
    }
}

