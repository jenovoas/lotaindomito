# Lota Indómito — Concepto del juego (Game Design Document)

**Título:** *Lota Indómito: Guardianes de la Cuenca*  
**Género:** MMO-RA Urbano / Exploración en Mundo Real (Pokémon GO × World of Warcraft)  
**Plataforma:** Web PWA Mobile-First con Visor de Realidad Aumentada (Vue 3 + TypeScript + MapLibre GL + WebXR / Cámara RA)  
**Estilo Visual:** Retro-industrial + victoriano + gamer (Turquesa `#3FE6C0`, Coral `#F5A285`, Cobre `#D17A4F`, Dorado `#FFD700`, fondo nocturno `#0F1216`)

---

## 1. Visión general y Fantasía Central

*Lota Indómito* es un **MMO del Mundo Real en Realidad Aumentada** ambientado en la histórica cuenca carbonífera de Lota (Chile). El jugador se adentra en una ciudad viva donde el pasado minero y aristocrático no está muerto: está atrapado en el carbón, en las olas y en la niebla.

A través del **«Visor del Tiempo»** (el candil espectral en el teléfono), el jugador descubre que las calles de Lota son transitadas por **sombras y personajes históricos que patrullan físicamente en tiempo real**. El jugador elige su **Facción**, adopta una **Clase de Explorador**, intercepta cuadrillas a pie, completa **Cadenas de Misiones Épicas (Quest Chains)**, participa en **Raids y World Bosses en RA** sobre el paisaje costero y reactiva el comercio local mediante la economía histórica de **Minerales y Fichas de Pulpería**.

---

## 2. Core Game Loop (Ciclo principal del juego)

> **Diseño actualizado (2026-08-13 — D-019):** fusión de exploración territorial en tiempo real con profundidad de rol y RA sincronizada. Diseño completo en [`_analisis/20_loop_jugador_dia_a_dia.md`](../_analisis/20_loop_jugador_dia_a_dia.md).

```
┌─────────────────────────────────────────────────────────────────┐
│           INTERCEPCIÓN & PATRULLA EN MARCHA (1-3 min)           │
│   Radar / Audio ──► Intercepción a pie ──► Visor RA activo     │
│   (Caminar hombro a hombro con el espectro por la calle real)   │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│               CADENAS DE MISIONES (Quest Chains)                │
│   Órdenes de despacho ──► Observación "Ojos Arriba" de ruinas   │
│   ──► Sello de cantería / Diálogo de facción                    │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│           WORLD EVENTS & RAIDS EN RA (Ventanas 5-30 min)        │
│   Campana / Niebla / Atardecer ──► Bosses en el mar/chimeneas   │
│   ──► Cuadrillas de jugadores cooperando en tiempo real         │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│             LA PULPERÍA (Economía Diegética y Canje)            │
│   Minerales (Cu/Au/Sn) ──► Fichas Mineras ──► Canje real en     │
│   gastronomía, panaderías y artesanías locales (D-014/D-016)    │
└────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│               PASAPORTE DE LEYENDA & REPUTACIÓN                 │
│   Reputación con Gremios ──► Títulos ──► Pasaporte compartido   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Sistema de Facciones y Clases de Personaje

### 3.1 Las Tres Facciones de la Cuenca
Al iniciar la aventura, el jugador jura afinidad con una fuerza viva del territorio:

1. **La Hermandad del Carbón (Los del Subsuelo):** Mineros, barreteros y herreros. Sede: *Chiflón del Diablo y Pabellón 83*. Enfoque en resistencia, trabajo en equipo y dominio de la oscuridad.
2. **El Linaje de la Luz (La Aristocracia Cousiño):** Isidora Goyenechea, ingenieros y diplomáticos. Sede: *Parque Isidora*. Enfoque en diplomacia, secretos arquitectónicos y progreso.
3. **El Gremio de las Mareas (Los Hijos del Golfo):** Chinchorreras, pescadores y vigías costeros. Sede: *Caleta El Blanco y Borde Costero*. Enfoque en navegación, mareas y sabiduría oceánica.

### 3.2 Clases de Explorador y Habilidades Pasivas
| Clase | Rol en el Mundo Real | Habilidad Pasiva de Campo |
|---|---|---|
| **Barretero** (*Tank / Minero*) | Explorador de piques, chimeneas y ruinas industriales. | **Golpe de Piqueta:** Duplica la extracción de minerales en vetas de geositios. |
| **Chinchorrera** (*Ranger / Rastreadora*) | Exploradora del viento, niebla y borde costero. | **Ojo de Vigía:** Detecta patrullas móviles a 300 m adicionales en el radar. |
| **Cronista de Salón** (*Scholar / Intelectual*) | Descifrador de enigmas, planos y archivos históricos. | **Traductor de Sellos:** Desbloquea enigmas de cantería y secretos en casonas. |
| **Fogonero** (*Engineer / Artesano*) | Maestro de la forja, hornos de barro y vapor. | **Forja de Reliquias:** Permite craftear y mejorar artefactos usando carbón y metales. |

---

## 4. Mecánicas de Exploración y RA por Ruta ("Ojos Arriba")

En lugar de minijuegos 2D aislados, cada una de las 8 rutas temáticas utiliza **interacciones de Realidad Aumentada conectadas al entorno físico**:

| Ruta | Enfoque Temático | Mecánica de Campo en RA |
|---|---|---|
| **Fuego y Carbón** | Hornos y Pabellones Obreros | **Resonancia Térmica en RA:** El jugador localiza el horno de barro real, apunta con el visor y estabiliza el halo de calor espectral alineando el ángulo visual. |
| **Ruta Geositio** | Chiflón y Piques Mineros | **Estratigrafía Ocular:** Escaneo RA de la roca real para revelar vetas fósiles y fracturas geológicas del período carbonífero. |
| **Ruta de las Bodegas** | Maestranza y Maquinaria | **Engranajes del Tiempo:** Superposición 3D de las máquinas de vapor de 1890 sobre las ruinas metálicas existentes. |
| **Oficios de Mar** | Caleta y Muelles | **Tiro de Chinchorro en RA:** Calibración de parábola con el viento real para rescatar cofres y redes flotando en las olas. |
| **Camina Lota** | Pabellones Históricos | **Phasing Arquitectónico:** Superposición en escala 1:1 de fachadas históricas sobre las edificaciones actuales para detectar sellos de cantería. |
| **Ruta del Comercio** | Mercado y Pulperías | **Acuñación de Ficha Minera:** Intercambio directo de minerales por fichas digitales en locales participantes. |
| **Ruta Costera** | Fuerte Viejo y Acantilados | **Prismáticos Espectrales:** Búsqueda en el horizonte marino de navíos históricos y fauna protegida del golfo. |
| **Ruta Indómita** | Parque Isidora Goyenechea | **El Velo de Isidora:** Encuentro directo con Isidora Goyenechea caminando por los senderos victorianos. |

---

## 5. Sistema de Economía In-Game (Minerales y Fichas)

> **Diseño multi-moneda (D-016 / D-017):** Cobre, Oro y Estaño como monedas soberanas del juego.

### 5.1 Jerarquía de Minerales
- **Cobre (Cu) 🟠:** Moneda de faena diaria. Obtenida en intercepciones, patrullas y tareas de comercio.
- **Oro (Au) 🟡:** Metal del cielo y la historia. Obtenido en eventos atmosféricos y capítulos de Quest Chains.
- **Estaño (Sn) ⚪:** Metal de portales y rareza máxima. Obtenido en convergencias matemáticas S60 y pasaporte al 100%.

### 5.2 La Ficha de Pulpería y Canje Real (D-014)
Los minerales acumulados se transforman en **Fichas Mineras Digitales** que se canjean directamente en el comercio local de Lota:
- Panaderías tradicionales (pan minero / amasado).
- Gastronomía marina en la Caleta.
- Artesanías en carbón de piedra y souvenirs locales.
- **Subastas de productos reales:** Sistema de puja exclusivamente en minerales (D-017).

---

## 6. World Events y Raids en RA

Eventos colectivos que transforman la comuna en momentos específicos del día o calendario:

1. **El Galeón Fantasma de la Bahía (Raid Costera):** Barco colosal que fondea en el mar frente al Fuerte Viejo. Los jugadores deben coordinar roles en RA (vigías apuntan, barreteros sostienen balizas).
2. **El Turno de Medianoche (Piques Mineros):** Cuadrillas de sombras que marchan hacia el túnel del Chiflón bajo la luna llena.
3. **World Events de Calendario:** Sincronización con Fiestas Patrias, San Juan, Día del Patrimonio y Aniversario de Lota con NPCs y recompensas de edición limitada.

---

## 7. Sistema de Progresión, Reputación y Rangos

El jugador progresa acumulando minerales y ganando reputación con las facciones:

| Rango de Pasaporte | Requisito | Título y Beneficios |
|---|---|---|
| **Aprendiz de la Cuenca** | 0 – 500 Cu | Acceso al radar básico y primeras rutas de calle. |
| **Capataz del Carbón** | 501 – 2.000 Cu | Habilidad de cooperar en Raids y bonificación de facción. |
| **Leyenda Indómita** | 2.001+ Cu o 1 Sn | Título ceremonial, diploma físico/digital y pasaporte dorado. |

**Reputación con Gremios:** *Neutral $\rightarrow$ Respetado $\rightarrow$ Honorable $\rightarrow$ Exaltado* (desbloquea cosméticos de época para el avatar y accesos exclusivos).

---

## 8. Interfaz del Usuario (HUD & Visor RA)

```
┌─────────────────────────────────────────────────────────────────┐
│ [Cu 1.250  Au 12  Sn 1]   [Facción: Hermandad]   [GPS: Sincro 🟢]│
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                 VISOR DEL TIEMPO / VISTA MAPA                   │
│         [ Radar de Patrullas Móviles en Tiempo Real ]           │
│                                                                 │
│      🚶 El Palanquero (a 80m ──► bajando por C. Cousiño)        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│ [🗺️ Mapa]  [👁️ Visor RA]  [📜 Quests]  [🎒 Mochila]  [🏪 Pulpería]│
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Alcance del MVP (Piloto Jugable de 30 Días)

1. **1 Corredor Activo:** Chiflón del Diablo ↔ Pabellón 83 ↔ Parque de Lota.
2. **2 Patrullas Sincronizadas en Movimiento:** *El Palanquero* e *Isidora Goyenechea* caminando por rutas reales.
3. **Visor RA Funcional:** Intercepción en calle y conversación en movimiento a escala 1:1.
4. **Sistema de Facciones y Clases:** Selección inicial con perks activos.
5. **1 Quest Chain de 3 Pasos:** Concluyendo con canje real en un comercio asociado (Pulpería).
6. **Sistema Multi-moneda:** Billetera de Cu/Au/Sn operativa.

---

## 10. Referencias Cruzadas

- **Loop de Jugador y Visita:** [`_analisis/20_loop_jugador_dia_a_dia.md`](../_analisis/20_loop_jugador_dia_a_dia.md)
- **World Events:** [`_analisis/21_world_events_d014.md`](../_analisis/21_world_events_d014.md)
- **Sistema Multi-moneda:** [`_analisis/23_sistema_monedas_minerales.md`](../_analisis/23_sistema_monedas_minerales.md)
- **Subastas Reales:** [`_analisis/24_subastas_reales.md`](../_analisis/24_subastas_reales.md)
## 10. ML Externo para Análisis de Comportamiento

> **Diseño conceptual (2026-08-10).** Servicio de ML externo que consume directamente la base de datos del juego (PostgreSQL + PostGIS) sobre vistas de solo lectura. Diseño completo en [`_analisis/22_ml_analytics_d014.md`](../_analisis/22_ml_analytics_d014.md).

- **Métricas:** Detección de flujos turísticos en tiempo real, calor de zonas patrimoniales y retorno económico al comercio local.
- **Regla dura:** 0 floats en el runtime del motor; todo el análisis predictivo se procesa en el servicio analítico externo.

---

## 11. Referencias Cruzadas

- **Loop de Jugador y Visita (MMO-RA):** [`_analisis/20_loop_jugador_dia_a_dia.md`](../_analisis/20_loop_jugador_dia_a_dia.md)
- **World Events:** [`_analisis/21_world_events_d014.md`](../_analisis/21_world_events_d014.md)
- **Sistema Multi-moneda:** [`_analisis/23_sistema_monedas_minerales.md`](../_analisis/23_sistema_monedas_minerales.md)
- **Subastas Reales:** [`_analisis/24_subastas_reales.md`](../_analisis/24_subastas_reales.md)
- **ML Externo:** [`_analisis/22_ml_analytics_d014.md`](../_analisis/22_ml_analytics_d014.md)
- **D-019 (Decisión de Juego MMO-RA Urbano):** [`docs/decisiones.md`](decisiones.md)
- **D-014 (Encuadre vigente) / D-016 (Minerales) / D-017 (Subastas):** [`docs/decisiones.md`](decisiones.md)