# Cotejo: Lo que dice CLIENTA vs Lo que propone el Prototipo Stitch
**Cliente:** CLIENTA (audios 2026-08-07)
**Prototipo:** Stitch `stitch_lota_ind_mito_ciudad_museo_gamificada/`
**Doc prototipo:** `documento_t_cnico_lota_ind_mito.md`

---

## ✅ Lo que el prototipo SÍ cubre del brief del cliente

| Ítem audios | Lo que tiene el prototipo |
|---|---|
| App gamificada de turismo cultural | ✓ "Ciudad Museo Gamificada" |
| Visitar sectores culturales vía interfaz de juego | ✓ 8 rutas con misiones |
| Estadísticas de participación | ✓ Historial de Impacto + Dashboard Ciudadanía |
| Alertas de zonas de peligro | ✓ Botón Reporte (basura, derrumbe, seguridad) |
| Datos al municipio / instituciones patrimoniales | ✓ Dashboard Autoridades + Cooperativa |
| Mecánicas de juego (insignias, diplomas) | ✓ Medallas + Rangos + Bóveda de Diplomas |
| Contador de pasos | ✓ "Historial de Impacto: calorías quemadas" |

**Coincidencia fuerte.** El prototipo es fiel al brief verbal en lo esencial.

---

## ⚠️ Lo que el prototipo AGREGÓ y el cliente NO pidió

Esto es importante: la clienta describe algo más simple. El diseñador infló el alcance:

1. **Realidad Aumentada como eje tecnológico**
   - Clienta: "mediante la interfaz de juego" — no menciona RA.
   - Prototipo: "Tecnología Eje: RA para reconstrucción de ruinas y visibilización de oficios".
   - **Implicación**: RA es mucho más caro y más lento de implementar. Si la clienta nunca lo pidió, es un riesgo de scope.

2. **8 rutas completas** con misiones específicas
   - Clienta: "ciertos sectores" — indefinido.
   - Prototipo: 8 rutas concretas (Bodegas, Geositio, Comercio, Camina Lota, Costera, Indómita, Oficios de Mar, Fuego y Carbón).
   - **Implicación**: cada ruta = contenido, geolocalización, relato histórico, misión. Para 10 palos esto es imposible cubrirlo entero.

3. **Sistema Carboncillos + panel comerciantes + canje en locales**
   - Clienta: NO menciona moneda virtual ni canje comercial.
   - Prototipo: "Canjeables en locales asociados" + "Panel para Comerciantes".
   - **Implicación**: alianza con el comercio local = relación con pymes, integración que toma semanas.

4. **Modo Familia con roles (Vigía, Cronista, Fotógrafo)**
   - Clienta: NO menciona.
   - Prototipo: lo da por hecho como modo central.
   - **Implicación**: dos sets de UI/UX, lógica multiplayer, etc.

5. **Onboarding con tótems QR físicos**
   - Clienta: NO menciona.
   - Prototipo: "Escaneo de QR en tótems de entrada".
   - **Implicación**: requiere instalar tótems físicos (involucra obra, hardware, mantención).

6. **Cooperativa de Trabajo como actor del sistema**
   - Clienta: NO menciona.
   - Prototipo: "Cooperativa de Trabajo: Administración de beneficios y curatoría de contenido".
   - **Implicación**: backend completo de gestión de cooperativa.

7. **Personajes AR con conversaciones**
   - Clienta: NO menciona.
   - Prototipo: 4 personajes RA (Isidora, Ciego, Chinchorrera, Palanquero).

---

## ❌ Lo que el prototipo NO cubre y la clienta SÍ pidió

| Clienta | Prototipo |
|---|---|
| Plazo: **fines de agosto / primera semana de septiembre** | (No es tema del prototipo, pero condiciona todo) |
| Presupuesto: **definido por la clienta** (incluye honorarios y gastos) | El prototipo no dice nada de costos. |
| **Primera etapa / piloto** antes de proyecto grande | El prototipo no diferencia MVP vs. completo. |

**El prototipo es un documento de diseño "ideal", no acotado al presupuesto ni al plazo.**

---

## 🚨 Gaps críticos para la propuesta

### 1. Alineación de expectativas
Antes de hacer cualquier propuesta técnica, **hay que alinear con CLIENTA qué del prototipo es "deseable" y qué es "obligatorio para el piloto"**. El prototipo es aspiracional. Para 10 palos en 3–4 semanas no es realista.

### 2. MVP realista con lo que SÍ está en el brief verbal
Lo que sí se puede hacer en el alcance acotado:
- App/web **mobile-first** (probablemente PWA para evitar stores).
- Mapa interactivo con **3–5 POIs** (no 8 rutas).
- Reporte ciudadano (basura / peligro) → backend simple → dashboard básico municipio.
- Insignias y diplomas digitales (sin RA).
- Estadísticas de uso: visitas, zonas recorridas, reportes.

### 3. RA, Carboncillos, tótems, Cooperativa, Modo Familia → **opcional / fase 2**
Cualquiera de estos individualmente dobla o triplica el alcance. Juntos, son un proyecto de 50+ palos, no 10.

### 4. Asignatura crítica: PRESENTACIÓN DEL FONDO
Lo que CLIENTA necesita en 3 semanas es una **propuesta para postulación**, no el producto terminado. Tal vez el entregable es:
- Doc de proyecto (memoria, alcance, presupuesto).
- **Diseño funcional** (mockups / prototipo Stitch existente).
- **Maqueta navegable** (algunas pantallas funcionales, no backend completo).
- Carta Gantt + equipo + costos.

---

## 📋 Recomendación inmediata (análisis interno, no se manda)

Antes de armar propuesta técnica, **conversar internamente** sobre:
1. ¿Cuál es la **fecha dura** de cierre del fondo? (¿agosto o septiembre?)
2. ¿El entregable es el producto corriendo o la **propuesta para el fondo**?
3. ¿Hay **avales** del Municipio / Cooperativa confirmados o solo intención?
4. ¿Cuántos lugares queremos **mínimo** en el piloto?
5. RA, tótems, Carboncillos, comercio: ¿los ponemos como **idea opcional** o los queremos sí o sí?
