# Análisis Comparativo de Tecnologías Disponibles — Lota Indómito

**Fecha:** 2026-08-09  
**Nota (2026-08-10):** documento histórico de análisis. La recomendación de Three.js/R3F fue superada por la decisión D-007 (Vue 3 + TypeScript) y el encuadre D-014 (maqueta Piloto A). Se conserva como registro del análisis comparativo.
**Objetivo:** Evaluar las tecnologías disponibles para la construcción del PWA Web 3D, geofencing, backend e infraestructura de *Lota Indómito*, considerando costos, rendimiento en móviles y tiempo de desarrollo.

---

## 1. Motor Gráfico 3D y Renderizado de Mapa

| Criterio | **Option A: Three.js / React Three Fiber (R3F) + MapLibre GL** (Recomendada) | **Option B: Google Maps Platform (WebGL 3D Overlay)** | **Option C: CesiumJS / Babylon.js** |
|---|---|---|---|
| **Costo de licencia** | 100% Gratuito y Open-Source (MIT/BSD) | De pago por consumo (desde $100 USD/mes) | 100% Gratuito / Open-Source |
| **Modelos 3D Custom (Personajes)** | Excelente (soporte nativo GLTF/GLB, animaciones, shaders) | Limitado (capas overlay complejas de integrar) | Alto (enfocado en modelos GIS y terreno) |
| **Rendimiento en Celulares** | Alto (bundle liviano < 1.5MB gzip) | Medio (depende de scripts externos de Google) | Bajo (bundle pesado > 5MB, alto uso de RAM) |
| **Estilo Visual del Juego** | Control total de luces, colores, texturas e iluminación nocturna | Limitado a estilos de vector de Google | Control total pero complejo |
| **Riesgo de Lock-in** | Nulo | Alto (dependencia directa de GCP) | Nulo |

> **Veredicto:** **Opción A (Three.js / R3F + MapLibre GL)** es la mejor opción. Permite estética gamer personalizada (turquesa, coral, cobre sobre fondo oscuro) sin pagar licencias mensuales.

---

## 2. Motor de Geolocalización y Geofencing

| Capa | Tecnología | Función | Evaluación |
|---|---|---|---|
| **Cliente (Navegador)** | `Turf.js` + Web Geolocation API | Verificación de polígonos GPS en tiempo real cada 15-30s | **Excelente:** Procesa todo en la GPU/CPU del teléfono sin latencia ni llamadas a red. Funciona en background suavemente. |
| **Backend (Base de Datos)** | `PostgreSQL 16` + `PostGIS 3.4` | Almacenamiento de zonas turísticas, polígonos de POIs y validación espacial de reportes | **Estándar de la industria:** Permite funciones como `ST_DWithin` y `ST_Contains` para verificar check-ins anti-spoofing. |

> **Veredicto:** Combinar **Turf.js en cliente + PostGIS en servidor** entrega la mejor respuesta y seguridad.

---

## 3. Framework Frontend y Arquitectura PWA

| Tecnología | Pros | Contras | Recomendación |
|---|---|---|---|
| **React 18 / 19 + Vite** | Ecosistema masivo, integración nativa con `@react-three/fiber` (R3F) y `drei`, estado reactivo fácil con `Zustand`. | Bundle ligeramente mayor que Svelte. | **Recomendado:** La facilidad de R3F para montar personajes 3D acelera el desarrollo. |
| **Vue 3 + Vite** | Muy liviano, sintaxis simple, excelente rendimiento. | Integración 3D requiere envoltorios manuales con Three.js puro (TresJS existe pero tiene menos ecosistema). | Buena alternativa si se prefiere Vue. |
| **Svelte 4 / SvelteKit** | Mínimo peso de JS en cliente. | Menor ecosistema de librerías 3D declarativas. | No prioritario para este proyecto. |

---

## 4. Backend y APIs

| Opción | Pros | Contras | Veredicto |
|---|---|---|---|
| **Python FastAPI** | Desarrollo ultra rápido, validación automática Pydantic, OpenAPI / Swagger automático. | Mayor consumo de memoria RAM que Rust. | **Recomendado para prototipo rápido / MVP.** |
| **Node.js (Fastify / Express)** | Mismo lenguaje (TypeScript) en front y back. Alto rendimiento asíncrono. | Menos utilidades geográficas nativas. | Alternativa sólida. |
| **Rust (Ejemplo: `celestial.rs`)** | Rendimiento máximo, consumo de RAM ínfimo (~10MB), ideal para **sincronizar eventos digitales in-game con eventos del mundo real** (mareas, iluminación ambiental/astronómica, clima o actividades comunitarias en vivo en Lota). | Requiere compilar a WASM para cliente o endpoint API en backend. | **Recomendado como motor de sincronización de eventos reales/digitales.** |

---

## 5. Proveedores de Mapa e Infraestructura (Self-Hosted vs Cloud)

```
                       ┌────────────────────────────────────────┐
                       │           OPCIONES DE MAPA             │
                       └───────────────────┬────────────────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    │                                             │
                    ▼                                             ▼
     ┌─────────────────────────────┐               ┌─────────────────────────────┐
     │   Self-Hosted Open-Source   │               │   Google Maps Platform      │
     │  (Tileserver-GL + OSRM)     │               │   (Maps JS API + Places)    │
     ├─────────────────────────────┤               ├─────────────────────────────┤
     │ • Costo: ~$15 USD/mes (VPS) │               │ • Costo: $100 - $300 USD/m  │
     │ • Control 100% de estilos   │               │ • Estilo estándar comercial │
     │ • Sin límite de peticiones │               │ • Cuotas por mil llamadas   │
     └─────────────────────────────┘               └─────────────────────────────┘
```

| Componente | Opción Self-Hosted (Open-Source) | Opción Google Maps Platform |
|---|---|---|
| **Tiles de Mapa** | `tileserver-gl` con datos OpenStreetMap de la Región del Biobío | Google Maps JS API |
| **Geocoding (Búsqueda)** | Nominatim self-hosted | Geocoding API de Google |
| **Ruteo Peatonal** | OSRM (Open Source Routing Machine) | Directions API de Google |
| **Costo Operativo Mensual** | **~$15 – $25 USD/mes** (Servidor VPS Hetzner/DigitalOcean) | **~$100 – $300 USD/mes** |

---

## 6. Cuadro de Decisión Tecnológica (Matriz Recomendada)

| Capa | Tecnología Seleccionada | Justificación |
|---|---|---|
| **Core Web App** | React + Vite + TypeScript (PWA) | Estándar de la industria, instalable en Android/iOS como app nativa. |
| **Render 3D y Mapa** | Three.js + React Three Fiber + MapLibre GL JS | Estética gamer sin licencias de pago por consumo. |
| **Geofencing** | Turf.js (cliente) + PostGIS (servidor) | Respuesta instantánea sin latencia de red. |
| **Backend API** | Python FastAPI (o Rust `celestial.rs`) | Facilidad de integración y velocidad de desarrollo. |
| **Base de Datos** | PostgreSQL 16 + extensiones espacial PostGIS 3.4 | Potencia espacial robusta para zonas y reportes. |
| **Servicios de Mapa** | Tileserver-GL + OpenStreetMap (Self-Hosted) | Costo operativo fijo ultra bajo ($15 USD/mes). |
