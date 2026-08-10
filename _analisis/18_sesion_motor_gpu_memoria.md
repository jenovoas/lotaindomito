# Resumen de Sesión: Motor GPU y Memoria (2026-08-09/10)

Este archivo es el resumen completo de la sesión 2026-08-09/10. Incluye qué se leyó, qué se descubrió y qué se construyó.

## 1. Qué se analizó en esta sesión
- Experimentos Python del prototipo (EXP-004, EXP-010, EXP-011, EXP-013, EXP-014) en `/home/jnovoas/Proyectos/sentinel/quantum/experiments/`.
- Módulos Rust reales de Sentinel: `liquid_memory.rs`, `resonant_matrix.rs`, `hexagonal_control.rs`, `dual_lane.rs`, `exp012_phase_compression.rs` (bin), `resonant_lattice_memory.rs` (bin), `memory_phonon_smoke.rs` (bin).
- Pipeline GPU ya construido en sesión anterior: `buffer_pack.rs`, `pipeline.rs`, shaders WGSL.

## 2. Descubrimiento clave de la sesión
El usuario aclara: **Python era solo el prototipo de validación de física. Todo lo real ya está portado a Rust en Sentinel.** Esto cambia el panorama completamente: no hay que "portar" los experimentos Python, hay que **conectar** los módulos Rust existentes con el pipeline GPU de Lota.

## 3. Lo que confirman los experimentos Python (física validada)
- **EXP-004:** Un solo cristal S60 puede almacenar datos como amplitud (codificación exacta BigInt→S60). Requiere damping=0 (superconductividad). ~32 bytes límite físico.
- **EXP-010:** Límite de Bekenstein: ~32-40 bytes/cristal en amplitud pura. Sobre 100 bytes la amplitud supera 10^80 (límite cosmológico). Solución: distribuir en red.
- **EXP-011:** Red distribuida 91 nodos = 1KB con integridad 100%. 15-16 bytes/nodo efectivo. Amplitud máxima < 10^41 (segura). Arquitectura hex rings=5.
- **EXP-013:** 70k nodos en Python = 1MB almacenado. Cuello de botella: estabilización Python 2s/ciclo. Conclusión del paper: necesita GPU o Rust.
- **EXP-014:** Arquitectura Sparse (solo nodos con energía > 0 en RAM): 24GB proyectados → 24.24MB reales. 1000x mejora. Esta optimización ya está implícita en `LiquidMemory` (HashMap en vez de Vec).

## 4. Lo que confirman los módulos Rust de Sentinel
- `resonant_matrix.rs`: malla hexagonal completa con `step()` (propagación energía), `inject_pai()` (división exacta PAI-60), `sync_to_shm()` / `load_from_shm()` (hot reload SHM), `measure_coherence_py()` (acumulador i128 para redes grandes), `get_hologram_py()` (retorna `Vec<(usize, i64, i64)>` amp+fase de cada nodo). Tests pasando.
- `hexagonal_control.rs`: `build_hex_lattice(size)` genera coordenadas axiales (q, r). `get_neighbors(idx)` retorna índices de los 6 vecinos. `compute_crystal_coupled_key(energy_raw, tick)` deriva clave dinámica base-60 acoplada al cristal. Inicializa fases con Salto-17: `phase[n] = (n * 17) % 60`.
- `dual_lane.rs`: `DualLaneRouter::classify_event()` separa por source/labels/contenido. `SecurityLaneCollector::emit_immediate()` WAL fsync síncrono (<10ms target). `ObservabilityLaneCollector::emit_buffered()` con backpressure y reordenamiento por timestamp. Tests 100%.
- `liquid_memory.rs`: `store(key, data)` → SHM POSIX + blake3 hash de integridad + inyección dual a LiquidLattice. `retrieve(key)` → lee SHM + verifica hash. `shm_name_for(key)` = `/liquid_{blake3[:16]}`. `MIN_DATA_LEN = 512` bytes padding mínimo. Tests 100%.
- `bin/resonant_lattice_memory.rs`: doble malla Lane A + Lane B en SHM. Bombeo QHC 60 ticks. Portal = `abs_diff(raw_a, raw_b) <= SCALE_0/50`. Compresion fractal via semilla. Corriendo.

## 5. Conexión arquitectural (el insight central de la sesión)
Los 4 campos de `IsochronousOscillator` (`natural_frequency`, `amplitude`, `phase`, `damping_factor: SPA`) mapean **exactamente** a los 4 campos de `GpuOscillator` que ya construimos. No hay adaptación, es una conversión directa campo a campo vía `GpuSPA::from_spa()`. El eslabón faltante es solo "empaquetar + subir a VRAM + dispatch".

## 6. Documentación creada en esta sesión
- `_analisis/17_arquitectura_gpu_motor_lota.md` — guía completa nueva.
- `docs/decisiones.md` — D-011 y D-012 agregadas.
- `_analisis/16_vision_motor_grafico_sentinel_completo.md` — secciones 5 y 6 actualizadas.

## 7. Próximos pasos (en orden)
1. **`upload_lattice_to_gpu(matrix: &ResonantMatrix)` en `pipeline.rs`** — el único eslabón faltante para tener el primer dispatch GPU con datos reales de Sentinel.
2. **Geofencing:** índice R-Tree con `rstar` para queries de POIs cercanos al jugador.
3. **Primer asset visual:** definir Carboncillo o POI costero como `IsochronousOscillator` con su frecuencia natural y su posición S60 en el mapa de Lota.
