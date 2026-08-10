# Memoria de Inicio Rápido - Lota Indómito

Este archivo es la memoria de inicio de sesión rápida. Cualquier IA que lo lea debe tener el contexto suficiente para continuar trabajando sin hacer preguntas básicas.

## Datos del proyecto
- **Nombre:** Lota Indómito
- **Tipo:** Juego tipo Pokémon GO ambientado en Lota, Chile.
- **Desarrollador:** Jaime Novoa Sepúlveda (INTERLOCUTOR). 
- **Cliente:** Fabiola (postulación a fondo público, 10M CLP).
- **Repositorio:** `/home/jnovoas/Proyectos/LotaIndomito/`
- **Sentinel (framework matemático base):** `/home/jnovoas/Proyectos/sentinel/me-60os-core/`

## Decisión de arquitectura del motor (Piloto B): Camino C
> Nota: esta es la arquitectura del Piloto B (motor propio), que es el CENTRO del concepto (D-014 corregida), NO R&D congelado. El teléfono (Piloto A) es la capa accesible; ver "Encuadre vigente" abajo.

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
- **ESLABÓN FALTANTE RESUELTO (2026-08-10):** `upload_and_dispatch(lane_a, lane_b, time_sec, delta_time, salto17_tick)` implementado en `LotaGpuPipeline`. Flujo: `ResonantMatrix::crystals → GpuLatticeNode::from_lanes() → VRAM → compute shader → staging readback → DispatchResult { wave_values, portal_count, portal_indices }`. 4/4 tests pasando. Integrado en `main.rs` con `ResonantMatrix` real (commits `de42f61`, `1f5e3f`).

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

## Encuadre vigente (2026-08-10, D-014 corregida) — LEER ANTES DE TRABAJAR
- **Norte del proyecto:** potenciar el turismo de Lota para **revivir el comercio local**. El juego es el medio, no el fin; el comercio revive y **autofinancia** la plataforma (etapa 2).
- **Idea fuerza:** *el mundo real maneja el juego.* Matemática soberana S60 (Sentinel), sin floats, sin Google.
- **Concepto:** evento real (cielo/hora) decide qué pasa → enjambre SOMA de NPCs simples y vivos → el jugador los caza por geolocalización en el teléfono (PWA) → encuentro en RA (gafas Meta, préstamo en sitio) que reconstruye la historia e imágenes reales de Lota. Costura de baja latencia vía carriles de la lattice. Etapa 2: avisos de comercio en RA + circuito de minerales (cobre/oro/estaño) → autofinanciamiento.
- **Expansión regional:** Lota es la prueba de concepto; el modelo se expande a Curanilahue, Lebu, Arauco y Concepción (corredor patrimonial de la zona del carbón). El motor es agnóstico de comuna: cada una aporta su contenido. Modelo regional escalable y autofinanciable por comuna.
- **Entregable de INTERLOCUTOR (~30 días):** un piloto / diseño de concepto que demuestra el diferenciador central. NO el juego completo. La fase 1 arranca después.
- **La postulación al fondo es dominio de Fabiola.** INTERLOCUTOR no se mete en su postulación. Los docs de fondo (`_analisis/08_carta_gantt_*`, `_analisis/09_presupuesto_*`, `_analisis/11_borrador_*`, `docs/propuesta-fondo.md`) son material de ella.
- **Capacidad:** INTERLOCUTOR programa desde los 9 años, autor de Sentinel, construye sistemas complejos rápido. NO recortar alcance por defecto ni tratarlo como primerizo.
- **Piloto B (motor/Sentinel) es el CENTRO del concepto, NO R&D congelado.** El teléfono (PWA, Piloto A) es la capa accesible; el motor es el diferenciador.

## Motor GPU (Piloto B) — estado: demo funcional, centro del concepto
- Eslabón faltante RESUELTO e INTEGRADO: `upload_and_dispatch` en `pipeline.rs` + integrado en `main.rs` con `ResonantMatrix` real de Sentinel (commits `de42f61`, `1f5e3f`). 4/4 tests pasando.
- El binario `lota-server` corre el ciclo completo: lattice dual-lane 91 nodos → VRAM → compute shader → readback → reporte de portales.
- El motor y los módulos Sentinel (SOMA, dual-lane, celestial, lattice) son el diferenciador del concepto. Próximos pasos del concepto: NPCs del enjambre SOMA, geofencing con R-Tree (`rstar`), encuentro RA.

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
- `CHANGELOG.md` — registro de hitos con evidencia real (commits, tests); material de portfolio. **Convención de INTERLOCUTOR: siempre CHANGELOG + `docs/decisiones.md`. Agregar una entrada al CHANGELOG con cada hito.**
- `docs/decisiones.md` — D-001 a D-014, decisiones de diseño registradas. **D-014 es el encuadre vigente.**
- `docs/estado.md` — estado vivo del proyecto.
- `docs/concepto-juego.md` — GDD completo.
- `_analisis/17_arquitectura_gpu_motor_lota.md` — guía del motor GPU (Piloto B, centro del concepto).
- `_analisis/15_inventario_sentinel_disponible_para_motor.md` — inventario detallado de Sentinel.
- `_analisis/16_vision_motor_grafico_sentinel_completo.md` — visión arquitectural actualizada.

## Cómo empezar una nueva sesión
1. Leer este archivo (el encuadre vigente está arriba).
2. Ver el estado del workstream activo en `docs/estado.md` sección 11 (maqueta piloto).
3. Verificar la build del motor si corresponde: `cd /home/jnovoas/Proyectos/LotaIndomito/rust && cargo test`.
4. El concepto usa dos niveles: teléfono (`piloto-a/`, PWA) y motor (`rust/`, Sentinel — el centro). Ver D-014 corregida en `docs/decisiones.md`.
