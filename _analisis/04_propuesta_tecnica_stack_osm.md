# Propuesta técnica — Lota Indómito
**Stack open-source self-hosted + alternativa Google Maps Platform**

**Fecha:** 2026-08-09
**Destino:** CLIENTA + Municipio / CMN (para postulación a fondos)

---

## 1. Resumen ejecutivo

Lota Indómito es una aplicación web progresiva (PWA) con mapa interactivo de la comuna, sistema de gamificación cultural y módulo de reportes ciudadanos alimentando un dashboard para el Municipio.

La propuesta presenta **dos alternativas técnicas** para el componente de mapas, ambas cumplen el brief del cliente:

| | **Opción A · Open-source** | **Opción B · Google Maps** |
|---|---|---|
| Costo recurrente | **$0** (solo VPS ~$15 USD/mes) | ~$100-275 USD/mes |
| Tiempo desarrollo | +1-2 semanas de setup inicial | Setup más rápido |
| Dependencia externa | Cero (autosuficiente) | Cuenta GCP activa |
| Calidad visual | Buena (estilo OpenStreetMap personalizable) | Excelente (Google) |
| Geofencing | PostGIS + Turf.js (open-source) | Nativo en Maps SDK |
| Portabilidad | El Municipio puede auto-hospedarlo | Lock-in con Google |

**Recomendación por defecto:** Opción A. La Opción B queda como contingencia si el Municipio decide licitar recursos para una cuenta corporativa de Google Cloud.

---

## 2. Arquitectura general

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO FINAL (PWA)                       │
│  MapLibre GL JS · Geolocation API · Turf.js (geofencing)   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────┴────────────────────────────────────┐
│              BACKEND (Node.js / Python FastAPI)              │
│   API REST · Auth · Lógica de misiones · Reportes            │
└──────┬──────────────────────────────────┬────────────────────┘
       │                                  │
┌──────┴──────────┐              ┌───────┴────────────┐
│ POSTGRESQL      │              │ SERVICIOS DE MAPAS │
│ + PostGIS       │              │                    │
│ (POIs, zonas,   │              │ Opción A:          │
│  reportes,      │              │   Nominatim (geo)  │
│  usuarios)      │              │   OSRM (rutas)     │
│                 │              │   tileserver-gl    │
│                 │              │                    │
│                 │              │ Opción B:          │
│                 │              │   Google Maps Plat.│
└─────────────────┘              └────────────────────┘
```

---

## 3. Stack tecnológico detallado

### 3.1 Frontend (lo que ve el usuario)
- **Tipo:** PWA (Progressive Web App) — funciona como app en celular sin publicar en stores.
- **Framework:** Vue 3 o Svelte (liviano, rápido). El equipo elige.
- **Mapa:** MapLibre GL JS (fork open-source de Mapbox GL).
- **Geofencing:** Turf.js (cálculo de polígonos en el cliente).
- **Geolocalización:** Web Geolocation API nativa del navegador.
- **UI:** Vuelve a tomar la paleta visual del Stitch (#3FE6C0, #F5A285, #D17A4F).

### 3.2 Backend
- **Lenguaje:** Node.js (Express/Fastify) o Python (FastAPI). INTERLOCUTOR decide.
- **Base de datos:** PostgreSQL 16 + PostGIS 3.4 (extensión espacial).
- **Auth:** simple email/password o magic link (sin OAuth al inicio).
- **API:** REST con JSON. Documentada con OpenAPI.

### 3.3 Servicios de mapas

**Opción A — Open-source self-hosted (recomendada):**

| Componente | Software | Función |
|---|---|---|
| Mapa base | OpenStreetMap data + tileserver-gl | Sirve los tiles del mapa |
| Geocoding | Nominatim | Convierte dirección → coordenadas y viceversa |
| Ruteo | OSRM | Calcula rutas óptimas (peatonal, auto) |
| Geofencing | PostGIS + Turf.js | Detecta entrada/salida de zonas |
| Tiles vectoriales | MapLibre style | Estilo de mapa personalizado con paleta del proyecto |

**Opción B — Google Maps Platform:**

| Componente | API de Google | Uso en el proyecto |
|---|---|---|
| Mapa interactivo | Maps JavaScript API | Render del mapa |
| Geocoding | Geocoding API | Convertir dirección ↔ coordenadas |
| Búsqueda de lugares | Places API | Listar POIs de Lota |
| Geofencing | Geofence API (nativa Android/iOS) o cálculo cliente con Google Maps SDK | Detectar entrada a zonas |
| Estimación costo mensual | Plan Starter $100 USD/mes | Ver `_analisis/03_costos_google_maps_platform.md` |

### 3.4 Infraestructura
- **VPS recomendado:** 4 vCPU, 8 GB RAM, 80 GB SSD.
- **Sistema operativo:** Ubuntu 24.04 LTS o Fedora 41.
- **Contenedores:** Docker + docker-compose.
- **HTTPS:** Let's Encrypt (gratis).
- **Costo estimado VPS:** $15-25 USD/mes en proveedores como Hetzner, DigitalOcean, Vultr.

---

## 4. Funcionalidades del MVP (alcance acotado)

Esto es lo que **sí** se construye en el piloto. Lo demás queda para fase 2.

### 4.1 Núcleo del producto
- **Mapa interactivo de Lota** con marcadores de zonas turísticas.
- **3-5 POIs iniciales** con ficha cultural (texto, fotos, audio guía si hay).
- **Sistema de check-in:** usuario confirma visita con foto o QR en sitio.
- **Insignias y diplomas digitales** al completar rutas.

### 4.2 Geofencing (el corazón técnico)
- **Definir 3-5 polígonos** de zonas turísticas en PostGIS.
- **Detección en cliente:** Turf.js verifica si la posición GPS del usuario cae dentro de algún polígono cada 30 segundos (con la app abierta).
- **Trigger:** al detectar entrada, el frontend consulta al backend → muestra "Estás en [zona], descubre su historia".
- **Privacidad:** la ubicación se procesa en el dispositivo; solo se registra telemetría agregada al backend.

### 4.3 Reportes ciudadanos
- **3 tipos:** basura, derrumbe/peligro, infraestructura dañada.
- **Foto + ubicación automática + descripción corta.**
- **Backend:** estado "pendiente" → "validado" → "resuelto".
- **Dashboard municipal:** vista web simple con lista de reportes y mapa de calor.

### 4.4 Estadísticas y dashboards
- **Dashboard Municipio:** visitas por zona, reportes recibidos, rutas más usadas.
- **Dashboard familia/usuario:** tus insignias, reportes enviados, kilómetros recorridos.

---

## 5. Funcionalidades NO incluidas en el MVP (quedan para fase 2)

| Feature | Por qué no va al MVP |
|---|---|
| Realidad Aumentada (personajes AR) | Costo de desarrollo y assets 3D altísimo |
| Sistema Carboncillos + canje comercial | Requiere alianzas con comercios ya formalizadas |
| Tótems QR físicos | Requiere obra e instalación de hardware |
| Modo Familia con roles multiplayer | Complejidad extra de UI y backend |
| Cooperativa de Trabajo | Requiere organización legal previa |
| 8 rutas completas | En MVP van 3-5 zonas, no las 8 |

---

## 6. Estimación de esfuerzo y costos

### 6.1 Costos operativos mensuales (piloto)

| Concepto | Opción A (OSM) | Opción B (Google) |
|---|---|---|
| VPS | $15-25 USD | $15-25 USD |
| Google Maps Platform | $0 | $100-275 USD |
| Dominio + SSL | $1 USD/mes | $1 USD/mes |
| **Total mensual** | **~$17-27 USD** | **~$117-302 USD** |

### 6.2 Costos de desarrollo (3-4 semanas)

Esta parte se discute en la sección de propuesta económica con CLIENTA. Para contexto, un proyecto de este tamaño típicamente requiere:

- 1 backend developer senior full-time × 3 semanas.
- 1 frontend developer × 3 semanas.
- 1 diseñador UI/UX × 1 semana.
- QA + deploy + post-lanzamiento × 1 semana.

---

## 7. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Tiempo de setup inicial de Nominatim/OSRM | Plan B: usar MapTiler free tier (100k tiles/mes) mientras se monta self-hosted |
| Calidad del mapa OSM en zonas rurales de Lota | Validar en OSM antes del piloto; completar lo que falte con datos del Municipio |
| Geofencing web poco confiable en interiores | Check-in manual por QR como fallback |
| Municipio sin capacidad técnica para mantener el stack | Documentación + handoff al cierre;可以考虑 capacitación al equipo municipal |
| Cambio de precios en Google Maps (pasó en 2025) | Revisar pricing oficial al cierre del piloto antes de renovar |

---

## 8. Próximos pasos para CLIENTA

1. **Confirmar elección de stack** (Opción A o B).
2. **Definir lista de 3-5 zonas turísticas prioritarias** para el MVP.
3. **Avales institucionales** confirmados del Municipio y/o CMN.
4. **Fecha dura de presentación** del fondo (a fines de agosto o septiembre).
5. **Identificar contraparte técnica municipal** que valide el despliegue.

---

## 9. Glosario técnico

- **PWA**: Progressive Web App. Webapp que se comporta como app nativa.
- **Geofencing**: Detectar entrada/salida de un área geográfica definida.
- **PostGIS**: Extensión espacial de PostgreSQL para consultas geográficas.
- **Nominatim**: Servicio open-source de geocoding de OSM.
- **OSRM**: Open Source Routing Machine, motor de ruteo open-source.
- **Tiles**: Cuadrantes de imagen del mapa que se cargan según zoom y posición.
