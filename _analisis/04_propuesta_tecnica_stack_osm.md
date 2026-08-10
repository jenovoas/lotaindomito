# Propuesta técnica — Lota Indómito
**Pila de código abierto autoalojada + alternativa Google Maps Platform**

**Fecha:** 2026-08-09
**Destino:** cliente + Municipio / CMN (para postulación a fondos)

---

## 1. Resumen ejecutivo

Lota Indómito es una aplicación web progresiva (PWA) con mapa interactivo de la comuna, sistema de gamificación cultural y módulo de reportes ciudadanos alimentando un panel para el Municipio.

La propuesta presenta **dos alternativas técnicas** para el componente de mapas, ambas cumplen el brief del cliente:

| | **Opción A · Código abierto** | **Opción B · Google Maps** |
|---|---|---|
| Costo recurrente | **$0** (solo VPS ~$15 USD/mes) | ~$100-275 USD/mes |
| Tiempo de desarrollo | +1-2 semanas de instalación inicial | Instalación más rápida |
| Dependencia externa | Cero (autosuficiente) | Cuenta GCP activa |
| Calidad visual | Buena (estilo OpenStreetMap personalizable) | Excelente (Google) |
| Cercos virtuales | PostGIS + Turf.js (código abierto) | Nativo en SDK de Google |
| Portabilidad | El Municipio puede autoalojarlo | Atadura con Google |

**Recomendación por defecto:** Opción A. La Opción B queda como contingencia si el Municipio decide licitar recursos para una cuenta corporativa de Google Cloud.

---

## 2. Arquitectura general

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO FINAL (PWA)                       │
│  MapLibre GL JS · API de Geolocalización · Turf.js (cercos virtuales)   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS
┌────────────────────────┴────────────────────────────────────┐
│              SERVIDOR (Node.js / Python FastAPI)              │
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

## 3. Pila tecnológica detallada

### 3.1 Interfaz (lo que ve el usuario)
- **Tipo:** PWA (Progressive Web App) — funciona como app en celular sin publicar en stores.
- **Marco de trabajo:** React 18 + Vite + TypeScript (decisión D-007; análisis en `_analisis/05_analisis_tecnologias_disponibles.md`).
- **Mapa:** MapLibre GL JS (fork de código abierto de Mapbox GL).
- **Cercos virtuales:** Turf.js (cálculo de polígonos en el cliente).
- **Geolocalización:** API de Geolocalización nativa del navegador.
- **UI:** Vuelve a tomar la paleta visual del Stitch (#3FE6C0, #F5A285, #D17A4F).

### 3.2 Servidor
- **Lenguaje:** Node.js (Express/Fastify) o Python (FastAPI). INTERLOCUTOR decide.
- **Base de datos:** PostgreSQL 16 + PostGIS 3.4 (extensión espacial).
- **Autenticación:** simple con correo y contraseña o enlace mágico (sin OAuth al inicio).
- **API:** REST con JSON. Documentada con OpenAPI.

### 3.3 Servicios de mapas

**Opción A — Código abierto autoalojado (recomendada):**

| Componente | Software | Función |
|---|---|---|
| Mapa base | OpenStreetMap data + tileserver-gl | Sirve los tiles del mapa |
| Geocodificación | Nominatim | Convierte dirección → coordenadas y viceversa |
| Cálculo de rutas | OSRM | Calcula rutas óptimas (peatonal, auto) |
| Cercos virtuales | PostGIS + Turf.js | Detecta entrada/salida de zonas |
| Tiles vectoriales | MapLibre style | Estilo de mapa personalizado con paleta del proyecto |

**Opción B — Google Maps Platform:**

| Componente | API de Google | Uso en el proyecto |
|---|---|---|
| Mapa interactivo | Maps JavaScript API | Render del mapa |
| Geocodificación | API de Geocodificación | Convertir dirección ↔ coordenadas |
| Búsqueda de lugares | API de Lugares | Listar POIs de Lota |
| Cercos virtuales | API de Cercos (nativa Android/iOS) o cálculo en cliente con SDK de Google Maps | Detectar entrada a zonas |
| Costo mensual estimado | Plan inicial $100 USD/mes | Ver `_analisis/03_costos_google_maps_platform.md` |

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

### 4.2 Cercos virtuales (el corazón técnico)
- **Definir 3-5 polígonos** de zonas turísticas en PostGIS.
- **Detección en cliente:** Turf.js verifica si la posición GPS del usuario cae dentro de algún polígono cada 30 segundos (con la app abierta).
- **Disparador:** al detectar entrada, la interfaz consulta al servidor → muestra "Estás en [zona], descubre su historia".
- **Privacidad:** la ubicación se procesa en el dispositivo; solo se registra telemetría agregada al servidor.

### 4.3 Reportes ciudadanos
- **3 tipos:** basura, derrumbe o peligro, infraestructura dañada.
- **Foto + ubicación automática + descripción corta.**
- **Servidor:** estado "pendiente" → "validado" → "resuelto".
- **Panel municipal:** vista web simple con lista de reportes y mapa de calor.

### 4.4 Estadísticas y paneles
- **Panel del Municipio:** visitas por zona, reportes recibidos, rutas más usadas.
- **Panel de familia o usuario:** tus insignias, reportes enviados, kilómetros recorridos.

---

## 5. Funcionalidades NO incluidas en el MVP (quedan para fase 2)

| Feature | Por qué no va al MVP |
|---|---|
| Realidad Aumentada (personajes en RA) | Costo de desarrollo y recursos 3D altísimo |
| Sistema Carboncillos + canje comercial | Requiere alianzas con comercios ya formalizadas |
| Tótems QR físicos | Requiere obra e instalación de hardware |
| Modo Familia con roles multijugador | Complejidad extra de interfaz y servidor |
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

Esta parte se discute en la sección de propuesta económica con cliente. Para contexto, un proyecto de este tamaño típicamente requiere:

- 1 desarrollador de servidor senior de tiempo completo × 3 semanas.
- 1 desarrollador de interfaz × 3 semanas.
- 1 diseñador de interfaz y experiencia de usuario × 1 semana.
- Aseguramiento de calidad + despliegue + post-lanzamiento × 1 semana.

---

## 7. Riesgos y mitigaciones

| Riesgo | Mitigación |
|---|---|
| Tiempo de instalación inicial de Nominatim y OSRM | Plan alternativo: usar plan gratuito de MapTiler (100 mil cuadrantes al mes) mientras se monta el autoalojamiento |
| Calidad del mapa de OSM en zonas rurales de Lota | Validar en OSM antes del piloto; completar lo que falte con datos del Municipio |
| Cercos virtuales en navegador poco confiables en interiores | Registro manual por QR como alternativa |
| Municipio sin capacidad técnica para mantener la pila | Documentación + entrega al cierre + capacitación al equipo municipal |
| Cambio de precios en Google Maps (pasó en 2025) | Revisar pricing oficial al cierre del piloto antes de renovar |

---

## 8. Próximos pasos para cliente

1. **Confirmar elección de stack** (Opción A o B).
2. **Definir lista de 3-5 zonas turísticas prioritarias** para el MVP.
3. **Avales institucionales** confirmados del Municipio y/o CMN.
4. **Fecha dura de presentación** del fondo (a fines de agosto o septiembre).
5. **Identificar contraparte técnica municipal** que valide el despliegue.

---

## 9. Glosario técnico

- **PWA (Aplicación web progresiva)**: aplicación web que se comporta como aplicación nativa.
- **Cercos virtuales**: detección de entrada y salida de un área geográfica definida.
- **PostGIS**: extensión espacial de PostgreSQL para consultas geográficas.
- **Nominatim**: servicio de código abierto de geocodificación de OpenStreetMap.
- **OSRM**: motor de código abierto para cálculo de rutas.
- **Cuadrantes del mapa**: imágenes del mapa que se cargan según el nivel de zoom y la posición en pantalla.
