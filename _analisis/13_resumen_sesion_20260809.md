# Resumen de sesión — 2026-08-09

**Sesión:** Hermes, modelo opencode-pro vía omniroute
**Lota Indómito:** cliente de Sentinel, postulación a fondos públicos (cierre fines de agosto / primera semana de septiembre 2026)
**Cliente:** cliente (cliente)

---

## Qué se hizo en esta sesión

### Decisiones registradas en `docs/decisiones.md`

- **D-004** · Entregable para el fondo = propuesta + maqueta + demo frontend.
- **D-005** · Alcance del piloto = lean (doc 04, sin 3D ni minijuegos).
- **D-006** · Backend Fase 1 = Python FastAPI.
- **D-007** · Frontend = React 18 + Vite + TypeScript.
- **D-008** · El stack del juego lo elige cliente de un menú de opciones (P-004 abierto).
- **D-009** · Autorización de uso de `celestial.rs/py` en Lota Indómito (Apache 2.0 + cláusula No Comercial, autorización de INTERLOCUTOR como autor).
- **D-010** · Lota Indómito integra módulos matemáticos del core S60 de Sentinel (celestial como caso de uso). Reescrito tras análisis crítico.
- **D-010-A** · Módulos del framework Sentinel identificados para integrar al juego, con roles propuestos pendientes de confirmación. Resuelto el R&D clocks (IsochronousClock 41.77 Hz maestro, tick juego subordinado); queda abierto R&D buses.

### Documentos nuevos / actualizados

| Archivo | Tamaño | Estado |
|---|---|---|
| `docs/decisiones.md` | 208 líneas | Modificado — incluye D-004 a D-010 + D-010-A + P-001 a P-004 |
| `docs/estado.md` | 148 líneas | Modificado — cliente registrada en "Quién es quién" + sección 9 "Lecciones aprendidas" con referencia a skills oficiales de Sentinel y al doc 12 |
| `_analisis/08_CARTA_GANTT_3_semanas.md` | 110 líneas | Nuevo — cronograma 3 semanas |
| `[doc retirado]` | 124 líneas | Nuevo — desglose [monto retirado], Opción A y B |
| `[doc retirado]` | 101 líneas | Antes `06_*`, renombrado para liberar slot 06 |
| `[doc retirado]` | 185 líneas | Antes `07_*`, renombrado para liberar slot 07 |
| `_analisis/12_inputs_pendientes_de_interlocutor.md` | 171 líneas | Nuevo — centraliza las 3 preguntas pendientes + cómo se propagan respuestas |

**Renombramientos en `_analisis/`:**

- `06_opciones_tecnologicas_para_clienta.md` → `10_opciones_tecnologicas_para_clienta.md`
- `07_borrador_propuesta_fondo.md` → `11_borrador_propuesta_fondo.md`

Libera slots `06_*` y `07_*` para los archivos de INTERLOCUTOR (`06_investigacion_motores_rust_juegos_ultra_rapidos.md` y `07_propuesta_arquitectura_servidor_rust_juego.md`).

### Conflictos y archivos no tocados

- `_analisis/04_propuesta_tecnica_stack_osm.md` — eliminado por INTERLOCUTOR; quedan `.conflict1`/`.conflict2` como artefactos. **No tocar.**
- `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md` — INTERLOCUTOR. Referenciado desde doc 10 y doc 11 (Opción B).
- `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` — INTERLOCUTOR. Referenciado desde doc 10 y doc 11 (Opción B).
- `_analisis/05_analisis_tecnologias_disponibles.md` — pre-existente, no tocado.
- `whatsapp/` y `stitch_lota_indomito_*` — gitignored por peso, en Drive. No en repo.

### Demo scaffold React

**Cancelado** — pivote a menú de opciones para cliente (D-008, P-004). Se retoma según elección de cliente.

---

## Qué está pendiente (3 preguntas explícitas)

Centralizadas en `_analisis/12_inputs_pendientes_de_interlocutor.md`:

| # | Pregunta | Bloqueado por |
|---|---|---|
| 1 | SOMA vs Redis Pub/Sub — ¿conviven como capas distintas, o uno reemplaza al otro? | INTERLOCUTOR |
| 2 | Roles específicos de módulos MVP en el juego — confirmación de roles, MHD en MVP o Fase 2, Hexagonal/Quantum/Crystal Lattice mantener/descartar | INTERLOCUTOR |
| 3 | Opción A (web progresiva) vs Opción B (videojuego Rust + servidor propio `lota-server`) | cliente |

### Tareas bloqueadas por las respuestas

- `[doc retirado]` sección 4 — ramas A/B según elección cliente, módulo buses según Pregunta 1, roles según Pregunta 2.
- `[doc retirado]` — ramas A/B según elección cliente.
- `_analisis/08_CARTA_GANTT_3_semanas.md` — alcance real según Pregunta 2.
- `[doc retirado]` — cerrar como comparativa o como opción única según Pregunta 3.
- `docs/decisiones.md` P-004 — registrar decisión de cliente.
- `docs/decisiones.md` D-010-A — actualizar con confirmación de roles y buses.

---

## Lecciones aprendidas (resumen)

1. **Skills oficiales de Sentinel** son `sentinel-knowledge-layer`, `sentinel-comprehension`, `sentinel-s60-stack` (en `/home/jnovoas/Proyectos/sentinel/docs/07_prompts/`). NO son `s60-dev`, `complex-spa`, `quantum-time-crystals`, `optomechanical-cooling`, `buffer-systems` (genéricas del ecosistema base-60, no del proyecto Sentinel). Documentado en `docs/estado.md` 9.1.

2. **Sentinel es framework matemático S60 para Linux, en producción y financiado.** Lota Indómito es **cliente** de Sentinel: aplica módulos del core S60 al caso de uso del juego. NO es producto independiente que desarrolla el framework desde cero. Documentado en `docs/estado.md` 9.2.

3. **"Implementado y financiado" se refería a Sentinel**, no a Lota Indómito. Documentado en `docs/decisiones.md` D-010.

4. **`IsochronousClock` 41.77 Hz de Sentinel es el reloj maestro** que sincroniza mundo real y mundo digital con exactitud matemática y baja latencia. El tick loop del juego a 64 Hz (`lota-server`) corre subordinado al reloj maestro. Documentado en `[doc retirado]` sección 4.2 y `docs/decisiones.md` D-010-A R&D clocks (resuelto).

5. **Error central de la sesión**: reducir el sistema celestial a "feature de geofencing del juego" o "posicionamiento del peatón" sin haber leído el código ni los docs reales. Corregido tras 4+ mensajes de retroalimentación de INTERLOCUTOR cargando las 3 skills oficiales. Documentado en `docs/estado.md` 9.1 y 9.3.

---

## Estado del repo (`git status --short`)

```
 M docs/_render/render-docs.py          (modificado por INTERLOCUTOR)
 M docs/concepto-juego.md              (modificado por INTERLOCUTOR)
 M docs/decisiones.md                  (modificado en esta sesión)
 M docs/estado.md                      (modificado en esta sesión)
 D _analisis/04_propuesta_tecnica_stack_osm.md   (eliminado por INTERLOCUTOR)
?? _analisis/04_propuesta_tecnica_stack_osm.md.conflict1   (artefacto)
?? _analisis/04_propuesta_tecnica_stack_osm.md.conflict2   (artefacto)
?? _analisis/05_analisis_tecnologias_disponibles.md          (pre-existente)
?? _analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md   (INTERLOCUTOR)
?? _analisis/07_propuesta_arquitectura_servidor_rust_juego.md        (INTERLOCUTOR)
?? _analisis/08_CARTA_GANTT_3_semanas.md                     (esta sesión)
?? [doc retirado]                   (esta sesión)
?? [doc retirado]        (esta sesión, antes 06_*)
?? [doc retirado]                  (esta sesión, antes 07_*)
?? _analisis/12_inputs_pendientes_de_interlocutor.md         (esta sesión)
?? _analisis/13_resumen_sesion_20260809.md                  (este archivo)
```

---

## Acción recomendada para próxima sesión

1. INTERLOCUTOR responde Preguntas 1 y 2 del doc 12 (cuando pueda, sin esperar a cliente).
2. cliente elige Opción A o B (reunión + decisión en P-004).
3. Con las 3 respuestas, ejecutar propagación según sección "Cómo se propagan las respuestas" del doc 12.
4. Cerrar `_analisis/11_borrador_*`, `_analisis/08_CARTA_GANTT_*`, `_analisis/09_presupuesto_*` y `_analisis/10_opciones_*`.
5. Archivar `_analisis/12_inputs_pendientes_de_interlocutor.md` y este resumen (`13_resumen_sesion_*`) en `_analisis/archive/` cuando todas las preguntas estén resueltas.