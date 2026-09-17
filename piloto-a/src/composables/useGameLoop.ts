import { onMounted, onBeforeUnmount } from 'vue'

/**
 * useGameLoop — bucle de presentación desacoplado de la red.
 *
 * - Usa requestAnimationFrame y entrega `dt` (delta en segundos).
 * - Pausa automático cuando `document.hidden === true` (no consume batería).
 * - Se desuscribe automáticamente en onBeforeUnmount del componente que lo usa.
 *
 * Uso típico:
 *   useGameLoop((dt) => {
 *     const pos = interpolationBuffer.lerpAt(performance.now() / 1000)
 *     marker.setLngLat([pos.lon, pos.lat])
 *   })
 */
export function useGameLoop(update: (dtSeconds: number) => void): void {
  let rafId = 0
  let lastTime = 0
  let running = true

  const loop = (now: number) => {
    if (!running) return
    if (typeof document !== 'undefined' && document.hidden) {
      lastTime = now
      rafId = requestAnimationFrame(loop)
      return
    }
    const dt = lastTime === 0 ? 0 : (now - lastTime) / 1000
    lastTime = now
    try {
      update(dt)
    } catch (err) {
      // El loop nunca debe morir por una excepción del consumidor.
      // eslint-disable-next-line no-console
      console.error('[useGameLoop] update error:', err)
    }
    rafId = requestAnimationFrame(loop)
  }

  const onVisibility = () => {
    // al volver de background, resetea lastTime para evitar un dt gigante
    if (typeof document !== 'undefined' && !document.hidden) {
      lastTime = 0
    }
  }

  onMounted(() => {
    if (typeof document !== 'undefined') {
      document.addEventListener('visibilitychange', onVisibility)
    }
    rafId = requestAnimationFrame(loop)
  })

  onBeforeUnmount(() => {
    running = false
    if (rafId !== 0) cancelAnimationFrame(rafId)
    if (typeof document !== 'undefined') {
      document.removeEventListener('visibilitychange', onVisibility)
    }
  })
}
