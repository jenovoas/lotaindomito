# Presupuesto referencial — Lota Indómito

**Fecha:** 2026-08-09
**Estado (2026-08-10):** referencial — los valores hora/hombre se ajustarán al confirmar tarifas con INTERLOCUTOR y la clienta. Este presupuesto es material de la **postulación al fondo, dominio de la clienta** (D-014). P-004 fue cerrado por D-013 (dos pilotos en paralelo); la coexistencia de buses se resolvió el 2026-08-09 (convivencia provisional SOMA + Redis Pub/Sub). Queda pendiente la confirmación de roles MVP de módulos Sentinel (pregunta 2 de `_analisis/12_inputs_pendientes_de_interlocutor.md`).

> **Nota clave:** Lota Indómito es **cliente de Sentinel** (framework matemático S60 en producción y financiado del cual se reutilizan módulos ya implementados). Esto reduce drásticamente el esfuerzo de desarrollo del núcleo matemático: no se construye desde cero, se acopla y configura. Ver `docs/decisiones.md` D-010 y D-010-A para el detalle de módulos.

---

## Consideraciones generales

- **Cobertura del presupuesto:** incluye todos los gastos del proyecto, honorarios de INTERLOCUTOR y la clienta, infraestructura, contenido y contingencias.
- **Período cubierto:** desde el 2026-08-09 hasta la presentación al fondo (2026-08-30), más eventuales observaciones hasta 2026-09-06.
- **Etapa posterior:** si se gana el fondo, este presupuesto se refinará para el piloto de 3-4 semanas posterior a la adjudicación.
- **Upstream Sentinel:** el framework matemático S60 ya está implementado, compilado y en producción (7 daemons activos en host Fan). Su arquitectura, lattice pentagonal, reloj isocrónico, sistema celestial y MycNet están disponibles para integración. INTERLOCUTOR es arquitecto principal de Sentinel, lo que elimina la curva de aprendizaje sobre el framework.

---

## Opción A — Aplicación web progresiva (PWA)

### Resumen por línea

|---|---|---|
| Honorarios INTERLOCUTOR | 3 semanas de tiempo completo (120 h) | 5.400.000 |
| Honorarios la clienta | 3 semanas de tiempo parcial (60 h) | 2.700.000 |
| Infraestructura (VPS autoalojado) | $25 USD/mes × 3 meses | 75.000 |
| Diseño de interfaz y experiencia de usuario | por confirmar (externo) | 600.000 |
| Contenido patrimonial (textos, fotos, audios) | producción propia con la clienta | 200.000 |
| Traducciones (inglés para turistas) | opcional | 100.000 |
| Contingencia (10%) | imprevistos | 925.000 |

### Tarifa hora/hombre supuesta

- [Ambas tarifas son referenciales; INTERLOCUTOR y la clienta confirman al firmar acuerdo.]

---

## Opción B — Videojuego multiplataforma en Rust

### Resumen por línea

|---|---|---|
| Honorarios INTERLOCUTOR | 3 semanas de tiempo completo (120 h) — incluye trabajo en Bevy, Rust, integración de módulos del framework Sentinel (celestial, lattices, MHD, memorias, reloj de cristal, MycNet) con la opción B | 5.400.000 |
| Honorarios la clienta | 3 semanas de tiempo parcial (60 h) | 2.700.000 |
| Infraestructura (VPS autoalojado) | $25 USD/mes × 3 meses | 75.000 |
| Diseño de interfaz y experiencia de usuario | por confirmar (externo) | 600.000 |
| Contenido patrimonial (textos, fotos, audios) | producción propia con la clienta | 200.000 |
| Assets 3D (modelos, animaciones) | comprados o producidos (3 modelos) | 300.000 |
| Traducciones (inglés para turistas) | opcional | 100.000 |
| Contingencia (10%) | imprevistos | 625.000 |

### Tarifa hora/hombre supuesta

- [Ambas tarifas son referenciales; INTERLOCUTOR y la clienta confirman al firmar acuerdo.]

---

## Comparación de ambas opciones

| Concepto | Opción A (PWA) | Opción B (Rust) |
|---|---|---|
| Diferencia en honorarios | igual | igual |
| Diferencia en infraestructura | igual | igual |
| Diferencia en diseño | igual | igual |
| Diferencia en contenido | igual | igual |
| Diferencia en assets 3D | — | +300.000 |
| Diferencia en contingencia | igual | igual |
| Compensación interna | menor costo de oportunidad para INTERLOCUTOR (más eficiente en PWA) | menor riesgo por curva de Bevy + Rust |

**Nota:** las opciones tienen el mismo costo total. La diferencia real está en qué recibe el cliente (factor "wow" del videojuego vs implementación inmediata en el celular) y en la curva de aprendizaje técnica.

---

## Fondo del Patrimonio (postulación paralela)

Si se postula también al Fondo del Patrimonio, los recursos adicionales se destinan a:
- Versión nativa móvil del juego (fase 2 con GPS real).
- Producción de contenido audiovisual (audios, videos documentales de los oficios).
- Ampliación a las 8 rutas completas.
- Tótems QR en sitio con pantalla integrada.
- Mantención durante 12 meses posteriores al lanzamiento.

El desglose se desarrolla si la clienta confirma la postulación al Fondo del Patrimonio.

---

## Forma de pago sugerida

|---|---|---|
| Firma de acuerdo | 30% | 3.000.000 |
| Entrega de demo navegable (semana 1) | 30% | 3.000.000 |
| Entrega de propuesta escrita aprobada (semana 3) | 30% | 3.000.000 |
| Cierre del proyecto (semana de gracia) | 10% | 1.000.000 |

---

## Supuestos que ajustar

- **Tarifa hora/hombre:** confirmar con INTERLOCUTOR y la clienta antes de firmar el acuerdo.
- **Diseño externo:** INTERLOCUTOR puede cubrir el rol de diseñador si la clienta lo prefiere (ahorra la línea).
- **Contingencia:** si el proyecto se atrasa o aparecen imprevistos técnicos, se reduce el alcance del demo (de 5 a 3 zonas) o se renuncia a la traducción al inglés.

---

## Datos de contexto para el fondo

- **Costo de oportunidad de INTERLOCUTOR:** tarifa de mercado para desarrollador senior en Chile con experiencia en Rust, bases de datos espaciales, game dev y, especialmente, **arquitectura del framework matemático S60 de Sentinel** (matemática sexagesimal, protocolo Yatra, lattice pentagonal, MHD, MycNet). Como autor del upstream, la integración de módulos Sentinel al juego tiene costo de oportunidad cero en curva de aprendizaje.
- **Costo de oportunidad de la clienta:** tarifa de mercado para curadora patrimonial con vínculo institucional en Lota.
- **Plazo del proyecto:** 3 semanas intensivas, no se compara con un proyecto de 3 meses a tarifa mensual fija.
- **Ventaja de upstream propio:** el framework Sentinel es propiedad intelectual de INTERLOCUTOR (autor: Jaime Novoa Sepúlveda, licencias documentadas en `celestial.rs` y `celestial_navigation.py` con Apache 2.0 + cláusula No Comercial, autorización explícita para Lota Indómito en D-009 de `docs/decisiones.md`). No se pagan regalías ni licencias a terceros por el núcleo matemático.
- **Benchmarks disponibles del upstream:** módulos Sentinel tienen criterios medibles (p95 RTT < 50ms en MycNet, convergencia < 1s tras failover, tolerancia 50% pérdida de nodos, mecánica Kepleriana validada vs vis-viva Kepler, MHD validado por Muir & Nikiforakis 2022 arXiv:2207.09857). Ver `sentinel/docs/07_prompts/sentinel-knowledge-layer/SKILL.md` y `sentinel/docs/02_ciencia_y_quantum/papers/`.
