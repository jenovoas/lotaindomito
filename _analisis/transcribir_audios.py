#!/usr/bin/env python3
"""
Transcribe los audios de WhatsApp del proyecto Lota Indómito usando faster-whisper local.
- Modelo: small (int8), CPU
- Idioma: español
- Salida: un .md por audio en _analisis/transcripciones/
"""
import os
import sys
from pathlib import Path
from faster_whisper import WhisperModel

AUDIO_DIR = Path("whatsapp")
OUT_DIR = Path("_analisis/transcripciones")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Orden natural por timestamp del nombre (WhatsApp los nombra por hora)
files = sorted(AUDIO_DIR.glob("*.ogg"))
print(f"Encontrados: {len(files)} audios")

model = WhisperModel("small", device="cpu", compute_type="int8")

for f in files:
    safe_name = f.stem.replace(" ", "_").replace(".", "")
    out_path = OUT_DIR / f"{safe_name}.md"
    print(f"\n→ {f.name}  ({f.stat().st_size} bytes)")
    segments, info = model.transcribe(
        str(f),
        language="es",
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    print(f"  idioma detectado: {info.language} (prob {info.language_probability:.2f})")
    lines = [f"# Transcripción: {f.name}", "", f"Duración: {info.duration:.1f}s", ""]
    for seg in segments:
        ts = f"[{seg.start:06.2f}–{seg.end:06.2f}]"
        lines.append(f"{ts} {seg.text.strip()}")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ {out_path.name}")

print("\nListo.")
