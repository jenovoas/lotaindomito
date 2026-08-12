# Decisiones del proyecto Lota Indómito

Registro de decisiones tomadas. **Fecha + decisión + razón + contraparte analizada.**

---

## Índice

### Por estado

| Estado | Decisiones |
|---|---|
| **Vigentes** (encuadran el proyecto hoy) | [D-006](#d-006--servidor-fase-1--python-fastapi), [D-007](#d-007--interfaz--vue-3--typescript), [D-011](#d-011--camino-c-confirmado--motor-propio-s60--pipeline-gpu-activo-2026-08-09), [D-012](#d-012--arquitectura-de-integracin-sentinel--gpu-confirmada-2026-08-09), [D-014](#d-014--encuadre-vigente-concepto-real-del-proyecto-2026-08-10-corregida-el-mismo-da), [D-018](#d-018--wire-format-s60-componentes-explcitos-en-api-rest-y-websocket-2026-08-12) |
| **Propuestas** (pendientes de aprobación) | [D-016](#d-016--reemplazo-de-carboncillo-por-sistema-multi-moneda-de-minerales-2026-08-10), [D-017](#d-017--subastas-digitales-de-cosas-reales-con-pago-en-minerales-2026-08-10) |
| **Operativas** (reglas y procedimientos) | [D-001](#d-001--sync-bidireccional-con-drive-para-lotaindomito), [D-002](#d-002--transcripcin-local-con-faster-whisper), [D-003](#d-003--espaol-chileno-obligatorio-en-redaccin) |
| **Históricas** (contexto de módulos y decisiones viejas) | [D-002](#d-002--memoria-operativa-en-docs-separada-de-_analisis), [D-003](#d-003--event-engine-ejemplo-celestialrs--sincronizacin-eventos-digitales--reales), [D-004](#d-004--entregable-para-el-fondo--propuesta--maqueta--demo-de-interfaz), [D-005](#d-005--alcance-del-piloto--lean-doc-04-sin-3d-ni-minijuegos), [D-008](#d-008--la-pila-tcnica-del-juego-la-elige-cliente-de-un-men-de-opciones), [D-009](#d-009--autorizacin-de-uso-de-celestialrspy-en-lota-indmito), [D-010](#d-010--lota-indmito-integra-mdulos-matemticos-del-core-s60-de-sentinel-celestial-como-caso-de-uso), [D-010-A](#d-010-a--mdulos-del-framework-sentinel-identificados-para-integrar-al-juego-rol-especfico-propuesto-pendiente-confirmacin), [D-013](#d-013--dos-pilotos-en-paralelo-motor-propio-vs-tecnologa-de-mercado-2026-08-10) |

### Por dominio

| Dominio | Decisiones |
|---|---|
| **Concepto / diseño del juego** | [D-014](#d-014--encuadre-vigente-concepto-real-del-proyecto-2026-08-10-corregida-el-mismo-da), [D-016](#d-016--reemplazo-de-carboncillo-por-sistema-multi-moneda-de-minerales-2026-08-10), [D-017](#d-017--subastas-digitales-de-cosas-reales-con-pago-en-minerales-2026-08-10) |
| **Motor / Piloto B (Sentinel S60)** | [D-009](#d-009--autorizacin-de-uso-de-celestialrspy-en-lota-indmito), [D-010](#d-010--lota-indmito-integra-mdulos-matemticos-del-core-s60-de-sentinel-celestial-como-caso-de-uso), [D-010-A](#d-010-a--mdulos-del-framework-sentinel-identificados-para-integrar-al-juego-rol-especfico-propuesto-pendiente-confirmacin), [D-011](#d-011--camino-c-confirmado--motor-propio-s60--pipeline-gpu-activo-2026-08-09), [D-012](#d-012--arquitectura-de-integracin-sentinel--gpu-confirmada-2026-08-09), [D-013](#d-013--dos-pilotos-en-paralelo-motor-propio-vs-tecnologa-de-mercado-2026-08-10), [D-018](#d-018--wire-format-s60-componentes-explcitos-en-api-rest-y-websocket-2026-08-12) |
| **Piloto A (frontend PWA)** | [D-005](#d-005--alcance-del-piloto--lean-doc-04-sin-3d-ni-minijuegos), [D-007](#d-007--interfaz--vue-3--typescript), [D-008](#d-008--la-pila-tcnica-del-juego-la-elige-cliente-de-un-men-de-opciones), [D-018](#d-018--wire-format-s60-componentes-explcitos-en-api-rest-y-websocket-2026-08-12) |
| **Backend / infra** | [D-001](#d-001--sync-bidireccional-con-drive-para-lotaindomito), [D-006](#d-006--servidor-fase-1--python-fastapi), [D-018](#d-018--wire-format-s60-componentes-explcitos-en-api-rest-y-websocket-2026-08-12) |
| **Operación y reglas del proyecto** | [D-002](#d-002--transcripcin-local-con-faster-whisper), [D-002](#d-002--memoria-operativa-en-docs-separada-de-_analisis), [D-003](#d-003--espaol-chileno-obligatorio-en-redaccin), [D-003](#d-003--event-engine-ejemplo-celestialrs--sincronizacin-eventos-digitales--reales), [D-004](#d-004--entregable-para-el-fondo--propuesta--maqueta--demo-de-interfaz) |

---

## 2026-08-12

### D-018 · Wire format S60 componentes explícitos en API REST y WebSocket (2026-08-12)

- **Decisión:** las coordenadas geográficas de los NPCs transmitidas por la API REST (`/npcs`) y eventos WebSocket se serializan como cinco componentes sexagesimales enteros explícitos: `{"d": i64, "m": i64, "s": i64, "t": i64, "q": i64}` (`0 ≤ m,s,t,q < 60`). NO se transmite `i64` plano raw ni floats en el contrato de API.
- **Razón técnica:** los cálculos compuestos (distancias, proyecciones, sumas e integraciones temporales) acumulan error de redondeo si se truncan a `i64` plano entre operaciones, destruyendo la coherencia de fase en cristales y memorias S60. El formato de 5 componentes mantiene la estructura sexagesimal completa y permite carries discretos exactos entre órdenes. La conversión a grados decimales ocurre únicamente en la última milla del cliente (PWA Vue → MapLibre) mediante `s60ToDegrees` con `BigInt`. Regla dura "0 floats en CPU del motor" respetada.
- **Implementación:**
  - Backend: `rust/src/server/mod.rs` función `i64_to_s60_components` y struct `NpcWire`.
  - Frontend: `piloto-a/src/utils/s60-to-degrees.ts` helper y tests Vitest `piloto-a/tests/s60.spec.ts`.
- **Reversible:** sí, si se modifica la API de wire format.

---

## 2026-08-10

### D-016 · Reemplazo de Carboncillo por sistema multi-moneda de minerales (2026-08-10)

- **Decisión:** reemplazar el **Carboncillo** (`₡`) como moneda única del juego por un **sistema multi-moneda de minerales** con tres monedas: **Cobre** (Cu, común, base), **Oro** (Au, medio, 100 cobre), **Estaño** (Sn, raro, 10.000 cobre = 100 oro). Cada mineral tiene identidad narrativa propia, valor relativo, y se gana por acciones diferenciadas (cobre por misiones de comercio, oro por eventos del cielo, estaño por portales S60). Las monedas son transferibles entre usuarios (P2P), truequeables bilateralmente, comercianteables en el comercio local, y usables en subastas digitales de cosas reales.
- **Razón:** el carbón no es un metal precioso — es combustible, no resuena con la identidad minera metálica de Chile (cobre sobre todo). Una moneda única no incentiva interacción social ni crea economía emergente. El sistema multi-moneda refuerza D-014 (autofinanciamiento) con tres vías nuevas: (1) misiones World Event que requieren el comercio real, (2) comercio acepta múltiples minerales a tipo de cambio configurable, (3) subastas de cosas reales con pago en minerales + comisión del juego.
- **Contraparte analizada:** mantener Carboncillo único (rechazado — desaprovecha interacción social y economía emergente).
- **Reversible:** sí. El sistema puede volver a Carboncillo si el piloto no valida la hipótesis.
- **Estado actual (2026-08-10):** propuesta, pendiente de aprobación. Diseño completo en [`_analisis/23_sistema_monedas_minerales.md`](../_analisis/23_sistema_monedas_minerales.md). GDD actualizado con §4 sistema multi-moneda.

### D-017 · Subastas digitales de cosas reales con pago en minerales (2026-08-10)

- **Decisión:** integrar al juego un **sistema de subastas digitales** donde usuarios listan productos o servicios del comercio local para subastar, otros pujan usando **únicamente minerales del juego** (cobre, oro, estaño), el juego cobra una comisión del 5-10% y la entrega se coordina localmente en Lota. Objetos subastables: gastronomía local, artesanía, souvenirs del juego, libros, edición limitada, servicios (tour guiado, cena en restaurant, hospedaje, taller). Pago en CLP está excluido (sin Webpay, sin MercadoPago). Sistema de escrow retiene minerales hasta confirmación de entrega; sistema de reputación bilateral; resolución de disputas manual.
- **Razón:** convierte al juego en **marketplace soberano**, refuerza D-014 por una vía nueva (la comisión por subasta crea flujo de ingresos directo), diferencia la propuesta (no hay otra plataforma en Chile que mezcle turismo + patrimonio + economía interna de juego + subastas reales). El mineral estaño (rara) gana demanda real para subastar productos caros, lo que ata la rareza del estaño al valor económico concreto.
- **Contraparte analizada:** venta directa sin subasta (rechazado — pierde tensión de puja y engagement). Pago en CLP (rechazado — pierde integración con el juego y agrega dependencia de sistemas externos).
- **Reversible:** sí. El sistema puede desactivarse si la complejidad operativa no se justifica en el piloto.
- **Estado actual (2026-08-10):** propuesta, pendiente de aprobación. Diseño completo en [`_analisis/24_subastas_reales.md`](../_analisis/24_subastas_reales.md). GDD actualizado con §11 subastas digitales.
