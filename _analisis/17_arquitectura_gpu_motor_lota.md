# Documento de Arquitectura: Motor Gráfico Lota (GPU)

**Fecha:** 2026-08-09 (actualizado 2026-08-10)
**Estado:** Motor con demo funcional (ciclo completo probado). Es el centro del concepto (D-014 corregida); el teléfono (Piloto A) es la capa accesible.
**Proyecto:** Lota Indómito
**Autor/Desarrollador:** Jaime Novoa

## 1. Resumen Ejecutivo
Este documento define la arquitectura técnica del motor de juego a medida para Lota Indómito, construido en Rust (Camino C) sin utilizar engines externos (ni Bevy, ni Godot). El motor opera bajo un paradigma estricto donde **cero números de punto flotante** (floats) son permitidos en la lógica de negocio; toda la simulación de estado, física, físicas de red y sincronización se controla mediante aritmética exacta S60 provista por `me60os_core` (Sentinel). Los únicos floats del sistema se originan y consumen exclusivamente dentro del shader WGSL en la GPU durante la fase de "última milla" de presentación visual.

## 2. Diagrama de Arquitectura (Flujo de Datos)

```mermaid
flowchart TD
    subgraph RAM / SHM (Cero Floats)
        A[ResonantMatrix / LiquidMemory] -->| crystals: Vec<IsochronousOscillator> | B(Lógica de Juego S60)
        B --> C{LotaGpuPipeline}
    end

    subgraph CPU-GPU Bridge (buffer_pack.rs)
        C -->|GpuOscillator::from_oscillator| D[Empaquetado Binario: GpuOscillator]
        D -->|wgpu::BufferInitDescriptor| E[wgpu Storage Buffer]
    end

    subgraph GPU VRAM (wgsl)
        E --> F[lattice_interference.wgsl]
        F -->|spa_raw_to_f32| G[Cómputo en Float32]
        G --> H{Detección de Convergencia}
        H -->|amp_A - amp_B < SCALE_0/50| I[Output Buffer: Flag Portal]
    end

    subgraph Readback
        I -->|tokio / async| C
        C -->|Actualización| A
    end
```

## 3. Módulos de Sentinel (`me60os_core`) Críticos para el Motor
Todos los componentes residen en `/home/jnovoas/Proyectos/sentinel/me-60os-core/src/`.

| Módulo | Struct/Función clave | Para qué sirve en Lota |
|---|---|---|
| `spa.rs` | `struct SPA { components: [i64; 5] }`, `SCALE_0 = 12_960_000` | Aritmética exacta sin float. |
| `spa_math.rs` | `SPAMath::sin`, `cos`, `sqrt` (Newton-Raphson), `PI`, `TWO_PI` | Trigonometría CPU-side. |
| `celestial.rs` | `struct SVector3 { x: SPA, y: SPA, z: SPA }` | Vector 3D sin float. |
| `isochronous_oscillator.rs` | `#[repr(C)] struct IsochronousOscillator` (natural_frequency, amplitude, phase, damping_factor: SPA) | Celdas de lattice, estado de entidades. Es `Copy`. |
| `quantum_core.rs` | `struct LiquidLattice`, `IsochronousClock`, `ResonantBuffer`, `S60PID` | Lattice de memoria, reloj maestro, PID de control. |
| `resonant_matrix.rs` | `struct ResonantMatrix { crystals: Vec<IsochronousOscillator>, ... }` | Malla hexagonal completa con `step()`, `inject_pai()`, `stabilize_py()`, `sync_to_shm()`, `get_hologram_py()`. |
| `hexagonal_control.rs` | `struct HexagonalController`, `build_hex_lattice(size)`, `get_neighbors(idx)`, `compute_crystal_coupled_key(energy, tick)` | Geometría hex base-60, vecinos, clave cifrado. |
| `liquid_memory.rs` | `struct LiquidMemory { lattice, file_table, owned_buffers }` | KV-store con SHM POSIX + blake3. |
| `dual_lane.rs` | `DualLaneRouter`, `SecurityLaneCollector` (WAL fsync), `ObservabilityLaneCollector` | Doble carril, audit trail, anti-cheat. |
| `qhc.rs` | `struct QhcTensor { pattern: [10,5,6,5], correction_interval: 68, correction_ns: 700_000 }` | Heartbeat del juego, corrección cada 68 ticks. |
| `crystal_cipher.rs` | `struct CrystalCipher` | Auth de cliente, cifrado de eventos (AES-256-GCM + Blake3, clave derivada de fase S60). |
| `flux_stabilizer.rs` | `struct FluxStabilizer`, `stabilize(steps)`, `residual_drift()` | Suavizado GPS, normalización input jugador. LCG determinista (59;59,59). |
| `dsp.rs` | `S60DSP::mul_pipeline(a, b) -> Result<SPA, DspConstraintError>` | Acumulador i128 para multiplicaciones seguras, matrices, raymarcher. |
| `atlantean.rs` | `struct GpuController` | Controlador P, target 20ms (50 FPS), ajuste batch dinámico para render GPU. |
| `pai60_lib.rs` | `pai60_divide(numerator: SPA, denominator: u32) -> Option<SPA>` | División exacta S60 sin float. |

## 4. Estructura Construida en Lota Engine (`rust/`)
El motor en Rust está ubicado en `/home/jnovoas/Proyectos/LotaIndomito/rust/`.

*   **`Cargo.toml`**: `lota_engine`. Dependencias configuradas: `me60os_core` (vía path a sentinel), `wgpu`, `bytemuck`, `anyhow`, `tokio`.
*   **`src/gpu/buffer_pack.rs`**: Define y ejecuta la conversión de los structs de S60 en distribuciones binarias (align/pack) aptas para la GPU.
    *   `GpuSPA` (32 bytes): `components: [i32; 4]`, `c4: i32`, `_pad0: i32`, `raw_lo: u32`, `raw_hi: i32`.
    *   `GpuVector3` (96 bytes): Tres `GpuSPA`.
    *   `GpuOscillator` (128 bytes): Cuatro `GpuSPA` (frecuencia, amplitud, fase, amortiguación).
    *   `GpuLatticeCell` (96+64+pad bytes): `GpuVector3` + `GpuOscillator` + `id: u32`.
    *   Aprobado el test unitario `test_gpu_spa_alignment` asegurando `size_of`.
*   **`src/gpu/pipeline.rs`**:
    *   `struct GlobalUniforms { time_sec: f32, delta_time: f32, node_count: u32, salto17_tick: u32 }`.
    *   `struct LotaGpuPipeline { instance, adapter, device, queue, compute_pipeline, controller: GpuController }`.
    *   El método asíncrono `LotaGpuPipeline::new()` inicializa exitosamente en la NVIDIA GTX 1050 (backend Vulkan).
    *   Layout de bindings definido: Binding 0 = Uniform (Global), Binding 1 = Storage (Lane A), Binding 2 = Storage (Lane B).
*   **`src/gpu/shaders/spa_unpack.wgsl`**: Provee decodificación en "última milla" `spa_raw_to_f32(raw_lo, raw_hi)` y `spa_components_to_f32(c0..c4)` convirtiendo representaciones exactas a flotantes puramente para rendering.
*   **`src/gpu/shaders/lattice_interference.wgsl`**: Shader de cómputo con un `@workgroup_size(64)` en el entry point `main`. Detecta el umbral de convergencia `|amp_A.raw - amp_B.raw| < SCALE_0 / 50` y determina un estado de "portal", exportándolo al buffer.

## 5. El Eslabón Faltante: `upload_lattice_to_gpu()` — ✅ RESUELTO (2026-08-10)

> **Estado:** implementado como `upload_and_dispatch(lane_a, lane_b, tick, time_sec, delta_time)`
> en `rust/src/gpu/pipeline.rs` (commits `de42f61`, integrado en `main.rs` en `1f5e3f`),
> usando `GpuLatticeNode` (272 bytes, dual-lane) en lugar del empaquetado simple de un
> solo carril. Flujo completo operativo: `ResonantMatrix::crystals → GpuLatticeNode::from_lanes()
> → VRAM → lattice_interference.wgsl → staging readback → DispatchResult { wave_values,
> portal_count, portal_indices }`. 4/4 tests pasando. La especificación original se conserva
> abajo como referencia histórica.

### Especificación técnica requerida:
Se debe crear el método `upload_lattice_to_gpu(&self, matrix: &ResonantMatrix) -> Result<(), anyhow::Error>` (o equivalente funcional con acceso a estado interno).

**Flujo interno a implementar:**
1.  Iterar sobre `matrix.crystals: Vec<IsochronousOscillator>`.
2.  Mapear cada `IsochronousOscillator` utilizando el empaquetado definido en `GpuOscillator::from_oscillator(&osc)` (`buffer_pack.rs`).
3.  Recolectar el resultado en un vector contiguo en memoria (`Vec<GpuOscillator>`).
4.  Castear el vector de salida a su representación binaria pura empleando `bytemuck::cast_slice`.
5.  Actualizar o crear un buffer de almacenamiento en el device WGPU (`wgpu::util::DeviceExt::create_buffer_init` o escribiendo sobre uno persistente mediante `queue.write_buffer`).
6.  Ejecutar un dispatch (invocar el compute pass) del shader `lattice_interference.wgsl` utilizando la cantidad correcta de workgroups considerando el `node_count` y un `workgroup_size(64)`.
7.  Configurar un pass para leer de regreso (readback) el buffer de salida/flags donde el shader comunica que un "portal se abrió" (detectó convergencia `SCALE_0/50`).
8.  En el lado CPU, el flag recibido influye el estado del motor actualizando la lógica del juego S60.

## 6. Reglas Duras (No Negociables)
El incumplimiento de cualquiera de estas reglas rompe la arquitectura del sistema.

1.  **CERO floats en lógica del juego (CPU)**: Absolutamente ningún `f32` o `f64` existirá o procesará lógica fuera de WGSL. F32 es válido SOLO y EXCLUSIVAMENTE dentro del shader en la GPU (para presentación/render de última milla).
2.  **`forbid(clippy::float_arithmetic)`** se mantiene activo y estricto en el crate `me60os_core`.
3.  **Alineación de Memoria Garantizada**: Cualquier estructura (`struct`) que pase a través del flujo RAM ↔ SHM ↔ VRAM debe llevar explícitamente `#[repr(C)]`.
4.  **Criterio de Interferencia Dual-Lane**: El portal dimensional del juego únicamente se considera abierto (activa su flag) cuando la convergencia exacta satisface: `|amp_A.raw - amp_B.raw| < SCALE_0 / 50`.
5.  **Aislamiento del Repositorio Core**: **NUNCA** escribir o commitear código al repositorio de Sentinel (`/home/jnovoas/Proyectos/sentinel/`). El desarrollo del motor sucede íntegramente dentro de `~/Proyectos/LotaIndomito/`.
6.  **Heartbeat QHC Determinístico**: El compás del motor está gobernado exclusivamente por la tensor `QhcTensor` con patrón (10;5,6,5). La corrección o tick principal sucede rigurosamente cada **68 ticks**.

## 7. Próximos Pasos (actualizado 2026-08-10)
1.  ✅ **Implementar `upload_lattice_to_gpu`** — resuelto como `upload_and_dispatch` (ver sección 5).
2.  ✅ **Configurar el Readback Async** — resuelto: staging readback con mapeo async en `pipeline.rs`.
3.  ✅ **Probar el Pipeline Completo End-to-End** — `main.rs` corre el ciclo completo con `ResonantMatrix` real (91 nodos dual-lane, 68 ticks, reporte de portales).
4.  **Siguiente (cuando se retome el Piloto B, post-maqueta según D-014):** geofencing con R-Tree (`rstar`) y primer asset visual como `IsochronousOscillator`.
