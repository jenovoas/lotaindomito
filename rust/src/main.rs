// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # ⚡ LOTA INDÓMITO ENGINE - DEDICATED SERVER / GPU ENGINE ⚡
//!
//! Binario `lota-server`. Inicializa el pipeline GPU (wgpu/Vulkan),
//! construye un `ResonantMatrix` real de Sentinel, lo sube a VRAM,
//! dispatchea el compute shader de interferencia dual-lane y reporta
//! portales abiertos.

use lota_engine::gpu::pipeline::LotaGpuPipeline;
use me60os_core::atlantean::GpuController;
use me60os_core::resonant_matrix::ResonantMatrix;
use me60os_core::spa::SPA;

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
    // Esto crea diferencias de amplitud entre Lane A y Lane B,
    // que el shader evalúa para detectar portales.
    for i in 0..5 {
        lane_a.inject(i * 18, 5_000_000); // presión SPA en nodos distribuidos
        lane_b.inject(i * 18 + 9, 3_000_000); // Lane B desfasada
    }

    // ── 4. Evolucionar la lattice algunos pasos ──
    // step() propaga la onda por la malla hexagonal
    for _tick in 0..68 {
        lane_a.step();
        lane_b.step();
    }
    println!("⚙️ Lattice evolucionada 68 ticks (1 ciclo Salto-17)");

    // ── 5. Subir a VRAM y dispatchear compute shader ──
    let tick = 68u32;
    let time_sec = 1.36f32; // 68 ticks × 20ms = 1.36s

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

    // Mostrar algunos valores de onda (muestra de los primeros 10 nodos)
    let sample = result.wave_values.iter().take(10).copied().collect::<Vec<_>>();
    println!("  Wave values (10):     {:?}", sample);
    println!("═══════════════════════════════════════════════");
    println!();

    // ── 7. GpuController P-Target info ──
    let controller = GpuController::new();
    println!("⚙️ GPU Controller P-Target Latency: {} ms", controller.target_latency_msx1000 / 1000);

    // ── 8. SPA sanity check ──
    let spa_test = SPA::new(1, 30, 0, 0, 0); // 1.5 en sexagesimal
    println!("💎 SPA S60 Test Value: {:?}", spa_test);

    println!();
    println!("✅ Lota Indómito Engine — ciclo completo OK");
    Ok(())
}
