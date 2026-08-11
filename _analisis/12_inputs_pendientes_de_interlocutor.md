# Inputs pendientes de INTERLOCUTOR

**Fecha:** 2026-08-09 (actualizado 2026-08-10)
**Estado:** de las 3 preguntas originales, 2 están resueltas (1: buses, 2026-08-09; 3: stack, 2026-08-10 vía D-013/D-014). Queda pendiente la Pregunta 2 (roles MVP de módulos Sentinel), que no bloquea la maqueta de 30 días (D-014).
**Para:** INTERLOCUTOR (Jaime).
**Por qué existe este documento:** durante la sesión 2026-08-09, los tres puntos abajo quedaron explícitamente pendientes de tu confirmación o de decisión de la clienta. No se avanzó sobre ellos en ningún documento del repo para evitar inventar contenido (error central de esta sesión, ya corregido). Este archivo es un único lugar donde responder todo de una vez.

---

## 1. D-010-A — R&D buses: coexistencia de eventos (SOMA vs Redis Pub/Sub) — RESUELTO (2026-08-09)

### Decisión tomada

**INTERLOCUTOR (2026-08-09):** "que convivan hasta que podamos hacer testing y estudiar el mejor".

→ SOMA y Redis Pub/Sub conviven como capas distintas (Opción A del menú original). La convivencia es **provisional** — sujeta a revisión cuando haya datos de testing (bajo carga real, latencia medida, comportamiento bajo failover).

### Distribución de responsabilidades (acordada)

- **SOMA** (dispatch interno coherente con pentaresonancia): eventos globales del juego vinculados al reloj maestro de Sentinel — eventos celestes (salida de Estrellas Reales, fase lunar), cambios de fase día/noche, misiones diarias, eventos rítmicos generados por la fase YHWH del cristal.
- **Redis Pub/Sub + Redis Streams** (transporte cliente↔servidor y entre instancias `lota-server`): posiciones de jugadores (64 Hz), deltas de Carboncillos, chat, reportes ciudadanos, tareas asíncronas (generación de diplomas PDF, validación comunitaria, persistencia diferida en PostgreSQL).

### Criterios de revisión (cuándo reconsiderar)

La convivencia se revisará cuando se disponga de datos de testing que muestren:
- Latencia inaceptable en eventos globales del juego (por sincronización de buses).
- Sobrecarga de SOMA por volumen de mensajes no coherentes con pentaresonancia.
- Conflictos entre ambos buses entregando el mismo evento.
- O cualquier otro motivo técnico identificado en testing.

### Fuentes (sin invención)

- **SOMA Orchestrator** (`sentinel/.soma`, ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` tabla "Matriz de Componentes Reutilizables"): patrón de contratos, validación de tareas, bus Pub/Sub sobre Redis. Lee fase YHWH; en fase VAV con coherencia > umbral hace dispatch.
- **Redis Pub/Sub** (`lota-server`, ver mismo doc): notificaciones instantáneas de eventos comunales, sincronización de estado entre instancias de `lota-server`. Plus Redis Streams para cola de tareas asíncronas (generación de diplomas PDF, validación comunitaria de reportes, persistencia diferida en PostgreSQL).

---

## 2. D-010-A — Roles específicos de módulos MVP en el juego

### Estado

En `docs/decisiones.md` D-010-A propuse roles específicos para cada módulo Sentinel identificado (columna "Rol propuesto en el juego" en la tabla). Roles no confirmados. Falta tu confirmación o refinamiento.

### Contexto técnico

Módulos en la tabla de D-010-A (todos con fuentes verificadas):
- Celestial (D-010): Event Engine del juego — sincronización con cielo real sobre Lota.
- Liquid Lattice Storage: persistencia holográfica del estado del jugador.
- MHD Shield: mecánica de "modo vehicular/narrativo" basada en coherencia Dicke > 95% — **marcado como HIPÓTESIS en mi propuesta**.
- Quantum Memory / `akashic_records`: memoria histórica del jugador y de Lota.
- Isochronous Clock / Time Crystal: reloj base del juego y fases del día/noche. **(Resuelto 2026-08-09: reloj maestro.)**
- Pentaresonance (la lattice YA cantada en `LiquidLattice`): capa matemática base del juego.
- MycNet Daemon: servidor HTTP/WS del juego (`lota-server`).
- MycNet Connect: sistema de handlers de eventos del juego.
- SOMA Orchestrator: orquestación del juego.
- MycNet Core S60 / Math Utils: capa matemática determinista compartida cliente-servidor.
- MycNet / ADM: infraestructura mesh del juego (tolerancia 50% pérdida de nodos, p95 RTT < 50ms, failover < 1s).
- Hexagonal Control, Quantum Lattice Engine, Crystal Lattice: propuestos por mí (no los mencionas en tu propuesta arquitectónica). Pendientes de tu visto bueno o descarte.
- MHD, Merkabah: marcados como hipótesis (vault etiquetado).

### Preguntas concretas para ti

1. **¿Confirmas los roles propuestos en la tabla de D-010-A** o quieres refinar/cambiar alguno?
2. **Hexagonal Control, Quantum Lattice Engine, Crystal Lattice** — los puse yo sin verlos en tu propuesta de arquitectura. ¿Los mantienes, los descartas, o los reemplazas con otra cosa?
3. **MHD Shield como mecánica de progresión** (coherencia Dicke > 95% activa perks) — ¿lo dejamos como Fase 2 o entra al MVP? (El vault lo etiqueta como hipótesis, no estándar.)
4. **¿Qué módulos entran en el MVP (3-4 semanas, demo de postulación) y cuáles a fases posteriores?** Mi propuesta actual:
   - MVP: celestial, liquid lattice, quantum memory, isochronous clock, pentaresonance, MycNet daemon/connect/S60, SOMA orchestrator.
   - Fase 2: MHD, Merkabah, crystal lattice, hexagonal control, quantum lattice engine, MycNet / ADM mesh completo.

### Por qué importa

La sección 4.2 del borrador (`_analisis/11_borrador_propuesta_fondo.md`), el presupuesto (`_analisis/09_presupuesto_referencial.md`), el cronograma (`_analisis/08_carta_gantt_3_semanas.md`) y el documento de opciones para la clienta (`_analisis/10_opciones_tecnologicas_para_clienta.md`) **no se pueden cerrar coherentemente** sin esta confirmación. Cualquier avance ahora sería especulación de roles.

---

## 3. P-004 — Elección de la clienta entre Opción A y Opción B — RESUELTA (2026-08-10)

### Estado

**RESUELTA.** P-004 fue cerrado el 2026-08-10: INTERLOCUTOR decidió no trasladar la
elección a la clienta y ejecutar dos pilotos en paralelo (D-013). Luego, D-014 (corregida)
fijó el encuadre real: Piloto A y Piloto B son capas de un mismo concepto (teléfono +
motor/Sentinel + RA), el motor es el centro y NO está congelado, y la postulación al
fondo es dominio de la clienta.

### Decisión tomada

- D-013: dos pilotos en paralelo (A = tecnología de mercado, B = motor propio). La decisión técnica es del responsable técnico.
- D-014 (corregida): concepto real — evento real → NPCs SOMA → caza en teléfono → encuentro RA; el motor es el centro; expansión regional Lota → Curanilahue/Lebu/Arauco/Concepción.

### Pregunta original (contexto histórico)

**la clienta debía elegir Opción A o Opción B.** Se resolvió sin su intervención: la
decisión técnica es del responsable técnico (D-013), y el encuadre de trabajo quedó
en D-014. El documento `_analisis/10_opciones_tecnologicas_para_clienta.md` queda
como comparativa histórica.

### Contexto técnico (de documentos del repo)

**Opción A — Aplicación web progresiva:**
- Interfaz: React 18 + Vite + TypeScript + PWA instalable.
- Mapa: MapLibre GL JS sobre OpenStreetMap.
- Cercos virtuales: Turf.js en cliente + PostGIS en servidor.
- Servidor: Python FastAPI + Pydantic + PostgreSQL 16 + PostGIS 3.4.
- GPS en celulares: día uno.
- Detalle: `_analisis/04_propuesta_tecnica_stack_osm.md` (restaurado 2026-08-10 desde copia de conflicto), `_analisis/05_analisis_tecnologias_disponibles.md` (tu versión actual).

**Opción B — Videojuego multiplataforma (Rust) con servidor propio:**
- Cliente: Bevy Engine (compila nativo + WASM/WebGPU).
- Servidor: `lota-server` (tokio + axum + QUIC + R-Tree + Redis Pub/Sub + PostgreSQL + PostGIS).
- GPS en celulares: Fase 2.
- Framework matemático S60 de Sentinel como capa de soberanía criptográfica.
- Detalle: `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md` (investigación de motores Rust), `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` (arquitectura `lota-server`).

### Pregunta concreta

~~la clienta debe elegir Opción A o Opción B.~~ **RESUELTA sin intervención de la clienta** — D-013 + D-014 (ver Estado arriba).

### Cómo desbloquear

Ya desbloqueada. Estado de las tres preguntas:
- Pregunta 1 RESUELTA 2026-08-09: convivencia SOMA + Redis Pub/Sub (provisional, revisar con testing).
- Pregunta 2 pendiente: confirmación de INTERLOCUTOR sobre roles MVP de módulos Sentinel. Con el encuadre D-014, esta pregunta aplica al Piloto B / fase 1+ (la maqueta de 30 días es Piloto A y no lleva módulos Sentinel).
- Pregunta 3 RESUELTA 2026-08-10: D-013 (dos pilotos) + D-014 (maqueta con Piloto A).

---

## Resumen ejecutivo

| # | Pregunta | Estado | Depende de | Cuándo se desbloquea |
|---|---|---|---|---|
| 1 | SOMA vs Redis Pub/Sub — ¿conviven o uno reemplaza al otro? | **RESUELTO 2026-08-09** (convivencia provisional) | — | Convivencia provisional; revisar con testing |
| 2 | Roles específicos de módulos MVP en el juego | Pendiente | INTERLOCUTOR | Cuando respondas (tecnología, no la clienta) |
| 3 | Opción A (web) vs Opción B (Rust/lota-server) | **RESUELTA 2026-08-10** (D-013 + D-014 corregida) | — | Cerrada: A y B son capas de un mismo sistema (teléfono + motor + RA); el motor NO está congelado |

**Tareas que NO puedo avanzar sin tu input** (Pregunta 2):
- Cerrar `_analisis/11_borrador_propuesta_fondo.md` sección 4.2 coherente con roles definitivos.
- Ajustar `_analisis/09_presupuesto_referencial.md` a los módulos MVP confirmados.
- Ajustar `_analisis/08_carta_gantt_3_semanas.md` al alcance real.

**Tareas que YA NO requieren input de la clienta** (Pregunta 3 resuelta por D-013 + D-014):
- ~~Reemplazar las opciones A/B en `_analisis/10_opciones_tecnologicas_para_clienta.md`~~ — el documento queda como comparativa histórica.
- ~~Cerrar `P-004` en `docs/decisiones.md`~~ — cerrado 2026-08-10.

**Acción recomendada (actualizada 2026-08-10):**
1. Preguntas 1 y 3 resueltas. Solo queda la Pregunta 2 (roles MVP de módulos Sentinel), que ahora aplica al Piloto B / fase 1+, no a la maqueta de 30 días (D-014).
2. La Pregunta 2 no bloquea la maqueta. Se responde cuando INTERLOCUTOR quiera, antes de retomar el Piloto B.

---

## Cómo se propagan las respuestas

Cuando lleguen las respuestas a las preguntas, los siguientes archivos se actualizan (sin invención de contenido; solo reflejar lo decidido).

### Pregunta 1 aplicada 2026-08-09 (buses SOMA + Redis Pub/Sub — convivencia)

1. ✅ `docs/decisiones.md` D-010-A — bloque "R&D abierto": quitado ítem buses; agregada entrada "(RESUELTO 2026-08-09) Coexistencia de buses" con la decisión tomada.
2. ✅ `_analisis/11_borrador_propuesta_fondo.md` sección 4.2 — nota de R&D abierto sobre buses reemplazada por nota "Buses de eventos (RESUELTO 2026-08-09)"; Estado del doc actualizado.
3. ✅ `_analisis/12_inputs_pendientes_de_interlocutor.md` — Pregunta 1 marcada como resuelta en este mismo doc (tabla resumen ejecutivo).

### Al responder Pregunta 2 (roles MVP + MHD + MVP/Fase 2)
1. `docs/decisiones.md` D-010-A — actualizar columna "Rol propuesto en el juego" y columna "MVP / Fase posterior" para cada módulo según lo confirmado; quitar "Pendiente" del título si todo está confirmado.
2. `_analisis/11_borrador_propuesta_fondo.md` sección 4.2 — reflejar los módulos MVP confirmados; actualizar lista de módulos y sus roles en el juego.
3. `_analisis/09_presupuesto_referencial.md` — ajustar según los módulos MVP confirmados (menos tiempo = menos horas-hombre; más tiempo = más).
4. `_analisis/08_carta_gantt_3_semanas.md` — ajustar cronograma al alcance real MVP.
5. `_analisis/12_inputs_pendientes_de_interlocutor.md` — marcar pregunta 2 como resuelta.

### Pregunta 3 aplicada 2026-08-10 (D-013 + D-014, sin intervención de la clienta)
1. ✅ `docs/decisiones.md` P-004 — cerrado 2026-08-10, reemplazado por D-013.
2. ✅ `docs/decisiones.md` D-013 — dos pilotos en paralelo; decisión técnica del responsable técnico.
3. ✅ `docs/decisiones.md` D-014 (corregida) — concepto real: evento real → NPCs SOMA → caza en teléfono → encuentro RA; el motor es el centro; postulación al fondo = dominio de la clienta.
4. `_analisis/10_opciones_tecnologicas_para_clienta.md` — queda como comparativa histórica (no se edita).
5. `_analisis/11_borrador_propuesta_fondo.md` y `_analisis/09_presupuesto_referencial.md` — material del fondo, dominio de la clienta (D-014); no se intervienen.

### Orden de propagación recomendado
- Estado actual (2026-08-10): Preguntas 1 y 3 resueltas. Pregunta 2 pendiente (no bloquea la maqueta).
- Si INTERLOCUTOR responde 2 antes que la clienta: aplicar propagación de 2, manteniendo ambos paths (A y B) en `_analisis/11_*` y `_analisis/09_*` con módulos actualizados. Luego, al cerrar 3, eliminar el path no elegido.
- Si la clienta responde 3 antes que INTERLOCUTOR responda 2: propagar 3 con paths A o B según elección, pero las secciones afectadas de esos docs quedan marcadas como "ajustar tras Pregunta 2". Doble pasada.
- Si responden en cualquier otro orden: aplicar cada propagación independiente en orden de llegada.

### Cierre del flujo
Cuando la Pregunta 2 esté resuelta, este documento puede archivarse en `_analisis/archive/` (o moverse a una sección histórica). Las referencias en los demás documentos pueden reemplazarse por una nota "ver `decisiones.md` P-004 + D-010-A + D-014 (cerrados)".

Ver también `_analisis/13_resumen_sesion_20260809.md` para el estado completo de la sesión y lecciones aprendidas.

---

## Referencias cruzadas

- `docs/decisiones.md` D-010-A (tabla de módulos, columna "Rol propuesto en el juego", ítems resueltos: clocks 2026-08-09, buses 2026-08-09).
- `docs/decisiones.md` P-004 (cerrado 2026-08-10 por D-013/D-014).
- `docs/estado.md` sección 9.3 (lecciones aprendidas, roles pendientes).
- `_analisis/11_borrador_propuesta_fondo.md` (sección 4.2, referencias a esta pregunta).
- `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` (fuente técnica para pregunta 1).
- `_analisis/10_opciones_tecnologicas_para_clienta.md` (las dos opciones que la clienta elige).
- `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md` (detalle técnico de Opción B).
