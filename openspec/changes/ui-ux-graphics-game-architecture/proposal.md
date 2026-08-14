## Why

El Piloto A (PWA Vue + MapLibre) y la estética actual de Lota Indómito funcionan técnicamente pero se sienten como una **página web con mapa** en lugar de un **juego geolocalizado inmersivo**. Tres brechas bloquean el posicionamiento del concepto:

1. **UI/UX de landing y HUD del Piloto A** no transmiten la capa de juego: tipografía plana, marcadores tipo "pin de Google", paleta inconsistente, sin identidad de marca fuerte.
2. **Gráfica de los encuentros** (NPCs como `👤` con texto) y la escena 3D del hero no alcanzan calidad de propuesta de patrimonio: el piloto visual del concepto está por debajo de lo que promete.
3. **Arquitectura del sistema** mezcla el patrón web clásico "solicitud-respuesta" con la realidad de un juego: el motor Rust emite eventos (lattice tick, NPCs móviles), el cliente los recibe, pero no hay un bucle de juego claro que conecte simulación, presentación e input.

Hay además un sesgo de raíz: el INTERLOCUTOR viene de software/web tradicional y no está habituado a escribir juegos, así que la nueva arquitectura debe explicitar el cambio de paradigma (Game Loop, interpolación, FSM, render-vs-sim).

## What Changes

- Rediseñar la **landing pública** (`index.html`) para presentar el concepto con calidad de patrimonio: hero narrativo, tarjetas tipo "encuentro coleccionable", identidad visual coherente con la paleta del Piloto A.
- Establecer un **sistema de diseño HUD táctico-patrimonial** para el Piloto A: tokens de color/tipografía/borde reutilizables; migrar `App.vue`, `MapaLota.vue` y modales al nuevo look (bisel carbón, esquinas recortadas, tipografía Grotesk + Mono).
- Elevar la **gráfica del Piloto A**:
  - Marcadores de NPC como retratos 2.5D estilizados (estilo *Hades/Persona*) en lugar de emojis con texto.
  - Capa de niebla/bruma costera animada (partículas) sobre el mapa MapLibre.
  - Animación de "encuentro" en mapa: pulso luminoso en la zona + handoff a un modal tipo "ficha de colección".
- Introducir la **arquitectura de juego explícita en 3 capas**:
  - **Capa 1 — Simulación (Rust):** Game Loop determinista, FSM de NPCs, lattice tick → Pub/Sub WebSocket.
  - **Capa 2 — Estado y sync (Vue/Pinia):** buffer de interpolación de posiciones (suaviza GPS y movimiento de NPC), estado de inventario offline-first.
  - **Capa 3 — Presentación (Vue + render loop):** dibuja estado, no calcula.
- Documentar el patrón **Game Loop vs Request/Response** en `_analisis/` para que futuras sesiones tengan el modelo mental correcto.
- Sin cambios breaking: el contrato WebSocket (`/ws/events`) se mantiene; sólo cambia el render loop del cliente y el empaquetado del HUD.

## Capabilities

### New Capabilities

- `hud-tactico-patrimonial`: sistema de diseño y migración del HUD/bottom-sheet/markers del Piloto A a una identidad visual unificada de "mina + faro + radar".
- `visual-encounter-graphics`: especificación de los assets visuales de encuentro (retratos NPC estilizados, niebla costera, animaciones de pulso en mapa, ficha de encuentro coleccionable).
- `game-loop-architecture`: arquitectura explícita de 3 capas (simulación, estado, presentación) con Game Loop determinista, FSM de NPCs y bucle de render/interpolación en cliente.

### Modified Capabilities

- (ninguna — los specs principales viven dentro de este cambio)

## Impact

- **Frontend Piloto A (Vue 3 + MapLibre + Pinia):** refactor de estilos, nuevos componentes `NpcAvatar.vue`, `EncuentroSheet.vue`, `BrumaCostera.vue`, refactor de `MapaLota.vue` para separar render loop de watcher reactivo, posible nuevo `useGameLoop.ts` composable.
- **Landing (`index.html`):** rediseño de secciones (hero, encuentros, impacto, pilotos, prototipo, documentos); revisión de la escena three.js para optimizar performance en móvil.
- **Engine Rust:** sin cambios funcionales; sólo se documenta el contrato existente `lattice_tick`/`npc_moved`/`portal_opened` como parte del Game Loop.
- **Backend FastAPI:** sin cambios; sigue siendo el puente `Piloto A ↔ Piloto B`.
- **Documentación:** nueva nota en `_analisis/` explicando Game Loop + interpolación; entrada en `docs/decisiones.md` (D-018); entrada en `CHANGELOG.md`.

## Out of scope

- Creación de modelos 3D pesados para el teléfono (la solución es 2.5D estilizado).
- Reescritura del motor Rust o de los módulos Sentinel.
- Cambios en la wallet, subastas (D-017), world events: esos ya están funcionando y no se tocan.
