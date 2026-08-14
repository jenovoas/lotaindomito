# Lota Indómito

Juego tipo Pokémon GO ambientado en Lota (Chile). El jugador camina por la ciudad, entra a zonas históricas, descubre personajes del pasado histórico (Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor, El Palanquero), completa misiones y sube de rango recolectando minerales del juego.

> **Estado:** diseño de concepto completo (D-014). Piloto demostrable en preparación: teléfono (PWA, Piloto A) + motor (Rust + wgpu + Sentinel S60, Piloto B — el centro del concepto). Propuesta de concepto en `docs/propuesta-concepto.md` (28 secciones). Resumen ejecutivo en `docs/resumen-ejecutivo.md`.

---

## El proyecto en una línea

Evento real (cielo, hora, festividades de Lota) → el enjambre de personajes históricos despierta → el jugador los caza caminando por la comuna, guiado por su teléfono → cada encuentro reconstruye la memoria real de Lota y reactiva el comercio local.

## Componentes

- **Piloto A — teléfono (PWA):** Vue 3 + TypeScript + Vite + MapLibre GL JS + Turf.js (geofencing en cliente) + Pinia. Mapa de Lota con zonas patrimoniales.
- **Piloto B — motor (centro del concepto):** crate `lota_engine` en `rust/` — wgpu + Sentinel S60 (aritmética en base 60, sin floats). Pipeline GPU corriendo sobre GTX 1050 / Vulkan: lattice dual-lane → VRAM → compute shader → readback → portales.
- **Backend:** Python FastAPI + PostgreSQL + PostGIS (fase 1), con geofencing y NPCs ya implementados.

## Estructura del repositorio

```
.
├── _analisis/          # Análisis técnicos (arquitectura, motor GPU, investigaciones)
├── docs/               # Documentación del proyecto
│   ├── propuesta-concepto.md   # Propuesta de concepto completa (28 secciones)
│   ├── resumen-ejecutivo.md    # Resumen de 1 página
│   ├── concepto-juego.md       # GDD
│   ├── estado.md               # Estado vivo del proyecto
│   └── decisiones.md           # D-001 a D-017 (D-014 es el encuadre vigente)
├── piloto-a/           # Piloto A — PWA Vue 3 + MapLibre
├── rust/               # Piloto B — motor GPU (lota_engine + lota-server)
├── public/stitch/      # Prototipo visual (52 pantallas)
├── index.html          # Landing de presentación
└── prototipo-stitch.html  # Navegador del prototipo visual
```

## Documentación

- `docs/propuesta-concepto.md` — la propuesta completa: concepto, especificación técnica, fundamentación (por qué S60, multi-moneda, World Events), plan por etapas (Etapa 0 piloto → Etapa 4 operación), marco normativo, riesgos ISO 31000 y decisiones de diseño.
- `docs/resumen-ejecutivo.md` — una página con lo esencial, en lenguaje humano.
- `docs/concepto-juego.md` — game design document (GDD).
- `docs/decisiones.md` — decisiones de diseño registradas (D-014 = encuadre vigente).
- `CHANGELOG.md` — hitos con evidencia real (commits, tests).

## Licencia

Apache License 2.0. Ver `LICENSE`.
