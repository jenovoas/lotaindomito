#!/usr/bin/env bash
# ============================================================================
# _scripts/archivar_sesion_20260809.sh
# ----------------------------------------------------------------------------
# Archiva los documentos de la sesión 2026-08-09 a _analisis/archive/
# cuando todas las preguntas pendientes del doc 12 estén resueltas.
#
# Uso:
#   bash _scripts/archivar_sesion_20260809.sh
#
# Pre-condición:
#   - Las 3 preguntas de _analisis/12_inputs_pendientes_de_interlocutor.md
#     están marcadas como resueltas (o eliminadas del bloque pendientes).
#   - Has corrido bash _scripts/propagar_respuestas_pendientes.sh todo (o
#     cada paso: buses, roles, pila A/B).
#
# Qué hace:
#   1. Crea _analisis/archive/2026-08-09/ si no existe.
#   2. Mueve los docs de sesión (12_inputs_pendientes_*, 13_resumen_sesion_*)
#      al directorio de archivo con sufijo _archived_20260809.
#   3. NO edita los docs principales. NO modifica el contenido.
#   4. NO toca los archivos de INTERLOCUTOR (06_investigacion_*,
#      07_propuesta_arquitectura_*) ni los .conflict1/.conflict2.
#
# Reversible:
#   mv _analisis/archive/2026-08-09/<archivo> _analisis/
# ============================================================================

set -euo pipefail

REPO="/home/jnovoas/Proyectos/LotaIndomito"
ARCHIVE_DIR="$REPO/_analisis/archive/2026-08-09"

DOCS_A_ARCHIVAR=(
  "_analisis/12_inputs_pendientes_de_interlocutor.md"
  "_analisis/13_resumen_sesion_20260809.md"
)

if [[ ! -d "$REPO/_analisis" ]]; then
  echo "ERROR: no existe _analisis/"
  exit 1
fi

mkdir -p "$ARCHIVE_DIR"
echo "→ Carpeta de archivo: $ARCHIVE_DIR"
echo

# Verificar que las 3 preguntas están resueltas en doc 12 antes de archivar
DOC12="$REPO/_analisis/12_inputs_pendientes_de_interlocutor.md"
if [[ -f "$DOC12" ]]; then
  echo "Verificando que las 3 preguntas estén resueltas en doc 12..."
  echo "  (Si alguna sigue como 'abierta' o 'pendiente', el script aborta.)"
  echo
  for preg in "Pregunta 1" "Pregunta 2" "Pregunta 3"; do
    # Buscar el número de pregunta
    line=$(grep -n "^## ${preg} —\|^## ${preg} -" "$DOC12" 2>/dev/null | head -1 | cut -d: -f1)
    if [[ -z "$line" ]]; then
      echo "  - No se encontró $preg en doc 12 (puede haber sido renombrada/archivada)."
      continue
    fi
    # Ver las siguientes 30 líneas para marcadores de resuelta
    context=$(sed -n "${line},$((line+30))p" "$DOC12" 2>/dev/null)
    if echo "$context" | grep -qiE "resuelt|cerrad|✓|x.*cerr"; then
      echo "  ✓ $preg: resuelta"
    else
      echo "  ✗ $preg: SIGUE ABIERTA — abortando"
      echo "    Resolverla primero con: bash _scripts/propagar_respuestas_pendientes.sh"
      exit 3
    fi
  done
  echo
fi

# Archivar docs
for doc in "${DOCS_A_ARCHIVAR[@]}"; do
  full="$REPO/$doc"
  if [[ -f "$full" ]]; then
    nombre=$(basename "$doc")
    destino="$ARCHIVE_DIR/$nombre"
    echo "→ Moviendo $doc → _analisis/archive/2026-08-09/$nombre"
    mv "$full" "$destino"
  else
    echo "  (no existe $doc, omitido)"
  fi
done
echo

# Limpiar referencias en otros docs (no automático — listar solo)
echo "→ Acciones manuales restantes (NO automáticas, las haces tú):"
echo "  1. En docs/estado.md sección 9.3:"
echo "     - Cambiar 'Inputs pendientes de INTERLOCUTOR y de Fabiola (centralizado)' por 'Resumen histórico de sesión 2026-08-09 (archivado)'."
echo "     - Quitar referencias a doc 12."
echo "  2. En docs/decisiones.md P-004 (si quedó abierta):"
echo "     - Ya debe estar cerrada tras propagar 'pila A/B'."
echo "  3. En _analisis/11_borrador_propuesta_fondo.md sección 4:"
echo "     - Quitar nota 'Bloqueado por: confirmación de roles específicos' y 'Bloqueado por elección de Fabiola'."
echo "  4. En _analisis/08_carta_gantt_3_semanas.md y _analisis/09_presupuesto_referencial.md:"
echo "     - Quitar notas de bloqueo."
echo "  5. En _analisis/10_opciones_tecnologicas_para_clienta.md:"
echo "     - Quitar referencia a doc 12 (ahora archivado)."
echo
echo "→ Hecho. Para revertir: mv _analisis/archive/2026-08-09/<archivo> _analisis/"