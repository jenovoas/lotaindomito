import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAnalyticsStore } from '../src/stores/analytics'

const FETCH_MOCK = vi.fn()
vi.stubGlobal('fetch', FETCH_MOCK)

describe('AnalyticsStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    FETCH_MOCK.mockReset()
    FETCH_MOCK.mockResolvedValue({ ok: true })
  })

  it('inicia sesion y dispara session_start', async () => {
    const store = useAnalyticsStore()
    store.init('user-123')
    await new Promise(r => setTimeout(r, 10))
    expect(store.userId).toBe('user-123')
    expect(store.enabled).toBe(true)
    expect(FETCH_MOCK).toHaveBeenCalled()
  })

  it('track poi_visit encola evento y hace flush', async () => {
    const store = useAnalyticsStore()
    store.init('user-123')
    FETCH_MOCK.mockClear()
    store.trackPoiVisit(89121388, 120)
    await new Promise(r => setTimeout(r, 10))
    const body = JSON.parse(FETCH_MOCK.mock.calls[0]?.[1]?.body || '{}')
    expect(body.events[0].event).toBe('poi_visit')
    expect(body.events[0].payload.poi_id).toBe(89121388)
    expect(body.events[0].payload.duration_s).toBe(120)
  })

  it('trackMissionComplete encola con mineral_earned', async () => {
    const store = useAnalyticsStore()
    store.init('user-456')
    FETCH_MOCK.mockClear()
    store.trackMissionComplete('chiflon', true, { cobre: 50, oro: 5 })
    await new Promise(r => setTimeout(r, 10))
    const body = JSON.parse(FETCH_MOCK.mock.calls[0]?.[1]?.body || '{}')
    expect(body.events[0].event).toBe('mission_complete')
    expect(body.events[0].payload.mineral_earned).toEqual({ cobre: 50, oro: 5 })
  })

  it('trackCouponRedeemed encola correctamente', async () => {
    const store = useAnalyticsStore()
    store.init('user-789')
    FETCH_MOCK.mockClear()
    store.trackCouponRedeemed('coupon-1', 'comercio-minero', 30)
    await new Promise(r => setTimeout(r, 10))
    const body = JSON.parse(FETCH_MOCK.mock.calls[0]?.[1]?.body || '{}')
    expect(body.events[0].event).toBe('coupon_redeemed')
    expect(body.events[0].payload.coupon_id).toBe('coupon-1')
  })

  it('endSession dispara session_end con duracion', async () => {
    const store = useAnalyticsStore()
    store.init('user-abc')
    FETCH_MOCK.mockClear()
    store.endSession()
    await new Promise(r => setTimeout(r, 10))
    const body = JSON.parse(FETCH_MOCK.mock.calls[0]?.[1]?.body || '{}')
    expect(body.events[0].event).toBe('session_end')
    expect(body.events[0].payload.duration_s).toBeGreaterThanOrEqual(0)
    expect(store.enabled).toBe(false)
  })

  it('flush reintenta en caso de error de red', async () => {
    const store = useAnalyticsStore()
    store.init('user-retry')
    FETCH_MOCK.mockClear()
    FETCH_MOCK.mockRejectedValueOnce(new Error('net'))
    store.track('session_start', {})
    await new Promise(r => setTimeout(r, 20))
    expect(store.queue.length).toBeGreaterThan(0)
  })

  it('getQueueSize devuelve tamano de la cola', () => {
    const store = useAnalyticsStore()
    store.init('user-qs')
    expect(store.getQueueSize()).toBe(0)
  })
})
