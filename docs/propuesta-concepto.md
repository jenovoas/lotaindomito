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

<!-- §8 PWA — Piloto A → Bloque C tarea 9 -->
