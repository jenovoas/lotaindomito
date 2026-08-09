# Lota Indómito — Concepto del juego (Game Design Document)

**Tipo:** juego tipo Pokémon GO, basado en geolocalización.
**Stack:** three.js + React Three Fiber, Web PWA.
**Plataforma objetivo:** navegador web (mobile-first), instalable como PWA.

---

## 1. Concepto en una línea

El jugador es un **Explorador del Carbón** que camina por Lota (físicamente o virtualmente), entra a zonas históricas y desbloquea misiones, descubre personajes del pasado (Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor, El Palanquero), y sube de rango recogiendo **Carboncillos** (la moneda virtual del juego).

---

## 2. Lectura de las pantallas del Stitch

El prototipo Stitch (~53 pantallas) **no es un sitio web de turismo**. Es la maqueta de los menús, HUDs e indicadores de un juego. Categorías reinterpretadas:

| Stitch dice | En el juego es |
|---|---|
| "Selección de modo" | Menú de inicio: Jugador (verde) vs Turista (coral) |
| "Pasaporte" | Perfil del jugador, avatar, nivel |
| "Mapas interactivos" | Vista del mundo 3D con marcadores de zonas (POIs) |
| "Rutas / itinerarios" | Tracks temáticos que agrupan zonas (Ruta de las Bodegas, etc.) |
| "Misiones" | Quests asociadas a cada zona: "Amasando Pan", "Arquitecto de Pabellones" |
| "Monumentos y AR" | POIs con encuentro AR: cuando entras, aparece un personaje fantasma que te cuenta historia |
| "Reportes y dashboards" | Menú de reportes ciudadanos (feature social) y dashboard de progreso |
| "Bitácoras y bóveda" | Colección de logros, skins, items desbloqueados |
| "Recompensas y canje" | Inventario, Carboncillos, canjeables en "ferias" (locales asociados) |
| "Diplomas" | Certificados de finalización de ruta, compartibles como PDF |
| "Modo familia" | Multiplayer cooperativo local (roles Vigía, Cronista, Fotógrafo) |

---

## 3. Mecánicas centrales

### 3.1 Movimiento y descubrimiento
- **Geofencing (real):** el jugador camina con la app abierta; al entrar al radio de un POI (50-200 m), se desbloquea el encuentro.
- **Modo virtual (fallback):** si no quiere caminar o no hay GPS, puede hacer "teleport" a cualquier POI desbloqueado previamente y revivir el encuentro.
- **Vista:** cámara cenital o tercera persona con three.js, mapa renderizado con elevación real de OSM.

### 3.2 Encuentros AR
- Al entrar a un POI, se abre un "encuentro" con un personaje histórico (Isidora, Ciego, Chinchorrera, Palanquero).
- Personaje es un modelo 3D que aparece en escena, no requiere cámara del usuario (es 3D dentro del mundo del juego, no AR en sentido estricto).
- Conversación corta (3-5 líneas) +授予de Carboncillos + activación de misión de la zona.

### 3.3 Misiones
- Cada zona tiene 1 misión específica. Ejemplos:
 - **Bodegas:** "El Inventario del Carbón" — encontrar 5 piezas en la zona.
 - **Geositio:** "El Geólogo del Tiempo" — ordenar estratos geológicos.
 - **Comercio:** "El Trueque Lota" — canjear Carboncillos en 3 locales.
 - **Camina Lota:** "Arquitecto de Pabellones" —拍照selfies comparativas (modo fácil: solo marcos de la app).
 - **Costera:** "Vigía del Golfo" — encontrar 3 especies nativas en una mini-guícon mini-juego.
 - **Indómita:** "Rastreador de la Flora" — ID plantas con pistas de la app.
 - **Oficios de Mar:** "Chinchorreando en el Blanco" — pesca simbólica.
 - **Fuego y Carbón:** "Amasando Pan" — minijuego de tiempo/cantidad.

### 3.4 Sistema de progresión
- **Carboncillos:** moneda virtual, ganados por misiones, canjeables en locales reales (alianza con comercio).
- **Rangos:** Aprendiz → Capataz → Leyenda de la Cuenca (basado en # de Carboncillos o # de zonas completadas).
- **Medallas:** Ojo de Lince (reportes), Amasadora de Memorias (pan), Vigía de la Cuenca.
- **Bóveda:** inventario persistente con diplomas PDF compartibles.

### 3.5 Modos de juego
- **Individual:** un solo jugador.
- **Familia:** 2-4 jugadores en un mismo dispositivo, roles:
 - **Vigía:** scanner de zonas.
 - **Cronista:** narrador de la historia.
 - **Fotógrafo:** captura in-game.

### 3.6 Reportes ciudadanos (side quest)
- Botón para reportar basura, derrumbe, infraestructura.
- Validación cooperativa: otros jugadores pueden confirmar.
- Estado: pendiente → validado → resuelto.
- Esto es **side quest**, no mecánica central, pero alimenta el "Historial de Impacto" del perfil.

---

## 4. Mapa del mundo

- **Render:** three.js sobre mapa real de Lota con elevación (DEM).
- **Estilo visual:** bajo-poli industrial-futurista (paleta Stitch: turquesa #3FE6C0, coral #F5A285, cobre #D17A4F).
- **Cámara:** cenital con orbital; en encuentros cambia a tercera persona.
- **Brújula y minimapa** en HUD.
- **Marcadores:** zonas turísticas con icono + distancia restante + estado (no descubierta / descubierta / completada).

---

## 5. UI / HUD

Reinterpretación de las pantallas Stitch como componentes de juego:

- **HUD superior:** Carboncillos, rango, misiones activas.
- **HUD inferior:** botones de acción (mapa, mochila, misiones, reportes, perfil).
- **Perfil:** pasaporte con avatar + stats + diplomas + historial de impacto.
- **Menú principal (modo Jugador):** iniciar partida, continuar, multijugador familia.
- **Menú principal (modo Turista):** recorrido contemplativo, audioguías, sin mecánicas de juego.
- **Mapas:** vista 3D + vista minimapa + lista de zonas por ruta.
- **Pantalla de encuentro:** personaje AR + diálogo +授予de Carboncillos + animación.
- **Pantalla de misión completada:** diploma + stats + opción de compartir.
- **Billetera:** Carboncillos + cupones de canje.
- **Reportes:** cámara (en el juego, no real) + tipo + descripción + enviar.
- **Dashboard familia:** misiones compartidas entre roles.

---

## 6. Stack técnico confirmado

| Capa | Tecnología |
|---|---|
| Frontend | React + TypeScript + Vite |
| 3D | three.js + React Three Fiber (R3F) + drei |
| Mapa base | OpenStreetMap + tileserver-gl o MapTiler (vector tiles) |
| Geolocalización | Web Geolocation API + Turf.js para geofencing cliente |
| Estado | Zustand |
| UI | React + CSS modules (sin Tailwind por ahora) |
| Build | Vite → PWA con service worker |
| Backend (futuro) | FastAPI (Python) + PostgreSQL + PostGIS |
| Auth (futuro) | magic link o email simple |

---

## 7. Alcance del MVP (primer entregable)

Esto es lo que sí se construye. Lo demás se queda como diseño.

1. **Mapa 3D de Lota** con 5 POIs desbloqueables (no las 8 rutas completas).
2. **Modo Jugador** funcional (no modo Turista todavía).
3. **Encuentros AR** con 2 personajes (Isidora + El Ciego).
4. **2 misiones** completas (1 de Bodegas, 1 de Geositio).
5. **Sistema de Carboncillos** funcional.
6. **Perfil** básico (sin diplomas todavía).
7. **Geofencing** real (GPS) + modo virtual (teleport).
8. **Brújula y minimapa** en HUD.

**Fuera del MVP (fase 2):**
- Modo Turista.
- Modo Familia multiplayer.
- Reportes ciudadanos reales.
- Comercio integrado (canje en locales).
- 8 rutas completas.
- Sistema de diplomas PDF.

---

## 8. Datos duros (sin cambios)

- **Presupuesto total:** 10 millones CLP.
- **Plazo de postulación:** fines de agosto / primera semana de septiembre 2026.
- **Fondos posibles:** principal (10 M) + fondo del patrimonio (15-20 M).
- **Entregable para el fondo:** demo del juego (MVP) + propuesta escrita + Gantt.