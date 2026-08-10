# Memoria de Inicio Rápido - Lota Indómito

Este archivo es la memoria de inicio de sesión rápida. Cualquier IA que lo lea debe tener el contexto suficiente para continuar trabajando sin hacer preguntas básicas.

## Datos del proyecto
- **Nombre:** Lota Indómito
- **Tipo:** Juego tipo Pokémon GO ambientado en Lota, Chile.
- **Desarrollador:** Jaime Novoa Sepúlveda (INTERLOCUTOR). 
- **Cliente:** Fabiola (postulación a fondo público, 10M CLP).
- **Repositorio:** `/home/jnovoas/Proyectos/LotaIndomito/`
- **Sentinel (framework matemático base):** `/home/jnovoas/Proyectos/sentinel/me-60os-core/`

## Decisión de arquitectura vigente: Camino C
- Motor gráfico propio desde cero.
- **Sentinel S60 (`me60os_core`) es la capa de INFRA:** aritmética S60 sin floats, GPU controller, lattice resonant, dual-lane. Se consume via `path` dependency en `rust/Cargo.toml`. NO se modifica Sentinel (es upstream estable).
- **Lota Indómito es la capa APLICACIÓN:** game state, pipeline GPU wgpu propio (`LotaGpuPipeline`), shaders WGSL propios, binario `lota-server`. Código nuevo que vive en `rust/src/`.
- **0 floats** en lógica de juego. F32 sólo dentro del shader WGSL (presentación final).
- Sin Bevy, Godot, Unity, Fyrox.
- GPU: GTX 1050 / Vulkan, corriendo.

## Estado del motor GPU (2026-08-10)
- **Pipeline GPU activo:** `rust/src/gpu/pipeline.rs` — `LotaGpuPipeline` inicializado, GTX 1050 / Vulkan detectado.
- **Buffer packer:** `rust/src/gpu/buffer_pack.rs` — `GpuSPA` (32B), `GpuVector3` (96B), `GpuOscillator` (128B), `GpuLatticeCell` (224B), `GpuLatticeNode` (272B dual-lane). 4/4 tests pasando.
- **Shaders:** `rust/src/gpu/shaders/spa_unpack.wgsl` (desempaquetado S60) y `lattice_interference.wgsl` (convergencia dual-lane `@workgroup_size(64)`).
- **Crate:** `lota_engine` (`rust/Cargo.toml`). Deps: `me60os_core` (path), `wgpu`, `bytemuck`, `anyhow`, `tokio`, `rstar`, `serde`.
- **ESLABÓN FALTANTE RESUELTO (2026-08-10):** `upload_and_dispatch(lane_a, lane_b, time_sec, delta_time, salto17_tick)` implementado en `LotaGpuPipeline`. Flujo: `ResonantMatrix::crystals → GpuLatticeNode::from_lanes() → VRAM → compute shader → staging readback → DispatchResult { wave_values, portal_count, portal_indices }`. 4/4 tests pasando. Próximo: integrar en `main.rs` con `ResonantMatrix` real.

## Módulos Sentinel ya en Rust (confirmados, no tocar)
Todos en `/home/jnovoas/Proyectos/sentinel/me-60os-core/src/`:
- `spa.rs` — `SPA { components: [i64; 5] }`, `SCALE_0 = 12_960_000`, aritmética exacta sin float.
- `spa_math.rs` — sin/cos/sqrt Newton-Raphson, PI, TWO_PI en S60.
- `celestial.rs` — `SVector3 { x: SPA, y: SPA, z: SPA }`, vector 3D sin float.
- `isochronous_oscillator.rs` — `#[repr(C)] IsochronousOscillator { natural_frequency, amplitude, phase, damping_factor: SPA }`. Es `Copy`. El átomo de la lattice.
- `quantum_core.rs` — `LiquidLattice`, `IsochronousClock`, `ResonantBuffer`, `S60PID`.
- `resonant_matrix.rs` — `ResonantMatrix { crystals: Vec<IsochronousOscillator>, ... }`. `step()`, `inject_pai()`, `sync_to_shm()`, `get_hologram_py()`. Malla hexagonal completa.
- `hexagonal_control.rs` — `HexagonalController`, `build_hex_lattice(size)`, `get_neighbors(idx)`, geometría hex base-60.
- `liquid_memory.rs` — `LiquidMemory` KV-store SHM POSIX + blake3 + dual injection. Tests pasando.
- `dual_lane.rs` — `DualLaneRouter`, `SecurityLaneCollector` (WAL fsync), `ObservabilityLaneCollector` (buffering + backpressure). Tests pasando.
- `qhc.rs` — `QhcTensor { pattern: [10,5,6,5], correction_interval: 68 }`. Heartbeat del juego.
- `crystal_cipher.rs` — AES-256-GCM + Blake3, clave derivada de fase S60, ciclo 68s.
- `flux_stabilizer.rs` — suavizado GPS/input, LCG determinista `magic_prime = 59;59,59`.
- `dsp.rs` — `mul_pipeline(a, b)` con acumulador i128, traps explícitos.
- `atlantean.rs` — `GpuController` controlador P, target 20ms (50 FPS).
- `pai60_lib.rs` — `pai60_divide(numer: SPA, denominator: u32)` división exacta.

## Próximo paso (eslabón faltante era upload_and_dispatch — ya resuelto 2026-08-10)
Integrar `upload_and_dispatch` en `main.rs` con un `ResonantMatrix` real de Sentinel:
```rust
let result = pipeline.upload_and_dispatch(&lane_a, &lane_b, tick, time_sec, delta_time, salto17_tick)?;
println!("Portales abiertos: {} en nodos {:?}", result.portal_count, result.portal_indices);
```

## Condición de portal (ya en el shader, no cambiar)
```wgsl
abs(amp_a_raw - amp_b_raw) < SCALE_0 / 50  // SCALE_0 = 12_960_000
```

## Límites físicos de la rejilla cristalina (validados en experimentos)
- ~32 bytes/cristal en amplitud pura (límite Bekenstein, EXP-010).
- Arquitectura Sparse (sólo instanciar nodos con energía > 0): de 24GB proyectados a 24MB reales para 1MB de datos (EXP-014).
- 15.03 bytes/nodo efectivo en redes grandes (EXP-013).
- Python = solo prototipos. Todo lo real está en Rust.

## Reglas duras (no negociables)
1. 0 floats en CPU. F32 sólo en shader WGSL.
2. `#[repr(C)]` en toda estructura RAM↔SHM↔VRAM.
3. No modificar el repo de Sentinel. Es upstream estable.
4. Heartbeat del juego = `QhcTensor` pattern `[10,5,6,5]`, corrección cada 68 ticks.
5. Portal dual-lane = convergencia `|amp_A - amp_B| < SCALE_0/50`.
6. Licencia: Apache 2.0 + cláusula No Comercial (heredada de Sentinel).

## Documentos clave para IAs
- `_analisis/17_arquitectura_gpu_motor_lota.md` — guía completa con diagrama mermaid, tabla de módulos, especificación del eslabón faltante.
- `_analisis/15_inventario_sentinel_disponible_para_motor.md` — inventario detallado de Sentinel.
- `_analisis/16_vision_motor_grafico_sentinel_completo.md` — visión arquitectural actualizada.
- `docs/decisiones.md` — D-001 a D-012, decisiones de diseño registradas.
- `docs/estado.md` — estado vivo del proyecto.

## Cómo empezar una nueva sesión
1. Leer este archivo.
2. Leer `_analisis/17_arquitectura_gpu_motor_lota.md`.
3. Verificar estado de la build: `cd /home/jnovoas/Proyectos/LotaIndomito/rust && cargo test`.
4. El siguiente paso concreto es implementar `upload_lattice_to_gpu()` en `rust/src/gpu/pipeline.rs`.
