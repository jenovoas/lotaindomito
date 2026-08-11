# Propuesta — Lota Indómito: Guardianes de la Cuenca

**Para:** Concurso público de turismo cultural / patrimonio
**Cierre:** Fines de agosto o primera semana de septiembre 2026
**Cliente:** la clienta
**Responsable técnico:** Jaime Novoa Sepúlveda
**Fecha:** 2026-08-10
**Estado:** consolidado — listo para revisión de la clienta

---

## 1. Resumen

**Lota Indómito: Guardianes de la Cuenca** es un juego de exploración patrimonial para celular, estilo Pokémon GO, ambientado en Lota, Chile. El jugador recorre la ciudad, descubre su historia carbonífera, completa misiones en cada lugar, gana insignias y diplomas, y reporta problemas al municipio.

**Qué se entrega en esta etapa:** propuesta escrita + demo jugable de interfaz + maqueta navegable de las pantallas del juego.

**Plazo de piloto:** 3-4 semanas tras adjudicación.

---

## 2. El problema

Lota tiene un patrimonio carbonífero único —el Chiflón del Diablo, los Pabellones, el Parque Isidora Cousiño, los oficios del mar— que no tiene una estrategia digital que conecte a los visitantes con la memoria del lugar.

Las instituciones no tienen herramientas para medir el interés de la comunidad en los distintos sectores. El municipio no recibe reportes ciudadanos estructurados. Los oficios y relatos del carbón se pierden sin registro vivo.

---

## 3. La solución

Un juego que transforma el recorrido patrimonial en una experiencia interactiva:

- El visitante abre el juego en su celular al llegar a Lota.
- Camina por la ciudad y al entrar a una zona patrimonial el juego se activa.
- Cada zona tiene una misión: descubrir un personaje histórico, resolver un acertijo, completar un recorrido.
- Al completar misiones gana Carboncillos (puntos del juego), insignias y diplomas digitales.
- Puede reportar problemas (basura, derrumbe, seguridad) que llegan directamente al municipio.
- El municipio y las instituciones patrimoniales reciben estadísticas: cuánta gente visita cada zona, qué rutas son las más recorridas, qué reportes se han enviado.

---

## 4. Zonas patrimoniales del piloto (3-5)

Tomadas del material que la clienta ya envió (prototipo Stitch + audios):

1. **Chiflón del Diablo** — mina de carbón, Monumento Nacional. Misión: descubrir la historia de los mineros.
2. **Parque de Lota / Isidora Cousiño** — parque histórico. Personaje: Isidora Goyenechea.
3. **Pabellón 83** — arquitectura industrial de los pabellones obreros.
4. **Teatro de Lota** — patrimonio cultural urbano.
5. **Costa / Oficios de Mar** — patrimonio inmaterial del borde mar. Personaje: La Chinchorrera Mayor.

Los personajes históricos (Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor, El Palanquero) aparecen en cada zona como guías del jugador.

**Nota:** las zonas se pueden ajustar según lo que la clienta priorice con el municipio. Esto es el punto de partida.

---

## 5. Mecánicas de juego

| Mecánica | Descripción |
|---|---|
| Exploración | El jugador camina por Lota y el GPS detecta cuándo entra a una zona |
| Misiones | Cada zona tiene una misión temática (acertijo, recorrido, foto) |
| Carboncillos | Puntos del juego que se ganan al completar hitos |
| Insignias | Medallas por logros específicos (ej: "Ojo de Lince" por reportes) |
| Diplomas | Certificado digital al completar un recorrido completo |
| Reportes | Botón de reporte ciudadano (basura, peligro, infraestructura) |
| Rangos | Progresión: Aprendiz → Capataz → Leyenda de la Cuenca |
| Estadísticas | Panel para el municipio con datos de visitas y reportes |

---

## 6. Modos de juego

- **Modo Jugador:** experiencia completa con misiones, ranking y recompensas.
- **Modo Turista:** recorrido contemplativo con audioguías e información histórica, sin temporizadores.
- **Modo Familia:** multijugador cooperativo con roles (Vigía, Cronista, Fotógrafo).

---

## 7. Interfaces del juego

El proyecto cuenta con 52 pantallas de referencia ya diseñadas (prototipo Stitch enviado por la clienta). Estas pantallas muestran cómo se ve el juego:

- Mapa interactivo de Lota con zonas y rutas
- Selección de modo de juego (Jugador / Turista / Familia)
- Pasaporte del jugador (perfil, rango, insignias)
- Bitácoras de guardianes (colección de logros)
- Encuentros con personajes históricos
- Misiones por zona
- Sistema de reportes ciudadanos
- Dashboard de autoridades (mapa de calor de incidencias)
- Canje de Carboncillos en feria
- Bóveda de diplomas

Estas pantallas son la guía visual para el desarrollo del piloto.

---

## 8. Tecnología (resumen para no técnicos)

El juego se construye con tecnología de código abierto, sin depender de Google Maps ni de plataformas privadas que cobran por uso. Todo el mapa, la geolocalización y los datos viven en servidores propios del proyecto.

**Se evaluarán dos pilotos en paralelo:**

- **Piloto A — Tecnología de mercado:** aplicación web progresiva (PWA) con Vue 3 + MapLibre + OpenStreetMap + FastAPI. Corre en el navegador del celular desde el primer día, GPS real, rápida de construir.
- **Piloto B — Motor gráfico propio:** videojuego construido en Rust con wgpu (Vulkan/WebGPU) y el framework matemático Sentinel S60. Permite control total de la experiencia y sincronización con el cielo real sobre Lota.

Ambos pilotos comparten el mismo contenido: las 5 zonas, las misiones, los personajes, los reportes ciudadanos y las estadísticas municipales. La diferencia está en la experiencia del jugador. La evaluación técnica decide cuál es la versión definitiva.

El proyecto aplica el framework matemático desarrollado por el responsable técnico (Jaime Novoa) llamado **Sentinel S60** — un sistema de cálculo de precisión que permite sincronizar el juego con eventos del cielo real sobre Lota (estrellas visibles, fase lunar, ciclos solares). Esto significa que el cielo del juego cambia con el cielo real del jugador: es un diferenciador único que ningún otro juego patrimonial ofrece.

El servidor del juego (`lota-server`) es propio: no depende de servicios externos de pago.

**Stack de código abierto autoalojado:**
- Mapa: OpenStreetMap + MapLibre
- Geolocalización: GPS del celular + cercos virtuales
- Base de datos: PostgreSQL + PostGIS (datos espaciales)
- Rutas: OSRM (cálculo de caminos)
- Piloto A: Vue 3 + TypeScript + MapLibre + OpenStreetMap + FastAPI
- Piloto B: Rust + wgpu + Sentinel S60 + Axum

---

## 9. Equipo

| Rol | Persona | Responsabilidad |
|---|---|---|
| Responsable técnico | Jaime Novoa Sepúlveda | Arquitectura, desarrollo, servidor, motor gráfico |
| Dirección de contenido | la clienta | Validación patrimonial, contenido histórico, vínculo municipio |

Jaime es arquitecto del framework matemático Sentinel (en producción, financiado), lo que elimina la curva de aprendizaje sobre el núcleo del proyecto.

---

## 10. Cronograma

| Semana | Foco | Entregable |
|---|---|---|
| 1 (10-16 ago) | Demo navegable + primer borrador de propuesta | Demo de interfaz jugable |
| 2 (17-23 ago) | Iteración con la clienta + ajuste de propuesta | Propuesta v2 + demo pulida |
| 3 (24-30 ago) | Cierre y envío | Propuesta final enviada al fondo |
| Gracia (31 ago-6 sep) | Respuesta a observaciones del fondo | (si las hay) |

**Hitos:**
- Viernes 14 de agosto: demo navegable lista para presentar
- Miércoles 19 de agosto: primera versión completa de la propuesta
- Sábado 22 de agosto: avales institucionales confirmados
- Viernes 28 de agosto: propuesta enviada al fondo

---

## 11. Presupuesto


|---|---|
| Honorarios Jaime (3 semanas, 120 h) | 5.400.000 |
| Honorarios la clienta (3 semanas, 60 h) | 2.700.000 |
| Infraestructura (servidor, 3 meses) | 75.000 |
| Diseño de interfaz | 600.000 |
| Contenido patrimonial | 200.000 |
| Assets visuales | 300.000 |
| Traducciones (inglés, opcional) | 100.000 |
| Contingencia (10%) | 625.000 |

**Forma de pago:**
- 30% al firmar acuerdo
- 30% al entregar demo navegable (semana 1)
- 30% al aprobar propuesta escrita (semana 3)
- 10% al cierre

---

## 12. Fondo del Patrimonio (postulación paralela)

Se puede postular en paralelo al Fondo del Patrimonio. Los recursos adicionales se destinan a:
- Versión móvil con GPS real (fase 2)
- Producción de contenido audiovisual (videos de oficios)
- Ampliación a las 8 rutas completas
- Tótems QR en sitio
- Mantención por 12 meses

---

## 13. Impacto esperado

- **Patrimonial:** visibilización del patrimonio carbonífero de Lota ante visitantes nacionales e internacionales.
- **Educativo:** aprendizaje vivencial sobre la historia del carbón, oficios del mar y arquitectura de pabellones.
- **Ciudadano:** canal directo de reportes desde los visitantes hacia el municipio.
- **Institucional:** métricas concretas de uso y de reportes para la toma de decisiones.
- **Económico:** prolongación de la estadía de turistas en Lota y dinamización del comercio local.

---

## 14. Anexos

- Documento de diseño del juego (`docs/concepto-juego.md`)
- 52 pantallas de referencia del prototipo Stitch (`public/stitch/`)
- Transcripciones de los audios de la clienta (`_analisis/transcripciones/`)
- Carta Gantt detallada (`_analisis/08_carta_gantt_3_semanas.md`)
- Presupuesto detallado (`_analisis/09_presupuesto_referencial.md`)
- Registro de decisiones (`docs/decisiones.md`)
