import { ref, onMounted, onUnmounted } from 'vue'
import { useGeofenceStore } from '@/stores/geofence'

export function useGeolocation() {
  const geofence = useGeofenceStore()
  const lat = ref<number | null>(null)
  const lon = ref<number | null>(null)
  const isWatching = ref(false)
  const gpsAvailable = ref(true)
  let watchId: number | null = null

  const TEST_USER = 'test-1'
  const POLL_INTERVAL = 3000 // 3s

  function startWatch(): void {
    // Intentar GPS real primero
    if ('geolocation' in navigator) {
      watchId = navigator.geolocation.watchPosition(
        (position) => {
          const newLat = position.coords.latitude
          const newLon = position.coords.longitude
          lat.value = newLat
          lon.value = newLon
          isWatching.value = true
          geofence.checkPosition(newLat, newLon, TEST_USER)
        },
        (_err) => {
          // GPS denegado o fallido — activar modo virtual
          gpsAvailable.value = false
          geofence.setVirtualMode(true)
          isWatching.value = true
        },
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 1000 }
      )
    } else {
      // No hay API de geolocalización — modo virtual
      gpsAvailable.value = false
      geofence.setVirtualMode(true)
      isWatching.value = true
    }
  }

  // Teletransporte virtual: fijar posición manual y verificar geocerca
  function teleport(targetLat: number, targetLon: number): void {
    lat.value = targetLat
    lon.value = targetLon
    geofence.checkPosition(targetLat, targetLon, TEST_USER)
  }

  function stopWatch(): void {
    if (watchId !== null) {
      navigator.geolocation.clearWatch(watchId)
      watchId = null
    }
    isWatching.value = false
  }

  onMounted(() => {
    startWatch()
  })

  onUnmounted(() => {
    stopWatch()
  })

  return {
    lat,
    lon,
    isWatching,
    gpsAvailable,
    startWatch,
    stopWatch,
    teleport,
  }
}
