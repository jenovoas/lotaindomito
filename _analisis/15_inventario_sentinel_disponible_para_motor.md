# Inventario de Sentinel (S60) disponible para el motor de Lota Indómito

> **Documento de inventario y propuesta de integración.**
> **Destinatario:** INTERLOCUTOR (Jaime).
> **Propósito:** Mapear qué módulos de Sentinel ya resuelven necesidades del motor de juego y qué partes hay que construir desde cero.

---

## 1. Contexto del proyecto Lota Indómito y de Sentinel

**Lota Indómito.** Juego tipo Pokémon GO ambientado en Lota, Chile. Postulación a fondo público por **[monto retirado]**. Cliente: **cliente**. Plazo: **3 semanas hasta deadline** de entrega de la propuesta. La promesa de producto es una experiencia geolocalizada de captura y exploración en el borde costero de Lota, con énfasis en jugabilidad móvil, narrativa local y dinámica comunitaria en tiempo real.

**Sentinel (S60).** Framework matemático escrito en Rust, ubicado en `~/Proyectos/sentinel/me-60os-core`. Su propiedad central: **es 100% libre de `float`**, validado en runtime por 100k iteraciones. Implementa el sistema S60 (`SPA` = S60 Positional Arithmetic), donde cada número se representa como un vector de `i64` con escala sexagesimal `60^4`. Su runtime es **isomorfo a física real** — la misma aritmética produce los mismos resultados en CPU, GPU (vía pack/unpack explícito) y simulación numérica.

Sentinel **no es "otra librería de math"**. Es la fuente de aritmética sin truncado para el proyecto. Cualquier camino que use `f32`/`f64` internamente rompe la promesa de isomorfismo y abre la puerta a errores de redondeo que, en un juego donde la física debe coincidir entre cliente y servidor, son inaceptables.

**Decisión de arquitectura (Camino C).** El INTERLOCUTOR (Jaime) ha decidido: **motor gráfico propio desde cero**, con el **lattice S60 controlando TODO el cómputo** — game state, física, render, sincronización cliente-servidor. **Cero dependencias** de motores que usen `f32` internamente. Esto descarta Bevy, Fyrox, Macroquad, Unity, Godot en su forma estándar, y descarta también librerías de math como `glam`, `cgmath` o `nalgebra`.

---

## 2. ¿Qué Sentinel ya tiene y qué tendría que construir el motor?

| Necesidad del juego | Módulo Sentinel disponible |
|---|---|
| Aritmética sin truncado (vectores 3D, matrices, normales, transforms) | `spa.rs`, `spa_math.rs`, `SVector3` (`celestial.rs`) |
| Estado de jugadores en RAM compartida, sin malloc dinámico | `buffer.rs`, `liquid_memory.rs`, `QuantumCore.lattice` |
| Reloj maestro que sincroniza mundo real ↔ digital (eventos celestes, mareas, día/noche) | `IsochronousOscillator` (`isochronous_oscillator.rs`) |
| Tick a 64Hz subordinado al reloj maestro 41.77Hz con autocorrección cada 68 ticks | `QhcTensor` (`qhc.rs`) + `IsochronousClock` (`quantum_core.rs`) |
| Bus de eventos cliente↔servidor a 64 Hz (posiciones, deltas, chat) | `SOMA` (`soma_orchestrator.rs`, `soma_worker.rs`) |
| Cifrado efímero por pulso del cristal para auth de cliente | `CrystalCipher` (`crystal_cipher.rs`) |
| Estabilización de flujos (drift, jitter, posición sucia de GPS) | `FluxStabilizer` (`flux_stabilizer.rs`) |
| Path traced con coherencia de fase / tiempo | DSP pipeline `i128` + traps (`dsp.rs`) |
| Servidor dedicado de alto tick | `scheduler.rs` + `resonant_matrix.rs` |
| Cifrado de eventos sensibles en SHM | `dual_lane.rs` (WAL router) |
| **Geofencing / R-Tree** (NUEVO, no existe en Sentinel) | **Construir** con `rstar` |
| **Render GPU** (NUEVO, no existe en Sentinel) | **Construir** con WGPU |
| **Mapeo de SPA a WGSL** (NUEVO) | **Construir** adapter/empaquetador |

---

## 3. Inventario detallado de archivos Sentinel (con evidencia)

> Todos los archivos a continuación fueron leídos directamente del repo `~/Proyectos/sentinel/me-60os-core/src/`. Las descripciones, structs y firmas expuestas son literales del código, no resúmenes.

### 3.1 `spa.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/spa.rs`
- **Líneas / tamaño:** 226 líneas / ~8 KB.
- **Qué expone:**
  - `pub const SCALE_0: i64 = 12_960_000;` (equivalente a `60^4`).
  - `pub struct SPA { components: [i64; 5] }` — el número S60 como tupla de cinco enteros. Los cinco componentes codifican signo, magnitud y precisión sexagesimal posicional.
  - Constructores: `from_raw`, `from_int`, `from_decimal_for_import_only`.
  - Implementaciones de `Add`, `Sub`, `Mul`, `Div`, `Rem`, `Neg`.
  - Variantes `checked_*` que entran en `panic!` explícito ante overflow / división por cero / resultado degenerado. Esto es por diseño: en Sentinel los errores aritméticos **no se silencian**, se detienen.
  - Cero operaciones con `f32`/`f64`. Verificado por clippy lints en compile-time.
- **Para qué sirve el motor del juego:** cualquier número del juego (posición, velocidad, ángulo, tiempo, recurso, score) vive en aritmética exacta. Cliente y servidor producen el mismo resultado bit-a-bit, eliminando drift numérico entre réplicas.
- **Tests:** la suite de tests vive en la implementación `pyo3` expuesta al binding Python; no hay `#[test]` separados en este archivo.

### 3.2 `spa_math.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/spa_math.rs`
- **Líneas / tamaño:** 371 líneas / ~13 KB.
- **Qué expone:**
  - `pub struct SPAMath`.
  - Constantes S60:
    - `pub const PI: SPA = SPA { components: [..., 3;8,29,44,0] };`
    - `pub const TWO_PI: SPA = ... 6;16,59,28,0;`
    - `pub const RESONANCE_RATIO: SPA = ... 1;32,2,24;` (Plimpton 322, Fila 12).
    - `pub const OSCILLATOR_FREQUENCY_MHZ: SPA = ... 153;24;`
  - Funciones: `sin`, `cos`, `sqrt` (Newton-Raphson), `exp`, `ln`, `log2`, `log_base`.
- **Para qué sirve el motor del juego:** trigonometría CPU-side para shaders procedurales, cálculo de distancias, ángulos de cámara, rotación de sprites en CPU, y cualquier cálculo geométrico que no se quiera delegar a la GPU.
- **Tests:** `sin/cos identity`, `sqrt`, `exp_decay`, `ln` — todos **PASS** según la suite verificada.

### 3.3 `celestial.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/celestial.rs`
- **Líneas / tamaño:** 237 líneas / ~8 KB.
- **Qué expone:**
  - `pub struct SVector3 { pub x: SPA, pub y: SPA, pub z: SPA }`.
  - `pub struct SovereignOrbit` con método `calculate_keplerian_elements(...)` que implementa, en aritmética S60, las fórmulas newtonianas clásicas:
      - Energía específica: `ε = v²/2 - μ/r`
      - Semi-eje mayor: `a = -μ/(2ε)`
      - Excentricidad: `e = √(1 + 2εh²/μ²)`
      - Período orbital: `T = 2π√(a³/μ)`
  - `spherical_to_cartesian(...)` para conversión esférica → cartesiana.
- **Para qué sirve el motor del juego:** vector 3D sin floats para posiciones, normales y transforms de los assets del juego. Si el juego necesita mecánica orbital (eventos celestes que afectan el gameplay, mareas como mecánica de captura), las fórmulas newtonianas ya están portadas. Si no, `SVector3` se usa directamente como tipo de posición/movimiento.
- **Tests:** `SVector3 magnitude`, `spherical_to_cartesian polo`, `Kepler LEO`, `Kepler escape`.

### 3.4 `quantum_core.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/quantum_core.rs`
- **Líneas / tamaño:** 480 líneas / ~18 KB.
- **Qué expone:**
  - `pub struct S60PID` — controlador PID con **kernel de historia No-Markoviano**, referencia Nandi & Vitiello 2026. A diferencia de un PID clásico, cada paso de control considera el historial de la señal, no sólo el estado actual.
  - `pub struct ResonantBuffer` + `pub struct ResonantCell` + `pub struct IsochronousClock` — el reloj maestro del sistema, basado en resonancia. Es el componente que produce el tick fundamental a frecuencia natural.
  - `pub struct LiquidLattice` — lattice de memoria compartida con `shm` pointer y **amplitudes por slot** en S60 (no en bytes).
- **Para qué sirve el motor del juego:** reloj maestro del mundo, lattice con amplitudes S60 por celda (no `Vec<u8>` plano) para estado de entidades, PID para estabilizar magnitudes físicas del juego (drift de posición, jitter de input). El reloj maestro es la fuente de verdad temporal — todo lo demás se subordina a él.
- **Tests:** `pid`, `lattice roundtrip`. El archivo `SKILL.md` del repo Sentinel referencia explícitamente este módulo.

### 3.5 `isochronous_oscillator.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/isochronous_oscillator.rs`
- **Líneas / tamaño:** 209 líneas / ~7 KB.
- **Qué expone:**
  - `#[repr(C)]` `pub struct IsochronousOscillator` con campos:
    - `pub name: [u8; 32]`
    - `pub natural_frequency: SPA`
    - `pub amplitude: SPA`
    - `pub phase: SPA`
    - `pub damping_factor: SPA`
  - Es `Copy` (estructura trivial, lista para SHM).
  - Métodos: `transduce_pulse`, `apply_entropy`, `oscillate`.
- **Para qué sirve el motor del juego:** celdas de memoria con **fase resonante**. Cada entidad / recurso del juego puede modelarse como un oscilador que pulsa con su propia frecuencia, permitiendo coherencia de fase entre elementos del mundo. La representación `#[repr(C)]` permite que el oscilador viva directamente en memoria compartida POSIX.
- **Tests:** `creation`, `pulse_injection`, `oscillation`, `entropy_decay`.

### 3.6 `qhc.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/qhc.rs`
- **Líneas / tamaño:** 52 líneas / ~1.5 KB.
- **Qué expone:**
  - `pub struct QhcTensor` con:
    - `pub pattern: [u8; 4] = [10, 5, 6, 5]` — la firma QHC (Quantum Harmonic Cascade).
    - `pub correction_interval: u64 = 68` — corrección cada 68 ticks.
    - `pub correction_ns: u64 = 700_000` — 0.7 ms de corrección.
  - Métodos: `get_phase_modulation`, `calculate_drift_correction` (implementa el "Salto-17" cada 68 ticks), `apply_modulation`.
- **Para qué sirve el motor del juego:** **heartbeat del juego**. El tick fundamental del motor a 41.77 Hz se autocorrige cada 68 ticks para mantener sincronía con el reloj maestro. Es el equivalente S60 del "frame budget" tradicional, pero con corrección de drift explícita.
- **Tests:** no tiene `#[test]` separados; se valida vía integración con `IsochronousClock`.

### 3.7 `crystal_cipher.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/crystal_cipher.rs`
- **Líneas / tamaño:** 169 líneas / ~6.3 KB.
- **Qué expone:**
  - `pub struct CrystalCipher` con:
    - `crystal: Mutex<IsochronousOscillator>` — la fase osciladora bajo mutex.
    - `pub pulse: u64` — contador de pulsos.
    - `key_cache: ...` — caché de claves derivadas.
  - Cifrado: **AES-256-GCM** + **Blake3**.
  - La clave se **deriva de la fase S60** del oscilador.
  - El **NONCE se deriva del pulso** (counter).
  - **Master cycle de 68 segundos** — cada 68 s, la fase se rota y la clave cambia.
- **Para qué sirve el motor del juego:** autenticación de cliente (handshake inicial), cifrado de mensajes de gameplay, integridad de eventos sensibles. La clave que rota con la fase del cristal hace que un atacante que intercepte un mensaje no pueda descifrar los siguientes.
- **Tests:** `same_phase_same_key`, `encrypt_decrypt_roundtrip`, `pulse_rotates_key`, `different_crystal_different_key`.

### 3.8 `liquid_memory.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/liquid_memory.rs`
- **Líneas / tamaño:** 274 líneas / ~10 KB.
- **Qué expone:**
  - `pub struct LiquidMemory` con:
    - `lattice: LiquidLattice`
    - `file_table: HashMap<...>`
    - `owned_buffers: Vec<NativeShm>`
  - `pub struct NativeShm` — wrapper sobre **POSIX `shm_open` / `mmap` / `munmap`**.
  - `shm_name_for(key)` — genera nombre determinista vía **Blake3**.
  - `store` / `retrieve` con verificación de integridad Blake3.
- **Para qué sirve el motor del juego:** KV-store de estado de jugadores con respaldo en memoria compartida POSIX. Sin malloc dinámico en hot path, sin GC, sin pausas. Cada celda del juego (jugador, NPC, recurso) tiene una clave Blake3 y su payload vive en SHM.
- **Tests:** `roundtrip`, `missing_key`, `overwrite`, `large_payload`.

### 3.9 `shm_bridge.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/shm_bridge.rs`
- **Líneas / tamaño:** 142 líneas / ~4.4 KB.
- **Qué expone:**
  - `pub struct PySharedBuffer` — wrapper `pyo3` para exponer memoria compartida a Python legacy.
  - Internamente usa `shm_open` / `mmap` POSIX.
  - Métodos `read` / `write` desde y hacia Python.
- **Para qué sirve el motor del juego:** bridge con componentes Python legacy si hace falta. En Camino C, **no es estrictamente necesario**, pero queda disponible para tooling o para integraciones con simuladores existentes.
- **Tests:** no tiene `#[test]` propios; los tests viven en `lib.rs`.

### 3.10 `flux_stabilizer.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/flux_stabilizer.rs`
- **Líneas / tamaño:** 227 líneas / ~8 KB.
- **Qué expone:**
  - `pub struct FluxStabilizer` con:
    - `target_sigma: SPA`
    - `damping_factor: SPA`
    - `current_flux: SPA`
    - `history: ...`
    - `seed: u64`
    - `limit_upper: SPA`
    - `limit_lower: SPA`
  - **LCG determinista** con `magic_prime = 59;59,59` (constante S60).
  - `pseudo_flux_noise(...)` — ruido pseudo-aleatorio reproducible.
  - `stabilize(steps: u64)` — itera la estabilización.
  - `residual_drift()` — mide el drift residual.
- **Para qué sirve el motor del juego:** estabilizar datos GPS ruidosos del cliente (input crudo), normalizar posición de jugadores antes de aplicar reglas de juego, suavizar trayectorias sin introducir latencia. El LCG determinista garantiza que dos clientes con el mismo seed produzcan la misma secuencia de ruido.
- **Tests:** `noise_deterministic`, `noise_bounded`, `stabilize_converges`, `stays_in_guardrails`, `seed_cycles`, `residual_drift_small`.

### 3.11 `dsp.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/dsp.rs`
- **Líneas / tamaño:** 185 líneas / ~7 KB.
- **Qué expone:**
  - `pub struct S60DSP` con método `mul_pipeline(a: SPA, b: SPA) -> Result<SPA, DspConstraintError>`.
  - **Acumulador `i128`** — la multiplicación de dos `i64` se hace en `i128` antes de reducir, evitando overflow intermedio.
  - **Traps** (errores que detienen el cálculo, no se silencian):
    - `AccumulatorMeltdown`
    - `RegisterOverflow`
- **Para qué sirve el motor del juego:** multiplicación con verificación de overflow para matrices grandes, productos vectoriales, y cualquier cómputo donde dos `SPA` se multipliquen muchas veces seguidas (ej.: un raymarcher, un path tracer simple, una simulación de muchos cuerpos).
- **Tests:** `mul_pipeline_trivial`, `leo_momentum`, `overflow_64_trap`, `mul_wide_pipeline_handles_large`, `scale_constant`, `mul_zero`, `mul_negative`.

### 3.12 `lib.rs`

- **Ruta:** `~/Proyectos/sentinel/me-60os-core/src/lib.rs`
- **Líneas / tamaño:** 108 líneas / ~4 KB.
- **Qué expone:** punto de entrada de la librería. Declara y expone los módulos (`spa`, `spa_math`, `celestial`, `quantum_core`, `isochronous_oscillator`, `qhc`, `crystal_cipher`, `liquid_memory`, `shm_bridge`, `flux_stabilizer`, `dsp`, etc.).
  - En la cabecera del crate aparecen lints `forbid` que **bloquean en compile-time** el uso de aritmética flotante:
    - `clippy::float_arithmetic`
    - `clippy::float_cmp`
    - `clippy::cast_possible_truncation`
    - `clippy::cast_precision_loss`
  - El build es **clean sin float** — cualquier introducción accidental de `f32`/`f64` falla la compilación.

---

## 4. Reglas duras de Sentinel (a respetar en el motor)

Las siguientes restricciones **no son negociables** en Camino C. Cualquier código del motor que las viole rompe la promesa de isomorfismo con la física real.

1. **`forbid` en compile-time.** `clippy::float_arithmetic`, `clippy::float_cmp`, `clippy::cast_possible_truncation`, `clippy::cast_precision_loss`. La crate principal los marca; el motor debe hacer lo propio en su `lib.rs`/`main.rs` para no retroceder.
2. **0 FPU ops.** Validado en runtime por Sentinel con 100k iteraciones. El motor debe poder demostrar lo mismo en su suite de tests.
3. **SPA = `i64` con escala `60^4`.** Cero floats. Si necesitas un número en formato decimal "humano" como punto de entrada, usa `SPA::from_decimal_for_import_only` — esa función existe **únicamente como puente de migración**, no como vía cotidiana.
4. **`i128` como acumulador.** Las multiplicaciones intermedias se hacen en `i128`. Si hay overflow, se **atrapa** (trap explícito vía `DspConstraintError` o `panic!`), nunca se satura en silencio.
5. **Estructuras `Copy` y `#[repr(C)]` para SHM.** Cualquier dato que cruce el límite entre Rust y memoria compartida POSIX debe tener layout C estable.
6. **Licencia.** Apache 2.0 + cláusula **No Comercial** (ver `LICENSE` en el repo). El motor derivado debe respetar la misma cláusula.
7. **Patrón QHC `10;5,6,5` + Salto-17.** Corrección cada 68 ticks. Úsalo como "heartbeat" del motor de juego — es el latido fundamental sobre el que se subordinan los sub-ticks (render, física, sync).
8. **Phenomena emergence.** NO hardcodear reglas del tipo "si fase > threshold entonces portal" — deja que el fenómeno **emerge** del cálculo armónico. Aplicado al motor: NO hardcodear "si tick == 64Hz entonces render" — deja que el `IsochronousOscillator` dicte el ritmo. Si necesitas render a 60Hz, sub-multiplica dentro del tick.

---

## 5. Cómo Spike un módulo render con S60 — antes de comprometer código

El spike es **antes** de comprometer código del motor. Su objetivo: probar que la cadena SPA → pack → WGSL → GPU funciona end-to-end con un caso mínimo.

**Pasos en orden:**

1. **Crear crate nuevo `lota-engine`.** Dependencia path a `../sentinel/me-60os-core` en `Cargo.toml`. Sin dependencias de `glam`, `cgmath` o `nalgebra`. Agregar WGPU como única dependencia de render.
2. **Crear ejemplo `bin/spa_vertex_test.rs`** que:
   - Importa `SPA` y `SVector3` desde Sentinel.
   - Define 3 vértices de un triángulo en S60 (posiciones x, y, z como `SPA`).
   - Los convierte a `vec4<u32>` para WGSL — cada componente S60 se empaqueta como `u32` (signo + magnitud + escala) para que el shader lo desempate en GPU.
   - Emite un shader WGSL mínimo que toma los tres vértices y los mueve en pantalla (un `vs_main` trivial con un offset animado en CPU).
3. **Verificar el roundtrip.** `cargo run --bin spa_vertex_test`. Confirmar visualmente que el triángulo aparece y se mueve con valores consistentes con el cómputo CPU-side en S60.
4. **Misma spike con `IsochronousOscillator`.** Un segundo binario que en lugar de vértices, instancia un oscilador y usa su `phase` para modular el offset del triángulo. Esto valida que el reloj maestro puede dictar el ritmo del render.

Si los dos spikes pasan, hay base para comprometer el crate `lota-engine`. Si no, hay que iterar sobre el empaquetador SPA → WGSL antes de seguir.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| **GPU no entiende S60.** El shader tendrá que desempacar decimales S60 → `f32` para operar. | Truncar a `f32` **en el último momento**, dentro del shader, justo antes del cómputo gráfico. El estado del juego y la física se mantienen en S60 en CPU; la GPU es sólo la última milla de presentación. |
| **`cos`/`sin` Taylor converge pero consume CPU.** Para hot loop (muchos sprites, muchos frames), llamar a `SPAMath::sin` cada vez es prohibitivo. | Pre-computar tabla `sin`/`cos` con iteración Taylor al **startup** del motor, luego lookup indexado por quadrant. La tabla vive en `LiquidLattice` (memoria compartida, compartida entre procesos). |
| **SPA no representa números muy pequeños ni muy grandes.** Escala `60^4` cubre limpio `[1e-4, 1e4]`. Para astronomía o simulaciones de muchos cuerpos, queda corto. | Para esos casos, usar `mul_wide_pipeline` (`dsp.rs`) con acumulador `i128` y representación manual de exponente. Diseñar desde el inicio una variante de SPA "wide" para magnitudes extremas si el juego la necesita. |
| **QHC tick 68 ≈ 7.4 s de game-tick.** Si cada 68 ticks "avanzo el mundo", el jugador ve el juego casi congelado. | Para render GPU a 60 Hz, **sub-multiplicar dentro del tick**. El `IsochronousOscillator` puede generar interrupts a frecuencia mayor; cada interrupt es un frame de presentación, pero el estado del juego sólo avanza en el tick fundamental. Es el patrón "fixed timestep, variable render" llevado a su forma S60. |
| **`CrystalCipher` requiere Mutex sobre la fase.** Si dos ticks del juego intentan cifrar mensajes simultáneos, hay contención de lock. | **Separar cipher por cliente**, no tener uno global. Cada jugador tiene su propio `CrystalCipher` instanciado con su seed. Así no hay lock compartido. |
| **`LiquidLattice` es "sound-of-Pythony".** El `inject_dual_channel` actual chunk-a-bytes en slots de 8 bytes. Útil para I/O binario legacy, pero no óptimo para amplitudes S60. | Diseñar **lattice custom** para el juego: amplitudes S60 por slot, no chunks de bytes. El `LiquidMemory` actúa como contenedor; el layout interno es decisión del motor. Esto se decide en la spike siguiente al render. |

---

## 7. Qué NO hacer

Lista de antipatrones explícitos. Cualquiera de estos rompe Camino C.

- **NO usar `glam`, `cgmath`, `nalgebra`.** Todas son librerías de math en `f32`. No se pueden integrar limpiamente con S60 sin capas de conversión que reintroducen truncado.
- **NO usar Bevy, Fyrox, Macroquad.** Cualquier motor de juegos Rust maduro usa `f32` internamente en su ECS, su física y su math. El Camino C exige motor propio.
- **NO hardcodear "if tick == 64Hz then render".** Esa regla rompe el principio de phenomena emergence. El ritmo debe emerger del `IsochronousOscillator`. Si necesitas 60 Hz de presentación, deja que el oscilador te los dé vía interrupt — no decidas tú.
- **NO usar Unity, OpenGL directo, Vulkan directo.** Unity es `f32` end-to-end. OpenGL y Vulkan como API están bien, pero暴露 them directamente rompe la portabilidad. **WGPU sí** — es el wrapper Rust sobre Vulkan/Metal/DX12/WebGPU que mantiene layout C-friendly y permite empaquetar SPA.
- **NO clonar el lattice a la GPU como textura.** Eso duplica estado y abre drift. Mapear SHM directo vía `wgpu::Buffer::map` / `memcpy` — la GPU ve la misma memoria que la CPU, sólo cambia la interpretación.
- **NO committear nada al repo de Sentinel.** El motor es crate aparte, vive en `~/Proyectos/LotaIndomito/`. Sentinel es upstream estable; el motor lo consume como dependencia.
- **NO hacer fudge tests.** No se baja la tolerancia de un assert para que pase. Si un test falla, el cálculo está mal o la tolerancia es incorrecta. Los traps de Sentinel existen para **detener**, no para negociar.

---

## 8. Próximos pasos (ACORDAR CON INTERLOCUTOR antes de avanzar)

Los siguientes puntos **requieren decisión explícita del INTERLOCUTOR** antes de avanzar. No son técnicos solamente — algunos tocan el modelo de negocio y la arquitectura de servidor.

1. **Spike `lota-engine` con `spa_vertex_test.rs`.** Primer paso concreto. Verificar la cadena SPA → WGSL → GPU end-to-end con un triángulo mínimo. Sin este spike verde, no se compromete código del motor.
2. **Mapeo de memoria espacial.** Decidir entre R-Tree (`rstar`), grid hexagonal (potencialmente vía `hexagonal_control.rs`), o estructura ad-hoc. Esto define cómo el juego indexa entidades por posición para queries de "qué hay cerca del jugador".
3. **Diseño del lattice custom.** No usar `LiquidLattice` actual tal cual. Decidir layout: amplitudes S60 por slot, tamaño de slot, granularidad de la grid, cómo se serializan entidades complejas.
4. **Política de doble carril (Lane A físico cliente, Lane B autoridad servidor).** Definir qué eventos viven en qué carril y cómo se sincronizan con el QHC. Esto toca anti-cheat y la separación cliente-servidor.
5. **Tests.** `cargo test` para el spacer (todo lo que no es GPU), y `wgpu-test` crate para validar el render. Necesario definir fixtures: ¿se mockea WGPU o se corre contra un device real en CI?

---

*Documento elaborado por Hermes (subagente) para INTERLOCUTOR — pendiente revisión humana*