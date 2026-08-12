# Definición del Piloto de Demostración (30 Días) — Lota Indómito

**Objetivo:** Establecer la especificación concreta de la zona de prueba y el encuentro narrativo/histórico para la maquetación del **Piloto A (PWA / Vue 3)** y la integración con el **Piloto B (`lota-server` / Sentinel S60)**.

---

## 1. Delimitación Geográfica de la Zona Piloto

Para el piloto de demostración de 30 días se prioriza el eje patrimonial y turístico de mayor flujo en Lota Alto:

### Eje Patrimonio y Mina (Lota Alto)
- **Zona 1: Chiflón del Diablo (Pique y Galería)**
  - *Coordenadas Ref:* `-37.0945, -73.1610`
  - *Identidad:* Entrada a la mina subterránea y memoria del trabajo minero.
  - *Personaje Emblemático:* **El Ciego de la Mina** (espíritu guía del pique).
  - *Minijuego:* **"El Geólogo del Tiempo"** (clasificación estratigráfica de capas de carbón y fósiles en 90s).
  - *Recompensa:* 50 Cobre (Cu) + Insignia *"Explorador de las Profundidades"*.

- **Zona 2: Parque Isidora Cousiño (Parque de Lota)**
  - *Coordenadas Ref:* `-37.0912, -73.1668`
  - *Identidad:* Botánica, arquitectura del siglo XIX y visión patrimonial.
  - *Personaje Emblemático:* **Isidora Goyenechea** (patrona y visión del desarrollo).
  - *Minijuego:* **"Rastreador de la Flora"** (trivia interactiva sobre especies nativas e introducidas del parque).
  - *Recompensa:* 30 Cobre (Cu) + 5 Oro (Au) (si hay evento de luz de atardecer).

- **Zona 3: Pabellón 81 (Centro Cultural y Memoria Social)**
  - *Coordenadas Ref:* `-37.0929, -73.1631` (POI real OSM, node/12557447365)
  - *Identidad:* Vivienda social minera, cultura e historia viva de la comunidad.
  - *Personaje Emblemático:* **El Palanquero / La Chinchorrera** (memoria colectiva).
  - *Minijuego:* **"Amasando Pan"** (QTE táctil de ritmo para amasar pan de mina).
  - *Recompensa:* 40 Cobre (Cu) + Cupón QR para Panadería/Café Local Asociado.
  - *Nota:* OSM no tiene el Pabellón 83 como way nombrado. Se usa Pabellón
    81 (POI confirmado en OSM) como zona 3 real. El polígono de geofencing es
    una aproximación sintética de ~30×30m alrededor del punto OSM, a ser
    reemplazada por el way real cuando se descargue de Overpass.

---

## 2. El Encuentro de Demostración (Core Flow)

El piloto de demostración sigue el **Flujo en 5 Tramos (4 minutos totales)**:

```
[ 1. Trigger (15s) ]     --> Vibración GPS + Banner: "Estás cerca del Chiflón del Diablo"
         │
[ 2. Contexto (45s) ]    --> Avatar 2D de El Ciego de la Mina + Diálogo corto (≤30 palabras)
         │
[ 3. Acción (90s) ]      --> Minijuego "El Geólogo del Tiempo" (QTE/Drag & Drop táctil)
         │
[ 4. Recompensa (60s) ]  --> +50 Cobre (Cu) agregados a la Wallet + Animación de Insignia
         │
[ 5. Dirección (30s) ]   --> "La Panadería 'El Minero' acepta tu Cobre. Siguiente POI: Parque de Lota (320m)"
```

### Integración con el Motor S60 (`lota-server` / GPU):
- Durante el recorrido, Sentinel S60 calcula el **Evento del Cielo** o **Portal Lattice**:
  - Si la diferencia de amplitud en GPU es `|amp_A - amp_B| < SCALE_0 / 50`, se gatilla un **Portal de Estaño (Sn)** en las coordenadas del Chiflón del Diablo.
  - La PWA recibe el evento vía WebSocket/Push e ilumina el marcador en el mapa con destello de Estaño plateado.

---

## 3. Próximos Pasos Técnicos Inmediatos
1. **Paso 2:** Extracción de polígonos GeoJSON de estas 3 zonas usando OSM / Overpass Turbo (`_scripts/download_lota_osm.py`).
2. **Paso 3:** Estructuración de la PWA Piloto A en `piloto-a/` (Vue 3 + MapLibre GL + Turf.js).
