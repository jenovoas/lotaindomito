import { describe, it, expect } from 'vitest'
import { s60ToDegrees, degreesToS60 } from '../src/utils/s60-to-degrees'

describe('s60ToDegrees', () => {
  it('convierte coordenadas de Isidora en Lota correctamente', () => {
    // Isidora lat: -37.089° -> d: -37, m: 5, s: 20, t: 24, q: 0  (approx)
    const latS60 = { d: -37, m: 5, s: 20, t: 24, q: 0 }
    const degLat = s60ToDegrees(latS60)
    expect(degLat).toBeLessThan(-37.08)
    expect(degLat).toBeGreaterThan(-37.10)

    const lonS60 = { d: -73, m: 9, s: 54, t: 0, q: 0 }
    const degLon = s60ToDegrees(lonS60)
    expect(degLon).toBeLessThan(-73.16)
    expect(degLon).toBeGreaterThan(-73.17)
  })

  it('hace round-trip con degreesToS60 preservando precisión submétrica', () => {
    const orig = -37.089166666
    const s60 = degreesToS60(orig)
    const back = s60ToDegrees(s60)
    expect(Math.abs(back - orig)).toBeLessThan(1e-6)
  })

  it('convierte el caso límite de 1 quinta (q=59)', () => {
    const s60 = { d: 0, m: 0, s: 0, t: 0, q: 59 }
    const deg = s60ToDegrees(s60)
    expect(deg).toBeCloseTo(59 / 12960000, 9)
  })

  it('lanza RangeError cuando componentes m, s, t, q están fuera de rango [0,59]', () => {
    expect(() => s60ToDegrees({ d: 0, m: 60, s: 0, t: 0, q: 0 })).toThrow(RangeError)
    expect(() => s60ToDegrees({ d: 0, m: -1, s: 0, t: 0, q: 0 })).toThrow(RangeError)
  })

  it('lanza TypeError cuando componentes no son números válidos', () => {
    expect(() => s60ToDegrees({ d: NaN, m: 0, s: 0, t: 0, q: 0 })).toThrow(TypeError)
  })
})
