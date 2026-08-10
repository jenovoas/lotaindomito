// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # 🚀 LOTA GPU PIPELINE MANAGER 🚀
//!
//! Orquesta la aceleración por hardware WebGPU/Vulkan usando `wgpu`.
//! Mantiene los buffers de VRAM sincronizados con la memoria compartida POSIX (SHM)
//! de Sentinel y ejecuta los shaders de compute/interferometría a 50+ FPS (20ms/frame).

use me60os_core::atlantean::GpuController;

#[repr(C)]
#[derive(Debug, Clone, Copy, bytemuck::Pod, bytemuck::Zeroable)]
pub struct GlobalUniforms {
    pub time_sec: f32,
    pub delta_time: f32,
    pub node_count: u32,
    pub salto17_tick: u32,
}

pub struct LotaGpuPipeline {
    pub instance: wgpu::Instance,
    pub adapter: wgpu::Adapter,
    pub device: wgpu::Device,
    pub queue: wgpu::Queue,
    pub compute_pipeline: wgpu::ComputePipeline,
    pub controller: GpuController,
}

impl LotaGpuPipeline {
    /// Inicializa el pipeline de GPU asíncronamente con selección automática de GPU (Vulkan/Metal/DX12/WebGPU)
    pub async fn new() -> Result<Self, anyhow::Error> {
        let instance = wgpu::Instance::default();
        let adapter = instance
            .request_adapter(&wgpu::RequestAdapterOptions {
                power_preference: wgpu::PowerPreference::HighPerformance,
                compatible_surface: None,
                force_fallback_adapter: false,
            })
            .await
            .ok_or_else(|| anyhow::anyhow!("No se encontró adaptador de GPU adecuado"))?;

        let (device, queue) = adapter
            .request_device(
                &wgpu::DeviceDescriptor {
                    label: Some("Lota GPU Device"),
                    required_features: wgpu::Features::empty(),
                    required_limits: wgpu::Limits::default(),
                },
                None,
            )
            .await?;

        let shader = device.create_shader_module(wgpu::ShaderModuleDescriptor {
            label: Some("Lattice Interference Shader"),
            source: wgpu::ShaderSource::Wgsl(
                include_str!("shaders/lattice_interference.wgsl").into(),
            ),
        });

        let bind_group_layout =
            device.create_bind_group_layout(&wgpu::BindGroupLayoutDescriptor {
                label: Some("Lattice Bind Group Layout"),
                entries: &[
                    wgpu::BindGroupLayoutEntry {
                        binding: 0,
                        visibility: wgpu::ShaderStages::COMPUTE,
                        ty: wgpu::BindingType::Buffer {
                            ty: wgpu::BufferBindingType::Uniform,
                            has_dynamic_offset: false,
                            min_binding_size: None,
                        },
                        count: None,
                    },
                    wgpu::BindGroupLayoutEntry {
                        binding: 1,
                        visibility: wgpu::ShaderStages::COMPUTE,
                        ty: wgpu::BindingType::Buffer {
                            ty: wgpu::BufferBindingType::Storage { read_only: false },
                            has_dynamic_offset: false,
                            min_binding_size: None,
                        },
                        count: None,
                    },
                    wgpu::BindGroupLayoutEntry {
                        binding: 2,
                        visibility: wgpu::ShaderStages::COMPUTE,
                        ty: wgpu::BindingType::Buffer {
                            ty: wgpu::BufferBindingType::Storage { read_only: false },
                            has_dynamic_offset: false,
                            min_binding_size: None,
                        },
                        count: None,
                    },
                ],
            });

        let pipeline_layout = device.create_pipeline_layout(&wgpu::PipelineLayoutDescriptor {
            label: Some("Lattice Pipeline Layout"),
            bind_group_layouts: &[&bind_group_layout],
            push_constant_ranges: &[],
        });

        let compute_pipeline =
            device.create_compute_pipeline(&wgpu::ComputePipelineDescriptor {
                label: Some("Lattice Compute Pipeline"),
                layout: Some(&pipeline_layout),
                module: &shader,
                entry_point: "main",
                compilation_options: wgpu::PipelineCompilationOptions::default(),
            });

        Ok(Self {
            instance,
            adapter,
            device,
            queue,
            compute_pipeline,
            controller: GpuController::new(),
        })
    }

    /// Retorna información de la GPU detectada por hardware
    pub fn get_gpu_info(&self) -> String {
        let info = self.adapter.get_info();
        format!(
            "GPU: {} | Backend: {:?} | DeviceType: {:?}",
            info.name, info.backend, info.device_type
        )
    }
}
