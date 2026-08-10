// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # ⚡ LOTA INDÓMITO ENGINE - DEDICATED SERVER / GPU ENGINE ⚡

use lota_engine::gpu::pipeline::LotaGpuPipeline;
use me60os_core::atlantean::GpuController;
use me60os_core::spa::SPA;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();

    println!("⚡ Inicializando Lota Indómito Engine (Camino C)...");
    
    // Probar inicialización de GPU pipeline
    match LotaGpuPipeline::new().await {
        Ok(pipeline) => {
            println!("🟢 GPU Pipeline inicializado correctamente!");
            println!("🎮 Info: {}", pipeline.get_gpu_info());
        }
        Err(err) => {
            println!("⚠️ Advertencia: No se pudo abrir backend GPU nativo (usando CPU fallback): {}", err);
        }
    }

    let controller = GpuController::new();
    println!("⚙️ GPU Controller P-Target Latency: {} ms", controller.target_latency_msx1000 / 1000);

    let spa_test = SPA::new(1, 30, 0, 0, 0); // 1.5 en sexagesimal (1;30,0,0,0)
    println!("💎 SPA S60 Test Value: {:?}", spa_test);

    Ok(())
}
