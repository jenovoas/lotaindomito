// ⚡ LOTA INDÓMITO DUAL-LANE LATTICE INTERFERENCE COMPUTE SHADER ⚡
// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.

struct GpuSPA {
    components: vec4<i32>,
    c4: i32,
    _pad0: i32,
    raw_lo: u32,
    raw_hi: i32,
};

struct GpuOscillator {
    natural_frequency: GpuSPA,
    amplitude: GpuSPA,
    phase: GpuSPA,
    damping_factor: GpuSPA,
};

struct LatticeNode {
    oscillator_lane_a: GpuOscillator,
    oscillator_lane_b: GpuOscillator,
    position_x: f32,
    position_y: f32,
    position_z: f32,
    coherence_flag: u32,
};

struct GlobalUniforms {
    time_sec: f32,
    delta_time: f32,
    node_count: u32,
    salto17_tick: u32,
};

@group(0) @binding(0) var<uniform> uniforms: GlobalUniforms;
@group(0) @binding(1) var<storage, read_write> nodes_a: array<LatticeNode>;
@group(0) @binding(2) var<storage, read_write> output_interference: array<f32>;

const S60_SCALE_0: f32 = 12960000.0;
const S60_TWO_PI: f32 = 6.28318530717958647692;

fn spa_to_f32(spa: GpuSPA) -> f32 {
    let sign_mult = select(1.0, -1.0, spa.components.x < 0);
    let abs_c0 = abs(f32(spa.components.x));
    let c1 = f32(spa.components.y) / 60.0;
    let c2 = f32(spa.components.z) / 3600.0;
    let c3 = f32(spa.components.w) / 216000.0;
    let c4 = f32(spa.c4) / 12960000.0;
    return sign_mult * (abs_c0 + c1 + c2 + c3 + c4);
}

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) global_id: vec3<u32>) {
    let index = global_id.x;
    if (index >= uniforms.node_count) {
        return;
    }

    var node = nodes_a[index];

    let amp_a = spa_to_f32(node.oscillator_lane_a.amplitude);
    let amp_b = spa_to_f32(node.oscillator_lane_b.amplitude);
    let freq_a = spa_to_f32(node.oscillator_lane_a.natural_frequency);
    let phase_a = spa_to_f32(node.oscillator_lane_a.phase);

    // Verificación de convergencia de doble carril: |amp_A - amp_B| < SCALE_0 / 50
    let diff = abs(amp_a - amp_b);
    let is_coherent = u32(diff < (1.0 / 50.0));
    
    // Interferometría de fase en el nodo
    let wave_val = amp_a * cos(S60_TWO_PI * freq_a * uniforms.time_sec + phase_a);

    nodes_a[index].coherence_flag = is_coherent;
    output_interference[index] = wave_val;
}
