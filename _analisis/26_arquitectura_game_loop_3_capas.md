# 26 · Arquitectura de Juego: 3 capas + Game Loop

> Estado: vigente (D-021, 2026-08-14). Internaliza el modelo mental de un juego
> geolocalizado para futuras sesiones que toquen Piloto A o el motor Rust.

## Contexto

Lota Indómito no es una API REST con un mapa delante. Es un **juego geolocalizado**
donde el motor (Rust S60) emite eventos en tiempo real, el GPS llega cada 3-5 s,
y el cliente debe **dibujar a 60 FPS** aunque los datos lleguen más lento.

El patrón web clásico ("componente hace fetch, recibe JSON, renderiza") no encaja:
genera stutters cuando hay muchos eventos y obliga a mezclar la lógica de
presentación con la lógica de sincronización.

## Las 3 capas

```
┌──────────────────────────────────────────────────────────────────┐
│  CAPA 1 · SIMULACIÓN (Rust + S60 engine, Piloto B)               │
│  ─ dueña del estado de mundo                                     │
│  ─ Game Loop determinista (target 50 Hz)                         │
│  ─ FSM de NPCs: Idle → Wander → Approach → Deliver               │
│  ─ Emite eventos por WebSocket /ws/events:                       │
│      lattice_tick, portal_opened, npc_moved, npc_state_changed   │
└──────────────────────────────────────┬───────────────────────────┘
                                       │ WebSocket (Pub/Sub)
                                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  CAPA 2 · ESTADO Y SYNC (Vue/Pinia, Piloto A)                   │
│  ─ dueña del estado del jugador + caché de mundo                 │
│  ─ Recibe eventos, empuja a RingBuffer<{lat, lon}> por entidad   │
│  ─ Buffer de interpolación (N=10, timestamp)                     │
│  ─ Inventario / wallet / misiones (offline-first)                │
│  ─ Reconnect exponencial con jitter (± 20 %)                     │
└──────────────────────────────────────┬───────────────────────────┘
                                       │ Pinia stores (síncrono, en memoria)
                                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  CAPA 3 · PRESENTACIÓN (Vue + render loop con rAF)              │
│  ─ Sólo dibuja el estado en pantalla                             │
│  ─ useGameLoop() entrega `dt` y lee del buffer                   │
│  ─ NpcAvatar, BrumaCostera, EncuentroSheet, BannerIntercept      │
│  ─ Marcadores MapLibre: NO llamar al backend                     │
└──────────────────────────────────────────────────────────────────┘
```

**Reglas duras:**

1. La Capa 3 NO llama al backend. Si necesita datos, los lee de Pinia.
2. La Capa 2 NO ejecuta lógica de simulación. No decide cuándo un NPC se mueve.
3. La Capa 1 NO conoce Vue ni MapLibre. Emite eventos agnósticos de UI.

## Flujo de un tick (lattice_tick)

```
motor.step()            → lattice_tick { tick, wave_value_sample }
  ─ wire JSON ─────────►  latticeStore.onmessage()
                            ─ lastTick.value = data.tick
                            ─ push a RingBuffer (opcional)
                                                ─ useGameLoop.update(dt)
                                                    ─ HUD lee lastTick.value
                                                    ─ MapLibre: marker.setLngLat(...)
```

## Flujo de movimiento de NPC

```
npc_fs.machine()        → npc_moved { npc_id, lat_s60, lon_s60, t }
  ─ wire JSON ─────────►  mobsStore.onmessage()
                            ─ push sample a npcBuffers.get(npc_id)
                                                ─ useGameLoop.update(dt)
                                                    ─ sampleAt(buffer, now) → LERP
                                                    ─ marker.setLngAt([lon, lat])
```

## Buffer de interpolación (`interpolationBuffer.ts`)

API pública:

```ts
const buf = new RingBuffer<{ lat: number; lon: number }>(10)
buf.push({ lat: -37.09, lon: -73.16 }, performance.now() / 1000)

// dentro del render loop:
const now = performance.now() / 1000
const pos = sampleAt(buf, now, ['lat', 'lon'] as const, 0.15)
// factor 0.15 = suavizado fuerte; sube a 0.5 si quieres respuesta más inmediata
```

Por qué LERP y no Kalman: las posiciones no requieren precisión sub-métrica;
solo queremos evitar saltos cuando GPS o WS entregan datos cada 3-5 s.

## `useGameLoop` — composable

```ts
useGameLoop((dt) => {
  // leer stores
  // actualizar markers
  // refrescar HUD numérico
})
```

- Usa `requestAnimationFrame` con control de `dt`.
- Pausa automático cuando `document.hidden === true` (ahorra batería).
- Cleanup automático en `onBeforeUnmount`.

## Reconnect resiliente

`stores/lattice.ts`:

```ts
function backoffMs(retries: number): number {
  const base = Math.min(30_000, 1_000 * 2 ** retries)
  const jitter = 1 + (Math.random() - 0.5) * 0.4
  return Math.max(500, Math.floor(base * jitter))
}
```

Mientras la conexión está caída:

- `connectionStatus === 'reconnecting' | 'offline'`
- el render loop sigue dibujando con el último estado conocido
- el HUD muestra `LATTICE EN PAUSA` (color ámbar, no rojo: el juego sigue jugable)

## `useGraphicsProfile` — degradación progresiva

```ts
const { value: graphics } = useGraphicsProfile()
// graphics.profile ∈ 'full' | 'lite' | 'css-only'
```

| Perfil     | Cuándo                                  | Efectos                                          |
|------------|-----------------------------------------|--------------------------------------------------|
| full       | GPU dedicada, dpr ≤ 2, viewport desktop | Bruma costera a 0.7 densidad, halo animado      |
| lite       | mem < 4 GB o viewport < 768 px          | Bruma 0.3, halo opcional, pulso 1 anillo        |
| css-only   | sin WebGL o mem < 2 GB                  | Landing reemplaza three.js por gradiente CSS     |

## Anti-patrones (qué NO hacer)

1. ❌ `watch(() => store.npcs, () => marker.setLngLat(...))` dentro de un componente.
   → usar `useGameLoop` y consumir del buffer.
2. ❌ Fetch desde `onMounted` de un componente visual.
   → si necesitas datos, hazlo en el store (Capa 2) y exponlos reactivos.
3. ❌ `setInterval` para actualizar HUD numérico.
   → el render loop ya pasa por ahí; usa `useGameLoop`.
4. ❌ Hardcodear colores hex en componentes (`#3FE6C0`).
   → usa `var(--lota-teal)` desde `design-tokens.css`.

## Relación con el motor Rust

El motor Rust (`lota_engine`) ya emite `lattice_tick` y `portal_opened`. La
emisión de `npc_moved` y `npc_state_changed` depende del avance del enjambre
SOMA (Piloto B). Mientras tanto, el cliente puede simular movimiento con
`mobsStore.startPatrolTicker()` (interval manual) que empuja al mismo buffer.

Cuando el motor emita eventos reales, no hay que tocar la Capa 3: el
`socket.onmessage` del store de mobs sigue siendo el único punto de entrada.

## Cómo extender

- **Añadir un nuevo NPC:** crear SVG en `NpcAvatar.vue` y registro en `isKnown`.
- **Añadir un nuevo evento WS:** declarar interface en `stores/lattice.ts`,
  actualizar `socket.onmessage`, exponer reactivo. La Capa 3 no se entera.
- **Cambiar la paleta:** modificar `design-tokens.css`. Todos los componentes
  consumen tokens; no requiere tocar CSS scoped.
- **Forzar perfil lite en testing:** añadir `?lite=1` y leerlo en `useGraphicsProfile`.

## Métricas objetivo

- ≥ 50 FPS en dispositivos gama media (Chrome Android, 4 GB RAM).
- Battery drain < 8 % en 60 s de visualización pasiva del Piloto A.
- ≤ 16 KB bundle JS adicional para retratos SVG (4 NPCs × ~4 KB).
- LERP smoothing factor: 0.15 por defecto, ajustable en `sampleAt`.
