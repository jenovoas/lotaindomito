# Todo — Lota Indómito (2026-08-12)

Tareas detectadas en el escaneo del repo. Referencias cruzadas a docs y código que las justifican.

## Pendientes por pilar del concepto

### Piloto A (teléfono, PWA Vue 3 + MapLibre)

- Geofencing real con Turf.js (implementado en MapaLota.vue con lota_pois.geojson).
- Wallet multi-moneda con UI (`WalletHUD.vue` existe, aún no sincroniza con backend).
- Micro-sesiones de las 3 zonas: Chiflón del Diablo (✅ MicroSesionChiflon.vue), Parque Isidora (✅ MicroSesionIsidora.vue staged), Pabellón 83 (✅ MicroSesionPabellon.vue staged).
- Instrumentación de 16 eventos anónimos para ML externo.
- 1 World Event demo con fecha real + NPC exclusiva + insignia.
- 1 comercio real con cupón QR multi-moneda.
- 1 listing demo de venta en cobre.
- URL pública del pasaporte.

### Piloto B (motor propio, Rust + wgpu + Sentinel)

- [x] **Puente Piloto A ↔ Piloto B** — RESUELTO (2026-08-12): `/ws/events` (lattice_tick, portal_opened) + `/npcs`, `/npcs/interact`, `/dispatch`, `/portales` con wire format S60 5 componentes. Commit `672d040`.
- NPCs del enjambre SOMA móviles — FSM existe en `rust/src/npc/fsm.rs` (282 líneas, estados Idle/Wander/Approach/Deliver). Falta integrarla con el server y hacer que se muevan realmente en el mapa.
- Geofencing con R-Tree (`rstar`) — dep ya está, falta lógica.
- Render visual del primer asset — compute shader existe, falta render pipeline.

## Decisiones de diseño

### D-016 · Sistema multi-moneda — **APROBADA (2026-08-12)**
- Cobre (Cu, base) / Oro (Au, 100 Cu) / Estaño (Sn, 10.000 Cu). Ratios fijos.
- Reemplaza a Carboncillo. Wallet pendiente de materializar en backend.
- Doc: `_analisis/23_sistema_monedas_minerales.md`.

### D-017 · Subastas digitales de cosas reales — **APROBADA (2026-08-12)**
- Pago solo en minerales (sin CLP). Comisión 5-10%. Escrow + reputación bilateral.
- Servicio de subastas pendiente en backend.
- Doc: `_analisis/24_subastas_reales.md`.

## Doc 17 — `_analisis/17_arquitectura_gpu_motor_lota.md`
- [x] `pollster` → `tokio` ✅ (commit `caebcf7`).
- [x] `GpuOscillator` 64 → 128 bytes ✅ (commit `caebcf7`).
- [x] `upload_and_dispatch` ya estaba implementado ✅.

## Doc — `docs/propuesta-fondo.md`
- [x] §8 "dos pilotos en competencia" → arquitectura de dos capas (D-014) ✅ (commit `caebcf7`).

## 21 decisiones de diseño abiertas
- Lista en `_analisis/25_todo_continuacion.md` §4 (Docs 20-24).
- Requieren OK de INTERLOCUTOR para bajar a implementación.

## Input requerido de terceros

### cliente / Municipio
- Fechas de festividades de Lota (aniversario, semana del carbón, fiesta patronal).
- Selección de 1 comercio real para cupones QR del piloto.
- Validación del modelo de autofinanciamiento (D-014).

### INTERLOCUTOR
- Resolver las 21 decisiones de diseño abiertas.
- Definir operador del servicio de ML.
- Decidir DB local (servidor fan) o nube.
