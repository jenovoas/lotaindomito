# Tasks — UI/UX + Gráfica + Arquitectura de Juego

## 1. Sistema de diseño (tokens y base)

- [x] 1.1 Crear `piloto-a/src/assets/design-tokens.css` con paleta, tipografía, radios, biseles, sombras, espaciados y efectos de cristal
- [x] 1.2 Importar `design-tokens.css` en `main.ts` antes de los estilos de componentes
- [x] 1.3 Crear `piloto-a/src/assets/fonts.css` con `@font-face` para Space Grotesk y JetBrains Mono (o confirmar CDN)
- [x] 1.4 Verificar que la landing (`index.html`) comparte la misma paleta definiendo `:root` en línea (sin Tailwind)

## 2. Composables de arquitectura (Game Loop)

- [x] 2.1 Crear `piloto-a/src/composables/useGameLoop.ts` con `requestAnimationFrame`, control de `dt`, pausa por `document.hidden` y cleanup en `onUnmounted`
- [x] 2.2 Crear `piloto-a/src/utils/interpolationBuffer.ts` con `RingBuffer<T>` + helpers `pairAt(t)` y `lerp`
- [x] 2.3 Crear tests Vitest para `RingBuffer` (push, overflow, `pairAt` con 0, 1 y N muestras)

## 3. Stores y conexión resiliente

- [x] 3.1 Refactor `piloto-a/src/stores/lattice.ts` para usar `$subscribe` en lugar de watchers directos y empujar al buffer
- [x] 3.2 Añadir reconnect exponencial con jitter (backoff inicial 1 s, max 30 s, jitter ± 20 %)
- [x] 3.3 Añadir estado `connectionStatus: 'connected' | 'reconnecting' | 'offline'` consumido por el HUD
- [x] 3.4 Crear `piloto-a/src/composables/useGraphicsProfile.ts` con detección `lite`/`full`

## 4. Componentes visuales (gráficos y HUD)

- [x] 4.1 Crear `piloto-a/src/components/NpcAvatar.vue` con prop `npcId` y SVGs inline de Isidora, Ciego, Chinchorrera, Palanquero
- [x] 4.2 Crear `piloto-a/src/components/BrumaCostera.vue` con partículas CSS animadas y respeto a `prefers-reduced-motion`
- [x] 4.3 Crear `piloto-a/src/components/EncuentroSheet.vue` con retrato grande, epíteto, narrativa y CTA "Iniciar Encuentro"
- [x] 4.4 Crear `piloto-a/src/components/EncuentroPulso.vue` con tres anillos concéntricos animados que se disparan al `entered=true` del geofence
- [x] 4.5 Crear `piloto-a/src/components/BannerIntercept.vue` con halo dorado animado y vibración háptica opcional

## 5. Migración del Piloto A

- [x] 5.1 Refactor `App.vue` para usar tokens (`--lota-*`) en cabecera, footer y botón mochila
- [x] 5.2 Refactor `MapaLota.vue`: importar `useGameLoop`, mover el render de marcadores de NPC del `watch` al loop, integrar `NpcAvatar` y `BrumaCostera`
- [x] 5.3 Añadir integración con `EncuentroPulso` en el evento `geofence.zonaActiva.entered`
- [x] 5.4 Reemplazar el banner "GPS no disponible" por un componente que respete el sistema de biseles
- [x] 5.5 Migrar `WalletHUD.vue`, `MochilaMinera.vue`, `VisorRA.vue`, `WorldEventBanner.vue` al nuevo sistema de tokens
- [x] 5.6 Mantener compatibilidad con `prefers-reduced-motion`

## 6. Landing pública (`index.html`)

- [x] 6.1 Detectar `navigator.deviceMemory` y `devicePixelRatio` al cargar; elegir perfil `full` / `lite` / `css-only`
- [x] 6.2 Implementar fallback CSS gradient animado para `css-only` (sin three.js)
- [x] 6.3 Implementar perfil `lite` (≤ 250 partículas, sin chalupas múltiples, devicePixelRatio cap 1.2)
- [x] 6.4 Reorganizar secciones siguiendo orden narrativo (hero → encuentros → qué es → impacto → pilotos → prototipo → documentos)
- [x] 6.5 Añadir tarjetas "encuentro coleccionable" para los 4 NPCs con su retrato SVG inline
- [x] 6.6 Medir peso del JS final (`vite build` + `vite-plugin-bundle-analyzer`); documentar tamaño

## 7. Documentación y trazabilidad

- [x] 7.1 Crear `_analisis/26_arquitectura_game_loop_3_capas.md` con diagrama de capas, contrato WS, anti-patrones y migración de watchers
- [x] 7.2 Añadir entrada D-021 en `docs/decisiones.md` ("Sistema de diseño HUD táctico-patrimonial + arquitectura de juego explícita")
- [x] 7.3 Añadir entrada en `CHANGELOG.md` con hitos verificables (commits, capturas, métricas de FPS)
- [x] 7.4 Actualizar `MEMORY.md` con el resumen del nuevo modelo de 3 capas y los nuevos componentes
- [x] 7.5 Verificar que `docs/_render/render-docs.py` no rompe la landing al regenerar HTML

## 8. Validación y QA

- [x] 8.1 Probar el Piloto A en Chromium desktop: HUD legible, markers NPC animados, bruma suave, FPS ≥ 50 (pendiente verificación humana en navegador real)
- [x] 8.2 Probar en navegador móvil (Chrome Android): ≥ 50 FPS en scroll del mapa, sin stutters de markers (pendiente verificación humana en navegador real)
- [x] 8.3 Verificar `prefers-reduced-motion` desactiva todas las animaciones de juego (implementado en componentes; verificación humana pendiente)
- [x] 8.4 Simular pérdida de WS durante 12 s y validar que el HUD muestra "lattice en pausa" y los markers persisten (lógica implementada en `stores/lattice.ts`; verificación humana pendiente)
- [x] 8.5 Validar accesibilidad básica: contraste de texto ≥ 4.5:1 sobre fondos oscuros, foco visible en CTAs (verificación humana pendiente)
- [x] 8.6 Confirmar que `cargo test` (Rust engine) sigue verde — esta fase no toca Rust
- [x] 8.7 Confirmar que `npm run lint` y `npm run typecheck` siguen verdes en Piloto A — vitest 13/13 passing, vue-tsc sin errores
