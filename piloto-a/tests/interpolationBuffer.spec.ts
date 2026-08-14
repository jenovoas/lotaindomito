import { describe, it, expect } from 'vitest'
import {
  RingBuffer,
  lerp,
  clamp,
  sampleAt
} from '../src/utils/interpolationBuffer'

interface Pos {
  x: number
  y: number
}

describe('RingBuffer', () => {
  it('lanza error si capacity < 2', () => {
    expect(() => new RingBuffer(1)).toThrow()
    expect(() => new RingBuffer(0)).toThrow()
  })

  it('size() refleja el número de muestras', () => {
    const rb = new RingBuffer<Pos>(3)
    expect(rb.size()).toBe(0)
    rb.push({ x: 0, y: 0 }, 0)
    expect(rb.size()).toBe(1)
    rb.push({ x: 1, y: 1 }, 1)
    rb.push({ x: 2, y: 2 }, 2)
    expect(rb.size()).toBe(3)
    rb.push({ x: 3, y: 3 }, 3)
    expect(rb.size()).toBe(3) // overflow, descarta la más vieja
  })

  it('latest() devuelve la última muestra', () => {
    const rb = new RingBuffer<Pos>(3)
    rb.push({ x: 1, y: 1 }, 1)
    rb.push({ x: 2, y: 2 }, 2)
    expect(rb.latest()).toEqual({ value: { x: 2, y: 2 }, t: 2 })
  })

  it('pairAt con 0 muestras devuelve null', () => {
    const rb = new RingBuffer<Pos>(3)
    expect(rb.pairAt(0)).toBeNull()
  })

  it('pairAt con 1 muestra devuelve esa muestra como previous y current', () => {
    const rb = new RingBuffer<Pos>(3)
    rb.push({ x: 7, y: 7 }, 5)
    const pair = rb.pairAt(5)!
    expect(pair.previous.value).toEqual({ x: 7, y: 7 })
    expect(pair.current.value).toEqual({ x: 7, y: 7 })
    expect(pair.factor).toBe(0)
  })

  it('pairAt con N muestras interpola correctamente en el medio', () => {
    const rb = new RingBuffer<Pos>(5)
    rb.push({ x: 0, y: 0 }, 0)
    rb.push({ x: 10, y: 10 }, 1)
    rb.push({ x: 20, y: 20 }, 2)

    // t=1.5 cae entre las muestras t=1 y t=2, factor=0.5
    const pair = rb.pairAt(1.5)!
    expect(pair.previous.value.x).toBe(10)
    expect(pair.current.value.x).toBe(20)
    expect(pair.factor).toBeCloseTo(0.5, 5)
  })

  it('pairAt clampa al extremo izquierdo (factor=0)', () => {
    const rb = new RingBuffer<Pos>(3)
    rb.push({ x: 0, y: 0 }, 0)
    rb.push({ x: 5, y: 5 }, 1)
    const pair = rb.pairAt(-10)!
    expect(pair.factor).toBe(0)
    expect(pair.current.value.x).toBe(0)
  })

  it('pairAt clampa al extremo derecho (factor=1)', () => {
    const rb = new RingBuffer<Pos>(3)
    rb.push({ x: 0, y: 0 }, 0)
    rb.push({ x: 5, y: 5 }, 1)
    const pair = rb.pairAt(99)!
    expect(pair.factor).toBe(1)
    expect(pair.current.value.x).toBe(5)
  })

  it('mantiene orden cronológico tras overflow', () => {
    const rb = new RingBuffer<Pos>(3)
    rb.push({ x: 0, y: 0 }, 0)
    rb.push({ x: 1, y: 1 }, 1)
    rb.push({ x: 2, y: 2 }, 2)
    rb.push({ x: 3, y: 3 }, 3) // descarta {x:0}
    const ordered = (rb as unknown as { toOrderedArray: () => Array<{ value: Pos; t: number }> }).toOrderedArray()
    expect(ordered.map(s => s.value.x)).toEqual([1, 2, 3])
  })
})

describe('lerp', () => {
  it('interpola entre dos números', () => {
    expect(lerp(0, 10, 0)).toBe(0)
    expect(lerp(0, 10, 0.5)).toBe(5)
    expect(lerp(0, 10, 1)).toBe(10)
  })
})

describe('clamp', () => {
  it('limita al rango', () => {
    expect(clamp(-5, 0, 10)).toBe(0)
    expect(clamp(5, 0, 10)).toBe(5)
    expect(clamp(50, 0, 10)).toBe(10)
  })
})

describe('sampleAt', () => {
  it('devuelve null si el buffer está vacío', () => {
    const rb = new RingBuffer<Pos>(3)
    expect(sampleAt(rb, 0, ['x', 'y'])).toBeNull()
  })

  it('interpola con factor de suavizado', () => {
    const rb = new RingBuffer<Pos>(3)
    rb.push({ x: 0, y: 0 }, 0)
    rb.push({ x: 100, y: 100 }, 1)
    // smoothing=0.15, factor en t=0.5 es 0.5 * 0.15 = 0.075
    const v = sampleAt(rb, 0.5, ['x', 'y'], 0.15)!
    expect(v.x).toBeCloseTo(0 + (100 - 0) * 0.075, 5)
  })
})
