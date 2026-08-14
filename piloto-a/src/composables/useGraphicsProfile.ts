import { ref } from 'vue'

export type GraphicsProfile = 'full' | 'lite' | 'css-only'

interface ProfileState {
  profile: GraphicsProfile
  devicePixelRatio: number
  deviceMemory: number | null
  hasWebGL: boolean
  narrowViewport: boolean
}

const state = ref<ProfileState>({
  profile: 'full',
  devicePixelRatio: 1,
  deviceMemory: null,
  hasWebGL: true,
  narrowViewport: false,
})

function detectWebGL(): boolean {
  try {
    const canvas = document.createElement('canvas')
    return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')))
  } catch {
    return false
  }
}

/**
 * Detecta capabilities del cliente y elige un perfil gráfico:
 *
 * - 'css-only': sin WebGL o deviceMemory < 2 → el cliente desactiva canvas/three.js
 * - 'lite':     deviceMemory < 4 o viewport móvil → partículas reducidas, sin shaders pesados
 * - 'full':     desktop moderno con GPU dedicada
 */
export function useGraphicsProfile(): ProfileState {
  if (typeof window === 'undefined') return state.value

  if (state.value.deviceMemory === null) {
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    const mem = (navigator as Navigator & { deviceMemory?: number }).deviceMemory ?? null
    const hasGL = detectWebGL()
    const narrow = window.innerWidth < 768

    let profile: GraphicsProfile = 'full'
    if (!hasGL || (mem !== null && mem < 2)) {
      profile = 'css-only'
    } else if ((mem !== null && mem < 4) || (dpr > 2 && narrow)) {
      profile = 'lite'
    } else if (narrow) {
      profile = 'lite'
    }

    state.value = {
      profile,
      devicePixelRatio: dpr,
      deviceMemory: mem,
      hasWebGL: hasGL,
      narrowViewport: narrow,
    }
  }

  return state.value
}
