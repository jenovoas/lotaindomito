## Purpose

Define la identidad visual y los componentes reutilizables del HUD del Piloto A para que transmita la sensación de un juego geolocalizado de patrimonio, no una página web con mapa.

## ADDED Requirements

### Requirement: Sistema de tokens visuales compartido

El proyecto SHALL proveer un único módulo CSS de tokens (`assets/design-tokens.css`) que defina y exporte la paleta, tipografía, espaciados, radios de borde, biseles y efectos de cristal del HUD. Todos los componentes del Piloto A SHALL consumir estos tokens vía variables CSS; queda prohibido hardcodear colores hex o fuentes en componentes individuales.

#### Scenario: Cambio de token propaga al HUD completo

- **WHEN** se modifica el valor de `--lota-teal` en `design-tokens.css`
- **THEN** todos los marcadores de NPC, paneles, botones y banners del Piloto A reflejan el nuevo color en la próxima recarga sin requerir edits adicionales

#### Scenario: Paleta coherente con landing

- **WHEN** se compara la paleta de la landing pública con la paleta del HUD
- **THEN** los tokens primarios (`--lota-teal`, `--lota-gold`, `--lota-peach`, `--lota-copper`, `--lota-coral`, `--lota-bg`) coinciden entre `index.html` y el Piloto A

### Requirement: Marcadores de NPC con avatar estilizado

El mapa SHALL mostrar a cada NPC del enjambre SOMA como un marcador compuesto por un **avatar 2.5D estilizado** (retrato SVG con gradiente cálido + halo dorado) dentro de un bisel hexagonal tipo "ficha de colección", reemplazando el actual `el.innerText = "${npc.avatar} ${npc.name}"`.

#### Scenario: Render del marcador en mapa

- **WHEN** el jugador entra a una zona patrimonial y la API `/npcs` devuelve NPCs activos
- **THEN** cada NPC se dibuja como un hexágono biselado con retrato, nombre en mono debajo y halo que pulsa a 1.5 Hz

#### Scenario: Estado "interceptado"

- **WHEN** la distancia GPS entre jugador y NPC es inferior al umbral de intercepción (definido en `useGeolocation.ts`)
- **THEN** el marcador del NPC se resalta con un anillo dorado animado y un banner "EN EL RANGO" aparece anclado al marcador

### Requirement: Paneles con bisel carbón

Todos los paneles del HUD (panel de zona, panel de LotaStops, banners, modales de micro-sesión) SHALL usar un bisel carbón consistente: borde de 2 px con color cobre/dorado, sombra interna que simula profundidad de mina, esquinas recortadas (clip-path o border-radius asimétrico) y fondo con `backdrop-filter: blur(12px)` sobre capa semitransparente.

#### Scenario: Inspección visual del bisel

- **WHEN** se abre el panel de LotaStops sobre el mapa
- **THEN** el panel tiene borde cobre visible, fondo oscuro semitransparente y la sombra interna se percibe sin distraer del mapa

### Requirement: Tipografía de juego

El Piloto A SHALL usar dos familias tipográficas: **Space Grotesk** para títulos y CTAs (uppercase, letter-spacing > 1px) y **JetBrains Mono** para datos numéricos y labels (estado WS, contador de inventario, coords). Queda prohibido usar `system-ui` para títulos o CTAs de juego.

#### Scenario: Títulos consistentes

- **WHEN** se renderiza cualquier encabezado o botón primario del HUD
- **THEN** la tipografía es Space Grotesk con `text-transform: uppercase` y `letter-spacing` ≥ 1 px

#### Scenario: Datos numéricos legibles

- **WHEN** se muestra el tick del lattice, contador de ítems o coordenadas
- **THEN** la tipografía es JetBrains Mono

### Requirement: Animaciones de pulso y captura

El HUD SHALL incluir animaciones CSS para tres estados: pulso de NPC en rango, captura (encuentro completado con éxito) y error (GPS no disponible o WS desconectado). Cada animación SHALL respetar `prefers-reduced-motion: reduce` desactivando el bucle.

#### Scenario: Animación de captura al completar micro-sesión

- **WHEN** el jugador completa una micro-sesión (Chiflón, Isidora o Pabellón 81)
- **THEN** el modal emite un destello dorado + vibración háptica (si la API `navigator.vibrate` está disponible) y un toast deslizante confirma el ítem recibido

#### Scenario: Accesibilidad de movimiento reducido

- **WHEN** el usuario tiene `prefers-reduced-motion: reduce` activo
- **THEN** ninguna animación de pulso o captura se reproduce; los estados se comunican con cambios de color estáticos

### Requirement: Landing pública rediseñada

La landing (`index.html`) SHALL reorganizar las secciones siguiendo el orden narrativo: hero con identidad visual fuerte → "qué es" (encuentro coleccionable de NPCs) → impacto social → pilotos A/B → prototipo (galería 3D) → documentos. El hero SHALL reducir el peso de la escena three.js en móvil (≤ 1.2 devicePixelRatio, ≤ 250 partículas) y SHALL exponer una variante "lite" automática cuando `navigator.deviceMemory < 4`.

#### Scenario: Carga de landing en móvil gama media

- **WHEN** el dispositivo reporta `navigator.deviceMemory < 4`
- **THEN** la escena three.js del hero se reemplaza por un fondo de gradiente CSS animado con la paleta del proyecto y se mantiene la legibilidad del título

#### Scenario: Identidad coherente landing ↔ Piloto A

- **WHEN** un visitante navega de la landing al Piloto A (o viceversa)
- **THEN** la paleta, tipografía y motivo visual (hexágono, bisel carbón, cobre/dorado) son inmediatamente reconocibles como el mismo producto
