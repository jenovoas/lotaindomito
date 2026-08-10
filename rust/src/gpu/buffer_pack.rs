// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # ⚡ LOTA GPU BUFFER PACKER & WGSL UNPACK ADAPTER ⚡
//!
//! Convierte las estructuras de aritmética exacta S60 (`SPA`, `SVector3`, `IsochronousOscillator`)
//! de `me60os_core` a layouts binarios alineados a 16 bytes (`#[repr(C)]`) compatibles con WebGPU / WGSL / Vulkan.
//!
//! ## Correspondencia de structs Rust ↔ WGSL
//! | Rust              | WGSL            | Bytes |
//! |-------------------|-----------------|-------|
//! | `GpuSPA`          | `GpuSPA`        | 32    |
//! | `GpuOscillator`   | `GpuOscillator` | 128   |
//! | `GpuLatticeNode`  | `LatticeNode`   | 272   |
//!
//! Permite la transferencia directa de memoria compartida (POSIX SHM) a VRAM
//! con cero-copia y sin pérdida de precisión sexagesimal en el pipeline de render/cómputo.

#[allow(unused_imports)]
use me60os_core::celestial::SVector3;

use me60os_core::spa::SPA;
use me60os_core::isochronous_oscillator::IsochronousOscillator;
use bytemuck::{Pod, Zeroable};

/// Representación binaria de `SPA` para GPU (16 bytes alineados).
/// Contiene los componentes sexagesimales `[i32; 4]` + el valor crudo i64 de baja/alta palabra.
#[repr(C)]
#[derive(Debug, Clone, Copy, Pod, Zeroable)]
pub struct GpuSPA {
    /// Componente entero + sexagesimales principales: [c0, c1, c2, c3]
    pub components: [i32; 4],
    /// Componente c4 (4to orden sexagesimal)
    pub c4: i32,
    /// Padding para alineación estricta en std140 / WGSL (16 bytes)
    pub _pad0: i32,
    /// Parte baja del entero i64 escalado sexagesimal (raw & 0xFFFFFFFF)
    pub raw_lo: u32,
    /// Parte alta del entero i64 escalado sexagesimal (raw >> 32)
    pub raw_hi: i32,
}

impl GpuSPA {
    /// Convierte `SPA` S60 de Rust a `GpuSPA` binario para GPU
    pub fn from_spa(spa: &SPA) -> Self {
        let raw = spa.to_raw();
        let comps = spa.components;
        Self {
            components: [comps[0] as i32, comps[1] as i32, comps[2] as i32, comps[3] as i32],
            c4: comps[4] as i32,
            _pad0: 0,
            raw_lo: (raw as u64 & 0xFFFF_FFFF) as u32,
            raw_hi: (raw >> 32) as i32,
        }
    }
}

/// Vector 3D exacto para GPU (48 bytes alineados).
/// Contiene 3 coordenadas `GpuSPA` (X, Y, Z).
#[repr(C)]
#[derive(Debug, Clone, Copy, Pod, Zeroable)]
pub struct GpuVector3 {
    pub x: GpuSPA,
    pub y: GpuSPA,
    pub z: GpuSPA,
}

impl GpuVector3 {
    pub fn from_svector3(vec: &SVector3) -> Self {
        Self {
            x: GpuSPA::from_spa(&vec.x),
            y: GpuSPA::from_spa(&vec.y),
            z: GpuSPA::from_spa(&vec.z),
        }
    }
}

/// Estructura de oscilador isócrono optimizada para VRAM (64 bytes alineados).
/// Mapea la celda cristalina de `IsochronousOscillator` a buffers de almacenamiento WGSL.
#[repr(C)]
#[derive(Debug, Clone, Copy, Pod, Zeroable)]
pub struct GpuOscillator {
    pub natural_frequency: GpuSPA, // 16 bytes
    pub amplitude: GpuSPA,         // 16 bytes
    pub phase: GpuSPA,             // 16 bytes
    pub damping_factor: GpuSPA,    // 16 bytes
}

impl GpuOscillator {
    pub fn from_oscillator(osc: &IsochronousOscillator) -> Self {
        Self {
            natural_frequency: GpuSPA::from_spa(&osc.natural_frequency),
            amplitude: GpuSPA::from_spa(&osc.amplitude),
            phase: GpuSPA::from_spa(&osc.phase),
            damping_factor: GpuSPA::from_spa(&osc.damping_factor),
        }
    }
}

/// Celda de Rejilla Líquida en RAM/VRAM (192 bytes).
/// Representa un nodo con posición 3D y oscilador de estado (single-lane).
#[repr(C)]
#[derive(Debug, Clone, Copy, Pod, Zeroable)]
pub struct GpuLatticeCell {
    pub position: GpuVector3,      // 96 bytes
    pub oscillator: GpuOscillator, // 128 bytes
    pub id: u32,
    pub _pad: [u32; 3],
}

/// Nodo de Rejilla Dual-Lane para el compute shader `lattice_interference.wgsl` (272 bytes).
///
/// Mapea campo a campo con el struct `LatticeNode` del shader:
/// ```wgsl
/// struct LatticeNode {
///     oscillator_lane_a: GpuOscillator,  // 128 bytes
///     oscillator_lane_b: GpuOscillator,  // 128 bytes
///     position_x: f32,                   //   4 bytes
///     position_y: f32,                   //   4 bytes
///     position_z: f32,                   //   4 bytes
///     coherence_flag: u32,               //   4 bytes  ← escrito por GPU post-dispatch
/// };
/// ```
/// El campo `coherence_flag` lo escribe la GPU: 1 = portal abierto (|amp_A − amp_B| < SCALE_0/50).
#[repr(C)]
#[derive(Debug, Clone, Copy, Pod, Zeroable)]
pub struct GpuLatticeNode {
    pub oscillator_lane_a: GpuOscillator, // 128 bytes — Lane A
    pub oscillator_lane_b: GpuOscillator, // 128 bytes — Lane B
    /// Posición X en unidades del mundo (f32, última milla de presentación).
    pub position_x: f32,
    /// Posición Y en unidades del mundo.
    pub position_y: f32,
    /// Posición Z en unidades del mundo.
    pub position_z: f32,
    /// Flag de coherencia escrito por la GPU. 0 = sin portal, 1 = portal abierto.
    pub coherence_flag: u32,
}

impl GpuLatticeNode {
    /// Construye un nodo dual-lane desde dos osciladores de Sentinel.
    ///
    /// # Parámetros
    /// - `osc_a`: oscilador del carril A (Lane A de `ResonantMatrix`).
    /// - `osc_b`: oscilador del carril B (Lane B de `ResonantMatrix`).
    /// - `pos`: posición en el mundo (x, y, z) en f32 (conversión S60 → f32 permitida
    ///   aquí porque es la última milla de presentación, no aritmética de juego).
    pub fn from_lanes(
        osc_a: &IsochronousOscillator,
        osc_b: &IsochronousOscillator,
        pos: (f32, f32, f32),
    ) -> Self {
        Self {
            oscillator_lane_a: GpuOscillator::from_oscillator(osc_a),
            oscillator_lane_b: GpuOscillator::from_oscillator(osc_b),
            position_x: pos.0,
            position_y: pos.1,
            position_z: pos.2,
            coherence_flag: 0, // la GPU lo sobreescribe en el dispatch
        }
    }

    /// Construye un nodo dual-lane con posición en origen (útil para tests y nodos sin coordenada).
    pub fn from_lanes_default_pos(
        osc_a: &IsochronousOscillator,
        osc_b: &IsochronousOscillator,
    ) -> Self {
        Self::from_lanes(osc_a, osc_b, (0.0, 0.0, 0.0))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gpu_spa_alignment() {
        assert_eq!(std::mem::size_of::<GpuSPA>(), 32);
        assert_eq!(std::mem::size_of::<GpuVector3>(), 96);
    }

    #[test]
    fn test_gpu_oscillator_size() {
        // 4 x GpuSPA (32 bytes cada uno) = 128 bytes
        assert_eq!(std::mem::size_of::<GpuOscillator>(), 128);
    }

    #[test]
    fn test_gpu_lattice_node_size() {
        // Debe coincidir exactamente con LatticeNode del shader WGSL:
        // 128 (lane_a) + 128 (lane_b) + 4 + 4 + 4 + 4 = 272 bytes
        assert_eq!(std::mem::size_of::<GpuLatticeNode>(), 272);
    }

    #[test]
    fn test_gpu_lattice_node_from_lanes() {
        use me60os_core::isochronous_oscillator::IsochronousOscillator;
        let osc_a = IsochronousOscillator::new("lane_a");
        let osc_b = IsochronousOscillator::new("lane_b");
        let node = GpuLatticeNode::from_lanes(&osc_a, &osc_b, (1.0, 2.0, 3.0));
        assert_eq!(node.coherence_flag, 0, "coherence_flag debe iniciar en 0");
        assert_eq!(node.position_x, 1.0);
        assert_eq!(node.position_y, 2.0);
        assert_eq!(node.position_z, 3.0);
    }
}
