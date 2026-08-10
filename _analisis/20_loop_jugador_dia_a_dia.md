# Loop del jugador día-a-día — Lota Indómito

> **Documento de diseño conceptual.**
> **Fecha:** 2026-08-10.
> **Destinatario:** INTERLOCUTOR (Jaime), para discusión antes de bajar a mecánica.
> **Encuadre:** D-014 (turista de paso + micro-sesión + eventos del cielo como anzuelo + retención D1/D7/D30). Cualquier decisión de este doc debe leerse contra `docs/decisiones.md` D-014 y `docs/concepto-juego.md` GDD.

---

## 0. Por qué este documento

El "Core Game Loop" descrito en `docs/concepto-juego.md` §2 es un **loop de encuentro** (mapa → zona → diálogo → minijuego → recompensa). Describe UNA acción mecánica, no un día del jugador.

Para validar el modelo de negocio D-014 (autofinanciamiento por comercio local), hace falta definir **el día-a-día del turista**: cuándo abre la app, qué hace, qué lo trae de vuelta, qué hace distinta a la sesión 50. Este doc cubre eso.

**Tesis central:** para un turista de paso (1-2 días en Lota), **no hay loop diario** — hay **loop de visita** (dentro de la estadía) y **loop de retorno** (después de irse). Las mecánicas clásicas de mobile tipo "racha diaria / energía que regenera" NO aplican y deben descartarse.

---

## 1. Mapa del día del turista

### 1.1 Pre-visita (D-3 → día 0)

Fuera del juego, pero apalancado por él:

- **Awareness:** alguien que ya jugó comparte su pasaporte público (URL) → efecto red orgánico.
- **Reservar la visita:** link al **Calendario del Cielo** (ver §3) → muestra qué eventos ocurren mientras el turista está en Lota.
- **Kit de viaje:** pasaporte descargable como PDF con las 8 rutas + mapa offline (funciona sin conexión en el Chiflón, el Parque, etc.).

### 1.2 Visita — Día 1 (2-4 h caminando, ~6-10 micro-sesiones)

1. **Llegada.** GPS detecta entrada a Lota → push: *"Bienvenido, Guardián. Tu pasaporte está activo. Hoy hay 3 eventos del cielo."*
2. **Primera micro-sesión.** Tutorial suave + elección de modo (Jugador / Turista / Familia).
3. **Exploración libre.** Camina por la ciudad → la app vibra al entrar a un POI (geofencing cliente, Turf.js). Cada POI = 1 micro-sesión.
4. **Pausa café/comercio.** El pasaporte sigue, no se pierde. Modo Turista es ideal aquí (sin temporizadores).
5. **Evento del cielo #1** (ver §3). Anzuelo intra-visita: urgencia real de 5-30 min.
6. **Atardecer.** Cambio de cielo → se desbloquean NPCs nocturnos (Chinchorreras, Palanquero).
7. **Antes de dormir.** Sugerencia de comercio local cercano para canjear Carboncillos. **Esto es D-014 operando.**

### 1.3 Visita — Día 2 (si se queda; sesión más corta, 1-2 h)

- Misiones pendientes del día 1: *"Te faltan 2 POIs para cerrar Ruta Fuego y Carbón."*
- Eventos matutinos puntuales (Amanecer del Minero, 07:00).
- Última compra antes de irse: gastar Carboncillos en comercio local.
- Despedida: pasaporte se cierra con stats finales + diploma descargable.

### 1.4 Post-visita (D+1 → D+30) — vector de retorno

- **D+1:** *"Tu pasaporte está al 75%. Vuelve antes del [próximo evento del cielo] para cerrarlo."*
- **D+7:** newsletter del cielo con la próxima ventana importante.
- **D+30:** *"Lota tiene 3 eventos esta temporada. ¿Vienes a completarlo?"*

El detalle de cada uno está en §4.

---

## 2. Anatomía de la micro-sesión (1-5 min)

Estructura **fija de 5 tramos**, ejecutada en 60-300 s. Es la unidad atómica de engagement.

| Tramo | Tiempo | Qué pasa | Regla dura |
|---|---|---|---|
| **Trigger** | 0-15 s | Vibración + banner: *"Estás en el Chiflón del Diablo. Toca para descubrir."* | Geofencing cliente (Turf.js). Sin texto antes del tap. |
| **Contexto** | 15-60 s | Mapa mini + avatar del personaje histórico + 2-3 frases de diálogo + audio opcional | Sin scrolls. Sin muros de texto. ≤30 palabras en pantalla. |
| **Acción** | 60-180 s | Minijuego táctil corto (QTE, hidden object, trivia) o escaneo de cámara | Pre-cargado. Cero loading entre tramos. |
| **Recompensa** | 180-240 s | +Carboncillos, +XP, animación de insignia, *"Has rescatado un fragmento del carbón."* | Siempre gana algo. Nunca "casi". |
| **Próximo** | 240-300 s | *"La próxima zona está a 320 m al sur."* Mini-mapa con ruta | Nunca terminar sin dirección. La pantalla siempre cierra con un "hacé X". |

### 2.1 Reglas del tramo Acción (clave para que entre en 1-5 min)

- **1 acción por micro-sesión.** Nunca encadenar minijuegos.
- **3 modos, 1 duración cada uno:**
  - **Jugador** = 90 s de acción dura (QTE, puzle).
  - **Turista** = 0 s (escaneo + foto, sin minijuego).
  - **Familia** = rol-asignado, todos participan en su rol (Vigía / Cronista / Fotógrafo).
- **Si pierde**, retry inmediato. Sin penalización de Carboncillos.

### 2.2 Lo que NO debe pasar en 1-5 min

- Tutoriales recurrentes (solo el primero).
- Loading screens entre tramos.
- Cualquier flujo que requiera conexión obligatoria (modo offline-first).
- Esperas por GPS fino: si el GPS está sucio, se muestra la última posición conocida + se reintenta.

---

## 3. Catálogo de eventos del cielo (anzuelo intra-visita)

Cuatro tipos, todos movidos por Sentinel S60 (sin floats, deterministas). El jugador consulta el **Calendario del Cielo** (tipo tabla de mareas) antes y durante la visita.

### 3.1 Astronómicos — predecibles, anuales

- **Salida/puesta de sol (±30 min):** desbloquea NPCs del carbón.
- **Luna llena:** el Palanquero se vuelve visible.
- **Luna nueva:** las Chinchorreras aparecen, más esquivas.
- **Equinoccios/solsticios (4 al año):** eventos especiales de 1-2 h.

### 3.2 Climáticos — ventana corta, parcialmente impredecibles

- **Niebla en el Parque:** visibilidad reducida, NPCs ocultos hasta que el jugador escanea.
- **Marejada:** eventos marinos activos en Borde Costero.
- **Lluvia:** el Chiflón del Diablo cambia de mecánica (agua, reflejo).

### 3.3 Temporales — reloj local, recurrentes

| Hora | Evento | Zona |
|---|---|---|
| 07:00 | Amanecer del Minero | El Ciego aparece en la Mina (Piques). |
| 14:00 | Hora del Trueque | NPCs en zonas de comercio. |
| 19:00 | Atardecer del Carbón | Isidora Goyenechea en el Parque. |
| 22:00 | Noche de las Chinchorreras | La Chinchorrera Mayor en la Caleta, ventana de 90 min. |

### 3.4 Raros (S60) — matemáticos, únicos

Cuando los dos carriles de la lattice convergen (`|amp_A - amp_B| < SCALE_0 / 50` en GPU, computado por `lota-server`), se abre un **portal** en alguna zona:

- Encuentro único: el Carboncillo que entrega **no se repite** nunca.
- Diploma especial *"Cazador de Portales"*.
- Es el **diferenciador central del concepto** (D-014) hecho jugable.

### 3.5 Reglas comunes a todos los eventos

- **Ventana corta** (5-30 min) → urgencia real, no FOMO cosmético.
- **Anuncio anticipado** (5-15 min antes), pero el marcador **no aparece en el mapa** hasta cerca de la hora.
- El **Calendario del Cielo SÍ los lista** con horario exacto → el turista planifica su visita alrededor.
- Cada evento tiene un **"ya pasó"** claro en el pasaporte — el jugador sabe qué se perdió, sin ansiedad retroactiva.

---

## 4. Vector de retorno

Para un turista de paso, **las mecánicas clásicas de mobile NO aplican** y deben sacarse. Lo que sí funciona:

### 4.1 Pasaporte incompleto (motor principal, orgánico)

- *"Te falta el 25% para Leyenda de la Cuenca."*
- **Diploma descargable al 100%** — objeto social (se comparte, se imprime, se pega en la pared).
- **Insignia *"Completó Lota en 1 día"*** — premium entre los completadores.

### 4.2 Calendario del Cielo público (1 año adelantado)

- Fechas concretas: equinoccios, luna llena, solsticios → *"vuelve el [fecha]"*.
- El calendario se publica en web abierta (no requiere tener la app instalada).
- Es el **anzuelo principal** del retorno.

### 4.3 Carboncillos sin gastar (D-014 directo)

- **Cupones digitales con caducidad corta** (30-60 días) en comercio local.
- Ato el retorno a un beneficio económico concreto, no a una promesa abstracta.
- Si el turista se va con Carboncillos en el bolsillo → razón directa para volver a Lota.

### 4.4 Contenido nuevo (largo plazo)

- **Temporada 2** introduce NPCs de Curanilahue → preludio de la expansión regional D-014 (Lota → Curanilahue → Lebu → Arauco → Concepción).
- Eventos ligados a festividades locales: San Juan, aniversario del carbón, etc.

### 4.5 Lo que NO incluir (antipatrones para turista de paso)

- Racha diaria / streak.
- Energía que regenera con tiempo.
- Notificación genérica *"vuelve a jugar"*.
- Cualquier mensaje que diga "hoy no jugaste" — para un turista de 1-2 días, es ruido insoportable.

---

## 5. Implicaciones para el piloto de 30 días

El piloto debe demostrar **una corrida completa del loop de visita**, no un día aislado:

| Ítem | Alcance piloto | Justificación |
|---|---|---|
| **Zonas** | 1 zona (Parque de Lota o Chiflón del Diablo) | La más rica culturalmente. Suficiente para demostrar el loop sin dispersión. |
| **Evento del cielo en vivo** | 1 evento, ejecutado durante la demo a Fabiola | Es el momento mágico de la urgencia. Sin él, no se ve el diferenciador. |
| **Calendario del Cielo** | Simulado para 30 días, con datos sintéticos de Sentinel | Demuestra que la mecánica es repetible, no un one-shot. |
| **Pasaporte público** | URL compartible, render público | Muestra efecto red. Cualquiera puede ver el pasaporte de otro sin instalar la app. |
| **Comercio local** | 1 comercio real con canje de Carboncillos (aunque sea simulado en maqueta) | Demuestra D-014 de un plumazo: el juego guía al turista al comercio. |
| **Modos** | Jugador + Turista (no Familia en piloto) | Suficiente para el slice. Familia es feature de fase 1. |

---

## 6. Preguntas abiertas (no resueltas en este doc)

Para discutir con INTERLOCUTOR antes de bajar a mecánica:

1. **¿Quién opera el Calendario del Cielo?** ¿Es generado automáticamente por Sentinel con datos astronómicos reales, o hay curación humana para eventos climáticos?
2. **¿El "modo virtual" (teleport para testing) entra en el piloto?** El GDD lo menciona para el MVP, pero si el loop depende de urgencia intra-visita, el modo virtual rompe la urgencia.
3. **¿La inscripción al evento del cielo es individual o por grupo?** Implica distinto diseño de notificaciones.
4. **¿Los portales S60 son solo en Lota o también en otras comunas?** Tiene implicaciones para la expansión regional D-014.

---

## 7. Referencias cruzadas

- **D-014** (encuadre vigente): `docs/decisiones.md`.
- **GDD completo:** `docs/concepto-juego.md` (este doc reemplaza §2 "Core Game Loop" cuando se apruebe; el resto se conserva).
- **Catálogo de NPCs:** `docs/concepto-juego.md` §3 — Isidora, El Ciego, La Chinchorrera Mayor, El Palanquero.
- **Motor GPU y portal dual-lane:** `docs/estado.md` §10 + `_analisis/17_arquitectura_gpu_motor_lota.md`.
- **Piloto B como centro del concepto:** `_analisis/16_vision_motor_grafico_sentinel_completo.md`.
