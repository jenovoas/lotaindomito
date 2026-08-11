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

Nombre e identificación: La Chinchorrera Mayor, figura representativa de las mujeres del borde costero de Lota que practicaban la extracción de mariscos en las rocas y transmitían orally los oficios del mar de generación en generación.

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

<!-- §7 Arquitectura general + SOLID + ISO/IEC 5055 → Bloque C tarea 8 -->
