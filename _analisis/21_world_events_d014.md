# World Events — Lota Indómito

> **Documento de diseño conceptual.**
> **Fecha:** 2026-08-10.
> **Destinatario:** INTERLOCUTOR (Jaime), para discusión antes de bajar a mecánica.
> **Encuadre:** D-014 (turismo + comercio local, motor/Sentinel como centro). Este doc extiende [`_analisis/20_loop_jugador_dia_a_dia.md`](20_loop_jugador_dia_a_dia.md) con una nueva capa: **World Events** — sincronización con eventos reales (festividades, fechas comerciales, efemérides) que tematizan el juego entero y coordinan flujos turísticos hacia el comercio local.
> **Referencia mecánica:** *World Events* de World of Warcraft (Hallow's End, Lunar Festival, Love is in the Air, Darkmoon Faire, Noblegarden).

---

## 0. Tesis central

Para que D-014 (autofinanciamiento por comercio local) funcione, el juego debe **coordinar flujos turísticos hacia el comercio en fechas reales**, no solo "tener carboncillos canjeables". El World Event es el mecanismo: durante una festividad o fecha significativa, el juego se viste con la temática, aparecen **NPCs exclusivas que caminan por el mapa**, se ofrecen **misiones temáticas con recompensa concreta** (bono de descuento en restaurant, café, completo, etc.), y el turista debe **salir del teléfono y entrar al comercio real** para completar la cadena. Las recompensas son **exclusivas y caducas** — si el turista no las obtiene durante el evento, no vuelven.

---

## 1. World Events vs eventos del cielo

`20_loop_jugador_dia_a_dia.md` §3 define el **Calendario del Cielo** con cuatro tipos de eventos: astronómicos, climáticos, temporales, raros (S60). Esos eventos son **driver atmosférico** — modifican cuándo y dónde aparecen los NPCs del enjambre SOMA. Son la capa base.

Los **World Events** son una capa encima:

| Capa | Driver | Efecto | Duración |
|---|---|---|---|
| Eventos del cielo | Cielo, hora, clima, lattice S60 | Modulan presencia y posición de NPCs en zonas | Minutos a horas |
| **World Event** | **Fecha real del calendario** | **Tematiza el juego entero, NPCs exclusivas, misiones con comercio real** | **1-3 días (turista de paso)** |

Los World Events **usan** el calendario del cielo como infraestructura de anuncios, pero **no son conducidos por él**.

---

## 2. Traducción WoW → Lota Indómito

| World of Warcraft | Lota Indómito |
|---|---|
| Hallow's End (Halloween) | Fiestas Patrias (18-19 sept): gastronomía típica, empanadas, vino. Temática carbón + gastronomía. |
| Lunar Festival (Año Nuevo lunar) | Aniversario de Lota: NPC fundadora aparece, pasaporte dorado al completar ruta. |
| Love is in the Air | San Juan (24 jun): el Ciego de la Mina enciende fogatas en el Chiflón. |
| Darkmoon Faire (feria mensual) | Calendario del Cielo: feria artesanal flotante en zona rotativa, una vez al mes. |
| Noblegarden (Pascua) | Día del Patrimonio (último dom de mayo): ruta completa abierta, doble XP, NPC histórico extra. |
| Recompensas exclusivas (mascotas, mounts, títulos) | Insignia única del evento + cupón real en comercio asociado + título de avatar. |
| Duración 1-2 semanas | Duración 1-3 días (cabida en una visita de turista de paso). |

---

## 3. Catálogo de eventos reales

### 3.1 Nacionales / regionales con fecha fija (verificables)

- **Fiestas Patrias** (18-19 sept). Nacional.
- **Día del Patrimonio** (último domingo de mayo). Nacional.
- **San Juan** (24 de junio). Especial en zona minera.
- **Temporada de ballenas** (julio-octubre, costa del Biobío). Regional.
- **Año Nuevo** (1 enero). Bajo turismo en Lota — evaluar si activar evento o no.

### 3.2 Locales de Lota (categorías — fechas exactas requieren input de cliente/Municipio)

- Aniversario de Lota (fundación).
- Semana de la industria del carbón.
- Festividades costumbristas del borde costero.
- Fiesta patronal de la parroquia local.
- Apertura de temporada de caletas / sardina / mariscos.

### 3.3 Comerciales (curados por cliente / Municipio / comercio local)

- Temporadas de productos: pan de mina, mariscos, sardina, empanadas.
- Temporada alta / baja de turismo (verano, invierno, semana santa).
- Aperturas, aniversarios, efemérides de locales asociados.
- Eventos deportivos / culturales: regatas, festivales, exposiciones en el Parque.

**Decisión:** las fechas nacionales son **duras** (Sentinel o calendario hardcodeado). Las locales y comerciales son **blandas** (curación humana vía un mini-CMS o carga manual).

---

## 4. Mecánica de World Event (5 componentes)

Todos juntos — no se trata solo de poner un evento en el calendario.

### 4.1 Trigger por fecha real

Sentinel o un calendario curado detecta la fecha del evento → activa el World Event 24-48 h antes. Push automático a jugadores suscritos a la zona.

### 4.2 Temática del juego

- **NPCs exclusivas** del evento (ej. "Doña Carmen, la Empanadera" en Fiestas Patrias). Visten con la temática.
- **Diálogos contextualizados** en todas las micro-sesiones (los NPCs fijos hablan del evento).
- **Decoraciones de mapa**: banderines, fogatas, motivos visuales (esto es para UI; en RA real es para fase 2).
- **Audio ambiental temático**: música acorde al evento.

### 4.3 Misiones exclusivas (3-5 por evento)

**Misiones temáticas con REQUIRE físico al comercio local** — este es el corazón de D-014. El jugador **debe salir del teléfono y entrar al comercio real** para completar la cadena.

**Ejemplos concretos:**

- **Fiestas Patrias** — *"El Sabor del Carbón"*: visita 3 locales con comida típica asociada, escanea el QR en cada uno → insignia *"Catador Patrio"* + 200 Carboncillos + cupón real (ej. 10% off en Restaurant X).
- **San Juan** — *"Fogatas del Ciego"*: encuentra al Ciego de la Mina durante la fogata nocturna en el Chiflón + lleva una foto del fuego al comercio asociado → insignia *"Vigía de San Juan"* + cupón real.
- **Día del Patrimonio** — *"Memoria Viva"*: completa la ruta completa + escanea 2 QRs en sitios patrimoniales → insignia *"Guardián del Patrimonio"* + cupón en café asociado.
- **Temporada de ballenas** — *"Vigía Costero"*: avista ballenas desde el mirador + foto del avistamiento + escaneo en restaurante de costa asociado → insignia *"Vigía del Golfo"* + cupón en restaurant de mariscos.
- **Aniversario de Lota** — *"Pasaporte Fundador"*: completa 5 POIs + visita comercio asociado → insignia única *"Fundador 2026"* + cupón en café.

**Diseño clave:** cada misión **conecta con 1-2 comercios reales** específicos. El comercio es **parte de la cadena de progresión**, no un destino opcional.

### 4.4 Recompensas exclusivas con caducidad real

| Tipo | Mecánica |
|---|---|
| **Insignia única** | No se obtiene después del evento. FOMO legítimo, estilo WoW. Se conserva en el pasaporte histórico. |
| **Título de avatar** | Visible en perfil y al chatear. |
| **Cupón real en comercio** | QR scaneable en el local. Descuento en restaurant, café, completo, o producto/regalo. Caducidad: 24-72 h tras el evento. |
| **Minerales bonus** | Cobre (10-100) o, rara vez, oro. Estándar, no exclusivo. |

**Anti-fraude:** cada cupón es único por jugador (ID + QR firmado). Se valida una sola vez en el comercio (escaneo del QR por el local). Si no se usa, expira.

### 4.5 Anuncio cross-channel

- **Calendario del Cielo público** (web abierta): lista el World Event con fecha, temática, NPCs exclusivas, comercios participantes.
- **Push 24-48 h antes**: "Mañana empieza Fiestas Patrias en Lota. Doña Carmen te espera."
- **Push 5-15 min antes** de cada ventana de misión.
- **Visible en el pasaporte**: el jugador ve qué eventos tiene activos y cuáles se perdió.
- **Afiche QR en el comercio asociado**: el local exhibe un afiche del evento con QR para que turistas no-jugadores descubran el juego.

---

## 5. NPCs que caminan por el mapa

Detalle explícito: las **NPCs exclusivas del World Event no son fijas**. Caminan.

### 5.1 Modelo de movimiento

Opciones (a decidir):

1. **Patrón fijo predefinido.** Ruta hardcodeada por zona. Simple, predecible, el jugador puede planificar. Bajo costo de cómputo.
2. **Patrón Sentinel S60 (lattice).** Los NPCs se mueven según reglas del lattice S60 — coherente con el enjambre SOMA del concepto D-014. Convergencia de carriles A y B modula la posición. Determinista, replicable, alineado con la matemática soberana del proyecto.
3. **Random walk dentro de zona.** Más "vivo" pero impredecible. Dificulta la caza del turista.
4. **Híbrido:** ruta base + perturbación S60.

**Recomendación conceptual:** opción 2 (S60-driven) — coherente con el resto del concepto. Pero en el piloto de 30 días se puede arrancar con opción 1 (ruta fija) y migrar a S60 en fase 1.

### 5.2 Zona de movimiento

Cada NPC exclusiva tiene una **zona de movimiento** (un polígono) — no deambula por toda la comuna. La zona se anuncia en el Calendario del Cielo y se muestra como un área translúcida en el mapa.

### 5.3 Caza por geolocalización

El turista **caza** al NPC caminando hacia su posición actual (geofencing cliente, Turf.js). El NPC se mueve mientras tanto. Si la distancia se cierra a <20 m, dispara el encuentro y la misión asociada.

**Tensión intencional:** el NPC no espera. Esto convierte la caza en una **micro-carrera** de 1-5 min dentro del loop de visita — encaja con la anatomía de micro-sesión definida en `20_loop_jugador_dia_a_dia.md` §2.3.

### 5.4 NPCs fijas vs NPCs móviles

| Tipo | Comportamiento |
|---|---|
| NPCs fijas del juego (Isidora, Ciego, Chinchorrera, Palanquero) | Están en sus POIs. Mismas reglas que en el GDD actual. |
| **NPCs exclusivas de World Event** | **Caminan por una zona predefinida.** Aparecen solo durante el evento. Desaparecen al cerrar el evento. |

La capa de World Event **no reemplaza** las NPCs fijas — **se suma** sobre ellas.

---

## 6. Recompensas concretas — el canal comercio real

La recompensa principal del World Event es el **cupón real en comercio asociado**. Tipos concretos:

| Tipo de comercio | Ejemplo de recompensa | Mecánica |
|---|---|---|
| **Restaurant** | 10-15% off en almuerzo / cena / menú del día | Cupón QR, se escanea en el local al pagar |
| **Café** | Café gratis con compra / 2x1 en café del día | Cupón QR |
| **Completo** (hot dog chileno) | Completo + bebida a precio único / 2x1 | Cupón QR |
| Panadería | Pan de mina de regalo con compra >$X | Cupón QR |
| Artesanía local | 10% off en producto seleccionado | Cupón QR |
| Librería / souvenir | Postales + descuento | Cupón QR |

**Decisión abierta:** la categoría puede extenderse a "cosas así" — cualquier comercio asociado que se inscriba al World Event puede proponer su recompensa. El CMS o el contrato con cliente/Municipio define la lista.

### 6.1 Geocerca vs cupón digital libre

| Opción | Mecánica | Pro | Contra |
|---|---|---|---|
| **Geocerca + escaneo in-situ** | El cupón se activa solo si el jugador está en el local; se escanea un QR del comercio | Anti-fraude fuerte, garantiza tráfico físico | Más complejo, requiere escaneo del local |
| **Cupón digital libre** | El cupón es un código que se muestra en el celular y se usa en caja sin geocerca | Simple, ya validado por muchos jugadores | Más fácil de compartir / revender |

**Recomendación:** empezar con cupón digital libre en el piloto, evolucionar a geocerca en fase 1.

### 6.2 Caducidad del cupón

| Opción | Pro | Contra |
|---|---|---|
| **24-72 h tras el evento** | Urgencia WoW-like, convierte el cupón en driver de retorno rápido | Puede ser demasiado rígido para turista de paso |
| **Hasta fin de mes** | Más flexible | Menor urgencia |
| **30-60 días tras obtención** | Balance | Comprometer si se obtiene tarde |

**Recomendación:** 30-60 días tras obtención, balance para turista de paso.

### 6.3 Inscripción del comercio al World Event

| Opción | Pro | Contra |
|---|---|---|
| **Inscripción abierta por formulario** | Escalable, el comercio se auto-selecciona | Requiere backend, validación |
| **Curación por cliente/Municipio** | Control de calidad, alianza estratégica | Escala limitada |
| **Combo: abierta + curada** | Lo mejor de ambos | Más complejo |

**Recomendación:** curación para el piloto; abierta con validación para fase 1.

---

## 7. Cómo refuerza D-014

| Antes (sin World Events) | Después (con World Events) |
|---|---|
| Carboncillos canjeables en comercio local (pasivo) | Misiones que **requieren** ir al comercio local |
| Comercio recibe jugadores "de a uno" cuando canjean | Comercio recibe **oleadas coordinadas** en fechas pico |
| Sin incentivo para que el comercio se sume activamente | Comercio se inscribe como "local del evento" → visibilidad en la app |
| D-014 funciona si el turista casualmente entra a un local | D-014 funciona **planificadamente**, con fechas que el turista puede reservar alrededor |
| El juego es un "GPS cultural" genérico | El juego es un **coordinador de flujos turísticos** en fechas reales |

**El cambio cualitativo:** el comercio local deja de ser un **destino opcional** y pasa a ser **parte del evento mismo**. El World Event **coordina oferta (comercio) con demanda (turista)** en fechas sincronizadas.

---

## 8. Decisiones de diseño abiertas

Antes de bajar a mecánica o persistir, estas decisiones estructuran todo lo demás:

1. **¿Quién opera el calendario de World Events?**
   - Sentinel automático con efemérides hardcodeadas (solo fechas nacionales).
   - Curación humana (cliente/Municipio cargan fechas locales y comerciales).
   - Mixto: nacionales automáticas + locales/comerciales curadas. *(recomendado)*

2. **¿Los World Events son solo en Lota o también en Curanilahue / Lebu / Arauco / Concepción desde el día 1?**
   - Implicación fuerte para la expansión regional D-014.
   - Empezar en Lota y expandir tras validar fase 1.

3. **¿Geocerca o cupón digital libre?**
   - Libre para piloto, geocerca para fase 1. *(recomendado)*

4. **¿Caducidad rígida estilo WoW (no se obtiene después) o flexible?**
   - Insignia/cupón exclusivos → no se obtienen después (estilo WoW).
   - Carboncillos → transferibles.

5. **¿Los NPCs que caminan son del World Event, o todos los NPCs del juego?**
   - Recomendación: solo del World Event en piloto; expansión a NPCs fijas en fase 1 (enjambre SOMA móvil).

6. **¿Mecánica de movimiento: ruta fija o S60-driven?**
   - Ruta fija en piloto; S60 en fase 1 (cuando el motor tenga `upload_and_dispatch` para NPCs móviles).

7. **¿Inscripción del comercio al evento: abierta o curada?**
   - Curada para piloto; abierta con validación para fase 1. *(recomendado)*

8. **¿El piloto de 30 días incluye 1 World Event o ninguno?**
   - Sí, 1 World Event mínimo para el piloto (ver §9).

---

## 9. Implicaciones para el piloto de 30 días

El piloto debería demostrar **un World Event mínimo**, no el sistema completo.

### 9.1 World Event del piloto: ejemplo concreto

**Selección:** uno de los eventos reales más próximos al deadline del piloto. Opciones razonables:

- **Día del Patrimonio** (si la fecha cae dentro de los 30 días).
- **Aniversario de Lota** (si la fecha cae dentro de los 30 días).
- Una **festividad local** que cliente/Municipio curen (ej. apertura de temporada, semana del carbón).

**Si ninguno cae en los 30 días:** demo simulada con datos sintéticos (igual que el Calendario del Cielo se simula para 30 días en `20_loop_jugador_dia_a_dia.md` §5).

### 9.2 Componentes del World Event del piloto

| Componente | Alcance del piloto |
|---|---|
| **1 NPC exclusiva** | Camina por una zona predefinida (ruta fija, no S60). Vestida con la temática. |
| **1 misión temática** | Cadena que requiera escaneo QR en 1 comercio real asociado. |
| **1 insignia exclusiva** | No obtenible después. Visible en el pasaporte. |
| **1 cupón real** | Cupón digital (no geocerca). Descuento en 1 comercio local real. |
| **Calendario del Cielo** | World Event listado, con fecha, zona, NPC, comercio asociado. |
| **Decoración de mapa** | Mínima: 1-2 elementos visuales de la temática (banderines, fogatas). |
| **Audio ambiental** | Opcional — música acorde al evento. |

### 9.3 Por qué esto vale para la postulación al fondo

El pitch a cliente / al fondo pasa de *"el juego detecta el cielo"* a *"el juego se sincroniza con la realidad, coordina flujos turísticos hacia el comercio en fechas reales, y el World Event es la prueba de que el modelo D-014 escala a nivel de comuna"*. Esa es la historia de portfolio que vale [monto retirado] — y el piloto lo demuestra en una demo de 5 minutos.

---

## 10. Referencias cruzadas

- **Loop de visita + retorno + micro-sesión:** [`_analisis/20_loop_jugador_dia_a_dia.md`](20_loop_jugador_dia_a_dia.md) — el World Event encaja en el loop como anzuelo de retorno (D+30) y como pico de engagement intra-visita.
- **Calendario del Cielo:** `20_loop_jugador_dia_a_dia.md` §3 — infraestructura de anuncios que el World Event reutiliza.
- **GDD §2 Core Game Loop:** `docs/concepto-juego.md` — el World Event debe agregarse como §2.6 o subsección del catálogo de eventos.
- **D-014 corregida:** `docs/decisiones.md` — encuadre vigente; el World Event es el mecanismo concreto que activa D-014.
- **Enjambre SOMA:** `MEMORY.md` §"Estado del motor GPU" + D-014 — los NPCs móviles del World Event son una instancia visible del enjambre SOMA.
- **Motor GPU + lattice:** `_analisis/17_arquitectura_gpu_motor_lota.md` + `docs/estado.md` §10 — la mecánica de movimiento S60 (cuando se implemente) se integra con el pipeline existente.
