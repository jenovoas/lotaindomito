# Lota Indómito

Juego tipo Pokémon GO ambientado en Lota (Chile). El jugador camina por la ciudad, entra a zonas históricas, descubre personajes del pasado (Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor, El Palanquero), completa misiones y sube de rango recogiendo Carboncillos. Construido como PWA web con Vue 3 + TypeScript (decisión D-007).

> **Estado:** maqueta piloto en preparación (D-014: slice jugable en 30 días, base de fase 1). Game design document en `docs/concepto-juego.md`. Estado vivo del proyecto en `docs/estado.md`.

---

## Componentes principales

- **Mapa interactivo** con marcadores de zonas turísticas.
- **Geofencing** que activa la experiencia al ingresar a una zona específica.
- **Sistema de check-in** con foto o QR en sitio.
- **Insignias y diplomas digitales** al completar rutas.
- **Reportes ciudadanos** (basura, derrumbe, infraestructura) → dashboard municipal.
- **Estadísticas de uso** para Municipio e instituciones patrimoniales.

## Stack técnico

- **Frontend PWA:** Vue 3 + TypeScript + Vite, MapLibre GL JS, Turf.js (geofencing en cliente), Pinia (estado). Decisión D-007.
- **Backend (fase 1):** Python FastAPI + PostgreSQL + PostGIS (decisión D-006). La maqueta no lleva servidor: datos locales.
- **Servicios de mapas:** OpenStreetMap self-hosted (Nominatim + OSRM) para fase 1 (P-002); tiles OSM públicos durante la maqueta.
- **Motor GPU (Piloto B, centro del concepto):** crate `lota_engine` en `rust/` — wgpu + Sentinel S60 (decisiones D-011 a D-014).
- **Sincronización con Drive:** `rclone bisync` bidireccional con `drive:/LotaIndomito/`.

Ver `_analisis/04_propuesta_tecnica_stack_osm.md` para la propuesta técnica completa.

## Estructura del repositorio

```
.
├── _analisis/          # Análisis, transcripciones, propuestas (incluye material del fondo)
│   └── transcripciones/
├── docs/               # Diseño del proyecto y estado vivo
│   ├── concepto-juego.md    # GDD
│   ├── estado.md
│   ├── decisiones.md
│   ├── procedimientos.md
│   └── propuesta-fondo.md
├── piloto-a/           # Maqueta Piloto A (Vue 3 + MapLibre) — base de fase 1 (D-014). Por crear.
├── rust/               # lota_engine — motor GPU Piloto B (centro del concepto, D-014)
├── public/stitch/      # 52 pantallas del prototipo Stitch (versionado)
└── whatsapp/           # Audios originales del cliente (no versionado, está en Drive)
```

> **Nota:** `whatsapp/` está en `.gitignore` (audios pesados, sincronizados con Google Drive vía `rclone bisync`). El prototipo Stitch sí se versiona, bajo `public/stitch/`.

## Documentación del proyecto

- `docs/concepto-juego.md` — Game design document (GDD).
- `docs/estado.md` — qué es el proyecto, datos duros, contactos.
- `docs/decisiones.md` — decisiones tomadas y abiertas (D-014 es el encuadre vigente).
- `docs/procedimientos.md` — cómo operar el proyecto.
- `docs/propuesta-fondo.md` — propuesta consolidada para el fondo (material de Fabiola).
- `_analisis/00_resumen_sesion.md` — estado al cierre de la sesión anterior.
- `_analisis/01_resumen_audios_cliente.md` — síntesis del brief verbal del cliente.
- `_analisis/02_cotejo_audis_vs_prototipo.md` — qué pidió el cliente vs qué propuso el diseñador.
- `_analisis/04_propuesta_tecnica_stack_osm.md` — propuesta técnica para el fondo (restaurada 2026-08-10 desde copia de conflicto rclone).

## Licencia

Apache License 2.0. Ver `LICENSE`.
