# Lota Indómito — Concepto del juego (Game Design Document)

**Título:** *Lota Indómito: Guardianes de la Cuenca*  
**Género:** Geo-RPG / Juego de exploración urbana, patrimonio y aventuras  
**Plataforma:** Web PWA Mobile-First (Vue 3 + TypeScript + MapLibre GL — decisión D-007)  
**Estilo Visual:** Retro-industrial + futurista-gamer (Turquesa `#3FE6C0`, Coral `#F5A285`, Cobre `#D17A4F`, fondo nocturno `#0F1216`)

---

## 1. Visión general del juego

*Lota Indómito* es un juego de exploración y aventuras en mundo real basado en geolocalización (estilo *Pokémon GO*). El jugador asume el rol de **Explorador del Carbón** o **Guardián de la Memoria**. 

Al recorrer las calles y zonas históricas de Lota (Chile), el jugador descubre zonas patrimoniales, interactúa con espíritus y personajes emblemáticos del pasado, resuelve minijuegos contextuales, junta **minerales del juego** (cobre, oro, estaño — un sistema multi-moneda que reemplazó al antiguo Carboncillo) y sube de rango en el pasaporte digital.

---

## 2. Core Game Loop (Ciclo principal del juego)

> **Diseño actualizado (2026-08-10):** el loop de encuentro que sigue es la **unidad atómica** dentro de un **loop de visita**. El día-a-día del turista se compone de ~6-10 micro-sesiones durante 1-2 días en Lota, más un loop de retorno posterior (D+1 → D+30) que ata al turista a la próxima visita. Diseño completo en [`_analisis/20_loop_jugador_dia_a_dia.md`](../_analisis/20_loop_jugador_dia_a_dia.md).
>
> **Tesis:** para un turista de paso (1-2 días en Lota) no hay loop diario tradicional. Hay **loop de visita** (dentro de la estadía) y **loop de retorno** (post-visita). Las mecánicas clásicas de mobile (racha diaria, energía que regenera) NO aplican y se descartan — ver §2.5.

### 2.1 El loop de visita (dentro de 1-2 días en Lota)

```
┌─────────────────────────────────────────────────────────────────┐
│            MICRO-SESIÓN (1-5 min, 6-10 por visita)              │
│   Trigger (geofence) → Contexto (NPC + diálogo) →               │
│   Acción (minijuego o escaneo) → Recompensa →                   │
│   Dirección (siguiente POI o evento del cielo)                   │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                       (Repetición n veces durante la visita)
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│         EVENTO DEL CIELO (5-30 min, 1-3 por día de visita)      │
│   Ventana corta con anuncio anticipado. Determinista, movido     │
│   por Sentinel S60: astronómico, climático, temporal, portal.   │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│               CANJE EN COMERCIO LOCAL (D-014)                   │
│   Sugerencia al turista antes de dormir: "Hay una panadería     │
│   con descuento a 200 m." Gasta cobre/oro, ata el juego        │
│   al comercio real. Esta es la pieza que convierte el juego     │
│   en motor de reactivación económica de Lota.                    │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PASAPORTE DIGITAL                           │
│   Stats finales, diploma descargable, % completado.             │
│   URL pública compartible (efecto red).                          │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 El loop de retorno (después de irse)

```
D+1  →  "Tu pasaporte está al 75%. Vuelve antes del [evento]."
D+7  →  Newsletter del cielo con la próxima ventana importante.
D+30 →  "Lota tiene 3 eventos esta temporada. ¿Vienes?"
```

Mecánicas activas: pasaporte incompleto, calendario del cielo público (1 año adelantado), cupones con caducidad (30-60 días), contenido nuevo por temporada.

### 2.3 Anatomía de la micro-sesión (1-5 min)

| Tramo | Tiempo | Qué pasa | Regla dura |
|---|---|---|---|
| **Trigger** | 0-15 s | Vibración + banner: *"Estás en el Chiflón del Diablo. Toca para descubrir."* | Geofencing cliente (Turf.js). Sin texto antes del tap. |
| **Contexto** | 15-60 s | Mapa mini + avatar del personaje histórico + 2-3 frases de diálogo + audio opcional | Sin scrolls. Sin muros de texto. ≤30 palabras en pantalla. |
| **Acción** | 60-180 s | Minijuego táctil corto (QTE, hidden object, trivia) o escaneo de cámara | Pre-cargado. Cero loading entre tramos. **1 acción por micro-sesión.** |
| **Recompensa** | 180-240 s | +cobre (o +oro según evento), +XP, animación de insignia, *"Has rescatado un fragmento del patrimonio."* | Siempre gana algo. Nunca "casi". Si pierde → retry sin penalización. |
| **Próximo** | 240-300 s | *"La próxima zona está a 320 m al sur."* Mini-mapa con ruta | Nunca terminar sin dirección. La pantalla siempre cierra con un "hacé X". |

**Variantes del tramo Acción según modo:**

- **Jugador** = 90 s de acción dura (QTE, puzle, estratigrafía).
- **Turista** = 0 s (escaneo + foto, sin minijuego).
- **Familia** = rol-asignado, todos participan en su rol (Vigía / Cronista / Fotógrafo).

### 2.4 Catálogo de eventos del cielo (resumen)

- **Astronómicos** (anuales): salida/puesta de sol, luna llena/nueva, equinoccios, solsticios.
- **Climáticos** (ventana corta, parcialmente impredecibles): niebla en el Parque, marejada en el Borde Costero, lluvia en el Chiflón.
- **Temporales** (recurrentes): Amanecer del Minero 07:00, Hora del Trueque 14:00, Atardecer del Carbón 19:00, Noche de las Chinchorreras 22:00.
- **Raros (S60)** — el diferenciador central: portales cuando `|amp_A - amp_B| < SCALE_0 / 50` en GPU. **Estaño único** (no se repite). Diploma *"Cazador de Portales"*.

> Cada evento tiene ventana corta (5-30 min) → urgencia real, no FOMO cosmético. Se anuncian con 5-15 min de anticipación, pero el marcador no aparece en el mapa hasta cerca de la hora. El **Calendario del Cielo** los lista con horario exacto para que el turista planifique su visita.

### 2.5 Lo que se descarta del modelo "loop diario" clásico

Para un turista de paso, las siguientes mecánicas **NO aplican** y se sacan del diseño:

- Racha diaria / streak con penalización por skip.
- Energía que regenera con tiempo real.
- Notificación genérica *"vuelve a jugar"*.
- Cualquier mensaje del tipo "hoy no jugaste" — para un turista de 1-2 días, es ruido insoportable.

El retorno se logra por **pasaporte incompleto + calendario del cielo + cupones con caducidad**, no por hábito forzado.

---

## 3. Mecánicas de juego y minijuegos por ruta

Cada una de las 8 rutas temáticas de la comuna activa una mecánica de juego o minijuego exclusivo:

| Ruta | Minijuego | Mecánica de juego |
|---|---|---|
| **Fuego y Carbón** | *Amasando Pan* | Minijuego QTE y ritmo táctil para sobar, amasar y hornear pan de mina en horno de barro. |
| **Ruta Geositio** | *El Geólogo del Tiempo* | Puzle estratigráfico donde el jugador clasifica capas de carbón, fósiles y rocas según eras geológicas. |
| **Ruta de las Bodegas** | *El Inventario del Carbón* | Búsqueda de objetos 3D ocultos (hidden object game) entre las herramientas y ruinas industriales. |
| **Oficios de Mar** | *Chinchorreando en el Blanco* | Minijuego de física donde se ajusta la fuerza y dirección para lanzar la red de pesca artesanal. |
| **Camina Lota** | *Arquitecto de Pabellones* | Superposición de fotos históricas vs actual; encuadre exacto para reconstruir el pabellón en 3D. |
| **Ruta del Comercio** | *El Trueque Lota* | Minijuego de gestión y canje de minerales en puestos del comercio local. |
| **Ruta Costera** | *Vigía del Golfo* | Desafío de avistamiento con prismáticos virtuales para identificar la fauna del borde costero. |
| **Ruta Indómita** | *Rastreador de la Flora* | Trivia botánica interactiva con pistas de la vegetación nativa del Parque de Lota. |

---

## 4. Sistema de economía in-game (minerales)

> **Diseño actualizado (2026-08-10, D-016 aprobada el 2026-08-12):** la moneda única **Carboncillo** (`₡`) se reemplaza por un **sistema multi-moneda de minerales** con tipo de cambio relativo, transferible entre usuarios y comercianteable en el comercio local. Esto refuerza D-014 (autofinanciamiento) y potencia la interacción social. Diseño completo en [`_analisis/23_sistema_monedas_minerales.md`](../_analisis/23_sistema_monedas_minerales.md).

### 4.1 Catálogo de minerales

| Mineral | Símbolo | Valor relativo | Identidad | Rareza |
|---|---|---|---|---|
| **Cobre** | Cu | 1 unidad (base) | Metal del trabajo y del comercio diario | Común |
| **Oro** | Au | 100 cobre | Metal del cielo, de los eventos, de la historia | Media |
| **Estaño** | Sn | 10.000 cobre (= 100 oro) | Metal de los portales S60, de las rarezas, del juego completo | Rara |

**Reglas duras:**
- Cobre se gana en misiones de comercio, World Events diarios y POIs fijos.
- Oro se gana en eventos del cielo y World Events temáticos.
- Estaño **solo** se gana en portales S60 (convergencia de lattice) y pasaporte 100%. Es el mineral más escaso y de mayor poder adquisitivo real.
- Ratios MVP: **1 estaño = 100 oro = 10.000 cobre**. Ratios fijos en piloto, fluctuantes en fase 1.

### 4.2 Formas de ganar minerales

| Acción | Mineral ganado | Cantidad |
|---|---|---|
| Micro-sesión de POI fijo completada | Cobre | 10-50 |
| Reporte ciudadano validado | Cobre | 75 |
| World Event: 1 misión temática completada | Cobre + Oro | 30 cobre + 5 oro |
| World Event: ruta completa del evento | Oro | 100-500 |
| Evento del cielo (astronómico, climático, temporal) | Oro | 20-100 |
| Portal S60 (convergencia lattice) | Estaño | 1 |
| Pasaporte digital al 100% completado | Estaño + Diploma | 10 |
| Logro "Leyenda Indómita" | Estaño + Título | 5 |

### 4.3 Usos y canje

- **Canje real en locales asociados:** descuento en restaurant, café, completo, panadería, artesanía (vía cupón QR). Ver §6 de [`_analisis/21_world_events_d014.md`](../_analisis/21_world_events_d014.md).
- **Transferencia P2P:** envío de cobre/oro/estaño entre usuarios por QR o nickname.
- **Trueque bilateral:** un jugador ofrece cobre+oro a cambio de estaño de otro.
- **Subastas digitales de cosas reales:** productos del comercio local subastados en minerales del juego. Ver §11.
- **Personalización in-game:** desbloqueo de marcadores de mapa personalizados, marcos para el Pasaporte y títulos de avatar.
- **Bóveda de Diplomas:** emisión de diplomas digitales de honor descargables en PDF.

### 4.4 Reglas anti-abuso y antifraude

- Límite diario de transferencia configurable por jugador.
- Cooldown entre transferencias al mismo jugador.
- Reporte de estafa con moderación manual.
- Historial público en el perfil del jugador.
- Estaño con stock limitado (≈1.000 unidades en circulación) para preservar escasez.

---

## 5. Sistema de progresión y rangos

El jugador acumula experiencia y **portafolio de minerales** (cobre principalmente) para avanzar en los rangos del pasaporte:

| Rango | Cobre acumulado (equivalente) | Desbloqueables |
|---|---|---|
| **Aprendiz del Carbón** | 0 – 500 Cu | Brújula básica, 3 zonas iniciales |
| **Capataz de la Cuenca** | 501 – 2.000 Cu | Modo Multijugador Familiar, 5 zonas adicionales, skins |
| **Leyenda Indómita** | 2.001+ Cu (o 1+ Sn) | Pasaporte de Oro, Diplomas PDF de Honor, Medalla de la Comuna |

**Nota:** el rango se calcula sobre el portafolio total (cobre + oro*100 + estaño*10000). Conseguir 1 estaño equivale automáticamente al rango máximo.

### Medallas especiales
- 🏅 **Ojo de Lince:** 5 reportes ciudadanos validados en el dashboard municipal.
- 🍞 **Amasadora de Memorias:** Puntaje máximo en el minijuego de pan de mina.
- 🌊 **Vigía del Golfo:** Completar toda la Ruta Costera y Oficios de Mar.
- ⛏️ **Cazador de Portales:** cerrar al menos 1 portal S60 (recibe estaño).

---

## 6. Modos de juego

### 6.1 Modo Jugador (Turquesa `#3FE6C0`)
- Experiencia gamificada completa con misiones, barra de energía, tiempo en minijuegos, ranking de puntuación y recompensas.

### 6.2 Modo Turista (Coral `#F5A285`)
- Modo contemplativo y de recorrido libre. Sin temporizadores ni minijuegos complejos. Enfoque en audioguías, fotos históricas y paseo tranquilo.

### 6.3 Modo Familia (Multijugador Cooperativo Local)
Juego en equipo en un solo dispositivo o sincronizado, asignando roles:
- 👁️ **El Vigía:** Escanea el terreno y localiza los marcadores y pistas en el mapa.
- 📜 **El Cronista:** Lee la historia y responde las preguntas de los personajes.
- 📸 **El Fotógrafo:** Encargado de encuadrar los minijuegos visuales y fotos de evidencia.

---

## 7. Interfaz del juego (HUD & UI)

El HUD se organiza respetando la paleta visual del proyecto (retro-futurista industrial):

```
┌─────────────────────────────────────────────────────────────────┐
│ [Cu 1.250  Au 12  Sn 1]   [Rango: Capataz]   [GPS: Activo 🟢]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                      CANVAS MAPA 3D (R3F)                       │
│             [ Avatar 3D / Posición del Jugador ]               │
│                                                                 │
│     [ Marcador POI: Chiflón ]        [ Marcador POI: Parque ]   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ [🗺️ Mapa]  [🎒 Mochila]  [📜 Quests]  [🪪 Perfil]  [📢 Reporte] │
└─────────────────────────────────────────────────────────────────┘
```

**Iconografía de minerales** (referencia visual):
- **Cobre (Cu)** 🟠 — color cobre `#D17A4F`, ícono de pepita.
- **Oro (Au)** 🟡 — color dorado `#FFD700`, ícono de pepita con brillo.
- **Estaño (Sn)** ⚪ — color plateado `#C0C0C0`, ícono de cristal facetado.

---

## 8. Alcance del MVP (Piloto jugable)

> **Nota de encuadre (D-005, D-014, D-016):** este MVP 3D es la visión de fase 2. El entregable
> vigente de 30 días es la maqueta piloto lean definida en D-014 (slice jugable 2D sobre
> mapa: zonas + teleport + 1 misión + sistema multi-moneda), que es la base de código de la fase 1.

Para el entregable de la postulación al fondo se construirá un demostrador web interactivo que incluya:

1. **Mapa interactivo de Lota** con 3 POIs principales (Chiflón del Diablo, Pabellón 83, Parque de Lota).
2. **2 Personajes con diálogo** (Isidora Goyenechea y El Ciego de la Mina).
3. **2 Minijuegos jugables:** *Amasando Pan* (Ruta Fuego y Carbón) y *El Geólogo del Tiempo* (Ruta Geositio).
4. **Sistema multi-moneda** cobre/oro/estaño funcional con wallet y balance.
5. **1 World Event demo** sincronizado con una fecha real cercana, con NPCs exclusivas caminando por una zona, 1 misión temática que requiera 1 comercio real, y recompensa exclusiva no obtenible después del evento. (Ver §10.)
6. **1 comercio local real** asociado que acepta cobre vía cupón QR.
7. **Pasaporte del Guardián** con stats del jugador y medallas, URL pública compartible.
8. **Geofencing dual:** GPS real + modo virtual (teleport para pruebas sin estar físicamente en Lota).
9. **1 listing demo** de producto del comercio local para venta con pago en cobre (sin subasta completa todavía — ver §11).
10. **Instrumentación mínima** para ML externo (eventos anónimos de sesión, POI, mission_complete, world_event_join) — ver §12.

---

## 9. Datos duros y plazos

- **Presupuesto total:** 10 millones CLP.
- **Plazo de postulación:** Fines de agosto / primera semana de septiembre 2026.
- **Fondos objetivo:** Fondo principal (10M) + Fondo del Patrimonio (15-20M).
- **Entregable clave:** Demo jugable en PWA web + Propuesta escrita de Game Design + Carta Gantt.

---

## 10. World Events (sincronización con fechas reales)

> **Diseño conceptual (2026-08-10).** Capa encima de los eventos del cielo. Diseño completo en [`_analisis/21_world_events_d014.md`](../_analisis/21_world_events_d014.md).

**Tesis:** el juego se sincroniza con festividades reales (Fiestas Patrias, San Juan, Día del Patrimonio, temporada de ballenas, aniversario de Lota, etc.) para tematizar la experiencia durante 1-3 días y coordinar flujos turísticos hacia el comercio local.

**Mecánica de 5 componentes:**
1. **Trigger por fecha real** (Sentinel o calendario curado detecta la fecha, activa 24-48 h antes).
2. **Temática del juego**: NPCs exclusivas vestidas con la temática, diálogos contextualizados, decoraciones de mapa, audio ambiental.
3. **Misiones exclusivas con REQUIRE físico al comercio local**: el turista debe salir del teléfono y entrar al comercio real. Ejemplo: "Visita 3 panaderías asociadas, escanea QR en cada una" → insignia exclusiva + cupón real.
4. **Recompensas exclusivas con caducidad real**: insignia única (no obtenible después, estilo WoW), título de avatar, cupón QR en restaurant, café, completo, panadería, artesanía.
5. **NPCs exclusivas que caminan por el mapa**: no están fijas en un POI — deambulan por una zona predefinida, creando micro-carreras de caza de 1-5 min.
6. **Anuncio cross-channel**: Calendario del Cielo público + push 24-48 h antes + push 5-15 min antes + afiche QR en el comercio asociado.

**Por qué importa para D-014:** convierte el comercio local de "destino opcional" a "parte del evento mismo". Coordina oferta (comercio) con demanda (turista) en fechas sincronizadas.

**Catálogo de eventos reales (no fabricada):**
- **Nacionales / regionales con fecha fija**: Fiestas Patrias (18-19 sept), Día del Patrimonio (último dom mayo), San Juan (24 jun), Temporada de ballenas (julio-octubre).
- **Locales de Lota** (fechas requieren input de cliente/Municipio): aniversario de Lota, semana del carbón, festividades costumbristas del borde costero, fiesta patronal.
- **Comerciales** (curados): temporadas de productos (pan de mina, mariscos, sardina, empanadas), temporada alta/baja de turismo, aperturas de locales asociados.

---

## 11. Subastas digitales de cosas reales

> **Diseño conceptual (2026-08-10, D-017 aprobada el 2026-08-12).** Sistema de subastas integrado al juego, donde los usuarios listan productos o servicios del comercio local para subastar, otros pujan usando únicamente minerales del juego (cobre, oro, estaño), el juego cobra una comisión y la entrega se coordina localmente en Lota. Diseño completo en [`_analisis/24_subastas_reales.md`](../_analisis/24_subastas_reales.md).

**Tesis:** convierte a Lota Indómito en **marketplace soberano**. Los minerales dejan de ser "puntos de juego" y pasan a tener poder adquisitivo real. Esto refuerza D-014 por una nueva vía (la comisión por subasta).

**Mecánica:**
1. **Vendedor lista** un producto o servicio del comercio local (descripción + fotos + precio base en minerales + duración).
2. **Puja abierta**: los usuarios pujan con minerales. Anti-sniping: si hay puja en últimos 5 min, se extiende 5 min.
3. **Cierre**: gana el mejor postor. Si no hay pujas, el vendedor puede relistar.
4. **Pago + escrow**: los minerales del ganador se retienen en escrow del juego.
5. **Entrega + confirmación**: vendedor y comprador coordinan entrega (punto de recogida, encuentro personal o envío). Comprador confirma en la app.
6. **Comisión del juego**: 5-10% del precio final según categoría.
7. **Reputación**: rating bilateral (vendedor y comprador).

**Objetos subastables (MVP):**
- **Productos del comercio local**: gastronomía (vino, pan de mina, conservas), artesanía, souvenirs del juego, libros, edición limitada.
- **Servicios locales**: tour guiado, cena en restaurant, hospedaje, taller.
- **Lo que NO entra**: antigüedades (regulación CMN), NFTs (cripto), productos importados.

**Pago:** únicamente con minerales del juego. Sin CLP, sin Webpay, sin MercadoPago.

**Logística:** local-first (entrega en punto de recogida, encuentro personal). Envío solo para expansión regional futura.

---

## 12. ML externo para análisis de comportamiento

> **Diseño conceptual (2026-08-10).** Servicio de ML externo que consume directamente la base de datos del juego (PostgreSQL + PostGIS), entrena modelos sobre comportamiento de usuarios y entrega dashboards accionables para cliente, Municipios y comercio local. Diseño completo en [`_analisis/22_ml_analytics_d014.md`](../_analisis/22_ml_analytics_d014.md).

**Tesis:** el juego no es solo una experiencia para turistas. Es un **sensor** que produce datos accionables sobre tres dimensiones:

1. **Comercial**: qué minerales se canjean, dónde, cuándo, por qué. ROI por World Event para el comercio.
2. **Social**: cómo se relacionan los jugadores entre sí (transferencias P2P, trueques, red social). Patrones de reciprocidad, detección de fraude.
3. **Turística**: cómo se mueven los turistas por Lota (heatmaps, path analysis, tiempo en zona), estacionalidad, demografía, retención D+1/D+7/D+30.

**Por qué externo (no en runtime):** la regla dura del proyecto es **0 floats en CPU** (motor S60). ML clásico usa floats. El servicio de ML corre en Python externo (scikit-learn, XGBoost, Prophet, NetworkX, GeoPandas) sobre vistas materializadas de solo-lectura de la DB del juego.

**Por qué importa para el Municipio:** un municipio informado por datos reales del juego puede **justificar gasto y medir impacto** de su inversión turística. Esto es un argumento adicional para el fondo.

**Instrumentación mínima del piloto (16 eventos anónimos):**
- **Turista**: `user_session_start/end`, `poi_visit`, `world_event_join`, `mission_complete`, `world_event_complete`, `coupon_redeemed`, `passport_update`.
- **Social**: `transfer_sent/received`, `trade_offered/accepted`, `gift_sent`.
- **Comercio**: `commerce_registered`, `coupon_issued/used`, `commerce_mineral_received`.

**Privacidad desde el diseño:** user_id seudónimo (UUID aleatorio), opt-in explícito al onboarding, cumplimiento Ley 19.628, datos agregados para Municipio (nunca individuales), logs encriptados, retención 24 meses y luego agregación permanente.

**Lo que se puede hacer en el piloto de 30 días:** instrumentación (los 16 eventos) + 2-3 vistas materializadas + dashboard estático simple + 1 modelo simple (predicción de retención D+1 con regresión logística). Modelos complejos para fase 1.

---

## 13. Referencias cruzadas

- **Loop de visita + retorno:** [`_analisis/20_loop_jugador_dia_a_dia.md`](../_analisis/20_loop_jugador_dia_a_dia.md)
- **World Events:** [`_analisis/21_world_events_d014.md`](../_analisis/21_world_events_d014.md)
- **Sistema multi-moneda:** [`_analisis/23_sistema_monedas_minerales.md`](../_analisis/23_sistema_monedas_minerales.md)
- **Subastas digitales:** [`_analisis/24_subastas_reales.md`](../_analisis/24_subastas_reales.md)
- **ML externo:** [`_analisis/22_ml_analytics_d014.md`](../_analisis/22_ml_analytics_d014.md)
- **D-014 corregida (encuadre vigente):** [`docs/decisiones.md`](decisiones.md)
- **D-016 aprobada (monedas minerales):** [`docs/decisiones.md`](decisiones.md)
- **D-017 aprobada (subastas):** [`docs/decisiones.md`](decisiones.md)