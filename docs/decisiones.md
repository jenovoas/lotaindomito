# Decisiones del proyecto Lota Indómito

Registro de decisiones tomadas. **Fecha + decisión + razón + contraparte analizada.**

---

## 2026-08-09

### D-001 · Sync bidireccional con Drive para LotaIndomito
- **Decisión:** usar el mismo patrón que `micellia` (skill `backup/rclone-drive-sync`).
- **Componentes:**
  - `rclone copy` inicial (subida segura, sin borrado).
  - `rclone bisync` autocurable con systemd user service.
  - `inotifywait -t 300` para sync casi instantáneo + pull periódico cada 5 min.
- **Razón:** la clienta (CLIENTA) sube archivos (correcciones, audios, fotos) y revisa avances sin tener que aprenderse nada.
- **Filtros activos:** excluye `.ogg`, `.venv`, `node_modules`, `.next`, `__pycache__`, `.git`, `.hermes/cache`, y la carpeta `stitch_*` (es estática y pesa).
- **Reversible:** sí. `systemctl --user stop lota-indomito-live.service` y se apaga.
- **Estado actual (2026-08-09):** operativo, 18 archivos sincronizados, prueba en vivo con `.probe.txt` exitosa.

---

### D-002 · Transcripción local con faster-whisper
- **Decisión:** usar `faster-whisper` modelo `small` int8, CPU, sin API.
- **Razón:** audios cortos (total ~6 min en 9 archivos), no amerita costo de API. Cero cuota.
- **Contraparte analizada:** OpenAI Whisper API (mejor calidad pero $$), Nous STT (no verificado si está en plan).
- **Reversible:** sí, si los audios crecen o la calidad no alcanza, subir a `medium` o `large-v3` local, o pasar a API.

### D-002 · Memoria operativa en `docs/` separada de `_analisis/`
- **Decisión:** crear `docs/estado.md` para memoria viva del proyecto.
- **Razón:** INTERLOCUTOR explícito en MEMORY.md: "a mí siempre se me olvida, dejar doc". `_analisis/` queda para análisis del prototipo Stitch, `docs/` para procedimientos y estado.
- **Contraparte:** mezclar todo en `_analisis/` (rechazado — confunde búsqueda).

### D-003 · Español chileno obligatorio en redacción
- **Decisión:** regla dura. Ningún argentinismo en docs ni respuestas.
- **Razón:** INTERLOCUTOR me lo ha pedido 5+ veces en sesiones. Tengo el patrón metido en el modelo y se desliza solo.
- **Contraparte:** dejarlo libre (rechazado — falla seguro).
- **Mitigación:** detector regex guardado en `procedimientos.md`. Memoria persistente MEMORY.md lo bloquea entre sesiones.

---

### D-003 · Event Engine (ejemplo: celestial.rs) — Sincronización Eventos Digitales ↔ Reales
- **Decisión:** Registrar el concepto de sincronización de eventos digitales con eventos del mundo real (ejemplo en Rust: `celestial.rs`) como línea de investigación e I+D.
- **Razón (aclarada por INTERLOCUTOR):** Idea conceptual para sincronizar la lógica in-game con eventos del mundo real (horarios, mareas, ciclos solares/lunares, iluminación ambiental de Lota y eventos comunitarios en vivo).
- **Estado (2026-08-09):** **Idea en estudio (I+D).** No bloquea el MVP y se evaluará para fases futuras.

---

### D-004 · Entregable para el fondo = propuesta + maqueta + demo de interfaz
- **Decisión:** lo que se entrega a fines de agosto es la propuesta escrita (memoria, alcance, presupuesto, Carta Gantt) + el prototipo Stitch como maqueta navegable + una demo jugable solo de interfaz (sin servidor).
- **Razón:** los audios de CLIENTA apuntan a "presentar algo sólido en una etapa bien primaria". Con 3 semanas hasta el cierre, un producto corriendo con servidor no es realista ni necesario para postular.
- **Contraparte analizada:** MVP corriendo con servidor completo (rechazado — consume las 3 semanas en código y no deja tiempo para la propuesta escrita, que es lo que evalúa el fondo).
- **Reversible:** sí. Si el fondo exige producto funcional, la demo de interfaz es la base del piloto.

### D-005 · Alcance del piloto = lean (doc 04), sin 3D ni minijuegos
- **Decisión:** si se gana el fondo, el MVP a construir con los 10M CLP es el del doc 04: mapa + 3-5 POIs + check-in (foto/QR) + insignias + reportes ciudadanos + panel municipal. Three.js/R3F, personajes 3D, minijuegos y Carboncillos con canje comercial quedan para fase 2.
- **Razón:** el MVP del GDD (mapa 3D + 2 personajes + 2 minijuegos + pasaporte) es un build de 2-3 meses que no calza en 10M CLP. El piloto lean sí calza en 3-4 semanas de desarrollo.
- **Contraparte analizada:** MVP del GDD completo (rechazado para esta etapa — se retoma si se adjudica el Fondo del Patrimonio de 15-20M).
- **Nota:** la sección 8 del GDD (`docs/concepto-juego.md`) describe el MVP 3D y queda como visión de fase 2; INTERLOCUTOR la está editando.
- **Estado (2026-08-09, tarde):** congelada — esta configuración pasa a ser la **Opción A** del menú para Fabiola (D-008). Pendiente de su elección.

### D-006 · Servidor Fase 1 = Python FastAPI
- **Decisión:** el servidor del piloto se escribe en Python con FastAPI + Pydantic (OpenAPI/Swagger automático).
- **Razón:** velocidad de desarrollo con plazo apretado; validación automática de datos geográficos y reportes.
- **Contraparte analizada:** Node.js Fastify + TypeScript (alternativa viable, un solo lenguaje de interfaz y servidor — se descarta por ahora pero no se quema).
- **Reversible:** sí, antes de escribir el servidor.
- **Estado (2026-08-09, tarde):** congelada — forma parte de la **Opción A** del menú para Fabiola (D-008). Si Fabiola elige la Opción B, el servidor pasa a ser Rust (Axum + PostGIS).

### D-007 · Interfaz = React 18 + Vite + TypeScript
- **Decisión:** la app (y la demo de postulación) se construye con React 18 + Vite + TypeScript.
- **Razón:** análisis comparativo en `_analisis/05_analisis_tecnologias_disponibles.md`. Si la fase 2 incorpora Three.js vía React Three Fiber, React queda amarrado de todas formas.
- **Contraparte analizada:** Svelte (menor ecosistema 3D declarativo) y Vue 3 + TresJS (envoltorio inmaduro) — ambas descartadas.
- **Nota:** el doc 04 queda actualizado con esta decisión.
- **Estado (2026-08-09, tarde):** congelada — forma parte de la **Opción A** del menú para Fabiola (D-008). Pendiente de su elección.

---

### D-008 · La pila técnica del juego la elige Fabiola de un menú de opciones
- **Decisión:** preparar documento con opciones tecnológicas para que Fabiola (CLIENTA) elija. Configuración actual del menú:
  - **Opción A — Aplicación web progresiva:** la de los docs 04/05 y decisiones D-005..D-007 (React + MapLibre + FastAPI + PostGIS; GPS en celulares desde el día uno).
  - **Opción B — Videojuego Rust multiplataforma + servidor propio:** motor Bevy (ejecutable de escritorio Win/Mac/Linux + versión WASM en la página web), servidor Rust (Axum + PostgreSQL/PostGIS), modo virtual (teletransporte) para la demo; GPS real en celulares en fase 2.
- **Razón:** INTERLOCUTOR (2026-08-09): "al menos esa tiene que ser una de las opciones que podemos darle a elegir a Fabiola". La pila técnica es decisión de la clienta, no solo técnica.
- **Contraparte analizada:** decidir la pila técnica solo técnicamente y presentar una única opción (rechazado — Fabiola decide qué producto quiere).
- **Documento:** `_analisis/10_opciones_tecnologicas_para_clienta.md`.

---

### D-009 · Autorización de uso de celestial.rs/py en Lota Indómito
- **Decisión:** se autoriza el uso del código de `celestial.rs` y `celestial_navigation.py` (Apache 2.0 + cláusula No Comercial, autoría de Jaime Novoa Sepúlveda) dentro del proyecto Lota Indómito.
- **Razón:** INTERLOCUTOR (2026-08-09) es el autor del código y resuelve la cláusula. Lota Indómito es un proyecto financiado con fondos públicos, no comercial.
- **Atribución obligatoria:** mantener en todo el código derivado el encabezado original: "Autor: Jaime Novoa Sepulveda — Todos los derechos reservados. Licencia: Apache 2.0 + Cláusula No Comercial".
- **Reversible:** no aplica — la autorización es irrevocable por ser el autor.

### D-010 · Lota Indómito integra módulos matemáticos del core S60 de Sentinel (celestial como caso de uso)
- **Decisión:** el sistema celestial de Sentinel (código en `sentinel/me-60os-core/src/celestial.rs` y `sentinel/quantum/celestial_navigation.py`, diseño en `~/Proyectos/PersonalVault/Simulacion/navegacion_estelar.md`) se incorpora al proyecto Lota Indómito. **Lota Indómito es un cliente de Sentinel**: aplica módulos del core soberano de Sentinel a un caso de uso de patrimonio cultural.
- **Contexto del proyecto Sentinel** (validado con lectura de `sentinel/docs/00_fundamentos/MODULOS_SENTINEL.md` y `MANIFESTO_ARQUITECTURA_SENTINEL_Y_MATEMATICA_ESPACIAL.md`):
  - Sentinel es un sistema implementado, en producción y financiado. Corre con 7 daemons activos en host Fan (`sentinel-cortex`, `sentinel-gamma-watchdog`, `sentinel-hex-daemon`, `sentinel-pai-neural`, `sentinel-qhc-agent`, `sentinel-vid-agent`, `sentinel-adm-agent`), rejilla dinámica de 67.951 nodos, exportación continua a Prometheus/Grafana. Matemática espacial en base-60 (S60, escala 60⁴ = 12.960.000), runtime Rust nativo, 0 floats. Claims patentables validados, papers externos (arXiv + Mansfield & Wildberger 2017 sobre Plimpton 322), 78 papers indexados, lattice hexagonal de 91 nodos, osciladores isocrónicos, eBPF LSM, escudos MHD. Valoración: $32-58M corto plazo, $161B-253B+ visión 20 años.
  - El módulo celestial es parte del core soberano, no un adorno. Su matemática Kepleriana en S60 alimenta la pentaresonancia del sistema (ver `orbital_ascent.rs`, marcado como "MUSEO DE ESTUDIO" — la dinámica orbital real está acoplada a `LiquidLattice` / `ResonantBuffer` / `soma_orchestrator`).
- **Lo que el código implementa** (lectura de `celestial.rs`):
  - **`SVector3`**: vector 3D en SPA, parte del core S60. Operaciones exactas sin redondeo flotante (protocolo Yatra).
  - **`SovereignOrbit::calculate_keplerian_elements`**: mecánica orbital Newtoniana Kepleriana en S60 puro (ε = v²/2 − μ/r, a = −μ/(2ε), h = r·v, e = √(1 + 2εh²/μ²), T = 2π·√(a³/μ)). Validado contra base de conocimiento Newton-Kepler.
  - **`spherical_to_cartesian`**: RA/Dec → vector unitario cartesiano, trigonométrica exacta vía `SPAMath::cos`/`sin` (series de Taylor en base 60).
  - **Tests** que pasan: Pythagoras 3-4-5, polo norte, LEO circular, escape.
  - **Nota explícita del código:** la cáscara de estudio (RoyalStar, catálogo Plimpton, precesión, astrolabio de triangulación estelar) está en Python (`celestial_navigation.py`); la función matemática determinista se replica en Rust.
- **Lo que el sistema completo hace** (Python):
  - **`SovereignAstrolabe`**: catálogo soberano de las 4 Estrellas Reales (Aldebarán, Régulo, Antares, Fomalhaut) con coordenadas RA/Dec J2000 y vectores unitarios precalculados.
  - **`get_stellar_fix_pure`**: validación de unitariedad.
  - **`calculate_triangulation_error`**: error medio contra catálogo.
  - **`calculate_procession_offset`**: corrección por precesión (72 años = 1 grado).
- **Lo que aporta a Lota Indómito** (cliente de Sentinel):
  - **Sincronización con eventos celestes reales sobre Lota** (sin cámara, sin internet, sin GNSS): la mecánica Kepleriana + trigonometría esférica en S60 calculan, dada la fecha, hora y latitud de Lota (-37.09, -73.16), qué cuerpos están visibles sobre el horizonte (Luna, planetas, Estrellas Reales, fase lunar). Cálculo determinista puro, reproducible bit a bit.
  - **Capa base de soberanía criptográfica:** matemática soberana en base-60. Las posiciones celestes son matemáticamente derivables de fecha/hora/lugar — no spoofeables (las estrellas no se pueden falsificar con SDR como el GPS).
  - **Independencia de infraestructura externa:** el sistema funciona offline, sin red, sin GNSS.
  - **Diferenciador único:** "juego con matemática soberana base-60, sin Google, sin decimales flotantes, sincronizado con cielo real" — narrativa potente para la propuesta al fondo y la comunicación pública.
  - **Integración con la pentaresonancia del sistema:** los osciladores isocrónicos y la pentaresonancia de Sentinel usan la misma matemática Kepleriana. En Lota Indómito, esto puede dar coherencia temporal sin deriva de fase acumulada (problema típico con floats).
- **Lo que el sistema NO es en el piloto de Lota Indómito:**
  - El sistema no reemplaza al GPS del celular como fuente práctica de lat/lon del peatón. La latitud/longitud del jugador sigue siendo del navegador (Opción A) o del GNSS del celular (fase 2 de Opción B).
  - El sistema no es un observador óptico (no usa cámara). El cálculo de eventos celestes es matemático puro, no observación.
- **Para el piloto:**
  - Reutilizar el módulo de efemérides (mecánica Kepleriana + trigonometría esférica) del core S60, en Rust, respetando protocolo Yatra (sin float en el core).
  - Si se requiere catálogo soberano de Estrellas Reales en Rust, migrar `SovereignAstrolabe` de Python a Rust (manteniendo pureza Yatra).
  - El Event Engine en vivo (qué Estrella Real está visible sobre Lota AHORA) es el entregable diferenciador para el fondo.
- **Lo que se decide a futuro** (post-adjudicación, según interés de Fabiola):
  - Mecánica opcional de avistamiento de Estrellas Reales en la Ruta Costera nocturna usando cámara del celular (fase 2).
  - Catálogo ampliado (más estrellas, cuerpos del sistema solar, eventos de alineación) si el proyecto crece.
- **Estado del upstream:** Sentinel implementado, en producción, financiado (7 daemons activos en Fan). Lota Indómito es cliente de Sentinel: aplica los módulos del core.
- **Nota:** la autorización legal de uso está en D-009. La matemática SPA exige protocolo Yatra (sin float, sin random, sin numpy en el core) en los módulos derivados. La eBPF de Sentinel detecta y bloquea syscalls float en tiempo de ejecución — el respeto del candado Yatra no es opcional.

---

### D-010-A · Módulos del framework Sentinel identificados para integrar al juego (rol específico propuesto, pendiente confirmación)

**Contexto:** INTERLOCUTOR (2026-08-09) declara: "utilizaré varios módulos para el juego que ya tengo creados, lattices, MHD, memorias de cristales, reloj de cristal para sincronía, mycnet para HA y clustering y sincronización de baja latencia". Lota Indómito es cliente de Sentinel: aplica los módulos del core matemático S60 al juego.

**Módulos identificados del framework Sentinel (fuentes verificadas):**

| Módulo | Qué es (validado contra docs reales) | Rol propuesto en el juego | MVP / Fase posterior |
|---|---|---|---|
| **Celestial** (`celestial.rs`, `celestial_navigation.py`) | Mecánica Kepleriana S60 + catálogo de 4 Estrellas Reales + sincronización con cielo real | **Event Engine del juego**: calcula en runtime qué Estrella Real, planeta y fase lunar están visibles sobre el horizonte de Lota en cada momento. Al entrar a una zona, el juego consulta y desbloquea quests/personajes según eventos celestes en tiempo real. Diferenciador único. | MVP |
| **Hexagonal Control** (`hexagonal_control.py`) | Red hexagonal de 91 nodos, codificación base-60, sincronización "Salto 17" (Axiomatic Key), clase `HexagonalController` | **Mapa mental de zonas patrimoniales**: los 91 nodos del lattice se corresponden con zonas del mapa de Lota. La sincronización Salto-17 cada 68 ticks genera eventos rítmicos del juego (aparición de personajes, dispatch de quests). Capa matemática de progresión, no visual directa. | MVP |
| **Quantum Lattice Engine** (`quantum_lattice_engine.py`) | Red cuántica discreta, `QuantumNode` con fase y energía S60, interacción XY con dinámica hamiltoniana `dφᵢ/dt = -J Σⱼ sin(φᵢ - φⱼ)` | **Red social de jugadores**: cada jugador es un nodo con fase (rango social) y energía (vitalidad/Carboncillos). Interacción XY modela comunidad: jugadores sincronizados comparten recompensas, desincronizados generan eventos competitivos. Modela equipos (modo Familia) o rivalidades. | MVP (modo Familia) |
| **MycNet Daemon** (`mycnet-daemon`) | Base del servidor HTTP/WebSocket en Axum para conexiones de clientes del juego. Integra mesh batman-adv + métricas S60 + modulación YHWH. | **Servidor HTTP/WebSocket del juego (`lota-server`)**: capa de transporte para clientes web. Integra el mesh bio-inspirado con métricas exactas en base-60. Ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` tabla "Matriz de Componentes Reutilizables". | MVP (Opción B) |
| **MycNet Connect** (`mycnet-connect`) | Estructura de traits y handlers asíncronos de eventos (`MycNetHandler`). | **Sistema de handlers de eventos del juego**: arquitectura basada en traits y canales `tokio::sync::mpsc` para procesar mensajes sin bloqueos. Ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` tabla "Matriz de Componentes Reutilizables". | MVP (Opción B) |
| **SOMA Orchestrator** (`sentinel/.soma`) | Patrón de contratos, validación de tareas, bus Pub/Sub sobre Redis. Lee fase YHWH; en fase VAV con coherencia > umbral hace dispatch. | **Orquestación del juego**: el bus Pub/Sub de eventos del juego (quests, misiones diarias, eventos celestes) corre sobre SOMA. Coexiste con Redis Pub/Sub de `lota-server`: SOMA para dispatch interno coherente con pentaresonancia, Redis para transporte cliente-servidor y entre instancias de `lota-server`. Ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` tabla "Matriz de Componentes Reutilizables". | MVP (Opción B) |
| **MycNet Core S60 / Math Utils** (`mycnet-core`) | Utilidades matemáticas deterministas de punto fijo para cálculos exactos. | **Capa matemática determinista compartida** entre cliente y servidor: distancias, geofencing, polígonos, scores, cálculos de Carboncillos. Garantiza reproducibilidad bit a bit sin floats. Ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` tabla "Matriz de Componentes Reutilizables". | MVP (Opción B) |
| **Liquid Lattice Storage** (`liquid_lattice_storage.py`) | Almacenamiento holográfico distribuido, fluid dynamics para auto-reparación, 256 sectores de fase | **Persistencia del estado del juego**: estado de cada jugador (rangos, Carboncillos, medallas, rutas completadas, reportes) se almacena holográficamente distribuido. 256 sectores de fase permiten recuperaciones parciales resilientes; auto-reparación por fluid dynamics. Servidor propio con latencia muy baja. | MVP |
| **MHD Shield** (escudo magnetohidrodinámico) | Ley de Lorentz (J×B) sobre plasma ionizado: coherencia Dicke >95% activa reducción de arrastre Cd 0.4 → 0.15 (validado por Muir & Nikiforakis 2022, arXiv:2207.09857) | **Mecánica de "modo vehicular/narrativo"**: cuando el jugador acumula coherencia (Carboncillos + misiones + reportes validados), si supera 95%, se activa un "modo MHD" en el juego con perks temporales (misiones especiales desbloqueadas, navegación narrativa extendida). Metáfora gamificada del escudo físico real. **HIPÓTESIS** — coherencia Dicke como mecánica de progresión, requiere validación de INTERLOCUTOR. | Fase 2 |
| **Crystal Lattice** (`crystal_lattice.py`) | Red de resonancia de cristales acoplados, acoplamiento 10/60, transferencia de energía entre nodos adyacentes, oscilación sincronizada paso a paso | **Mecánica de misiones cooperativas**: cuando varios jugadores están en zonas próximas (acoplamiento 10/60), pueden transferir energía entre sí para activar eventos grupales (resonancia, quests comunitarias). Simulación de simpatía vibratoria en multijugador. | MVP (modo Familia) |
| **Quantum Memory / akashic_records** (`quantum_memory.py`, `liquid_memory.py`) | Memoria no-Markoviana, kernel Ornstein-Uhlenbeck, `akashic_records` almacena claves S60 | **Memoria histórica del jugador y de Lota**: cada acción del jugador se almacena como clave S60. La consulta devuelve trayectoria coherente. Útil para narrativa procedural (qué hizo, qué personajes conoció, qué misiones completó) y para que el Municipio vea el impacto acumulado. | MVP |
| **Isochronous Clock / Time Crystal** (`isochronous_oscillator.rs`, `time_crystal.rs`) | Oscilador isocrónico a 41.77 Hz (tick 23.939.835 ns), respiración 41–43 Hz / 4 fases YHWH / autocorrección cada 68 ticks (Salto-17). Sin drift de fase porque base-60. | **Reloj base del juego y fases del día/noche**: el tick 41.77 Hz es la unidad de tiempo fundamental. La respiración YHWH (YOD/HEH/VAV/HEH) define las fases del día en el juego (amanecer, día, atardecer, noche). El Salto-17 cada 68 ticks genera eventos globales (cambio de hora, misiones diarias). Sin drift: el juego siempre sabe la hora con exactitud matemática. | MVP |
| **Pentaresonance** (no es un módulo aislado — es la lattice YA cantada) | `LiquidLattice` con `inject_dual_channel(a,b)` (canal dual A/B: amplitud 8 bytes + fase 1 byte→grados) + `S60PID` por celda + `soma_orchestrator` dispara dispatch en fase VAV. Estado = `ComplexSPA` con magnitud = coherencia Dicke, fase = phi del cristal. | **Capa matemática base del juego**: todo estado coherente del juego (posición de jugador, fase de quest, tiempo del mundo) se representa como `ComplexSPA`. La pentaresonancia es la LATTICE del juego, no un módulo a construir. Cualquier módulo nuevo del juego debe acoplarse a `LiquidLattice` con PIDs/fase-YHWH/baño-16-bit en RAM, no a `ResonantMatrix` pelada (PITFALL `sentinel-s60-stack`). | MVP |
| **MycNet / ADM** (`adm.rs`, `mycnet/`) | Red mesh bio-inspirada: batman-adv (capa L2/L3) + fq_codel/cake (colas) + MinIO/Ceph (storage) + modulación armónica YHWH + métricas S60. Criterios: p95 RTT < 50ms, convergencia < 1s tras failover, tolerancia a 50% pérdida de nodos. | **Infraestructura de servidor del juego**: múltiples nodos mesh distribuyen la carga del juego (jugadores concurrentes, checkpoints de Carboncillos, eventos celestes calculados). Tolerancia 50% pérdida de nodos = el juego no se cae si la mitad del servidor falla. MinIO/Ceph almacena los `akashic_records` y los assets del juego (imágenes de zonas, audios de personajes). Modulación YHWH en el rebalanceo = coherencia de fase en la red. | MVP (servidor) |
| **Merkabah** (acoplamiento `m_eff = m_static / (1 + k·coherencia)`, asintótico) | Masa inercial efectiva, NO anulación rígida del 95%. La "masa faltante" se transfiere a momento angular del campo. Etiquetado como hipótesis en vault, no borrar. | **Mecánica de "modo cognitivo" del juego**: cuando el jugador acumula coherencia (Carboncillos + misiones + reportes validados), la "masa narrativa efectiva" baja (más acceso a secretos del炭ón, diálogos extendidos con personajes, rutas bloqueadas que se desbloquean). **HIPÓTESIS** — etiquetada en vault, podría usarse como mecánica avanzada o dejarse para fases posteriores. | Fase 2 (validar antes) |

**Arquitectura real de pentaresonancia (no asumir módulo aislado):**
- `quantum_core.rs::ResonantBuffer` — malla de `IsochronousOscillator`, **un `S60PID` por celda**, `phase: "YOD"` (respiración YHWH 4 fases), `coherence` medida, `clock` 41.77 Hz.
- `quantum_core.rs::LiquidLattice` + `inject_dual_channel(a,b)` — canal dual A/B. Levitación de datos (binario → lattice).
- `ram_meter.rs::recommend_lattice_ring` — dimensiona la malla por RAM real.
- `shm_bridge.rs` (`PySharedBuffer`, libc `shm_open`/`mmap`) + `ResonantMatrix::sync_to_shm` — ancla la lattice a host RAM (POSIX SHM). Nodos se bañan en amplitudes de 16 bits cada uno en RAM.
- `resonant_dashboard.rs` — visualiza nodos con `load: u16`, `progress: u16`.
- `soma_orchestrator.rs` — lee fase YHWH, en fase VAV con coherencia > umbral hace dispatch.

**PITFALL CLAVE (skill `sentinel-s60-stack`):** "El ascenso/estado NO es un módulo aislado a escribir entero: debe **acoplarse a `LiquidLattice`** (PIDs/fase-YHWH/baño-16-bit en RAM), no a `ResonantMatrix` pelada." Cualquier módulo nuevo que se escriba debe acoplarse a esta lattice pentaresonante ya existente.

**Lo que NO se ha decidido:**
- Confirmación de los roles específicos propuestos por INTERLOCUTOR (puede refinarlos o cambiarlos).
- Qué módulos entran en el MVP (3-4 semanas, demo de postulación al fondo) y qué queda para fases posteriores — propuesto arriba pero requiere confirmación.
- Benchmarks de cada módulo bajo carga de juego (muchos usuarios, baja latencia, persistencia de eventos celestes).
- Cómo se relacionan estos módulos con la opción de stack elegida por Fabiola (P-004: Opción A PWA vs Opción B Rust).
- **R&D abierto:** (ninguno al 2026-08-09 — ver ítems resueltos abajo)
- **(RESUELTO 2026-08-09) Coexistencia de buses (SOMA vs Redis Pub/Sub):** INTERLOCUTOR decidió "que convivan hasta que podamos hacer testing y estudiar el mejor". SOMA = dispatch interno coherente con pentaresonancia (eventos celestes, fases día/noche, misiones rítmicas); Redis Pub/Sub + Streams = transporte cliente↔servidor y entre instancias de `lota-server` (posiciones 64 Hz, deltas Carboncillos, chat, reportes, tareas asíncronas). Convivencia provisional — revisar cuando haya datos de testing bajo carga real. Ver `_analisis/12_inputs_pendientes_de_interlocutor.md` pregunta 1.
- **(RESUELTO 2026-08-09) Coexistencia de clocks:** el `IsochronousClock` 41.77 Hz de Sentinel es el **reloj maestro** que sincroniza mundo real y mundo digital con exactitud matemática (base-60, sin drift) y baja latencia. El tick loop del juego a 64 Hz (`lota-server`) corre subordinado al reloj maestro, alineándose en el Salto-17 cada 68 ticks de Sentinel (≈ 1.6 s por fase de cambio de hora real). Ver `_analisis/11_borrador_propuesta_fondo.md` sección 4.2.

**Referencias cruzadas actualizadas (2026-08-09):**
- `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md` — investigación de motores Rust (Bevy, WGPU, Fyrox, Macroquad) + arquitectura de servidor dedicado (UDP/QUIC, ECS, R-Tree con `rstar`, H3 con `h3o`, 64-128 Hz tick loop).
- `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` — propuesta detallada de `lota-server` (tokio+axum+QUIC+R-Tree+Redis Pub/Sub+PostgreSQL+PostGIS+Bevy cliente) y matriz de componentes reutilizables del ecosistema Sentinel (mycnet-daemon, mycnet-connect, SOMA, mycnet-core S60/utils).

**Pendiente:** confirmación de INTERLOCUTOR sobre roles propuestos y módulos MVP antes de avanzar en `_analisis/10_opciones_tecnologicas_para_clienta.md`, `_analisis/11_borrador_propuesta_fondo.md` (sección 4 tecnología), `_analisis/08_carta_gantt_3_semanas.md` y `_analisis/09_presupuesto_referencial.md` con esos roles.

---

### D-011 · Camino C confirmado — motor propio S60 + pipeline GPU activo (2026-08-09)
- **Decisión:** motor gráfico propio desde cero. Sentinel S60 (`me60os_core`) controla TODO el cómputo. Sin Bevy, Godot, Unity, Fyrox. Sin `f32` en lógica de juego.
- **Estado:** GPU pipeline inicializado y corriendo contra GTX 1050 / Vulkan. Binary `lota-server` ejecutándose. Tests pasando.
- **Componentes construidos:**
  - `rust/src/gpu/buffer_pack.rs` — empaquetadores `GpuSPA`, `GpuVector3`, `GpuOscillator`, `GpuLatticeCell`.
  - `rust/src/gpu/pipeline.rs` — `LotaGpuPipeline` con WGPU, bind group layout dual-lane.
  - `rust/src/gpu/shaders/spa_unpack.wgsl` — desempaquetado S60 en shader.
  - `rust/src/gpu/shaders/lattice_interference.wgsl` — convergencia dual-lane `@workgroup_size(64)`.
- **Razón:** Sentinel ya tiene todo el math exacto portado a Rust. El motor propio evita contaminar el pipeline con f32 de motores de terceros. Costo: más trabajo de render; ganancia: isomorfismo total CPU↔GPU↔simulación.
- **Contraparte analizada:** Bevy (f32 interno, incompatible con YATRA), Godot (f32 interno), Unity (C#, no aplica).
- **Reversible:** sí, a Bevy si se acepta f32 en render, pero rompe el contrato YATRA.

### D-012 · Arquitectura de integración Sentinel → GPU confirmada (2026-08-09)
- **Decisión:** la malla de cristales de Sentinel (`ResonantMatrix::crystals: Vec<IsochronousOscillator>`) se sube a VRAM vía `GpuOscillator::from_oscillator()` sin copia intermedia innecesaria.
- **Flujo de datos confirmado:**
  ```
  ResonantMatrix (RAM / SHM POSIX)
    → GpuOscillator::from_oscillator()   [buffer_pack.rs]
    → wgpu::Buffer (VRAM, storage)       [pipeline.rs]
    → lattice_interference.wgsl dispatch [GPU compute]
    → readback output buffer             [portal detectado]
    → game state update
  ```
- **Módulos Sentinel ya en Rust y disponibles para el motor:** `liquid_memory`, `resonant_matrix`, `hexagonal_control`, `dual_lane`, `qhc`, `crystal_cipher`, `flux_stabilizer`, `dsp`, `atlantean`, `pai60_lib`, `quantum_core`.
- **Eslabón faltante:** método `upload_lattice_to_gpu(matrix: &ResonantMatrix)` en `LotaGpuPipeline` que empaqueta los cristales y dispatchea el shader. Ver `_analisis/17_arquitectura_gpu_motor_lota.md`.
- **Invariantes que no cambian:** (1) f32 sólo dentro del shader WGSL, (2) `#[repr(C)]` en toda estructura que cruce RAM↔VRAM, (3) portal dual-lane = `|amp_A.raw - amp_B.raw| < SCALE_0/50`.

---

## Decisiones pendientes (abiertas)

### P-001 · Alcance del MVP vs prototipo Stitch
- **Estado:** abierto. Se debate en `_analisis/02_cotejo_audis_vs_prototipo.md`.
- **Hay que decidir:** qué entra al piloto (10 palos / 3-4 semanas) y qué se deja para fase 2.
- **Pendiente:** elección de Fabiola entre Opción A y Opción B (D-008, P-004).

### P-002 · Pila técnica de la aplicación — DECIDIDO código abierto
- **Decisión (2026-08-09):** pila de código abierto autoalojada, no Google Maps Platform.
- **Razón:** el proyecto es servicio comunal, no debe cobrar al usuario final. Google Maps Platform tiene costo por uso (incluso el plan más barato cuesta plata), OSM es gratis.
- **Pila confirmada:**
  - Mapa base: OpenStreetMap + MapLibre GL JS (cliente).
  - Geocodificación e inversa: Nominatim autoalojado.
  - Cálculo de rutas: OSRM (motor de código abierto).
  - Cercos virtuales: Turf.js en cliente + PostGIS en servidor.
  - Base de datos espacial: PostgreSQL + PostGIS.
- **Trade-off aceptado:** más tiempo de desarrollo (1-2 semanas solo para tener Nominatim + OSRM con datos de Chile funcionando).
- **Acción inmediata:** ver propuesta detallada en `_analisis/04_propuesta_tecnica_stack_osm.md`.

### P-003 · Qué entregar al fondo (producto corriendo vs propuesta) — CERRADO (2026-08-09)
- **Cierre:** D-004 — propuesta escrita + maqueta Stitch + demo jugable sin servidor completo.
- **Lectura de los audios (confirmada):** "presentar algo sólido en una etapa bien primaria".

### P-004 · Fabiola elige la pila técnica (Opción A vs Opción B)
- **Estado:** CERRADO (2026-08-10) — reemplazado por D-013.
- **Cierre:** INTERLOCUTOR decide evaluar dos pilotos en paralelo. La decisión técnica es del responsable técnico, no de la clienta.

---

### D-013 · Dos pilotos en paralelo: motor propio vs tecnología de mercado (2026-08-10)
- **Decisión:** ejecutar dos pilotos paralelos con el mismo contenido (5 zonas, misiones, personajes, reportes, estadísticas) para evaluar cuál es la versión definitiva.
  - **Piloto A — Tecnología de mercado:** PWA con React + Vite + TypeScript + MapLibre + OpenStreetMap + FastAPI. GPS real en celular desde el primer día.
  - **Piloto B — Motor gráfico propio:** Rust + wgpu (Vulkan/WebGPU) + Sentinel S60 + Axum. Control total, sincronización con cielo real.
- **Razón:** la decisión técnica es del responsable técnico (INTERLOCUTOR), no de la clienta. Se le quita la carga a Fabiola y se evalúa con datos reales. Ambos pilotos comparten contenido: la evaluación es de experiencia y viabilidad técnica.
- **Contraparte analizada:** pedir a Fabiola que elija entre A y B (rechazado — es preguntarle algo que no maneja y que no es su responsabilidad).
- **Piloto B ya tiene el eslabón resuelto:** `upload_and_dispatch` implementado y probado (4/4 tests, commit `de42f61`).
- **Reversible:** sí. La evaluación decide cuál pasa a ser la versión del piloto para el fondo.
