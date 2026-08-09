# Lota Indómito — Lota Indómito
## Resumen de sesión 2026-08-09 (Hermes, modelo opencode-pro vía omniroute)

---

## 1. Ubicación del proyecto

- **Raíz**: ``
- **Prototipo Stitch del cliente**: `stitch_lota_ind_mito_ciudad_museo_gamificada/`
- **Doc técnico del prototipo**: `stitch_lota_ind_mito_ciudad_museo_gamificada/documento_t_cnico_lota_ind_mito.md`
- **Cada pantalla**: carpeta con `code.html` + `screen.png`
- **Audios del cliente (WhatsApp)**: pendientes de descarga por INTERLOCUTOR en `~/Proyectos/`

---

## 2. Producto

**Lota Indómito** — ciudad-museo interactiva y gamificada de Lota (Chile), territorio carbonífero.
- **Concepto**: "Experiencia Empírica" (aprendizaje vivencial).
- **Narrativa**: usuario = "Explorador del Carbón" / "Guardián de la Memoria".
- **Eje tecnológico**: Realidad Aumentada (reconstrucciones de ruinas + visibilización de oficios).

---

## 3. Dos modos de uso

| Modo | Color acento | Perfil | Mecánicas |
|---|---|---|---|
| **Jugador** | Turquesa #3FE6C0 | Explorador | Desafíos AR, rankings, recompensas, misiones |
| **Turista** | Coral #F5A285 | Visitante | Contemplación, audioguías, AR histórica, paseo guiado |

*(El usuario puede alternar entre modos desde su perfil.)*

---

## 4. 8 rutas / itinerarios

1. **Ruta de las Bodegas** — Logística industrial. Misión: "El Inventario del Carbón".
2. **Ruta Geositio** — Valor geológico. Misión: "El Geólogo del Tiempo" (RA para estratos).
3. **Ruta del Comercio** — Conexión con pymes. Misión: "El Trueque Lota" (canje de Carboncillos).
4. **Camina Lota** — Urbanismo social y pabellones. Misión: "Arquitecto de Pabellones" (selfies comparativas).
5. **Ruta Costera** — Borde mar y muelles. Misión: "Vigía del Golfo".
6. **Ruta Indómita** — Naturaleza recuperada. Misión: "Rastreador de la Flora".
7. **Oficios de Mar** — Patrimonio Inmaterial. Misión: "Chinchorreando en el Blanco".
8. **Fuego y Carbón** — Gastronomía y artesanía. Misión: "Amasando Pan".

---

## 5. Gamificación

- **Moneda virtual**: **Carboncillos** (canjeables en locales asociados).
- **Medallas**: "Ojo de Lince" (reportes), "Amasadora de Memorias" (pan), "Vigía de la Cuenca".
- **Rangos**: Aprendiz → Capataz → Leyenda de la Cuenca.
- **Modos de juego**: Individual / Familia (roles Vigía, Cronista, Fotógrafo) / Ranking.
- **Personajes AR**:
  - Isidora Goyenechea (Parque de Lota)
  - El Ciego de la Mina (Piques)
  - La Chinchorrera Mayor (Costa)
  - El Palanquero (Ferrocarriles)

---

## 6. Funcionalidades app (UI/UX)

- **Onboarding**: escaneo QR en tótems de entrada (captura métricas iniciales).
- **Mapa Interactivo**: POIs + rutas.
- **Módulo RA**: cámara para reconstrucciones 3D + filtros de oficios.
- **Billetera Digital**: Carboncillos + cupones de canje.
- **Bóveda de Diplomas**: certificados PDF compartibles.
- **Gobernanza Colaborativa (Citizen Science)**: botón de Reporte (basura, derrumbe, seguridad) → validación cooperativa → alerta Municipio/CMN → notificación de solución.

---

## 7. Perfiles de usuario

- Avatar y estatus (nivel + medallas).
- Dashboard de Ciudadanía: seguimiento de reportes institucionales.
- Historial de Impacto: métricas de ayuda a familias locales + calorías quemadas.

---

## 8. Ecosistema backend (alianzas)

- **Dashboard Autoridades** (Municipio): mapa de calor de incidencias.
- **Panel Comerciantes**: validación de QR para canjes + métricas de flujo.
- **Cooperativa de Trabajo**: administración de beneficios + curatoría de contenido.

---

## 9. Estética visual (de la pantalla "selección de modo")

- **Fondo**: negro/gris muy oscuro, textura cuadriculada sutil.
- **Acento primario**: turquesa/menta #3FE6C0 (modo Jugador + moneda).
- **Acento secundario**: durazno/coral #F5A285 (modo Turista).
- **Acento terciario**: cobre/naranja oxidado #D17A4F (logo, "Carboncillo").
- **Tipografía**: display gruesa, condensada e inclinada (cinetipo/cartel).
- **Efectos**: glow suave sobre iconos, badges con borde, líneas tipo "grieta/estrato".
- **Estilo**: retro-industrial + futurista-gamer. Misterio + acción + contemplación.
- **Idioma**: español localizado (chileno/lotino: "mina", "Chiflón del Diablo").

---

## 10. Inventario de pantallas del prototipo Stitch

~50 carpetas, una por pantalla. Ejemplos:
- `selecci_n_de_modo_lota_ind_mito/` ✅ analizada (vista + descripción)
- `mapa_interactivo_y_misiones/` ⏳ pendiente vision_analyze
- `encuentro_ar_el_ciego_de_la_mina/` ⏳ pendiente
- `dashboard_de_ciudadan_a_reportes_1/`, `dashboard_de_ciudadan_a_reportes_2/`
- `dashboard_de_familia_el_clan_minero/`, `family_dashboard_english_version`
- `monumento_chifl_n_del_diablo/`, `monumento_pabell_n_83/`, `monumento_pabell_n_83_detalle/`, `monumento_parque_de_lota/`, `monumento_teatro_de_lota/`
- `mapa_de_lota_*` (varias variantes de iconografía)
- `misi_n_*` (varias: amasando pan, arquitecto de pabellones, oficios de mar, etc.)
- `modo_familia_selecci_n_de_roles/`, `family_mode_english_version`
- `pasaporte_ind_mito_*` (selector, perfil, versiones EN)
- `b_veda_de_*` (beneficios, certificados, recompensas)
- `canje_*` (canje de carboncillos feria, canje exitoso ficha)
- `captura_de_memoria_c_mara/`, `desaf_o_vig_a_del_golfo/`
- `ruta_*` (varias: bodegas, caminata, comercio, geositio, fuego y carbón)
- `selecci_n_de_modo_lota_ind_mito/`
- Versiones en inglés: `*_english_version` (mapa, pasaporte, family dashboard, team mission, mission complete)

> Nota: vision_analyze dio 503 (cuota saturada) tras la primera pantalla. Continuar análisis visual cuando el servicio responda.

---

## 11. Pendientes para próxima sesión

1. **Audios WhatsApp del cliente**: INTERLOCUTOR los descarga a `~/Proyectos/`. Sin ellos no se puede extraer alcance real (lo del prototipo puede no coincidir con lo que el cliente pide verbalmente).
2. **Transcripción de audios** (Whisper) → análisis de requisitos vs prototipo.
3. **Cruzar doc técnico del prototipo vs requisitos del cliente en audio** → identificar gaps.
4. **Completar análisis visual** del resto de pantallas del Stitch (cuando vision_analyze responda).
5. **Síntesis de propuesta**: tecnología, arquitectura, costos, plazos, hitos.

---

## 12. Archivos creados en la sesión

- `_analisis/00_resumen_sesion.md` (este documento)

---

## 13. Contexto de la sesión

- **Sesión activa**: `20260809_133724_2a7128` (recuperada al iniciar)
- **Modelo**: opencode-pro (omniroute, plan free-stack con fallback opencode)
- **MEMORY.md aplicado**: reglas anti-sabotaje, razonar en español, brevedad, no quemar cuota, no tocar trabajo de INTERLOCUTOR sin "cámbialo".
