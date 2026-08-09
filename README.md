# Lota Indómito

Aplicación web progresiva (PWA) con mapa interactivo, gamificación cultural y módulo de reportes ciudadanos para la comuna de Lota (Chile).

> **Estado:** prototipo en diseño. Ver `docs/estado.md` para el estado vivo del proyecto.

---

## Componentes principales

- **Mapa interactivo** con marcadores de zonas turísticas.
- **Geofencing** que activa la experiencia al ingresar a una zona específica.
- **Sistema de check-in** con foto o QR en sitio.
- **Insignias y diplomas digitales** al completar rutas.
- **Reportes ciudadanos** (basura, derrumbe, infraestructura) → dashboard municipal.
- **Estadísticas de uso** para Municipio e instituciones patrimoniales.

## Stack técnico

- **Frontend PWA:** MapLibre GL JS, Turf.js (geofencing en cliente).
- **Backend:** Node.js o Python FastAPI + PostgreSQL + PostGIS.
- **Servicios de mapas:** OpenStreetMap self-hosted (Nominatim + OSRM) **o** Google Maps Platform.
- **Sincronización con Drive:** `rclone bisync` bidireccional con `drive:/LotaIndomito/`.

Ver `_analisis/04_propuesta_tecnica_stack_osm.md` para la propuesta técnica completa.

## Estructura del repositorio

```
.
├── _analisis/          # Análisis del prototipo Stitch, transcripciones, propuesta
│   └── transcripciones/
├── docs/               # Estado vivo del proyecto (NO es análisis)
│   ├── estado.md
│   ├── decisiones.md
│   └── procedimientos.md
├── stitch_lota_ind_mito_ciudad_museo_gamificada/  # Prototipo Stitch (no versionado, está en Drive)
└── whatsapp/           # Audios originales del cliente (no versionado, están en Drive)
```

> **Nota:** la carpeta `stitch_*` y `whatsapp/` están en `.gitignore` porque pesan y ya están sincronizadas con Google Drive vía `rclone bisync`.

## Documentación del proyecto

- `docs/estado.md` — qué es el proyecto, datos duros, contactos.
- `docs/decisiones.md` — decisiones tomadas y abiertas.
- `docs/procedimientos.md` — cómo operar el proyecto.
- `_analisis/00_resumen_sesion.md` — estado al cierre de la sesión anterior.
- `_analisis/01_resumen_audios_cliente.md` — síntesis del brief verbal del cliente.
- `_analisis/02_cotejo_audis_vs_prototipo.md` — qué pidió el cliente vs qué propuso el diseñador.
- `_analisis/04_propuesta_tecnica_stack_osm.md` — propuesta técnica para el fondo.

## Licencia

Apache License 2.0. Ver `LICENSE`.
