# Todo — Lota Indómito (2026-08-10)

Tareas detectadas en el escaneo del repo. Referencias cruzadas a docs y código que las justifican.

## Pendientes por pilar del concepto

### Piloto A (teléfono, PWA Vue 3 + MapLibre)

- Polígonos reales de zonas (doc 19 §2 — GeoRust + rstar).
- Geofencing real con Turf.js (doc 19 §3.4).
- FastAPI backend Piloto A (D-007 + D-013 dicen Vue + FastAPI pero FastAPI no existe).

## Lo que detecté en el escaneo y debe entrar a docs

### Doc 17 — `_analisis/17_arquitectura_gpu_motor_lota.md` — correcciones pendientes
- §4: dice `pollster` como dep, real es `tokio`.
- §4: dice `GpuOscillator` 64 bytes, real es 128 bytes (4×GpuSPA).
- §7 "Próximos pasos" lista `upload_and_dispatch` como pendiente, pero está implementado (commit `de42f61` + integración `b1f5e3f`).

### Doc — `docs/propuesta-fondo.md` — verificación pendiente
- §8 sigue diciendo "dos pilotos en competencia". D-014 los redefine como capas del mismo sistema, no competencia. Incoherencia si la clienta lo lee. Verificar si el commit `e7b868c` ("asentar D-014 y alinear todos los docs") lo actualizó o quedó pendiente.

### Piloto B (motor propio, Rust + wgpu + Sentinel)
- NPCs del enjambre SOMA — `soma_orchestrator.rs` y `soma_worker.rs` son para agentes IA, no para NPCs de RPG. Falta worker liviano (FSM simple, determinista). Doc 19 §6 confirma: FSM basta.
- Geofencing con rstar — dep ya está, falta implementar.
- Render visual del primer asset — hay compute shader, no render pipeline.
- Puente Piloto A ↔ Piloto B vía `lota-server` (WebSocket/HTTP).
