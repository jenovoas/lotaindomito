# Changelog — Lota Indómito

Registro de hitos del proyecto en orden cronológico inverso (lo más reciente primero).
Cada entrada cita su evidencia real (commits, tests) — este archivo es a la vez el
registro técnico del avance y el material de portfolio/currículum.

Las decisiones de diseño se registran aparte, en [`docs/decisiones.md`](docs/decisiones.md).

---

## 2026-08-10

### Concepto y diseño
- Asentado el concepto real del proyecto (D-014 corregida): evento real → NPCs del
  enjambre SOMA → caza en el teléfono → encuentro RA que reconstruye la historia real
  de Lota; motor/Sentinel como centro; etapa 2 de comercio RA + autofinanciamiento;
  expansión regional Lota → Curanilahue/Lebu/Arauco/Concepción. (`e7b868c`)
- Propuestos dos pilotos paralelos — motor propio vs tecnología de mercado (D-013). (`b9b485b`)
- Consolidada la propuesta al fondo en lenguaje humano. (`1e87bf4`)
- Rediseñado el **Core Game Loop** del GDD: el turista de paso (1-2 días en Lota)
  no tiene loop diario, sino **loop de visita** (6-10 micro-sesiones de 1-5 min cada
  una + 1-3 eventos del cielo por día) y **loop de retorno** (D+1 → D+30 vía
  pasaporte incompleto, calendario del cielo y cupones con caducidad). Las mecánicas
  clásicas de mobile (racha diaria, energía que regenera) se descartan por no
  aplicar al turista. Nuevo análisis completo en
  `_analisis/20_loop_jugador_dia_a_dia.md`. `docs/concepto-juego.md` §2
  reescrito con 5 subsecciones (loop de visita, loop de retorno, anatomía de
  micro-sesión, catálogo de eventos, descartes del modelo clásico). (`8a92131`)

### Piloto A (web — teléfono)
- Scaffold Vue 3 + TypeScript + MapLibre: mapa de Lota con 5 zonas patrimoniales. (`9e793c4`)
- Corregido el stack a Vue 3 (descartados React/Vite/Svelte para el piloto). (`37f6008`)

### Motor (Piloto B — Rust + Sentinel)
- Integrado `upload_and_dispatch` en `main.rs` con un `ResonantMatrix` real de Sentinel:
  el binario `lota-server` corre el ciclo completo — lattice dual-lane de 91 nodos → VRAM
  → compute shader → readback → reporte de portales. (`b1f5e3f`)
- Resuelto el eslabón faltante SHM→VRAM→compute→readback: `upload_and_dispatch` +
  `GpuLatticeNode` dual-lane (272 bytes). 4/4 tests pasando. (`de42f61`)
- Creado el crate `lota_engine`: pipeline GPU con wgpu sobre GTX 1050 / Vulkan,
  empaquetadores binarios `#[repr(C)]` (GpuSPA 32B, GpuVector3 96B, GpuOscillator 128B,
  GpuLatticeCell 224B) y shaders WGSL (`spa_unpack.wgsl`, `lattice_interference.wgsl`
  con `@workgroup_size(64)`). (`ece04f6`)

### Infra y documentación
- Clarificada la arquitectura: Sentinel es la capa de infra (upstream estable), Lota
  Indómito la capa de aplicación. (`c9ab077`)
- Análisis técnicos 05-18: stack, arquitectura GPU, bitácoras de sesión. (`3b17e33`)
- Actualizados concepto, decisiones D-003..D-007, estado y scripts. (`60517d1`)
- Gitignore: excluye `rust/target`, `.omo/`, `.codegraph/`, conflictos huérfanos. (`6f82eab`)

---

## 2026-08-09

### Concepto y diseño
- Definido que Lota Indómito es un **juego tipo Pokémon GO, no una app de turismo**. (`144f5b2`, `c051b6d`)

### Infra
- Integrado el prototipo Stitch de la clienta como maqueta navegable en el sitio. (`f6d7e19`)
- Montado el sitio cliente (`index.html`) y el pipeline `render-docs.py`. (`b749d0a`, `93ec6cd`)
- Commit inicial del proyecto. (`23deb74`)
