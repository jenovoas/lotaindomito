# Proyecto Lota Indómito — Estado vivo

**Última actualización:** 2026-08-10
**Raíz:** ``

---

## 1. Quién es quién

- **INTERLOCUTOR (tú)**: encargado técnico, interlocutor de la clienta.
- **CLIENTA (Fabiola)**: clienta. Postula a fondos públicos para turismo cultural en Lota (Chile).
- **Audios de CLIENTA**: 9 audios de WhatsApp del 2026-08-07, transcritos en `_analisis/transcripciones/`.

---

## 2. El proyecto en una línea

Juego tipo Pokémon GO ambientado en Lota (Chile). El jugador (Explorador del Carbón / Guardián de la Memoria) camina por la ciudad, entra a zonas turísticas, descubre historia, recoge Carboncillos y sube de rango (Aprendiz → Capataz → Leyenda de la Cuenca). **No es turismo literal, es un game con objetivos y metas de recorrido.** Ver GDD completo en `docs/concepto-juego.md`.

---

## 3. Datos duros confirmados (de audios)

| Dato | Valor |
|---|---|
| Presupuesto total del proyecto | **10 millones CLP** (incluye gastos + honorarios de ambos) |
| Plazo de presentación | **Fines de agosto / primera semana de septiembre 2026** |
| Fondo secundario posible | **Fondo del patrimonio: 15 a 20 millones CLP** |
| Postulación a dos fondos | **Sí, se puede** (audio 8) |
| Entregable implícito | **Propuesta para el fondo** (maqueta + doc), NO el producto terminado |

---

## 4. Estructura del repo

```
LotaIndomito/
├── _analisis/                    # Análisis del prototipo Stitch
│   ├── 00_resumen_sesion.md     # Estado al cierre de sesión anterior
│   ├── 01_resumen_audios_cliente.md
│   ├── 02_cotejo_audis_vs_prototipo.md
│   ├── transcribir_audios.py    # Script para reproducir transcripciones
│   └── transcripciones/         # 9 .md, uno por audio
├── docs/                        # ESTE DIRECTORIO — memoria operativa del proyecto
├── stitch_lota_ind_mito_ciudad_museo_gamificada/
│   ├── documento_t_cnico_lota_ind_mito.md   # Doc del prototipo Stitch
│   └── <~50 carpetas de pantallas>
└── whatsapp/                    # Audios originales (.ogg)
```

---

## 5. Convenciones de estilo de redacción (duro)

- **Español chileno obligatorio.** Sin conjugaciones argentinas.
- Prohibido: "vos", "tenés", "querés", "sos", "po", "che", "boludo", "bárbaro", "genial", "decime", "dale".
- Permitido: "tú", "tienes", "quieres", "eres", "ya", "listo", "ok", "dime".
- Audios transcritos pueden contener "vos"/"po"/"síbo" — es cita textual del audio, se conserva tal cual. Marcar con nota al inicio del archivo.

---

## 6. Sincronización con Google Drive (cliente sube archivos)

**Decidido (2026-08-09):** sync bidireccional con `drive:/LotaIndomito` (o nombre equivalente), usando `rclone bisync` + `inotifywait` + systemd user service.

- Mismo patrón que `micellia`. Ver skill `backup/rclone-drive-sync/`.
- **Caso de uso:** CLIENTA (clienta) sube archivos (correcciones, audios, fotos, documentos) a la carpeta Drive. La sync los baja a esta carpeta local en ≤5 min.
- Equivalentemente, lo que yo guarde aquí aparece en Drive y ella lo ve.
- **Pendiente:** aún no se ha configurado. Esperar OK explícito de INTERLOCUTOR para `rclone bisync --resync` inicial.

## 7. Repositorio git (laptop + servidor fan)

**Estado:** **NO creado todavía.** Pendiente.

- Plan: `git init` en ``, primer commit, después replicar a servidor fan vía la pipeline que INTERLOCUTOR ya tiene.
- Esperar instrucción "cámbialo" o similar para ejecutar. NO hacer por mi cuenta.

## 8. Procedimientos operativos

### Re-transcribir audios (si se borran o se agregan nuevos)

```bash
cd _analisis
python3 transcribir_audios.py
```

Usa `faster-whisper` local, modelo `small` int8, CPU. Sin API, sin cuota.

### Detector de argentinismos en el repo

```bash
cd LotaIndomito
find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.py" \) ! -path "*/transcripciones/*" \
  | xargs grep -niE "\bvos\b|\btenés\b|\btenes\b|\bquerés\b|\bqueres\b|\bsos\b|\bpo\b|\bche\b|..." 
```

(Ver `decisiones.md` para el patrón regex completo.)

## 9. Lecciones aprendidas — sesión 2026-08-09

### 9.1 Skills oficiales del framework Sentinel (no cargar las genéricas)

**Fuente:** `/home/jnovoas/Proyectos/sentinel/docs/07_prompts/` (NO `docs/skills/` — esos symlinks en `~/.hermes/skills/` apuntaban a directorio vacío).

**Las 3 skills oficiales son:**

1. **`sentinel-knowledge-layer`** — Capa 1 de 3: Agent Reach + vault Obsidian + git como licencia. Flujo de cotejo de fórmulas contra papers primarios.
2. **`sentinel-comprehension`** — Capa 2 de 3: el POR QUÉ del sistema. Pentaresonancia (no 2D), cristal respirando 41–43 Hz con autocorrección cada 68 ticks (Salto-17), gap que ahorra energía (superradiancia Dicke), Merkabah asintótico, levitación de datos = canal de fase en RAM.
3. **`sentinel-s60-stack`** — Capa 3 de 3: build/run/verify del stack me-60os S60. PITFALL: la pentaresonancia YA está implementada (no escribir módulo aislado). Módulo aislado = MUSEO, no se borra.

**Skills genéricas (NO usar para Sentinel):** `s60-dev`, `complex-spa`, `quantum-time-crystals`, `optomechanical-cooling`, `buffer-systems`. Estas son skills del ecosistema base-60 más amplio (usadas en `~/.claude/skills/`), NO son las oficiales del proyecto Sentinel.

### 9.2 Lota Indómito es cliente de Sentinel

- Sentinel es el framework matemático S60 para Linux, en producción y financiado (7 daemons activos en host Fan).
- Lota Indómito es un cliente que aplica módulos del core S60 a un caso de uso de patrimonio cultural (juego Pokémon GO del carbón en Lota).
- Módulos identificados para integrar al juego: celestial (D-010), hexagonal control, quantum lattice engine, liquid lattice storage, MHD shield, crystal lattice, quantum memory, isochronous clock / time crystal, pentaresonance (no es módulo aislado, ya vive en `LiquidLattice`), MycNet / ADM, Merkabah (etiquetado como hipótesis en vault).
- Ver D-010 y D-010-A en `decisiones.md` para el detalle y las fuentes.

### 9.3 Inputs pendientes de INTERLOCUTOR y de Fabiola (centralizado)

A la fecha de cierre de esta sesión (2026-08-09), tres preguntas están explícitamente pendientes de input de terceros. **No se avanzó sobre ellas en ningún documento del repo para evitar inventar contenido** (error central de esta sesión, ya corregido).

**Documento centralizado:** `_analisis/12_inputs_pendientes_de_interlocutor.md` — contiene las tres preguntas con contexto técnico, fuentes reales, opciones cuando aplica y referencias cruzadas.

**Resumen ejecutivo de la sesión:** `_analisis/13_resumen_sesion_20260809.md` — estado completo de la sesión 2026-08-09 (decisiones D-004..D-010, documentos modificados/nuevos, renombramientos, conflictos no tocados, tareas pendientes, lecciones aprendidas, `git status`).

**Resumen ejecutivo de las 3 preguntas:**

| # | Pregunta | Depende de |
|---|---|---|
| 1 | SOMA vs Redis Pub/Sub — ¿conviven como capas distintas (SOMA para dispatch interno coherente con pentaresonancia, Redis para transporte cliente-servidor) o uno reemplaza al otro? | INTERLOCUTOR |
| 2 | Roles específicos de módulos MVP en el juego — confirmación o refinamiento de la propuesta en D-010-A | INTERLOCUTOR |
| 3 | Opción A (aplicación web progresiva) vs Opción B (videojuego Rust + servidor propio `lota-server`) | Fabiola |

**Tareas bloqueadas por cada pregunta:**

- Pregunta 1: cerrar coherentemente `_analisis/11_borrador_propuesta_fondo.md` sección 4.2 sobre buses, y el bloque "R&D abierto" en D-010-A.
- Pregunta 2: cerrar `_analisis/11_borrador_propuesta_fondo.md` sección 4.2 sobre roles, ajustar `_analisis/09_presupuesto_referencial.md` al alcance MVP, ajustar `_analisis/08_carta_gantt_3_semanas.md` al cronograma real.
- Pregunta 3: cerrar `P-004` en `docs/decisiones.md`, ajustar `_analisis/10_opciones_tecnologicas_para_clienta.md` a la opción única elegida por Fabiola.

**Notas de avance parcial durante la sesión 2026-08-09:**

- Resuelto: coexistencia de clocks (D-010-A) — `IsochronousClock` 41.77 Hz de Sentinel es el reloj maestro que sincroniza mundo real y mundo digital con exactitud matemática (base-60, sin drift) y baja latencia; el tick loop del juego a 64 Hz (`lota-server`) corre subordinado.
- Documentos coherentes con el upstream: `_analisis/10_opciones_tecnologicas_para_clienta.md` y `_analisis/11_borrador_propuesta_fondo.md` sección 4.2 ya referencian explícitamente la arquitectura `lota-server` (`_analisis/07_propuesta_arquitectura_servidor_rust_juego.md`) y la investigación de motores Rust (`_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md`).
- Resuelto conflicto de numeración en `_analisis/`: mi `06_opciones_tecnologicas_para_clienta.md` renombrado a `10_*`, mi `07_borrador_propuesta_fondo.md` renombrado a `11_*`, para liberar slots `06_*` y `07_*` a los archivos de INTERLOCUTOR (`06_investigacion_motores_rust_juegos_ultra_rapidos.md` y `07_propuesta_arquitectura_servidor_rust_juego.md`).

## 10. Motor GPU — estado del eslabón faltante (2026-08-10)

### 10.1 Eslabón faltante RESUELTO

El puente SHM→VRAM→compute→readback está implementado y probado:

- `GpuLatticeNode` (272 bytes, dual-lane): Lane A + Lane B + position xyz + coherence_flag
- `upload_and_dispatch(lane_a, lane_b, time_sec, delta_time, salto17_tick)` en `pipeline.rs`
- `DispatchResult { wave_values, portal_count, portal_indices }`
- 4/4 tests pasando (alignment, sizes 128/272, from_lanes)

Flujo completo conectado:

  ResonantMatrix::crystals (Sentinel Rust)
    ↓  GpuLatticeNode::from_lanes()
  Vec<GpuLatticeNode>  [272 bytes/nodo, interleaved A+B]
    ↓  device.create_buffer_init() → VRAM
  wgpu::Buffer STORAGE
    ↓  dispatch_workgroups(ceil(n/64), 1, 1)
  lattice_interference.wgsl  [@workgroup_size(64)]
    ↓  staging readback + unmap
  DispatchResult { wave_values, portal_count, portal_indices }

### 10.2 Integración en main.rs — RESUELTA (2026-08-10)

`upload_and_dispatch` quedó integrado en `main.rs` con un `ResonantMatrix` real de
Sentinel (commits `de42f61` + `1f5e3f`). El binario `lota-server` corre el ciclo
completo: lattice dual-lane de 91 nodos → VRAM → compute shader → readback →
reporte de portales. 4/4 tests pasando. **Piloto B es el centro del concepto (D-014 corregida), no R&D.**

---

## 11. Workstream activo: piloto de concepto (D-014 corregida, desde 2026-08-10)

**Norte del proyecto:** potenciar el turismo de Lota para **revivir el comercio local**.
El juego es el medio: patrimonio + jugabilidad llevan turistas a la comuna, el juego los
guía por las zonas y el comercio, el comercio revive y **autofinancia** la plataforma.

**Encuadre vigente:** la postulación al fondo es dominio de Fabiola. INTERLOCUTOR prepara
el proyecto y su diseño: un **piloto / diseño de concepto** en ~30 días que demuestra el
diferenciador central. NO el juego completo. La fase 1 arranca después.

**Concepto (visión completa):**
- Evento real (cielo/hora, Sentinel) → decide qué pasa en el juego.
- Enjambre SOMA de NPCs simples y vivos (deambulan en su zona, sin IA pesada).
- La caza en el teléfono (PWA accesible, stack Piloto A).
- Encuentro en RA (gafas Meta Quest 3/3S, préstamo en sitio) que reconstruye la historia
  e imágenes reales de Lota.
- Costura de baja latencia: teléfono ↔ lota-server + SOMA ↔ gafas (carriles de la lattice).
- Etapa 2: avisos de comercio en RA + circuito de Carboncillos → autofinanciamiento.
- Expansión regional: Lota es la prueba de concepto; se expande a Curanilahue, Lebu,
  Arauco y Concepción (corredor patrimonial de la zona del carbón). El motor es agnóstico
  de comuna: cada una aporta su contenido. Modelo regional escalable.

| Ítem | Valor |
|---|---|
| Entregable ~30 días | Piloto / diseño de concepto que demuestra el diferenciador (evento real → NPC vivo → caza → encuentro) |
| Dispositivos | Teléfono (PWA, Piloto A: Vue 3 + MapLibre + Turf) + gafas RA (Meta Quest 3/3S) |
| Motor | Piloto B / Sentinel — centro del concepto, NO congelado |
| Ubicación código | `piloto-a/` (teléfono) y `rust/` (motor); convenciones en `.gitignore` |
| Fuera de alcance (~30 días) | Juego completo, 8 rutas, GPS real, etapa 2 de comercio |

**Nota de capacidad:** INTERLOCUTOR programa desde los 9 años, autor de Sentinel,
construye sistemas complejos rápido. No recortar alcance por defecto.

**Pendiente inmediato:** definir la zona y el encuentro con que el piloto demuestra el
diferenciador; obtener polígonos reales de las zonas de Lota (Overpass/OSM).
