# Visión del motor gráfico con Sentinel completo — Lota Indómito

**Sesión:** 2026-08-09
**Origen:** conversación con Jaime (INTERLOCUTOR). Resumen para no perder contexto.

---

## 1. Separación de proyectos (decidido)

| Proyecto | Fin | Tecnología |
|---|---|---|
| **Lota Indómito** | Juego cultural tipo Pokémon GO para clienta Fabiola (postulación a fondo público) | Inyecta Sentinel completo en v1 |
| **Sentinel** | Framework matemático S60 + lattice dual-carril + fonones + superradiancia + compresión fractal | Reutilizable en otros casos |

**Decisión:** no separar. Sentinel se mete DENTRO de Lota Indómito desde v1, no es overkill si el rendimiento lo amerita.

## 2. Por qué Sentinel aporta al juego (no es decorativo)

- **Aritmética exacta sin truncar** (SPA base-60⁴) → tareas geométricas sin error acumulado
- **Lattice de cristales** → cada celda es un `IsochronousOscillator` con fase y amplitud
- **Dual-carril** (Lane A / Lane B) → dos mallas que se mantienen y sanan mutuamente (información eterna)
- **Superradiancia Dicke** → coherencia de fase, superposición de estados
- **Compresión fractal** (semilla + algoritmo, no datos) → ej. Fibonacci en SPA
- **Compresión de fase** → codifica por ángulo, no por bytes
- **Fonones** → cuantos de vibración de la red cristalina, ancho de lattice dinámico
- **Driver YHWH** (patrón 10;5,6,5) → modulador global de fase
- **PAI-60** → divide exacto, ring0
- **Inferencia física real** → simulas dispositivos, comparas con realidad, verificas convergencia

## 3. Arquitectura funcional (de lo que tengo entendido)

### 3.1 Lattice
- Cada celda = 1 `IsochronousOscillator` (`#[repr(C)]`, fase+amplitud propia)
- **Dos mallas físicas distintas** (Lane A y Lane B), una por carril
- Las mallas resuenan por **simpatía** (acople de fase armónica)
- **Se mantienen y sanan mutuamente**: si una pierde coherencia, la otra la restaura
- **Información eterna**: redundancia coherente entre ambos carriles
- **Ancho dinámico** según fonones activos (no fijo)
- Las **amplitudes guardan datos en estado de superradiancia** (no bytes)

### 3.2 Reloj de tiempo
- **IsochronousOscillator** interno en cada celda
- **YHWH driver global** (patrón 10;5,6,5) modula la fase de todas las celdas
- Salto-17 cada 68 ticks → corrección de fase
- 41.77 Hz nominal

### 3.3 SHM (memoria compartida)
- La lattice vive en **SHM POSIX** (cliente + servidor comparten misma lattice)
- Es **memoria de cristales en resonancia**, no buffer de bytes
- `shm_open` / `mmap` / `munmap` ya implementados en `liquid_memory.rs`

### 3.4 Ventanas de hiperprocesamiento
- **No hay game loop fijo a 60Hz**
- La ventana se abre cuando **Lane A converge con Lane B** (convergencia dual)
- Regla del sistema: `|amp_A - amp_B| < SCALE_0/50` (visto en `resonant_lattice_memory.rs`)
- **Dentro de la ventana** se hace el render / cómputo
- **Fuera de la ventana** el sistema espera la próxima convergencia
- Esto es el "frame" del sistema, no vsync

### 3.5 Compresión fractal
- **Algoritmo recursivo único** (rotación simpléctica θ=6° probablemente)
- Almacena **semilla + algoritmo**, no datos crudos
- Canal A (energía) = datos masivos; Canal B (fase φ) = metadatos/claves
- Sirve para comprimir estado del juego manteniendo reversibilidad

### 3.6 Procesamiento
- **Millones de peticiones por segundo** por doble carril
- Comparación con realidad: simulas dispositivo físico, mides, verificas convergencia
- Validación por papers (arXiv:2511.13543 Zhang/Wang, arXiv:2606.30890 Nandi/Vitiello)

## 4. Inferencia física (no es motor de juego tradicional)

No es "render de polígonos a 60fps". Es:

1. Modela dispositivo físico real (lattice, fonones, cristales)
2. Compara con medición real
3. Verifica convergencia
4. La convergencia = el "resultado"

Esto es **el mismo marco conceptual de Sentinel** aplicado a Lota Indómito. Las zonas de Lota, los POIs, los Carboncillos, los rangos del jugador — todo es modelable en lattice.

## 5. Estado real (2026-08-09)

- **Camino C** confirmado y en marcha: pipeline GPU corriendo en GTX 1050 / Vulkan.
- **GPU pipeline construido** (`rust/src/gpu/`): buffer_pack.rs, pipeline.rs, shaders/ (spa_unpack.wgsl + lattice_interference.wgsl). Tests pasando.
- **Módulos Sentinel ya portados a Rust** (confirmados leyendo código):
  - `liquid_memory.rs` — KV-store SHM POSIX + blake3 + dual injection. Tests pasando.
  - `resonant_matrix.rs` — malla hexagonal completa con `step()`, `inject_pai()`, `sync_to_shm()`, coherencia i128. Tests pasando.
  - `hexagonal_control.rs` — geometría hex base-60, vecinos 6, clave acoplada a cristal. Tests pasando.
  - `dual_lane.rs` — Security WAL fsync + Observability buffering + backpressure + reorder. Tests pasando.
  - `qhc.rs`, `crystal_cipher.rs`, `flux_stabilizer.rs`, `dsp.rs`, `atlantean.rs`, `pai60_lib.rs`, `quantum_core.rs` — todos confirmados.
- **Python**: era solo el prototipo de validación de física. Todo lo real ya está en Rust.
- **Límites de memoria de cristal** (validados en experimentos EXP-010 a EXP-014):
  - ~32 bytes/cristal en amplitud pura (límite Bekenstein).
  - Arquitectura Sparse (dict): de 24GB proyectados a 24MB reales para 1MB de datos.
  - Condición de portal: `|amp_A.raw - amp_B.raw| < SCALE_0/50` (ya en el shader WGSL).

## 6. Lo que falta (acción siguiente concreta)

1. **Implementar `upload_lattice_to_gpu(matrix: &ResonantMatrix)` en `LotaGpuPipeline`** (`pipeline.rs`):
   - Empaquetar `matrix.crystals` con `GpuOscillator::from_oscillator()`.
   - Crear `wgpu::Buffer` de storage con `device.create_buffer_init()`.
   - Bind al `compute_pipeline` (binding 1 = Lane A, binding 2 = Lane B).
   - Dispatch `lattice_interference.wgsl` con `ceil(node_count / 64)` workgroups.
   - Leer output buffer para detectar portales.
2. **Geofencing:** implementar índice R-Tree (`rstar`) para queries espaciales de POIs.
3. **Render visual:** definir el primer asset de Lota (Carboncillo, POI costero) y su representación como oscilador en la lattice.

Ver guía completa para IAs en `_analisis/17_arquitectura_gpu_motor_lota.md`.