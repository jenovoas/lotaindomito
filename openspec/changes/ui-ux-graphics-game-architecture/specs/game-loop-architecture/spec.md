## Purpose

Definir la arquitectura de tres capas (Simulación → Estado → Presentación) para que el Piloto A y el motor Rust operen como un sistema de juego, no como una API REST con mapa. Esta arquitectura es explícita y autodocumentada para que cualquier sesión futura entienda el modelo mental correcto.

## ADDED Requirements

### Requirement: Separación de capas

El sistema SHALL organizarse en tres capas con responsabilidades y dependencias unidireccionales:

1. **Simulación (Rust + S60 engine, Piloto B):** dueña del estado de mundo. Game Loop determinista que avanza `ticks` a frecuencia fija (target 50 Hz), ejecuta la FSM de cada NPC y emite eventos por WebSocket.
2. **Estado y sync (Vue/Pinia, Piloto A):** dueña del estado del jugador y de la caché de mundo. Recibe eventos, aplica buffer de interpolación y mantiene el inventario/wallet offline-first.
3. **Presentación (Vue + render loop):** dibuja el estado en pantalla. Consume stores de Pinia; no calcula.

Queda prohibido que la capa de Presentación llame directamente al backend sin pasar por la capa de Estado. Queda prohibido que la capa de Estado ejecute lógica de simulación.

#### Scenario: Flujo de un tick de lattice

- **WHEN** el motor Rust emite `lattice_tick` por `/ws/events`
- **THEN** la capa de Estado (Pinia store `lattice`) actualiza `lastTick`; el render loop en la capa de Presentación lee el valor y lo pinta en el HUD sin lógica adicional

#### Scenario: Movimiento de NPC en el cliente

- **WHEN** el motor Rust emite `npc_moved` con `(npc_id, lat_s60, lon_s60, timestamp)`
- **THEN** la capa de Estado lo encola en un buffer de interpolación con `timestamp`; el render loop interpola la posición del marcador hacia la nueva coordenada usando un LERP suave (factor configurable, default 0.15)

### Requirement: Game Loop determinista en cliente

El Piloto A SHALL ejecutar un bucle de presentación desacoplado de los eventos de red, basado en `requestAnimationFrame`, que: (1) lee posiciones interpoladas del store, (2) aplica transformaciones de marcador, (3) actualiza el HUD numérico. El bucle SHALL correr siempre que la pestaña esté visible y SHALL pausar cuando `document.hidden === true`.

#### Scenario: Bucle activo

- **WHEN** el jugador abre el Piloto A en el teléfono
- **THEN** el `useGameLoop()` composable arranca y mantiene ≥ 50 FPS en dispositivos gama media

#### Scenario: Pausa por visibilidad

- **WHEN** el jugador cambia de pestaña o bloquea el teléfono
- **THEN** el bucle se pausa (no consume batería) y reanuda exactamente donde quedó al volver

### Requirement: Buffer de interpolación para GPS y NPC

La capa de Estado SHALL mantener un buffer circular de las últimas N posiciones (default N=10, timestamp-based) por entidad móvil (NPC y jugador). El render loop SHALL consumir ese buffer con interpolación LERP entre la última muestra y la anterior, evitando saltos visibles cuando el GPS reporta cada 3-5 segundos.

#### Scenario: GPS intermitente

- **WHEN** el GPS no actualiza durante 4 segundos y luego entrega una nueva coordenada con offset de 30 m
- **THEN** el marcador del jugador se desliza visualmente durante ~800 ms en lugar de saltar

#### Scenario: NPC en movimiento

- **WHEN** el motor Rust emite tres `npc_moved` consecutivos para Isidora en 1.5 s
- **THEN** el marcador de Isidora se mueve suavemente entre las tres posiciones sin saltos perceptibles

### Requirement: FSM de NPCs como contrato de simulación

La capa de Simulación SHALL mantener una FSM por NPC con los estados `Idle`, `Wander`, `Approach`, `Deliver`. Las transiciones SHALL ser públicas vía WebSocket (evento `npc_state_changed`) para que la UI pueda reflejar el estado (ej: NPC en `Deliver` muestra icono de intercambio). La FSM SHALL ser determinista: dado el mismo seed y los mismos inputs, produce la misma secuencia de estados.

#### Scenario: NPC en estado Wander

- **WHEN** el motor Rust reporta `npc_state_changed` con `new_state=Wander`
- **THEN** el marcador del NPC muestra un icono de "caminar" sobre el avatar y entra en animación de oscilación

#### Scenario: NPC en estado Approach

- **WHEN** el motor Rust reporta `new_state=Approach` y la distancia al jugador es < 100 m
- **THEN** aparece el banner "EN EL RANGO" anclado al marcador

### Requirement: Reconnect resiliente del WebSocket

La capa de Estado SHALL implementar una reconexión exponencial con jitter al WebSocket (`/ws/events`): backoff inicial 1 s, máximo 30 s, jitter ± 20 %. Mientras la conexión esté caída, el cliente SHALL seguir dibujando con el último estado conocido y SHALL mostrar un indicador discreto "lattice en pausa" en el HUD.

#### Scenario: Caída de red en terreno

- **WHEN** el jugador pierde señal durante 12 segundos en una zona con NPCs
- **THEN** los marcadores permanecen visibles (último estado), el HUD muestra "lattice en pausa" y al recuperar señal el cliente reconecta sin intervención manual

### Requirement: Documento de arquitectura para futuras sesiones

El proyecto SHALL incluir `_analisis/26_arquitectura_game_loop_3_capas.md` describiendo: el diagrama de las tres capas, el flujo de un tick, el contrato WebSocket actual (`lattice_tick`, `portal_opened`, `npc_moved`, `npc_state_changed`), las diferencias con el patrón CRUD web y un anti-patrón "qué NO hacer" (ej: presentación llamando directo al backend).

#### Scenario: Sesión futura lee el documento

- **WHEN** un agente nuevo abre el proyecto y lee `_analisis/26_*`
- **THEN** entiende el modelo mental del Game Loop sin necesidad de pedir aclaraciones

## ADDED Requirements

### Requirement: Migración de watchers Vue a render loop explícito

El componente `MapaLota.vue` SHALL refactorizarse para que los `watch(() => mobsStore.mobsActivos, ...)` ya no manipulen directamente `Marker.setLngLat`; SHALL delegar al render loop del composable `useGameLoop()` que lee del buffer de interpolación.

#### Scenario: Sin saltos al actualizar NPC

- **WHEN** el store de mobs recibe un nuevo `npc_moved`
- **THEN** el marcador del NPC se actualiza vía render loop con interpolación, no por asignación síncrona dentro del watcher
