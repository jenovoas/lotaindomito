export interface S60Components {
  d: number
  m: number
  s: number
  t: number
  q: number
}

/**
 * Convierte componentes sexagesimales S60 `[d, m, s, t, q]` a grados decimales.
 * Usa BigInt para acumulaciones fraccionales internas y Number para la salida.
 */
export function s60ToDegrees(c: S60Components): number {
  if (
    typeof c.d !== 'number' ||
    typeof c.m !== 'number' ||
    typeof c.s !== 'number' ||
    typeof c.t !== 'number' ||
    typeof c.q !== 'number' ||
    Number.isNaN(c.d) ||
    Number.isNaN(c.m) ||
    Number.isNaN(c.s) ||
    Number.isNaN(c.t) ||
    Number.isNaN(c.q)
  ) {
    throw new TypeError('Todos los componentes S60 deben ser números válidos')
  }

  if (c.m < 0 || c.m >= 60) throw new RangeError('m debe estar en [0,59]')
  if (c.s < 0 || c.s >= 60) throw new RangeError('s debe estar en [0,59]')
  if (c.t < 0 || c.t >= 60) throw new RangeError('t debe estar en [0,59]')
  if (c.q < 0 || c.q >= 60) throw new RangeError('q debe estar en [0,59]')

  const isNegative = c.d < 0 || Object.is(c.d, -0)
  const absD = Math.abs(c.d)
  const sign = isNegative ? -1 : 1

  const fractionUnits =
    BigInt(c.m) * 216000n +
    BigInt(c.s) * 3600n +
    BigInt(c.t) * 60n +
    BigInt(c.q)

  const fractionDeg = Number(fractionUnits) / 12960000.0
  const absTotal = absD + fractionDeg

  return sign * absTotal
}

/**
 * Convierte grados decimales a componentes sexagesimales S60 `[d, m, s, t, q]`.
 */
export function degreesToS60(deg: number): S60Components {
  if (typeof deg !== 'number' || Number.isNaN(deg)) {
    throw new TypeError('El valor de grados debe ser un número válido')
  }

  const isNegative = deg < 0
  const absDeg = Math.abs(deg)

  let d = Math.floor(absDeg)
  const remDeg = absDeg - d
  let rawUnits = Math.round(remDeg * 12960000)

  let m = Math.floor(rawUnits / 216000)
  rawUnits %= 216000
  let s = Math.floor(rawUnits / 3600)
  rawUnits %= 3600
  let t = Math.floor(rawUnits / 60)
  let q = rawUnits % 60

  if (q >= 60) { t += Math.floor(q / 60); q %= 60 }
  if (t >= 60) { s += Math.floor(t / 60); t %= 60 }
  if (s >= 60) { m += Math.floor(s / 60); s %= 60 }
  if (m >= 60) { d += Math.floor(m / 60); m %= 60 }

  return {
    d: isNegative ? -d : d,
    m,
    s,
    t,
    q,
  }
}
