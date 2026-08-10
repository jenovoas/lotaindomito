# Lota Indómito — Concepto del juego (Game Design Document)

**Título:** *Lota Indómito: Guardianes de la Cuenca*  
**Género:** Geo-RPG / Juego de exploración urbana, patrimonio y aventuras  
**Plataforma:** Web PWA Mobile-First (Vue 3 + TypeScript + MapLibre GL — decisión D-007)  
**Estilo Visual:** Retro-industrial + futurista-gamer (Turquesa `#3FE6C0`, Coral `#F5A285`, Cobre `#D17A4F`, fondo nocturno `#0F1216`)

---

## 1. Visión general del juego

*Lota Indómito* es un juego de exploración y aventuras en mundo real basado en geolocalización (estilo *Pokémon GO*). El jugador asume el rol de **Explorador del Carbón** o **Guardián de la Memoria**. 

Al recorrer las calles y zonas históricas de Lota (Chile), el jugador descubre zonas patrimoniales, interactúa con espíritus y personajes emblemáticos del pasado, resuelve minijuegos contextuales, junta **Carboncillos** (la moneda virtual) y sube de rango en el pasaporte digital.

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
│   con descuento a 200 m." Gasta Carboncillos, ata el juego      │
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
| **Recompensa** | 180-240 s | +Carboncillos, +XP, animación de insignia, *"Has rescatado un fragmento del carbón."* | Siempre gana algo. Nunca "casi". Si pierde → retry sin penalización. |
| **Próximo** | 240-300 s | *"La próxima zona está a 320 m al sur."* Mini-mapa con ruta | Nunca terminar sin dirección. La pantalla siempre cierra con un "hacé X". |

**Variantes del tramo Acción según modo:**

- **Jugador** = 90 s de acción dura (QTE, puzle, estratigrafía).
- **Turista** = 0 s (escaneo + foto, sin minijuego).
- **Familia** = rol-asignado, todos participan en su rol (Vigía / Cronista / Fotógrafo).

### 2.4 Catálogo de eventos del cielo (resumen)

- **Astronómicos** (anuales): salida/puesta de sol, luna llena/nueva, equinoccios, solsticios.
- **Climáticos** (ventana corta, parcialmente impredecibles): niebla en el Parque, marejada en el Borde Costero, lluvia en el Chiflón.
- **Temporales** (recurrentes): Amanecer del Minero 07:00, Hora del Trueque 14:00, Atardecer del Carbón 19:00, Noche de las Chinchorreras 22:00.
- **Raros (S60)** — el diferenciador central: portales cuando `|amp_A - amp_B| < SCALE_0 / 50` en GPU. Carboncillo único (no se repite). Diploma *"Cazador de Portales"*.

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
| **Ruta del Comercio** | *El Trueque Lota* | Minijuego de gestión y canje de Carboncillos en puestos del comercio local. |
| **Ruta Costera** | *Vigía del Golfo* | Desafío de avistamiento con prismáticos virtuales para identificar la fauna del borde costero. |
| **Ruta Indómita** | *Rastreador de la Flora* | Trivia botánica interactiva con pistas de la vegetación nativa del Parque de Lota. |

---

## 4. Sistema de economía in-game (Carboncillos)

La moneda oficial del juego es el **Carboncillo** (`₡`).

### 4.1 Formas de ganar Carboncillos
- **Descubrir nuevo POI / Zona:** +50 ₡
- **Completar diálogo con personaje histórico:** +100 ₡
- **Minijuego superado con puntaje perfecto:** +150 ₡
- **Reporte ciudadano validado por la comunidad:** +75 ₡
- **Racha diaria de exploración:** +30 ₡

### 4.2 Usos y canje de Carboncillos
- **Canje real en locales asociados:** Cupones de descuento en panaderías, cafeterías y locales de artesanía local de Lota.
- **Personalización in-game:** Desbloqueo de marcadores de mapa personalizados, marcos para el Pasaporte y títulos de avatar.
- **Bóveda de Diplomas:** Emisión de diplomas digitales de honor descargables en PDF.

---

## 5. Sistema de progresión y rangos

El jugador acumula experiencia y Carboncillos para avanzar en los rangos del pasaporte:

| Rango | Carboncillos acumulados | Desbloqueables |
|---|---|---|
| **Aprendiz del Carbón** | 0 – 500 ₡ | Brújula básica, 3 zonas iniciales |
| **Capataz de la Cuenca** | 501 – 2.000 ₡ | Modo Multijugador Familiar, 5 zonas adicionales, skins |
| **Leyenda Indómita** | 2.001+ ₡ | Pasaporte de Oro, Diplomas PDF de Honor, Medalla de la Comuna |

### Medallas especiales
- 🏅 **Ojo de Lince:** 5 reportes ciudadanos validados en el dashboard municipal.
- 🍞 **Amasadora de Memorias:** Puntaje máximo en el minijuego de pan de mina.
- 🌊 **Vigía del Golfo:** Completar toda la Ruta Costera y Oficios de Mar.

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
│ [₡ 1.250 Carboncillos]   [Rango: Capataz]   [GPS: Activo 🟢]    │
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

---

## 8. Alcance del MVP (Piloto jugable)

> **Nota de encuadre (D-005, D-014):** este MVP 3D es la visión de fase 2. El entregable
> vigente de 30 días es la maqueta piloto lean definida en D-014 (slice jugable 2D sobre
> mapa: zonas + teleport + 1 misión + Carboncillos), que es la base de código de la fase 1.

Para el entregable de la postulación al fondo se construirá un demostrador web interactivo que incluya:

1. **Mapa 3D interactivo de Lota** con 3 POIs principales (Chiflón del Diablo, Pabellón 83, Parque de Lota).
2. **2 Personajes 3D** con diálogo (Isidora Goyenechea y El Ciego de la Mina).
3. **2 Minijuegos jugables:** *Amasando Pan* (Ruta Fuego y Carbón) y *El Geólogo del Tiempo* (Ruta Geositio).
4. **Sistema de Carboncillos** funcional con contador y balance.
5. **Pasaporte del Guardián** con stats del jugador y medallas.
6. **Geofencing dual:** GPS real + modo virtual (teleport para pruebas sin estar físicamente en Lota).

---

## 9. Datos duros y plazos

- **Presupuesto total:** 10 millones CLP.
- **Plazo de postulación:** Fines de agosto / primera semana de septiembre 2026.
- **Fondos objetivo:** Fondo principal (10M) + Fondo del Patrimonio (15-20M).
- **Entregable clave:** Demo jugable en PWA web + Propuesta escrita de Game Design + Carta Gantt.