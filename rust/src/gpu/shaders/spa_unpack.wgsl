// ⚡ SENTINEL S60 SEXAGESIMAL UNPACK & MATH MODULE FOR WGSL ⚡
// Autor: Jaime Novoa Sepulveda — Todos los derechos reservados.
// Licencia: Apache 2.0 + Cláusula No Comercial.

// Constante sexagesimal fundamental: SCALE_0 = 60^4 = 12,960,000
const S60_SCALE_0: f32 = 12960000.0;
const S60_TWO_PI: f32 = 6.28318530717958647692;

struct GpuSPA {
    components: vec4<i32>, // [c0, c1, c2, c3]
    c4: i32,
    _pad0: i32,
    raw_lo: u32,
    raw_hi: i32,
};

struct GpuVector3 {
    x: GpuSPA,
    y: GpuSPA,
    z: GpuSPA,
};

struct GpuOscillator {
    natural_frequency: GpuSPA,
    amplitude: GpuSPA,
    phase: GpuSPA,
    damping_factor: GpuSPA,
};

// Desempaqueta un GpuSPA a un flotante normalizado f32 en GPU (usado para rendering visual)
fn spa_to_f32(spa: GpuSPA) -> f32 {
    let sign_mult = select(1.0, -1.0, spa.components.x < 0);
    let abs_c0 = abs(f32(spa.components.x));
    let c1 = f32(spa.components.y) / 60.0;
    let c2 = f32(spa.components.z) / 3600.0;
    let c3 = f32(spa.components.w) / 216000.0;
    let c4 = f32(spa.c4) / 12960000.0;
    
    return sign_mult * (abs_c0 + c1 + c2 + c3 + c4);
}

// Desempaqueta un GpuVector3 a vec3<f32> para posicionamiento en la escena GPU
fn svector3_to_vec3(v: GpuVector3) -> vec3<f32> {
    return vec3<f32>(
        spa_to_f32(v.x),
        spa_to_f32(v.y),
        spa_to_f32(v.z)
    );
}

// Evalúa la fase y amplitud de un IsochronousOscillator en el tiempo `time_sec`
fn evaluate_oscillator(osc: GpuOscillator, time_sec: f32) -> vec2<f32> {
    let freq = spa_to_f32(osc.natural_frequency);
    let amp = spa_to_f32(osc.amplitude);
    let phase = spa_to_f32(osc.phase);
    let damp = spa_to_f32(osc.damping_factor);
    
    let current_phase = S60_TWO_PI * freq * time_sec + phase;
    let envelope = amp * exp(-damp * time_sec);
    
    let real_val = envelope * cos(current_phase);
    let imag_val = envelope * sin(current_phase);
    
    return vec2<f32>(real_val, imag_val);
}
