import { ref } from 'vue'
import { defineStore } from 'pinia'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
const QUEUE_KEY = 'lota_analytics_queue'

export type EventName =
  | 'session_start'
  | 'session_end'
  | 'poi_visit'
  | 'world_event_join'
  | 'mission_complete'
  | 'world_event_complete'
  | 'coupon_redeemed'
  | 'passport_update'
  | 'transfer_sent'
  | 'transfer_received'
  | 'trade_offered'
  | 'trade_accepted'
  | 'gift_sent'
  | 'commerce_registered'
  | 'coupon_issued'
  | 'commerce_mineral_received'

interface EventPayload {
  user_id: string
  timestamp: string
  [key: string]: unknown
}

export interface AnalyticsEvent {
  event: EventName
  payload: EventPayload
}

const EVENT_SCHEMAS: Record<EventName, string[]> = {
  session_start: ['user_id', 'timestamp', 'lat', 'lng', 'mode'],
  session_end: ['user_id', 'timestamp', 'duration_s'],
  poi_visit: ['user_id', 'poi_id', 'timestamp', 'duration_s'],
  world_event_join: ['user_id', 'event_id', 'timestamp'],
  mission_complete: ['user_id', 'mission_id', 'timestamp', 'success', 'mineral_earned'],
  world_event_complete: ['user_id', 'event_id', 'timestamp'],
  coupon_redeemed: ['user_id', 'coupon_id', 'commerce_id', 'timestamp', 'mineral_amount'],
  passport_update: ['user_id', 'completion_pct', 'timestamp'],
  transfer_sent: ['from_user', 'to_user', 'mineral_type', 'amount', 'timestamp', 'channel'],
  transfer_received: ['to_user', 'from_user', 'mineral_type', 'amount', 'timestamp'],
  trade_offered: ['from_user', 'to_user', 'offer_json', 'timestamp'],
  trade_accepted: ['from_user', 'to_user', 'exchange_json', 'timestamp'],
  gift_sent: ['from_user', 'to_user', 'mineral_type', 'amount', 'message', 'timestamp'],
  commerce_registered: ['commerce_id', 'name', 'location', 'accepted_minerals', 'exchange_rates'],
  coupon_issued: ['coupon_id', 'commerce_id', 'mineral_type', 'amount', 'expiry', 'world_event_id'],
  commerce_mineral_received: ['commerce_id', 'mineral_type', 'amount', 'timestamp', 'source'],
}

export const useAnalyticsStore = defineStore('analytics', () => {
  const queue = ref<AnalyticsEvent[]>([])
  const userId = ref<string>('')
  const sessionStart = ref<number>(0)
  const enabled = ref(false)

  function init(userIdParam: string) {
    userId.value = userIdParam
    sessionStart.value = Date.now()
    enabled.value = true
    loadQueue()
    track('session_start', { lat: 0, lng: 0, mode: 'explorer' })
  }

  function track(event: EventName, extra: Record<string, unknown> = {}) {
    if (!enabled.value) return
    const payload: EventPayload = {
      user_id: userId.value,
      timestamp: new Date().toISOString(),
      ...extra,
    }
    queue.value.push({ event, payload })
    persistQueue()
    flush()
  }

  async function flush() {
    if (queue.value.length === 0) return
    const batch = [...queue.value]
    queue.value = []
    persistQueue()
    try {
      await fetch(`${API_BASE}/api/events`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ events: batch }),
      })
    } catch {
      queue.value.unshift(...batch)
      persistQueue()
    }
  }

  function endSession() {
    const duration = Math.round((Date.now() - sessionStart.value) / 1000)
    track('session_end', { duration_s: duration })
    enabled.value = false
  }

  function trackPoiVisit(poiId: number, durationS: number) {
    track('poi_visit', { poi_id: poiId, duration_s: durationS })
  }

  function trackMissionComplete(missionId: string, success: boolean, mineralEarned: { cobre?: number; oro?: number; estanio?: number }) {
    track('mission_complete', {
      mission_id: missionId,
      success,
      mineral_earned: mineralEarned,
    })
  }

  function trackWorldEventJoin(eventId: string) {
    track('world_event_join', { event_id: eventId })
  }

  function trackWorldEventComplete(eventId: string) {
    track('world_event_complete', { event_id: eventId })
  }

  function trackCouponRedeemed(couponId: string, commerceId: string, mineralAmount: number) {
    track('coupon_redeemed', {
      coupon_id: couponId,
      commerce_id: commerceId,
      mineral_amount: mineralAmount,
    })
  }

  function trackPassportUpdate(completionPct: number) {
    track('passport_update', { completion_pct: completionPct })
  }

  function trackTransferSent(toUser: string, mineralType: string, amount: number, channel: string) {
    track('transfer_sent', {
      to_user: toUser,
      mineral_type: mineralType,
      amount,
      channel,
    })
  }

  function trackTransferReceived(fromUser: string, mineralType: string, amount: number) {
    track('transfer_received', {
      from_user: fromUser,
      mineral_type: mineralType,
      amount,
    })
  }

  function trackTradeOffered(toUser: string, offerJson: string) {
    track('trade_offered', { to_user: toUser, offer_json: offerJson })
  }

  function trackTradeAccepted(toUser: string, exchangeJson: string) {
    track('trade_accepted', { to_user: toUser, exchange_json: exchangeJson })
  }

  function trackGiftSent(toUser: string, mineralType: string, amount: number, message: string) {
    track('gift_sent', {
      to_user: toUser,
      mineral_type: mineralType,
      amount,
      message,
    })
  }

  function persistQueue() {
    try {
      localStorage.setItem(QUEUE_KEY, JSON.stringify(queue.value))
    } catch { /* storage full */ }
  }

  function loadQueue() {
    try {
      const stored = localStorage.getItem(QUEUE_KEY)
      if (stored) {
        queue.value = JSON.parse(stored)
        flush()
      }
    } catch { /* corrupted storage */ }
  }

  function getQueueSize() {
    return queue.value.length
  }

  return {
    init,
    track,
    endSession,
    trackPoiVisit,
    trackMissionComplete,
    trackWorldEventJoin,
    trackWorldEventComplete,
    trackCouponRedeemed,
    trackPassportUpdate,
    trackTransferSent,
    trackTransferReceived,
    trackTradeOffered,
    trackTradeAccepted,
    trackGiftSent,
    flush,
    getQueueSize,
    enabled,
    userId,
    queue,
  }
})
