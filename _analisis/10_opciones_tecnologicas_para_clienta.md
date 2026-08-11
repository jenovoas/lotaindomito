# Opciones tecnológicas para Lota Indómito

**Para:** la clienta (CLIENTA)
**Fecha:** 2026-08-09
**Autor:** INTERLOCUTOR
**Nota (2026-08-10):** este menú quedó sin efecto — la decisión técnica es del responsable técnico, no de la clienta (D-013). El encuadre vigente es D-014 (corregida): A y B son capas de un mismo concepto (teléfono + motor/Sentinel + RA), y el motor es el centro. El documento se conserva como comparativa histórica de ambas opciones.

---

## Qué hay que decidir

Lota Indómito puede construirse de dos formas distintas. Las dos cumplen el brief (juego de recorrido por Lota, gamificación, estadísticas para el Municipio). La diferencia está en la experiencia del jugador, los plazos y la forma de llegar al celular.

---

## Opción A · Aplicación web progresiva

**Qué es:** una aplicación que vive en el navegador del celular. La persona abre un enlace (o instala la aplicación desde el navegador, sin pasar por tiendas), ve el mapa de Lota, camina, el GPS detecta que entró a una zona y se activan las misiones.

**Qué incluye el piloto:**
- Mapa interactivo de Lota con 3-5 zonas patrimoniales.
- Detección por GPS al entrar a cada zona (cercos virtuales).
- Registro en el lugar con foto o código QR en el sitio.
- Insignias y diplomas digitales.
- Reportes ciudadanos (basura, derrumbe, infraestructura) hacia un panel para el Municipio.
- Estadísticas de uso.

| | |
|---|---|
| GPS real en celulares | Desde el día uno, en cualquier celular (Android y iPhone) |
| Instalación | Enlace directo o "agregar a pantalla de inicio" |
| Costo mensual | ~$15-25 USD (servidor) |
| Tiempo de piloto | 3-4 semanas |
| Estética | Mapa real de Lota estilizado con la paleta del proyecto |

**Fortalezas:** llega al celular de inmediato, barata, rápida de construir, fácil de mantener por el equipo municipal.

**Limitaciones:** la experiencia es de "aplicación con mapa", no de videojuego inmersivo; el 3D y los efectos de juego son limitados en el navegador.

---

## Opción B · Videojuego multiplataforma (Rust) con servidor propio

**Qué es:** un videojuego de verdad, construido con tecnología de punta usada en la industria (motor Bevy, lenguaje Rust). Se instala como programa en computador (Windows, Mac, Linux) y también corre dentro de la página web del proyecto. En una segunda fase llega al celular con GPS real.

**Qué incluye:**
- Videojuego con estética retro-industrial completa (paleta turquesa/coral/cobre, efectos, personajes).
- Versión de escritorio (ejecutable) para demostraciones y tótems.
- Versión web: el juego corre en la página oficial del proyecto, sin instalar nada.
- **Servidor propio dedicado (`lota-server`)** con arquitectura detallada en `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md`: `tokio` + `axum` + WebSockets + QUIC sobre UDP (`quinn`) para clientes nativos + R-Tree espacial (`rstar`, geofencing < 50 nanosegundos por punto en polígono) + opcional `h3o` (H3 hexagonal) + Redis Pub/Sub y Streams para eventos globales y cola de tareas asíncronas + PostgreSQL 16 + PostGIS para persistencia.
- **Cliente gráfico ultra rápido** según `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md`: Bevy Engine (ECS puro, paralelización automática multihilo, render WGPU Vulkan/Metal/DX12/WebGPU, 120+ FPS) o WGPU directo (acceso máximo a GPU). Compilación nativa (Linux/Win/Android/iOS) y WASM (WebGPU/WebGL2) para navegador.
- **Sistema celestial soberano sincronizado con estrellas reales** del core S60 de Sentinel (matemática base-60, sin decimales flotantes): el juego calcula en tiempo real qué estrellas, planetas y fase lunar están visibles sobre Lota (latitud -37.09, longitud -73.16) y desbloquea quests, personajes y eventos cuando determinada Estrella Real — Aldebarán, Régulo, Antares, Fomalhaut — sale por el horizonte o cuando la Luna entra en fase específica. El cielo del juego cambia con el cielo real del jugador. Es un diferenciador único: ningún otro juego patrimonial hace esto. Ver `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md` sección 5 (estrategia) que referencia explícitamente el estado en `celestial` del servidor dedicado.
- Modo virtual (teletransporte a las zonas) para probar y demostrar sin estar en Lota.
- Fase 2: versión para celulares con GPS real.

| | |
|---|---|
| GPS real en celulares | Fase 2 (la tecnología móvil de Rust está madurando; el piloto usa modo virtual + página web) |
| Instalación | Computador: ejecutable. Página web: nada. Celular: fase 2. |
| Costo mensual | ~$15-25 USD (servidor propio) |
| Tiempo de demo | 3-4 semanas (demo de escritorio + página web para la postulación) |
| Estética | Videojuego completo: control total de luces, efectos, personajes 3D |
| Diferenciador | Sistema celestial soberano sincronizado con cielo real, sin Google ni decimales flotantes |
| Arquitectura | `lota-server` (tokio+axum+QUIC+rstar+Redis+PostGIS+Bevy cliente) — ver `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` |

**Fortalezas:** experiencia de videojuego real (lo que más impresiona); sin dependencia de tiendas ni plataformas externas; la página web incluye el juego jugable; tecnología de alto rendimiento (Data-Oriented Design, R-Tree < 50ns, QUIC/UDP sin head-of-line blocking, 64 Hz tick loop); sistema de posicionamiento soberano que diferencia el proyecto; cliente nativo + web del mismo codebase.

**Limitaciones:** el GPS real en el celular llega en fase 2; el desarrollo del juego completo toma más tiempo que la aplicación web; R&D sobre coexistencia de clocks (64 Hz tick del juego + 41.77 Hz `IsochronousClock` de Sentinel) y buses (Redis Pub/Sub + `SOMA` orchestrator) está abierto.

---

## Comparación directa

| Criterio | Opción A (aplicación web) | Opción B (videojuego Rust) |
|---|---|---|
| GPS en celulares | Día uno | Fase 2 |
| Experiencia de juego | Aplicación gamificada | Videojuego inmersivo |
| Página web del proyecto | Informativa + enlace a la aplicación | Informativa + el juego corriendo en la web |
| Costo mensual | ~$15-25 USD | ~$15-25 USD |
| Tiempo de piloto / demo | 3-4 semanas | 3-4 semanas (demo), juego completo en más fases |
| Dependencia externa | Ninguna | Ninguna |
| Sistema celestial | — (no aplica) | Soberano (base-60) sincronizado con cielo real |
| Riesgo principal | Menor "factor wow" | GPS móvil se resuelve en fase 2 |

---

## Camino recomendado (se pueden combinar)

Las opciones no se excluyen en el tiempo: se puede partir con la Opción A como piloto para validar el recorrido en Lota con GPS real, y desarrollar la Opción B como la versión definitiva del juego cuando el proyecto esté adjudicado. También se puede apostar directo por la B si la prioridad es la experiencia de videojuego desde la postulación.

**Para decidir, la pregunta clave es:** ¿qué importa más para el piloto — que funcione en el celular de cualquier visitante desde el primer día (A), o mostrar el videojuego completo que Lota Indómito llegará a ser (B)?

---

## Documentos de respaldo

- `_analisis/05_analisis_tecnologias_disponibles.md` — comparativa de marcos de trabajo y motor de renderizado.
- `_analisis/06_investigacion_motores_rust_juegos_ultra_rapidos.md` — investigación de motores Rust (Bevy, WGPU, Fyrox, Macroquad) + arquitectura de servidor dedicado (UDP/QUIC, ECS, R-Tree con `rstar`, H3 con `h3o`, 64-128 Hz tick loop).
- `_analisis/07_propuesta_arquitectura_servidor_rust_juego.md` — propuesta detallada de `lota-server` (tokio+axum+QUIC+R-Tree+Redis Pub/Sub+PostgreSQL+PostGIS+Bevy cliente) y matriz de componentes reutilizables del ecosistema Sentinel (mycnet-daemon, mycnet-connect, SOMA, mycnet-core S60/utils).
- `sentinel/me-60os-core/src/celestial.rs` y `sentinel/quantum/celestial_navigation.py` — código del sistema celestial soberano (base-60 puro) del core de Sentinel (implementado, en producción, financiado) que se integra como cliente en la Opción B. Lota Indómito aplica los módulos del core S60 a su caso de uso.
- `docs/decisiones.md` D-010 y D-010-A — decisiones sobre la integración de módulos Sentinel en Lota Indómito (roles específicos propuestos pendientes de confirmación con INTERLOCUTOR).
- `docs/concepto-juego.md` — documento de diseño del juego del proyecto.
- `_analisis/12_inputs_pendientes_de_interlocutor.md` — inputs pendientes para cerrar este documento: buses SOMA vs Redis Pub/Sub (R&D), confirmación de roles MVP, elección la clienta (P-004).
