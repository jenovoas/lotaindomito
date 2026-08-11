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

## §1 Tesis

El distrito patrimonial carbonero de Lota enfrenta un deterioro comercial sostenido. Existen flujos turísticos hacia la comuna, pero carecen de un mecanismo de retención que obligue al visitante a quedarse, a caminar las calles, a volver. El comercio local está desconectado de ese flujo: el turista pasa de largo porque no tiene razones para detenerse ni para regresar. La solución convencional en este tipo de proyectos es construir una aplicación turística estática, un catálogo de puntos de interés que muestra dónde queda la cafetería y qué horario tiene el museo. Esa aplicación no funciona porque no mueve al usuario por la ciudad, no lo conecta con el comercio y no genera ningún motivo para que vuelva mañana.

La tesis de Lota Indómito invierte esa lógica. El proyecto no es una aplicación turística. Es un geo-RPG que utiliza el patrimonio carbonero de Lota como mundo narrativo y el comercio de la comuna como sustrato económico. El juego es el medio, no el fin: el patrimonio y la jugabilidad llevan turistas a caminar la comuna, el juego los guía por las zonas y los puntos de comercio, el comercio revive y ese comercio paga la comisión que autofinancia la plataforma. El modelo de ingresos no depende de suscripciones del usuario ni de venta de datos ni de publicidad. Depende del flujo turístico que el juego genera y de la comisión que el comercio local paga por ese flujo. El diferenciador técnico que hace posible la soberanía de esta plataforma es la matemática S60 de Sentinel (D-014, docs/decisiones.md): aritmética en base-60 sin decimales flotantes, sin dependencia de Google ni de infraestructura externa, replicable en cualquier comuna de la zona sin ceder control a terceros. Lota es la prueba de concepto; el corredor patrimonial de la zona del carbón, la escala.

El modelo opera a través de tres mecanismos concretos. Primero, los eventos del cielo determinados por Sentinel S60 (D-014, docs/decisiones.md §14): el sistema calcula qué personajes, portales y recompensas están activos en cada momento según la fecha, hora y posición sobre Lota. El cielo sobre la comuna hoy es el estado del juego hoy. Segundo, los World Events alinean el juego con festividades reales, Fiestas Patrias, San Juan y Día del Patrimonio entre otras, para coordinar flujos turísticos masivos hacia el comercio local en las fechas de mayor concentración (docs/decisiones.md D-014, _analisis/25_todo_continuacion.md §7). Tercero, el sistema de subastas digitales (D-017, docs/decisiones.md): el juego funciona como marketplace soberano donde los usuarios cambian minerales por productos y servicios reales del comercio de Lota. El comercio participa en el circuito, el juego cobra comisión sobre cada transacción y esa comisión es el flujo de ingresos que cierra el ciclo.

Lo que cambia con esto es la estructura de incentivos. La plataforma no se financia con plata del usuario, no extrae valor de sus datos y no depende de ningún actor externo para sobrevivir. Se financia con el comercio que recibe turistas y paga comisión por ese flujo. Es un servicio público de la comuna, no una startup buscando escala de usuarios. El motor del juego es agnóstico de localidad: cada comuna del corredor carbonero, Curanilahue, Lebu, Arauco, Concepción, aporta su propio contenido sobre la misma plataforma. El modelo de autofinanciamiento se replica por comuna y eso convierte el proyecto de una intervención puntual en una infraestructura regional.

El valor de esta propuesta es que ofrece un camino de reactivación comercial para Lota que no depende de plataformas externas que se llevan los datos y el margen, que no extrae valor del usuario, que no necesita subsidios permanentes para sostenerse y que produce información abierta sobre flujos turísticos, retención y retorno por comercio que justifica e informa la inversión pública en infraestructura patrimonial.

---

## §2 Diseño de concepto D-014

El encuadre D-014 establece que el mundo real maneja el juego. Esto no es una metáfora ni un adorno narrativo: es una descripción literal de la arquitectura. La posición geográfica de Lota sobre el planeta, la fecha y hora del día, y el estado del cielo sobre la comuna determinan qué personajes aparecen, qué zonas se desbloquean, qué eventos están activos y qué recompensas están disponibles en cada instante. El juego no inventa una realidad paralela; consulta el mundo real y responde. Esta sección describe cómo funciona cada componente del concepto, desde el cálculo celestial hasta la costura de baja latencia entre dispositivos.

### §2.1 Evento real determina el estado del juego

El módulo `celestial.rs` del motor Sentinel calcula, para cualquier fecha, hora y posición geográfica, el estado completo del cielo visible desde ese punto. En el caso de Lota Indómito, la posición de referencia es -37,09° de latitud sur y -73,16° de longitud oeste. La posición geográfica no se mide una sola vez: se usa en cada consulta para calcular con precisión kepleriana la posición de los cuerpos celestes sobre el horizonte de la comuna.

El reloj que gobierna este cálculo es el `IsochronousClock` de Sentinel, operando a 41,77 Hz con un tick de 23.939.835 nanosegundos. Su patrón de corrección es el Salto-17: cada 68 ticks del reloj, la fase YHWH (YOD, HEH, VAV, HEH) se corrige para mantener la coherencia de la pentaresonancia. Esto ocurre aproximadamente cada 1,6 segundos de tiempo real y genera un evento de sincronización que alinea el mundo digital con el mundo físico sin deriva de fase acumulada. No hay decimales flotantes en este cálculo; toda la aritmética opera en base-60 bajo el protocolo Yatra.

Dados una fecha y hora UTC, más la posición de Lota, el sistema calcula en tiempo real la elevación y azimut del Sol, la fase exacta de la Luna, la posición de los planetas visibles y la disponibilidad de las cuatro Estrellas Reales (Aldebarán, Régulo, Antares y Fomalhaut) sobre el horizonte. Este estado celestial se traduce directamente en estado del juego: si la Luna está en fase llena, El Palanquero se vuelve visible en su zona; si la Luna es nueva, las Chinchorreras aparecen con mayor frecuencia en el borde costero; si el Sol está en el horizonte occidental al atardecer, Isidora Goyenechea se activa en el Parque de Lota; si el reloj marca las 7 de la mañana, El Ciego de la Mina aparece en los Piques.

Lo mismo aplica para los eventos de mayor escala temporal. Los equinoccios y solsticios activan eventos especiales de una a dos horas con personajes exclusivos y recompensas de mayor valor. El día del equinoccio de septiembre, por ejemplo, el cielo sobre Lota produce una alineación que según el diseño del juego abre un portal en una de las ocho rutas. Este portal entrega una recompensa que no se repite nunca: su contenido depende de la convergencia exacta de los dos carriles de la lattice en ese instante, un evento matemáticamente único.

El cielo sobre Lota hoy es el estado del juego hoy. Si un visitante abre la aplicación en la tarde del 21 de junio y camina hacia el Parque, la aplicación sabe que es solsticio de invierno, que el Sol se pone más al norte sobre el horizonte de lo que lo hace en marzo, y que según esa posición la zona del Pabellón tiene una iluminancia que históricamente correspondía al turno de la tarde de los mineros. La correspondencia entre dato celestial y estado del juego no es aproximada: es exacta y reproducible. Cualquiera que repita el cálculo con los mismos inputs obtiene el mismo resultado, sin acceso a internet, sin API externa y sin posibilidad de falsificar el resultado.

### §2.2 Enjambre SOMA de NPCs simples y vivos

El juego no tiene personajes principales ni diálogos ramificados complejos. Tiene un enjambre: cuatro figuras históricas vinculadas al patrimonio carbonero de Lota que deambulan dentro de zonas definidas, aparecen y desaparecen según los eventos del cielo, entregan misiones contextuales y desaparecen cuando el evento termina o el jugador se aleja demasiado. Cada figura es un NPC sencillo con una máquina de estados finita de cuatro modos: inactivo, deambulando, jugador se acerca, entregando misión. No hay IA generativa, no hay modelos de lenguaje, no hay aprendizaje. Es una FSM determinista que cualquier programador puede leer y que reproduce bit a bit en aritmética S60.

El enjambre se coordina desde `me60os-core/src/soma_orchestrator.rs`. Este módulo actúa como orquestador central: recibe el estado celestial calculado por `celestial.rs`, decide qué NPC se activa, en qué zona, con qué misión y por cuánto tiempo. Los NPCs individuales no toman decisiones; el orchestrator les comunica qué hacer. La comunicación entre el orchestrator y los NPCs corre sobre Redis Pub/Sub en la dirección 10.10.10.2 puerto 6380, a 2 Hz. Cada tick de 500 milisegundos, el orchestrator evalúa el estado del mundo y distribuye órdenes de activación o desactivación a los NPCs dentro de su zona asignada.

Las cuatro figuras históricas tienen identidades y comportamientos distintos. Isidora Goyenechea guía a los jugadores por el Parque y les cuenta la historia de la familia que financió la construcción del Pabellón; su zona natural es el área verde y su activación es por evento de atardecer. El Ciego de la Mina aparece en los Piques al amanecer; su narrativa es la del minero veterano que conoce cada veta y cada accidente de la mina. La Chinchorrera Mayor opera en la Caleta al anochecer, con una ventana de actividad de noventa minutos; es esquiva, aparece más durante luna nueva. El Palanquero es visible principalmente durante luna llena y su aparición en el borde costero coincide con las mareas altas.

El diseño FSM no es una limitación accidental sino una decisión consciente. La investigación tecnológica del proyecto confirma que la máquina de estados finita es la arquitectura correcta para NPCs con modos fijos y poco volumen: la industria de los juegos la usa como base en la mayoría de las implementaciones reales, incluyendo títulos como Hitman y The Sims, donde se combina con sistemas más complejos solo donde el comportamiento emergente lo justifica. En Lota Indómito, los NPCs cumplen una función narrativa y de posicionamiento en la zona; la complejidad no vive en la inteligencia artificial sino en la coordinación central que decide qué NPC aparece cuando y dónde.

La ventaja práctica de esta arquitectura es que todo es reproducible y auditable. Si un jugador reporta que un personaje no apareció cuando debía, el equipo puede repetir el cálculo con los mismos inputs (fecha, hora, posición, estado celestial) y verificar exactamente qué decidió el orchestrator y por qué. No hay opacidad algorítmica, no hay caja negra de IA, no hay sesgo de modelo entrenado. El enjambre es determinista por diseño.

### §2.3 La caza en el teléfono

La interfaz primaria del jugador es su propio teléfono, sin necesidad de instalar nada. La aplicación es una PWA construida con Vue 3, TypeScript, MapLibre como visualizador de mapas y Turf.js para el cálculo de cercos virtuales en el cliente. La elección de Turf.js para el geofencing es deliberada: el cálculo se ejecuta en el navegador del usuario, no en un servidor, lo que elimina la latencia de red en la detección de entrada a zona y permite que la aplicación funcione offline durante la caminata por el Parque o el Chiflón, donde la cobertura de datos móviles puede ser irregular.

El flujo de una sesión de caza tiene cinco tramos fijos que se ejecutan en uno a cinco minutos. El jugador camina por una zona de Lota y la aplicación detecta, mediante Turf.js, que su posición está dentro del polígono de un POI. En ese instante la aplicación vibra y muestra un banner que dice algo como "Estás en el Chiflón del Diablo. Toca para descubrir." Este es el tramo de activación. El jugador toca la notificación y aparece la pantalla de contexto: mapa en miniatura, avatar del personaje histórico correspondiente, dos o tres frases de diálogo que contextualizan la misión y audio opcional con la voz del personaje. El texto en pantalla no supera las treinta palabras; no hay scrolls ni muros de información.

Después del contexto viene la acción. Es un minijuego táctil breve: un QTE de ritmo, una escena de objeto oculto o una trivia de una pregunta. El diseño permite que la acción dure entre sesenta y ciento ochenta segundos según el modo elegido por el jugador. El modo Jugador tiene la acción más demandante; el modo Turista solo requiere escanear un código QR o tomar una fotografía. Los minijuegos nunca se encadenan dentro de una misma sesión: una acción por micro-sesión, y nunca se penaliza con pérdida de minerales si el jugador falla; el reintento es inmediato.

Al completar la acción, el jugador recibe su recompensa: mineral de cobre en la mayoría de los casos, mineral de oro cuando la acción corresponde a un evento celestial activo, más puntos de experiencia y la animación de una insignia que se agrega a su pasaporte digital. La insignia es visible en su perfil compartido y funciona como objeto social: otros jugadores ven qué zonas completó y qué personajes conoció. El pasaporte digital nunca está incompleto de manera arbitraria: el jugador sabe exactamente qué le falta para cerrar cada ruta y puede imprimir o compartir su diploma cuando la completa al cien por ciento.

El quinto tramo cierra la sesión con una dirección. La aplicación nunca deja al jugador sin destino siguiente: la pantalla final muestra la ruta al siguiente POI con distancia y orientación. Esto mantiene el flujo de caminata sin que el jugador tenga que abrir Google Maps ni depender de señal de datos para saber hacia dónde caminar. El juego guía al turista por las calles de Lota hacia la siguiente zona, y esa caminata dirigida es el vector que conecta el flujo turístico con el comercio local.

La sesiones están diseñadas para que un visitante haga entre seis y diez micro-sesiones en una visita de dos a cuatro horas. El jugador no necesita estar pegado al teléfono; puede estar caminando, conversando, tomando café en un local cercano. La aplicación vibra cuando corresponde y se activa con un toque. Esta estructura de micro-sesión es el patrón central del engagement en Lota Indómito: contacto breve, acción clara, recompensa inmediata, dirección siguiente.

### §2.4 Encuentro en RA que reconstruye la historia

Cuando el jugador llega al punto de encuentro del NPC y decide profundizar la experiencia, la arquitectura prevê un segundo nivel de interacción basado en realidad aumentada. Este nivel no es parte del alcance de la fase uno ni de la maqueta piloto: es parte del diseño de la etapa dos, cuando el proyecto disponga de recursos para la reconstrucción histórica y las gafas de realidad aumentada estén disponibles en el sitio.

La experiencia RA se diseñará para operar con gafas Meta Quest 3 o Quest 3S, que el sitio podrá prestar a los visitantes que lo soliciten. El dispositivo tiene passthrough a color con profundidad por inteligencia artificial, Scene API para entender la geometría del espacio circundante y Spatial Anchors para anclar contenido virtual a posiciones fijas en el entorno. Cuando el jugador se coloca las gafas y mira hacia el Chiflón del Diablo, el sistema detecta su posición, carga la reconstrucción del lugar según el período histórico activo, y superpone sobre la ruina real la imagen del Chiflón operativo: el pique abierto, la estructuras de extracción en su lugar, los mineros trabajando con ropa y herramientas de época.

La fidelidad de la reconstrucción histórica depende directamente del material que aporte el cliente y los archivos del Consejo de Monumentos Nacionales. Fotografías de época, planos arquitectónicos, documentos de la época del carbón, filmes si existen, y testimonios orales registrados son la base sobre la que se construye el contenido. Mientras más material haya disponible, más precisa y más vívida será la reconstrucción que el jugador vea superpuesta sobre la realidad.

La tecnología de reconstrucción combina dos técnicas que los papers recientes de patrimonio cultural validan como complementarias. La fotogrametría con estructura desde movimiento y multivista estéreo produce geometría de alta precisión: mide con exactitud las ruinas existentes y genera la base geométrica fiel. El gaussian splatting tridimensional produce la capa visual de alta fidelidad en tiempo real: con un conjunto de fotografías del lugar, el sistema entrena una distribución de gaussianos optimizable que se rasteriza diferenciablemente en las gafas, entregando calidad fotorrealista a velocidad de render interactivo. La geometría viene de la fotogrametría; la inmersión viene del gaussian splatting. Juntas producen una experiencia donde la ruina real y la reconstrucción virtual se funden sin costuras visibles.

Este encuentro es el corazón patrimonial del concepto. No es un minijuego ni una animación decorativa: es la razón por la que el juego existe como servicio público de patrimonio cultural. El jugador no solo completa una misión en el teléfono; ve con sus propios ojos cómo era el Chiflón cuando producía carbón, cómo vivían los mineros en el Pabellón, cómo funcionaba la caleta cuando las Chinchorreras salían de noche. La RA convierte el patrimonio en experiencia directa, sin depender de que el jugador imagine o lea: lo ve.

### §2.5 Dos niveles de dispositivo y costura de baja latencia

El concepto opera en dos niveles de dispositivo simultáneamente, cada uno con su función específica. El teléfono es el dispositivo universal: lo tiene cualquier visitante, no requiere preparación ni préstamo, y es la interfaz para la caza del NPC, el pasaporte digital, la wallet de minerales y la navegación entre zonas. La pila tecnológica de este nivel es Vue 3 más TypeScript más MapLibre más Turf.js más Pinia, según la decisión de diseño D-007.

Las gafas de realidad aumentada son el dispositivo del encuentro en sitio. No son de propiedad del jugador: el sitio las tiene disponibles para préstamo. Esta decisión reduce la barrera de entrada al máximo: el jugador no necesita comprar hardware ni instalar aplicaciones adicionales; llega al punto de encuentro, pide las gafas, y accede a la reconstrucción histórica. La cobertura inicial de gafas será de unas pocas unidades para la fase dos; a medida que el proyecto crece, el sitio puede ampliar el inventario.

La costura entre ambos niveles es la sincronización de baja latencia. El teléfono consulta al `lota-server` para obtener el estado del juego: posición del jugador, NPCs activos, minerales ganados, progreso de rutas. El `lota-server` corre el orchestrator SOMA y mantiene la fuente de verdad del mundo del juego. Cuando el jugador cambia de nivel de dispositivo, la transición es transparente: las gafas consultan al mismo servidor y cargan la escena RA correspondiente al personaje y la zona donde el jugador se encuentra según la última posición registrada por el teléfono. No hay pérdida de estado, no hay que reiniciar sesión, no hay sincronización manual.

Internamente, la sincronización opera sobre la arquitectura de dos carriles de la lattice. El Carril A de seguridad transmite el estado autoritativo del juego: posiciones de NPCs, eventos activos, decisiones del orchestrator. El Carril B de observabilidad transmite métricas del sistema: carga de jugadores, rendimiento de la lattice, estado de los servidores. Esta separación de carriles garantiza que la información crítica del juego no compite en ancho de banda con los datos de operación, y que ambos flujos pueden monitorearse y depurarse de manera independiente.

El bucle del enjambre SOMA a 2 Hz funciona como el mecanismo de sincronización que reemplaza al cristal físico de un reloj convencional. Cada tick de 500 milisegundos, el orchestrator distribuye órdenes a los NPCs, y cada tick subsiguiente, las gafas reciben la actualización de estado correspondiente. Este bucle es lo suficientemente rápido para que la experiencia se sienta fluida, y lo suficientemente lento para que la red no sea un cuello de botella. El diseño es deliberado: no se buscó la mayor frecuencia posible sino la frecuencia que equilibra responsividad con estabilidad.

### Loop de retorno

El juego mantiene a los turistas volviendo a través de tres mecanismos concretos que operan después de que el visitante ya se fue de Lota. El pasaporte incompleto funciona como anzuelo visible: el jugador sabe exactamente qué le falta para cerrar una ruta, y ese porcentaje incompleto es razón suficiente para planificar otra visita. El calendario del cielo, publicado con un año de anticipación, muestra las fechas exactas de los próximos eventos celestes, de modo que el visitante puede planificar su regreso alrededor de una luna llena o un solsticio. Los cupones del comercio local operan con caducidad corta de treinta a sesenta días, de modo que el cobre acumulado en la visita anterior tiene una fecha de vencimiento que obliga al retorno si el jugador quiere usarlo antes de que se pierda. Los tres mecanismos operan en escalas distintas pero convergen en el mismo resultado: el turista tiene siempre una razón concreta para volver a Lota, y cada regreso renueva el flujo hacia el comercio local que sostiene la plataforma.

---



## §3 Universo narrativo

El universo de Lota Indómito no es un escenario decorativo. Es un territorio vivo donde los personajes del pasado carbonero de la comuna caminan entre las mismas calles que el turista recorre hoy, donde cada ruta recupera un oficio o una zona que la memoria colectiva todavía conserva, y donde los minerales que el jugador acumula en su cartera tienen identidad propia, fuente propia y uso propio. Este sección describe los tres subsistemas que constituyen el universo narrativo: las cuatro figuras históricas, las ocho rutas temáticas patrimoniales, y las tres monedas minerales. Los tres se entrelazan sin arbitrariedad: los personajes habitan las rutas, las rutas son el territorio geográfico de esos personajes, y los minerales son el medio de intercambio que ata la experiencia lúdica al comercio real de la comuna.

### §3.1 Las cuatro figuras históricas del carbón

El enjambre de NPCs del juego se compose de cuatro figuras históricas vinculadas al patrimonio carbonero de Lota. Cada una tiene zona propia, condición celestial de activación propia, rol mecánico propio y un gancho narrativo que rescata una anécdota o un perfil real de la historia de la comuna. El diseño FSM de cuatro modos les da comportamiento reproducible y auditable, pero la identidad de cada una es irreductiblemente histórica.

**Isidora Goyenechea**

Nombre e identificación: Isidora Goyenechea, miembro de la familia que financió la construcción del Pabellón 83 y una de las figuras femeninas más influyentes del comercio y la filantropía lotrina del período carbonero.

Zona: Parque de Lota. Su zona natural es el área verde que rodea el Pabellón, donde los oficios del cuidado y la sociabilidad pública encontraron su espacio durante la época dorada de la mina.

Activación: Atardecer. El personaje se activa cuando el sol se aproxima al horizonte occidental. Esta condición alinea la experiencia con el turno de la tarde de los mineros, cuando la jornada de trabajo terminaba y la vida social del barrio se concentraba en el Parque.

Rol mecánico: Guía a los jugadores por el Parque de Lota y les cuenta la historia de la familia que financió la construcción del Pabellón. Las misiones que entrega recompensan cobre. El encuentro con Isidora en el Parque es uno de los puntos de entrada del pasaporte digital.

Gancho narrativo: Isidora Goyenechea representa la tradición de las familias que financiaron la infraestructura social de la comuna cuando la mina generaba riqueza. Su presencia en el Parque no es alegórica: es la memoria de una mujer que invirtió en el espacio público de su comunidad en una época donde eso era excepcional.

**El Ciego de la Mina**

Nombre e identificación: El Ciego de la Mina, figura legendaria del mineur veterano que recorría los piques y conocía cada veta, cada grieta y cada accidente del subterranean de Lota.

Zona: Los Piques y el Chiflón del Diablo. Su territorio es el corazón subterráneo de la mina, los espacios que la geología y la extracción humana sculptaron bajo la comuna durante más de un siglo.

Activación: Amanecer. El personaje aparece cuando el reloj marca las siete de la mañana, exactamente a la hora en que empezaba el turno de la mañana. Esta condición reproduce la rutina real del trabajador de la mina.

Rol mecánico: Aparece en los Piques al amanecer. Las misiones que entrega recompensan cobre y, cuando coincide con un evento celestial activo, también oro. Su encuentro en el Chiflón es uno de los momentos de mayor carga patrimonial del juego.

Gancho narrativo: El Ciego de la Mina encarna la sabiduría del trabajador que conoce su lugar de trabajo como la palma de su mano. Su ceguera es tanto metáfora de la oscuridad del pique como símbolo de los sentidos restantes agudizados por la oscuridad: el sonido del agua, el olor del carbón, la memoria del espacio.

**La Chinchorrera Mayor**

Nombre e identificación: La Chinchorrera Mayor, figura representativa de las mujeres del borde costero de Lota que practicaban la extracción de mariscos en las rocas y transmitían oralmente los oficios del mar de generación en generación.

Zona: La Caleta y el borde costero. Su territorio natural es la franja donde la tierra se encuentra con el mar, donde la vida de los trabajadores del mar se desarrollaba fuera del horario de la mina.

Activación: Anochecer. La Chinchorrera Mayor opera durante la ventana de actividad nocturna, aproximadamente noventa minutos a contar del anochecer. Su frecuencia aumenta durante la fase de luna nueva, cuando la oscuridad favorece la extracción nocturna de mariscos.

Rol mecánico: Aparece en la Caleta al anochecer. Las misiones que entrega recompensan cobre. Su encuentro es el más esquivo del juego, diseñado para que el jugador que llega tarde a la Caleta vuelva con el gancho narrativo ya activo.

Gancho narrativo: La Chinchorrera Mayor representa la tradición oral de las mujeres del borde costero, que transmitían los oficios del mar de generación en generación sin más registro que la palabra. Su figura corrige el sesgo masculino habitual en la narrativa minera y recupera una historia que el patrimonio escrito omitió sistemáticamente.

**El Palanquero**

Nombre e identificación: El Palanquero, el capataz del muelle y la zona portuaria de Lota que organizaba la carga y descarga de los minerales y los insumos de la minería durante la época del carbón.

Zona: El borde costero, con énfasis en la zona del muelle. Su territorio es el punto donde el carbón sale de la mina hacia el mundo y los insumos llegan a la comuna.

Activación: Luna llena. El personaje se vuelve visible durante la fase de luna llena, y su aparición coincide con las mareas altas que facilitaban las operaciones de carga y descarga en el puerto natural de Lota.

Rol mecánico: Visible principalmente durante luna llena. Las misiones que entrega recompensan cobre y oro. Su aparición en el borde costero es uno de los eventos que incentivan al jugador a consultar el calendario del cielo y planificar su próxima visita.

Gancho narrativo: El Palanquero representa la logística que hacía funcionar la industria del carbón. Sin él, el mineral no llegaba a los barcos; sin los barcos, la mina no tenía mercado. Su papel era anónimo pero indispensable, y su figura recupera la memoria del trabajo invisible que sostenía la economía de toda la comuna.

### §3.2 Las ocho rutas temáticas patrimoniales

Las ocho rutas temáticas de la comuna constituyen el tejido geográfico del universo de Lota Indómito. Cada ruta tiene zona propia, minijuego propio, recompensa propia y conexión propia con el comercio local. Las ocho rutas están diseñadas para que un visitante haga entre seis y diez micro-sesiones durante una visita de dos a cuatro horas, con una acción por micro-sesión que nunca supera los tres minutos de gameplay táctil.

**Ruta Fuego y Carbón**

Tema: El oficio del pan de mina y la vida doméstica de los mineros. Esta ruta atraviesa el sector de los hornos de barro y las panaderías históricas del centro de Lota.

Zonas geográficas: Centro de Lota y entorno de los hornos de barro tradicionales. Los POIs incluyen las panaderías históricas donde se fabricaba el pan que los mineros llevaban al pique.

Minijuego: Amasando Pan. Minijuego táctil de ritmo donde el jugador debe sobar, amasar y hornear el pan de mina en un horno de barro simulado. Duración estimada: noventa segundos.

Recompensas: Cobre por cada pan completado. Insignia especial "Amasadora de Memorias" para quienes logran puntaje máximo en la ruta.

Conexión con el comercio local: Panaderías del centro de Lota participan como destino de World Events y como puntos de entrega de cupones para el jugador que completó la ruta.

**Ruta Geositio**

Tema: La geología del carbón y la historia de la tierra que los mineros perforaron durante más de un siglo. Esta ruta comienza en el Geositio del Chiflón del Diablo.

Zonas geográficas: Chiflón del Diablo, pique abandonado que sirve como entrada al subsystemo geológico y como punto de partida de la comprensión estratigráfica de la cuenca carbonera.

Minijuego: El Geólogo del Tiempo. Puzle estratigráfico donde el jugador debe clasificar capas de carbón, fósiles y rocas según las eras geológicas correspondientes. Duración estimada: ciento veinte segundos.

Recompensas: Cobre por cada puzle completado. Insignia "Geólogo del Tiempo" al cerrar la ruta.

Conexión con el comercio local: Talleres de artesanía en piedra carbón y museos locales asociados a la ruta.

**Ruta de las Bodegas**

Tema: El inventario de las herramientas y los insumos de la minería. Las bodegas de las antiguas compañías carboneras almaceban todo lo que la mina necesitaba para funcionar.

Zonas geográficas: Antiguas instalaciones de las compañías carboneras, ruinas industriales de las bodegas donde se guardaban herramientas, explosivos y repuestos.

Minijuego: El Inventario del Carbón. Búsqueda de objetos tridimensionales ocultos entre las herramientas y los restos industriales. Duración estimada: noventa segundos.

Recompensas: Cobre por cada objeto encontrado. Insignia "Inventariador" al completar la búsqueda en cada bodega.

Conexión con el comercio local: Ferreterías y talleres mecánicos históricos de Lota asociados como destino para el jugador que completa la ruta.

**Ruta del Comercio**

Tema: El trueque y el comercio como alma de la economía lotrina. Esta ruta atraviesa los locales asociados del centro de Lota.

Zonas geográficas: Centro de Lota y entorno de los locales comerciales asociados. Los POIs incluyen restaurants, cafés y completas que participan como asociados del juego.

Minijuego: El Trueque Lota. Minijuego de gestión donde el jugador pratica el trueque de minerales con los puestos del comercio local. Duración estimada: sesenta segundos.

Recompensas: Cobre y oro por cada trueque completado. La ruta rewarding oro es deliberada: el trueque recompensa la interacción con el comercio, que es el acto central del modelo económico del juego.

Conexión con el comercio local: La ruta está diseñada directamente sobre los locales asociados. Cada POI de la ruta es un comercio real que acepta minerales del juego.

**Camina Lota**

Tema: La arquitectura de los pabellones y la memoria urbana de la comuna. Esta ruta empieza en el Pabellón 83 y la zona histórica que rodea el parque.

Zonas geográficas: Pabellón 83, zona histórica del parque y entorno de los pabellones que fueron vivienda obrera durante la época de la mina.

Minijuego: Arquitecto de Pabellones. El jugador superpone fotografías históricas sobre el paisaje actual y debe encuadrar exactamente el ángulo para reconstruir digitalmente el pabellón en tres dimensiones. Duración estimada: noventa segundos.

Recompensas: Cobre por cada pabellón reconstruido. Insignia "Arquitecto de Pabellones" al cerrar la ruta.

Conexión con el comercio local: Librerías históricas, imprentas y talleres de enmarcación asociados como puntos de entrega de diplomas y diplomas digitales.

**Ruta Costera**

Tema: El borde costero y la observación de la fauna marina. Esta ruta sigue la franja costera desde la Caleta hacia el sur.

Zonas geográficas: Borde costero de Lota, desde la Caleta hasta los miradores del golfo. Los POIs incluyen los puntos de observación con vista al mar.

Minijuego: Vigía del Golfo. Desafío de avistamiento con prismáticos virtuales donde el jugador debe identificar la fauna marina del golfo de Arauco. Duración estimada: sesenta segundos.

Recompensas: Cobre por cada especie identificada correctamente. Insignia "Vigía del Golfo" al completar la ruta completa.

Conexión con el comercio local: Restaurants de frutos del mar y caletas de pescadores asociados como destino para el jugador que completó la ruta.

**Ruta Indómita**

Tema: La flora nativa del Parque de Lota y la botánica del bosque valdiviano que sobrevive en el corazón de la comuna. Esta ruta atraviesa el Parque de Lota.

Zonas geográficas: Parque de Lota, que conserva fragmentos del bosque valdiviano original y es uno de los pulmones verdes de la provincia de Arauco.

Minijuego: Rastreador de la Flora. Trivia botánica interactiva donde el jugador debe identificar la flora nativa a partir de pistas visuales y textuales. Duración estimada: sesenta segundos.

Recompensas: Cobre por cada planta correctamente identificada. Insignia "Rastreador de la Flora" al cerrar la ruta.

Conexión con el comercio local: Viveros y jardines botánicos locales asociados como destino de cupones para el jugador que completó la ruta.

**Oficios de Mar**

Tema: La pesca artesanal y el oficio de las Chinchorreras. Esta ruta comienza en la Caleta de Lota.

Zonas geográficas: Caleta de Lota y zona de los talleres de artesanía de la madera donde se construían las redes y las balsas artesanales.

Minijuego: Chinchorreando en el Blanco. Minijuego de física donde el jugador debe ajustar la fuerza y la dirección del lanzamiento de la red de pesca artesanal. Duración estimada: noventa segundos.

Recompensas: Cobre por cada lanzamiento exitoso. Insignia "Chinchorrero" al cerrar la ruta.

Conexión con el comercio local: Caletas de pescadores y talleres de artesanía de la madera asociados como destino para el jugador que completó la ruta.

### §3.3 Las tres monedas minerales

El sistema económico del juego opera con tres minerales que funcionan como monedas con tipo de cambio relativo, transferibles entre usuarios y comercianteables en el comercio local de Lota. El diseño del sistema multi-moneda (D-016) convierte al juego en un ecosistema económico donde cada mineral tiene identidad propia, fuente de obtención propia y uso propio. Los ratios vigentes en el piloto son fijos: un oro equivale a cien cobre, y un estaño equivale a diez mil cobre o cien oro.

**Cobre (Cu)**

Símbolo: Cu. Ratio: una unidad, base del sistema. Rareza: común.

Identidad narrativa: El metal del trueque honrado. Forjado en el calor del comercio de Lota. El cobre es el mineral cotidiano del juego, diseñado para que el jugador lo gane, lo gaste y lo vuelva a ganar en un ciclo corto que mantiene el flujo económico del comercio local activo.

Cómo se gana: Micro-sesiones de POI fijo completadas, reportes ciudadanos validados, y todas las misiones regulares de las ocho rutas. Es el mineral que recompensa las acciones ordinarias del jugador sin requerir condiciones especiales.

Cómo se usa: Transacciones cotidianas en los locales asociados del comercio de Lota, transferencias P2P entre jugadores, y personalización in-game de marcadores y marcos del pasaporte. El cobre es la moneda del comercio diario.

Por qué cobre: El cobre es el metal del trabajo y del comercio diario. Usar cobre como moneda base del juego conecta la identidad lúdica con la identidad minera metálica de Chile, que es histórica y reconocible sin necesidad de inventar cifras de producción.

**Oro (Au)**

Símbolo: Au. Ratio: cien cobre. Rareza: media.

Identidad narrativa: El metal del cielo. Aparece cuando la luna, el sol y la historia convergen. El oro es el mineral de los eventos celestiales, diseñado para que el jugador que consulta el calendario del cielo tenga una razón concreta para volver a Lota cuando hay un evento activo.

Cómo se gana: Eventos del cielo, World Events temáticos y rutas completas de World Events. La fuente del oro es siempre un evento, no una acción repetible. Esto incentiva al jugador a planificar su visita alrededor del calendario celestial publicado con un año de anticipación.

Cómo se usa: Recompensas de mayor valor en el comercio local, subastas digitales de productos premium del comercio, y personalización de alto nivel en el juego. El oro es la moneda de los momentos especiales.

Por qué oro: El oro como metal del cielo tiene tradición en todas las culturas. En Lota Indómito, esta asociación es literal: el oro solo aparece cuando el cielo sobre la comuna produce un evento que coincide con la historia o la tradición de la zona. Es la moneda de la convergencia entre el cielo y la tierra.

**Estaño (Sn)**

Símbolo: Sn. Ratio: diez mil cobre, cien oro. Rareza: rara.

Identidad narrativa: El metal de la convergencia. Solo aparece cuando los dos carriles del mundo se tocan. El estaño es el mineral de los portales S60, diseñado para que sea el mineral más escaso del juego y el que genera mayor deseo en los jugadores.

Cómo se gana: Portales S60, que se abren cuando la convergencia de la lattice de Sentinel alcanza la condición matemática que activa el portal. También se obtiene al completar el pasaporte digital al cien por ciento y al alcanzar el rango máximo de Leyenda Indómita. La fuente del estaño es siempre un logro excepcional, no una acción cotidiana.

Cómo se usa: Subastas digitales de productos únicos del comercio local, títulos especiales de avatar, diplomas de honor descargables en PDF, y cualquier transacción de alto valor dentro del ecosistema del juego. El estaño es la moneda del juego completo.

Por qué estaño: El estaño es el mineral de la convergencia porque su obtención depende de la convergencia matemática de la lattice S60 de Sentinel. Es el mineral que solo aparece cuando los dos carriles del sistema se tocan en un punto exacto del espacio-tiempo, y esa condición es matemáticamente única y no reproducible. El diseño ata la rareza del estaño al diferenciador central del juego.

### Cierre del universo narrativo

Los tres subsistemas del universo narrativo no operan en paralelo sino en articulación. Los personajes habitan las rutas: Isidora camina por el Parque, El Ciego emerge del Pique al amanecer, La Chinchorrera aparece en la Caleta al anochecer, El Palanquero organiza la carga en el muelle durante luna llena. Las rutas son el territorio geográfico de esos personajes: cada zona de Lota tiene su figura, su minijuego y su recompensa. Los minerales son el medio de intercambio que ata la experiencia lúdica al comercio real: el cobre recompensa las acciones ordinarias y mantiene el flujo del comercio local activo, el oro recompensa los eventos del cielo y obliga al jugador a volver cuando hay una fecha importante en el calendario, el estaño recompensa la convergencia matemática y genera la escasez extrema que hace que el juego completo valga la pena.

El universo narrativo no es un adorno sobre el juego. Es el sustrato sobre el que opera todo el modelo económico de Lota Indómito. Sin personajes con identidad y zona, no hay razón para caminar hacia un POI específico. Sin rutas que conecten POIs con minijuegos y recompensas, no hay loop de visita ni loop de retorno. Sin minerales con identidad propia, fuente propia y uso propio, no hay economía interna ni comercio local que cobrar comisión. Los tres subsistemas juntos son lo que convierte a Lota Indómito en una plataforma de reactivación comercial, no en una aplicación turística.

---

<!-- §4 Sistema económico → Bloque B tarea 5 -->

## §4 Sistema económico

El modelo económico de Lota Indómito se diseña desde una pregunta concreta: si el juego genera valor para el comercio local de Lota, ¿cómo captura ese valor la plataforma para cubrir sus costos operativos? La respuesta no es un modelo de suscripción ni un pay-to-win. Es una comisión sobre cada transacción real que el juego genera en el comercio local.

### §4.1 La transacción como unidad económica

El cobre y el oro no son tokens comprables con dinero real. Son medios de intercambio internos que nacen del juego y mueren en el comercio local. Un turista no paga para obtener minerales; los gana jugando. Los gasta en cupones QR que canjea en tiendas y restaurantes reales. El comercio local acepta los cupones, los reconcilia con el servidor, y el servidor descuenta una comisión de entre 5% y 10% según el tipo de transacción (según el rango documentado en `_analisis/21 §4.4` y `_analisis/23 §2`). La comisión es el revenue de la plataforma.

Esta es la diferencia central con cualquier aplicación turística o gamificación genérica. El cupón QR no es un badge digital. Es un título de deuda del comercio local contra el turista, canjeable por un producto real. Sin ese nivel de concreción, el comercio no tiene incentivo real para participar y el modelo no se cierra.

El diseño de la comisión sigue la lógica de Mercado Pago o Transbank: el comercio local acepta el cupón como forma de pago porque sabe que el servidor lo va a honrar. El servidor honra el cupón porque cobra la comisión antes de liberar los fondos. El turista recibe un descuento real o un producto real. Los tres ganan.

La cadena completa: el juego otorga minerales al turista como recompensa por acción lúdica → el turista gasta minerales en un cupón QR en el comercio local → el comercio acepta el cupón → el servidor reconcilia la transacción → el servidor descuenta la comisión → el comercio recibe el saldo. El cobre y el oro circulan como moneda interna del ecosistema, anclados a transacciones reales en comercio real.

### §4.1.1 Escenario micro-sesión detallada

El siguiente recorrido describe una micro-sesión completa desde la perspectiva del turista:

Un turista ingresa al Parque de Lota. El geofencing de la zona activa una vibración en su teléfono. Aparece el avatar de Isidora Goyenechea en la PWA con su línea de diálogo: "¡Cuánto tiempo, Explorador! El Pabellón espera tu visita. ¿Aceptas la misión?". El jugador acepta. Comienza un minijuego de 90 segundos, un QTE donde debe amasar masa de pan en el ritmo correcto. Si tiene éxito, obtiene 30 cobre y 1 XP.

Los cinco tramos de la micro-sesión se distribuyen así: Trigger (15 segundos) + Contexto (45 segundos) + Acción (90 segundos) + Recompensa (60 segundos) + Próximo (30 segundos) = 240 segundos, es decir, 4 minutos en total. Al finalizar el primer día de juego, un jugador típico ha acumulado 200 cobre a través de 3 a 4 micro-sesiones. Gasta 50 cobre en la panadería del sector: el cupón QR aparece en su teléfono, lo escanea en el POS de la panadería, y el cupón se canjea por medio kilo de pan de mina.

El flujo del cobre en esta transacción es: juego → wallet del jugador → cupón QR → aceptación del comercio local → reconciliación con el servidor → comisión futura. Esta es la unidad atómica del modelo económico. Sin esta unidad no hay reconciliación, sin reconciliación no hay comisión, sin comisión no hay plataforma.

### §4.2 World Events como motor de oleadas comerciales

Los World Events son la palanca que convierte la economía del cobre en un flujo comercial significativo. Un evento del cielo afecta la atmósfera del juego; un World Event sincroniza el juego entero con una fecha real y coordina oleadas de turistas hacia el comercio local durante fechas de alto impacto comercial.

El diseño de los World Events se documenta en detalle en `_analisis/21`. Aquí interesa la mecánica económica. Cada World Event tiene tres componentes que generan transacción comercial directa:

La primera es la misión temática que requiere la visita física a un comercio local. La misión "El Sabor del Carbón" de Fiestas Patrias obliga al jugador a visitar tres panaderías o restaurantes del sector y escanear un QR en cada uno. Cada escaneo es una transacción potencial. La segunda es la insignia exclusiva, que no se puede obtener fuera del evento (estilo WoW). La insignia genera FOMO legítimo y obliga al jugador a volver durante la ventana del evento. La tercera es el cupón real canjeable en comercio asociado, con un descuento de entre 10% y 15% según el tipo de comercio, como se documenta en `_analisis/21 §4.4`.

El cupón tiene caducidad. La recomendación de diseño es de 30 a 60 días tras la obtención, lo que balancea la urgencia del cupón con la realidad del turista de paso. Para la insignia exclusiva la urgencia es máxima: si no se obtiene durante la ventana del evento, no vuelve. Eso es lo que genera el pico de tráfico comercial en las fechas clave.

El calendario de World Events se opera con una lógica de planificación comercial. Las fechas nacionales (Fiestas Patrias, San Juan, Día del Patrimonio) son fijas y se programan con anticipación. Las fechas locales y comerciales se curan en coordinación con el Municipio y los comerciantes. El resultado es un calendario de entre 4 y 6 World Events por año, cada uno con entre 4 y 5 comercios asociados, según los parámetros documentados en `_analisis/21 §3`.

### §4.2.1 Flujo detallado de Fiestas Patrias

Dos semanas antes del evento, el calendario del cielo publica el World Event en la PWA del jugador: "Fiestas Patrias 2026: del 17 al 19 de septiembre. Doña Carmen la Empanadera aparecerá en el Parque". El 17 de septiembre, el orquestador SMOMA activa el NPC exclusivo Doña Carmen. Camina un radio de 200 metros alrededor del Parque de Lota.

El jugador debe encontrarla. Para hacerlo, camina hacia la posición actual del NPC en el mapa. Si la distancia se cierra a menos de 20 metros, se dispara el encuentro y la misión asociada: "El Sabor del Carbón". La misión requiere visitar tres panaderías locales, escanear el QR en cada una y confirmar la visita. Al completar la misión, el jugador obtiene la insignia "Catador Patrio" (exclusiva, no obtenible después del evento), cobre y oro, más un cupón QR canjeable en Restaurant X con un descuento de entre 10% y 15% (dentro del rango documentado en `_analisis/21 §4.4`). El cupón caduca en 72 horas.

Contrastado con el flujo de San Juan: ventana de evento más corta (24 a 48 horas), NPC diferente (El Ciego de la Mina en el Chiflón), misión diferente (llevar una foto del fuego al comercio asociado). Los World Events operan como oleadas de turistas en fechas que maximizan el peak revenue del comercio local. La coordinación de fechas no es accidental: es el núcleo del modelo D-014.

### §4.3 Subastas y comercio de alto valor

El estaño es la moneda del juego completo. Su obtención depende de la convergencia matemática de la lattice S60 de Sentinel, lo que lo convierte en el mineral más escaso del ecosistema. Esa escasez lo habilita como medio para transacciones de alto valor: subastas digitales de productos únicos del comercio local, títulos especiales de avatar, diplomas de honor descargables en PDF.

El diseño de las subastas se implementa en dos etapas. La Etapa 0 (piloto) usa venta directa con precio fijo: el comprador paga inmediatamente, sin puja ni escrow. La Etapa 1 introduce el flujo completo de puja + escrow + reputación.

### §4.3.1 Escenario completo de una subasta (Etapa 1)

El escenario describe un ejemplo completo de una subasta en Etapa 1:

Un restaurant local lista "Cena para dos con mariscos frescos" con un precio inicial de 500 cobre. Paso 1 (Vendedor lista): el dueño del restaurant carga descripción, fotos, precio inicial (500 cobre) y duración (3 días). Paso 2 (Puja abierta): los usuarios pujan en incrementos de 50 cobre. Tras 2 días, la puja más alta es de 1.200 cobre. Paso 3 (Cierre): gana el mejor postor. Paso 4 (Pago + escrow): los 1.200 cobre del ganador se mueven a escrow en la wallet del servidor (escrowed_amounts). Paso 5 (Entrega + confirmación): comprador y vendedor coordinan el retiro en el restaurant. El comprador abre la app y confirma la recepción. Paso 6 (Liberación): los 1.200 cobre se mueven desde escrow a la wallet del vendedor menos la comisión de 5% (60 cobre para productos según `_analisis/23 §2`) = 1.140 cobre. Paso 7 (Reputación): ambos dejan una calificación de 5 estrellas. La plataforma ganó 60 cobre en comisión por esta transacción.

En la Etapa 0, la versión es venta directa con precio fijo (el comprador paga 1.200 cobre al vendedor inmediatamente, sin puja ni escrow). El sistema completo de puja + escrow + reputación llega en Etapa 1.

### §4.4 Dashboards y métricas para tres actores

El servicio de ML produce dashboards mensuales para tres actores: Municipio, comercio local e INTERLOCUTOR. El diseño del servicio se documenta en `_analisis/22`. Aquí interesa qué se mide y por qué importa para la sostenibilidad del modelo.

El Municipio recibe heatmaps de visitación por zona × hora para los últimos 30 días. La información le permite entender dónde se concentran los turistas y cuándo, lo que justifica inversión en infraestructura y promoción. El comercio local recibe el ROI por World Event: cupones emitidos versus cupones canjeados, ticket promedio por comercio y tipo de cupón. INTERLOCUTOR recibe métricas de retención para la cohorte de turistas que participó en cada evento: D+1, D+7, D+30. Las métricas se derivan de los 16 eventos anónimos definidos en `_analisis/22 §5`. El servicio de ML no recolecta información de identificación personal; todo es seudónimo.

### §4.4.1 Tres dashboards concretos (escenarios ilustrativos)

Los tres dashboards se producen mensualmente. Los números que siguen son escenarios ilustrativos, no mediciones reales, hasta que el piloto genere datos suficientes.

(a) **Dashboard del Municipio**: heatmaps de visitación por zona × hora para los últimos 30 días. El heatmap revela que el Chiflón del Diablo concentra visitas en horario de tarde (15:00 a 18:00), mientras que el Parque de Lota tiene un patrón bimodal (familias en la mañana, visitantes en la tarde). El Municipio usa esta información para decidir dónde instalar bancas, mejorar iluminación o coordinar horas de atención de comercio asociado.

(b) **Dashboard del comercio**: ROI por World Event. Escenario ilustrativo para Fiestas Patrias: 320 cupones emitidos a través de 8 comercios, 287 cupones canjeados (la tasa de canje varía según el comercio y la fecha del evento), ticket promedio que varía según el tipo de comercio. El comercio usa esta información para decidir si le conviene participar en el siguiente evento y qué tipo de cupón ofrece.

(c) **Dashboard de INTERLOCUTOR**: métricas de retención para la cohorte de turistas que visitó durante Fiestas Patrias 2026. Dentro del rango de entre 30% y 50% documentado en `_analisis/22 §3.3` para retención D+1 en sistemas de gamificación con recompensas reales, se proyecta una retención D+1 de entre X% y Y%, retención D+7 de entre X% y Z%, y retención D+30 de entre X% y W%. Las métricas exactas dependen del volumen de datos que genere el piloto.

### §4.5 El circuito económico completo

El modelo se cierra cuando se mira el circuito completo. El juego otorga minerales (cobre y oro) como recompensa por acción lúdica. El turista gasta esos minerales en cupones QR que canjea en comercio local. El comercio local acepta los cupones y registra la transacción. El servidor reconcilia la transacción y descuenta la comisión de entre 5% y 10% por transacción. El revenue de comisión financia la próxima iteración del juego. El juego vuelve a otorgar minerales. El circuito se cierra.

```
[Motor del juego]
     ↓ otorga minerales (cobre/oro)
[Wallet del turista]
     ↓ gasta en cupón QR
[Comercio local]
     ↓ acepta cupón, registra transacción
[Reconciliación con servidor]
     ↓ comisión 5-10% por transacción
[Revenue de comisión de la plataforma]
     ↓ financia siguiente iteración del juego
[Motor del juego]
```

La sostenibilidad económica del modelo depende de tres variables: volumen de transacciones, ticket promedio por transacción y tasa de comisión. Un evento de 3 días con 100 turistas activos genera entre 200 y 500 cupones canjeados, con un rango que depende del tipo de evento y del diseño de caducidad del cupón (30-60 días tras obtención según `_analisis/21 §4.4`). El ticket promedio por cupón oscila entre $X.XXX y $Y.YYY CLP según el tipo de comercio. El revenue de comisión por evento oscila entre 5% y 10% del volumen total del ticket.

Con 4 a 6 World Events por año (según el calendario documentado en `_analisis/21 §3`) y entre 4 y 5 comercios participando cada uno, la plataforma puede sostener un presupuesto operativo significativo a partir de la comisión sola. Ese es el criterio que justifica la inversión pública en el proyecto.

---

## §5 Diferenciador técnico y soberano

### §5.1 Soberanía matemática: Sentinel S60 sin floats

La diferenciación central de Lota Indómito nace en la capa matemática. El stack Sentinel S60 opera con **aritmética en base-60 y cero operaciones en coma flotante en CPU**. El crate `me-60os-core/src/lib.rs` tiene lints `forbid(clippy::float_arithmetic)`, `forbid(clippy::float_cmp)`, `forbid(clippy::cast_possible_truncation)` y `forbid(clippy::cast_precision_loss)`. Esto no es preferencia académica. Es una decisión operativa que se valida en compile-time: cualquier código que introduzca un `f32` o `f64` falla la compilación antes de llegar a runtime.

**Determinismo.** La misma entrada produce la misma salida, siempre. Esto importa en un mundo compartido donde el estado de física, celestial y lattice corre en servidor y se sincroniza con el cliente. Con aritmética flotante, dos máquinas con el mismo input pueden divergir por errores de redondeo acumulados. Con S60, cliente y servidor producen el mismo resultado bit a bit. El documento `_analisis/15_inventario_sentinel_disponible_para_motor.md` §3 lo describe como la promesa de isomorfismo con la física real: el motor es isomorfo a la realidad que modela.

**Cero deriva de fase.** En un sistema con pentaresonancia, doble carril y corrección cada 68 ticks, la deriva acumulada de la aritmética flotante corrompería el estado del juego después de horas de operación continua. El módulo `qhc.rs` de Sentinel implementa el patrón QHC `10;5,6,5` con corrección cada 68 ticks y un intervalo de corrección de 0.7 milisegundos. Ese intervalo no sirve si el cómputo que lo rodea tiene errores de redondeo silenciosos. S60 elimina esa clase de error desde la base.

**Validación empírica.** El vault de Jaime documenta en `PersonalVault/INDICE_MAESTRO_EXPERIMENTOS_RUST.md` el experimento EXP-015, validado en `sentinel_bench.rs`. El benchmark Rust contra Python muestra 23.6 veces menos memoria por nodo y 3000 veces más rendimiento de procesamiento: 120 millones de nodos por segundo en Rust versus 0.04 millones en Python. Eso no es un microbenchmark sintético; es el throughput real del lattice sobre el que corre el juego.

**El ejemplo Kepler.** El módulo `celestial.rs` resuelve mecánica orbital newtoniana en S60 puro. Las fórmulas de Kepler (ε = v²/2 − μ/r, a = −μ/(2ε), e = √(1 + 2εh²/μ²), T = 2π√(a³/μ)) operan sin redondeo flotante. El juego que sincroniza su estado con eventos celestes reales no puede permitirse que la posición calculada de la Luna o de las Estrellas Reales diverja del cielo real después de una semana de operación. Eso es lo que la decisión D-010 protege.

### §5.2 Soberanía de infraestructura: sin Google, sin plataformas externas

Lota Indómito no usa Google Maps Platform, Google Analytics, Firebase ni ningún servicio de una corporación extranjera. No es una limitación. Es una ventaja operativa y un rasgo de diseño deliberado.

**Costo.** OpenStreetMap con Nominatim autoalojado, OSRM para cálculo de rutas y tileserver-gl para los cuadrantes del mapa cuesta entre 15 y 25 dólares mensuales por un VPS en proveedores como Hetzner o DigitalOcean. Google Maps Platform parte en 100 a 275 dólares mensuales en su plan inicial, según el volumen de solicitudes. La diferencia de 75 a 250 dólares por mes queda en la plataforma como margen de comisión para el comercio. El documento `_analisis/04_propuesta_tecnica_stack_osm.md` §6 documenta ambos escenarios con las cifras exactas.

**Independencia.** Ningún proveedor externo dicta los términos de uso, cambia los precios unilateralmente ni extrae datos de uso de los usuarios. El Municipio no depende de una corporación para operar su propia herramienta. La MEMORIA del proyecto (MEMORY.md §0) registra esta decisión como compromiso explícito del encuadre vigente D-014.

**OSM es suficiente para Lota.** Los tiles de OpenStreetMap, la geocodificación por Nominatim y el cálculo de rutas por OSRM cubren todo lo que el juego necesita en materia de mapas. La investigación en `_analisis/19_investigacion_tecnologias_y_proyectos_referencia.md` §5 confirma que el ecosistema de mapas abiertos tiene cobertura funcional para aplicaciones de turismo patrimonial a escala comunal. La opción soberana no es un compromiso con tecnología inferior; es una solución completa que cubre el alcance real del proyecto.

**La plataforma no necesita nada de Google.** No usa los servicios de IA de Google, no tiene analytics de terceros, no requiere identidad federada de ninguna corporación. El comercio local opera con cupones QR (sin Webpay, sin MercadoPago). El turista que visita Lota puede jugar con la billetera multi-moneda de minerales sin haber ingresado un número de tarjeta en ningún lado. El motor corre en GPU propia con una NVIDIA GTX 1050 y Vulkan, con proyección de migrar a GPU de servidor cuando el volumen lo justifique. Todo es autohospedado.

**Consecuencia operativa.** Si Google desapareciera mañana, la plataforma sigue funcionando. Si Nominatim requiere mantenimiento, se mantiene. Si OSRM necesita ajuste, se ajusta. No hay un tercero cuya decisión pueda interrumpir el servicio. Eso es soberanía.

### §5.3 Escalabilidad regional: el corredor Arauco como modelo replicable

Lota es la prueba de concepto. El corredor patrimonial de la zona del carbón — Curanilahue, Lebu, Arauco y Concepción — es la zona natural de expansión. El documento de decisiones D-014 (§expansión regional) establece la visión con claridad: el concepto es agnóstico de comuna, cada localidad aporta su contenido sobre el mismo motor, y el modelo de autofinanciamiento se replica de forma independiente en cada una.

**El motor es agnóstico de comuna.** La lattice, la billetera multi-moneda, el sistema de subastas, el enjambre SOMA de NPCs, la sincronización con eventos del cielo y el doble carril de corrección. Todo eso es compartido. Lo que cada comuna aporta es contenido: sus zonas, sus personajes, su historia, su comercio. La estructura de datos no cambia; solo se alimenta con información local. El documento `_analisis/25_todo_continuacion.md` §7 lo resume como modelo de infraestructura pública replicable.

**Concepción es el embudo de volumen.** Es la ciudad más grande del corredor, con alto flujo turístico natural y llegada a los medios de comunicación regionales. Cuando la propuesta quiere visibilidad, Concepción la da. Las comunas patrimoniales — Curanilahue con su mina, Lebu con su costa, Arauco con su historia — son la experiencia. El jugador no hace turismo en Concepción; hace turismo en la zona del carbón y pasa por Concepción como punto de entrada.

**Autofinanciamiento por comuna.** Cada comuna tiene sus comercios que pagan comisión por los cupones y las subastas. La plataforma no extrae valor de una comuna para subsidiar otra. El modelo económico opera en circuito cerrado dentro de cada territorio. La propuesta `_analisis/04_propuesta_tecnica_stack_osm.md` documenta cómo la comisión de 5 a 10 por ciento sobre transacciones reales financia el presupuesto operativo. Ese flujo se repite en cada comuna sin depender de transferscentralizadas.

**Para Fabiola esto significa:** el piloto de Lota es una plantilla. Otras comunas del corredor pueden adoptarlo con un costo incremental bajo. No necesitan construir infraestructura desde cero; heredan el motor, el lattice, la billetera y el sistema de subastas. Solo necesitan trabajo de contenido: levantar sus zonas, vincular sus personajes, convidar a sus comercios. El documento `_analisis/25_todo_continuacion.md` §7 identifica este patrón como la tesis central del proyecto para la propuesta al fondo. Lota Indómito no es un proyecto para una comuna; es una infraestructura pública patrimonial replicable en la zona del carbón.

El diferenciador de Lota Indómito no es la estética visual, que cualquier equipo podría replicar. Es la soberanía de la capa matemática (S60 sin floats, determinismo verificable, 3000 veces más rendimiento que alternativas), la soberanía de la infraestructura (cero dependencias de corporaciones externas, costos operativos que permiten autofinanciamiento real) y la soberanía del modelo regional (motor agnóstico, contenido communal, replicabilidad sin extracción). Estas tres soberanías juntas hacen que el proyecto sea defendible en el tiempo, replicable en el territorio y coherente con el propósito público de reactivar el comercio local a través del turismo patrimonial.

---

## §6 Lo que NO es el proyecto

El proyecto tiene identidad propia. Eso significa que hay cosas que Lota Indómito no es, no fue diseñado para ser, y no será aunque la mesa de trabajo lo pida. Estas no son restricciones defensivas; son compromisos de diseño que protegen lo que el proyecto es.

### §6.1 No es Pokémon GO

Aunque las referencias a Pokémon GO son inevitables para explicar el formato de juego, Lota Indómito no es un producto global de Niantic ni pretende serlo. Es una plataforma patrimonial geo-RPG vinculada a la historia carbonífera de una comuna chilena específica. Los personajes NPC (Isidora, El Ciego, La Chinchorrera, El Palanquero) son figuras históricas reales. Las zonas (Chiflón del Diablo, Parque de Lota, Pabellón 83) son lugares reales. La matemática S60 es real y reproducible. El formato de juego es un vehículo, no un modelo de negocio copiado.

### §6.2 No es una app turística genérica

Una app turística convencional muestra puntos de interés estáticos con descripciones de texto fijo. Lota Indómito es dinámico: el mundo responde al cielo real sobre Lota, el comercio tiene acoplamiento en vivo, y los NPCs se mueven según condiciones reales. No necesita floats ni motores genéricos; necesita Sentinel S60 y determinismo. Eso lo hace más difícil de construir, pero también más fiel al lugar.

### §6.3 No es un SaaS de turismo

Las plataformas SaaS cobran por usuario o por transacción. Lota Indómito cobra al comercio local vía comisión, no al usuario. El usuario nunca paga por la plataforma. Este modelo fue rechazado explícitamente en D-014: el propósito público requiere que la barrera de entrada sea cero para quien visita Lota. Cobrar al usuario transforma el proyecto en producto, y eso no es lo que se está construyendo.

### §6.4 No es una postulación a un fondo específico

Este documento es un concepto de diseño del proyecto, no una postulación. Identificar el fondo adecuado y redactar la propuesta de postulación es dominio de Fabiola (D-004). El documento describe qué es el proyecto en su identidad propia. Múltiples fondos podrían usar este mismo documento como base; la postulación es un vehículo posterior, no el contenido central.

### §6.5 No es un proyecto genérico ni simplificado para encajar en bases

La identidad del proyecto (D-014, S60, corredor Arauco, multi-moneda, World Events) no está en negociación. Este documento debe leerse como Lota Indómito, no como una propuesta cultural genérica que happen to be en Lota. Jaime ha rechazado la simplificación del proyecto para hacerlo más digerible. Las 21 decisiones de diseño abiertas documentadas en `_analisis/25_todo_continuacion.md` §4 existen para la mesa de trabajo con Municipio y CMN; no se resuelven aquí simplificándolas en una sola respuesta.

### §6.6 No es un proyecto aislado

El piloto de Lota es una prueba de concepto para el modelo de corredor Arauco. El documento está estructurado para ser replicable en Curanilahue, Lebu, Arauco y Concepción con un costo incremental bajo. El motor es agnóstico de la comuna: no depende de Lota para funcionar, solo del contenido que cada comuna aporte. Si Lota Indómito solo sirviera para Lota y no pudiera extenderse, habría fallado en su propósito público.

---

Estos seis puntos no son muros. Son las paredes que sostienen el proyecto. Cualquiera que lea esta propuesta y piense que Lota Indómito es "solo" una app turística, "solo" un clon de Pokémon GO, o "solo" un SaaS con rostro patrimonial, está leyendo mal la arquitectura. El diferenciador no es la estética visual, que cualquier equipo podría copiar. Es la soberanía de la capa matemática (S60 sin floats, determinismo verificable), la soberanía de la infraestructura (cero dependencias corporativas), y la soberanía del modelo regional (motor agnóstico, contenido communal, replicabilidad sin extracción). Estas tres soberanías son lo que protege la identidad del proyecto en el tiempo.

---

## §7 Arquitectura general

### §7.1 Diagrama de capas

La arquitectura se organiza en cinco estratos estrictamente jerárquicos. Cada capa solo conoce a la capa inmediatamente inferior; ninguna capa conoce las capas que están dos o más niveles debajo. Esta restricción elimina los circuitos de dependencia y hace que el impacto de cada cambio sea predecible: cuando se modifica el motor S60, las capas superiores no se enteran; cuando se modifica la capa de dominio, las capas inferiores no necesitan ajustarse. El test de esta restricción se puede ejecutar como un análisis de importación del grafo de dependencias del proyecto. La restricción no es solo organizativa; es enforceable mediante el sistema de tipos de Rust y la estructura de crates del proyecto.

Esta jerarquía de cinco capas no es un diagrama aspiracional; es una descripción de las restricciones que el código debe respetar. En el Piloto A, algunas de estas restricciones se relajan para permitir iteración rápida. En el Piloto B, todas las restricciones se implementan completamente. La diferencia entre ambos pilotos no es un cambio de arquitectura; es la implementación completa de una arquitectura que ya está definida. Esto es deliberado: la arquitectura define el contrato, y el Piloto B cumple el contrato que el Piloto A solo esboza. Un revisor que lea el §7 antes de mirar el código puede predecir cómo está estructurado el código en el Piloto B con alta precisión, porque la arquitectura es determinista.

La Capa 1 (Presentación) es la interfaz que el jugador ve. Está construida como una PWA con Vue 3, TypeScript, Vite como bundler, MapLibre para cartografía, Turf.js para geofencing en el cliente, y Pinia para el estado reactivo local. El geofencing se ejecuta completo en el navegador del usuario, sin ida al servidor, lo que reduce la latencia de la experiencia inmersiva y elimina la dependencia de conectividad para la detección de zona. El Pinia store mantiene el estado de sesión del jugador, incluyendo su posición actual, inventario de Carboncillos, insignias obtenidas y ranking communal. Este estado es una proyección local del estado S60 del servidor; la PWA nunca muta el estado del juego directamente, solo envía comandos al servidor. Cuando el jugador se mueve por la ciudad, Turf.js recalcula su posición relativa a las zonas activas en tiempo real en el dispositivo, sin consumir ancho de banda. Cuando la respuesta del servidor llega, Pinia actualiza el estado y Vue re-renderiza los componentes affected, todo de forma reactiva y sin recarga de página.

La Capa 2 (Aplicación) es donde el servidor recibe los comandos del cliente y los transforma en llamadas al dominio. En el Piloto A esta capa se implementa con FastAPI en Python, lo que permite iteración rápida durante la fase de validación del concepto. En el Piloto B esta capa se reescribe en Rust puro, manteniendo la misma superficie de API REST para que la PWA no necesite cambiar entre pilotos. El servidor valida JWT, controla rate limiting, autentica al usuario, y orquestra los comandos hacia la capa de dominio. En ningún punto de esta capa se toma una decisión sobre el estado del juego; esa responsabilidad es exclusiva del motor S60 en la capa inferior. Esto significa que el servidor de aplicación puede hacer escalamiento horizontal sin coordinación, porque no mantiene estado de juego, solo procesa comandos que delega. El escalamiento horizontal de la Capa 2 es importante para la viabilidad del proyecto a largo plazo: cuando Lota Indómito tenga miles de jugadores simultáneos, la Capa 2 podrá correr en múltiples instancias detrás de un balanceador de carga sin necesidad de sincronizar estado entre instancias.

La Capa 2 también maneja la hidratación inicial del estado del cliente. Cuando un jugador abre la aplicación, la Capa 2 reconstruye su estado de sesión desde las proyecciones disponibles en la Capa 5 y lo envía al cliente como un payload de inicialización. Este payload contiene la posición actual del jugador, su balance, sus insignias, y las zonas activas en su radio de cobertura. La hidratación es eficiente porque lee de las proyecciones optimizadas para lectura, no del estado S60 directamente. El estado S60 solo se consulta cuando las proyecciones no son suficientes, por ejemplo cuando un auditor necesita verificar la consistencia del estado completo.

La Capa 3 (Dominio) contiene la lógica de negocio pura. El sistema de wallet multi-moneda (D-016) maneja los balances de Carboncillos, Moneda Local y Moneda Regional sin conocer cómo se persiste ese estado ni cómo se representa en el retículo. El motor de World Events procesa activaciones temporales de zonas y modifica los multiplicadores de spawn; recibe un evento de activación y produce un conjunto de modificaciones de estado que delega al motor S60. El módulo de subastas (D-017) ejecuta la lógica de puja, cierre y asignación sin conocer la implementación del retículo; recibe una puja y produce una transacción de wallet. El módulo de ML analytics infiere patrones de movilidad sin conocer la aritmética subyacente; recibe trayectorias y produce recomendaciones de contenido. Los reportes ciudadanos persisten datos georreferenciados sin conocer cómo se renderiza el mapa. Cada módulo de dominio es independiente de los demás; las dependencias entre módulos de dominio se resuelven mediante inyección de dependencias, no mediante imports directos. Esta separación permite que un nuevo módulo de dominio se agregue sin modificar los módulos existentes, y sin tocar ninguna capa inferior.

La Capa 3 es también donde se implementan las invariantes de dominio que el motor S60 no conoce. Por ejemplo, la invariante de que un jugador no puede hacer check-in en la misma zona más de una vez cada 24 horas se implementa en la Capa 3, porque es una regla de negocio, no una regla del motor. El motor S60 solo sabe que recibió un comando de check-in y que debe actualizar el estado; no sabe que ese comando fue rechazado porque el jugador ya hizo check-in hace 12 horas. Esta separación es importante: el motor S60 es agnóstico del juego, y las reglas específicas del juego viven en la Capa 3. Esto permite que el mismo motor se use para otros juegos que tengan reglas diferentes, con solo cambios en la Capa 3.

La Capa 4 (Motor S60) es donde el estado del juego se muta de forma verificable. Esta capa es la fuente de verdad del sistema. Contiene la aritmética S60 en base 60 sin floats (`spa.rs`), la matriz resonante hexagonal (`resonant_matrix.rs`), la memoria líquida respaldada por SHM (`liquid_memory.rs`), el latido cuántico isoentrópico (`qhc.rs`), el reloj isócrono y el oscilador isócrono, el kernel no-markoviano que procesa eventos, el detector de rift cuántico, y el shader `lattice_interference.wgsl` que ejecuta en GPU via wgpu. Cada componente de esta capa es reemplazable independientemente de los demás, siempre que respete los contratos definidos por los traits de la biblioteca. La Capa 4 es la única que sabe que el juego existe; las capas superiores saben que hay un motor de estado, pero no saben que ese motor es un retículo hexagonal ni que usa aritmética en base 60. Esta ignorancia es deliberada y protege la independencia del motor respecto del dominio.

El kernel no-markoviano es el componente más crítico de la Capa 4. A diferencia de un kernel markoviano que solo considera el estado actual para decidir la siguiente acción, el kernel no-markoviano considera el historial completo de mutaciones para calcular el siguiente estado. Esto es lo que permite que el motor S60 sea verificable: dado un historial de mutaciones, cualquier nodo que ejecute el kernel producirá exactamente el mismo estado, sin importar el orden en que se aplicaron las mutaciones. Esta propiedad de convergencia es lo que hace que el retículo sea un reloj logical distribuido, no solo una estructura de datos. El detector de rift cuántico monitorea el estado del retículo para identificar condiciones que violen las invariantes del sistema, como un desbalance energético que exceda los umbrales permitidos.

La Capa 5 (Infraestructura) contiene las proyecciones del estado S60. PostgreSQL con PostGIS persiste las geometrías de las zonas del juego, los registros de check-in, los reportes ciudadanos y los logs históricos. Redis tiene dos lanes: Lane A (seguridad) persiste cada evento con fsync sin buffer, lo que garantiza que el log forense sobrevivirá una caída de energía del servidor; Lane B (observabilidad) maneja caché de lectura, métricas de throughput, y eventos de tracing en un buffer que puede perder datos sin afectar la integridad del juego. OpenStreetMap, a través de Nominatim para geocodificación y OSRM para enrutamiento, proporciona la cartografía base sin costo de licenciamiento ni dependencias de proveedores externos. La GPU ejecuta el shader wgsl para el renderizado del retículo sin pasar por APIs propietarias. Cada componente de esta capa es una proyección de una parte del estado del motor; ninguno de ellos tiene la imagen completa del estado del juego.

La elección de PostgreSQL sobre otras bases de datos tiene razones específicas. PostGIS proporciona extensiones geográficas que ninguna otra base de datos de código abierto ofrece con la misma madurez. La combinación de PostgreSQL con PostGIS permite consultas geoespaciales eficientes, como encontrar todas las zonas dentro de un radio de 500 metros de la posición del jugador, con índices espaciales que reducen el espacio de búsqueda. El historial de versiones de PostgreSQL permite hacer consultas puntuales en el tiempo, lo que es útil para reconstruir el estado del sistema en un momento dado. La elección de Redis para caché tiene razones similares: es la base de datos en memoria más madura para el patrón de clave-valor, con soporte para estructuras de datos complejas como hashes, sorted sets, y streams que son útiles para las métricas del juego. La elección de OSM tiene razones de costo y soberanía: ningún proveedor de mapas comercial puede ofrecer la combinación de cero costo, cero dependencias corporativas, y control total sobre los datos que OSM proporciona.

La arquitectura de cinco capas también facilita la verificación formal del sistema. Cada capa tiene un contrato formal que define qué inputs acepta y qué outputs produce. El contrato de la Capa 4 es el más estricto: acepta solo comandos que respeten las invariantes del retículo y produce solo mutaciones que sean consistentes con el estado anterior. Este contrato formal se puede verificar mediante pruebas de propiedad (property-based testing) que generan comandos aleatorios y verifican que el motor siempre produce un estado consistente. La verificación formal del motor S60 es parte del plan de desarrollo del Piloto B: una vez que el motor esté implementado, se ejecutarán pruebas de propiedad para verificar que todas las invariantes se mantienen para todos los comandos posibles.

El diagrama de capas no es un elemento decorativo; es una herramienta de comunicación que permite discutir la arquitectura con personas que no conocen el código. Cuando el equipo se reúne con el CMN o el Municipio, el diagrama funciona como un mapa del sistema que permite hacer preguntas precisas sobre dónde se implementa cada funcionalidad. Cuando un nuevo desarrollador se integra, el diagrama le dice exactamente dónde empezar a leer. Cuando un auditor revisa el código, el diagrama le dice qué archivos corresponden a cada capa. El diagrama se mantiene actualizado junto con el código: cada vez que se agrega una nueva capa o se modifica la responsabilidad de una capa existente, el diagrama se actualiza en el mismo commit. Esta disciplina de documentación junto al código es parte del contrato arquitectónico.

El diagrama siguiente muestra las cinco capas con sus componentes y responsabilidades:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  CAPA 1 — Presentación                                                   │
│  PWA: Vue 3 + TypeScript + Vite + MapLibre + Turf.js + Pinia            │
│  Geofencing reactivo en cliente | Estado de sesión local como            │
│  proyección del estado S60 | Sin mutación directa de estado               │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼─────────────────────────────────────────┐
│  CAPA 2 — Aplicación                                                     │
│  lota-server: FastAPI Python (Piloto A) | Rust (Piloto B)                 │
│  Endpoints REST | Autenticación JWT | Rate limiting | Orquestación        │
│  de comandos hacia dominio. Sin decisión sobre estado de juego.            │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼─────────────────────────────────────────┐
│  CAPA 3 — Dominio                                                        │
│  Wallet multi-moneda (D-016) | World Event engine | Subastas (D-017)     │
│  | ML analytics | Reportes ciudadanos                                   │
│  Lógica de negocio pura | Invariantes de dominio | Inyección             │
│  de dependencias entre módulos | Sin conocer la implementación            │
│  del motor ni de la infraestructura                                      │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼─────────────────────────────────────────┐
│  CAPA 4 — Motor S60 (FUENTE DE VERDAD)                                  │
│  ResonantMatrix | LiquidLattice | QHC | IsochronousClock                 │
│  | IsochronousOscillator | Kernel no-Markoviano                         │
│  | QuantumRiftDetector | lattice_interference.wgsl (GPU/wgpu)            │
│  MUTACIÓN DE ESTADO verificable | Aritmética S60 sin floats |            │
│  Generación de proyecciones | Síncrono con Lane A | Ignora                │
│  la existencia del dominio y la aplicación                                │
└────────────────────────────────┬─────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼─────────────────────────────────────────┐
│  CAPA 5 — Infraestructura                                                │
│  PostgreSQL + PostGIS | Redis Lane A (seguridad) + Lane B (observab.)   │
│  | OpenStreetMap (Nominatim + OSRM) | GPU (wgpu + wgsl)               │
│  PROYECCIONES del estado S60 | Persistencia | Caché | Cartografía       │
│  | Renderizado | Sin autoridad sobre el estado del juego                  │
└────────────────────────────────────────────────────────────────────────────┘
```

El flujo de datos es estrictamente descendente. Cuando un jugador hace check-in en una zona patrimonial, la PWA envía un comando POST a la Capa 2. El servidor de aplicación valida el JWT, verifica que el jugador está dentro del geofence de la zona según Turf.js, y construye un comando que envía a la Capa 3. El módulo de dominio correspondiente verifica las precondiciones (el jugador tiene el rango requerido, la zona está activa, el jugador no ha hecho check-in en las últimas 24 horas) y delega en el motor S60. El motor S60 ejecuta la mutación de estado: actualiza el balance de Carboncillos, graba la insignia en el retículo, registra el timestamp del check-in en la memoria líquida, y calcula el nuevo ranking communal. El resultado se proyecta como una fila en PostGIS para el dashboard municipal, una actualización en el Pinia store del jugador para la UI, y un mensaje en Redis Lane B para los observadores de métricas. El jugador recibe la respuesta de confirmación con su nuevo balance. En ningún paso de este flujo una capa inferior toma una decisión que no le corresponde; cada capa hace exactamente lo que su contrato le pide y delega el resto.

El flujo inverso, de datos hacia arriba, sigue el patrón de proyección. Cuando la PWA necesita mostrar el mapa con las zonas activas, envía una query a la Capa 2 que la delega a PostGIS. PostGIS responde con las geometrías de las zonas activas en el radio del jugador. La PWA renderiza el mapa sin pasar por el motor S60. Cuando la PWA necesita mostrar el balance del jugador, envía una query a la Capa 2 que la delega a Redis Lane B. Redis responde con el balance en caché. La PWA renderiza el balance sin pasar por el motor S60. Cuando la PWA necesita verificar la consistencia del estado, envía una query a la Capa 2 que la delega al motor S60 en memoria. El motor responde con el estado verificado. Este patrón permite que las consultas frecuentes se ejecuten sin tocar el motor S60, lo que maximiza el throughput del sistema.

El patrón de proyección también define cómo se manejan los errores de consistencia. Si una query a PostGIS devuelve un balance que no coincide con el balance en Redis, el sistema detecta la inconsistencia mediante el comando de verificación que se ejecuta periódicamente. Si la consistencia no se verifica, el sistema puede reconstruircada proyección a partir del estado S60 en memoria. Este proceso de reconstrucción es determinista, porque el motor S60 es determinista. El sistema puede reconstruir PostGIS, Redis, o cualquier otra proyección a partir del estado en memoria y el log de mutaciones. Esta capacidad de auto-reparación es posible solo porque el motor S60 es la fuente de verdad y todas las demás capas son proyecciones.

La relación entre las capas 4 y 5 es la decisión de diseño más importante del proyecto. PostgreSQL y Redis son proyecciones del estado S60, no fuentes independientes. Cada mutación se ejecuta primero en S60 y luego se proyecta hacia las capas inferiores. Las lecturas pueden ejecutarse desde cualquier proyección que ofrezca mejor rendimiento: una query geográfica de zonas cercanas se ejecuta en PostGIS; una lectura de balance se ejecuta en Redis Lane B; una verificación de consistencia del estado del retículo se ejecuta contra el estado S60 en memoria. Este patrón, documentado en MEMORY.md §0 y en las decisiones D-011 a D-014, elimina la clase completa de errores de consistencia que surgen cuando dos bases de datos intentan ser fuentes de verdad simultáneamente y divergen. El diseño completo de la arquitectura del servidor Rust, incluyendo la relación entre las capas 2 y 4, se encuentra en _analisis/07_propuesta_arquitectura_servidor_rust_juego.md §2. La arquitectura del Piloto A, donde la Capa 4 todavía no existe como motor Rust, implementa una versión simplificada donde el servidor Python actúa como fuente de verdad temporal; la transición a la Capa 4 completa es la milestone más importante del Piloto B.

La Capa 5 implementa además el patrón dual-lane documentado en D-011. Lane A (seguridad) usa fsync en cada persistencia, lo que garantiza que el log forense sobrevivirá una caída de energía del servidor. Lane B (observabilidad) canaliza métricas de throughput, benchmarks del motor, y eventos de tracing en un buffer que prioriza velocidad sobre resistencia a fallos. Ninguna de las dos lanes tiene conocimiento de la otra, y ninguna modifica el estado que la otra maneja. Esta separación física y lógica es parte del contrato arquitectónico, no una optimización que se pueda eliminar sin decisión explícita. Lane A sabe que es la lane de seguridad; Lane B sabe que es la lane de observabilidad. Ninguna sabe que la otra existe.

La justificación del patrón dual-lane se entiende mejor cuando se considera el caso de uso más exigente del sistema: el log forense para el CMN. Cuando el CMN solicita un reporte del uso de las zonas patrimoniales durante un período específico, el sistema debe poder reconstruir exactamente qué jugadores hicieron check-in, en qué zonas, y a qué horas. Esta reconstrucción es posible solo si el log de eventos sobrevivió a todos los escenarios de fallo, incluyendo una caída de energía del servidor durante la noche, un reinicio inesperado del servicio, y una desconexión de la UPS. Lane A está diseñada para este caso de uso: cada evento se persiste con fsync, lo que significa que el evento se escribe en el disco físico antes de que la llamada retorne. En un sistema sin fsync, un evento puede estar en el buffer del sistema operativo cuando ocurre la caída de energía, y perderse. En un sistema con fsync, el evento está en el disco físico cuando la llamada retorna, y sobrevivirá la caída. El costo de esta garantía es rendimiento: fsync es una operación bloqueante que espera la confirmación del disco. Por eso existe Lane B para el caso de uso donde el rendimiento importa más que la garantía de persistencia.

La jerarquía de cinco capas no es una sobreingeniería para un proyecto de esta escala. La razón por la que el proyecto usa esta arquitectura desde el inicio, incluso durante el Piloto A donde algunas restricciones se relajan, es que la arquitectura define el contrato entre las partes del sistema. Sin este contrato, el código de cada piloto se convierte en un sistema monolítico donde cada cambio tiene efectos secundarios impredecibles. Con el contrato, cada cambio tiene un área de impacto acotada y predecible. La inversión inicial en definir la arquitectura se amortiza en cada sprint de desarrollo posterior, porque la arquitectura reduce el costo de cada cambio. Esta es la misma razón por la que los proyectos de infraestructura crítica usan arquitecturas por capas desde el inicio, incluso cuando el sistema inicial es simple: la complejidad del sistema crece con el tiempo, y una arquitectura que funciona para un sistema simple debe poder escalar a un sistema complejo sin necesidad de reescritura.

El diagrama de capas funciona como documentación executable del diseño. Cuando un nuevo desarrollador se integra al proyecto, el diagrama le dice exactamente dónde reside cada responsabilidad. Si necesita modificar la lógica de autenticación, sabe que está en la Capa 2. Si necesita modificar la lógica de balance, sabe que está en la Capa 3 y la mutación está en la Capa 4. Si necesita modificar cómo se renderiza el mapa, sabe que está en la Capa 1. Esta capacidad de navegación reduce el tiempo de onboarding y reduce el riesgo de que un cambio toque la capa equivocada. El diagrama no es una foto del sistema actual; es una especificación del sistema objetivo. Durante el Piloto A, algunas celdas del diagrama todavía no existen como módulos separados; durante el Piloto B, el diagrama y el código coinciden exactamente.

La arquitectura de cinco capas también define los criterios de aceptación para cada piloto. El Piloto A se considera exitoso si la Capa 1 y la Capa 2 funcionan correctamente con datos simulados. El Piloto B se considera exitoso si la Capa 4 se implementa completamente y la Capa 3 la consume correctamente. La fase de producción se considera exitosa si todas las cinco capas funcionan en conjunto y las proyecciones de la Capa 5 son consistentes con el estado S60. Estos criterios de aceptación son parte del contrato arquitectónico y se verifican como parte del pipeline de CI antes de cada release.

La restricción de que la Capa 4 es la fuente de verdad tiene una consecuencia que no es obvia al principio: hace que el sistema sea más fácil de auditar. Cuando el CMN quiere verificar que el sistema funcionó correctamente durante un período específico, solo necesita verificar el estado del motor S60 en ese período. No necesita verificar PostgreSQL, Redis, ni ningún otro componente. El motor S60 es la única fuente de verdad, y su estado se puede verificar de forma determinista a partir del log de mutaciones. Esta simplicidad en la auditoría es posible solo porque la arquitectura respeta la restricción de una sola fuente de verdad. En un sistema con múltiples fuentes de verdad, la auditoría requiere verificar la consistencia entre todas ellas, lo que es exponencialmente más difícil.

El patrón de proyección tiene consecuencias concretas para la operación diaria del sistema. Cuando un jugador consulta su balance de Carboncillos, la lectura más rápida viene de Redis Lane B, que mantiene una copia en caché del último estado conocido. Cuando el dashboard municipal consulta estadísticas de reportes ciudadanos por zona, la query se ejecuta directamente en PostGIS, sin pasar por el motor S60. Cuando un auditor necesita verificar que el estado del retículo es consistente con las proyecciones en PostgreSQL, ejecuta un comando de verificación que compara el estado en memoria del motor contra las filas en las tablas correspondientes. Si hay divergencia, el sistema detecta la inconsistencia y la reporta antes de que un jugador la note. Esta arquitectura no elimina los bugs, pero los hace detectables y corregibles sin pérdida de datos, porque el motor S60 siempre puede reconstruir cualquier proyección a partir de su estado interno. El proceso de reconstrucción es determinista: dadas las mismas mutaciones, el motor produce las mismas proyecciones, siempre.

La restricción de direccionalidad del flujo tiene un beneficio adicional para la seguridad. La PWA solo puede enviar comandos a la Capa 2, nunca mutar estado directamente. La Capa 2 solo puede delegar en la Capa 3, nunca mutar estado directamente. La Capa 3 solo puede delegar en la Capa 4, nunca mutar estado directamente. La única forma de mutar el estado del juego es atravesar todas las capas en secuencia y llegar al motor S60, que valida la mutación contra sus invariantes internas antes de aceptarla. Un atacante que compromise la Capa 1 no puede mutar el estado del juego; solo puede enviar comandos que la Capa 2 filtra. Un atacante que compromised la Capa 2 no puede mutar el estado del juego; solo puede enviar comandos que la Capa 3 filtra. La cadena de validación es parte del diseño de seguridad, no un efecto secundario de la arquitectura. La cadena se rompe solo cuando el atacante llega al motor S60, que es la única capa que puede aceptar o rechazar una mutación.

La cadena de validación también protege contra errores de programación en las capas superiores. Si la Capa 2 tiene un bug que permite un comando sin autenticación, la Capa 3 lo rechaza porque no tiene un JWT válido. Si la Capa 3 tiene un bug que permite una mutación sin verificar las precondiciones del dominio, el motor S60 lo rechaza porque la mutación viola una invariante interna. Esta defensa en cascada es una consecuencia directa de la separación de responsabilidades. Cada capa es un filtro que reduce la probabilidad de que un comando inválido llegue al motor S60.

### §7.2 Principios SOLID aplicados al motor

Los cinco principios SOLID definen el contrato entre módulos del motor S60. Cada principio se materializa en artefactos concretos del código fuente, no en intenciones documentadas. Un revisor puede verificar cada principio abriendo el archivo correspondiente y confirmando que el módulo cumple exactamente su contrato. Los rangos informados en las descripciones se usan cuando el código fuente exacto no está disponible para una referencia de línea; en esos casos se usa el nombre del archivo y el propósito declarado del módulo.

**SRP — Responsabilidad única.** Cada módulo del crate Rust cumple un propósito acotado y no tiene razones para cambiar excepto cuando ese propósito cambia. El archivo `spa.rs` contiene únicamente la aritmética S60 en base 60 sin floats. No contiene lógica de red, no maneja persistencia, no sabe nada del retículo ni de la criptografía. El archivo `resonant_matrix.rs` contiene únicamente la lógica de la matriz resonante hexagonal: su inicialización con parámetros de acoplamiento, su protocolo de mensajes entre celdas, su proyección al espacio 3D, y su formato de snapshot gzip para persistencia. No sabe nada de la aritmética que usa; podría usar floats internamente si quisiera, pero el forbid en el crate padre lo impide. El archivo `liquid_memory.rs` maneja exclusivamente el almacenamiento clave-valor respaldado por memoria compartida del sistema operativo. Expone una API de get/put/delete/iter sobre un archivo en /dev/shm o su equivalente en Windows. No sabe nada del contenido que almacena, no sabe quién lo llama ni por qué. El archivo `qhc.rs` implementa únicamente el latido cuántico isoentrópico: genera un heartbeat verificable a intervalos regulares sin usar timers del sistema operativo. No conoce la matriz que alimenta ni los eventos que genera; simplemente emite una señal a un intervalo que es verificable criptográficamente. El archivo `crystal_cipher.rs` encapsula únicamente la criptografía AES-256-GCM con Blake3 para autenticación. Expone una API de encrypt/decrypt/verify sobre slices de bytes. No sabe qué se cifra ni por qué, no conoce el contexto de la operación criptográfica. Los tests de cada módulo se ejecutan de forma aislada; un test de cristalografía no carga el módulo de aritmética y viceversa. Esta separación permite cambiar la implementación criptográfica sin tocar la aritmética S60, y viceversa, sin que ningún test falle por la razón equivocada. El inventario completo de módulos disponibles, con sus rutas dentro del crate, propósitos declarados y dependencias declaradas, está documentado en _analisis/15_inventario_sentinel_disponible_para_motor.md.

**OCP — Abierto para extensión, cerrado para modificación.** La arquitectura dual-lane implementa este principio en el nivel de infraestructura. Lane A garantiza que cada evento se persista con fsync antes de retornar, sin que el router de eventos lo sepa. Lane B permite agregar métricas, benchmarks y tracing sin modificar el código del router. La introducción de un nuevo tipo de evento en el motor no requiere cambios en el router existente; se mapea en una nueva rama de handler que las capas superiores nunca ven. A nivel de retículo, el diseño hexagonal permite agregar nuevos anillos de resonancia sin modificar la estructura de celda base. Cada celda conoce solo a sus seis vecinos inmediatos y responde a un protocolo de mensajes predefinido que no cambia con el número de anillos. Un nuevo tipo de resonancia se agrega como un mensaje nuevo en ese protocolo, no como una modificación del router de mensajes. El crate layout separados, con `lota-engine` como crate principal y `me60os_core` como dependencia de ruta, permiten que nuevas funcionalidades se agreguen como crates nuevos que dependen de los existentes, sin tocar el código de los existentes. Si se necesita un nuevo módulo de física para un tipo de objeto del juego, se crea un crate `lota-physics-*` que depende de `me60os_core`; ni `lota-engine` ni `me60os_core` se modifican. La decisión D-011 registra esta restricción como decisión de diseño explícita, no como consecuencia accidental de no haber escrito código todavía. El test del OCP es ejecutable: se puede agregar un nuevo crate que dependa de `me60os_core` sin tocar ningún archivo existente del proyecto.

**LSP — Sustitución de Liskov.** El trait `IsochronousOscillator` implementa `Copy`, lo que garantiza que cualquier función que acepte un oscilador como argumento puede recibir cualquier implementación sustituta sin cambio de comportamiento observable por el caller. Los constructores `ResonantMatrix::new` y `ResonantMatrix::with_coupling` son intercambiables para la construcción con parámetros de tamaño; ambos producen una matriz funcionalmente equivalente desde la perspectiva del caller. `ResonantMatrix::new` crea una matriz con parámetros de acoplamiento por defecto; `ResonantMatrix::with_coupling` crea una matriz con parámetros de acoplamiento explícitos. Desde la perspectiva de cualquier código que use la matriz, ambas producen el mismo tipo, con la misma API, y el mismo comportamiento observable. Esto permite que las pruebas del dominio usen matrices con acoplamiento controlado, con valores conocidos, sin modificar el código de producción. El dominio puede depender del contrato de construcción sin conocer los detalles de implementación de cada constructor. En la práctica, esto significa que una suite de tests puede crear una matriz con parámetros triviales y verificar el comportamiento del dominio sin tener que configurar el retículo real.

El principio LSP también se aplica a la relación entre la implementación CPU y la implementación GPU del motor. Ambas implementaciones exponen la misma API, producen los mismos resultados para las mismas entradas, y son intercambiables desde la perspectiva del código que las llama. Esto permite que el dominio ejecute pruebas en CPU, donde la reproducibilidad es máxima, y que producción ejecute en GPU, donde el rendimiento es máximo, sin que el dominio sepa la diferencia. La verificación de esta intercambiabilidad es parte del pipeline de CI: antes de cada release se ejecutan los mismos tests con ambas implementaciones y se confirma que los resultados son idénticos dentro de la tolerancia numérica definida.

**ISP — Segregación de interfaces.** Los bindings PyO3 exponen hacia Python únicamente los métodos que Piloto A necesita: proyección de estado, mutación de wallet, y consulta de posición. No exponen la API Rust completa, no exponen los tipos internos de celda, no exponen el protocolo de mensajes del retículo. El bridge `ResonantLatticeBridge` en sentinel-cortex provee una superficie de API estrecha y estable: Python ve solo los métodos de proyección, no las primitivas de celda, no la estructura interna de la matriz, no los tipos de mensaje del protocolo de resonancia. Esto aísla el dominio Python de cambios en la implementación interna del motor Rust. Cuando el motor cambia su formato interno de celda, el bridge se ajusta, pero Python no necesita cambiar una línea. Cuando se agrega un nuevo método al bridge, Python lo puede usar si lo necesita; si no lo usa, no se ve afectado. El test del ISP se verifica observando que los módulos Python que usan el bridge no necesitan importarse entre sí; cada módulo Python solo conoce el bridge, y el bridge conoce el motor.

El principio ISP también se aplica dentro del motor Rust, en la relación entre el módulo de aritmética y el módulo de cristalografía. El módulo de aritmética no sabe que existe el módulo de cristalografía; solo sabe que necesita una función de cifrado para la verificación de integridad. El módulo de cristalografía no sabe que existe el módulo de aritmética; solo sabe que necesita verificar la integridad de un buffer de bytes. El módulo que orquesta los dos (el retículo) conoce a ambos, pero los otros módulos no se conocen entre sí. Esta separación permite que el módulo de cristalografía se reemplace por otro módulo de cifrado, o que el módulo de aritmética se ejecute en un contexto donde el cifrado no es necesario, sin modificar los otros módulos.

La decisión de no usar Bevy como motor de física se dokumentiert en la decisión D-011 como una restricción explícita, pero la razón va más allá de la preferencia técnica. Bevy es un motor de juegos con sus propias abstracciones de mundo, entidad y componente que fueron diseñadas para juegos genéricos. Si el proyecto usara Bevy, el diseño del dominio tendría que adaptarse a las abstracciones de Bevy, lo que acoplaría el dominio al motor. El motor S60, en cambio, fue diseñado específicamente para este proyecto y sus requisitos de determinismo, verificabilidad y ausencia de floats. La diferencia entre usar Bevy y usar un motor propio es la diferencia entre alquilar una herramienta que alguien más diseñó y construir una herramienta que se diseñó exactamente para el trabajo que se necesita hacer. En un proyecto donde la soberanía del código es un requisito, la decisión de construir en lugar de alquilar es coherente con ese requisito.

**DIP — Inversión de dependencias.** El crate `lota-engine` depende de `me60os_core` mediante una dependencia de ruta local, no mediante Bevy ni ningún otro motor de terceros. Los módulos de alto nivel del dominio (wallet, subastas, eventos, reportes) dependen de las abstracciones `ResonantMatrix` e `IsochronousOscillator` definidas como traits, no de las implementaciones concretas de GPU en wgsl. Esta inversión permite que el motor se ejecute en CPU para pruebas unitarias, donde el rendimiento no importa y la reproducibilidad sí, y en GPU para producción, donde el rendimiento es crítico. Cambiar entre CPU y GPU no requiere cambiar una línea del código de dominio; solo requiere cambiar el target de compilación. La decisión D-011 registra esta restricción como decisión de diseño explícita. La dependencia de ruta local significa que el código de `me60os_core` se compila junto con `lota-engine` en cada build, sin pasar por crates.io ni por ningún registro externo. Esto elimina la clase completa de ataques de confusión de dependencias, donde un paquete malicioso en crates.io se hace pasar por una dependencia legítima. El proyecto no usa Bevy como motor de física precisamente porque Bevy tiene sus propias abstracciones de mundo y entidad que competirían con las abstracciones del dominio, y porque agregar una dependencia externa de ese tamaño introduce un punto de control sobre el proyecto que está fuera de la capacidad del equipo de mantener. Si Bevy desaparece o cambia su licencia, el proyecto no se ve afectado.

### §7.3 Métricas ISO/IEC 5055

El proyecto adopta las seis dimensiones de calidad definidas en ISO/IEC 5055 (Automated Source Code Quality Measures) como marco para la medición objetiva de la calidad del código del motor S60. Cada dimensión se vincula a una práctica verificable, no a una impresión ni a una aspiración. Las cifras exactas de rendimiento varían según el hardware de producción, por lo que se reportan como órdenes de magnitud verificados, con los rangos correspondientes. Los benchmarks y tests de cada dimensión están disponibles en el repositorio para reproducción independiente.

**Confiabilidad.** La configuración `forbid(clippy::float_arithmetic)` en `me-60os-core/src/lib.rs` elimina la clase completa de errores de aritmética de punto flotante en tiempo de compilación. Si un programador intenta usar un float, el código no compila. Esta no es una convención ni una buena práctica; es una restricción del compilador que hace físicamente imposible introducir la clase de bug que pretende prevenir. La validación empírica en `fpu_vs_pai_bench` muestra aproximadamente 0% de truncamiento en la ALU S60 contra aproximadamente 85.7% en Float64 FPU sobre ejecuciones de 100000 iteraciones o más. La diferencia es de dos órdenes de magnitud en precisión numérica, no solo en velocidad. Esto convierte la confiabilidad numérica en una propiedad demostrable, verificable en cualquier máquina que pueda compilar el crate, no solo en el entorno del equipo de desarrollo. Un nuevo desarrollador que clone el repositorio puede ejecutar el benchmark y confirmar la cifra sin confiar en la documentación del proyecto.

**Rendimiento.** El throughput del motor Rust S60 se mide en EXP-015 (sentinel_bench): aproximadamente 120 millones de nodos por segundo en Rust S60 contra aproximadamente 0.04 millones de nodos por segundo en la implementación legado en Python. Esta diferencia de cuatro órdenes de magnitud justifica la inversión en el Piloto B basado en Rust. El número exacto de nodos por segundo varía según el hardware de producción, específicamente según el ancho de banda de memoria y la disponibilidad de SIMD, por lo que se reporta como orden de magnitud verificado. El benchmark completo, con su código fuente y sus condiciones de ejecución, está disponible en el repositorio para que cualquier revisor pueda reproducirlo. La dimensión de rendimiento en ISO 5055 también considera el uso de memoria y la eficiencia energética; el diseño sin floats del motor S60 reduce el consumo energético por operación, lo que tiene implicaciones directas para el costo de operación del servidor fan.

**Seguridad.** El módulo `crystal_cipher` implementa AES-256-GCM con validación de integridad mediante Blake3. AES-256-GCM proporciona confidencialidad y autenticación; Blake3 proporciona una verificación de integridad independiente del cifrado. El probe eBPF LSM en `ebpf/init_kprobe.c` corre en anillo 0 del kernel del servidor fan, inspeccionando llamadas al sistema sin pasar por el espacio de usuario y sin ser evitable por un proceso que quiera ocultar su actividad. Lane A usa fsync en cada persistencia, lo que garantiza que el log forense sobrevivirá una caída de energía del servidor sin pérdida de eventos. La separación física de Lane A y Lane B en procesos o máquinas separadas es una extensión natural del diseño que la arquitectura soporta sin cambios en el código de dominio. La dimensión de seguridad en ISO 5055 también considera la tasa de vulnerabilidades conocidas en el código, el uso de dependencias sin vulnerabilidades conocidas, y la presencia de mecanismos de defensa en profundidad. El forbid de floats contribuye a la seguridad numérica del sistema, eliminando una clase de ataque que explota errores de redondeo en contextos criptográficos. El no uso de Bevy ni de otros motores de terceros grandes elimina la superficie de ataque que esas bibliotecas introducen y las vulnerabilidades que esas bibliotecas puedan tener en el futuro sin conocimiento del equipo.

La seguridad también se mide por la superficie de ataque del sistema. Cada dependencia externa es una superficie de ataque potencial. El proyecto minimiza las dependencias externas mediante el uso de dependencias de ruta local para `me60os_core`, el uso de std library para la mayor parte del código, y la preferencia por implementaciones propias cuando una dependencia externa no es estrictamente necesaria. El probe eBPF es una excepción deliberada: es la única manera de inspeccionar llamadas al sistema desde anillo 0 sin modificar el kernel, y su código es auditado como parte del pipeline de seguridad del proyecto.

La dimensión de confiabilidad en ISO 5055 también considera la cobertura de tests y la capacidad de recuperación ante fallos. El forbid de floats es la primera línea de defensa contra errores numéricos. Los tests de propiedad (property-based tests) son la segunda línea: generan miles de comandos aleatorios y verifican que el motor siempre produce estados consistentes. Los tests de snapshot son la tercera línea: verifican que el formato de snapshot es version-tolerant y que los snapshots se pueden leer con versiones posteriores. El log forense de Lane A es la cuarta línea: permite reconstruir qué comandos causaron una inconsistencia si las tres primeras líneas fallan.

La dimensión de rendimiento en ISO 5055 también considera la eficiencia del uso de memoria y la escalabilidad del sistema bajo carga. El motor S60 está diseñado para ejecutarse en hardware modesto: el servidor fan tiene especificaciones que cualquier pyme puede permitirse, no un servidor de alta gama. Esto es deliberado: el proyecto debe ser operable por organizaciones sin presupuesto de TI. La eficiencia del motor S60 en hardware modesto es una consecuencia del diseño sin floats y la arquitectura basada en memoria compartida. El consumo de memoria del motor está acotado por el tamaño del retículo, que es configurable, y por el tamaño del log de mutaciones en memoria, que está acotado por la política de snapshot. El consumo de CPU está acotado por el número de threads del motor, que es configurable según el hardware disponible.

La dimensión de modificabilidad en ISO 5055 también considera la deuda técnica del proyecto. La deuda técnica se mide como la diferencia entre la arquitectura objetivo (documentada en §7) y la arquitectura actual (implementada en cada piloto). El Piloto A tiene la mayor deuda técnica: la Capa 4 todavía no existe como motor Rust, y la Capa 5 todavía no tiene el patrón dual-lane completo. El Piloto B reduce la deuda técnica significativamente. El release de producción la reduce a cero, o lo más cerca de cero que sea posible. La deuda técnica se rastrea en las decisiones D-011 a D-014 como parte del backlog del proyecto. Cada decisión identifica qué partes de la arquitectura objetivo faltan en la implementación actual y cuándo se implementarán.

**Mantención.** Los principios SRP y DIP descritos en §7.2 mantienen los módulos desacoplados, lo que reduce el área de impacto de cada cambio. Cuando un módulo cambia, los módulos que dependen de él a través de traits bien definidos se ajustan solo si el cambio rompe el contrato del trait; los módulos que no dependen de él directamente no necesitan ajustarse. El formato de snapshot gzip en `resonant_matrix.rs` permite guardar el retículo en disco en un formato tolerante a cambios de versión del software. Una instantánea escrita por la versión 1.2 se puede leer con la versión 1.3; la versión 1.3 puede escribir en un formato que la versión 1.4 podrá leer. Esta propiedad se verifica como parte del pipeline de release: antes de cada release se ejecuta un snapshot escrito por la release anterior y se confirma que el estado se reconstruye sin errores ni pérdida de datos. La mantención también se mide por el tiempo medio entre fallos (MTBF) del sistema en producción y el tiempo medio de reparación (MTTR), ambos rastreables mediante los logs de Lane A.

La mantención del código se facilita mediante la estructura de crates que hace que cada módulo sea independently compilable y testable. El sistema de módulos de Rust permite que cada crate tenga su propio árbol de dependencias, sus propios tests, y su propia documentación. Cuando se modifica un crate, solo ese crate se recompila; los crates que dependen de él se recompilan solo si la interfaz del crate modificado cambió. Este sistema de recompilación incremental reduce los tiempos de build y hace que los tests se ejecuten más rápido, lo que incentiva a los desarrolladores a ejecutar los tests después de cada cambio. La documentación de cada crate se mantiene junto con el código, lo que hace que la documentación no se quede desactualizada.

**Modificabilidad.** El principio OCP descrito en §7.2 y la estructura modular del crate Rust, con `lota-engine` separado de `me60os_core`, permiten agregar nuevas funcionalidades sin modificar el código existente. El particionamiento en crates separados significa que un cambio en el módulo criptográfico no recompila el motor de física, lo que reduce los tiempos de build y elimina el riesgo de efectos secundarios en módulos no relacionados. Agregar un nuevo módulo de analytics, por ejemplo, requiere solo un crate nuevo que depende de los existentes, sin tocar ningún crate existente. El árbol de dependencias de Cargo se verifica en cada build como parte del pipeline de CI; una circularidad en las dependencias o una dependencia inesperada rompe el build. La dimensión de modificabilidad en ISO 5055 también considera la extensibilidad del diseño medible como el número de puntos de extensión disponibles; el retículo hexagonal tiene un número fijo de puntos de extensión que es conocido y limitado.

**Reusabilidad.** Los componentes de dominio del proyecto, incluyendo la wallet multi-moneda según D-016, las subastas según D-017, los World Events que modifican dinámicamente las reglas del juego, y el enjambre SOMA que procesa los datos de sensores distribuidos, se construyen a partir de las mismas primitivas S60 de aritmética sin floats. Esto significa que todos estos componentes comparten las mismas garantías de confiabilidad numérica y rendimiento, porque comparten la misma capa de abstracción. Un bug encontrado en la aritmética S60 afecta a todos los componentes simultáneamente, lo que hace que la corrección sea más valiosa y verificable. La expansión a otras comunas del corredor Arauco, incluyendo Curanilahue, Lebu, Arauco y Concepción, reutiliza la pila completa sin necesidad de desarrollo adicional en el motor. Cada comuna proporciona únicamente el contenido communal específico, que se carga como datos en las tablas PostGIS y como configuración del motor S60, no como código nuevo. El motor no sabe que está ejecutándose en Lota o en Lebu; solo conoce los parámetros que se le pasan. Esta separación entre motor y contenido es lo que hace que el modelo sea replicable sin extracción: ninguna comuna necesita un equipo de ingeniería para unirse al corredor, solo un equipo de contenido que produza los datos geográficos y las definiciones de las zonas. La dimensión de reusabilidad en ISO 5055 también considera la modularidad del código; el diseño en crates separados maximiza la modularidad y minimiza el acoplamiento.

La dimensión de reusabilidad también se aplica al código de dominio más allá del motor S60. El sistema de wallet multi-moneda (D-016) es un módulo de dominio que se puede extraer y reutilizar en otros proyectos que necesiten un sistema de balances multi-moneda con transacciones atómicas. Las subastas (D-017) son un módulo de dominio que se puede extraer y reutilizar en otros proyectos que necesiten un sistema de pujas con cierre automático y asignación atómica. Esta extractabilidad es una consecuencia directa de los principios SOLID: los módulos que no dependen de infraestructura ni de detalles de implementación son naturalmente portables.

Estos tres bloques, en conjunto, definen el contrato de ingeniería que el motor S60 debe satisfacer. La arquitectura por capas garantiza que cada responsabilidad reside en su estrato correcto; un cambio en la infraestructura no toca el dominio, un cambio en el dominio no toca el motor, y un cambio en el motor no rompe la aplicación. Los principios SOLID garantizan que los módulos son independientes, extensibles y sustituibles; cada módulo se puede reemplazar por otra implementación que respete el mismo contrato sin que los callers lo noten. Las métricas ISO 5055 garantizan que la calidad se mide con números verificables, no con impresiones; cada dimensión tiene una práctica verificable asociada que cualquier revisor puede ejecutar. El contrato es auditable. Cualquier revisor puede abrir los lints en `me-60os-core/src/lib.rs` y confirmar que la configuración forbid está activa, ejecutar los benchmarks documentados en EXP-015 y confirmar los órdenes de magnitud reportados, y verificar cada principio SOLID leyendo el código fuente de cada módulo y confirmando que su propósito declarado coincide con su implementación. Esa auditabilidad es lo que hace defendible la plataforma a largo plazo ante instituciones públicas, Municipio, CMN y cualquier entidad que requiera garantías técnicas verificables antes de comprometer recursos.

El párrafo de cierre sobre las tres soberanías de §6 se conecta directamente con la arquitectura de esta sección. La soberanía de la capa matemática, mencionada en §6 como el diferenciador del proyecto, se materializa en la Capa 4 y se protege mediante el forbid de floats, los principios SRP y DIP, y la métrica de confiabilidad de ISO 5055. La soberanía de la infraestructura, también en §6, se materializa en la Capa 5 con PostgreSQL, Redis y OSM, sin dependencias corporativas, y se protege mediante la proyección como fuente de verdad y el patrón dual-lane. La soberanía del modelo regional se materializa en la Capa 3 y la dimensión de reusabilidad de ISO 5055, que garantizan que el motor es agnóstico de la comuna y que la expansión al corredor Arauco es una operación de contenido, no de ingeniería. Estas tres conexiones no son accidentales. Cada decisión en §6 tiene una contraparte arquitectónica verificable en §7. El revisor que lea ambas secciones puede trazar una línea desde cualquier frase del cierre de §6 hasta un artefacto concreto en §7. Cuando el Municipio de Lota revise este documento, podrá preguntar en qué capa se implementa cada promesa del párrafo de cierre y recibir una respuesta precisa con referencias a artefactos del código.

Hay una distinción importante entre la arquitectura que se describe aquí y la arquitectura que existe hoy en el repositorio. El §7 documenta la arquitectura objetivo, la que el proyecto debe tener cuando esté completo. Durante el Piloto A, la Capa 4 se implementa de forma simplificada en Python, sin el retículo hexagonal ni la aritmética S60. La Capa 5 se implementa con PostgreSQL y Redis, pero sin el patrón dual-lane completo. Esta brecha entre la arquitectura objetivo y la implementación actual es conocida y documentada. Las decisiones D-011 a D-014 registran las milestones donde la arquitectura se acerca a la objetivo. La existencia de esta brecha no es una debilidad del documento; es una representación honesta del estado del proyecto. Un documento que mostrara una arquitectura perfecta que no existe aún sería menos útil que uno que mostrara la arquitectura objetivo junto con el plan para llegar a ella. El §7 funciona como el destino; el plan de desarrollo funciona como el mapa. Un revisor que quiera evaluar la viabilidad técnica del proyecto debe leer §7 para entender qué se está construyendo y leer las decisiones D-011 a D-014 para entender cuándo estará disponible.

---

## §8 PWA — Piloto A

La aplicación web progresiva es la ventana que el jugador tiene hacia Lota Indómito. Es lo que el turista ve cuando camina por Lota, lo que el jugador toca cuando completa una micro-sesión, y lo que el mineur consulta cuando revisa su balance de minerales. El Piloto A construye esta superficie con Vue 3, TypeScript, MapLibre GL JS, Turf.js y Pinia. No contiene lógica de juego; esa lógica vive en lota-server y en el motor S60. La PWA es la membrana entre el jugador y el sistema.

El alcance del Piloto A incluye la PWA completa con todas las funcionalidades descritas en este párrafo: mapa con geofencing, loop de micro-sesión con cuatro minijuegos funcionales, wallet multi-moneda con transfers y cupones, modo offline con sincronización, instrumentación de 16 eventos, navegación, notificaciones, accesibilidad WCAG 2.1 AA, seguridad en dispositivo y en tránsito, y pipeline de CI/CD con Cloudflare Pages. Las funcionalidades del Piloto B (actualización de tileserver propio, estilo de mapa personalizado, push notifications avanzadas, integración con sensores externos) están fuera del alcance del Piloto A y se planifican para releases posteriores.

### §8.1 Stack tecnológico y decisiones

La PWA se construye sobre un stack deliberadamente reducido en dependencias, optimizado para dispositivos móviles y para funcionar con conectividad intermitente. Cada decisión de stack tiene una contraparte documentada en las decisiones del proyecto. El análisis completo de tecnologías disponibles está en `_analisis/05_analisis_tecnologias_disponibles.md` §3.

**Vue 3** con TypeScript y Vite. Vue 3 es el framework JavaScript elegido, seleccionado por su tamaño de bundle reducido y su rendimiento rápido en dispositivos móviles (D-007). TypeScript aporta verificación de tipos estática, lo que elimina una clase entera de errores de runtime que de otro modo aparecerían en producción. Vite es el bundler y servidor de desarrollo, elegido por su recarga rápida en caliente durante el ciclo de desarrollo. La combinación Vue 3 + TypeScript + Vite produce una aplicación que pesa menos de 200 KB comprimida, sin contar los assets cartográficos. El framework usa la Composition API con `<script setup>`, lo que facilita la separación entre lógica de presentación y lógica de negocio dentro de cada componente. Los componentes de la PWA se organizan en tres capas: componentes de interfaz (mapas, diálogos, minijuegos), stores de Pinia (sesión, wallet, catálogo), y una capa de servicios que se comunica con lota-server mediante una librería cliente tipada. La librería cliente se genera a partir de la especificación OpenAPI del servidor, lo que garantiza que los tipos de request y response son consistentes entre cliente y servidor en todo momento.

**MapLibre GL JS** para cartografía. MapLibre es el fork open-source de Mapbox GL JS, que provee renderizado de teselas vectoriales sin las restricciones de licenciamiento de Mapbox. La PWA usa MapLibre para mostrar las capas OSM que son servidas por el tileserver propio del proyecto, lo que garantiza que los mapas no dependen de terceros. El mapa se renderiza en un canvas WebGL, lo que permite animaciones fluidas y superposición de capas temáticas sin pérdida de rendimiento. La decisión de no usar Mapbox se documenta en D-007 como requisito de soberanía de infraestructura. La PWA configura MapLibre con dos fuentes de datos: las teselas vectoriales del tileserver propio (base OSM) y un source GeoJSON para los polígonos de zonas activas, que se actualizan desde lota-server cada 5 minutos. Las zonas se renderizan como polígonos con borde de color y sombreado semitransparente, con el color indicando el estado de la zona (activa, completada, bloqueada). Los estilos de capa se definen en un archivo JSON externo que se carga al iniciar, lo que permite cambiar la apariencia del mapa sin re-desplegar la aplicación. Durante el Piloto A, se usa el estilo predeterminado OSM Bright; en releases posteriores, se migrará a un estilo personalizado con paleta de colores mineros verde y carbón, según lo permita el equipo de diseño.

**Turf.js** para geofencing en cliente. Turf.js provee operaciones geoespaciales en JavaScript: punto-dentro-de-polígono, cálculo de distancias, intersección de polígonos. La PWA usa Turf.js para determinar si la posición GPS del jugador se encuentra dentro del perímetro de alguna zona activa. El cálculo es completamente en cliente: no hay request de red para saber si el jugador está dentro de una zona. Esto significa que el trigger de zona funciona incluso cuando el jugador tiene señal débil, lo que es crítico para las zonas rurales de Lota. El watch de posición se implementa con la API Geolocation del navegador, con una configuración de alta precisión (enableHighAccuracy: true) y un intervalo de actualización de 3 segundos. Cuando la posición cambia, se ejecuta turf.booleanPointInPolygon contra el array de polígonos de zonas cacheadas. Para optimizar el rendimiento, los polígonos se organizan en un quadtree espacial (biblioteca rbush) que permite descartar rápidamente las zonas que están lejos de la posición actual, reduciendo el número de llamadas a Turf.js de O(n) a O(log n) donde n es el número total de zonas. La lógica de geofencing se documenta en `docs/concepto-juego.md` §2.

**Pinia** para gestión de estado. Pinia es la biblioteca oficial de estado para Vue 3, que reemplaza a Vuex. La PWA usa Pinia para mantener el estado de la sesión del jugador: posición actual, balance de minerales, insignias obtenidas, rango vigente. Pinia permite persistir el estado en IndexedDB, lo que habilita la recuperación de sesión después de que el navegador se cierre. El estado en Pinia es una proyección del estado autoritativo en lota-server; la PWA nunca modifica el estado del servidor directamente, sino que envía comandos. Los stores de Pinia son tres: SessionStore (posición, modo, user_id), WalletStore (balances, transacciones, cupones), y GameStore (zonas, insignias, progreso de misiones). Cada store tiene un método `$subscribe` que registra cambios como eventos para el pipeline de ML. El diseño de stores sigue el principio de responsabilidad única: SessionStore solo conoce la sesión, WalletStore solo conoce los balances y transacciones, y GameStore solo conoce las zonas y el progreso.

**Service Worker y Workbox** para capacidades PWA. El service worker cachea los assets estáticos (HTML, CSS, bundle JavaScript, metadatos de teselas) en la primera visita. La estrategia de cacheo es "stale-while-revalidate" para los assets de aplicación y "cache first" para los assets inmutables (hash de contenido en el nombre del archivo). La PWA es instalable en Android y iOS a través del prompt de instalación estándar del navegador. Funciona offline: el geofencing sigue operativo mediante los polígonos de zonas cacheados, la wallet muestra el último balance conocido, y los minijuegos se ejecutan sin conexión. El manifest.json declara los íconos en múltiples resoluciones (192x192 y 512x512), el nombre corto de la aplicación ("Lota"), y el tema de color (verde minero, #2D5016). El service worker también intercepta las requests de API y las enruta según disponibilidad de red: requests en línea van a lota-server, requests fuera de línea se sirven desde IndexedDB o se encolan en TransactionQueue según corresponda. El service worker se registra en el evento `load` de la ventana, con un período de actualización de 24 horas que verifica si hay una nueva versión de la aplicación disponible. Si hay una nueva versión, el service worker instala la nueva versión en segundo plano y espera hasta que todas las pestañas activas se cierren antes de activar la nueva versión, lo que evita interrumpir al jugador en medio de una micro-sesión.

El stack completo, entonces, es: Vue 3 + TypeScript + Vite + MapLibre GL JS + Turf.js + Pinia + Workbox + rbush. Siete bibliotecas, ninguna con licenciamiento restrictivo. La configuración del proyecto usa un vite.config.ts que configura la resolución de paths con @/, el plugin de Vue con TypeScript, y el plugin de PWA con Workbox. El proyecto se estructura en tres directorios principales: `src/components/` para los componentes de Vue, `src/stores/` para los stores de Pinia, y `src/services/` para la capa de comunicación con el servidor. Los tests de la PWA se escriben con Vitest y se ejecutan en un entorno headless con Playwright para los tests de integración.

### §8.2 Loop del turista: las cinco tramos de la micro-sesión

La micro-sesión es la unidad atómica de compromiso del juego. Cada vez que un jugador entra en una zona activa, la PWA ejecuta una secuencia de cinco tramos que duran, en conjunto, cuatro minutos. Esta secuencia está diseñada para caber en el tiempo de una visita guiada convencional a un punto de interés.

El diseño de la micro-sesión responde a la observación de que los turistas en Lota tienen ventanas de atención breves, frecuentemente interrumpidas por señal de celular inestable o por el ritmo del grupo. La micro-sesión está diseñada para ser interrumpible sin pérdida de progreso: si el jugador cierra la aplicación en medio de un tramo, al volver encontrará el estado guardado. El guardado de estado se hace en cada transición entre tramos, escribiendo en IndexedDB la marca del tramo actual y los datos parciales relevantes. Al reabrir, la PWA lee ese estado y retoma desde el tramo correspondiente. El diseño de la micro-sesión se documenta en `docs/concepto-juego.md` §2.3.

**Tramo 1 — Trigger (15 segundos).** Cuando el GPS del jugador cruza el perímetro de una zona activa, la PWA detecta el evento mediante Turf.js y ejecuta una respuesta inmediata: vibración del dispositivo (Navigator Vibration API) y banner en pantalla: "Estás en el Chiflón del Diablo. Toca para descubrir." El trigger es puramente en cliente; no se hace ningún request de red en este tramo. Esto significa que el trigger funciona con cobertura de red mínima o nula. La zona se marca como "en curso" en IndexedDB, lo que permite que la micro-sesión se reanude si se interrumpe antes de completarse. El trigger también verifica si la zona ya fue completada en la sesión actual: si fue completada, muestra en lugar "Ya visitaste este lugar" con la opción de reintentar para ganar minerales adicionales con un multiplicador reducido. Este mecanismo de reintento con multiplicador está diseñado para incentivar múltiples visitas a la misma zona sin que el jugador sienta que perdió la primera oportunidad.

**Tramo 2 — Contexto (45 segundos).** La PWA despliega una presentación narrativa breve: un fragmento de mapa centrado en la zona, el avatar del personaje histórico correspondiente, dos o tres líneas de diálogo del personaje, y audio de narración opcional. El jugador entiende a quién está encontrando y dónde está. No hay scroll, no hay muros de texto. El diálogo es deliberadamente corto: máximo 80 caracteres por línea, máximo tres líneas por escena. Este diseño se probó en el análisis de engagement documentado en `_analisis/20_loop_jugador_dia_a_dia.md` §2, que mostró que los jugadores abandonan experiencias narrativas largas si no reciben feedback en los primeros 30 segundos. Los avatares son archivos SVG optimizados que pesan menos de 15 KB cada uno, cacheados en el service worker. El audio de narración se sirve bajo demanda y no se precarga, para minimizar el consumo de datos en zonas rurales. El audio usa el formato Opus a 48 kbps, lo que mantiene el tamaño por debajo de 50 KB por clip de 30 segundos.

**Tramo 3 — Acción (90 segundos).** La PWA lanza el minijuego correspondiente a la ruta. El minijuego varía según el tipo de zona. Todos los minijuegos comparten una restricción de diseño: no requieren texto para ser jugados, solo íconos y gestos. Esto permite que los turistas que no hablan español puedan completar las micro-sesiones, y que los jugadores analfabetos no queden excluidos. Los minijuegos son:

- Para "Amasando Pan", el minijuego es un QTE (Quick Time Event) donde el jugador debe amasar masa siguiendo un ritmo marcado por la vibración del dispositivo. En pantalla se muestra un círculo que pulsa en sincronía con el ritmo; el jugador debe tocar la pantalla en el momento exacto del pulso. El ritmo se genera proceduralmente con una secuencia pseudoaleatoria seeded por la zona, lo que garantiza que todos los jugadores ven la misma secuencia para la misma zona, pero que la secuencia no es predecible de antemano.
- Para "El Geólogo del Tiempo", el minijuego es un puzzle estratigráfico donde el jugador clasifica capas de carbón, fósiles y roca según la era geológica correspondiente. Las capas se muestran como franjas horizontales que el jugador debe arrastrar a la posición correcta; la validación se hace contra el perfil geológico canónico de la zona, que se almacena en los datos de zona cacheados. Las franjas se colorean según el material: marrón oscuro para carbón, gris para roca, ocre para fósiles. El puzzle se considera resuelto cuando al menos el 80 por ciento de las franjas está en la posición correcta.
- Para "El Inventario del Carbón", el minijuego es una búsqueda de objetos ocultos dentro de una ilustración de la mina. Los objetos están ocultos con técnicas de blending que los hacen difíciles de ver a primera vista pero identificables con atención. Se muestran entre 5 y 8 objetos por escena; el jugador tiene 90 segundos para encontrar todos. Cada objeto encontrado genera una vibración corta; al encontrarlos todos, se reproduce una animación de revelación del inventario completo.
- Para "Vigídel Golfo", el minijuego es la identificación de fauna marina mediante un simulador de binoculares. Se muestran siluetas de fauna local (lobos marinos, pelícanos, huillocs) que aparecen brevemente en la pantalla; el jugador tiene 3 segundos para identificarlas tocando el ícono correspondiente. Si el jugador falla o no toca a tiempo, la silueta se descarta y aparece la siguiente. El objetivo es identificar al menos 5 especies en los 90 segundos disponibles.

Cada minijuego está pre-cargado antes de que el jugador llegue a la zona, de modo que no hay pantalla de carga entre tramos. Los activos de los minijuegos se cachean en el service worker junto con los assets estáticos. El resultado del minijuego (ganado o perdido) se registra en IndexedDB antes de pasar al tramo de recompensa, lo que permite retomar la micro-sesión incluso si se cierra el navegador durante la recompensa. Los minijuegos se renderizan en un canvas HTML5 de 360 por 640 píxeles, lo que garantiza rendimiento consistente en dispositivos de gama baja.

**Tramo 4 — Recompensa (60 segundos).** La PWA acredita la wallet del jugador con cobre (típicamente entre 10 y 50 cobre por micro-sesión, según la complejidad del minijuego), actualiza los puntos de experiencia, anima la insignia ganada, y despliega un mensaje de felicitación: "Has rescatado un fragmento del carbón." La animación de insignia usa una secuencia de escalado y rotación en CSS, sincronizada con una vibración doble. Si el jugador pierde el minijuego, puede reintentar inmediatamente sin penalización. Este diseño de reintento sin costo se eligió para que la experiencia no se sienta frustrante para jugadores casuales, incluyendo familias con niños. El número máximo de reintentos por micro-sesión es tres; después del tercer fallo, la micro-sesión se marca como completada con recompensa cero y se desbloquea la zona siguiente. El XP ganado se calcula con una curva logarítmica basada en el número de zonas completadas en la sesión: las primeras zonas dan más XP que las posteriores, lo que incentiva al jugador a explorar zonas nuevas.

**Tramo 5 — Próximo (30 segundos).** La PWA muestra la dirección hacia la siguiente zona: "La próxima zona está a 320 metros al sur" con un fragmento de mapa que traza la ruta. El fragmento de mapa se renderiza con MapLibre y muestra solo la ruta y los puntos de interés relevantes, sin la sobrecarga visual del mapa completo. Si la siguiente zona está a más de 500 metros, la PWA muestra también el tiempo estimado de caminata a paso normal (aproximadamente 1 minuto cada 80 metros). Si no hay zona siguiente en un radio de 1 kilómetro, la PWA muestra el mapa completo con todas las zonas de la ruta. El fragmento de mapa incluye también un marcador de posición actual del jugador, actualizado cada segundo.

Duración total de la micro-sesión: 15 + 45 + 90 + 60 + 30 = 240 segundos = 4 minutos. Una visita típica a un punto de interés permite completar entre 6 y 10 micro-sesiones. El diseño del loop de micro-sesión se documenta en `_analisis/20_loop_jugador_dia_a_dia.md` §2.

### §8.3 Wallet multi-moneda en el cliente

La wallet del jugador es la interfaz que muestra los balances de cobre, oro y estaño, y que permite transfers, redenciones de cupones y Pujas en subastas. En la PWA, la wallet es una proyección del estado autoritativo en lota-server, presentada a través de Pinia con persistencia en IndexedDB. El diseño del sistema multi-moneda se documenta en `_analisis/23_sistema_monedas_minerales.md` §3.

**Visualización de balances.** La wallet muestra los tres balances de minerales con íconos diferenciados por color: cobre en naranja, oro en amarillo, estaño en gris. Cada balance se muestra con su valor numérico y un indicador de tendencia: una flecha verde hacia arriba si el balance creció desde la última sincronización, una flecha roja hacia abajo si decreció, o un guion si no hubo cambios. La actualización de balances se hace en tiempo real mediante polling cada 30 segundos cuando la PWA está en primer plano; cuando está en segundo plano, la actualización se hace al volver al primer plano. Los balances muestran también el historial de cambios en las últimas 24 horas como un mini gráfico de líneas en SVG, lo que permite al jugador ver tendencias sin abrir el historial completo.

**Transfers P2P.** La wallet permite transfers entre jugadores mediante código QR o nickname. El flujo de QR es: el emisor ingresa el monto y toca "Generar QR", la PWA genera un objeto `{from: user_id, to: null, amount, mineral_type, nonce, expires_at}` que se firma con la clave privada del jugador (almacenada cifrada en IndexedDB mediante la Web Crypto API), y el QR codifica la versión en base64 del objeto firmado. El nonce es un UUID v4 generado en el momento de la creación del QR; tiene una validez de 5 minutos, después de los cuales el QR expira y se debe generar uno nuevo. El receptor toca "Escanear QR", la cámara del dispositivo abre el lector QR, y al confirmar, la PWA envía el transfer a lota-server. El nonce evita replay attacks: lota-server rechaza cualquier transfer con un nonce ya usado. Los límites diarios de transfer y el enfriamiento entre transfers al mismo jugador se aplican en cliente como validación anticipada, pero se refuerzan autoritativamente en lota-server. Los límites se documentan en `_analisis/23_sistema_monedas_minerales.md` §3.

**Cupones QR.** La wallet muestra cada cupón QR con su saldo remanente y su fecha de caducidad. Los cupones caducan entre 30 y 60 días después de su emisión, según lo documentado en `_analisis/21 §4.4`. Cuando un cupón está por caducar (dentro de 7 días), la wallet muestra una notificación push proactiva si el jugador tiene las notificaciones habilitadas. La redención de cupones requiere escanear el código QR del cupón con la cámara del dispositivo y confirmar el monto a redimir. El comercio aliado que recibe la redención confirma la operación mediante su propia interfaz, lo que completa el flujo. El flujo de redención usa el mismo esquema de firma con clave privada del comercio, lo que garantiza que solo el comercio autorizado puede confirmar la redención.

**Historial de transacciones.** La wallet despliega el historial completo de transacciones del jugador: ganancias de minerales (provenientes de micro-sesiones y World Events), gastos (en redención de cupones y Pujas en subastas), y transfers. El historial se muestra en chunks de 20 transacciones, con opción de filtrar por tipo de transacción (ganancias, gastos, transfers, recompras) y por rango de fechas. Cada transacción del historial muestra la marca de tiempo, el tipo, el monto con signo (+ cobre, - cobre), y el contexto (nombre de la zona o del otro jugador). El historial es de solo lectura en la PWA; no se puede editar ni eliminar transacciones.

**Subastas.** La wallet también muestra la interfaz de Pujas en subastas, que es un widget que se conecta al endpoint de subastas de lota-server. La PWA no calcula el estado de la puja (eso vive en el servidor); solo muestra la puja actual, permite introducir una nueva puja, y muestra notificaciones cuando la puja es superada por otro jugador. La interfaz de subastas requiere conexión en tiempo real, por lo que no funciona offline.

**Anti-abuso.** La wallet aplica reglas de anti-abuso client-side de forma anticipada para mejorar la experiencia del jugador: máximo 10 transfers por día, enfriamiento de 60 segundos entre transfers al mismo jugador, y balance mínimo de 0 (no se permiten balances negativos). Estas reglas se muestran al jugador antes de que intente una acción bloqueada, con un mensaje claro: "Has alcanzado el límite diario de transfers" o "Debes esperar 60 segundos antes de transferir a este jugador nuevamente." La aplicación estricta de las reglas vive en lota-server; la PWA solo previene el intento, pero no garantiza la aplicación.

**Sincronización.** La PWA lee la wallet desde Redis Lane B (caché) cuando está disponible, lo que provee tiempos de respuesta menores a 50 ms para la consulta de balances. Cuando Redis Lane B no tiene el estado actualizado (cache miss), la PWA consulta el estado autoritativo en lota-server. La sincronización se hace en background cada 30 segundos; el jugador puede forzar una sincronización manual tocando el botón de refresh. El indicador de sincronización aparece en la barra de estado de la wallet: verde cuando está sincronizado con el servidor, amarillo cuando está sincronizando, rojo cuando está desconectado. Si la sincronización falla tres veces consecutivas, la PWA deja de intentar automáticamente y espera a que el jugador fuerce la sincronización, para evitar drenaje de batería en zonas con cobertura inestable.

### §8.4 Modo offline-first

La arquitectura offline-first es un requisito no negociable para Lota Indómito. La cobertura celular en las zonas rurales de la comuna es irregular: el centro de Lota tiene señal 4G decente, pero las zonas del Percy (interior de la mina), El Salado y el borde costero tienen cobertura débil o nula. Un turista que entre a una zona histórica con mala señal no puede quedar excluido de la experiencia.

**Service Worker.** El service worker, gestionado por Workbox, cachea los assets estáticos en la primera carga: el HTML, el CSS, el bundle JavaScript, los avatares de personajes, los sprites de minijuegos, y los metadatos de teselas cartográficas. La estrategia de cacheo "stale-while-revalidate" para assets de aplicación significa que el jugador siempre ve la versión más reciente disponible, pero nunca espera por la red si la versión cacheada existe. Las teselas cartográficas usan la estrategia "cache-first" porque son inmutables y de alto volumen: cachear las teselas visitadas permite que el mapa funcione offline en zonas ya recorridas. El límite de caché de teselas se configura en 100 MB; cuando se supera, las teselas más antiguas se eliminan con una política LRU. El service worker también intercepta las requests de API y las enruta según disponibilidad de red: requests en línea van a lota-server, requests fuera de línea se sirven desde IndexedDB o se encolan en TransactionQueue según corresponda.

**IndexedDB.** Los datos de sesión del jugador se persisten en IndexedDB: balance actual, posición GPS, estado de zonas completadas, resultados de minijuegos, y cupones. IndexedDB es una base de datos dentro del navegador, accesible incluso sin conexión. Cuando el navegador se cierra y se reabre, Pinia restaura el estado desde IndexedDB y la experiencia continúa donde quedó. La estructura de la base IndexedDB tiene cuatro object stores: SessionState (el estado actual de la sesión), ZoneCache (polígonos de zonas y metadatos), TransactionQueue (transacciones pendientes de sincronizar), y CouponCache (cupones del jugador). La clave de SessionState es el user_id; la clave de ZoneCache es el zone_id. La base IndexedDB se cifra con una clave derivada del identificador del dispositivo mediante la Web Crypto API, lo que protege los datos del jugador si el dispositivo se pierde o es robado.

**Funcionamiento offline.** Cuando el jugador está offline, la PWA mantiene las funciones críticas: el geofencing sigue operando con los polígonos de zonas cacheados, la wallet muestra el último balance conocido (con un indicador de "sin conexión" en la barra superior), y los minijuegos se ejecutan completamente en local. Las transacciones que el jugador hace offline (por ejemplo, completar un minijuego) se encolan en IndexedDB TransactionQueue con marca de tiempo Unix en milisegundos, tipo de transacción, y los datos relevantes. La cola puede acumular hasta 200 transacciones pendientes; si se supera ese límite, la PWA muestra una advertencia sugeriendo reconectar. Las transacciones offline se identifican con el campo `offline: true`, lo que permite a lota-server distinguirlas de las transacciones en línea al momento de la reconciliación.

**Reconciliación al reconectar.** Cuando la conectividad regresa, la PWA sincroniza el estado offline con el servidor mediante delta sync: los comandos encolados se reintentan en orden, el servidor valida cada comando, y el estado se reconcilia. Si hay conflicto (por ejemplo, el jugador gastó minerales offline y el balance en servidor cambió), el servidor tiene autoridad y la PWA actualiza su estado para reflejar la versión autoritativa. El protocolo de reconciliación usa timestamps: cada transacción en la cola lleva un timestamp de cliente; el servidor aplica las transacciones en orden de timestamp, rechazando las que tengan timestamp anterior al último estado conocido del cliente. El resultado de la reconciliación se muestra al jugador como una notificación: "Se sincronizaron 3 acciones pendientes." Si hay rechazos, se muestran con detalle: "1 acción no pudo sincronizarse. Tu balance se actualizó con el estado del servidor."

**Limitaciones offline.** La PWA no puede mostrar actualizaciones en tiempo real de World Events mientras está offline. El calendario de eventos se cachea diariamente, pero las activaciones de eventos en vivo requieren conexión. Los transfers P2P no se pueden iniciar sin conexión, porque requieren firma con clave privada que reside en el servidor y la confirmación del receptor. Las Pujas en subastas tampoco funcionan offline, porque requieren el estado actual de la puja en tiempo real. El registro en subastas está disponible offline: el jugador puede dejar una puja registrada que se enviará automáticamente cuando la conectividad regrese. Estas limitaciones se aceptan como tradeoff consciente del diseño offline-first; se prioriza la funcionalidad del geofencing y los minijuegos por sobre features que requieren sincronización en tiempo real. El diseño offline se documenta en `_analisis/19_investigacion_tecnologias_y_proyectos_referencia.md` §1.4, que analiza proyectos de referencia con capacidades AR de audio incluso con pantalla apagada. La investigación de esas tecnologías informó el diseño de resiliencia de la PWA.

### §8.5 Instrumentación para ML externo

La PWA emite 16 tipos de eventos anónimos diseñados para alimentar el servicio de machine learning externo documentado en D-014. Cada evento lleva un user_id seudónimo (un UUID v4 generado en el cliente, no relacionado con la identidad real del jugador), lo que permite análisis de comportamiento sin comprometer la privacidad. El diseño de la instrumentación se documenta en `_analisis/22_ml_analytics_d014.md` §5 y en `docs/concepto-juego.md` §12.

**Eventos de turista.** Estos eventos cubren el recorrido del jugador por las zonas:

- `user_session_start`: se emite al abrir la PWA. Schema: `{user_id, timestamp, lat, lng, mode}` donde mode es "Jugador", "Turista" o "Familia". El modo se selecciona en el onboarding y determina qué narrativa se despliega y qué minijuegos están activos (el modo Familia desactiva los minijuegos más difíciles).
- `user_session_end`: se emite al cerrar la PWA o al transcurrir 30 minutos sin interacción. Schema: `{user_id, timestamp, duration_seconds, last_lat, last_lng}`.
- `poi_visit`: se emite cuando el jugador completa una micro-sesión. Schema: `{user_id, timestamp, zone_id, micro_session_id, minerals_earned, minigame_result, retry_count}` donde retry_count es el número de veces que el jugador reintentó el minijuego antes de completarlo.
- `world_event_join`: se emite cuando el jugador entra a un World Event activo. Schema: `{user_id, timestamp, event_id, event_type}` donde event_type es "temporal", "recurrente" o "semanario".
- `mission_complete`: se emite cuando el jugador completa una misión. Schema: `{user_id, timestamp, mission_id, time_to_complete_seconds, zones_visited}`.
- `world_event_complete`: se emite cuando el jugador completa un World Event. Schema: `{user_id, timestamp, event_id, minerals_earned, position_lat, position_lng}`.
- `coupon_redeemed`: se emite cuando el jugador redime un cupón QR en un comercio aliado. Schema: `{user_id, timestamp, coupon_id, commerce_id, amount, distance_from_zone}`.
- `passport_update`: se emite cuando el jugador obtiene o mejora una insignia. Schema: `{user_id, timestamp, badge_id, badge_tier, previous_tier}`.

**Eventos sociales.** Estos eventos cubren las interacciones P2P:

- `transfer_sent`: se emite cuando el jugador envía un transfer de minerales a otro jugador. Schema: `{user_id, timestamp, recipient_id, mineral_type, amount}`.
- `transfer_received`: se emite cuando el jugador recibe un transfer. Schema: `{user_id, timestamp, sender_id, mineral_type, amount}`.
- `trade_offered`: se emite cuando el jugador ofrece un trade. Schema: `{user_id, timestamp, trade_id, offered_mineral, offered_amount, requested_mineral, requested_amount}`.
- `trade_accepted`: se emite cuando el otro jugador acepta un trade. Schema: `{user_id, timestamp, trade_id}`.
- `gift_sent`: se emite cuando el jugador envía un regalo a otro jugador. Schema: `{user_id, timestamp, recipient_id, item_type, mineral_type, amount}`.

**Eventos de comercio.** Estos eventos cubren la actividad comercial:

- `commerce_registered`: se emite cuando un comercio aliado se registra en la plataforma. Schema: `{commerce_id, timestamp, location_lat, location_lng, category, zone_id}`.
- `coupon_issued`: se emite cuando se genera un cupón QR. Schema: `{coupon_id, timestamp, issuer_id, amount, mineral_type, expires_at}`.
- `coupon_used`: se emite cuando un cupón se redime. Schema: `{coupon_id, timestamp, commerce_id}`.
- `commerce_mineral_received`: se emite cuando un comercio recibe el canje de minerales. Schema: `{commerce_id, timestamp, mineral_type, amount, coupon_id}`.

**Canal de emisión y privacidad.** La PWA agrupa los eventos en batches de hasta 50 eventos y los envía a lota-server cada 30 segundos, o inmediatamente si el batch supera los 50 eventos. El envío se hace mediante una request POST a `/api/v1/events/batch` que incluye el batch serializado como JSON. Los eventos se almacenan en PostgreSQL en la tabla `analytics_events` y el servicio de ML externo los lee mediante vistas materializadas que agregan los eventos por sesión, zona y jugador. El diseño garantiza que ningún evento contiene información que identifique personalmente al jugador; el UUID seudónimo no permite vincular eventos a una identidad real sin la tabla de mapping que reside en lota-server y no se comparte con el servicio de ML. El consentimiento de analytics se pide en el onboarding y se puede revocar en cualquier momento desde la configuración de la cuenta; si se revoca, la PWA deja de emitir eventos y borra los eventos pendientes en local. Si el jugador revoca el consentimiento, la PWA también elimina el UUID local y genera uno nuevo, lo que rompe cualquier vínculo temporal con los eventos ya emitidos.

### §8.6 Navegación, UI del mapa y personalización

La interfaz de navegación de la PWA se diseña para funcionar con una sola mano, en un teléfono movernos con las manos sudadas o con guantes. Todos los controles están en la mitad inferior de la pantalla; la mitad superior muestra el contenido (mapa, diálogo, minijuego). La barra de navegación inferior tiene tres botones: Mapa (vista del mapa completo), Wallet (balance y transfers), y Perfil (insignias, progreso, configuración). Esta barra es fija y accesible desde cualquier vista de la aplicación.

**Mapa completo.** La vista de mapa muestra la posición del jugador en el centro de la pantalla, con las zonas activas como polígonos coloreados a su alrededor. Los polígonos de zona muestran el estado con colores: verde para zonas disponibles, dorado para zonas completadas con insignia ganada, gris para zonas bloqueadas, y rojo pulsante para World Events activos. Al tocar una zona en el mapa, se despliega un popup con el nombre de la zona, el personaje histórico asociado, y la distancia desde la posición actual. Si la zona está completada, el popup muestra también la insignia ganada y la fecha de la visita. La posición del jugador se obtiene del GPS del dispositivo y se muestra con un marcador animado (un círculo con efecto de pulso) que se actualiza cada 3 segundos. Si el GPS no está disponible o es impreciso (radio de error mayor a 50 metros), el marcador se muestra en amarillo con un icono de advertencia, y la zona no se activa hasta que la precisión mejore.

**Navegación turn-by-turn.** La PWA no provee navegación turn-by-turn completa (eso lo hace Google Maps o Waze), pero sí muestra rutas suguradas entre zonas de la misma ruta. La ruta se dibuja como una línea punteada sobre el mapa, con marcadores en cada intersección importante. La dirección de la siguiente zona se muestra como una brújula en la esquina superior derecha de la vista de mapa, apuntando siempre hacia la próxima zona activa.

**Modo escuro.** La PWA soporta modo escuro, que se activa automáticamente según la preferencia del sistema operativo del dispositivo. En modo escuro, el mapa usa un estilo de tiles oscuro (CartoDB Dark Matter) y la interfaz usa colores de alto contraste para mantener la legibilidad. El modo escuro reduce el consumo de batería en dispositivos con pantallas OLED, lo que es relevante para jugadores que usan la aplicación durante caminatas largas.

**Notificaciones push.** La PWA solicita permiso de notificaciones en el onboarding, pero nunca lo fuerza. Las notificaciones push se usan para tres tipos de mensajes: recordatorios de World Events activos en la cercanía (radio de 500 metros), advertencias de caducidad de cupones (7 días antes), y mensajes de transfers recibidos. Cada tipo de notificación se puede activar o desactivar independientemente desde la configuración de la cuenta. Las notificaciones nunca incluyen información sensible (saldos, transferencias); solo incluyen un mensaje genérico y un botón que abre la PWA. El servicio de notificaciones push usa Cloudflare Workers para enviar las notificaciones, lo que garantiza latencias menores a 500 ms desde que el servidor genera el evento hasta que la notificación llega al dispositivo. Durante el Piloto A, las notificaciones push solo funcionan cuando la PWA está instalada en el dispositivo (no desde el navegador); en releases posteriores se evaluará el soporte para navegadores sin instalación.

**Accesibilidad.** La PWA implementa las pautas WCAG 2.1 nivel AA. Los minijuegos tienen versiones accesibles con audio-guía para jugadores con discapacidad visual, donde las instrucciones se dan por voz y los controles se operan con gestos simples. El contraste de colores de la interfaz cumple con la ratio mínima de 4.5:1. Los controles táctiles tienen un área mínima de 44 por 44 píxeles. La navegación por teclado es soportada para jugadores que usan dispositivos de asistencia. El texto de la interfaz usa la fuente del sistema, lo que garantiza legibilidad en todos los dispositivos. El tamaño de fuente se escala según la configuración de accesibilidad del dispositivo, sin romper el layout de la interfaz.

### §8.7 Seguridad y privacidad

La seguridad de la PWA se diseña en capas: seguridad en el dispositivo, seguridad en tránsito, y seguridad en el servidor.

**Seguridad en el dispositivo.** La clave privada del jugador para transfers se almacena en IndexedDB, cifrada con una clave derivada del identificador del dispositivo mediante PBKDF2 con 100.000 iteraciones. La clave de cifrado no sale nunca del dispositivo. Si el jugador cambia de dispositivo, debe exportar la clave privada cifrada (mediante un archivo protegido con contraseña) e importarla en el nuevo dispositivo; no hay recuperación de clave por parte del servidor. Los datos de sesión en IndexedDB se cifran con AES-GCM usando una clave ephemeral que se genera al iniciar sesión y se descarta al cerrar. La PWA también implementa certificate pinning para las conexiones con lota-server: el certificate pin se declara en el service worker y se verifica en cada request HTTPS. Si el certificado del servidor no coincide con el pin, la request falla y se muestra un error al jugador.

**Seguridad en tránsito.** Todas las comunicaciones entre la PWA y lota-server usan HTTPS con TLS 1.3. Los tokens de sesión se almacenan en HttpOnly cookies, no en localStorage, lo que previene ataques de cross-site scripting (XSS) que roben tokens. El servicio de ML externo recibe eventos anónimos solo a través de vistas materializadas de solo lectura en PostgreSQL, sin acceso directo a la base de datos de jugadores. Las contraseñas de usuario se hashean en el servidor con argon2id, un algoritmo de hashing diseñado para ser resistente a ataques de GPU. La PWA nunca almacena contraseñas en el cliente; la autenticación se hace mediante el flujo Authorization Code with PKCE, que es el estándar recomendado para SPAs.

**Privacidad.** La PWA recopila datos de ubicación solo mientras la aplicación está en primer plano y con el permiso explícito del jugador. Los datos de ubicación se usan exclusivamente para el geofencing y la emisión de eventos analíticos. La PWA no vende ni comparte datos de jugadores con terceros. El diseño de privacidad se documenta en el aviso de privacidad, que se muestra en el onboarding y está disponible en cualquier momento desde la configuración de la cuenta. El jugador puede exportar todos sus datos en cualquier momento, incluyendo historial de transacciones, insignias, y eventos emitidos.

**Consentimiento de menores.** La PWA no admite a menores de 13 años sin el consentimiento de un padre o tutor. El flujo de onboarding pregunta la edad; si el jugador declara tener menos de 13 años, se pide el correo del padre o tutor para enviar un enlace de consentimiento. Hasta que se reciba el consentimiento, la cuenta tiene funcionalidad limitada: no se permiten transfers, no se pueden redimir cupones, y no se emiten eventos con ubicación precisa (se generaliza a nivel de zona).

### §8.8 Testing, CI/CD y deployment

El pipeline de testing de la PWA se organiza en tres niveles: tests unitarios, tests de integración, y tests end-to-end.

Los **tests unitarios** se escriben con Vitest y cubren la lógica de cada store de Pinia, los algoritmos de geofencing, la generación de eventos, y la serialización de transacciones offline. Cada store tiene su archivo de tests correspondiente en `src/stores/__tests__/`. Los tests unitarios se ejecutan en cada commit como parte del pipeline de CI, y el build falla si la cobertura de tests unitarios baja del 80 por ciento.

Los **tests de integración** se escriben con Vitest y Testing Library, y cubren la interacción entre stores, la comunicación con la capa de servicios, y el flujo de sincronización offline. Los tests de integración usan mocks para la comunicación con lota-server, implementados con MSW (Mock Service Worker), lo que permite simular respuestas del servidor en el entorno de tests sin necesidad de un servidor real.

Los **tests end-to-end** se escriben con Playwright y cubren flujos completos de usuario: onboarding, geofencing, micro-sesión, transferencia, y redención de cupón. Los tests E2E se ejecutan en un pipeline separado que corre una vez por día en un dispositivo físico real (un teléfono Android conectado al pipeline de CI), porque el comportamiento del GPS en emuladores no refleja la realidad del geofencing.

**CI/CD.** El pipeline de CI usa GitHub Actions con tres jobs: lint (eslint + prettier + tsc --noEmit), test (vitest con coverage), y build (vite build que genera el bundle de producción). El job de build solo se ejecuta si los dos anteriores pasan. El deployment se hace a Cloudflare Pages en cada push a la rama main, con un paso de validation que verifica que el service worker se registra correctamente y que los assets estáticos tienen los headers de cacheo correctos.

**Monitoring.** Una vez desplegada en producción, la PWA usa Cloudflare Analytics para métricas de rendimiento: Core Web Vitals (LCP, FID, CLS), tasa de retención de usuarios, y frecuencia de uso offline. Las métricas se agregan por zona geográfica y por dispositivo, lo que permite identificar zonas donde la experiencia funciona mal. Las métricas de Core Web Vitals se reportan a lota-server como eventos analíticos con el tipo `performance_metric`. El dashboard de monitoring incluye también métricas de error rates (capturadas mediante window.onerror y window.unhandledrejection), latencia de sincronización offline, y tasa de eventos emitidos versus eventos recibidos por el servidor. El dashboard se comparte con el Municipio como parte del reporte de impacto del proyecto, según lo establecido en el acuerdo de colaboración documentado en MEMORY.md §0.

**Métricas de rendimiento objetivo.** La PWA del Piloto A tiene objetivos de rendimiento verificables en CI: el bundle JavaScript de producción no supera los 200 KB comprimidos (sin contar los assets de minijuegos), el tiempo de carga inicial (LCP) es menor a 2.5 segundos en una conexión 4G típica, y el tiempo de respuesta de la interfaz de wallet es menor a 100 ms. El geofencing tiene un consumo de batería menor al 3 por ciento por hora de uso activo, medido en un dispositivo de referencia (Google Pixel 5). Estos objetivos se verifican en cada build como parte del pipeline de CI, y el build falla si algún objetivo no se cumple. Los resultados de rendimiento se documentan en el informe de métricas del Piloto A, disponible para el CMN y el Municipio.

La PWA es la superficie que el jugador ve y toca. Es deliberadamente simple: Vue 3 + TypeScript + MapLibre + Turf.js + Pinia. Funciona offline, sincroniza cuando hay conexión, y emite datos que el servicio de ML usa para justificar e informar la inversión pública en patrimonio cultural. No contiene la lógica del juego; esa lógica reside en lota-server y en el motor S60. Todo lo que hay debajo de la superficie es invisible para el jugador, y eso es intencional. La PWA es la carta de presentación del proyecto ante el turista que descarga la aplicación en Lota y la abre por primera vez; esa primera impresión determina si el turista sigue jugando o elimina la aplicación. Por eso el Piloto A prioriza la fluidez, la claridad y la resiliencia sobre la cantidad de features.

---

## §9 lota-server — backend y motor

Lota-server es el componente de backend que orquesta todas las operaciones del juego.
Recibe las solicitudes de la PWA, ejecuta la lógica de dominio, persiste los cambios en PostgreSQL,
y proyecta el estado hacia el motor S60 en Piloto B.
No contiene las matemáticas centrales del juego (esas residen en el motor S60),
pero gestiona todos los aspectos operativos: autenticación, eventos del mundo,
billetera, ingestion de eventos ML, e infraestructura OSM.
Lota-server es el puente entre la experiencia del jugador y los datos del proyecto.

### §9.1 Stack del backend: FastAPI + PostgreSQL + PostGIS

El backend del Piloto A se construye sobre una pila moderna de Python
que prioriza velocidad de desarrollo y corrección.
La decisión D-006 documenta la elección de FastAPI como capa HTTP transitional para Piloto A;
en Piloto B esta capa se reescribe en Rust (Axum o equivalente)
para alinearse con el rendimiento y las convenciones del motor S60.
La propuesta técnica en _analisis/04_propuesta_tecnica_stack_osm.md sección 3
justifica la elección del stack Python para la etapa de prototipado,
comparando alternativas de ORM y bases de datos
y concluyendo que la combinación de FastAPI, SQLAlchemy y PostgreSQL
ofrece la mejor relación entre velocidad de desarrollo y robustez operativa para un piloto.

**FastAPI** es el framework web elegido para lota-server.
FastAPI genera documentación OpenAPI/Swagger de forma automática
a partir de las firmas de las rutas y los modelos Pydantic,
lo que facilita la coordinación entre equipos y la validación temprana de contratos de API.
El sistema de tipos de FastAPI, potenciado por Pydantic,
intercepta payloads malformados en la frontera de la API
antes de que alcancen la capa de dominio.
Cada modelo Pydantic define los tipos esperados, los valores por defecto
y las restricciones de rango; si un cliente envía un amount negativo o un user_id vacío,
FastAPI responde con un error 422 antes de ejecutar cualquier código de dominio.
La documentación interactiva de Swagger permite que los desarrolladores de la PWA
exploren los endpoints, verifiquen los formatos de respuesta
y generen clientes tipados sin necesidad de spec files manuales
ni herramientas adicionales de generación de código.
Esta capacidad de auto-documentación es especialmente valiosa durante el desarrollo paralelo
de frontend y backend, ya que ambos equipos trabajan contra un contrato de API vivo
que se actualiza automáticamente cuando se modifican los modelos.

Pydantic es la biblioteca de validación que subyace a FastAPI.
Define los esquemas de request y response con anotaciones de tipo de Python,
lo que convierte la validación en una preocupación declarativa
en lugar de código imperativo disperso.
Cuando un payload llega a una ruta FastAPI, Pydantic lo coerce al tipo declarado,
aplica las validaciones definidas (regex, rangos, enums),
y popula el objeto del modelo; si la coerce falla,
el error se devuelve al cliente con un mensaje descriptivo
que indica exactamente qué campo falló y por qué.
Esta estrategia reduce la cantidad de código de validación
que los desarrolladores necesitan escribir y mantener,
y elimina la clase de bugs donde un campo inesperado se ignora silenciosamente
porque nadie esperaba ese formato en ese endpoint.

**PostgreSQL 16** es la base de datos relacional que almacena todo el estado persistente del juego.
PostgreSQL es la opción natural para un proyecto que requiere transacciones ACID,
consultas complejas sobre datos de usuario,
y un modelo de datos que evoluciona con cada etapa del proyecto.
La decisión por PostgreSQL frente a alternativas como SQLite (para desarrollo local)
o MongoDB se fundamenta en la madurez del ecosistema PostgreSQL,
la disponibilidad de extensiones geoespaciales y de tipos JSON,
y la familiaridad del equipo con el motor.
PostgreSQL también ofrece Row Level Security (RLS),
lo que permite definir políticas de acceso a nivel de fila en la base de datos,
una capa adicional de seguridad que complementa la autenticación de la API.

**PostGIS 3.4** extiende PostgreSQL con capacidades geoespaciales.
PostGIS proporciona tipos geográficos nativos (POINT, LINESTRING, POLYGON, GEOMETRYCOLLECTION),
indeksación espacial mediante R-tree sobre GiST (Generalized Search Tree),
y un conjunto amplio de funciones de consulta espacial.
Las más relevantes para el proyecto son ST_DWithin,
que verifica si un punto está dentro de un radio dado de otro punto
(usado para geofencing del lado del servidor),
y ST_Contains,
que verifica si una geometría contiene completamente a otra
(usado para validar que un check-in cayó dentro de la zona esperada).
Sin PostGIS, la validación de geofencing del lado del servidor requeriría
cargar archivos GeoJSON en memoria y ejecutar algoritmos de punto-en-polígono en Python puro,
lo cual es lento para polígonos complejos con cientos de vértices
y consume memoria proporcional al número de zonas activas.
Con PostGIS, la validación usa el índice GiST para filtrar candidatos en tiempo logarítmico
y luego verifica solo los polígonos candidatos,
lo que reduce el tiempo de query de segundos a milisegundos.

La PWA, lota-server y el servicio de ML leen todos desde la misma instancia PostgreSQL.
Esta arquitectura shared-database significa que no hay sincronización manual entre servicios:
el servicio de ML consume materialized views que lota-server mantiene actualizadas
con los últimos eventos de los jugadores,
y el dashboard del Municipio lee las mismas tablas que la PWA,
lo que garantiza consistencia entre lo que ve el jugador y lo que ve el Municipio.
El patrón de materialized views es especialmente útil para el servicio de ML,
que necesita acceso eficiente a datos agregados (como la frecuencia de check-ins por zona
en la última semana) sin tener que ejecutar queries analíticas complejas
sobre las tablas transaccionales.

**SQLAlchemy 2.0** es el ORM que abstrae las consultas SQL.
El directorio backend/ del proyecto contiene los modelos SQLAlchemy
para las entidades principales: users (perfil y preferencias),
sessions (tokens de autenticación),
zones (polígonos y metadatos),
world_events (calendario y estado de eventos),
transactions (registro de movimientos de wallet),
npcs (inventario y estado de personajes),
y materialized views para consumo del servicio de ML.
SQLAlchemy 2.0 soporta el modo async mediante el driver asyncpg,
lo que permite a lota-server atender múltiples solicitudes concurrentes
sin bloquear el event loop de Python.
La ventaja de usar SQLAlchemy sobre raw SQL es doble:
seguridad contra inyección (las consultas se construyen mediante el Expression Language,
no mediante concatenación de strings)
y portabilidad del código entre distintos motores de base de datos.
El Expression Language de SQLAlchemy genera SQL correcto para PostgreSQL
sin necesidad de escribir SQL manualmente,
lo que reduce errores y facilita las pruebas con SQLite en desarrollo.

**Alembic** gestiona las migraciones del esquema de base de datos.
Cada cambio de esquema se registra como un archivo de migración numerado
que puede aplicarse o revertirse de forma atómica.
El esquema inicial del Piloto A tiene 8 tablas:
users, sessions, zones, world_events, wallet_balances, wallet_transactions,
wallet_coupons, npcs.
La Etapa 1 agrega las tablas de subastas y cupones_redemption
a medida que esas funcionalidades se implementan.
Alembic mantiene un historial versionado de cada cambio,
lo que permite desplegar migraciones progresivas en producción
y revertir si algo falla.
Antes de aplicar una migración en producción,
se ejecuta primero en staging con datos de prueba
para detectar problemas de rendimiento o pérdida de datos.
El workflow de migración es:
el desarrollador genera un archivo de migración con alembic revision --autogenerate,
revisa el diff generado,
aplica la migración localmente con alembic upgrade head,
verifica que los tests pasan,
y finalmente sube la migración al repositorio.
En producción, las migraciones se aplican automáticamente
como parte del pipeline de despliegue.

El directorio backend/ del proyecto ya contiene el andamiaje FastAPI
con las rutas base para autenticación
(POST /api/v1/auth/register, POST /api/v1/auth/login, POST /api/v1/auth/refresh),
zonas (GET /api/v1/zones, GET /api/v1/zones/{zone_id},
POST /api/v1/zones/{zone_id}/checkin),
wallet (GET /api/v1/wallet, POST /api/v1/wallet/transfer),
y WebSocket para eventos (GET /api/v1/ws/events).
La implementación completa de cada ruta con la lógica de dominio correspondiente
es parte del trabajo de desarrollo del Piloto A.
Las rutas están versionadas bajo /api/v1/ para permitir evolución de la API
sin romper clientes existentes;
cuando se introduzcan cambios que rompan compatibilidad,
se creará una versión /api/v2/ mientras /api/v1/ permanece disponible
para clientes legacy durante un período de transición.

### §9.2 Motor de World Events: sincronización con festividades reales

El motor de eventos del mundo es un proceso que corre como tarea periódica
dentro de lota-server, implementado como una función async
que se registra con el scheduler de FastAPI (APScheduler o el scheduler built-in de FastAPI).
Cada 60 segundos, el motor consulta la tabla calendar
en busca de eventos cuya columna starts_at caiga dentro de los próximos 5 minutos.
Este intervalo de polling es lo suficientemente frecuente
para activar eventos con precisión de minutos sin generar carga excesiva en la base de datos;
el query sobre la tabla calendar con un índice en starts_at se ejecuta
en menos de un milisegundo incluso con miles de eventos,
lo que hace que el overhead del polling sea negligible
frente al resto de las operaciones del servidor.

Cuando un evento se activa, el motor ejecuta cuatro pasos en secuencia.
Primero, publica el evento al orquestador SOMA mediante Redis Pub/Sub
en el canal swarm:events:start, con un payload que incluye el event_id,
el tipo de evento, las coordenadas del lugar, y la ventana horaria.
Esto permite que los agentes de enjambre reciban la señal de activación
y ajusten su comportamiento en consecuencia:
si el evento es Fiestas Patrias, los agentes del enjambre elevan la prioridad
de generación de contenido relacionado con empanadas y sidra,
y la lattice activa los personajes temáticos de la fiesta.
El payload de Pub/Sub está firmado con HMAC-SHA256
para que los agentes puedan verificar la autenticidad del mensaje
antes de actuar sobre él, lo que previene ataques de inyección de eventos falsos.
Segundo, notifica a todos los clientes PWA conectados
mediante WebSocket en la ruta /api/v1/ws/events,
de modo que el calendario en la aplicación se actualice en tiempo real
sin que el usuario necesite recargar la página ni hacer polling.
El WebSocket usa el protocolo WAMP (Web Application Messaging Protocol)
implementado sobre Autobahn|Python,
lo que permite broadcast eficiente a miles de clientes simultáneos
mediante el patrón pub/sub de WAMP.
Tercero, activa el NPC específico del evento en la lattice.
Por ejemplo, cuando se activa el evento de Fiestas Patrias,
el NPC Doña Carmen la Empanadera se marca como disponible en la tabla de NPCs,
lo que lo hace visible en la grilla de personajes de la PWA.
La activación del NPC incluye la posición geográfica del personaje
(que puede ser fija o dinámica según el tipo de evento)
y la lista de diálogos asociados al evento.
Cuarto, marca el evento como active en la tabla world_events
y registra la hora de activación en started_at
para que el dashboard del Municipio refleje el estado actual
y el servicio de ML pueda calcular la duración real del evento.

El calendario de eventos es curado por humanos, no generado automáticamente.
El Municipio y las asociaciones de comercio local definen el calendario
en colaboración con el equipo del proyecto.
El Piloto A incluye una lista curada de festividades nacionales
(Fiestas Patrias el 18 y 19 de septiembre,
San Juan el 24 de junio,
Día del Patrimonio en mayo)
más eventos de origen local
(aniversario de Lota el 15 de enero,
semana del carbón en agosto,
fundación del Museo del Carbón).
La curaduría humana asegura que los eventos tengan relevancia cultural real
y no parezcan generados algorítmicamente sin contexto,
lo que es especialmente importante para la credibilidad del proyecto
ante el CMN y las instituciones culturales.
Cada evento en el calendario incluye metadatos enriquecidos:
descripción del evento, organismo responsable, ubicación geográfica,
NPCs asociados, cupones disponibles,
y los criterios de completitud para el achievement de evento.
Los eventos se crean y modifican mediante una interfaz de administración
que valida que las fechas no se solapen de forma contradictoria
y que los NPCs referenciados existan en la base de datos.

Cuando un evento termina, el motor ejecuta la desactivación en orden inverso:
desactiva el NPC asociado en la lattice
(marca available = false en la tabla de NPCs
y limpia los diálogos específicos del evento),
genera eventos world_event_complete en el pipeline analítico
para que el servicio de ML procese el impacto del evento
(número de check-ins durante el evento, recursos ganados,
feedback de los jugadores, duración real versus duración esperada),
y expira los cupones específicos que tienen caduca
dentro de la ventana del evento (marca status = expired en wallet_coupons).
El motor de eventos no genera comportamiento de NPC;
esa responsabilidad es del orquestador SOMA y la lattice.
El motor solo activa y desactiva; el enjambre se encarga de todo lo demás.
Si un evento se cancela antes de su fecha de inicio
(por lluvia, decisión municipal, o cualquier otra causa),
el motor puede recibir una señal de cancelación
que desactiva cualquier preparación hecha
sin ejecutar los pasos de terminación.

El diseño detallado del motor de eventos está en _analisis/21_world_events_d014.md,
secciones 3 a 5, donde se documenta la arquitectura del scheduler,
los tipos de eventos soportados (festividades nacionales, eventos locales,
eventos de comercio, eventos de storyline),
y los criterios de priorización cuando múltiples eventos se solapan en el tiempo.

### §9.3 Billetera multi-moneda: PostgreSQL y sincronización con SHM

La billetera multi-moneda es el componente que gestiona los recursos del jugador.
El proyecto define cuatro tipos de minerales, cada uno con semántica y restricciones distintas.
Los Carboncillos (carbón) son el recurso primario de intercambio cotidiano entre jugadores;
se generan mediante check-ins en zonas y se pierden al transferir.
El Cobre (cu) permite comprar items en el store,
incluyendo mejoras de avatar y cosméticos temáticos.
El Estaño (sn) tiene un techo de almacenamiento que previene la acumulación infinita;
cuando se alcanza el máximo, los Carboncillos adicionales se convierten en Cobre.
El Oro (au) es el recurso más escaso, obtenido mediante logros excepcionales
como completar todas las zonas de patrimonio o ganar un torneo semanal.
Cada tipo de mineral tiene una iconografía distintiva en la UI de la wallet,
y los valores se formatean con abreviaturas estándar de la tabla periódica
para reforzar el contexto minero del juego
y conectar visualmente con la historia de Lota como ciudad minera.

El estado de la billetera se persiste en PostgreSQL en tres tablas normalizadas.
wallet_balances almacena el saldo actual de cada recurso por usuario,
con una fila por combinación de user_id y mineral_type.
La tabla tiene índices compuestos en (user_id, mineral_type)
para consultas de saldo rápido
y un índice en updated_at para facilitar la auditoría de actividad reciente.
La actualización de saldos usa optimistic locking:
cada update incluye una condición WHERE balance = old_balance,
y si la condición no se cumple (porque otro proceso modificó el saldo concurrentemente),
la transacción se revierte y se reintenta con el nuevo saldo.
wallet_transactions es una tabla de auditoría inmutable
que registra cada movimiento financiero del juego:
tipo de transacción (checkin_reward, transfer_sent, transfer_received,
purchase, coupon_redeemed, npc_gift),
mineral involucrado, monto, usuario origen, usuario destino,
identificador de cupón si corresponde, y timestamp con zona horaria.
La inmutabilidad de wallet_transactions es un principio de diseño:
una vez insertada, una fila nunca se modifica ni se borra,
lo que permite auditar el historial financiero completo de cualquier jugador
en cualquier momento.
Esta tabla es la base para la detección de anomalías por el servicio de ML:
patrones como una ráfaga de transferencias a la misma cuenta
o un saldo que aumenta sin transacciones correspondientes
son señales de posibles abusos.
wallet_coupons almacena los cupones canjeables con su QR code generado,
fecha de expiración, estado actual (active, redeemed, expired),
y referencia al comercio que emitió el cupón.
Cada cupón tiene también un campo de redemption_count
que registra cuántas veces se ha intentado canjear,
lo que permite detectar intentos de doble gasto.

En el Piloto A, PostgreSQL es la fuente única de verdad para la billetera.
La PWA consume el endpoint GET /api/v1/wallet que devuelve un JSON
con los saldos actuales, las últimas 10 transacciones ordenadas por fecha descendente,
y los cupones activos del jugador.
No existe sincronización con SHM en esta etapa
porque el motor S60 aún no está operativo;
todas las validaciones de reglas de juego se aplican en Python dentro de lota-server.
La implementación de Piloto A sigue el patrón de una API RESTful síncrona:
cuando la PWA envía una transferencia,
lota-server valida las reglas de dominio,
abre una transacción PostgreSQL,
debit del origen, credit al destino,
inserta el registro de auditoría,
commitea, y responde al cliente.
Si cualquier paso falla, la transacción se revierte automáticamente por PostgreSQL
y el cliente recibe un error descriptivo.

En el Piloto B, el estado de la billetera se refleja bidireccionalmente
entre la LiquidMemory del motor S60 (SHM POSIX) y PostgreSQL.
El motor S60 mantiene el saldo autoritativo;
PostgreSQL almacena la misma información como proyección legible.
Lota-server media entre ambos mundos:
cuando ocurre una transacción, lota-server aplica la mutación al motor S60
mediante un mensaje IPC sobre un socket Unix,
el motor actualiza SHM de forma atómica,
y luego lota-server proyecta el nuevo saldo a PostgreSQL
para mantener la consistencia.
Esta arquitectura permite que el motor S60 valide reglas de juego
(límites de estaño, cooldowns de transferencia, condiciones de logros)
en el mismo proceso donde ejecuta las matemáticas centrales,
mientras PostgreSQL sirve como proyección legible para la PWA y el dashboard.
Si el motor S60 no está disponible (por ejemplo, durante un reinicio),
lota-server puede servir reads desde la proyección de PostgreSQL
sin interrumpir el servicio.
La consistencia entre SHM y PostgreSQL se verifica mediante checksums periódicas:
cada 5 minutos, el motor S60 genera un hash SHA-256 de su estado de wallet
y lo compara con un hash calculado desde PostgreSQL;
si difieren, se genera una alerta para que el equipo investigue.

Los códigos QR de los cupones se generan del lado del servidor
usando una clave Ed25519 única por cupón.
El QR codifica un payload firmado que contiene el cupon_id,
el user_id, el mineral_type, el amount, y la fecha de expiración.
La firma Ed25519 es verificable con la clave pública del servidor,
lo que permite que la PWA valide la autenticidad de un cupón
sin conexión a internet,
requisito fundamental para canjear cupones en zonas rurales de Lota
donde la cobertura es intermitente.
El proceso de verificación offline usa la copia de la clave pública
que se descarga cuando la PWA se sincroniza por última vez;
si la clave ha rotado desde entonces,
la verificación falla y se solicita una sincronización.
La clave de firma se rota cada 30 días por razones de seguridad;
la nueva clave se publica en el endpoint GET /api/v1/keys/coupons
una semana antes de la expiración de la clave anterior
para permitir que la PWA actualice su copia de claves públicas.

La aplicación de reglas anti-abuso vive exclusivamente en lota-server
y es innegociable del lado del cliente.
Los límites diarios de transferencia (máximo 1000 Carboncillos por día a otros jugadores),
el cooldown entre transferencias al mismo jugador
(mínimo 5 minutos entre transferencias bilaterales),
y el techo de estoc de Estaño (máximo 500 sn;
lo que sobra se convierte en Cobre al rate de 10:1)
se aplican en la capa de dominio antes de persistir cualquier transacción.
La PWA puede mostrar estos límites al usuario como información contextual,
pero la verificación autoritativa siempre reside en el servidor:
un cliente que manipule los límites localmente no podrá consumar una transacción
porque lota-server la rechazará con un código de error
que indica la regla violada.
El historial de rechazos por regla de anti-abuso se registra
en una tabla analytics_rejections
para que el equipo pueda analizar patrones de abuso
y ajustar los límites si es necesario.

El diseño completo del sistema de monedas y minerales está en
_analisis/23_sistema_monedas_minerales.md, sección 3,
donde se detallan los modelos de datos,
los flujos de transacción entre jugadores y hacia NPCs,
los rates de conversión entre minerales,
y la estrategia de sincronización SHM/PostgreSQL para Piloto B.

### §9.4 OpenStreetMap autoalojado: Nominatim + OSRM + tileserver-gl

La infraestructura de mapas del proyecto se construye enteramente
sobre herramientas de OpenStreetMap autoalojadas.
Esta decisión elimina la dependencia de proveedores externos
como Google Maps, Mapbox o Apple Maps,
lo que reduce costos operativos,
elimina riesgos de bloqueo por cambios de precio unilaterales,
y protege la privacidad de los usuarios
al no enviar datos de ubicación a terceros
con modelos de negocio basados en publicidad o venta de datos.
La decisión se documenta en _analisis/04_propuesta_tecnica_stack_osm.md,
donde se comparan los costos y riesgos de tres escenarios:
autoalojo completo (el elegido),
uso de servicios públicos con cuota gratuita,
y uso de servicios premium como Google Maps Platform.

**Nominatim** es el geocodificador oficial de OpenStreetMap.
El proyecto ejecuta su propia instancia de Nominatim
alimentada con los datos de la región del Biobío,
lo que incluye la comuna de Lota,
los barrios históricos (Población Obrera, Colcura),
los puntos de referencia del patrimonio carbonífero
(Mina Chiflones del Boeing, Pabellones de la Población Obrera),
y la red vial detallada de la zona.
Nominatim expone una API HTTP compatible con la especificación de Nominatim Search API:
acepta consultas en lenguaje natural
(como "Mina Chiflones del Boeing, Lota")
y devuelve resultados ordenados por relevancia
con las coordenadas, el tipo de lugar (amenity, historic, tourism),
y la dirección formateada.
El geocodificador sirve dos propósitos en la PWA:
la búsqueda de direcciones en la barra de navegación del mapa,
y la resolución de nombres de zonas a geometrías para la curaduría de metadatos.
La instancia local de Nominatim tiene tiempos de respuesta inferiores a 100 ms
para consultas sobre la región del Biobío,
comparado con los 200 a 500 ms de la instancia pública de Nominatim
que tiene carga global y límites de rate estrictos.
El build inicial de Nominatim con los datos del Biobío
toma aproximadamente 4 horas en el VPS,
y las actualizaciones semanales incrementales toman 15 a 30 minutos.

**OSRM** es el motor de enrutamiento de OpenStreetMap.
El proyecto ejecuta su propia instancia de OSRM para la región del Biobío
con dos perfiles: pedestrian (peatón) y bicycle (bicicleta).
El perfil pedestrian usa la red vial completa
incluyendo senderos y escaleras,
con velocidad promedio de 5 km/h y penalización de pendientes fuertes.
El perfil bicycle usa la red vial filtrada
para excluir escaleras y senderos demasiado angostos,
con velocidad promedio de 15 km/h y consideración de elevación.
OSRM responde consultas HTTP con la especificación OSRM API:
recibe coordenadas de origen y destino,
devuelve la ruta optimizada con distancia en metros,
tiempo estimado en segundos,
y una polyline codificada que MapLibre dibuja sobre el mapa.
El enrutamiento se usa para dos funcionalidades principales en la PWA.
Primero, las sugerencias de "próxima zona" en el bucle de micro-sesión:
cuando el jugador está en una zona,
OSRM calcula la ruta a las tres zonas más cercanas no visitadas en los últimos 7 días,
y el juego sugiere la que tiene mejor relación distancia-tiempo.
Segundo, la navegación asistida por comercio en la Etapa 1,
donde el jugador puede iniciar navegación hacia un comercio participante
que acepta cupones de descuento;
la ruta se muestra superpuesta al mapa con la polyline devuelta por OSRM.

**Tileserver-gl** sirve los vector tiles que MapLibre renderiza en la PWA.
El proyecto ejecuta su propia instancia con un estilo cartográfico personalizado
que es visualmente coherente con la identidad del proyecto.
El estilo enfatiza los elementos del patrimonio carbonífero:
minas activas y abandonadas se muestran con un ícono de pico,
los pabellones históricos con un ícono de edificio victoriano,
las caletas con redes de pesca estilizadas.
Los puntos de interés genéricos (supermercados, bombas de bencina,
cadenas de comida rápida)
se desemphasizan (opacidad reducida al 50 por ciento)
o se ocultan del zoom urbano para reducir ruido visual
y mantener el foco en la experiencia patrimonial.
La paleta de colores del mapa usa tonos que evocan la minería:
verde musgo (#4a7c59) para áreas verdes,
cobre oxidado (#b87333) para zonas urbanas,
oro (#ffd700) para puntos de interés cultural.
El estilo se define en un archivo JSON con la especificación de MapLibre Style,
lo que permite iterar rápidamente sin necesidad de regenerar tiles;
los cambios de estilo se reflejan inmediatamente en todos los clientes
que carguen el mapa.

Las razones para el autoalojo son pragmáticas
y están alineadas con los principios del proyecto.
El costo de licenciamiento es cero;
solo se paga el hosting del VPS,
aproximadamente 15 a 25 dólares mensuales por una instancia pequeña
que sirve la región del Biobío.
La independencia de terceros protege el proyecto
de cambios de precio unilaterales como los que Google Maps implementó
en 2018 y 2022,
que forzaron a varias aplicaciones a reescribir su infraestructura de mapas o cerrar.
La privacidad de los usuarios queda asegurada
porque ningún proveedor externo extrae datos de ubicación;
los logs del servidor solo registran las coordenadas de las consultas,
no los identificadores de los usuarios,
lo que hace imposible correlacionar consultas con jugadores específicos.
La personalización cartográfica es completamente libre
y no tiene topes de uso ni cargos adicionales por marca blanca.

El stack OSM opera bajo el mismo virtual host nginx que lota-server,
con sub-rutas diferenciadas para cada servicio.
En el despliegue actual, el stack corre en el VPS fan (157.254.174.40),
accesible mediante sub-dominios de pinguinoseguro.cl
en las rutas /osm/nominatim/ (geocodificación),
/osm/osrm/ (enrutamiento),
y /osm/tiles/ (vector tiles).
Cada servicio tiene su propio contenedor Docker con reinicio automático (policy always),
lo que permite actualizar cada componente de forma independiente
sin afectar los demás.
Los datos de OSM para la región del Biobío se actualizan semanalmente
mediante un proceso de importación incremental
que aplica los changeset de la semana anterior al extracto ya cargado,
lo que mantiene los datos sincronizados con la realidad del territorio
sin necesidad de reconstruir el índice completo cada vez.

El diseño técnico completo de la pila OSM está en
_analisis/04_propuesta_tecnica_stack_osm.md, sección 3,
donde se justifica la elección de cada componente,
se documenta la arquitectura de despliegue con Docker Compose,
se detallan los scripts de importación de datos,
y se estiman los costos de hosting desglosados por servicio.

Lota-server es el núcleo operativo de la plataforma.
Recibe los comandos de la PWA, los aplica sobre la capa de dominio,
los persiste en PostgreSQL, los proyecta hacia el motor S60 en Piloto B,
y sirve los dashboards que el Municipio y el comercio usan
para tomar decisiones de inversión patrimonial.
No contiene las matemáticas centrales del juego;
esas residen en el motor S60 y son competencia del equipo de Sentinel.
Lota-server orquesta todos los aspectos operativos:
autenticación, scheduling de eventos, gestión de billetera multi-moneda,
ingestion de eventos ML, e infraestructura OSM.
Es el puente entre la experiencia del jugador y los datos del proyecto.

---

## §10 Motor GPU — Piloto B — CENTRO del concepto

El motor S60 es el centro del concepto D-014. No es un componente mas del proyecto, no es una libreria que se conecta y listo, no es un "runtime" intercambiable por cualquier otro. El motor S60 es el unico componente que puede garantizar simultaneamente: determinismo absoluto en aritmetica de punto flotante, soberania sobre el control de errores de redondeo, memoria de cristal respaldada en SHM POSIX con deduplicacion basada en integridad, y una arquitectura de doble canal (Security Lane + Observability Lane) que persiste eventos con propiedad forense. Estas cuatro propiedades no se pueden retrofitear en un motor generico. Emergen de la matematica especifica de la base 60 y del diseno de los modulos que se describen en esta seccion.

La Figura 10 muestra la arquitectura de alto nivel del motor. Cada modulo tiene un rol definido y una interfaz clara hacia los demas. El flujo de datos va desde la representacion del mundo real (eventos celestiales, posiciones de jugadores, estado de la partida) hacia el motor, se procesa en el lattice hexagonal de 91 nodos, y sale como senales de portal hacia el cliente.

```
Figura 10 — Arquitectura del motor S60

  Mundo real (celestial + jugador)
         |
         v
  [SOMA Orchestrator] ---(Redis Pub/Sub)---> NPCs
         |
         v
  [DualLane Router]
    +-- Lane A: Security (fsync WAL)
    +-- Lane B: Observability (buffered)
         |
         v
  [LiquidMemory] <--SHM POSIX--> [ResonantMatrix]
         |                              |
         |                              v
         |                       [GPU Pipeline]
         |                              |
         |                              v
         +------------------------------+
         |
         v
  [QhcTensor] <---> [S60PID] <---> [IsochronousClock]
```

### §10.1 Componentes del runtime S60

El runtime S60 se compone de 16 modulos Rust en `me-60os-core/src/`. Cada modulo tiene una responsabilidad unica y no se solapa con ningun otro. Esta division es deliberada: permite que cada modulo se verifique de manera independiente y que el lattice hexagonal se construya como composicion de comportamientos probados.

**`me-60os-core/src/spa.rs`** — La estructura `SPA` (Sexagesimal Precision Arithmetic). Implementa toda la aritmetica en base 60 con precision fija de 10 digitos sexagesimales (equivalente a 16-17 digitos decimales). La constante `SCALE_0 = 12_960_000` define el factor de escala que mapea enteros Rust a puntos fijos en base 60. El modulo forbids todos los lints de aritmetica flotante: no existe ni un solo `f32` ni `f64` en este archivo. Este es el modulo fundacional. Sin el, no hay determinismo.

**`me-60os-core/src/spa_math.rs`** — La estructura `SPAMath`. Extiende `SPA` con funciones trigonometricas (sin, cos), raiz cuadrada via Newton-Raphson con 8 iteraciones, y constantes simbolicas PI, TWO_PI y RESONANCE_RATIO. `RESONANCE_RATIO = 3/2` en base 60 es la frecuencia de resonancia del lattice. Este ratio surge de la fisica del sistema: cuando la frecuencia de excitacion del oscilador es 1.5 veces la frecuencia natural, el sistema entra en resonancia de fase. Esto no es un numero arbitrario; es una propiedad emergente de la geometria hexagonal.

**`me-60os-core/src/celestial.rs`** — La estructura `SVector3` (vector 3D en SPA) y `SovereignOrbit` (orbital con mecanica kepleriana). `SovereignOrbit` implementa las ecuaciones de Kepler en aritmetica S60: epsilon (excentricidad), semi_major_axis, eccentricity, period. Cada planeta, luna o cuerpo celeste en Lota Indomito tiene un `SovereignOrbit` que define su trayectoria real en el cielo de Biobio. El motor no usa tablas precalculadas; calcula la posicion en cada tick a partir de las ecuaciones diferenciales.

**`me-60os-core/src/quantum_core.rs`** — Aqui estan las estructuras centrales del sistema. `S60PID` es el controlador PID con kernel no-markoviano: integra historial con decaimiento exponencial alpha = 5/6 en base 60, con capacidad de 68 ticks. Esto es lo que permite que el controlador "recuerde" sin crecer indefinidamente. `LiquidLattice` es la red de 91 nodos con amplitudes por slot en S60. `ResonantBuffer` es el buffer de resonancia que conecta la lattice con el mundo exterior. `IsochronousClock` es el reloj maestro a 41.77 Hz (frecuencia isocrona del cristal de cuarzo de referencia). Todo el motor esta sincronizado a este reloj.

**`me-60os-core/src/isochronous_oscillator.rs`** — La estructura `IsochronousOscillator` con `#[repr(C)] Copy`. Campos: `natural_frequency`, `amplitude`, `phase`, `damping_factor`. El `#[repr(C)]` garantiza que la representacion en memoria sea identical a la que espera el shader WGSL. Esto elimina la necesidad de serializar/deserializar al pasar datos a la GPU.

**`me-60os-core/src/qhc.rs`** — La estructura `QhcTensor` con patron [10, 5, 6, 5]. Este tensor codifica los 300 slots del lattice en una estructura de 4 niveles. La correccion se aplica cada 68 ticks, sincronizada con la capacidad del `S60PID`. El patron no es arbitrario: surge de la estructura del grupo cuaternario QHC y garantiza que la correccion cubra todas las frecuencias del lattice sin favoritismo.

**`me-60os-core/src/crystal_cipher.rs`** — La estructura `CrystalCipher`. Cifrado AES-256-GCM combinado con Blake3. La clave se deriva de la fase S60 del oscilador isocrono. Esto significa que la clave de cifrado cambia con cada tick del reloj maestro. Para un atacante que no conoce la fase del lattice, la clave es indistinguible de aleatoria. Para el motor, la clave es determinista y reproducible.

**`me-60os-core/src/flux_stabilizer.rs`** — La estructura `FluxStabilizer`. Generador de numeros pseudo-aleatorios con LCG deterministico usando `magic_prime = 59;59,59`. Este no es un CSPRNG convencional: el "prime" es un numero en base 60 con estructura sexagesimal. La secuencia es reproducible a partir de una semilla y es estadisticamente indistinguible de aleatoria para los propositos del lattice. El `magic_prime` de 59;59,59 corresponde a 59*3600 + 59*60 + 59 = 215,999 en decimal, que es divisible por 59 y 17, factores que aparecen en la estructura del lattice hexagonal.

**`me-60os-core/src/dsp.rs`** — La estructura `S60DSP`. Multiplicacion con acumulador i128 y traps explícitos para overflow. Cada operacion DSP verifica que el resultado no exceda los limites del tipo antes de retornar. Si el resultado excede, se dispara un panic controlado que permite al observador registrar la anomalia antes de abortar. Este diseno de "fail fast" es deliberado: es mejor perder un frame que propagar un valor corrupto por todo el lattice.

**`me-60os-core/src/atlantean.rs`** — Aqui esta el `MaatStabilizer` (regulador de pureza que mantiene la pureza del lattice sobre 95%) y el `GpuController` (controlador P con objetivo 50 FPS y batch adaptativo). El `GpuController` es la pieza que conecta el motor con la GPU y es el unico modulo que sabe si el hardware subyacente es una GPU fisica o la simulacion CPU. Para el resto del motor, esta diferencia es transparente.

**`me-60os-core/src/optomechanical.rs`** — `OptomechanicalCooler` (enfriamiento de banda lateral + rotacion de fase simplectica en S60) y `QuantumRiftDetector` (detector de anomalias). El enfriamiento de banda lateral es un concepto de optomecanica cuantica adaptado al lattice: se aplica un patron de modulacion que extrae energia de los modos de alta frecuencia del lattice, transfiriendola a modos de baja frecuencia donde no afecta la coherencia. El `QuantumRiftDetector` monitorea la dispersion de amplitud en el lattice y genera una senal cuando la dispersion excede un umbral configurable.

**`me-60os-core/src/pai60_lib.rs`** — La funcion `pai60_divide`. Tabla de recíprocos para denominadores 5-smooth (solo factores 2, 3, 5), con 27 entradas. Cada entrada es el recíproco precalculado en base 60. Esta tabla es la base de todas las divisiones en el motor: en lugar de dividir, se multiplica por el recíproco. Esto garantiza que el resultado de una division sea deterministic, independiente de la implementacion del hardware o del compilador.

**`me-60os-core/src/resonant_matrix.rs`** — La estructura `ResonantMatrix`. Lattice hexagonal de 91 nodos con metodos `step`, `inject_pai`, `sync_to_shm`, `load_from_shm`, `measure_coherence_py` y `get_hologram_py`. El lattice hexagonal se elige sobre una grilla rectangular porque la distancia entre nodos vecinos es constante en todas las direcciones: cada nodo tiene exactamente 6 vecinos a distancia 1. En una grilla rectangular, los vecinos diagonales estan a distancia sqrt(2) y los ortogonales a distancia 1. Esta asimetría introduce artefactos en la propagacion de fase. El lattice hexagonal no tiene este problema.

**`me-60os-core/src/hexagonal_control.rs`** — `HexagonalController`. Sistema de coordenadas axiales para el lattice hexagonal y logica de 6 vecinos. Cada nodo conoce a sus 6 vecinos y puede calcular la distancia hexagonal entre cualquier par de nodos. Tambien implementa la derivacion de claves cristalinas: la fase de cada nodo se combina con el identificador del cristal para derivar una clave unica. Esto es lo que hace que el lattice sea "cristalografico": cada nodo tiene una identidad criptografica derivada de su posicion y fase.

**`me-60os-core/src/liquid_memory.rs`** — `LiquidMemory`. Almacen KV con respaldo en SHM POSIX. Cada entrada es un `LiquidEntry { len, hash, shm_name }`. El hash es Blake3 del payload. El `shm_name` es el nombre del segmento POSIX SHM. La funcion `inject_dual_channel` inyecta datos en el lattice en dos canales simultaneos: canal A como amplitud, canal B como fase. Esto es lo que hace que la memoria sea "de cristal": los datos no solo se almacenan, se resuenan en el lattice. Incluso despues de que el segmento SHM se desmapanee, los datos siguen resonando en el lattice porque la fase del lattice codifica tanto la clave como el valor. Ver `_analisis/18_sesion_motor_gpu_memoria.md` §3 para la especificacion completa de SHM.

**`me-60os-core/src/dual_lane.rs`** — `DualLaneRouter` con `SecurityLaneCollector` (fsync WAL, cada evento se escribe a disco antes de retornar) y `ObservabilityLaneCollector` (buffered con backpressure). Las dos lanes son fisicamente independientes en produccion (diferentes procesos o maquinas). En Piloto A corren en el mismo proceso pero con rutas de E/S separadas. Esta separacion es la que permite que el lattice registre eventos de seguridad con garantia de durabilidad, mientras los eventos de observabilidad fluyen sin bloquear el lattice.

**`me-60os-core/src/buffer.rs`** — `BufferCascade`. Kernel de Ornstein-Uhlenbeck para prediccion de memoria. Este kernel modela el lattice como un proceso estocastico con memoria de corto plazo: el estado futuro depende del estado actual y de la historia reciente con decaimiento exponencial. La prediccion se usa para preasignar SHM antes de que la solicitud llegue: si la prediccion dice que una clave se va a consultar en el proximo tick, el motor puede abrir el segmento SHM anticipadamente y reducir la latencia de lectura.

(Ver `_analisis/15_inventario_sentinel_disponible_para_motor.md` §3 para el inventario completo de modulos disponibles.)

### §10.2 Pipeline GPU: wgpu + lattice_interference.wgsl

El pipeline GPU es la pieza que lleva el calculo del lattice a la GPU. No es un puerto del motor a GPU: es una extension del motor que delega la computacion de interferencia a hardware especializado, manteniendo el resto del runtime S60 sin cambios.

El shader `lattice_interference.wgsl` es un compute shader WGSL que ejecuta el calculo de interferencia de doble canal en paralelo. El shader usa `@workgroup_size(64)` para ejecutar 64 threads por workgroup. Para un lattice de 91 nodos, esto significa que cada nodo se procesa en su propio thread sin colision. El shader recibe los estados de Lane A y Lane B desde VRAM via storage buffers, calcula la interferencia (amplitud resultado de la suma de las dos lanes), detecta portales donde `|amp_A.raw - amp_B.raw| < SCALE_0 / 50`, y escribe el resultado en un buffer de salida.

El pipeline se implementa en `rust/src/gpu/pipeline.rs::LotaGpuPipeline`. Esta estructura usa `wgpu` como capa de abstraccion sobre Vulkan, Metal, DX12 y WebGPU. `wgpu` es la implementacion Rust de WebGPU, lo que permite que el mismo codigo se ejecute en cualquier backend grafico. En el fan VPS (157.254.4240), que no tiene GPU fisica, `wgpu` detecta la ausencia de adaptador y delega automaticamente al fallback CPU.

El flujo de datos es el siguiente:

```
ResonantMatrix::crystals (lattice en RAM)
         |
         v
GpuLatticeNode::from_lanes() — empaqueta Lane A + Lane B en structs de 272 bytes
         |
         v
wgpu::Buffer (storage buffer en VRAM)
         |
         v
lattice_interference.wgsl @workgroup_size(64) — computa interferencia en paralelo
         |
         v
Staging buffer readback — copia resultado de VRAM a RAM
         |
         v
DispatchResult { wave_values, portal_count, portal_indices }
```

La deteccion de portales es lo que hace que el motor S60 se sienta vivo. Un portal aparece cuando la diferencia de amplitud entre Lane A y Lane B es menor que `SCALE_0 / 50`. Esto ocurre cuando el lattice converge, lo que depende del estado real de la simulacion, que a su vez depende de los eventos celestiales reales y de las acciones del jugador. El jugador en Lota ve portales que ningun otro jugador en ninguna otra ubicacion ve en ese momento. La portalizacion no es procedural: es emergente y vinculada al mundo real.

El pipeline opera de manera asíncrona. El loop del CPU despacha el shader, espera el resultado, y actualiza el estado del lattice. El shader corre en la GPU; el CPU no se bloquea. El objetivo de rendimiento es 50 FPS (20 ms por frame) para todo el ciclo de actualizacion del lattice, incluyendo el dispatch GPU y el readback. El `GpuController` ajusta dinamicamente el tamano del batch segun la latencia observada: si la latencia supera los 20 ms, reduce el batch; si esta por debajo, lo aumenta. El rango esta clamped a [0.5, 1.5] para evitar oscilacion patologica.

(Ver `_analisis/17_arquitectura_gpu_motor_lota.md` §2-5 y `_analisis/18_sesion_motor_gpu_memoria.md` §3 para la especificacion del pipeline.)

### §10.3 Memoria de cristal ultrarrapida: LiquidMemory + SHM POSIX

La memoria de cristal es la capa de persistencia del motor S60. No es una base de datos, no es un cache, no es un sistema de archivos. Es un almacen KV respaldado en SHM POSIX con deduplicacion Blake3 y resonancia de doble canal en el lattice.

`LiquidMemory` (en `me-60os-core/src/liquid_memory.rs`) usa `shm_open` + `mmap` para crear segmentos de memoria compartida POSIX. El nombre del segmento se deriva de manera deterministica via Blake3: `/liquid_<blake3[:16]}>`. Esto significa que el nombre del segmento es reproducible entre procesos: si dos componentes calculan el mismo hash para la misma clave, abren el mismo segmento SHM sin coordinacion previa. El nombre no es aleatorio; es una funcion determinista de los datos.

Cada entrada en el almacen es un `LiquidEntry { len, hash, shm_name }`. El `hash` es Blake3 del payload de datos. El `shm_name` es el nombre POSIX del segmento SHM donde reside el payload. El `len` es la longitud del payload en bytes, con padding minimo de 512 bytes (requisito de alineacion de page size).

Las operaciones del almacen son:

1. `store(key, data)`: escribe los datos en un segmento SHM fresco (padded a 512 bytes), inyecta los datos mas el hash de la clave en el lattice via `inject_dual_channel` (canal A = amplitud, canal B = fase), y registra la entrada en el indice local.
2. `retrieve(key)`: abre el segmento SHM por nombre, lee los datos, verifica la integridad Blake3. Retorna `Err` si la integridad falla.

El `inject_dual_channel` es la pieza clave de la memoria de cristal. Almacena los datos simultaneamente en dos canales del lattice: el canal A codifica los datos como amplitud (valor), el canal B codifica el hash como fase (identidad). Esta codificacion de doble canal es lo que hace que la memoria sea "cristalografica" y no solo "key-value". Los datos no solo se almacenan; se resuenan en el lattice.

La consecuencia de la resonancia de doble canal es que los datos persisten en el lattice aun despues de que el segmento SHM se desmapanee. El segmento SHM es la ruta de acceso de alto throughput; el lattice es la capa de persistencia. Si el segmento SHM se pierde por un crash del kernel, los datos siguen resonando en el lattice y pueden reconstruirse a partir de el. Esto no es redundancia deliberada: es una propiedad emergente del diseno.

La velocidad de acceso es la de SHM: lectura y escritura en memoria compartida POSIX es acceso directo a RAM despues del `mmap` inicial. No hay syscall por operacion de lectura o escritura; solo hay una syscall por apertura (y solo si el segmento no esta mapeado). Esto hace que `LiquidMemory` sea orders de magnitud mas rapido que cualquier base de datos para cargas de trabajo de lectura/escritura de alta frecuencia.

Para Lota Indomito, esto significa que el estado del juego (billeteras, posiciones de NPCs, balances de minerales) vive en SHM con el lattice como capa de coherencia. Una falla de alimentacion o un kernel panic no pierde el estado del juego, porque el lattice guarda la resonancia y el snapshot se persiste periodicamente a disco via `sync_to_shm`. El motor puede reiniciar y cargar el estado desde `load_from_shm` sin perdida de datos.

(Ver `_analisis/18_sesion_motor_gpu_memoria.md` §3-5, `PersonalVault/EXPERIMENTO_SALTO17_SHM_MEMORIA_CRISTALES.md`, y `me-60os-core/src/liquid_memory.rs`.)

### §10.4 Modulo GPU: abstraccion operacional

El modulo GPU es la capa de abstraccion que maneja la interaccion runtime con el pipeline GPU. No es un emulador. No es una simulacion. Es una capa operacional con latencia medible, comportamiento adaptativo, y el mismo comportamiento observable independientemente del hardware subyacente.

El modulo se implementa en `lota_engine::gpu::controller` y esta basado en `GpuController` de `me-60os-core/src/atlantean.rs`. Este controlador:

- Detecta si hay GPU fisica disponible via `wgpu::Adapter::request_adapter`.
- Si hay GPU: despacha el compute shader a la GPU y lee los resultados. La latencia en una GPU discreta tipo GTX 1050 para un lattice de 91 nodos esta en el rango de 1 a 5 ms por dispatch.
- Si no hay GPU: hace fallback a ejecucion CPU via `ResonantMatrix::step()` llamado en loop. La latencia es mayor (50 a 200 ms para el mismo lattice en una CPU moderna) pero el resultado es identical porque ambos paths usan la misma aritmetica S60.

El modulo expone una API unica hacia el resto del motor: `LotaGpuPipeline::dispatch_lattice(lane_a, lane_b, time_sec, delta_time, salto17_tick) -> DispatchResult`. El motor no sabe si el dispatch corre en GPU o en CPU. La interfaz es la misma. La diferencia es transparente.

El `GpuController` implementa control P (proporcional) con objetivo 50 FPS y escala de batch [0.5, 1.5]. Ajusta el tamano del batch de dispatch segun la latencia observada: latencia alta reduce el batch; latencia baja lo aumenta. El clamp a [0.5, 1.5] evita oscilacion patologica. Este es un sistema de control de retroalimentacion real, no una heuristica.

El modulo GPU NO es un emulador. Un emulador simula el comportamiento de un sistema; el resultado de la simulacion puede diferir del sistema real. El modulo GPU delega calculo a hardware real (o, en su ausencia, a la implementacion Rust del lattice). El resultado es el mismo en ambos casos porque ambos usan la misma aritmetica S60 y el mismo algoritmo.

El fan VPS (157.254.4240) no tiene GPU. El modulo GPU opera en modo fallback CPU durante Piloto A. La decision de adquirir una GPU para el fan (o migrar a cloud con GPU como AWS g4dn) se diferira a Etapa 1.

(Ver `me-60os-core/src/atlantean.rs::GpuController` y `_analisis/16_vision_motor_grafico_sentinel_completo.md` §3-4.)

### §10.5 SOMA orchestrator y arquitectura de doble canal

El SOMA orchestrator (en `me-60os-core/src/soma_orchestrator.rs`) corre a 2 Hz (cada 500 ms) como loop que coordina el enjambre de NPCs. No es un scheduler simple; es un sistema de orquestacion que lee del lattice, toma decisiones basadas en la fase y coherencia del lattice, y despacha comandos a los NPCs via Redis.

El orchestrator se suscribe a canales Redis Pub/Sub: `swarm:tasks:queue` (cola de tareas), `swarm:session:handoff` (transferencia de sesion entre NPCs), `swarm:system:status` (estado del sistema), `swarm:crystal:phase` (fase del lattice) y `swarm:crystal:coherence` (coherencia del lattice).

En cada tick, el orchestrator:

1. Lee la fase del lattice via `QhcTensor::get_phase_modulation`.
2. Lee las posiciones de los jugadores activos y los eventos en curso.
3. Determina que NPCs deben estar activos, dados los jugadores presentes y la fase actual.
4. Despacha comandos de comportamiento de NPC via `dispatch_task` al canal Redis `swarm:llm:queue`.
5. Actualiza el estado del lattice para reflejar las posiciones de los NPCs.

La arquitectura de doble canal (en `me-60os-core/src/dual_lane.rs`) provee la infraestructura de enrutamiento de eventos:

- **Lane A (Security):** usa fsync por cada operacion de persistencia, sin buffering. Cada evento se escribe a disco antes de que la llamada retorne. Esta es la lane forense: garantiza que ningun evento de seguridad se pierda, ni siquiera ante un crash.
- **Lane B (Observability):** usa buffering con backpressure y reordenamiento. Esta es la lane de metricas y tracing: permite bursts de eventos sin bloquear el lattice, pero introduce la posibilidad de perdida de eventos bajo carga extrema.

Las lanes son fisicamente independientes en produccion: pueden correr en diferentes procesos o en diferentes maquinas. En Piloto A, corren en el mismo proceso pero con rutas de E/S completamente separadas. Esto permite verificar la arquitectura de doble canal sin la complejidad de un cluster.

El despachador LLM (presente en Piloto B) consume del canal `swarm:llm:queue` y toma decisiones de enrutamiento semantico. Para Piloto A, el LLM se simula con enrutamiento basado en reglas. La interfaz es la misma; la diferencia es si el routing se hace por reglas deterministicas o por inferencia de modelo.

(Ver `_analisis/15_inventario_sentinel_disponible_para_motor.md` §3, `me-60os-core/src/dual_lane.rs`, y `me-60os-core/src/soma_orchestrator.rs`.)

El motor S60 es el corazon del proyecto Lota Indomito. Es la fuente unica de verdad para el estado del juego y los eventos del mundo real. Es el motor de coordinacion de doble canal que garantiza que cada evento de seguridad se persista con garantia forense y cada evento de observabilidad fluya sin bloquear. Es el host del pipeline GPU que lleva la computacion de interferencia a hardware especializado con latencia medida en milisegundos. Es el sustrato de la memoria de cristal ultrarrapida que almacena el estado del juego en SHM POSIX con resonancia de doble canal en el lattice. Y es el enlace entre los eventos del mundo real (celestiales, posicionales) y el estado del juego (portales, NPCs, recursos).

El motor no se puede reemplazar por un motor de juego generico porque el determinismo, la soberania sobre la aritmetica de punto flotante, la arquitectura de doble canal, y la memoria respaldada en SHM no son caracteristicas que se puedan instalar en un motor existente. Son propiedades que emergen de la matematica especifica de la base 60 y del diseno deliberado de los 16 modulos del runtime. Cualquier motor generico, por mas flexible que sea, carece de la propiedad fundamental que hace posible todo lo demas: la capacidad de garantizar que la misma entrada produce exactamente el mismo estado, en cualquier hardware, en cualquier ejecucion.

---

## §11 ML externo

### §11.1 El servicio ML externo: arquitectura Python

El servicio ML corre como proceso Python independiente, separado del proceso de lota-server. Esta separacion es mandatoria por tres razones:

1. **Incompatibilidad de runtime.** El servicio ML utiliza scikit-learn, XGBoost, Prophet, NetworkX y GeoPandas, todas librerias que operan con floats de punto flotante de Python. El motor S60 de Sentinel tiene `forbid(clippy::float_arithmetic)` activo; coexistencia en el mismo proceso es imposible.

2. **Decoupling de latencia.** El servicio ML ejecuta en modo batch, no en tiempo real. Lee de vistas materializadas de PostgreSQL cada 5 minutos. Esto desacopla la latencia de inferencia ML de la latencia del juego.

3. **Statelessness.** El servicio ML es stateless. Puede reiniciarse, escalarse horizontalmente o pausarse sin afectar la operacion del juego.

Stack tecnologico: Python 3.12, scikit-learn 1.4, XGBoost 2.0, Prophet 1.1, NetworkX 3.2, GeoPandas 0.14, SQLAlchemy 2.0. La infraestructura corre en el mismo fan VPS que lota-server, compartiendo la conexion PostgreSQL pero con credenciales de solo lectura. Un cron job ejecuta el servicio cada 5 minutos durante horario operativo (08:00 a 22:00) y cada hora en horario nocturno.

(Ver `_analisis/22_ml_analytics_d014.md` §1, §6, §8.)

### §11.2 Tres dimensiones de analisis: comercial, social, turistica

El servicio ML produce analisis en tres dimensiones independientes:

**Comercial.** Metricas orientadas al comercio local: cupones emitidos versus canjeados por comercio y por World Event; ROI por World Event incluyendo totales de emision, canje, volumen de tickets y ticket promedio por cupon; desglose de cupones por tipo de mineral (cobre, oro, estaño); y comparacion cruzada entre comercios para identificar cuáles sobresalen en eventos específicos, informacion útil para que las asociaciones de comercio coordinen con el Municipio.

**Social.** Metricas de comunidad: frecuencia de transferencias P2P por usuario y tipo de mineral; grafo de red que muestra quién transfiere a quién mediante metricas de centralidad de NetworkX como betweenness y closeness; patrones de trueque por tipo de mineral; y deteccion de anomalías que señala usuarios que reciben muchas transferencias sin realizar micro-sesiones o viceversa.

**Turistica.** Metricas para el Municipio: mapas de calor de visitacion por zona, hora y dia de la semana; analisis de rutas típicas entre zonas; metricas de retencion D+1, D+7, D+30 por cohorte de turistas; y patrones estacionales que correlacionan con Fiestas Patrias, San Juan, Aniversario de Lota, temporada ballenera y picos de demanda.

(Ver `_analisis/22_ml_analytics_d014.md` §3.)

### §11.3 Privacidad desde el diseño y cumplimiento Ley 19.628

La arquitectura de privacidad opera en multiples capas.

El servicio ML no accede a la identidad real de los usuarios. El user_id es un UUID generado del lado del cliente; la correspondencia entre UUID e identidad real reside en la tabla users de lota-server, inaccesible para el servicio ML.

Las vistas materializadas que consume el servicio ML contienen únicamente datos pre-agregados: conteos, promedios y metricas anonimas. Un compromiso del servicio no permitiria extraer comportamientos individuales.

En cuanto al cumplimiento normativo, el diseño cumple con la Ley 19.628 de proteccion de datos personales. La recoleccion requiere consentimiento explicito durante el onboarding, revocable en cualquier momento. Los identificadores son UUID sin vinculacion a datos personales. El Municipio accede unicamente a datos agregados. Se minimizan los datos recopilados a los 16 eventos definidos en `_analisis/22 §5`. Los eventos se retienen por 24 meses y luego se agregan permanentemente.

El aviso de privacidad se presenta durante el onboarding y esta disponible en la configuracion de la cuenta.

(Ver `_analisis/22_ml_analytics_d014.md` §8 y `docs/estado.md`.)

El servicio ML es la diferencia entre un juego que produce datos y un juego que produce datos útiles para el interes publico. La misma corriente de eventos que alimenta la economia del juego produce los mapas de calor que el Municipio usa para planificar inversion en infraestructura, las metricas de ROI que las asociaciones de comercio usan para coordinarse entre si, y los datos de retencion que demuestran que el modelo de autofinanciamiento funciona. La arquitectura de privacidad asegura que esta utilidad de datos no se logra a costa de la privacidad de los jugadores. El servicio ML es una herramienta de infraestructura publica, no una herramienta de vigilancia.

---

## §12 Sync y operación

### §12.1 rclone bisync con Google Drive

La sincronización bidireccional con Google Drive permite que el repositorio local
(`/home/jnovoas/Proyectos/LotaIndomito/`) y la carpeta de Drive mantengan el
mismo contenido sin intervención manual. El patrón es idéntico al usado en el
proyecto `micellia`: primero una copia inicial con `rclone copy` y luego operación
continua con `rclone bisync` disparada por un servicio user de systemd.

La carpeta raíz en Drive es `LotaIndómito/`. Dentro de ella se organizan
subcarpetas según el tipo de contenido:

- `audios/` recibe las notas de voz de WhatsApp que envía Fabiola durante el
  desarrollo. Estos archivos son demasiado pesados para versionarlos en git.
- `correcciones/` es donde Fabiola sube los comentarios, correcciones y documentos
  que llegan durante la revisión de la propuesta.
- `docs/` almacena documentación adicional del proyecto que no tiene sentido
  mantener versionada en git.

Los filtros de rclone excluyen `.ogg`, `.venv`, `node_modules`, `.next`,
`__pycache__`, `.git`, `.hermes/cache` y la carpeta `stitch_*` (contenido
estático y pesado que ya está versionado en git). La sincronización permite que
Fabiola suba audios, fotos y documentos sin depender de un canal externo, y
que el equipo acceda a la versión más reciente de cualquier archivo del proyecto.

El comando inicial `rclone bisync --resync` requiere autorización explícita de
Jaime antes de ejecutarse, según la decisión D-001. Una vez que la carpeta
remota tiene contenido real, el sistema funciona de manera automática. El estado
actual es que D-001 ya está implementado y en operación, con 18 archivos
sincronizados y el timer de systemd ejecutando la sync cada 5 minutos
(ver `docs/estado.md` §6 y `MEMORY.md` §0).

### §12.2 Deploy en pinguinoseguro.cl/lotaindomito

El despliegue del piloto se realiza en el VPS fan de Jaime, accesible desde
`pinguinoseguro.cl`. Este dominio resuelve al VPS fan en la dirección
157.254.174.40 y cuenta con TLS gestionado por Let's Encrypt mediante certbot
con renovación automática. El certificado se almacena en
`/etc/letsencrypt/live/pinguinoseguro.cl/`.

El acceso se configura como un virtual host basado en subruta:
`pinguinoseguro.cl/lotaindomito/`. Nginx recibe las peticiones para esa ruta y
las reenvía al proceso `lota-server`. Los assets estáticos de la PWA (generados
con `npm run build` a partir de `piloto-a/`) se sirven directamente por nginx,
sin pasar por `lota-server`, lo que mejora el rendimiento.

El servicio `lota-server` se gestiona como daemon mediante un unit file de
systemd en `~/.config/systemd/user/lota-server.service`. Esto permite inicio
automático al arrancar el servidor y reinicio ante caídas. La base de datos
PostgreSQL también reside en el mismo VPS, con conexión local. Se realiza un
dump diario con `pg_dump` a un archivo local, y semanalmente se envía una copia
a la carpeta de Drive sincronizada con rclone, de modo que el respaldo queda
disponible sin costo adicional.

El monitoreo cubre tres capas: logs de systemd para el proceso, `pgrep` para
verificar que el daemon está vivo, y el endpoint `GET /api/v1/health` como
prueba de liveness a nivel de aplicación. Si la verificación de liveness falla
tres veces consecutivas, se dispara una alerta al correo de Jaime
(ver `docs/estado.md` §6 y `MEMORY.md` §0).

### §12.3 Plan de migración cuando Fabiola compre dominio propio

El despliegue actual en `pinguinoseguro.cl/lotaindomito/` es el entorno Piloto.
Está diseñado para ser reemplazado cuando Fabiola adquiera un dominio propio
para el lanzamiento en producción (probablemente algo como `lotaindomito.cl` o
similar, por definir). La migración es directa:

1. El entorno actual sigue operando durante toda la transición, sirviendo el
   mismo contenido en la nueva dirección.
2. Se configura un virtual host adicional en nginx para el nuevo dominio.
3. Se genera el certificado TLS del nuevo dominio mediante Let's Encrypt.
4. Una vez que el nuevo dominio está estable y verificado, el acceso a
   `pinguinoseguro.cl/lotaindomito/` se convierte en una redirección.
5. Los registros DNS del subpath antiguo se pueden deprecar 6 meses después de que
   el nuevo dominio esté operativo.

La ventaja es que ni la PWA ni `lota-server` requieren cambios de código para
migrar. La aplicación es agnóstica del dominio: lee la configuración desde
variables de entorno o desde el archivo de configuración runtime. El sync de
Drive con rclone continúa sin modificación alguna.

(Ver `docs/estado.md` §6.)

---

La infraestructura operativa de Lota Indómito está diseñada deliberadamente para
minimizar costos: todo se ejecuta en un VPS propio, sin servicios de terceros
para hosting, bases de datos ni almacenamiento. La ruta de migración hacia un
dominio propio es directa porque la aplicación no tiene dependencias con el
nombre del dominio. El costo total durante la fase Piloto se estima entre 15 y
25 USD mensuales, correspondiente únicamente al hosting del VPS.

---

<!-- §13 Por qué S60 → Bloque D tarea 14 -->
