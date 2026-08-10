# Propuesta de Arquitectura y Estudio Técnico: Servidor Dedicado de Juego en Rust (`lota-server`)

**Fecha:** 2026-08-09  
**Estado:** Documento de Estudio e Investigación (R&D)  
**Destino:** Equipo técnico de *Lota Indómito*

---

## 1. Resumen Ejecutivo

Este documento reúne la propuesta de arquitectura técnica para el desarrollo de un **servidor de juego dedicado de ultra alto rendimiento en Rust (`lota-server`)**, capaz de ofrecer una experiencia gráfica fluida (60–140+ FPS en cliente y latencia < 20 ms) para el juego *Lota Indómito*.

La arquitectura integra:
- **Simulación espacial a alto tick-rate (64 Hz – 128 Hz)** en Rust.
- **Geofencing en sub-microsegundos** mediante R-Trees en memoria RAM (`rstar`).
- **Comunicación híbrida de red** (WebSockets Axum + UDP/QUIC).
- **Bus de eventos en tiempo real y colas de tareas** con Redis Pub/Sub y Streams (basado en los patrones de `mycnet` y `soma`).
- **Persistencia espacial** con PostgreSQL 16 y PostGIS 3.4.

---

## 2. Diagrama General de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CLIENTES DE JUEGO (MULTIPLATAFORMA)                  │
│                                                                         │
│  ┌──────────────────────────────────┐  ┌──────────────────────────────┐  │
│  │ Cliente Nativo Rust (Bevy Engine)│  │ PWA Web (WASM / WebGPU / R3F)│  │
│  │ Render 120+ FPS (Desktop/Mobile) │  │ Render Web (Navegador)       │  │
│  └──────────────────┬───────────────┘  └──────────────┬───────────────┘  │
└─────────────────────┼─────────────────────────────────┼─────────────────┘
                      │ QUIC / UDP                      │ WebSocket (ws://)
                      ▼                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   SERVIDOR DEDICADO RUST (`lota-server`)                │
│                                                                         │
│  ┌──────────────────────────────┐    ┌───────────────────────────────┐  │
│  │ Network Layer (Axum + Tokio) │    │ Simulation Loop (64/128 Hz)   │  │
│  │ Sockets, API REST, WebSocket │    │ Tick Engine & Estado de Juego │  │
│  └──────────────┬───────────────┘    └──────────────┬────────────────┘  │
│                 │                                   │                   │
│                 ▼                                   ▼                   │
│  ┌──────────────────────────────┐    ┌───────────────────────────────┐  │
│  │ Memory Spatial Index (rstar) │    │ Event Handlers (mycnet style) │  │
│  │ R-Tree Geofencing < 50ns     │    │ Reacciones asíncronas         │  │
│  └──────────────────────────────┘    └──────────────┬────────────────┘  │
└─────────────────────────────────────────────────────┼───────────────────┘
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       │                                                             │
                       ▼                                                             ▼
┌──────────────────────────────────────────┐    ┌──────────────────────────────────────────┐
│      REDIS (Broker & Worker Queue)       │    │         POSTGRESQL 16 + POSTGIS          │
│ • Eventos globales en vivo (Pub/Sub)     │    │ • Persistencia de usuarios y Carboncillos│
│ • Colas de tareas pesadas (Streams)      │    │ • Almacenamiento de polígonos de la comuna│
└──────────────────────────────────────────┘    └──────────────────────────────────────────┘
```

---

## 3. Especificación Detallada por Capa

### 3.1 Servidor Dedicado (`lota-server`)
- **Lenguaje:** Rust (Edición 2021 / 2024).
- **Runtime Asíncrono:** `tokio` (multi-threaded executor).
- **Paralelización de Cómputo:** `rayon` / Bevy Tasks para procesamiento paralelo SIMD de entidades.
- **Bucle de Simulación (Tick Loop):** 64 Hz con temporizador atómico de alta precisión (`tokio::time::interval_at`).
- **Protocolos de Entrada/Salida:**
  - `axum 0.7` + `tokio-tungstenite` para conexiones WebSocket desde navegadores PWA (`/api/v1/stream`).
  - `quinn` (QUIC sobre UDP) para clientes nativos con transmisión binaria ultra rápida.

### 3.2 Motor Espacial y Geofencing en Memoria
- **Crate:** `rstar` (R-Tree 2D/3D en memoria RAM).
- **Funcionamiento:** Todos los polígonos de las zonas turísticas de Lota se cargan en la RAM al iniciar el servidor en una estructura R-Tree.
- **Rendimiento:** Las consultas espacial `is_point_in_polygon` o `nearest_neighbors` se resuelven en **menos de 50 nanosegundos**, eliminando consultas a base de datos en el bucle principal.
- **Integración Hexagonal:** Soporte opcional con `h3o` (Uber H3 en Rust) para indexación espacial $O(1)$.

### 3.3 Bus de Eventos y Orquestador (Patrones `mycnet` y `soma`)
- **Pub/Sub de Eventos Globales (Redis Channels):**
  - Notificación instantánea de eventos comunales (ej. festividades patrimoniales, eventos especiales en la Ruta del Carbón).
  - Sincronización de estado cuando se ejecutan múltiples instancias de `lota-server`.
- **Cola de Tareas Asíncronas (Redis Streams / Workers):**
  - Desacoplamiento de tareas pesadas fuera del bucle de simulación:
    - Generación de diplomas PDF descargables.
    - Validación comunitaria de reportes ciudadanos.
    - Persistencia diferida en PostgreSQL.
- **Handlers Desacoplados:** Arquitectura basada en traits (`MycNetHandler`) y canales `tokio::sync::mpsc` para procesar mensajes sin bloqueos.

### 3.4 Cliente de Juego (Multiplataforma)
- **Opción A (Nativa de Alto Rendimiento):** **Bevy Engine** en Rust. Compila directamente a Vulkan (Linux/Android), Metal (macOS/iOS) y DirectX 12 (Windows) alcanzando **120+ FPS**.
- **Opción B (Web PWA):** Mismo código de Rust compilado a **WebAssembly (`wasm32-unknown-unknown`)** con WebGPU/WebGL2 o integración con Three.js / React Three Fiber.
- **Técnicas de Fluidez:**
  - *Client-Side Prediction:* El movimiento local se procesa a 0 ms de respuesta visual.
  - *Server Reconciliation:* Interpolación suave (*lerp*) ante deltas recibidos del servidor.

---

## 4. Matriz de Componentes Reutilizables del Ecosistema

| Módulo / Crate | Proyecto de Origen | Función en `lota-server` |
|---|---|---|
| **`mycnet-daemon`** | `mycnet` | Base del servidor HTTP/WebSocket en Axum para conexiones de clientes. |
| **`mycnet-connect`** | `mycnet` | Estructura de traits y handlers asíncronos de eventos (`MycNetHandler`). |
| **Orquestación SOMA** | `sentinel/.soma` | Patrón de contratos, validación de tareas y bus Pub/Sub sobre Redis. |
| **S60 / Math Utils** | `mycnet-core` | Utilidades matemáticas deterministas de punto fijo para cálculos exactos. |

---

## 5. Puntos de Estudio Recomendados para la Siguiente Fase

1. **Pruebas de Carga en R-Tree:** Validar el consumo de memoria y tiempo de respuesta de `rstar` con la cartografía real OpenStreetMap de Lota.
2. **Evaluación de Protocolo Web:** Comparar la latencia de WebSockets vs WebTransport (`wtransport`) en redes móviles 4G/5G de la Región del Biobío.
3. **Estrategia de Fallback Web:** Diseñar el pipeline de compilación Bevy WASM ↔ React Three Fiber para asegurar compatibilidad total en celulares gama media/baja.
