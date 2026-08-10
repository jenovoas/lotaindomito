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

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXPLORACIÓN DEL MAPA 3D                      │
│   El jugador navega el mapa 3D de Lota (GPS real o modo virtual) │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                     (Llegada a Zona / Geofence)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ENCUENTRO 3D CON PERSONAJE                    │
│   Aparece un personaje histórico (Isidora, El Ciego, etc.)      │
│   con diálogo contextual e historia vivencial.                   │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                        (Aceptar la Quest)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MINIJUEGO Y DESAFÍO EN SITIO                 │
│   Minijuego táctil (amasar pan, clasificar estratos, etc.)      │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                     (Misión Completada con Éxito)
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PROGRESIÓN Y RECOMPENSAS                      │
│   + Carboncillos (₡) · + Puntos de Experiencia (XP)              │
│   Insignias unlocked · Certificado en el Pasaporte              │
└─────────────────────────────────────────────────────────────────┘
```

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