# Loop del jugador día-a-día — Lota Indómito: MMO-RA Urbano

> **Documento de diseño conceptual.**
> **Fecha:** 2026-08-10 (Actualizado: 2026-08-13 — Encuadre MMO-RA D-019).
> **Destinatario:** INTERLOCUTOR (Jaime).
> **Encuadre:** D-014 + D-016 + D-019 (MMO-RA del Mundo Real: Pokémon GO × World of Warcraft con patrullas sincronizadas en RA, diseño "Ojos Arriba" y economía viva de minerales y comercio).

---

## 0. Por qué este documento y Filosofía de Diseño

El juego fusiona la **exploración territorial en mundo real (estilo Pokémon GO)** con la **profundidad de rol, facciones, clases, cadenas de misiones y World Bosses (estilo World of Warcraft)**, potenciado por **Realidad Aumentada (RA)** y **patrullas de NPCs que se desplazan físicamente por las calles en tiempo real con sincronización extrema**.

### Pilares Fundamentales:
1. **Diseño "Ojos Arriba" (Look-Up Game Design):** El teléfono es un *Visor del Tiempo / Candil Espectral*, un artefacto para conectar con el entorno real de Lota, no una pantalla para aislarse jugando minijuegos genéricos.
2. **Patrullas Vivas en Movimiento:** Los NPCs no son marcadores estáticos. Tienen turnos de trabajo, horarios y caminan físicamente por las veredas de la comuna. El jugador debe calcular rutas a pie e interceptarlos.
3. **Caminar Hombro a Hombro en RA:** La interacción ocurre en marcha. El jugador camina junto al espectro histórico en RA mientras escucha su relato o recibe su encomienda.
4. **Sincronización Extrema:** Si varios jugadores están en la misma esquina, todos presencian al mismo personaje cruzar el mismo paso peatonal en el mismo segundo exacto.
5. **Sin mecánicas móviles artificiales:** No hay energía que recarga con tiempo ni rachas diarias forzadas. El compromiso nace de la inmersión, el pasaporte de aventuras y el calendario del cielo.

---

## 1. Mapa del día del explorador (El Viaje en Lota)

### 1.1 Pre-visita (D-3 → Día 0)

Fuera del juego, pero apalancado por él:

- **Elegir Facción y Clase:** El jugador selecciona su alineación (*Hermandad del Carbón*, *Linaje de la Luz*, o *Gremio de las Mareas*) y su especialidad (*Barretero*, *Chinchorrera*, *Cronista de Salón*, *Fogonero*).
- **Calendario del Cielo y de Patrullas:** Consulta los horarios de aparición de personajes legendarios y ventanas de World Events (astronómicos, climáticos o festividades).
- **Kit de Exploración Offline:** Descarga del mapa base y pasaporte digital para operar en zonas con sombra de señal (galerías del Chiflón, senderos densos del Parque).

### 1.2 Visita — Día 1 (2-4 h de expedición activa)

1. **Llegada a la Cuenca:** El visor se activa al entrar a Lota con el eco sordo de una campana de pique: *"Bienvenido a la Cuenca, Explorador. Las almas del carbón despiertan hoy a las 14:00."*
2. **Primera Intercepción en Calle:** El radar detecta una patrulla móvil (*El Palanquero* bajando hacia la Maestranza). El jugador camina a cortarle el paso y activa el Visor RA para acompañarlo unos metros.
3. **Inicio de Quest Chain (Cadena de Misiones):** El personaje entrega una orden de despacho histórica que requiere buscar una marca física de cantería en el Pabellón 83 y forjar un sello de carbón.
4. **Encuentro en Geositio / RA Arquitectónica:** En las ruinas del Pique Carlos, el visor superpone el palacio o la torre de extracción original en 3D sobre los cimientos reales.
5. **Alerta de World Event / Raid Urbana:** A las 19:00 (Atardecer del Carbón), suena la alarma general: *"Aparición del Galeón Fantasma en el Fuerte Viejo"*. Los jugadores convergen en el mirador para cooperar en RA.
6. **Canje en la Pulpería:** Antes de terminar la jornada, los minerales recolectados (cobre/oro) se usan en comercios locales asociados (panaderías, cafés, artesanías) reviviendo el histórico canje de fichas.

### 1.3 Visita — Día 2 (Cierre de gestas y rango)

- Cierre de cadenas de misiones de facción pendientes.
- Eventos matutinos especiales (Amanecer del Minero a las 07:00 en la boca del túnel).
- Subasta de artesanías o productos locales en minerales del juego.
- Emisión del **Pasaporte de Leyenda** con estadísticas finales, títulos honoríficos y diploma de explorador.

### 1.4 Post-visita (D+1 → D+30) — Retorno Orgánico

- **D+1:** Pasaporte compartido en redes; visualización del porcentaje de secretos descubiertos.
- **D+7:** Notificación del próximo evento de temporada (ej. Luna Llena o Día del Patrimonio).
- **D+30:** Nuevos capítulos y expansión del corredor patrimonial (Curanilahue, Lebu).

---

## 2. Anatomía del Encuentro y la Micro-Sesión en RA (1-3 min)

Estructura dinámica de interacción en campo:

| Fase | Duración | Experiencia del Jugador | Enfoque "Ojos Arriba" & RA |
|---|---|---|---|
| **1. Detección & Radar** | 0-15 s | Alerta sensorial (audio de pasos, silbato o vibración). El mapa muestra el vector de movimiento del NPC. | El jugador levanta la vista y ubica la calle física por donde viene la patrulla. |
| **2. Intercepción a pie** | 15-45 s | El jugador camina hacia el punto de cruce en la acera real. | Tensión de encuentro en tiempo real: si no te apuras, el NPC sigue su camino. |
| **3. Encuentro en Marcha (RA)** | 30-90 s | Se activa el *Visor del Tiempo*. El NPC camina a escala 1:1 por la vereda. | El jugador camina a su lado; escucha su voz espacial y recibe la misión o pista. |
| **4. Acción de Campo** | 30-60 s | Resolver el enigma observando el entorno físico (buscar un relieve, alinear una silueta, enfocar la bruma). | Cero QTEs de pulsar botones; la acción valida la agudeza visual en el mundo real. |
| **5. Recompensa & Rastro** | 15-30 s | Acuñación de minerales (Cu/Au), reputación con la facción y la dirección de la siguiente posta. | Animación de reliquia en 3D y rastro de huellas espectrales hacia el siguiente hito. |

---

## 3. Catálogo de Eventos del Mundo (World Events & Raids en RA)

Integración de eventos atmosféricos con fechas reales del calendario:

### 3.1 Eventos Diarios y Atmosféricos
- **Amanecer del Minero (07:00):** Salida de cuadrillas espectrales desde los piques hacia los pabellones.
- **Atardecer del Carbón (19:00):** Isidora Goyenechea recorre los senderos altos del Parque; secretos de alcoba y diplomacia.
- **Noche de las Chinchorreras (22:00):** Sombras en la playa preparando redes; requiere linterna o visor nocturno.
- **Niebla del Golfo / Marejada:** Eventos marinos y apariciones de naufragios en el borde costero.

### 3.2 Raids Comunitarias y World Bosses en RA
- **El Galeón Fantasma de la Bahía:** Aparición colosal en el mar frente al Fuerte Viejo. Requiere que múltiples jugadores coordinen habilidades (avistamiento, señalización, descifrado).
- **La Fisura del Pique Grande:** Derrumbe espectral en las ruinas que debe ser sellado colectivamente aportando minerales y resolviendo sellos de cantería en RA.

---

## 4. Economía Diegética: La Ficha de Pulpería y Minerales

El comercio local no es publicidad intrusiva, es parte de la historia:
- **Cobre (Cu):** Moneda de faena diaria y comercio cotidiano.
- **Oro (Au):** Obtenido en gestas de facción y eventos de cielo.
- **Estaño (Sn):** Obtenido en portales raros de convergencia matemática y pasaporte 100%.
- **La Pulpería:** Locales reales de Lota donde el jugador gasta sus minerales acuñados para canjear productos tradicionales reales (pan amasado, gastronomía marina, artesanías en carbón de piedra).

---

## 5. Alcance para el Piloto (30 Días)

| Componente | Demostración en Piloto |
|---|---|
| **Zona de Operación** | 1 corredor conectado (Chiflón del Diablo ↔ Pabellón 83 ↔ Parque de Lota). |
| **Patrullas Sincronizadas** | 2 NPCs con rutas activas en tiempo real (*El Palanquero* e *Isidora Goyenechea*). |
| **Visor RA en Marcha** | Intercepción y diálogo en movimiento a escala 1:1 con audio espacial. |
| **Facciones y Clases** | Selección de bando y perfil con bonificación pasiva visible en UI. |
| **1 Quest Chain de 3 Pasos** | Misión que inicia en calle, pasa por observación de ruina real y concluye en comercio. |
| **Comercio Local (Pulpería)** | 1 local real con canje de Ficha/Mineral vía QR. |
