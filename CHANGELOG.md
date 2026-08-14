# Changelog — Lota Indómito

Registro de hitos del proyecto en orden cronológico inverso (lo más reciente primero).
Cada entrada cita su evidencia real (commits, tests) — este archivo es a la vez el
registro técnico del avance y el material de portfolio/currículum.

Las decisiones de diseño se registran aparte, en [`docs/decisiones.md`](docs/decisiones.md).

---

## 2026-08-13

### Redefinición de la Experiencia de Juego Temática: MMO-RA Urbano (D-019)
- **Fusión Pokémon GO × World of Warcraft en RA:** Redefinido el GDD ([`docs/concepto-juego.md`](docs/concepto-juego.md)) y el loop del jugador ([`_analisis/20_loop_jugador_dia_a_dia.md`](_analisis/20_loop_jugador_dia_a_dia.md)) para transformar el juego en un MMO del Mundo Real.
- **Patrullas Sincronizadas en Movimiento:** Especificada la dinámica de intercepción física a pie y diálogo en marcha ("caminar hombro a hombro" en RA) con personajes históricos desplazándose por las calles reales con sincronización determinista entre jugadores.
- **Diseño "Ojos Arriba" (Look-Up Design):** Reemplazo de minijuegos 2D abstractos por mecánicas de Realidad Aumentada que exigen observar y alinear el entorno patrimonial físico (resonancia térmica, phasing arquitectónico, sellos de cantería).
- **Facciones, Clases y Raids Urbanas:** Integradas 3 Facciones (*Hermandad del Carbón*, *Linaje de la Luz*, *Gremio de las Mareas*), 4 Clases de Explorador (*Barretero*, *Chinchorrera*, *Cronista*, *Fogonero*) y eventos de World Bosses en RA cooperativos sobre el paisaje real.
- **Decisión D-019 registrada** en [`docs/decisiones.md`](docs/decisiones.md).

---

## 2026-08-12

### Implementación del Piloto de Demostración (Pasos 1, 2 y 3)
- **Especificación del Piloto (Paso 1):** Creado [`docs/piloto_zonas_especificacion.md`](docs/piloto_zonas_especificacion.md) definiendo las 3 zonas clave de Lota Alto (Chiflón del Diablo, Parque Isidora Cousiño, Pabellón 83), el flujo de 5 tramos (4 min) de la micro-sesión y el gatillado de Portales Lattice S60.
- **Geometría OSM (Paso 2):** Implementado [`_scripts/download_lota_osm.py`](_scripts/download_lota_osm.py) para consultar Overpass API y generado [`public/data/lota_pois.geojson`](public/data/lota_pois.geojson) con 41 POIs turísticos e históricos reales de Lota.
- **Micro-sesión e Integración PWA (Paso 3):** Construido el componente [`piloto-a/src/components/MicroSesionChiflon.vue`](piloto-a/src/components/MicroSesionChiflon.vue) (diálogo con *El Ciego de la Mina*, minijuego de clasificación geológica y recompensa en Cobre), e integrado en [`MapaLota.vue`](piloto-a/src/components/MapaLota.vue) y [`App.vue`](piloto-a/src/App.vue) con sincronización de la billetera `WalletHUD`.
- **Commit:** `7e9b395` con build limpia en Vue 3 (`npm run build-only`).

---

## 2026-08-11

### Limpieza pre-demo (coherencia con D-014 y correcciones técnicas)
- **`docs/propuesta-fondo.md` §8 alineado con D-014:** reemplazado el enunciado
  "Se evaluarán dos pilotos en paralelo. La evaluación técnica decide cuál es la
  versión definitiva" por "Arquitectura en dos capas (D-014)" — Piloto A (capa
  accesible) + Piloto B (capa diferenciadora, motor soberano). El motor es el
  diferenciador central, no una alternativa en competencia. D-013 queda como
  decisión histórica reinterpretada por D-014.
- **`_analisis/17_arquitectura_gpu_motor_lota.md` (3 correcciones de hecho):**
  `pollster` → `tokio` (diagrama §2 y dependencias §4), `GpuOscillator (64 bytes)`
  → `(128 bytes)` (§4). El eslabón `upload_and_dispatch` ya estaba marcado ✅ en §5/§7.
- **`MEMORY.md`:** corregida nota obsoleta sobre §6.5 perdido — el §6.5 actual
  ("No es un proyecto genérico ni simplificado") sí existe en `propuesta-concepto.md`
  línea 620 y cierra bien el bloque "Lo que NO es".
- Validación demo en vivo: `index.html`, `prototipo-stitch.html`,
  `docs/propuesta-concepto.html`, `README.html` responden 200 en
  https://pinguinoseguro.cl/lotaindomito/ con navbar única compartida.
- Push a GitHub al día (HEAD `8fdc1f5` = `origin/main`).
- Archivos de conflicto `propuesta-concepto.md.conflict1/2` se conservan como
  evidencia histórica (decisión del INTERLOCUTOR).

### Documentación y propuesta de concepto
- **Propuesta de concepto del proyecto completada** (`docs/propuesta-concepto.md`, 3,161 líneas, ~60 págs). Documento técnico-diseño integral organizado en 5 partes y 28 secciones:
  - **Parte I (Concepto):** Tesis (turismo + patrimonio + S60), diseño de concepto D-014, universo narrativo (4 figuras, 8 rutas, 3 minerales), sistema económico (D-016 multi-moneda, D-017 subastas, World Events, ML externo), diferenciador técnico (S60 sin floats, sin Google), lo que NO es el proyecto.
  - **Parte II (Especificación técnica):** Arquitectura en 5 capas + SOLID + ISO/IEC 5055, PWA Piloto A (Vue 3 + MapLibre + Turf.js + Pinia + 16 eventos ML), backend `lota-server` (FastAPI + PostGIS + OSM self-hosted), motor GPU Piloto B (Rust + wgpu + Sentinel S60 lattice 91 nodos), ML externo (Python, vistas materializadas, privacidad Ley 19.628), sync y operación (rclone bisync, deploy fan VPS).
  - **Parte III (Fundamentación teórica):** Por qué S60 y memoria de cristal (sin deriva floats, LiquidMemory SHM), por qué multi-moneda ( rareza diferenciada, P2P, anti-inflación), por qué World Events (turista de paso vs racha diaria), por qué expansión regional (corredor Arauco), por qué autosustentable (comisión comercio vs SaaS).
  - **Parte IV (Plan por etapas y testing):** Marco normativo ISO (12207, 25010, 27001, 31000, 9241 — alineamiento declarado), procesos de testing (pirámide 70/20/10, CI/CD, lints), Etapa 0 (Piloto de concepto 30 días), Etapa 1 (MVP + lote piloto público 100+ usuarios, decisión GPU real), Etapa 2 (Escala local + subastas D-017, RA Meta Quest 3, modo Familia), Etapa 3 (Expansión regional corredor Arauco), Etapa 4 (Operación continua 12 meses 1000+ usuarios, ITIL 4 diferido).
  - **Parte V (Cierre):** Matriz de riesgos ISO 31000 (7 riesgos con mitigación), gestión de servicios ITIL 4 (en evaluación, 6 preguntas abiertas), las 21 decisiones de diseño abiertas con recomendación por doc, referencias cruzadas (docs, análisis 04..25, bóveda PersonalVault, módulos Sentinel `me-60os-core`).
- Commits de entrega: `07664f4`, `9ac9ee5`, `e8202b2`.

---

## 2026-08-10

### Concepto y diseño
- Asentado el concepto real del proyecto (D-014 corregida): evento real → NPCs del
  enjambre SOMA → caza en el teléfono → encuentro RA que reconstruye la historia real
  de Lota; motor/Sentinel como centro; etapa 2 de comercio RA + autofinanciamiento;
  expansión regional Lota → Curanilahue/Lebu/Arauco/Concepción. (`e7b868c`)
- Propuestos dos pilotos paralelos — motor propio vs tecnología de mercado (D-013). (`b9b485b`)
- Consolidada la propuesta al fondo en lenguaje humano. (`1e87bf4`)
- Rediseñado el **Core Game Loop** del GDD: el turista de paso (1-2 días en Lota)
  no tiene loop diario, sino **loop de visita** (6-10 micro-sesiones de 1-5 min cada
  una + 1-3 eventos del cielo por día) y **loop de retorno** (D+1 → D+30 vía
  pasaporte incompleto, calendario del cielo y cupones con caducidad). Las mecánicas
  clásicas de mobile (racha diaria, energía que regenera) se descartan por no
  aplicar al turista. Nuevo análisis completo en
  `_analisis/20_loop_jugador_dia_a_dia.md`. `docs/concepto-juego.md` §2
  reescrito con 5 subsecciones (loop de visita, loop de retorno, anatomía de
  micro-sesión, catálogo de eventos, descartes del modelo clásico). (`8a92131`)

### Piloto A (web — teléfono)
- Scaffold Vue 3 + TypeScript + MapLibre: mapa de Lota con 5 zonas patrimoniales. (`9e793c4`)
- Corregido el stack a Vue 3 (descartados React/Vite/Svelte para el piloto). (`37f6008`)

### Motor (Piloto B — Rust + Sentinel)
- Integrado `upload_and_dispatch` en `main.rs` con un `ResonantMatrix` real de Sentinel:
  el binario `lota-server` corre el ciclo completo — lattice dual-lane de 91 nodos → VRAM
  → compute shader → readback → reporte de portales. (`b1f5e3f`)
- Resuelto el eslabón faltante SHM→VRAM→compute→readback: `upload_and_dispatch` +
  `GpuLatticeNode` dual-lane (272 bytes). 4/4 tests pasando. (`de42f61`)
- Creado el crate `lota_engine`: pipeline GPU con wgpu sobre GTX 1050 / Vulkan,
  empaquetadores binarios `#[repr(C)]` (GpuSPA 32B, GpuVector3 96B, GpuOscillator 128B,
  GpuLatticeCell 224B) y shaders WGSL (`spa_unpack.wgsl`, `lattice_interference.wgsl`
  con `@workgroup_size(64)`). (`ece04f6`)

### Infra y documentación
- Clarificada la arquitectura: Sentinel es la capa de infra (upstream estable), Lota
  Indómito la capa de aplicación. (`c9ab077`)
- Análisis técnicos 05-18: stack, arquitectura GPU, bitácoras de sesión. (`3b17e33`)
- Actualizados concepto, decisiones D-003..D-007, estado y scripts. (`60517d1`)
- Gitignore: excluye `rust/target`, `.omo/`, `.codegraph/`, conflictos huérfanos. (`6f82eab`)

---

## 2026-08-09

### Concepto y diseño
- Definido que Lota Indómito es un **juego tipo Pokémon GO, no una app de turismo**. (`144f5b2`, `c051b6d`)

### Infra
- Integrado el prototipo Stitch de la clienta como maqueta navegable en el sitio. (`f6d7e19`)
- Montado el sitio cliente (`index.html`) y el pipeline `render-docs.py`. (`b749d0a`, `93ec6cd`)
- Commit inicial del proyecto. (`23deb74`)

### Concepto y diseño (continuación)
- Diseñado el sistema multi-moneda de minerales cobre/oro/estaño (D-016 propuesta):
  reemplaza al Carboncillo como moneda única; cada mineral tiene identidad narrativa
  propia, valor relativo (1 estaño = 100 oro = 10.000 cobre), se gana por acciones
  diferenciadas y es transferible/truequeable/comercianteable. Refuerza D-014 con
  tres vías nuevas (misiones World Event, comercio multi-moneda, subastas reales).
  Nuevo análisis en `_analisis/23_sistema_monedas_minerales.md`. (entrada sin SHA: pendiente del commit de los docs modificados)
- Diseñadas las subastas digitales de cosas reales con pago en minerales (D-017 propuesta):
  el juego cobra 5-10% de comisión; objetos subastables son productos/servicios
  del comercio local; pago únicamente en minerales; sistema de escrow + reputación
  bilateral + resolución de disputas manual. Convierte al juego en marketplace
  soberano y refuerza D-014. Nuevo análisis en `_analisis/24_subastas_reales.md`.
  (entrada sin SHA: pendiente del commit de los docs modificados)
- Diseñado el ML externo para análisis de comportamiento: servicio Python (scikit-learn,
  XGBoost, Prophet) que consume vistas materializadas de solo-lectura de la DB,
  entrega dashboards para la clienta, el Municipio y el comercio sobre tres dimensiones
  (comercial, social, turística). Justifica gasto municipal con datos reales.
  Nuevo análisis en `_analisis/22_ml_analytics_d014.md`. (entrada sin SHA)

### Piloto A (web — teléfono)
- GDD actualizado con nuevo sistema económico (§4 multi-moneda), rangos redefinidos (§5),
  HUD multi-moneda (§7), MVP reescrito (§8) y tres secciones nuevas: World Events (§10),
  Subastas digitales (§11) y ML externo (§12). Decisiones D-016 y D-017 registradas
  en `docs/decisiones.md`. (entrada sin SHA)

### Infra y documentación
- Corregidos bugs de caracteres chinos mezclados con español en `_analisis/20-24`
  (10 instancias) — bug de generación que mezclaba caracteres chinos con texto en español.
- Actualizadas referencias a Carboncillos → minerales en `MEMORY.md`, `docs/estado.md`,
  `_analisis/20_loop_jugador_dia_a_dia.md` y `_analisis/21_world_events_d014.md`.
- (entradas sin SHA: pendiente del commit)
