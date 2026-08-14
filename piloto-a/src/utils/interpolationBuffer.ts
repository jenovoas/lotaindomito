/**
 * RingBuffer + helpers de interpolación LERP.
 *
 * Caso de uso: suavizar el marcador del jugador y de los NPCs en el mapa
 * cuando el GPS o el WebSocket entregan muestras cada 3-5 s, evitando saltos.
 *
 * Cada muestra lleva su `t` (timestamp en segundos). pairAt(tSec) devuelve
 * la dupla (previous, current) que envuelve el tiempo pedido, y `lerpFactor`
 * entre 0 y 1 indica cuánto interpolar hacia `current`.
 *
 * Determinismo: la estructura es FIFO circular; los timestamps crecen
 * monótonamente al hacer push. `pairAt` requiere orden ascendente.
 */

export interface Sample<T> {
  value: T
  t: number
}

export class RingBuffer<T> {
  private buf: Sample<T>[]
  private capacity: number
  private head = 0
  private count = 0

  constructor(capacity = 10) {
    if (capacity < 2) {
      throw new Error('RingBuffer: capacity debe ser >= 2')
    }
    this.capacity = capacity
    this.buf = new Array(capacity)
  }

  push(value: T, t: number): void {
    this.buf[this.head] = { value, t }
    this.head = (this.head + 1) % this.capacity
    if (this.count < this.capacity) this.count++
  }

  size(): number {
    return this.count
  }

  latest(): Sample<T> | null {
    if (this.count === 0) return null
    const idx = (this.head - 1 + this.capacity) % this.capacity
    return this.buf[idx] ?? null
  }

  /**
   * Devuelve la dupla (previous, current) que envuelve `atSec`, junto con
   * un factor de interpolación ∈ [0, 1]. Si el buffer tiene 0 o 1 muestras,
   * devuelve la única muestra o null. Si `atSec` está fuera de rango,
   * clampa a los extremos.
   */
  pairAt(atSec: number): {
    previous: Sample<T>
    current: Sample<T>
    factor: number
  } | null {
    if (this.count === 0) return null

    // Volcar a orden cronológico ascendente.
    const ordered = this.toOrderedArray()

    if (this.count === 1) {
      const only = ordered[0]!
      return { previous: only, current: only, factor: 0 }
    }

    if (atSec <= ordered[0]!.t) {
      return {
        previous: ordered[0]!,
        current: ordered[0]!,
        factor: 0,
      }
    }

    const last = ordered[ordered.length - 1]!
    if (atSec >= last.t) {
      const prev = ordered[ordered.length - 2]!
      return { previous: prev, current: last, factor: 1 }
    }

    for (let i = 1; i < ordered.length; i++) {
      const cur = ordered[i]!
      const prev = ordered[i - 1]!
      if (atSec <= cur.t) {
        const span = cur.t - prev.t
        const factor = span === 0 ? 0 : (atSec - prev.t) / span
        return { previous: prev, current: cur, factor }
      }
    }

    // No debería llegar aquí.
    return null
  }

  private toOrderedArray(): Sample<T>[] {
    const out: Sample<T>[] = []
    if (this.count === 0) return out
    const start = (this.head - this.count + this.capacity) % this.capacity
    for (let i = 0; i < this.count; i++) {
      out.push(this.buf[(start + i) % this.capacity]!)
    }
    return out
  }
}

/** Interpolación lineal entre dos valores numéricos. */
export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * t
}

/** Clamp ∈ [min, max]. */
export function clamp(x: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, x))
}

/**
 * Helper que combina RingBuffer + lerp sobre objetos con claves numéricas.
 * Devuelve el valor interpolado en `tSec`, escalado por un factor de
 * suavizado (0 = congelado, 1 = salta directo).
 */
export function sampleAt<T extends Record<string, number>>(
  buffer: RingBuffer<T>,
  tSec: number,
  keys: readonly (keyof T)[],
  smoothing = 0.15
): T | null {
  const pair = buffer.pairAt(tSec)
  if (!pair) return null
  const t = clamp(pair.factor * smoothing, 0, 1)
  const out = { ...pair.previous.value } as T
  for (const k of keys) {
    const a = pair.previous.value[k] as number
    const b = pair.current.value[k] as number
    ;(out as Record<string, number>)[k as string] = lerp(a, b, t)
  }
  return out
}
