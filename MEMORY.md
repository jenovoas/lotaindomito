# Memoria de Inicio Rápido - Lota Indómito

Este archivo es la memoria de inicio de sesión rápida. Cualquier IA que lo lea debe tener el contexto suficiente para continuar trabajando sin hacer preguntas básicas.

## Datos del proyecto
- **Nombre:** Lota Indómito
- **Tipo:** Juego tipo Pokémon GO ambientado en Lota, Chile.
- **Desarrollador:** Jaime Novoa Sepúlveda (INTERLOCUTOR). 
- **Cliente:** (sin info — atribución de INTERLOCUTOR, no del repo)
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

## Encuadre vigente (revisado 2026-08-10) — LEER ANTES DE TRABAJAR
- **Norte del proyecto:** Lota Indómito es una plataforma de juego geolocalizado que usa matemática soberana S60 (Sentinel), sin floats, sin Google.
- **Qué hace:** evento real (cielo/hora) → enjambre SOMA de NPCs simples y vivos → el jugador los caza por geolocalización en el teléfono (PWA) → encuentro en RA que reconstruye la historia de Lota.
- **Expansión regional:** Lota es la prueba de concepto; el modelo se expande a Curanilahue, Lebu, Arauco y Concepción (corredor patrimonial de la zona del carbón). El motor es agnóstico de comuna.
- **Entregable INTERLOCUTOR (~30 días):** piloto / diseño de concepto que demuestra el diferenciador central. NO el juego completo.
- **Piloto B (motor/Sentinel) es el CENTRO del concepto.** El teléfono (PWA, Piloto A) es la capa accesible; el motor es el diferenciador.
- **Capacidad:** INTERLOCUTOR es senior, autor de Sentinel, construye sistemas complejos rápido. NO recortar alcance por defecto ni tratarlo como primerizo.

## WEB PÚBLICA Y DEPLOY (2026-08-11) — ESTADO ACTUAL
- **URL:** https://pinguinoseguro.cl/lotaindomito/ (subruta de pinguinoseguro.cl; NO hay dominio propio todavía).
- **Repo público:** https://github.com/jenovoas/lotaindomito (jenovoas/lotaindomito). Es la vitrina de desarrollo real para Fabiola — siempre visible en nav/footer.
- **Flujo de deploy:** commit + push a main → el fan (`ssh fan`) hace `git pull --rebase` cada 1 min (timer `lotaindomito-pull.timer`) → corre `docs/_render/render-docs.py` que regenera los HTML de docs.
- **Landing:** `index.html` — dark industrial (turquesa #65dabc / dorado #D4AF37 / melocotón #F4A261), escena three.js (lattice hexagonal + portal + partículas, movida a la izquierda en desktop), capa de cristal para legibilidad, secciones: hero, proyecto, cómo funciona, IMPACTO SOCIAL (función social: turismo/comercio/datos/comunidad), pilotos A/B, galería prototipo (mockups teléfono), documentos. Logo SVG hexagonal en nav + menú hamburguesa móvil.
- **Navbar ÚNICA compartida:** fragmento `docs/_render/nav.html` (con placeholder {BASE}) → render-docs.py lo inyecta en TODOS los docs generados. `index.html`, `prototipo-stitch.html` y los docs usan la misma navbar (logo SVG, links, hamburguesa, GitHub). Al agregar una sección al nav: actualizar index.html Y nav.html (mismo orden).
- **prototipo-stitch.html:** visor de 52 pantallas Stitch (header viejo reemplazado por navbar nueva; el nav de categorías es `.cats`).
- **HTML generados (docs/*.html, README.html) están en .gitignore** — se regeneran en el fan con cada pull. Lo versionado es el generador (render-docs.py + nav.html).
- **PENDIENTE:** el §6.5 actual de la propuesta cierra el bloque "Lo que NO es el proyecto" con "No es un proyecto genérico ni simplificado para encajar en bases".
- **Regla dura:** NUNCA montos de dinero en docs del proyecto (son de la clienta). Limpiar solo líneas de Fabiola, NO eliminar documentos completos.

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

## Arquitectura de Juego: 3 capas + Game Loop (D-021, 2026-08-14)
- **Capa 1 · Simulación (Rust + S60, Piloto B):** dueña del estado de mundo. Game Loop determinista, FSM de NPCs. Emite por WebSocket: `lattice_tick`, `portal_opened`, `npc_moved`, `npc_state_changed`.
- **Capa 2 · Estado y sync (Vue/Pinia, Piloto A):** dueña del estado del jugador y caché de mundo. Recibe eventos, los empuja a `RingBuffer` (N=10), mantiene inventario/wallet offline-first. Reconnect exponencial con jitter.
- **Capa 3 · Presentación (Vue + render loop):** dibuja estado, no calcula. Usa `useGameLoop()` (rAF con pausa por `document.hidden`).
- **Regla:** la Capa 3 NO llama al backend. Si necesita datos, los lee de Pinia. La Capa 2 NO ejecuta lógica de simulación.
- **Tokens visuales centralizados** en `piloto-a/src/assets/design-tokens.css` (consumidos vía variables CSS, no hardcoded hex).
- **Componentes nuevos Piloto A:** `NpcAvatar.vue`, `BrumaCostera.vue`, `EncuentroSheet.vue`, `EncuentroPulso.vue`, `BannerIntercept.vue`.
- **Perfiles gráficos:** `full` / `lite` / `css-only` detectados automáticamente por `useGraphicsProfile()` (memoria, dpr, WebGL) y aplicados en BrumaCostera, EncuentroPulso y la landing.
- **Referencia completa:** `_analisis/26_arquitectura_game_loop_3_capas.md`.

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
