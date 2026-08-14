## Purpose

Especificar los recursos visuales del Piloto A (mapa y encuentros) para elevar la calidad gráfica del concepto sin introducir modelos 3D pesados ni romper el principio de "0 floats en CPU".

## ADDED Requirements

### Requirement: Retratos 2.5D estilizados para NPCs

El Piloto A SHALL mostrar a cada NPC del enjambre SOMA como un **retrato SVG 2.5D** con tres capas: silueta base (vector), iluminación lateral (gradiente cálido simulado con `feFlood`/`feGaussianBlur`) y detalle de vestimenta histórica. Los retratos SHALL entregarse como componentes Vue (`NpcAvatar.vue`) parametrizados por `npcId` con fallback determinista.

#### Scenario: Render del retrato en mapa

- **WHEN** el marcador de un NPC aparece en el mapa
- **THEN** el retrato ocupa ≥ 64 px en pantalla, tiene halo dorado animado y una sombra interior carbón que lo integra al HUD oscuro

#### Scenario: Catálogo inicial de retratos

- **WHEN** el Piloto A inicia en una zona con NPCs activos
- **THEN** los cuatro NPCs canónicos (Isidora Goyenechea, El Ciego de la Mina, La Chinchorrera Mayor, El Palanquero) tienen retratos disponibles y reutilizables

### Requirement: Bruma costera animada sobre el mapa

El mapa SHALL superponer una capa sutil de **bruma costera** (partículas CSS o canvas overlay) que evoca la costa de Lota: niebla baja translúcida con desplazamiento lento (≤ 8 px/s) en colores `#65DABC` desaturado a `#0B0E14`. La capa SHALL respetar `prefers-reduced-motion`.

#### Scenario: Niebla visible sin distraer del mapa

- **WHEN** el jugador observa el mapa durante ≥ 5 segundos
- **THEN** percibe movimiento sutil de bruma que no tapa los POIs patrimoniales ni los marcadores de NPC

#### Scenario: Niebla se intensifica al acercarse a la costa

- **WHEN** el jugador está a menos de 200 m del borde costero (polígono de costa en `zonas-lota.json`)
- **THEN** la opacidad de la bruma aumenta un 30 % y la velocidad de desplazamiento se reduce un 20 %

### Requirement: Pulso luminoso de encuentro

Cuando el jugador entra en una zona patrimonial con NPCs activos, SHALL aparecer un **anillo de pulso** en el centroide de la zona: tres anillos concéntricos que se expanden desde r=0 hasta r=80 m en 2 s con opacidad decreciente. El pulso SHALL dispararse una sola vez por entrada a la zona.

#### Scenario: Pulso al entrar a Chiflón del Diablo

- **WHEN** el geofence detecta `entered=true` para la zona del Chiflón
- **THEN** el centroide del polígono del Chiflón emite el anillo de pulso durante 2 segundos y luego se apaga

### Requirement: Ficha de encuentro coleccionable

Al tocar un marcador de NPC o su banner de intercepción, el Piloto A SHALL abrir un modal tipo **"ficha de colección"** (`EncuentroSheet.vue`) con: retrato grande del NPC a la izquierda, nombre + epíteto histórico, fragmento narrativo de 280 caracteres (atributo `historia` del NPC), barra de progreso de la micro-sesión y CTA "Iniciar Encuentro".

#### Scenario: Apertura de la ficha

- **WHEN** el jugador toca el marcador de Isidora Goyenechea en el mapa
- **THEN** se muestra la ficha con retrato, su epíteto "La dama del carbón" y el fragmento narrativo correspondiente

#### Scenario: Cierre y retorno al mapa

- **WHEN** el jugador descarta la ficha sin iniciar el encuentro
- **THEN** el modal cierra con animación slide-down y el marcador de Isidora permanece visible

### Requirement: Optimización gráfica móvil

El Piloto A SHALL medir el `devicePixelRatio` y `navigator.deviceMemory` al iniciar; si el dispositivo es gama baja (`devicePixelRatio > 2 && deviceMemory < 4`), SHALL aplicar un perfil "lite" que: reduce el halo de los marcadores a una versión estática, desactiva la bruma costera y limita el pulso de encuentro a un único anillo.

#### Scenario: Detección automática de perfil lite

- **WHEN** el dispositivo cumple ambas condiciones de gama baja
- **THEN** el estado `useGraphicsProfile()` retorna `lite` y los componentes condicionales renderizan la versión simplificada

## ADDED Requirements

### Requirement: Capa de niebla en hero de landing

La landing SHALL reemplazar la escena three.js del hero por una versión optimizada con: ≤ 250 partículas en móvil, niebla exponencial desaturada y un faro simplificado (sin chalupas múltiples) cuando `devicePixelRatio > 2`.

#### Scenario: Render de hero en móvil

- **WHEN** el visitante abre la landing en un smartphone gama media
- **THEN** el hero mantiene ≥ 50 FPS en scroll y la batería no cae más de 8 % en 60 segundos de visualización pasiva

#### Scenario: Fallback CSS en gama muy baja

- **WHEN** el dispositivo no soporta WebGL o `deviceMemory < 2`
- **THEN** el hero renderiza un fondo de gradiente CSS animado con la paleta del proyecto, sin canvas three.js
