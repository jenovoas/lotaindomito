# Procedimientos operativos — Lota Indómito

Cómo hacer tareas recurrentes del proyecto.

---

## Re-transcribir los audios de WhatsApp

**Cuándo:** si se pierden los `.md` o llegan audios nuevos.

```bash
cd _analisis
python3 transcribir_audios.py
```

- Modelo: `faster-whisper small` int8, CPU, idioma `es`.
- Salida: `_analisis/transcripciones/<nombre_audio>.md`.
- Tiempo: ~30-60s por minuto de audio en CPU.
- Dependencia: `pip install faster-whisper` (instalado en sesión 2026-08-09).

---

## Detector de argentinismos en el repo

**Cuándo:** antes de hacer commit o de cerrar sesión.

```bash
cd LotaIndomito/_analisis

# Patrón regex (excluye transcripciones/, donde el "vos" es cita textual)
find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.py" \) \
  ! -path "*/transcripciones/*" | while read f; do
    grep -niE "\bvos\b|\btenés\b|\btenes\b|\bquerés\b|\bqueres\b|\bsos\b|\bpo\b|\bche\b|\bboludo\b|\bbárbaro\b|\bbarbaro\b|\bgenial\b|\bdecime\b|\bdale\b|\bpiola\b|\bquilombo\b|\bchabón\b|\bchabon\b|\bguita\b|\bjeta\b|\bmilanga\b|\bchamuyo\b|\bpibe\b|\borre\b|\bcanbiar\b|\bparate\b|\bpasame\b|\bnaranjuna\b" "$f"
done
```

- **Si encuentra algo:** corregir a chileno.
- **Si la coincidencia está en `transcripciones/`:** es cita textual del audio. NO se toca. Marcar con nota al inicio del archivo.

---

## Audios nuevos del cliente

1. INTERLOCUTOR descarga el `.ogg` (o `.opus`, `.m4a`) en `whatsapp/`.
2. Correr `python3 _analisis/transcribir_audios.py`.
3. Revisar `_analisis/transcripciones/` y agregar resumen a `_analisis/01_resumen_audios_cliente.md` si aporta info nueva.

---

## Estado del proyecto (dónde mirar)

- `docs/estado.md` — qué es el proyecto, quién es quién, datos duros.
- `docs/decisiones.md` — qué se decidió, qué está abierto.
- `docs/procedimientos.md` — este archivo, cómo se hacen las tareas.
- `_analisis/` — análisis del prototipo Stitch vs audios. Se actualiza cuando llega material nuevo.
