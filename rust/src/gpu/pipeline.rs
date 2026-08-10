// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.
//! # 🚀 LOTA GPU PIPELINE MANAGER 🚀
//!
//! Orquesta la aceleración por hardware WebGPU/Vulkan usando `wgpu`.
//! Mantiene los buffers de VRAM sincronizados con la memoria compartida POSIX (SHM)
//! de Sentinel y ejecuta los shaders de compute/interferometría a 50+ FPS (20ms/frame).

use me60os_core::atlantean::GpuController;
use me60os_core::resonant_matrix::ResonantMatrix;
use wgpu::util::DeviceExt;

use crate::gpu::buffer_pack::GpuLatticeNode;

#[repr(C)]
#[derive(Debug, Clone, Copy, bytemuck::Pod, bytemuck::Zeroable)]
pub struct GlobalUniforms {
    pub time_sec: f32,
    pub delta_time: f32,
    pub node_count: u32,
    pub salto17_tick: u32,
}

/// Resultado de un ciclo de dispatch del compute shader.
#[derive(Debug)]
pub struct DispatchResult {
    /// Valor de interferencia de onda por nodo (output del shader, un f32 por nodo).
    /// `wave_val[i] = amp_a * cos(2π * freq_a * t + phase_a)` para el nodo i.
    pub wave_values: Vec<f32>,
    /// Número de nodos donde el portal dual-lane está abierto.
    /// Portal = `|amp_A − amp_B| < SCALE_0 / 50` (condición YATRA de convergencia).
    pub portal_count: u32,
    /// Índices de los nodos con portal abierto (coherence_flag == 1).
    pub portal_indices: Vec<u32>,
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

    /// Empaqueta la doble malla de cristales en VRAM y ejecuta el compute shader.
    ///
    /// # Parámetros
    /// - `lane_a`: malla resonante del carril A (`ResonantMatrix`).
    /// - `lane_b`: malla resonante del carril B (`ResonantMatrix`).
    /// - `tick`: contador de ticks QHC actual (salto-17 se activa cada 68 ticks).
    /// - `time_sec`: tiempo de juego en segundos (f32, solo para la onda de presentación).
    ///
    /// # Flujo interno
    /// ```text
    /// lane_a.crystals + lane_b.crystals
    ///   → Vec<GpuLatticeNode> (interleaved A+B, 272 bytes/nodo)
    ///   → wgpu::Buffer STORAGE (VRAM, binding 1)
    ///   → lattice_interference.wgsl dispatch (@workgroup_size(64))
    ///   → readback staging → wave_values + portal_count
    /// ```
    ///
    /// # Condición de portal (YATRA)
    /// El shader marca `coherence_flag = 1` cuando `|amp_A − amp_B| < SCALE_0 / 50`.
    pub fn upload_and_dispatch(
        &self,
        lane_a: &ResonantMatrix,
        lane_b: &ResonantMatrix,
        tick: u32,
        time_sec: f32,
    ) -> anyhow::Result<DispatchResult> {
        let n = lane_a.crystals.len().min(lane_b.crystals.len());
        if n == 0 {
            return Ok(DispatchResult {
                wave_values: vec![],
                portal_count: 0,
                portal_indices: vec![],
            });
        }

        // ── 1. Empaquetar crystals → Vec<GpuLatticeNode> (Lane A + Lane B interleaved) ──
        let nodes: Vec<GpuLatticeNode> = lane_a
            .crystals
            .iter()
            .zip(lane_b.crystals.iter())
            .map(|(a, b)| GpuLatticeNode::from_lanes_default_pos(a, b))
            .collect();

        // ── 2. Uniform buffer ──
        let uniforms = GlobalUniforms {
            time_sec,
            delta_time: 0.02, // 20ms target (50 FPS) — ajustar con IsochronousClock
            node_count: n as u32,
            salto17_tick: tick,
        };
        let uniforms_buf = self.device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
            label: Some("GlobalUniforms"),
            contents: bytemuck::bytes_of(&uniforms),
            usage: wgpu::BufferUsages::UNIFORM | wgpu::BufferUsages::COPY_DST,
        });

        // ── 3. Nodes buffer (LatticeNode dual-lane → binding 1) ──
        let nodes_size = (std::mem::size_of::<GpuLatticeNode>() * n) as u64;
        let nodes_buf = self.device.create_buffer_init(&wgpu::util::BufferInitDescriptor {
            label: Some("LatticeNodes"),
            contents: bytemuck::cast_slice(&nodes),
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
        });

        // ── 4. Output buffer (f32 por nodo → binding 2) ──
        let output_size = (std::mem::size_of::<f32>() * n) as u64;
        let output_buf = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("OutputInterference"),
            size: output_size,
            usage: wgpu::BufferUsages::STORAGE | wgpu::BufferUsages::COPY_SRC,
            mapped_at_creation: false,
        });

        // ── 5. Staging buffers (CPU-readable, MAP_READ) ──
        let staging_output = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("StagingOutput"),
            size: output_size,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });
        let staging_nodes = self.device.create_buffer(&wgpu::BufferDescriptor {
            label: Some("StagingNodes"),
            size: nodes_size,
            usage: wgpu::BufferUsages::MAP_READ | wgpu::BufferUsages::COPY_DST,
            mapped_at_creation: false,
        });

        // ── 6. Bind group ──
        let bind_group_layout = self.compute_pipeline.get_bind_group_layout(0);
        let bind_group = self.device.create_bind_group(&wgpu::BindGroupDescriptor {
            label: Some("LatticeBindGroup"),
            layout: &bind_group_layout,
            entries: &[
                wgpu::BindGroupEntry {
                    binding: 0,
                    resource: uniforms_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 1,
                    resource: nodes_buf.as_entire_binding(),
                },
                wgpu::BindGroupEntry {
                    binding: 2,
                    resource: output_buf.as_entire_binding(),
                },
            ],
        });

        // ── 7. Command encoder: compute pass + copias a staging ──
        let mut encoder =
            self.device
                .create_command_encoder(&wgpu::CommandEncoderDescriptor {
                    label: Some("LatticeDispatchEncoder"),
                });

        {
            let mut pass = encoder.begin_compute_pass(&wgpu::ComputePassDescriptor {
                label: Some("LatticeComputePass"),
                timestamp_writes: None,
            });
            pass.set_pipeline(&self.compute_pipeline);
            pass.set_bind_group(0, &bind_group, &[]);
            // ceil(n / 64) workgroups — cada workgroup procesa 64 nodos en paralelo
            let workgroups = ((n as u32) + 63) / 64;
            pass.dispatch_workgroups(workgroups, 1, 1);
        }

        // Copiar resultados a staging ANTES del submit (se ejecuta después del compute pass)
        encoder.copy_buffer_to_buffer(&output_buf, 0, &staging_output, 0, output_size);
        encoder.copy_buffer_to_buffer(&nodes_buf, 0, &staging_nodes, 0, nodes_size);

        // ── 8. Submit + poll hasta completar ──
        self.queue.submit(std::iter::once(encoder.finish()));

        // ── 9. Readback: output_interference (wave values) ──
        let wave_values = {
            let (tx, rx) = std::sync::mpsc::channel();
            staging_output
                .slice(..)
                .map_async(wgpu::MapMode::Read, move |v| tx.send(v).unwrap());
            self.device.poll(wgpu::Maintain::Wait);
            rx.recv()
                .unwrap()
                .map_err(|e| anyhow::anyhow!("map output_interference falló: {:?}", e))?;
            let mapped = staging_output.slice(..).get_mapped_range();
            let values: Vec<f32> = bytemuck::cast_slice(&*mapped).to_vec();
            drop(mapped);
            staging_output.unmap();
            values
        };

        // ── 10. Readback: nodes (leer coherence_flag escrito por GPU) ──
        let (portal_count, portal_indices) = {
            let (tx, rx) = std::sync::mpsc::channel();
            staging_nodes
                .slice(..)
                .map_async(wgpu::MapMode::Read, move |v| tx.send(v).unwrap());
            self.device.poll(wgpu::Maintain::Wait);
            rx.recv()
                .unwrap()
                .map_err(|e| anyhow::anyhow!("map nodes falló: {:?}", e))?;
            let mapped = staging_nodes.slice(..).get_mapped_range();
            let nodes_back: Vec<GpuLatticeNode> = bytemuck::cast_slice(&*mapped).to_vec();
            drop(mapped);
            staging_nodes.unmap();
            let indices: Vec<u32> = nodes_back
                .iter()
                .enumerate()
                .filter_map(|(i, node)| {
                    if node.coherence_flag == 1 { Some(i as u32) } else { None }
                })
                .collect();
            let count = indices.len() as u32;
            (count, indices)
        };

        Ok(DispatchResult {
            wave_values,
            portal_count,
            portal_indices,
        })
    }
}
