# Design — UI/UX + Gráfica + Arquitectura de Juego

## Context

Lota Indómito tiene un Piloto A funcional (Vue 3 + MapLibre + Pinia, geofencing, wallet, micro-sesiones, world events) y un motor Rust S60 que ya emite eventos por WebSocket (`/ws/events` con `lattice_tick`, `portal_opened`, `npc_moved`, `npc_state_changed`). Lo que falta es:

- Una identidad visual coherente que comunique "juego de patrimonio" en lugar de "mapa web".
- Una separación explícita entre Simulación, Estado y Presentación para que el código refleje el modelo mental de un juego (Game Loop), no el de una API REST.
- Retratos y gráficos de encuentro que eleven el Piloto A a la altura de la propuesta conceptual.

Restricciones heredadas (no negociables, ver `MEMORY.md` §Reglas duras):

- 0 floats en CPU; f32 solo en shaders WGSL.
- `#[repr(C)]` en estructuras RAM↔SHM↔VRAM.
- No modificar el repo Sentinel (`/home/jnovoas/Proyectos/sentinel/me-60os-core/`).
- Wallet, subastas (D-017) y world events ya implementados — no se tocan.

## Goals / Non-Goals

**Goals:**

- Tokens visuales únicos compartidos entre landing y Piloto A.
- Retratos 2.5D SVG (sin PNGs externos) para los 4 NPCs canónicos + extensible.
- Composable `useGameLoop()` que desacople render loop de watchers reactivos.
- Buffer de interpolación LERP para suavizar GPS y movimiento de NPCs.
- Documento `_analisis/26_arquitectura_game_loop_3_capas.md` que internalice el modelo mental.

**Non-Goals:**

- No introducir un engine de juego (Phaser, PixiJS, Three.js en el cliente del Piloto A) — se mantiene MapLibre + SVG + Canvas2D overlay.
- No añadir modelos 3D a los NPCs (caros en ancho de banda móvil y rompen el principio de frugalidad).
- No cambiar el contrato WebSocket existente — sólo se documenta y se consume explícitamente.
- No tocar el motor Rust ni el backend FastAPI — sólo el Piloto A.

## Decisions

### D1. Tokens visuales en CSS (no en TS)

**Decisión:** Crear `piloto-a/src/assets/design-tokens.css` con variables CSS consumidas directamente por componentes Vue (no exponerlas vía JS).

**Por qué:** CSS variables se evalúan en tiempo de render sin overhead; cambiar un token recompila estilos sin ciclo de reactividad Vue.

**Alternativas consideradas:**

- *Theme con TS + Pinia:* más type-safe pero introduce reactive overhead y desacopla el token del CSS real.
- *Tailwind config:* ya hay `tailwind`-like inline pero no instalado formalmente; agregar Tailwind para este cambio es sobredimensionar.

### D2. Retratos NPC como SVG inline, no como PNGs

**Decisión:** `NpcAvatar.vue` recibe `npcId` y un slot con un SVG hardcodeado por NPC (4 SVGs iniciales: Isidora, Ciego, Chinchorrera, Palanquero).

**Por qué:**

- 0 dependencia de red.
- 0 costo de batería en móvil (vs canvas redibujando).
- Escalable a cualquier densidad de pantalla.
- Encaja con la regla "0 floats": todo es vectorial.

**Alternativas consideradas:**

- *PNGs comprimidos WebP:* mejor calidad artística pero +50 KB por NPC mínimo, latencia de carga en terreno con mala señal.
- *Lottie (animaciones JSON):* excesivo para retratos estáticos.

### D3. Render loop con `requestAnimationFrame` + composable

**Decisión:** Crear `piloto-a/src/composables/useGameLoop.ts` que:

1. Recibe un callback `update(deltaSec: number)`.
2. Usa `requestAnimationFrame` con control de tiempo (acumula dt).
3. Pausa automático cuando `document.hidden === true`.
4. Se desregistra en `onUnmounted`.

**Por qué:** Los `watch` de Vue son ideales para reactividad declarativa pero malos para animaciones de alta frecuencia — disparan en cada cambio de referencia, lo que con eventos WS (varios por segundo) genera stutters.

**Alternativas consideradas:**

- *Mantener `watch` y usar `nextTick`:* no resuelve el problema de frecuencia, sólo lo aplaca.
- *Web Workers para lógica de interpolación:* sobreingeniería para esta escala (decenas de marcadores, no miles).

### D4. Buffer de interpolación circular

**Decisión:** `piloto-a/src/utils/interpolationBuffer.ts` con una clase `RingBuffer<T>` de tamaño N=10, basada en `timestamp`. Cada `npc_moved` o muestra GPS empuja un sample; el render loop lee `latest()` y `previous()` para hacer LERP.

```ts
// Pseudo-API
const buffer = new RingBuffer<{ x: number; y: number; t: number }>(10)
buffer.push(currentSample)
const { current, previous } = buffer.pairAt(timeSec)
const t = clamp((timeSec - previous.t) / (current.t - previous.t), 0, 1)
const rendered = lerp(previous, current, t * 0.15) // factor 0.15
```

**Por qué:** Los GPS de teléfono actualizan cada 3-5 s y el motor Rust emite `npc_moved` con frecuencia similar. Sin interpolación, el marcador salta.

**Alternativas consideradas:**

- *Mostrar posición sin interpolar:* defecto actual → stutters visibles en terreno.
- *Kalman filter:* más preciso pero innecesario para marcadores en mapa (no se busca precisión sub-métrica).

### D5. Reconnect con backoff exponencial y jitter

**Decisión:** En `stores/lattice.ts`, añadir lógica de reconexión:

```ts
const backoffMs = Math.min(30_000, 1_000 * 2 ** retries) * (1 + (Math.random() - 0.5) * 0.4)
```

`retries` se resetea a 0 al recibir el primer mensaje tras reconectar.

**Por qué:** Evita el "thundering herd" cuando varios clientes pierden señal a la vez (túnel, evento masivo).

**Alternativas consideradas:**

- *Reconnect inmediato en bucle:* consume batería y puede DoS-ear al servidor en outages regionales.

### D6. Landing: degradación progresiva de three.js

**Decisión:** Detectar capabilities al cargar la landing:

```ts
if (!window.WebGLRenderingContext || navigator.deviceMemory < 2) {
  // Fallback CSS gradient animado
} else if (navigator.deviceMemory < 4 || window.innerWidth < 768) {
  // Perfil lite: devicePixelRatio cap 1.2, 250 partículas, sin chalupas
} else {
  // Full: tres.js completo
}
```

**Por qué:** El hero actual pesa ~14 KB de JS + escena three.js completa; en móviles gama media baja el FPS cae bajo 30.

**Alternativas consideradas:**

- *Mantener escena actual:* confirmado problema en testing informal (visible en `MEMORY.md`).
- *Reemplazar por video MP4:* banda ancha móvil prohibitive.

### D7. Bruma costera como CSS particles, no canvas

**Decisión:** `BrumaCostera.vue` usa `position: absolute` con múltiples `div`s animadas con `@keyframes` translate3d; nada de canvas ni WebGL extra.

**Por qué:** El mapa MapLibre ya consume GPU; añadir un canvas encima pelearía por el compositor. CSS animations se delegan al hilo del compositor sin JS.

**Alternativas consideradas:**

- *Canvas overlay:* más control de partículas pero riesgo de tearing sobre el mapa.

## Risks / Trade-offs

- **[Riesgo: regresión visual al migrar tokens]** → Mitigation: implementar `design-tokens.css` en paralelo al CSS actual y migrar componente por componente con screenshots before/after.
- **[Riesgo: render loop fuera de sync con watchers Vue]** → Mitigation: convertir el watcher de `mobsStore.mobsActivos` en *reactivo a nivel de store* (Pinia `$subscribe`) que empuja al buffer; el render loop sólo lee del buffer.
- **[Riesgo: aumento de peso del bundle por SVGs inline]** → Mitigation: cada SVG ≤ 4 KB (validar con `vite build --analyze`); total de los 4 NPCs ≤ 16 KB.
- **[Riesgo: caída de FPS en móvil gama baja con todas las features activas]** → Mitigation: el perfil "lite" del spec `visual-encounter-graphics` ya cubre este caso; documentar flag `?lite=1` para testing.
- **[Riesgo: el motor Rust no emite `npc_moved` aún]** → Mitigation: el buffer acepta también muestras manuales del store de mobs (interval-based), así el cliente puede mostrar movimiento simulado hasta que el motor emita en producción. Marcar esto como task con D-018 explícita.

## Migration Plan

1. **Fase 0 (sin cambios visibles):** crear `design-tokens.css`, `useGameLoop.ts`, `RingBuffer.ts`. Commits chicos, sin tocar componentes existentes.
2. **Fase 1 (UI/UX base):** migrar `App.vue` + `MapaLota.vue` a tokens nuevos. La landing sigue intacta.
3. **Fase 2 (gráficos):** introducir `NpcAvatar.vue`, `BrumaCostera.vue`, `EncuentroSheet.vue`. Reemplazar markers actuales.
4. **Fase 3 (arquitectura):** mover watchers a `$subscribe`, conectar `useGameLoop` al render de marcadores, introducir reconnect exponencial.
5. **Fase 4 (landing):** rediseñar `index.html`, añadir perfil lite y fallback CSS.
6. **Fase 5 (docs):** escribir `_analisis/26_*`, actualizar `MEMORY.md` y `docs/decisiones.md` con D-018.

**Rollback:** cada fase es un commit independiente. Si una fase rompe, se revierte ese único commit sin perder las anteriores.

## Open Questions

- ¿El motor Rust ya emite `npc_moved` con `(npc_id, lat_s60, lon_s60, timestamp)` o sólo emite `lattice_tick`? (verificar `rust/src/main.rs` y `lota-server` antes de la fase 3; si no, generar mocks en el store de mobs.)
- ¿Los retratos SVG deben tener también una versión "silueta" para vistas lejanas en el mapa? (defensible: sí, para mantener 60 FPS con muchos markers en pantalla.)
