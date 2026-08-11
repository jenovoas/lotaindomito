#!/usr/bin/env bash
# ============================================================================
# _scripts/propagar_respuestas_pendientes.sh
# ----------------------------------------------------------------------------
# Aplica la propagación de respuestas a las 3 preguntas del doc 12 a los
# documentos afectados. NO especula contenido: solo refleja lo decidido.
#
# Uso:
#   bash _scripts/propagar_respuestas_pendientes.sh buses|roles|pila|todo
#
# Comandos:
#   buses  → Pregunta 1 (SOMA vs Redis Pub/Sub)
#   roles  → Pregunta 2 (roles MVP módulos Sentinel)
#   pila   → Pregunta 3 (la clienta elige la opción)
#   todo   → ejecutar los 3 en orden
#
# Requisito: leer _analisis/12_inputs_pendientes_de_interlocutor.md para
# entender qué pregunta hace cada comando.
#
# IMPORTANTE:
# - Este script NO edita contenido técnico. Solo refleja lo que tú decides.
# - Antes de correr, asegurarte de que tienes la respuesta clara para esa
#   pregunta en particular.
# - El script es idempotente: si lo corres dos veces con la misma respuesta,
#   no rompe nada (los mensajes ya están marcados).
# - Si el script aborta, revisar el log y corregir manualmente.
# ============================================================================

set -euo pipefail

REPO="/home/jnovoas/Proyectos/LotaIndomito"
DOC12="_analisis/12_inputs_pendientes_de_interlocutor.md"
DEC="docs/decisiones.md"

if [[ ! -f "$REPO/$DOC12" ]]; then
  echo "ERROR: no existe $REPO/$DOC12"
  exit 1
fi

accion=${1:-}

case "$accion" in
  buses)
    echo "→ Pregunta 1: SOMA vs Redis Pub/Sub"
    echo "  Revisar _analisis/12_inputs_pendientes_de_interlocutor.md pregunta 1."
    echo "  Después, abrir docs/decisiones.md D-010-A y:"
    echo "    - Quitar ítem 'Coexistencia de buses de eventos' del bloque 'R&D abierto'."
    echo "    - Marcar la decisión tomada en 'Lo que se decidió' (agregar nueva entrada)."
    echo "    - Actualizar _analisis/11_borrador_propuesta_fondo.md sección 4.2:"
    echo "      * Quitar nota 'R&D abierto (decisión de INTERLOCUTOR): coexistencia de buses'."
    echo "      * Reflejar la arquitectura de buses definitiva."
    echo "    - Marcar pregunta 1 como resuelta en $DOC12."
    ;;
  roles)
    echo "→ Pregunta 2: Roles específicos módulos MVP"
    echo "  Revisar _analisis/12_inputs_pendientes_de_interlocutor.md pregunta 2."
    echo "  Después, abrir docs/decisiones.md D-010-A y:"
    echo "    - Actualizar columna 'Rol propuesto en el juego' con confirmación o refinamiento."
    echo "    - Actualizar columna 'MVP / Fase posterior' según respuesta a pregunta 4."
    echo "    - Quitar 'Pendiente' del título D-010-A si todo confirmado."
    echo "    - En _analisis/11_borrador_propuesta_fondo.md sección 4.2:"
    echo "      * Reflejar módulos MVP confirmados y sus roles."
    echo "      * Quitar nota 'Bloqueado por: confirmación de roles específicos.'"
    echo "    - En _analisis/09_presupuesto_referencial.md:"
    echo "      * Ajustar tarifa de INTERLOCUTOR al alcance real del MVP."
    echo "    - En _analisis/08_carta_gantt_3_semanas.md:"
    echo "      * Ajustar cronograma al alcance real."
    echo "    - Marcar pregunta 2 como resuelta en $DOC12."
    ;;
  pila)
    if [[ -z "${2:-}" ]]; then
      echo "ERROR: para 'pila' necesitas indicar A o B como segundo argumento."
      echo "Uso: bash $0 pila A"
      echo "     bash $0 pila B"
      exit 2
    fi
    opcion=${2^^}
    if [[ "$opcion" != "A" && "$opcion" != "B" ]]; then
      echo "ERROR: opción debe ser A o B, recibí '$2'"
      exit 2
    fi
    echo "→ Pregunta 3: la clienta eligió la opción $opcion"
    echo "  Después, abrir docs/decisiones.md P-004 y:"
    echo "    - Cambiar 'abierto' por 'cerrado (fecha): la clienta eligió la opción $opcion'."
    echo "    - Marcar decisión en 'Decisiones tomadas'."
    echo "    - En _analisis/10_opciones_tecnologicas_para_clienta.md:"
    if [[ "$opcion" == "A" ]]; then
      echo "      * Mantener como comparativa o reescribir como opciones para web progresiva."
    else
      echo "      * Reescribir enfocando en Rust/lota-server, o mantener como comparativa para anexo."
    fi
    echo "    - En _analisis/11_borrador_propuesta_fondo.md sección 4:"
    echo "      * Eliminar rama 'Si Opción A/B' y dejar rama $opcion completa."
    echo "    - En _analisis/09_presupuesto_referencial.md:"
    echo "      * Eliminar rama no elegida."
    echo "    - Marcar pregunta 3 como resuelta en $DOC12."
    ;;
  todo)
    echo "Ejecutando propagación completa (3 pasos)..."
    echo
    echo "PASO 1: buses"
    bash "$0" buses
    echo
    echo "PASO 2: roles"
    bash "$0" roles
    echo
    echo "PASO 3: pila"
    echo "  Antes de correr 'pila', la clienta debe haber elegido."
    echo "  Luego corre: bash $0 pila A  (o B)"
    ;;
  *)
    echo "Uso: bash $0 {buses|roles|pila|todo} [A|B]"
    echo "  buses  → propaga respuesta a Pregunta 1"
    echo "  roles  → propaga respuesta a Pregunta 2"
    echo "  pila   → propaga respuesta a Pregunta 3 (requiere A o B)"
    echo "  todo   → muestra el orden recomendado"
    exit 1
    ;;
esac

echo
echo "Hecho. Verificar con grep que las referencias estén actualizadas:"
echo "  grep -rn 'Pendiente' $REPO/docs/decisiones.md $REPO/_analisis/11_borrador_propuesta_fondo.md | head -10"
echo "  grep -rn 'P-004' $REPO/docs/decisiones.md | head -5"