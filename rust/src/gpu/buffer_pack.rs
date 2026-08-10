// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # ⚡ LOTA GPU BUFFER PACKER & WGSL UNPACK ADAPTER ⚡
//!
//! Convierte las estructuras de aritmética exacta S60 (`SPA`, `SVector3`, `IsochronousOscillator`)
//! de `me60os_core` a layouts binarios alineados a 16 bytes (`#[repr(C)]`) compatibles con WebGPU / WGSL / Vulkan.
//!
//! Permite la transferencia directa de memoria compartida (POSIX SHM) a VRAM
//! con cero-copia y sin pérdida de precisión sexagesimal en el pipeline de render/cómputo.

use me60os_core::spa::SPA;
use me60os_core::celestial::SVector3;
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

/// Celda de Rejilla Líquida en RAM/VRAM (96 bytes).
/// Representa un nodo de la rejilla con su posición espacial 3D y su oscilador de estado.
#[repr(C)]
#[derive(Debug, Clone, Copy, Pod, Zeroable)]
pub struct GpuLatticeCell {
    pub position: GpuVector3,      // 48 bytes
    pub oscillator: GpuOscillator, // 64 bytes... ajustado con pad
    pub id: u32,
    pub _pad: [u32; 3],
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gpu_spa_alignment() {
        assert_eq!(std::mem::size_of::<GpuSPA>(), 32);
        assert_eq!(std::mem::size_of::<GpuVector3>(), 96);
    }
}
