# Borrador de propuesta al fondo — Lota Indómito

**Destino:** Concurso público de turismo cultural / patrimonio (cierre fines de agosto o primera semana de septiembre 2026)
**Cliente:** la clienta (CLIENTA)
**Responsable técnico:** INTERLOCUTOR
**Fecha de este borrador:** 2026-08-09
**Estado (2026-08-10):** borrador — material de la postulación al fondo, que es dominio de la clienta (D-014). P-004 fue cerrado por D-013/D-014 (la decisión técnica es del responsable técnico; maqueta con Piloto A). Pendiente: confirmación de roles específicos de módulos MVP en el juego (pregunta 2, D-010-A). (Coexistencia de buses RESUELTA 2026-08-09: convivencia SOMA + Redis Pub/Sub.)

---

## 1. Resumen ejecutivo (250 palabras)

**Lota Indómito: Guardianes de la Cuenca** es un videojuego de exploración y aventuras en mundo real basado en geolocalización (estilo *Pokémon GO*) ambientado en Lota, Chile. El jugador asume el rol de **Explorador del Carbón** o **Guardián de la Memoria** y al recorrer las calles y zonas históricas de la comuna descubre el patrimonio carbonífero (Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor, El Palanquero), completa misiones contextuales, acumula **Carboncillos** (moneda virtual) y sube de rango.

**Producto mínimo viable:** mapa interactivo de Lota con 3-5 zonas patrimoniales, detección automática de entrada a zonas (cercos virtuales), misiones temáticas, insignias y diplomas digitales, reportes ciudadanos hacia un panel municipal, y estadísticas de uso para el Municipio y las instituciones patrimoniales.

**Tecnología:** Lota Indómito es un cliente del framework matemático **Sentinel** — proyecto en producción y financiado del cual se aplican módulos del core S60 (matemática sexagesimal pura, 0 floats, protocolo Yatra): sincronización con eventos celestes reales sobre Lota (Estrellas Reales Aldebarán, Régulo, Antares, Fomalhaut y efemérides de Luna/planetas), pentaresonancia de la lattice pentagonal de 91 nodos, reloj isocrónico de cristal a 41.77 Hz, MycNet como infraestructura mesh distribuida con tolerancia a 50% de pérdida de nodos. Capa de aplicación [Opción A web progresiva o Opción B videojuego multiplataforma en Rust, pendiente elección de la clienta].

**Equipo:** INTERLOCUTOR (responsable técnico y arquitecto del framework Sentinel, 3 semanas de dedicación completa) + la clienta (dirección de contenido, validación patrimonial, vínculo con el Municipio).

**Plazo:** presentación a fines de agosto o primera semana de septiembre 2026.

---

## 2. Problema y oportunidad

Lota (Chile) es un territorio carbonífero con un patrimonio único — el Chiflón del Diablo, los Pabellones 83 y compañía, el Parque Isidora Cousiño, los oficios del mar — que actualmente no tiene una estrategia digital que conecte a los visitantes con la memoria del lugar. Las instituciones patrimoniales carecen de herramientas para medir el interés de la comunidad y de los turistas en los distintos sectores; el Municipio no recibe reportes ciudadanos estructurados; los oficios y relatos del carbón se pierden sin registro vivo.

La oportunidad: una experiencia digital que **transforme el recorrido patrimonial en un juego**, aumente el tiempo de permanencia de los visitantes en Lota, entregue métricas concretas a las instituciones y abra un canal de participación ciudadana.

---

## 3. Solución propuesta

### 3.1 Producto
Una aplicación [web progresiva o videojuego multiplataforma — pendiente elección de la clienta] que el visitante abre en su celular (o computador para la versión de escritorio) y que lo acompaña mientras camina por Lota. Al entrar a una zona patrimonial, el juego se activa y le presenta al personaje histórico correspondiente, le propone una misión contextual y le entrega Carboncillos.

El producto aplica el framework matemático S60 de Sentinel: la sincronización con el cielo real (Estrellas Reales visibles sobre Lota en cada momento), la pentaresonancia del lattice hexagonal de 91 nodos como capa de progresión, el reloj isocrónico de cristal a 41.77 Hz como unidad de tiempo del juego, y MycNet como infraestructura mesh distribuida. Diferenciador único en juegos patrimoniales.

### 3.2 Modalidades de uso
- **Modo Jugador:** experiencia gamificada completa con misiones, ranking, recompensas.
- **Modo Turista:** recorrido contemplativo con audioguías y fotos históricas, sin temporizadores.
- **Modo Familia:** multijugador cooperativo local con roles (Vigía, Cronista, Fotógrafo).

### 3.3 Funcionalidades del MVP
1. Mapa interactivo de Lota con 3-5 zonas patrimoniales priorizadas.
2. Detección automática por GPS al entrar a cada zona (cercos virtuales).
3. Misiones temáticas por zona (ejemplos: *Amasando Pan* en la Ruta Fuego y Carbón, *El Geólogo del Tiempo* en la Ruta Geositio).
4. **Eventos celestes en vivo** (Event Engine de Sentinel): el cielo del juego cambia con el cielo real sobre Lota — quests y personajes se desbloquean cuando una Estrella Real (Aldebarán, Régulo, Antares, Fomalhaut) sale por el horizonte o cuando la Luna entra en fase específica.
5. Sistema de Carboncillos (moneda virtual) con balance y logros.
6. Insignias y diplomas digitales al completar rutas.
7. **Persistencia holográfica distribuida** (Liquid Lattice de Sentinel): estado del jugador y trazabilidad completa de cada acción para narrativa procedural y métricas municipales.
8. **Sincronía del juego** (Isochronous Clock + fases YHWH del framework Sentinel): el día/noche del juego, los eventos globales y las misiones diarias se disparan con la respiración del cristal de tiempo.
9. Reportes ciudadanos (basura, derrumbe, infraestructura) hacia un panel del Municipio.
10. Estadísticas de uso (visitas por zona, rutas más usadas, reportes enviados).

### 3.4 Rutas temáticas previstas
8 rutas que conectan la geografía y la memoria de Lota:
1. **Ruta de las Bodegas** — Logística industrial.
2. **Ruta Geositio** — Valor geológico.
3. **Ruta del Comercio** — Conexión con el comercio local.
4. **Camina Lota** — Urbanismo social y pabellones.
5. **Ruta Costera** — Borde mar y muelles.
6. **Ruta Indómita** — Naturaleza recuperada.
7. **Oficios de Mar** — Patrimonio inmaterial.
8. **Fuego y Carbón** — Gastronomía y artesanía.

El piloto incluye 3-5 rutas priorizadas con la clienta; el resto se desarrolla en fases posteriores.

---

## 4. Tecnología

[Completar tras elección de la clienta.]

### 4.1 [Si Opción A — aplicación web progresiva]
- Interfaz: React 18 + Vite + TypeScript + PWA instalable.
- Mapa: MapLibre GL JS sobre datos abiertos de OpenStreetMap.
- Cercos virtuales: Turf.js en cliente + PostGIS en servidor.
- Servidor: Python FastAPI + Pydantic + PostgreSQL 16 + PostGIS 3.4.

### 4.2 [Si Opción B — videojuego multiplataforma en Rust]

**Arquitectura detallada** (ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` y `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md`):

- **Servidor dedicado (`lota-server`):** Rust puro con `tokio` (runtime asíncrono multihilo) + `axum` (HTTP/WebSocket) + `quinn` (QUIC sobre UDP) + `tokio-tungstenite` (WebSocket). Tick loop interno a 64 Hz con `tokio::time::interval_at`. R-Tree espacial (`rstar`) para geofencing en < 50 nanosegundos por punto en polígono. Opcional `h3o` (H3 hexagonal de Uber) para indexación O(1). Redis Pub/Sub + Streams para eventos globales y cola de tareas asíncronas. PostgreSQL 16 + PostGIS 3.4 para persistencia.
- **Cliente gráfico ultra rápido:** Bevy Engine (ECS puro, paralelización automática multihilo, render WGPU Vulkan/Metal/DX12/WebGPU, 120+ FPS) compilando a nativo (Linux/Win/Android/iOS) y a WASM (WebGPU/WebGL2) para navegador. Técnicas: client-side prediction (0 ms de respuesta visual local) + server reconciliation (lerp ante deltas).
- **Reutilización de módulos del core S60 de Sentinel:** el framework matemático S60 (matemática sexagesimal pura, protocolo Yatra, 0 floats, eBPF que bloquea syscalls float) se aplica en módulos como `mycnet-daemon` (base del servidor HTTP/WS), `mycnet-connect` (traits + handlers asíncronos), `SOMA` (orquestación con contratos, validación y bus Pub/Sub sobre Redis), y `mycnet-core S60/utils` (utilidades matemáticas deterministas para cálculos exactos compartidos cliente-servidor).

**Sincronización entre mundo real y mundo digital:**

- **`IsochronousClock` de Sentinel (41.77 Hz, base-60, sin drift de fase) es el reloj maestro** del proyecto. Provee la sincronización con eventos del mundo real (estrellas visibles sobre Lota, fase lunar, mareas, eventos celestes en general, eventos comunitarios en vivo) **con exactitud matemática** (base-60 sin redondeos flotantes) y **baja latencia** (sub-microsegundo).
- El tick loop del juego a 64 Hz (`lota-server`) corre subordinado al reloj maestro: cada N ticks de simulación se alinea con el tick del cristal (Salto-17 cada 68 ticks de Sentinel ≈ 1 tick cada ~1.6 segundos, correspondiente a fases de cambio de hora del mundo real).
- **Implicación:** los eventos del juego (quests basadas en cielo real, misiones diarias, cambios de fase día/noche, eventos globales) disparan desde el `IsochronousClock` sin drift, y el cliente los recibe vía `lota-server` con baja latencia de red (p95 RTT < 50ms, failover < 1s, tolerancia 50% pérdida de nodos en MycNet mesh).
- **Buses de eventos (RESUELTO 2026-08-09):** coexistencia confirmada por INTERLOCUTOR — SOMA (Sentinel, fase YHWH en VAV) + Redis Pub/Sub de `lota-server`. SOMA = dispatch interno coherente con pentaresonancia; Redis = transporte cliente-servidor y entre instancias. Convivencia provisional — revisar con datos de testing bajo carga real. Ver `_analisis/12_inputs_pendientes_de_interlocutor.md` pregunta 1 y `docs/decisiones.md` D-010-A.

**Sistema celestial soberano:** matemática base-60 propia (sin decimales flotantes, protocolo Yatra), sincronizado con estrellas reales sobre Lota (Estrellas Reales Aldebarán, Régulo, Antares, Fomalhaut; efemérides de Luna y planetas visibles). El juego reacciona al cielo real del jugador. Esta capa matemática es provista por el core S60 de Sentinel (proyecto en producción y financiado del cual Lota Indómito es cliente).

- Piloto en modo virtual (teletransporte a las zonas) para validar el recorrido sin necesidad de estar físicamente en Lota.
- GPS real en celulares en fase 2.

---

## 5. Equipo

| Rol | Persona | Dedicación |
|---|---|---|
| Responsable técnico, arquitecto del framework matemático y desarrollador | INTERLOCUTOR | 3 semanas de tiempo completo + coordinación post-lanzamiento. Arquitecto principal de Sentinel (framework matemático S60 en producción y financiado del cual Lota Indómito es cliente). |
| Dirección de contenido y validación patrimonial | la clienta (CLIENTA) | 3 semanas de tiempo parcial + vínculo con Municipio |
| [Diseñador de interfaz y experiencia de usuario — por confirmar] | — | 1 semana |

---

## 6. Cronograma

Ver `_analisis/08_carta_gantt_3_semanas.md` para el detalle semana a semana.

| Semana | Foco |
|---|---|
| 1 (10-16 ago) | Postulación escrita + demo de presentación |
| 2 (17-23 ago) | Iteración de demo con la clienta + ajuste de propuesta |
| 3 (24-30 ago) | Cierre de propuesta + envío a fondo |
| Semana de gracia (31 ago - 6 sep) | Respuesta a observaciones del fondo |

---

## 7. Presupuesto

Ver `_analisis/09_presupuesto_referencial.md` para el desglose.

- Honorarios de INTERLOCUTOR y la clienta.
- Infraestructura (servidor autoalojado).
- Diseño y contenido.
- Imprevistos.

---

## 8. Impacto esperado

- **Patrimonial:** visibilización del patrimonio carbonífero de Lota ante visitantes nacionales e internacionales.
- **Educativo:** aprendizaje vivencial sobre la historia del carbón, oficios del mar y arquitectura de pabellones.
- **Ciudadano:** canal directo de reportes desde los visitantes hacia el Municipio.
- **Institucional:** métricas concretas de uso y de reportes para la toma de decisiones del Municipio y el Consejo de Monumentos Nacionales.
- **Económico:** prolongación de la estadía de turistas en Lota y dinamización del comercio local (canje de Carboncillos en locales asociados en fase 2).
- **Tecnológico diferenciador:** el proyecto aplica el framework matemático soberano S60 de Sentinel (base-60 puro, 0 floats, protocolo Yatra) — el primer juego patrimonial del Biobío con matemática soberana sincronizada con cielo real, sin dependencia de Google Maps ni decimales flotantes. Esto abre una línea de investigación reproducible sobre integración de matemática espacial en aplicaciones culturales.
- **Científico-académico:** el framework Sentinel tiene base documental cotejada (papers arXiv + Mansfield & Wildberger 2017 sobre Plimpton 322, Muir & Nikiforakis 2022 sobre MHD, Dicke 1954 sobre superradiancia, vis-viva Kepler). Lota Indómito es un caso de estudio público de aplicación de esa matemática a patrimonio cultural.

---

## 9. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Plazo ajustado (3 semanas hasta cierre) | Cronograma conservador con semana de gracia; demo de presentación lista a fin de semana 1 |
| Disponibilidad del Municipio para avales | la clienta gestiona vínculo institucional desde semana 1 |
| Calidad del mapa en zonas rurales | Validación previa con OpenStreetMap; completar con datos del Municipio si es necesario |
| Cobertura GPS en interiores | Plan alternativo con registro por código QR como respaldo |
| Cambio de prioridades del fondo | Diseño modular permite pivote entre opciones A y B sin reescritura total |
| Acoplamiento con framework Sentinel en plazos ajustados | Sentinel ya está implementado y en producción; los módulos a aplicar están maduros. No se requiere reescritura, solo integración. Validar disponibilidad de INTERLOCUTOR como mantenedor activo durante el piloto. |
| Licencia del código Sentinel (Apache 2.0 + cláusula No Comercial) | Autorizado explícitamente por INTERLOCUTOR (D-009 en `docs/decisiones.md`). Mantener atribución obligatoria y encabezado de licencia en código derivado. Lota Indómito es proyecto financiado con fondos públicos, no comercial. |
| Complejidad del protocolo Yatra (sin float en core) | El equipo desarrollador (INTERLOCUTOR) ya tiene experticia en SPA. Ningún módulo de cálculo core del juego debe usar f32/f64 — usar S60 del framework. |

---

## 10. Próximos pasos

1. **Semana en curso:** definir stack con la clienta (Opción A o B), priorizar 3-5 zonas patrimoniales, asegurar avales institucionales.
2. **Confirmar roles específicos de módulos Sentinel en el juego:** INTERLOCUTOR revisa y ajusta los roles propuestos en D-010-A de `docs/decisiones.md` antes de cerrar la propuesta técnica.
3. **Semana 1:** producir demo jugable + primer borrador de propuesta escrita.
4. **Semana 2:** iteración con la clienta y stakeholders.
5. **Semana 3:** cierre y envío al fondo.

---

## Anexos (a adjuntar)

- Documento de diseño del juego (`docs/concepto-juego.md`).
- Documento de opciones tecnológicas (`_analisis/10_opciones_tecnologicas_para_clienta.md`).
- Investigación de motores Rust para juegos (`_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md`).
- Propuesta de arquitectura del servidor Rust del juego (`_analisis/07_propuesta_arquitectura_servidor_rust_juego.md`).
- Comparativa de tecnologías (`_analisis/05_analisis_tecnologias_disponibles.md`).
- Carta Gantt detallada (`_analisis/08_carta_gantt_3_semanas.md`).
- Presupuesto referencial (`_analisis/09_presupuesto_referencial.md`).
- Inputs pendientes centralizados (`_analisis/12_inputs_pendientes_de_interlocutor.md`).
- Resumen de la sesión 2026-08-09 (`_analisis/13_resumen_sesion_20260809.md`).
- Capturas del prototipo Stitch (referencia visual).
