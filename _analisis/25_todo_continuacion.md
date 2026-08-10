# TODO consolidación — continuación post 2026-08-10

> **Documento de continuidad.** Estado del proyecto tras la sesión de diseño del 2026-08-10.
> **Próxima sesión:** leer este archivo + `MEMORY.md` (encuadre vigente D-014) + `docs/decisiones.md` + `docs/estado.md` §11.

---

## 1. Estado del repo tras la sesión

- **Rama:** `main`, sincronizada con `origin/main`.
- **Commits nuevos pusheados (sesión 2026-08-10):**
  - `1e5ab7d` concepto: añadir 4 docs de diseño (World Events, ML, monedas, subastas).
  - `7978cda` docs: propagar al GDD el sistema multi-moneda, World Events, subastas y ML externo.
- **Commits previos pendientes de push (también ya pusheados):**
  - `8a92131` docs: rediseñar Core Game Loop — loop de visita y retorno del turista.
  - `8bc3466` docs: registrar rediseño del Core Game Loop en CHANGELOG.
  - `b36bb2e` piloto A: mapa con polígonos reales de Lota (Overpass API).

## 2. Trabajo ajeno intacto (NO se commiteó, regla TRABAJO AJENO)

- `_analisis/19_investigacion_tecnologias_y_proyectos_referencia.md` (sin seguimiento).
- `piloto-a/package-lock.json`, `piloto-a/package.json`, `piloto-a/src/App.vue`, `piloto-a/src/components/MapaLota.vue`.
- `piloto-a/public/data/`, `piloto-a/src/data/`.

Si esto es trabajo en curso tuyo, decime "cámbialo" y lo commiteo.

## 3. Decisiones pendientes de aprobación

### D-016 · Sistema multi-moneda cobre/oro/estaño — **PROPUESTA**
- Diseño completo en [`_analisis/23_sistema_monedas_minerales.md`](23_sistema_monedas_minerales.md).
- Requiere OK explícito de INTERLOCUTOR para reemplazar Carboncillo formalmente.
- Si se aprueba: propagar a otros docs (`propuesta-fondo.md` es dominio de cliente — verificar alcance), implementar wallet en Piloto A.

### D-017 · Subastas digitales de cosas reales — **PROPUESTA**
- Diseño completo en [`_analisis/24_subastas_reales.md`](24_subastas_reales.md).
- Requiere OK explícito de INTERLOCUTOR.
- Si se aprueba: diseñar backend, integrar con wallet multi-moneda, validar regulación chilena.

## 4. Decisiones de diseño abiertas (por doc)

### Doc 23 (monedas minerales) — 6 decisiones
1. ¿Ratio fijo o fluctuante en piloto?
2. ¿Quién define el ratio?
3. ¿Hay límite total de cada mineral en circulación?
4. ¿Se pueden comprar minerales con dinero real?
5. ¿Mercado abierto en piloto o solo trueque bilateral?
6. ¿Inscripción del comercio: abierta o curada?

### Doc 24 (subastas reales) — 3 decisiones
1. ¿Geocerca o cupón digital libre?
2. ¿Caducidad rígida estilo WoW o flexible?
3. ¿Movimiento de NPCs: ruta fija o S60-driven?

### Doc 22 (ML externo) — 4 decisiones
1. ¿DB local (servidor fan) o nube?
2. ¿Stack Python confirmado?
3. ¿Quién opera el servicio de ML?
4. ¿El dashboard es público o restringido?

### Doc 21 (World Events) — 4 decisiones
1. ¿Quién opera el calendario de World Events?
2. ¿Solo Lota o también expansión regional?
3. ¿Geocerca para activar el cupón?
4. ¿Caducidad rígida o flexible?

### Doc 20 (loop del jugador) — 4 preguntas
1. ¿Quién opera el Calendario del Cielo?
2. ¿El modo virtual (teleport) entra en el piloto?
3. ¿Inscripción al evento individual o grupal?
4. ¿Portales S60 solo en Lota o en otras comunas?

**Total:** 21 decisiones abiertas, todas con recomendación en su doc respectivo. Requieren OK explícito para bajar a mecánica o implementación.

## 5. Trabajo de implementación pendiente

### Piloto A (PWA Vue 3 + MapLibre) — sprint del mes
- [ ] Wallet multi-moneda (3 minerales, ratios fijos, UI simple).
- [ ] Geofencing cliente con Turf.js.
- [ ] Anatomía de micro-sesión 1-5 min (5 tramos: trigger, contexto, acción, recompensa, próximo).
- [ ] Instrumentación de 16 eventos anónimos para ML externo.
- [ ] 1 World Event demo (fecha real cercana, 1 NPC exclusiva caminando, 1 misión con comercio real, 1 insignia exclusiva).
- [ ] 1 comercio real asociado con cupón QR multi-moneda.
- [ ] 1 listing demo para venta con pago en cobre (sin subasta completa).
- [ ] URL pública del pasaporte (efecto red).
- [ ] Render HTML del sitio (`index.html` + `render-docs.py`).

### Backend (NUEVO, no existe aún)
- [ ] PostgreSQL + PostGIS (D-006).
- [ ] Servicio de sincronización del wallet multi-moneda.
- [ ] Servicio de subastas (cuando D-017 se apruebe).
- [ ] Servicio de ML externo (cuando haya volumen).
- [ ] Vistas materializadas para ML.

### Piloto B (motor GPU + Sentinel) — centro del concepto
- [ ] Geofencing con R-Tree (`rstar`) — pendiente del concepto.
- [ ] NPCs del enjambre SOMA móviles (mecánica de movimiento S60).
- [ ] Integración del motor con el PWA cliente.

### Material para el fondo
- [ ] `[doc retirado]` — actualizar con D-016 y D-017 si se aprueban.
- [ ] `[doc retirado]` — ajustar al alcance MVP real.
- [ ] `_analisis/08_CARTA_GANTT_3_semanas.md` — ajustar al cronograma real.

> **Nota del proyecto:** el material de fondo (`_analisis/08_*`, `_analisis/09_*`, `_analisis/11_*`, `[doc retirado]`) es **dominio de cliente**. INTERLOCUTOR no se mete en la postulación; INTERLOCUTOR prepara el proyecto y su diseño.

## 6. Input requerido de terceros

### cliente / Municipio
- Fechas exactas de festividades locales de Lota (aniversario, semana del carbón, fiesta patronal).
- Selección de 1 comercio real para el piloto (cupones QR, canje de minerales).
- Validación del modelo de autofinanciamiento (D-014).

### INTERLOCUTOR (decisiones de arquitectura)
- Aprobar D-016 y D-017 formalmente.
- Resolver las 21 decisiones de diseño abiertas (lista en §4).
- Definir operador del servicio de ML (¿él mismo, cliente, externo?).
- Decidir si DB va en servidor fan o nube.

## 7. Pitch consolidado para el fondo

> "Lota Indómito no es solo un juego — es una **plataforma económica soberana** donde los usuarios acumulan minerales (cobre, oro, estaño) explorando el patrimonio, y luego pueden **comprar productos reales del comercio local** en subastas digitales. El juego se sincroniza con festividades reales (Fiestas Patrias, San Juan, Día del Patrimonio), tematiza la experiencia con NPCs exclusivos que caminan por el mapa, y coordina flujos turísticos hacia el comercio. Un servicio de ML entrega dashboards accionables para Municipio y comercio, justificando la inversión pública con datos reales."

Esa propuesta es difícil de rechazar para un Municipio que busca reactivación económica del patrimonio.

## 8. Cómo retomar la próxima sesión

1. **Leer este archivo** (`_analisis/25_todo_continuacion.md`).
2. Releer `MEMORY.md` (encuadre vigente D-014).
3. Revisar `docs/decisiones.md` (D-014 a D-017).
4. Si vas a aprobar D-016/D-017: hacerlo explícito antes de propagar más.
5. Si vas a implementar Piloto A: empezar por el wallet multi-moneda.
6. Si vas a implementar Piloto B: revisar [`_analisis/17_arquitectura_gpu_motor_lota.md`](17_arquitectura_gpu_motor_lota.md).
7. Si vas a iterar concepto: retomar `docs/estado.md` §11.

## 9. Referencias cruzadas

- **MEMORY.md** — encuadre vigente (D-014 corregida).
- **docs/decisiones.md** — D-001 a D-017.
- **docs/estado.md** — estado vivo del proyecto, sección 11 = workstream activo.
- **docs/concepto-juego.md** — GDD actualizado.
- **`_analisis/20_loop_jugador_dia_a_dia.md`** — loop del turista.
- **`_analisis/21_world_events_d014.md`** — World Events.
- **`_analisis/22_ml_analytics_d014.md`** — ML externo.
- **`_analisis/23_sistema_monedas_minerales.md`** — multi-moneda (D-016).
- **`_analisis/24_subastas_reales.md`** — subastas reales (D-017).
