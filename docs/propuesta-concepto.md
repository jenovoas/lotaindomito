# Propuesta de Concepto del Proyecto Lota Indómito

Diseño, especificación y plan de desarrollo por etapas

---

**Autor:** Jaime Novoa Sepúlveda

**Licencia:** Apache 2.0 + Cláusula No Comercial (D-009)

**Estado del proyecto:** concepto cerrado, especificación completa, plan de desarrollo por etapas

**Audiencia:** Municipio de Lota, CMN, instituciones patrimoniales, comerciantes locales,
empresas co-financiadoras, Fabiola (clienta) y quien ella indique

**Nota sobre el alcance de este documento:** lo que sigue es la propuesta de concepto
del proyecto Lota Indómito. No es una propuesta de postulación a fondo específico.
Este documento describe lo que el proyecto ES y puede servir como material de soporte
técnico y diseño para lo que Fabiola decida hacer con él.

---

## Encabezado

### Resumen del proyecto

Lota Indómito es un juego tipo Pokémon GO ambientado en Lota, Chile. El encuadre
vigente del concepto es D-014: el mundo real maneja el juego, matemática soberana
S60 sin floats, sin Google.

El jugador recorre las calles y zonas históricas de la comuna, descubre personajes
del pasado carbonero de Lota, completa misiones, recoge minerales y sube de rango.
Los personajes confirmados en el GDD son cuatro figuras históricas vinculadas a la
cultura del carbón: Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor
y El Palanquero. Las rutas temáticas son ocho, cada una con mecánicas de juego
propias.

El sistema económico del juego es un esquema multi-moneda de minerales (D-016,
propuesta vigente): Cobre (Cu, base, común), Oro (Au, medio, 100 cobre) y
Estaño (Sn, raro, 10.000 cobre). Cada mineral tiene identidad narrativa propia,
se gana por acciones diferenciadas y es transferible entre usuarios.

La sincronización con el mundo real opera en dos niveles. Los World Events
(§10 del GDD) alinean el juego con festividades reales y estaciones del año
para coordinar flujos turísticos hacia el comercio local. Los eventos del
cielo calculados por Sentinel S60 (§2.4 del GDD) determinan qué personajes,
portales y recompensas están activos en cada momento.

El sistema de subastas digitales (D-017, propuesta vigente) integra al juego
un marketplace donde usuarios listan productos o servicios del comercio local
de Lota para subastar, pagados exclusivamente con minerales del juego. El juego
cobra comisión sobre cada operación.

### Norte del proyecto

Potenciar el turismo de Lota para revivir el comercio local. El juego es el
medio, no el fin: patrimonio y jugabilidad llevan turistas a la comuna, el
juego los guía por las zonas y el comercio, el comercio revive y autofinancia
la plataforma. El modelo de ingresos es el comercio local que paga comisión
por el flujo que el juego le genera. La plataforma no cobra al usuario final.

### Expansión regional

Lota es la prueba de concepto. El modelo se expande a Curanilahue, Lebu,
Arauco y Concepción, que forman el corredor patrimonial de la zona del carbón
en la Provincia de Arauco. El motor del juego es agnóstico de comuna: cada
localidad aporta su propio contenido, sobre la misma plataforma. El modelo
de autofinanciamiento se replica por comuna. Esto convierte el proyecto de
una comuna en un modelo regional escalable, uno de los argumentos más
fuertes para la propuesta a fondos públicos.

### Estado actual

Según `docs/estado.md` §11, la maqueta piloto está en preparación con D-014
como encuadre vigente. El entregable de los próximos treinta días es un
piloto o diseño de concepto que demuestra el diferenciador central, no el
juego completo. La fase 1 arranca después de la maqueta.

| Ítem | Valor |
|---|---|
| Entregable treinta días | Piloto o diseño de concepto que demuestra el diferenciador |
| Dispositivos | Teléfono (PWA, Piloto A: Vue 3 + MapLibre + Turf) + gafas RA (Meta Quest 3/3S) |
| Motor | Piloto B / Sentinel es el centro del concepto, no R&D congelado |
| Código | `piloto-a/` (teléfono) y `rust/` (motor); convenciones en `.gitignore` |
| Fuera de alcance (~30 días) | Juego completo, ocho rutas completas, GPS real, etapa dos de comercio |

La postulación a fondos públicos es dominio de la clienta. El diseño del
proyecto es dominio del responsable técnico. La decisión de cómo usar este
documento en una postulación es de Fabiola.

---

## Propósito del documento

Este documento es la propuesta de concepto del proyecto Lota Indómito.
No es una propuesta de postulación a fondo específico. Es el material
técnico y de diseño que describe lo que el proyecto ES, y que Fabiola puede
usar como soporte en lo que ella decida hacer con él.

La postulación a fondos públicos es domino de Fabiola. Este documento
describe el proyecto, no a qué fondo va ni cómo se estructura la postulación.

El documento cubre cinco partes:

- **Parte I — Concepto cerrado:** visión, personajes, rutas, mecánicas,
  sistema multi-moneda, World Events, subastas digitales, modelo económico.

- **Parte II — Especificación técnica:** arquitectura del sistema,
  motor propio S60, módulos de Sentinel en producción integrados al juego,
  Piloto A (PWA web) y Piloto B (motor Rust + Sentinel) como capas de un
  mismo sistema.

- **Parte III — Fundamentación teórica:** por qué funciona el modelo,
  turismo + patrimonio + jugabilidad como motor de comercio local,
  regionalidad y escalabilidad.

- **Parte IV — Plan de desarrollo por etapas:** alcance de la maqueta
  piloto, alcance de la fase uno, testing, normativa y gobernanza de datos.

- **Parte V — Cierre:** riesgos identificados, evaluación de ITIL como
  marco de operación, decisiones abiertas y referencias cruzadas.

---

## Convenciones del documento

**Idioma.** Este documento se redacta en español chileno. Las conjugaciones
y formas verbales respetan el registro chileno. Antes de cada commit se
ejecuta el detector de argentinismos sobre todos los archivos del repo;
cualquier coincidencia se corrige. La palabra "vale" es válida en español
chileno y no se trata como error.

**Reutilización de material existente.** El material preexistente del
proyecto se cita como referencia y no se duplica. Esto incluye:

- El GDD en `docs/concepto-juego.md` (350 líneas, Game Design Document).
- Las decisiones en `docs/decisiones.md` (D-014 es el encuadre vigente;
  D-016 y D-017 son propuestas abiertas).
- Los análisis técnicos en `_analisis/` (sistema multi-moneda,
  subastas digitales, World Events, loop del jugador, ML externo).
- Los módulos Rust de Sentinel integrados al juego (celestial,
  hexagonal control, lattice, SOMA orchestrator, isochronous clock,
  quantum memory, entre otros, todos documentados en decisiones).
- La bóveda de conocimiento en `~/Proyectos/PersonalVault/`.

El material del cliente almacenado en Google Drive se trata como referencia
externa. Los archivos `propuesta-fondo.md`, `_analisis/08_CARTA_GANTT_3_semanas.md`,
`_analisis/09_*`, `_analisis/11_*` y otros bajo la carpeta del Drive no se
modifican desde el repo. Se citan como referencia cuando se sincronizan
con `rclone bisync`.

---

## Notas operativas

| Campo | Valor |
|---|---|
| Estado del documento | Primera versión completa, 2026-08-10 |
| Responsable técnico | Jaime Novoa Sepúlveda |
| Clienta | Fabiola (operadora de la postulación a fondos) |
| Licencia | Apache 2.0 + Cláusula No Comercial (D-009) |
| Encuadre vigente | D-014, `docs/decisiones.md` §14 |

<!-- Las siguientes secciones (§1 Tesis, §2 Diseño de concepto D-014, §3 Sistema
multi-moneda D-016, §4 World Events, §5 Subastas digitales D-017, §6 Especificación
técnica Parte I, §7 Especificación técnica Parte II, §8 Módulos Sentinel en
producción, §9 Fundamentación teórica, §10 Plan de desarrollo por etapas,
§11 Testing y normativa, §12 Riesgos, §13 ITIL en evaluación, §14 Decisiones
abiertas, §15 Referencias) se desarrollan en las tareas 2-29 del plan. -->
