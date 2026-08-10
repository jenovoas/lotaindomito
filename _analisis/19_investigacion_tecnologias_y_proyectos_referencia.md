# Investigación: tecnologías y proyectos de referencia — Lota Indómito

**Fecha:** 2026-08-10
**Autor:** Qwen 3.8 (investigación web directa)
**Para:** INTERLOCUTOR (Jaime)
**Objetivo:** panorama REAL y ACTUAL de tecnologías y proyectos que resuelven problemas análogos a los de Lota Indómito, para mejorar la propuesta y el diseño técnico.
**Cómo leerlo:** cada sección mapea un pilar del concepto, describe proyectos/tecnologías reales con fuentes, y cierra con "qué aprender para Lota". No es una lista genérica; todo lo de abajo existe y está citado.

> Relación con el concepto (D-014): evento real → NPCs del enjambre SOMA → caza en el teléfono → encuentro RA que reconstruye la historia real de Lota; dos niveles de dispositivo (teléfono + gafas); etapa 2 de comercio; expansión regional.

---

## 1. Juegos geolocalizados (LBG) — los grandes y cómo están construidos

### 1.1 Pokémon GO (Niantic) — arquitectura de referencia obligada

Es el LBG de referencia y su arquitectura está documentada públicamente (Google Cloud blog + deep-dives de la comunidad).

**Stack de servidor:**
- **Google Kubernetes Engine (GKE):** todos los microservicios. Escaló de 1 cluster a ~15.000 nodos.
- **Cloud Spanner:** base de datos fuertemente consistente para jugador + mapa + Pokémon. ~5.000 nodos Spanner en cualquier momento. Migraron desde Datastore (NoSQL) a Spanner por límites de escala.
- **Spatial Query Backend:** el servicio clave. Cache *shardeada por ubicación*. Decide qué Pokémon se muestra, qué gimnasios/PokéStops hay alrededor, la zona horaria — todo lo location-based. "El frontend maneja al jugador; el Spatial Query Backend maneja el mapa."
- **Redis on Google Cloud:** para la arquitectura de Raids (stateless, cache centralizado).
- **NGINX** como reverse-proxy delante de los servicios.
- **Bigtable + Pub/Sub + BigQuery:** logging y pipeline de análisis.

**Lo más importante para Lota — el determinismo del servidor:**
> "Everything on our servers is deterministic. Therefore, even if multiple players are on different machines, but in the same physical location, all the inputs would be the same and the same Pokémon would be returned to both users."

Esto es *exactamente* la filosofía de Jaime (matemática exacta, reproducible). Niantic llega al determinismo con caching + timing sincronizado de eventos; Jaime llega con matemática S60 sin floats. Es una validación de que el enfoque determinista es el correcto para un mundo compartido.

**S2 Cells — el índice espacial de Pokémon GO:**
Pokémon GO está construido sobre **S2 Geometry** (Google). Divide la esfera terrestre en celdas indexadas por un entero de 64 bits, con 31 niveles. Usos confirmados por nivel:
| Nivel S2 | Uso en Pokémon GO | Tamaño aprox. |
|---|---|---|
| L10 | Ubicación de captura, clima | 81 km² |
| L13 | Distribución de EX Raids | 5 km² |
| L14 | Cantidad de gimnasios | 0.32 km² |
| L15 | Bloquear zonas militares | 0.079 km² |
| L16 | Render del mapa (radio 500 m) | 0.019 km² |
| L17 | Colocación de PokéStops | 4.948 m² |
| L20 | **Spawns** (siempre en el centro de la celda L20) | 77 m² |

**Qué aprender para Lota:**
- La separación **frontend (jugador) / spatial query backend (mapa)** es el patrón a replicar en `lota-server`.
- Un **índice espacial jerárquico** (S2 o H3) para zonas/spawns/NPCs, no fuerza bruta.
- **Servidor determinista y autoritativo**: el estado del NPC y del mundo vive en el servidor; el teléfono solo visualiza. Calza con Sentinel.
- Spawns anclados a celdas (no coordenadas arbitrarias) → reproducibles y cacheables.

*Fuentes:* cloud.google.com/blog (How Pokémon GO scales), fullstackexpress.io/p/pokemon-go-architecture, pokemongohub.net (S2 cells guide + backend deep dive).

### 1.2 Otros LBG de Niantic (mismo motor, distintas mecánicas)

- **Ingress / Ingress Prime:** el origen. Portales en lugares de interés histórico/cultural, dos facciones, control de territorio. **Lección clave:** los jugadores *descubren* lugares de su propio barrio ("el parque por el que pasaste mil veces"). Los Portals los pone la comunidad (hoy **Niantic Wayfarer**), y los escaneos alimentan el mapa 3D de **Lightship VPS**. Es el precedente directo de "el patrimonio como tablero".
- **Monster Hunter Now (2023, con Capcom):** el mundo real se divide en **biomas** que spawnean monstruos distintos; combates de **75 segundos** (diseñado para jugar de pie en la calle); el **Palico** recolecta recursos y marca monstruos *con la app cerrada* (juego pasivo/asíncrono); **Paintball** para "guardar" un monstrón y cazarlo después desde casa. 15M descargas.
- **Pikmin Bloom / Peridot:** el primero premia *caminar* (Change-of-Distance); el segundo es mascota virtual con Search-and-Find.

**Qué aprender para Lota:**
- **Biomas/zonas temáticas** que cambian qué aparece → mapea directo a las zonas patrimoniales de Lota (mina, costa, pabellones, parque).
- **Combate/interacción corta** (75 s) para juego en la calle → las misiones de Lota deben ser breves y de una mano.
- **Modo pasivo/asíncrono** (algo progresa con la app cerrada) → idea para etapa 2.
- **Contenido puesto por la comunidad/curadores** (Wayfarer) → Fabiola + municipio como curadores de zonas.

### 1.3 LBG fuera de Niantic

- **Dragon Quest Walk (Square Enix + Colopl, 2019):** usa **Google Maps Platform Gaming**. Datos clave: pidieron a Google *evitar estaciones y lugares muy concurridos* para los spawns (seguridad), y usaron la **Playable Locations API** (un "score" de qué tan conocido/concurrido es un lugar) para dirigir jugadores a destinos. 10M descargas en 2 meses.
  - **Lección:** la *calidad del dato de ubicaciones* es crítica; y hay que diseñar para **no** crear aglomeraciones peligrosas. Para Lota: dirigir el flujo a zonas patrimoniales *y* al comercio, evitando puntos peligrosos.

### 1.4 Patrones de diseño LBG (taxonomía académica)

Un paper de SBGames 2024 analizó los LBG de Niantic (Peridot, Monster Hunter Now, Pikmin Bloom, Pokémon GO, Ingress) y clasificó sus mecánicas:
- **P1 Search-and-Find** y **P4 Change-of-Distance** son las dos mecánicas dominantes.
- **P2 Follow-the-Path** casi no aparece (solo rutas recientes de Pokémon GO).
- **P3 Chase-and-Catch** está *ausente* en todos.
- Clasifican los objetos en **VO** (virtuales puros), **VOR** (virtuales con coordenadas reales, solo logísticos) y **RO** (objetos reales donde la ubicación impacta el juego — ej. clima real, escanear un lugar).
- Conclusión del paper: hay **poca affordance locacional real (RO)** en los LBG actuales — es un espacio abierto de diseño.

**Qué aprender para Lota:** la caza del NPC es **Search-and-Find** (P1), y el recorrer zonas es **Change-of-Distance** (P4). Pero Lota puede ser de los pocos que use **RO de verdad**: el *cielo real* y la *hora real* como objetos reales que dirigen el juego. Eso es el diferenciador, y el paper confirma que casi nadie lo hace.

*Fuente:* sol.sbc.org.br (SBGames 2024, "Identifying patterns and affordances in location-based games: The practices of Niantic").

### 1.5 Juegos de caminar narrativos (sin pantalla)

- **Zombies, Run! (Six to Start, 2012, 10+ años, 2M+ jugadores):** juego de correr + aventura de **audio**. Lecciones de Adrian Hon (co-creador):
  - **Audio en primera persona** como salida principal, mezclado con la música del jugador — porque corriendo no puedes mirar la pantalla.
  - **La velocidad del jugador como input**, los audífonos como output. Recolectas supplies automáticamente sin tocar nada.
  - **GPS no es suficientemente preciso/rápido** para dirigirte a puntos exactos con seguridad → por eso el juego es de "corre y escucha", no de "ve a esta coordenada exacta".
  - **Robustez:** un crash durante una corrida arruina una hora de esfuerzo; la app corre con la pantalla apagada (audio + GPS + música + red).
  - **Ubicación exacta es difícil:** "no podíamos dirigir a la gente a ubicaciones precisas de forma fiable".

**Qué aprender para Lota:**
- Para la **caza del NPC**, no depender solo de "llega a esta coordenada" (GPS urbano falla 5-15 m). Combinar GPS con **audio espacial** y feedback "frío/caliente".
- **Audio narrativo** para los encuentros con los personajes históricos (Isidora, El Ciego de la Mina) — encaja con los oficios y relatos orales de Lota, y funciona con la pantalla apagada.
- Diseñar para **pantalla apagada** en los tramos de caminata.

*Fuentes:* blog.zombiesrungame.com (Ten Years of Zombies, Run!), mssv.net (Adrian Hon, wearable gaming), medium.com/@adrianhon.

---

## 2. Indexación geoespacial — S2 vs H3 vs Geohash vs R-tree

Para zonas, NPCs, spawns y geofencing. Tres sistemas de grilla global + índices locales:

| Sistema | Forma celda | Proyección | Vecinos | Quién lo usa |
|---|---|---|---|---|
| **S2** (Google) | cuadrilátero esférico | cubo desplegado + curva de Hilbert | 4 u 8 (ambiguo) | **Pokémon GO**, Google Maps |
| **H3** (Uber) | hexágono (12 pentágonos) | icosaedro | **6 exactos** | Uber, Overture Maps |
| **Geohash** | rectángulo | equirectangular + curva Z | 8 (4 borde + 4 esquina) | Redis GEO, Elasticsearch |

**Claves:**
- **S2:** subdivisión *exacta* (una celda hija está siempre contenida en la padre), 31 niveles, ideal para contención de polígonos (`S2RegionCoverer`) y distribución global uniforme. Es lo que usa Niantic.
- **H3:** hexágonos → **todos los vecinos equidistan del centro** y `gridDisk(cell, k)` devuelve el anillo completo en una llamada. Mejor para análisis de vecinos y visualización. 16 resoluciones. La subdivisión NO es estrictamente contenida.
- **Geohash:** el más simple, nativo en Redis/Elasticsearch, pero con *bugs de frontera* (celdas vecinas geográficamente pueden no compartir prefijo).
- **R-tree / R\*-tree (`rstar` en Rust):** índice local (no global) para nearest-neighbor y point-in-polygon sobre geometrías ya cargadas. Es lo que ya está en el `Cargo.toml` de Lota.

**Recomendación para Lota:**
- **`rstar` (R-tree)** para el geofencing y nearest-neighbor de NPCs/zonas ya cargadas (ya lo tienes como dependencia).
- Si quieres una grilla global para spawns/NPCs reproducibles (estilo Pokémon GO), **H3** es el mejor default moderno (vecinos limpios, sin bugs de frontera, hay crate Rust `h3`); **S2** si quieres replicar el patrón exacto de Niantic o indexar polígonos arbitrarios.
- **PostGIS** (ya en el stack de la fase 1) soporta ambos como funciones.

*Fuentes:* h3geo.org, github.com/uber/h3, ky-gis.com (H3 vs Geohash vs S2), benfeifke.com, taylor-amarel.com, docs.cloud.google.com (grid systems).

---

## 3. AR en sitio — geo-anclaje y localización (el pilar del encuentro)

El problema central del encuentro RA: **anclar contenido a un lugar real con precisión** y que persista. Hay cuatro familias.

### 3.1 Niantic Lightship VPS (Visual Positioning System)
- **Qué es:** servicio en la nube que localiza el dispositivo con **precisión de centímetros en segundos**, comparando lo que ve la cámara contra el **Niantic Map** (mapa 3D del mundo, petabytes de datos, construido con escaneos AR de usuarios).
- **Cómo funciona:** el dispositivo manda un frame de cámara + GPS aproximado; el servicio devuelve la **pose 6DOF** (posición + orientación). Contenido anclado persiste entre sesiones y entre usuarios.
- **ACE (Accelerated Coordinate Encoding):** el relocalizador de Niantic. Compila una escena en **4 MB de pesos de un MLP en ~5 minutos** (300× más rápido que el estado del arte previo), desplegado en ~200.000 lugares.
- **Cobertura:** +1M locaciones "VPS-Activated". Se construye con escaneos (app **Scaniverse**); si un lugar no está mapeado, puedes escanearlo tú.
- **World Pose:** odometría visual del lado cliente para áreas sin cobertura VPS (mejora GPS+IMU).
- **VPS2:** modos *Coarse* (geoposición global, sin mapa) y *Precise* (pose relativa a un mapa VPS). Estados de ancla: `notTracked` / `limited` / `tracked`.
- **Nota de dependencia:** es un servicio de Niantic (cloud, con user-id, políticas de privacidad). Choca con la narrativa soberana — evaluar.

**Qué aprender para Lota:** el concepto de **ancla persistente geo-referenciada** y de **localización visual** (cámara contra un mapa del lugar). Para el encuentro en el Chiflón, un ancla VPS daría precisión centimétrica. *Pero* es dependencia externa; la alternativa soberana es GPS+SLAM o marcadores fiduciales (ver 3.4 y 3.5).

*Fuentes:* nianticspatial.com/docs (VPS, VPS2), nianticlabs.github.io/ace.

### 3.2 ARCore Geospatial API (Google)
- Ancla contenido AR a **cualquier área cubierta por Google Street View**, a escala global.
- Usa el **VPS de Google** (point cloud 3D derivado de Street View) + GPS + sensores. Precisión típica **mejor que 5 m, a menudo ~1 m**, rotación <5°.
- Tipos de ancla: **WGS84** (lat/lon/alt), **Terrain** (altura relativa al suelo), **Rooftop** (relativa a techo de edificio).
- Requiere Google Cloud Project + internet. Disponible también en **Jetpack XR** (headsets/gafas Android XR).

**Qué aprender para Lota:** es la opción "ancla a coordenadas WGS84 sin mapear manualmente" más madura en Android. Útil para anclar el encuentro a la lat/lon exacta de la zona. Dependencia de Google (choca con soberanía — decidir conscientemente).

*Fuente:* developers.google.com/ar/develop/geospatial.

### 3.3 Meta Quest 3 — Mixed Reality (Presence Platform)
Esto es lo que Jaime eligió para el encuentro en sitio. Capacidades relevantes:
- **Passthrough a color:** Quest 3 tiene passthrough full-color con **10× más píxeles que Quest 2** y un depth engine por IA. Es la base para ver el mundo real y superponer lo virtual.
- **Depth API:** profundidad por ojo por frame → **oclusión dinámica** (un objeto virtual detrás de un muro real se oculta). Requiere el sensor de profundidad del Quest 3/3S.
- **Scene API / Scene Model:** representación geométrica + semántica del espacio (piso, muros, mesas), con **Scene Anchors**. El OS mantiene hasta 15 habitaciones escaneadas.
- **Spatial Anchors / Shared Spatial Anchors:** anclar contenido persistente; los *shared* permiten **colocación multi-usuario** (varias personas ven el mismo objeto en el mismo lugar).
- **Mesh API:** malla del entorno para que un personaje virtual navegue el espacio físico.
- **MR Utility Kit (MRUK):** capa de utilidades sobre Scene API (raycasts, posiciones válidas de spawn, etc.).
- **WebXR en Quest:** el navegador de Quest soporta WebXR; hay un **Reality Accelerator Toolkit** (Three.js + XRPlane/XRAnchor/HitTest/XRMesh). Apps de referencia open-source: **Phanto** y **Discover** (Scene + Spatial Anchors + Passthrough + networking con Photon Fusion).

**Qué aprender para Lota:**
- El encuentro se construye con **Passthrough + Spatial Anchors + Depth API** (oclusión para que la reconstrucción se vea real detrás de ruinas reales).
- **Shared Spatial Anchors** si quieren que varios turistas vean el mismo encuentro a la vez (modo Familia).
- **Hay camino WebXR** en Quest → podría servir una experiencia web en vez de una app nativa de la Meta Store (reduce la dependencia de la tienda, aunque no del hardware).
- Muestra open-source: **Discover** (github) para ver Scene + anchors + colocation resueltos.

*Fuentes:* developers.meta.com/horizon (Building for MR on Quest 3, Passthrough, Scene overview, Discover sample).

### 3.4 Web AR (sin instalar nada) — la opción soberana y de baja fricción
- **WebXR Device API:** estándar del navegador para AR (`immersive-ar`, hit-test, dom-overlay). Corre en Android con ARCore y en Quest Browser. Codelab oficial de Google.
- **AR.js / LocAR.js:** librería open-source, liviana, con **Location-Based AR** (ancla contenido a lat/lon usando GPS + brújula). "Turismo, treasure hunts, juegos de historia situados". Corre en cualquier teléfono con WebGL/WebRTC, **sin instalar nada**. LocAR.js es el fork mantenido (mejor iOS).
- **8th Wall (ahora open-source):** motor WebAR con World Tracking, Image Targets, Sky Effects. Ahora gratis, sin login, self-hosted. Trabaja con Three.js/Babylon/A-Frame/PlayCanvas.
- **location-based-webxr (cs-util-com):** Three.js + GPS + WebXR con **fusión de sensores GPS↔SLAM** que mantiene el contenido anclado a coordenadas reales mientras caminas. **Sin app nativa, sin VPS, sin signup, funciona offline.** Sub-métrico. Puede usar un **QR en un punto topografiado como ancla de alta precisión** (lo detecta la cámara y siembra la alineación GPS↔AR). PWA.

**Qué aprender para Lota — esto es oro para la propuesta soberana:**
- **location-based-webxr** demuestra que se puede hacer AR geolocalizada **en el navegador, offline, sin VPS de terceros** — exactamente la filosofía de Jaime. El truco del **QR como ancla topografiada** encaja con los **tótems QR** que ya están en el GDD.
- **AR.js location-based** es la forma más rápida de prototipear "ver un personaje en una coordenada" en el teléfono.
- Para el teléfono (Piloto A), la caza puede ser mapa 2D; el encuentro AR puede ser **WebAR** (sin instalar app).

*Fuentes:* codelabs.developers.google.com/ar-with-webxr, ar-js-org.github.io, 8thwall.org, github.com/cs-util-com/location-based-webxr.

### 3.5 Niantic ARDK / NSDK — oclusión, meshing y semántica
- **NSDK (Niantic Spatial SDK)** extiende AR Foundation con: **Oclusión** (dinámica, por malla, o estabilizada), **Meshing** (reconstruye el entorno en malla triangular por chunks, con niveles de detalle), **Scene Segmentation** (etiqueta suelo/cielo/etc.), **Depth Estimation**, **Object Detection**, **Navigation Mesh**.
- Funciona **con o sin LiDAR**, a mayor distancia que el depth por hardware, en Unity/Swift/Kotlin.
- Modos de oclusión: *Instant Dynamic* (rápida, objetos en movimiento), *Mesh* (estable, entornos estáticos), *Blended* (ambas).

**Qué aprender para Lota:** si el encuentro necesita que la reconstrucción se ocluya correctamente detrás de las ruinas reales, estas son las técnicas (depth + mesh + semántica). En Quest 3, la Depth API nativa cubre gran parte.

*Fuente:* nianticspatial.com/docs/ardk y /nsdk (features, meshing, occlusion).

---

## 4. Reconstrucción histórica 3D — cómo capturar el patrimonio real

Para "reconstruir la historia e imágenes reales de Lota" en RA, hay que digitalizar el patrimonio. Tres técnicas, comparadas en papers recientes de patrimonio cultural:

| Técnica | Qué es | Fortaleza | Debilidad |
|---|---|---|---|
| **Fotogrametría (SfM+MVS)** | fotos superpuestas → nube de puntos → malla texturizada | **Precisión geométrica** (survey-grade), madura, estándar en restauración | Lenta con muchas imágenes; falla en superficies reflectantes/transparencias |
| **NeRF** | red neuronal que aprende el campo de radiancia de la escena | Fotorrealista; **mejor con pocas imágenes/baja resolución**; maneja materiales difíciles | Costosa de entrenar/renderizar; no tiempo real |
| **3D Gaussian Splatting (3DGS)** | escena como distribuciones gaussianas 3D optimizables + rasterización diferenciable | **Render en tiempo real**, altísima calidad visual, entrena rápido | Precisión geométrica algo menor que fotogrametría; sensible a calidad de input |

**Hallazgos de los papers (ISPRS 2026, MDPI):**
- 3DGS **supera a la fotogrametría en calidad visual y render en tiempo real**, pero es ligeramente inferior en precisión geométrica (no sirve para documentación métrica/survey, sí para **visualización e inmersión**).
- Fotogrametría y 3DGS son **complementarias**: fotogrametría para geometría precisa, 3DGS para presentación visual inmersiva.
- Herramientas 3DGS estables: **Postshot (Jawset)**, **LichtFeld Studio**; la original **GraphDeco** es más sensible a parámetros. **Mip-splatting** reduce ruido; **SuGaR** extrae malla desde gaussianas.
- NeRF es recomendable cuando hay **pocas imágenes** (ej. relevamiento de emergencia).

**Qué aprender para Lota:**
- Para el **encuentro RA inmersivo** (ver el Chiflón operativo), **3D Gaussian Splatting** es la técnica moderna: captura el sitio real con fotos/video (incluso dron o teléfono) y renderiza en tiempo real en las Quest.
- Para **personajes** (Isidora, El Ciego), fotogrametría de objetos/actores o modelado 3D tradicional + rigging.
- Pipeline sugerido: **fotogrametría para la base geométrica fiel + 3DGS para la capa inmersiva de alta fidelidad visual**. Esto es un diferenciador técnico real para la propuesta.
- **Dependencia de contenido:** la fidelidad depende del material histórico (fotos de archivo, planos, investigación) — eso lo aporta Fabiola + archivos/CMN.

*Fuentes:* isprs-archives.copernicus.org (Photogrammetry and 3DGS for CH; comparative evaluation), mdpi.com (NeRF vs Photogrammetry, GS mesh extraction from churches), sciencedirect.com.

---

## 5. Proyectos de patrimonio gamificados — referencias directas

Estos son los proyectos más cercanos a lo que hace Lota. Todos reales, publicados (2023-2026).

| Proyecto | Lugar | Qué hace | Tech | Lección para Lota |
|---|---|---|---|---|
| **Dvaravati-Khmer AR** | Tailandia | AR + VR360 + **rally digital** por una ruta de sitios conectados | Unity + Vuforia | **+40% retención de conocimiento histórico**, 92% completitud. Conecta sitios en una ruta (como las 8 rutas de Lota). Design Thinking con stakeholders. |
| **Amiternum** | Italia | **Treasure hunt** location-based, 5 POIs validados, reconstrucción 3D AR, motor de gamificación (puntos/badges), **asistente conversacional GPT** | Unity + ARCore + microservicios REST | Arquitectura **modular y escalable a otros sitios**; gamification engine como servicio separado. |
| **HeritageSite AR** | China (Shuangta) | Juego de exploración AR: **NPCs históricos** como narradores, treasure hunt + role-playing, pistas, colección, fotos | AR móvil | **NPCs históricos que dan pistas y cuentan la historia** = exactamente los personajes de Lota. Triadic Game Design (reality/meaning/play). |
| **Glastonbury Stories** | UK (abadía) | AR + gamificación para familias; "rifts" temporales, devolver objetos fragmentados al pasado, VR360 de edificios | AR + VR360 | Objetos **fragmentados como están en la realidad arqueológica**; narrativa co-creada con el equipo de historia viva; testeo con familias. |
| **Ancient Kydonia AR Tour** | Grecia (Chania) | **Audio-AR** al aire libre por 6 sitios arqueológicos, storytelling no lineal, **audio espacial**, iluminación 3D que calza con el clima/hora real | AR móvil + spatial audio | **Audio AR** + iluminación que se ajusta al clima real en tiempo real (pariente del "evento real dirige el juego"). |
| **ARDION** | Grecia (Dodona) | Plataforma XR + **IA para co-crear guías**, gamificación con **framework RAMP de Marczewski**, avatares digitales | Web platform + AR + AI | Gamificación con teoría de motivación (autonomy/mastery/purpose); co-creación de contenido. |
| **Tour-Castellar** | España | Guía turística AR de un sitio ibérico, personaje ficticio (Aretaunin), **2 minijuegos** (excavar objetos, moblar) | Vuforia + AR Foundation | Minijuegos temáticos de excavación/mobiliario → análogos a "Amasando Pan"/"Geólogo del Tiempo". |
| **Armenia AR/AI** | Armenia (Vedi Valley) | AR/AI para turismo arqueológico, tracking markerless multi-sensor, reconstrucciones 3D + narrativas comunitarias, **asistente de itinerarios con IA** | AR/AI cross-platform | Conecta patrimonio con **comunidad local** (puente visitantes↔locales), multilingüe. |

**Patrones que se repiten (y que Lota ya tiene o debería reforzar):**
1. **NPCs/personajes históricos como narradores** que dan pistas y misiones (HeritageSite, Tour-Castellar) → los 4 personajes de Lota.
2. **Treasure hunt / búsqueda** como mecánica central (Amiternum, HeritageSite) → la caza del NPC.
3. **Gamificación con motor de puntos/badges/progresión** (todos) → Carboncillos + rangos.
4. **Rutas que conectan múltiples sitios** (Dvaravati-Khmer) → las 8 rutas de Lota.
5. **Reconstrucción 3D AR de lo que ya no está** (todos) → el encuentro RA.
6. **Evidencia de impacto:** miden **+40% retención de conocimiento** y engagement — Lota debería medir algo parecido para la propuesta.
7. **Vincular con la comunidad/comercio local** (Armenia) → la etapa 2 de comercio de Lota.

---

## 6. NPCs y agentes — arquitecturas para el enjambre SOMA

Jaime quiere NPCs **simples, deterministas, coordinados centralmente** (no IA pesada). El estado del arte confirma que esa es la llamada correcta para este caso.

### Las cuatro familias de decisión de NPCs
| Arquitectura | Cómo decide | Cuándo usarla | Costo |
|---|---|---|---|
| **FSM** (máquina de estados finita) | "estoy haciendo X; con evento Y paso a Z" | Modos fijos y pocos; **NPCs simples** | Bajo |
| **Behavior Tree** | árbol de nodos (selector/sequencia), tick por frame | Comportamiento jerárquico, iterable por diseñadores | Medio |
| **Utility AI** | puntúa cada acción posible y elige la de mayor score | Comportamiento fluido/emergente (The Sims) | Medio-alto |
| **GOAP / HTN** | planificador A* sobre acciones con precondiciones/efectos | Planes multi-paso emergentes (F.E.A.R.) | Alto |

**Consenso de la industria (GameAIPro, Socratopia, Utility Worlds):**
- **FSM es la respuesta correcta para NPCs con pocos modos fijos.** "Las state machines siguen siendo la respuesta correcta para muchos comportamientos de entidades."
- La mayoría de IAs reales son **híbridos**: FSM para modos grandes + utility/BT dentro.
- **Separar decisión de ejecución** permite correr la decisión a menor frecuencia que la ejecución (rendimiento).
- **Utility AI** brilla cuando quieres comportamiento "natural/emergente" — sobreingeniería para un NPC de misión.

**Recomendación para el enjambre SOMA de Lota:**
- Cada NPC = **FSM simple** (idle → deambular → jugador cerca → entregar misión) + **steering/waypoints** para moverse dentro del polígono de la zona. Determinista y reproducible en S60.
- El **enjambre (coordinación central)** vive en el servidor/SOMA: decide qué NPC está activo (según evento real), en qué zona, qué misión trae. Los NPCs individuales son tontos; la inteligencia está en la coordinación. Esto es exactamente lo que Jaime describió.
- Para muchos NPCs, un **ECS** (Entity-Component-System) es el patrón de rendimiento (Bevy ECS, EnTT, specs) — pero a la escala de Lota (pocos NPCs por zona) ni hace falta.
- **Server-authoritative:** el estado del NPC (posición, misión, estado) vive en el servidor; el teléfono/gafas solo lo reciben. Calza con la costura de baja latencia.

**Librerías de referencia:** BehaviorTree.CPP, Nez (C#, tiene FSM+BT+GOAP+Utility), Behavior Designer / Utility AI (Unity), Open Behavior Trees. Para Rust: hay crates de behavior tree y FSM, pero a esta escala se escribe a mano.

*Fuentes:* gameaipro.com (Reactivity and Deliberation), socratopia.app (Beyond State Machines), blog.utilityworlds.com, tonogameconsultants.com, papers.ssrn.com (FSM/BT/GOAP in Hitman/Skyrim/DEFCON).

---

## 7. Sync con eventos reales (cielo / hora) — el diferenciador de Lota

El concepto de Jaime (el cielo/hora reales dirigen el juego) tiene pocos precedentes — eso es lo que lo hace diferenciador. Referencias:

**Juegos/simuladores con cielo real:**
- **Stargazer Simulator (Steam):** simulador de astronomía en primera persona sobre **datos astronómicos reales**; el cielo cambia con ubicación, fecha y hora; clima, contaminación lumínica y atmósfera afectan qué se ve.
- **Skyos (Steam):** simulación espacial en tiempo real; la Tierra rota con la fecha/hora reales; satélites, constelaciones, eclipses sincronizados.
- **Signs and Seasons Explorer:** simula el cielo en cualquier punto de la historia (precesión, edades zodiacales).
- **My Starry Night (Wii):** planetario con ~20.000 objetos.
- **Zenith (OpenPhysics, GitHub):** planetarium first-person open-source; proyecta el cielo nocturno desde lat/lon y tiempo sidéreo local; usa la librería **`astronomy-engine`** para efemérides de Sol/Luna/planetas. PWA.

**Sync con clima/hora/fase lunar:**
- **Weather Watch (mod de Minecraft):** sincroniza clima, hora, estación y **fase lunar** del juego con el clima/tiempo real de tu ubicación (vía WeatherAPI). Es el precedente más directo de "el mundo real dirige el estado del juego".

**Precedentes mainstream de eventos reales:**
- **Animal Crossing:** reloj real (día/noche, estaciones) dirige el mundo.
- **Pokémon GO:** el **clima real** afecta qué Pokémon aparecen (affordance RO según el paper de SBGames); eventos programados.

**Librerías de efemérides/cómputo astronómico:**
- **`astronomy-engine`** (la que usa Zenith): efemérides de Sol/Luna/planetas, multi-lenguaje.
- **SOFA** (Standards of Fundamental Astronomy): la referencia astronómica de precisión.
- **astropy** (Python) para prototipos.
- Jaime ya tiene **`celestial.rs`** en Sentinel (mecánica kepleriana + trigonometría esférica en S60) — es el análogo soberano y determinista de estas librerías.

**Qué aprender para Lota:**
- El patrón "estado del juego = función determinista de (fecha, hora, lat/lon)" está validado por varios proyectos; Jaime lo hace *mejor* (S60 exacto, sin floats, sin depender de APIs externas).
- Para la **demo**, un evento celestial visible y verificable (fase lunar, o qué Estrella Real está sobre el horizonte de Lota ahora) es el "wow" reproducible.
- **No hay ningún juego patrimonial que sincronice el cielo real con encuentros de NPCs históricos** — ese es el hueco que Lota llena. Decirlo explícitamente en la propuesta.

*Fuentes:* store.steampowered.com (Stargazer, Skyos, Signs and Seasons), github.com/OpenPhysics/Zenith, github.com/ConsularAtol/weatherwatch, nintendo.com.

---

## 8. Ecosistema Rust — lo que ya existe para el motor

El stack de Jaime es Rust; esto es lo relevante del ecosistema (GeoRust es de los ecosistemas geoespaciales más maduros de Rust).

| Crate | Qué es | Uso en Lota |
|---|---|---|
| **`geo`** | primitivas (Point/LineString/Polygon) + algoritmos (contención, intersección, distancia haversine, buffer, DE-9IM) | geometría de zonas, point-in-polygon del jugador |
| **`rstar`** | **R\*-tree** (índice espacial), `no_std`, sin alocar en query | geofencing + nearest-neighbor de NPCs/zonas (**ya está en Cargo.toml**) |
| **`geo-index`** | índices espaciales packed/inmutables/zero-copy | datasets estáticos de zonas |
| **`geozero`** | lectura/escritura zero-copy de formatos geo (GeoJSON, WKB, FlatGeobuf, MVT) | cargar polígonos de OSM |
| **`geojson`** | parseo de GeoJSON | zonas desde Overpass/OSM |
| **`proj` / `geodesy`** | transformación de coordenadas y proyecciones | WGS84 ↔ coordenadas locales del mapa |
| **`geohash`** | geohash de ubicaciones | si se elige geohash como grilla |
| **`h3` (bindings)** | índice hexagonal H3 | si se elige H3 como grilla de NPCs/spawns |
| **`gdal`** | bindings de GDAL | datos raster/vectoriales pesados |

**Netcode / servidor:** `tokio` (async runtime), `axum` (HTTP/WS), `quinn` (QUIC), `redis` (pub/sub) — ya contemplados en la arquitectura de `lota-server`.
**GPU:** `wgpu` — ya en uso (pipeline compute del motor).

**Qué aprender para Lota:**
- `geo` + `rstar` + `geozero`/`geojson` + `proj` cubren todo el geofencing y la carga de zonas desde OSM **en Rust puro**, sin depender de servicios externos. Refuerza la soberanía.
- El motor ya tiene `rstar` y `wgpu`; agregar `geo`/`geozero`/`proj` completa la capa geoespacial determinista.

*Fuentes:* georust.org, github.com/georust (geo, rstar, geozero, geo-index), eors-workspace (Field Guide to GeoRust).

---

## 9. Síntesis — qué aprender/adoptar por pilar de Lota Indómito

| Pilar del concepto | Referencia clave | Qué adoptar concretamente |
|---|---|---|
| Servidor determinista + mapa | Pokémon GO (GKE+Spanner+Spatial Query Backend) | Separar frontend(jugador)/backend(mapa); servidor determinista y autoritativo (ya es la filosofía Sentinel) |
| Zonas/spawns/NPCs | S2 (Pokémon GO), H3 (Uber), rstar | rstar para geofencing local; H3 o S2 como grilla global reproducible |
| Caza del NPC | HeritageSite AR, Amiternum, Zombies Run! | Search-and-Find + feedback frío/caliente + audio; no depender solo de coordenada exacta (GPS urbano falla) |
| NPCs del enjambre | FSM + steering (GameAIPro), server-authoritative | FSM simple por NPC + coordinación central en SOMA; estado en servidor |
| Encuentro RA (gafas) | Meta Quest Presence Platform (Passthrough+Depth+Spatial Anchors), Discover sample | Passthrough + Spatial Anchors + Depth API para oclusión; Shared Anchors para multi-usuario |
| Encuentro RA (soberano/web) | location-based-webxr, AR.js, 8th Wall | WebAR geolocalizada offline; **QR topografiado como ancla** (encaja con los tótems QR del GDD) |
| Reconstrucción histórica | 3DGS + fotogrametría (papers ISPRS) | Fotogrametría para geometría fiel + 3DGS para capa inmersiva tiempo-real |
| Evento real dirige el juego | Weather Watch, Stargazer, Zenith, ARCore/astronomy-engine | Evento celestial verificable como disparador; celestial.rs es el análogo soberano |
| Rutas patrimoniales | Dvaravati-Khmer, Ingress | Rutas que conectan sitios; zonas como "portales" de interés |
| Comercio (etapa 2) | Dragon Quest Walk (Playable Locations), Armenia AR | Dirigir flujo al comercio evitando aglomeraciones; vincular visitantes↔locales |
| Gamificación | ARDION (RAMP de Marczewski), Amiternum | Motor de puntos/badges/progresión con teoría de motivación |
| Ecosistema Rust | GeoRust (geo, rstar, geozero, proj) | Completar la capa geoespacial determinista en Rust puro |

---

## 10. Recomendaciones priorizadas

**Investigar/prototipar primero (alto impacto, calza con lo que ya hay):**
1. **`geo` + `rstar` + `geozero` + `proj`** para el geofencing determinista de las zonas de Lota (ya tienes rstar). Es la base de la caza.
2. **Un encuentro AR de prueba**: decidir la vía — (a) Quest nativo con Passthrough+Spatial Anchors (más wow, más dependencia Meta), o (b) **WebAR geolocalizado (location-based-webxr / AR.js) con QR topografiado como ancla** (soberano, offline, sin instalar nada, encaja con los tótems QR). Para la propuesta, la vía soberana (b) es más coherente con la narrativa.
3. **Evento celestial verificable** como disparador de la demo (fase lunar o Estrella Real sobre Lota ahora), usando `celestial.rs`.

**Adoptar como narrativa de propuesta (ya validado por la industria):**
4. **Servidor determinista y autoritativo** (como Pokémon GO, pero con matemática soberana) — decirlo explícitamente.
5. **Medir impacto** como los proyectos de patrimonio (+40% retención de conocimiento) — proponer métricas.
6. **3D Gaussian Splatting** para la reconstrucción inmersiva del Chiflón — diferenciador técnico moderno.

**Evaluar conscientemente (trade-off de soberanía):**
7. **Niantic Lightship VPS / ARCore Geospatial:** precisión centimétrica, pero dependencia cloud de terceros. Si se usan, nombrarlo como opción; la vía soberana es WebAR + QR/GPS+SLAM.
8. **Meta Quest:** el hardware del encuentro es de Meta (inevitable si van por gafas), pero el *software/contenido* puede ser soberano (WebXR en Quest, sin pasar por la Meta Store).

**Descartar / no sobre-ingenierizar:**
9. **Utility AI / GOAP / HTN** para los NPCs — sobreingenería; FSM simple basta (la industria lo confirma).
10. **ECS pesado** — a la escala de Lota (pocos NPCs por zona) no hace falta.

---

## Fuentes principales

- Pokémon GO: cloud.google.com/blog (scaling), pokemongohub.net (S2 + backend), fullstackexpress.io
- Niantic: nianticspatial.com (VPS, VPS2, ARDK/NSDK), nianticlabs.github.io/ace
- Geospatial: h3geo.org, github.com/uber/h3, ky-gis.com, benfeifke.com, taylor-amarel.com
- AR web: codelabs.developers.google.com/ar-with-webxr, ar-js-org.github.io, 8thwall.org, github.com/cs-util-com/location-based-webxr
- Meta: developers.meta.com/horizon (MR Quest 3, Passthrough, Scene, Discover)
- Patrimonio: f1000research.com (Dvaravati-Khmer), imeko.org (Amiternum), dl.acm.org (HeritageSite AR), research.reading.ac.uk (Glastonbury), ancientkydonia.gr, link.springer.com (ARDION), github.com/VicenteMurguiSanchis/Tour-Castellar, atlab.hku.kh (Armenia)
- 3D: isprs-archives.copernicus.org (3DGS vs fotogrametría), mdpi.com (NeRF vs fotogrametría; GS churches)
- LBG design: sol.sbc.org.br (SBGames 2024 Niantic patterns), gamedeveloper.com (10 years of Ingress), blog.zombiesrungame.com, mapsplatform.google.com (Dragon Quest Walk)
- NPCs: gameaipro.com, socratopia.app, blog.utilityworlds.com, tonogameconsultants.com
- Cielo real: store.steampowered.com (Stargazer, Skyos, Signs and Seasons), github.com/OpenPhysics/Zenith, github.com/ConsularAtol/weatherwatch
- Rust: georust.org, github.com/georust (geo, rstar, geozero, geo-index)
