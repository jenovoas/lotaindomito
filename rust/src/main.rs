// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # ⚡ LOTA INDÓMITO ENGINE - DEDICATED SERVER / GPU ENGINE ⚡
//!
//! Binario `lota-server`. Inicializa el pipeline GPU (wgpu/Vulkan),
//! construye un `ResonantMatrix` real de Sentinel, lo sube a VRAM,
//! dispatchea el compute shader de interferencia dual-lane y reporta
//! portales abiertos, todo mientras corre el servidor HTTP de NPCs.

use std::sync::Arc;

use axum::serve;
use lota_engine::gpu::pipeline::LotaGpuPipeline;
use lota_engine::npc::orchestrator::NpcOrchestrator;
use lota_engine::server::{create_app, AppState, ServerEvent};
use me60os_core::atlantean::GpuController;
use me60os_core::resonant_matrix::ResonantMatrix;
use me60os_core::spa::SPA;
use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    println!("⚡ Inicializando Lota Indómito Engine (Camino C)...");

    // ── 1. Inicializar pipeline GPU ──
    let pipeline = match LotaGpuPipeline::new().await {
        Ok(p) => {
            println!("🟢 GPU Pipeline inicializado correctamente!");
            println!("🎮 {}", p.get_gpu_info());
            p
        }
        Err(err) => {
            eprintln!("⚠️ No se pudo abrir backend GPU nativo: {}", err);
            eprintln!("   El motor requiere una GPU con soporte Vulkan/Metal/DX12.");
            std::process::exit(1);
        }
    };

    // ── 2. Construir mallas resonantes duales (Lane A + Lane B) ──
    // 91 nodos = lattice pentagonal de Sentinel (7 anillos hexagonales)
    let mut lane_a = ResonantMatrix::new(91);
    let mut lane_b = ResonantMatrix::new(91);

    println!("🔮 ResonantMatrix dual-lane construida: {} nodos por carril", lane_a.size());

    // ── 3. Injectar perturbación inicial en algunos nodos ──
    for i in 0..5 {
        lane_a.inject(i * 18, 5_000_000);
        lane_b.inject(i * 18 + 9, 3_000_000);
    }

    // ── 4. Evolucionar la lattice algunos pasos ──
    for _tick in 0..68 {
        lane_a.step();
        lane_b.step();
    }
    println!("⚙️ Lattice evolucionada 68 ticks (1 ciclo Salto-17)");

    // ── 5. Subir a VRAM y dispatchear compute shader ──
    let tick = 68u32;
    let time_sec = 1.36f32;

    println!("🚀 Dispatcheando compute shader (lattice_interference.wgsl)...");
    let result = pipeline.upload_and_dispatch(&lane_a, &lane_b, tick, time_sec)?;

    // ── 6. Reportar resultados ──
    println!();
    println!("═══════════════════════════════════════════════");
    println!("  RESULTADO DEL DISPATCH GPU");
    println!("═══════════════════════════════════════════════");
    println!("  Nodos procesados:     {}", result.wave_values.len());
    println!("  Portales abiertos:    {}", result.portal_count);

    if result.portal_count > 0 {
        println!("  Índices de portales:   {:?}", result.portal_indices);
    }

    let sample = result.wave_values.iter().take(10).copied().collect::<Vec<_>>();
    println!("  Wave values (10):     {:?}", sample);
    println!("═══════════════════════════════════════════════");
    println!();

    // ── 7. GpuController P-Target info ──
    let controller = GpuController::new();
    println!("⚙️ GPU Controller P-Target Latency: {} ms", controller.target_latency_msx1000 / 1000);

    // ── 8. SPA sanity check ──
    let spa_test = SPA::new(1, 30, 0, 0, 0);
    println!("💎 SPA S60 Test Value: {:?}", spa_test);

    // ── 9. Inicializar orquestador de NPCs y estado compartido ──
    let app_state = AppState::new(NpcOrchestrator::new());
    // Guardar resultado del dispatch para endpoints /dispatch y /portales.
    *app_state.last_dispatch.write().unwrap() = Some(result);

    // ── 10. Lanzar tick loop NPCs y broadcast de eventos WS en background ──
    let tick_state = Arc::clone(&app_state);
    tokio::spawn(async move {
        let mut interval = tokio::time::interval(std::time::Duration::from_millis(1000));
        let mut tick_count: u64 = 0;
        let mut last_portal_count: u32 = 0;

        loop {
            interval.tick().await;
            tick_count += 1;
            tick_state.orchestrator.write().unwrap().tick();

            // Emitir lattice_tick cada 68 ticks (heartbeat Qhc / Salto-17)
            if tick_count % 68 == 0 {
                let sample = {
                    let dispatch_guard = tick_state.last_dispatch.read().unwrap();
                    dispatch_guard
                        .as_ref()
                        .map(|d| d.wave_values.iter().take(10).copied().collect::<Vec<f32>>())
                        .unwrap_or_default()
                };

                let _ = tick_state.tx_events.send(ServerEvent::LatticeTick {
                    tick: (tick_count % 0xFFFF_FFFF) as u32,
                    node_count: 91,
                    wave_value_sample: sample,
                });
            }

            // Emitir portal_opened cuando se detecten portales y haya cambio
            let (portal_count, indices) = {
                let dispatch_guard = tick_state.last_dispatch.read().unwrap();
                dispatch_guard
                    .as_ref()
                    .map(|d| (d.portal_count, d.portal_indices.clone()))
                    .unwrap_or((0, vec![]))
            };

            if portal_count > 0 && portal_count != last_portal_count {
                last_portal_count = portal_count;
                let _ = tick_state.tx_events.send(ServerEvent::PortalOpened {
                    indices,
                    count: portal_count,
                    tick: (tick_count % 0xFFFF_FFFF) as u32,
                });
            }
        }
    });

    // ── 11. Iniciar servidor HTTP (bloquea hasta Ctrl+C) ──
    let app = create_app(app_state);
    let listener = TcpListener::bind("0.0.0.0:8080").await?;
    println!("🌐 Servidor HTTP escuchando en 0.0.0.0:8080");

    serve(listener, app).await?;

    Ok(())
}
