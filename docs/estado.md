# Proyecto Lota Indómito — Estado vivo

**Última actualización:** 2026-08-09
**Raíz:** ``

---

## 1. Quién es quién

- **INTERLOCUTOR (tú)**: encargado técnico, interlocutor de la clienta.
- **CLIENTA**: clienta. Postula a fondos públicos para turismo cultural en Lota (Chile).
- **Audios de CLIENTA**: 9 audios de WhatsApp del 2026-08-07, transcritos en `_analisis/transcripciones/`.

---

## 2. El proyecto en una línea

App gamificada de turismo cultural para Lota (ciudad carbonífera, Chile). Visita a sectores culturales, mecánica de juego, estadísticas y alertas ciudadanas alimentan un dashboard para municipio + instituciones patrimoniales.

---

## 3. Datos duros confirmados (de audios)

| Dato | Valor |
|---|---|
| Presupuesto total del proyecto | **10 millones CLP** (incluye gastos + honorarios de ambos) |
| Plazo de presentación | **Fines de agosto / primera semana de septiembre 2026** |
| Fondo secundario posible | **Fondo del patrimonio: 15 a 20 millones CLP** |
| Postulación a dos fondos | **Sí, se puede** (audio 8) |
| Entregable implícito | **Propuesta para el fondo** (maqueta + doc), NO el producto terminado |

---

## 4. Estructura del repo

```
LotaIndomito/
├── _analisis/                    # Análisis del prototipo Stitch
│   ├── 00_resumen_sesion.md     # Estado al cierre de sesión anterior
│   ├── 01_resumen_audios_cliente.md
│   ├── 02_cotejo_audis_vs_prototipo.md
│   ├── transcribir_audios.py    # Script para reproducir transcripciones
│   └── transcripciones/         # 9 .md, uno por audio
├── docs/                        # ESTE DIRECTORIO — memoria operativa del proyecto
├── stitch_lota_ind_mito_ciudad_museo_gamificada/
│   ├── documento_t_cnico_lota_ind_mito.md   # Doc del prototipo Stitch
│   └── <~50 carpetas de pantallas>
└── whatsapp/                    # Audios originales (.ogg)
```

---

## 5. Convenciones de estilo de redacción (duro)

- **Español chileno obligatorio.** Sin conjugaciones argentinas.
- Prohibido: "vos", "tenés", "querés", "sos", "po", "che", "boludo", "bárbaro", "genial", "decime", "dale".
- Permitido: "tú", "tienes", "quieres", "eres", "ya", "listo", "ok", "dime".
- Audios transcritos pueden contener "vos"/"po"/"síbo" — es cita textual del audio, se conserva tal cual. Marcar con nota al inicio del archivo.

---

## 6. Sincronización con Google Drive (cliente sube archivos)

**Decidido (2026-08-09):** sync bidireccional con `drive:/LotaIndomito` (o nombre equivalente), usando `rclone bisync` + `inotifywait` + systemd user service.

- Mismo patrón que `micellia`. Ver skill `backup/rclone-drive-sync/`.
- **Caso de uso:** CLIENTA (clienta) sube archivos (correcciones, audios, fotos, documentos) a la carpeta Drive. La sync los baja a esta carpeta local en ≤5 min.
- Equivalentemente, lo que yo guarde aquí aparece en Drive y ella lo ve.
- **Pendiente:** aún no se ha configurado. Esperar OK explícito de INTERLOCUTOR para `rclone bisync --resync` inicial.

## 7. Repositorio git (laptop + servidor fan)

**Estado:** **NO creado todavía.** Pendiente.

- Plan: `git init` en ``, primer commit, después replicar a servidor fan vía la pipeline que INTERLOCUTOR ya tiene.
- Esperar instrucción "cámbialo" o similar para ejecutar. NO hacer por mi cuenta.

## 8. Procedimientos operativos

### Re-transcribir audios (si se borran o se agregan nuevos)

```bash
cd _analisis
python3 transcribir_audios.py
```

Usa `faster-whisper` local, modelo `small` int8, CPU. Sin API, sin cuota.

### Detector de argentinismos en el repo

```bash
cd LotaIndomito
find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.py" \) ! -path "*/transcripciones/*" \
  | xargs grep -niE "\bvos\b|\btenés\b|\btenes\b|\bquerés\b|\bqueres\b|\bsos\b|\bpo\b|\bche\b|..." 
```

(Ver `decisiones.md` para el patrón regex completo.)

## Live test 15:53:45
