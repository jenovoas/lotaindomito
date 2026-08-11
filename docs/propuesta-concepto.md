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



<!-- §3 Universo narrativo → Bloque B tarea 4 -->
