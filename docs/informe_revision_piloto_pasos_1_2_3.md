# Informe de Revisión Técnica — Piloto de Demostración (Pasos 1, 2 y 3)

**Proyecto:** Lota Indómito: Guardianes de la Cuenca  
**Fecha de informe:** 12 de Agosto, 2026  
**Estado:** PWA Piloto A + Integración OSM + Especificación del Piloto (Listos para revisión)

---

## 📑 Resumen Ejecutivo

Se han ejecutado y completado exitosamente los tres pasos prioritarios para la construcción y fundamentación del **Piloto de Demostración (30 Días)** de Lota Indómito, respetando la arquitectura de dos capas (D-014):

1. **Paso 1: Especificación Formal del Piloto** ([`docs/piloto_zonas_especificacion.md`](../docs/piloto_zonas_especificacion.md)).
2. **Paso 2: Geometría Reales y POIs de Lota** ([`public/data/lota_pois.geojson`](../public/data/lota_pois.geojson)).
3. **Paso 3: Componente Interactivo de Micro-sesión y Wallet HUD** ([`piloto-a/src/components/MicroSesionChiflon.vue`](../piloto-a/src/components/MicroSesionChiflon.vue)).

---

## 🎯 Detalle de los Pasos Implementados

### 1. Especificación del Piloto de Demostración (Paso 1)

Se definió el marco geográfico y operativo para la prueba de concepto en **Lota Alto**:

* **Eje Patrimonial (3 Zonas Clave):**
  * **Chiflón del Diablo (Pique):** Personaje *El Ciego de la Mina*, Minijuego *"El Geólogo del Tiempo"*, Recompensa: 50 Cobre (Cu).
  * **Parque Isidora Cousiño:** Personaje *Isidora Goyenechea*, Minijuego *"Rastreador de la Flora"*, Recompensa: 30 Cobre (Cu) + 5 Oro (Au).
  * **Pabellón 83:** Personaje *La Chinchorrera / El Palanquero*, Minijuego *"Amasando Pan"*, Recompensa: 40 Cobre (Cu) + Cupón QR.
* **Flujo Atómico de 5 Tramos (4 min totales):**
  1. *Trigger (15s):* Detección por Geofence GPS.
  2. *Contexto (45s):* Avatar 2D + Diálogo corto (≤30 palabras).
  3. *Acción (90s):* Minijuego táctil / QTE.
  4. *Recompensa (60s):* Asignación de Cobre/Oro/Estaño + Insignia.
  5. *Dirección (30s):* Indicación de ruta hacia el siguiente POI o Comercio Local asociado.
* **Integración S60 (GPU):** Gatillado de Portales de Estaño (Sn) al detectar convergencia dual-lane (`|amp_A - amp_B| < SCALE_0 / 50`).

---

### 2. Extracción y Procesamiento Geográfico OSM (Paso 2)

Se construyó e integró el pipeline de datos geográficos para la comuna de Lota:

* **Script Creado:** [`_scripts/download_lota_osm.py`](../_scripts/download_lota_osm.py)
* **API Consultada:** Overpass API (`overpass-api.de`).
* **Delimitación (Bounding Box Lota):** Latitud `[-37.11 a -37.07]`, Longitud `[-73.18 a -73.13]`.
* **Resultado:** [`public/data/lota_pois.geojson`](../public/data/lota_pois.geojson) con **41 puntos patrimoniales y turísticos reales** (Chiflón del Diablo, Pueblito Minero, Bahía Lota, Residencia Doña Isidora, miradores y ruinas históricas).

---

### 3. Maquetación e Integración PWA Piloto A (Paso 3)

Se construyó la interfaz interactiva de la PWA en Vue 3 + MapLibre GL:

* **Micro-sesión Chiflón del Diablo:**
  * Componente [`MicroSesionChiflon.vue`](../piloto-a/src/components/MicroSesionChiflon.vue) que ejecuta el modal interactivo de la micro-sesión.
  * Incluye diálogo narrativo, minijuego de clasificación de eras geológicas y secuencia de entrega de recompensa.
* **Billetera Multi-moneda (Wallet HUD):**
  * Integrado [`WalletHUD.vue`](../piloto-a/src/components/WalletHUD.vue) en el header principal (`App.vue`), reflejando de forma reactiva el saldo de Cobre (Cu), Oro (Au) y Estaño (Sn) acumulados por el usuario.
* **Mapa Interactivo:**
  * [`MapaLota.vue`](../piloto-a/src/components/MapaLota.vue) despliega las zonas geofenced, permitiendo teletransporte de prueba e inicio de la misión.
* **Verificación:** Compilación verificada con `npm run build-only` sin errores.

---

## 📈 Evidencia de Registros e Historial

* **Commits Realizados:**
  * `7e9b395`: `feat: especificar piloto de 30 días, extraer POIs de Lota y maquetar micro-sesión Chiflón del Diablo`
  * `0333108`: `docs: actualizar CHANGELOG con hito de pasos 1, 2 y 3`
* **Archivos Clave Modificados/Creados:**
  * [`docs/piloto_zonas_especificacion.md`](../docs/piloto_zonas_especificacion.md)
  * [`_scripts/download_lota_osm.py`](../_scripts/download_lota_osm.py)
  * [`public/data/lota_pois.geojson`](../public/data/lota_pois.geojson)
  * [`piloto-a/src/components/MicroSesionChiflon.vue`](../piloto-a/src/components/MicroSesionChiflon.vue)
  * [`piloto-a/src/components/MapaLota.vue`](../piloto-a/src/components/MapaLota.vue)
  * [`piloto-a/src/App.vue`](../piloto-a/src/App.vue)
  * [`CHANGELOG.md`](../CHANGELOG.md)
