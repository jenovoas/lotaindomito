# Decisiones del proyecto Lota Indómito

Registro de decisiones tomadas. **Fecha + decisión + razón + contraparte analizada.**

---

## 2026-08-09

### D-001 · Sync bidireccional con Drive para LotaIndomito
- **Decisión:** usar el mismo patrón que `micellia` (skill `backup/rclone-drive-sync`).
- **Componentes:**
  - `rclone copy` inicial (subida segura, sin borrado).
  - `rclone bisync` autocurable con systemd user service.
  - `inotifywait -t 300` para sync casi instantáneo + pull periódico cada 5 min.
- **Razón:** la clienta (CLIENTA) sube archivos (correcciones, audios, fotos) y revisa avances sin tener que aprenderse nada.
- **Filtros activos:** excluye `.ogg`, `.venv`, `node_modules`, `.next`, `__pycache__`, `.git`, `.hermes/cache`, y la carpeta `stitch_*` (es estática y pesa).
- **Reversible:** sí. `systemctl --user stop lota-indomito-live.service` y se apaga.
- **Estado actual (2026-08-09):** operativo, 18 archivos sincronizados, prueba en vivo con `.probe.txt` exitosa.

---

### D-002 · Transcripción local con faster-whisper
- **Decisión:** usar `faster-whisper` modelo `small` int8, CPU, sin API.
- **Razón:** audios cortos (total ~6 min en 9 archivos), no amerita costo de API. Cero cuota.
- **Contraparte analizada:** OpenAI Whisper API (mejor calidad pero $$), Nous STT (no verificado si está en plan).
- **Reversible:** sí, si los audios crecen o la calidad no alcanza, subir a `medium` o `large-v3` local, o pasar a API.

### D-002 · Memoria operativa en `docs/` separada de `_analisis/`
- **Decisión:** crear `docs/estado.md` para memoria viva del proyecto.
- **Razón:** INTERLOCUTOR explícito en MEMORY.md: "a mí siempre se me olvida, dejar doc". `_analisis/` queda para análisis del prototipo Stitch, `docs/` para procedimientos y estado.
- **Contraparte:** mezclar todo en `_analisis/` (rechazado — confunde búsqueda).

### D-003 · Español chileno obligatorio en redacción
- **Decisión:** regla dura. Ningún argentinismo en docs ni respuestas.
- **Razón:** INTERLOCUTOR me lo ha pedido 5+ veces en sesiones. Tengo el patrón metido en el modelo y se desliza solo.
- **Contraparte:** dejarlo libre (rechazado — falla seguro).
- **Mitigación:** detector regex guardado en `procedimientos.md`. Memoria persistente MEMORY.md lo bloquea entre sesiones.

---

## Decisiones pendientes (abiertas)

### P-001 · Alcance del MVP vs prototipo Stitch
- **Estado:** abierto. Se debate en `_analisis/02_cotejo_audis_vs_prototipo.md`.
- **Hay que decidir:** qué entra al piloto (10 palos / 3-4 semanas) y qué se deja para fase 2.
- **Pendiente input de INTERLOCUTOR.**

### P-002 · Stack técnico de la app — DECIDIDO open-source
- **Decisión (2026-08-09):** stack open-source self-hosted, no Google Maps Platform.
- **Razón:** el proyecto es servicio comunal, no debe cobrar al usuario final. Google Maps Platform tiene costo por uso (incluso plan más barato es plata), OSM es gratis.
- **Stack confirmado:**
  - Mapa base: OpenStreetMap + MapLibre GL JS (cliente).
  - Geocoding/reverse: Nominatim self-hosted.
  - Ruteo: OSRM (Open Source Routing Machine).
  - Geofencing: Turf.js en cliente + PostGIS en servidor.
  - Base de datos espacial: PostgreSQL + PostGIS.
- **Trade-off aceptado:** más tiempo de desarrollo (1-2 semanas solo para tener Nominatim + OSRM con datos de Chile funcionando).
- **Acción inmediata:** ver propuesta detallada en `_analisis/04_propuesta_tecnica_stack_osm.md`.

### P-003 · Qué entregar al fondo (producto corriendo vs propuesta)
- **Estado:** abierto.
- **Lectura de los audios:** probablemente propuesta + maqueta navegable, no el producto cerrado.
- **Pendiente confirmar con INTERLOCUTOR.**
