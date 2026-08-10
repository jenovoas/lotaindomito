# ML externo para análisis de comportamiento — Lota Indómito

> **Documento de diseño conceptual.**
> **Fecha:** 2026-08-10.
> **Destinatario:** INTERLOCUTOR (Jaime), para discusión antes de bajar a mecánica.
> **Encuadre:** D-014 (turismo + comercio local, motor/Sentinel como centro) + D-006 (PostgreSQL + PostGIS como backend) + D-007 (Vue 3 PWA cliente) + D-016 propuesta (sistema multi-moneda de minerales, ver [`_analisis/23_sistema_monedas_minerales.md`](23_sistema_monedas_minerales.md)).
> **Decisión propuesta:** montar un **servicio de ML externo** que consume directamente la base de datos del juego, entrena modelos sobre comportamiento de usuarios, predice tendencias y entrega **dashboards accionables** para Fabiola, Municipios y comercio local.

---

## 0. Tesis central

El juego no es solo una experiencia para turistas. Es un **sensor** que produce datos accionables sobre tres dimensiones:

1. **Comercial:** qué minerales se canjean, dónde, cuándo, por qué.
2. **Social:** cómo se relacionan los jugadores entre sí, qué patrones de trueque emergen.
3. **Turística:** cómo se mueven los turistas por Lota, qué zonas prefieren, qué los retiene.

Estos datos, agregados y anonimizados, son **insumo directo para los municipios** que toman decisiones de inversión en infraestructura, promoción turística, eventos y temporadas. **Un municipio informado por datos reales del juego es un municipio que puede justificar gasto y medir impacto.**

El ML externo convierte a Lota Indómito de "juego entretenido" a **plataforma de inteligencia turística + comercial**.

---

## 1. Por qué ML externo (no en runtime)

| Criterio | ML externo (esta propuesta) | ML en runtime del juego |
|---|---|---|
| **Regla "0 floats en CPU" del motor S60** | No aplica (corre en Python externo) | Rompe la regla si es en S60 |
| **Costo computacional** | Se ejecuta en batch / programado | Cada request consume cómputo |
| **Privacidad** | Procesa datos ya almacenados | Procesa datos en tiempo real (más expuesto) |
| **Complejidad técnica** | Servicio Python independiente | Integrado al binario `lota-server` |
| **Latencia** | Batch (no tiempo real) | Tiempo real |
| **Casos de uso típicos** | Análisis, predicción, dashboards | Recomendaciones in-game, anti-fraude en vivo |

**Recomendación:** **ML externo en batch** para análisis, predicción y dashboards. Si más adelante se necesitan recomendaciones in-game o anti-fraude en vivo, evaluar servicio de inferencia separado (también Python, también externo).

---

## 2. Acceso directo a la base de datos

El ML lee directamente de la DB del juego (PostgreSQL + PostGIS, decisión D-006). Razones:

- **Los datos ya están ahí.** No tiene sentido duplicar ni construir un pipeline ETL complejo.
- **Vistas materializadas** permiten acceso de solo-lectura sin impactar el rendimiento del juego.
- **PostGIS** habilita queries geoespaciales eficientes (heatmaps, path analysis).
- **Time-series extension** (TimescaleDB opcional) si el volumen lo justifica.

**Consideraciones:**
- El servicio de ML corre con un **usuario de DB de solo lectura**, sin permisos de escritura.
- Las vistas materializadas se refrescan con periodicidad configurable (ej. cada 5 min para datos casi-en-vivo, o cada hora para análisis pesados).
- Si la DB es local en el servidor fan de INTERLOCUTOR, el servicio de ML también corre ahí. Si la DB migra a nube, el ML migra con ella.

**Decisión abierta:** ¿DB local en el fan de INTERLOCUTOR o nube (RDS, Supabase)? Afecta arquitectura del ML.

---

## 3. Objetivos en tres dimensiones

### 3.1 Dimensión comercial

| Objetivo | Métrica | Caso de uso |
|---|---|---|
| **ROI por World Event para el comercio** | Cupones usados / cupones emitidos × ticket promedio | Comercios evalúan si conviene participar |
| **Demanda predicha por fecha** | Predicción de visitas/minerales canjeados por fecha | Comercio planifica stock y personal |
| **Tipo de cambio óptimo del comercio** | Análisis de qué tipo de cambio maximiza uso de cupones | Comercios ajustan política de aceptación |
| **Análisis de minerales** | Qué mineral entra/sale del comercio | Comercios identifican preferencias |
| **Comparación entre comercios** | Ranking de uso de cupones, ticket promedio | Municipio identifica comercios exitosos |

### 3.2 Dimensión social

| Objetivo | Métrica | Caso de uso |
|---|---|---|
| **Patrones de transferencia** | Quién envía a quién, qué minerales, cuánto | Detectar usuarios centrales, ligas, reciprocidad |
| **Trueques emergentes** | Pares más comunes de trueque, tasas de éxito | Diseñar misiones que incentiven cooperación |
| **Red social del juego** | Grafo de transferencias, centralidad, comunidades | Entender estructura social, diseñar features |
| **Engagement colectivo** | % de usuarios activos que interactúan con otros | Medir "viralidad" interna |
| **Detección de abuso** | Patrones anómalos de transferencia (lavado, farming) | Sistema anti-fraude |

### 3.3 Dimensión turística

| Objetivo | Métrica | Caso de uso |
|---|---|---|
| **Heatmaps de visitación** | Densidad de turistas por zona × horario | Municipio decide inversión en infraestructura |
| **Path analysis** | Recorridos típicos entre zonas | Diseñar rutas y señalética |
| **Tiempo en zona** | Permanencia promedio por POI | Identificar puntos de interés subutilizados |
| **Estacionalidad** | Visitas por mes, semana, día de semana | Municipio planifica promoción |
| **Demografía de turistas** | Origen geográfico (si hay datos), rango etario inferido | Municipio ajusta marketing |
| **Retención** | D+1, D+7, D+30 por cohorte | Validar el loop de retorno definido en `20_*` |
| **Satisfacción in-app** | Si hay encuestas o ratings, análisis de sentimiento | Detectar pain points |

---

## 4. Casos de uso priorizados

### 4.1 Alta prioridad (piloto + fase 1)

1. **Heatmap de visitación por zona y horario** — bajo costo de cómputo, alto valor para municipio.
2. **Análisis de conversión de misiones** — instrumentación mínima en PWA, valor para INTERLOCUTOR.
3. **ROI por World Event para comercio** — datos directos del cupón, valor para comercio.
4. **Reporte de comportamiento agregado para municipio** — entrega en formato dashboard o PDF mensual.

### 4.2 Prioridad media (fase 1)

5. **Predicción de demanda por fecha** — requiere histórico suficiente (3-6 meses).
6. **Segmentación de turistas** — KMeans sobre features de comportamiento.
7. **Análisis de red social (grafos de transferencia)** — NetworkX, visualizaciones.
8. **Predicción de retención por cohorte** — modelos de supervivencia.

### 4.3 Prioridad baja (fase 2+)

9. **Recomendación personalizada al turista** — collaborative filtering o reglas.
10. **Detección de fraude avanzada** — modelos de anomalía.
11. **Análisis de sentimiento en feedback** — NLP sobre encuestas o comentarios.
12. **Optimización automática de ratios de cambio** — reinforcement learning.

---

## 5. Datos a recolectar (instrumentación mínima del piloto)

Para que el ML tenga material, hay que recolectar desde el día 1. El piloto debe definir qué eventos se loggean:

### 5.1 Eventos del turista

| Evento | Schema sugerido |
|---|---|
| `user_session_start` | `{user_id, timestamp, lat, lng, mode}` |
| `user_session_end` | `{user_id, timestamp, duration_s}` |
| `poi_visit` | `{user_id, poi_id, timestamp, duration_s}` |
| `world_event_join` | `{user_id, event_id, timestamp}` |
| `mission_complete` | `{user_id, mission_id, timestamp, success, mineral_earned}` |
| `world_event_complete` | `{user_id, event_id, timestamp}` |
| `coupon_redeemed` | `{user_id, coupon_id, commerce_id, timestamp, mineral_amount}` |
| `passport_update` | `{user_id, completion_pct, timestamp}` |

### 5.2 Eventos sociales

| Evento | Schema sugerido |
|---|---|
| `transfer_sent` | `{from_user, to_user, mineral_type, amount, timestamp, channel}` |
| `transfer_received` | `{to_user, from_user, mineral_type, amount, timestamp}` |
| `trade_offered` | `{from_user, to_user, offer_json, timestamp}` |
| `trade_accepted` | `{from_user, to_user, exchange_json, timestamp}` |
| `gift_sent` | `{from_user, to_user, mineral_type, amount, message, timestamp}` |

### 5.3 Eventos de comercio

| Evento | Schema sugerido |
|---|---|
| `commerce_registered` | `{commerce_id, name, location, accepted_minerals, exchange_rates}` |
| `coupon_issued` | `{coupon_id, commerce_id, mineral_type, amount, expiry, world_event_id}` |
| `coupon_used` | `{coupon_id, commerce_id, user_id, timestamp, real_amount_clp}` |
| `commerce_mineral_received` | `{commerce_id, mineral_type, amount, timestamp, source}` |

### 5.4 Privacidad desde el diseño

- **Anonimización en reposo**: `user_id` es un UUID opaco, no derivado de email/teléfono.
- **Agregación antes de exponer**: ningún reporte incluye usuarios individuales identificables.
- **Opt-in explícito** en el onboarding del juego: el usuario acepta el uso de datos anónimos para mejora del servicio.
- **Cumplimiento legal:** Ley 19.628 de Protección de Datos Personales de Chile.
- **Retención**: logs de eventos con `user_id` seudónimo se conservan por 24 meses y luego se agregan permanentemente.

---

## 6. Arquitectura propuesta

```
┌──────────────────────┐
│  PWA Cliente (Vue)   │ ── eventos anónimos ──┐
└──────────────────────┘                        │
                                                ▼
┌──────────────────────────────────────────────────────────────┐
│  PostgreSQL + PostGIS (Decisión D-006)                       │
│  ├── Tablas operacionales (game state, wallet, etc.)         │
│  └── Vistas materializadas (eventos anónimos agregados)      │
└──────────────────────────────────────────────────────────────┘
                │                                │
                │ read-only                      │ read-only
                ▼                                ▼
┌─────────────────────────┐    ┌─────────────────────────────┐
│  Servicio ML (Python)   │    │  Servicio ML (Python)       │
│  - Batch diario         │    │  - Batch semanal            │
│  - Heatmaps, funnels    │    │  - Predicción demanda       │
│  - Anti-fraude básico   │    │  - Segmentación             │
└─────────────────────────┘    └─────────────────────────────┘
                │                                │
                ▼                                ▼
┌──────────────────────────────────────────────────────────────┐
│  Dashboard Web (estático o app liviana)                      │
│  ├── Vista Fabiola: KPIs globales, salud del juego           │
│  ├── Vista Municipio: heatmaps, demografía, estacionalidad   │
│  ├── Vista Comercio: ROI por evento, minerales recibidos     │
│  └── Vista INTERLOCUTOR: comportamiento, retención, fraude   │
└──────────────────────────────────────────────────────────────┘
```

**Stack sugerido (a confirmar en fase de implementación):**

- **ML service:** Python 3.12, scikit-learn, XGBoost, Prophet, NetworkX, GeoPandas.
- **Visualización:** Streamlit o Dash (liviano) o Grafana (más estándar).
- **Orquestación:** cron simple + Airflow si crece.
- **Almacenamiento de modelos:** MLflow o simple filesystem versionado.

---

## 7. Lo que se puede hacer en el piloto de 30 días

El piloto NO entrena modelos complejos. Sí puede:

| Componente | Alcance piloto |
|---|---|
| **Instrumentación** | Implementar los 16 eventos definidos en §5. Backend mínimo para recibirlos y almacenarlos. |
| **Vistas materializadas** | 2-3 vistas básicas: `events_per_user_per_day`, `commerce_coupon_redemption`, `visits_per_zone_per_hour`. |
| **Dashboard estático** | Una página web simple que muestra las 3 vistas. Refresh manual. |
| **Reporte manual** | Un PDF mensual con las 3 dimensiones (comercial, social, turística) que se entrega a Fabiola y Municipio. |
| **1 modelo simple** | Predicción de retención D+1 con regresión logística (con datos sintéticos si no hay suficientes reales). |

**Lo que se difiere a fase 1:** todos los modelos priorizados en §4.2 y §4.3.

---

## 8. Privacidad y regulación

**Ley 19.628 (Chile) — Protección de Datos Personales:**

- El juego **no recolecta datos personales identificables** (email, teléfono, RUT) en el flujo normal.
- El `user_id` es seudónimo (UUID aleatorio).
- Los datos agregados que se entregan al Municipio **nunca contienen usuarios individuales**.
- El opt-in se solicita al crear la cuenta: "Acepto el uso de datos anónimos para mejorar el servicio".

**Buenas prácticas adicionales:**

- **Logs encriptados** en reposo.
- **Acceso al servicio ML restringido** por IP / VPN.
- **Auditoría** de quién consulta qué datos y cuándo.
- **Retención limitada** y agregación permanente.

---

## 9. KPIs del sistema de ML

Para validar que el sistema está dando valor:

| KPI | Meta piloto | Meta fase 1 |
|---|---|---|
| Eventos recibidos / día | 1.000 | 50.000 |
| Cobertura de eventos definidos | 100% de §5.1-5.3 | 100% + eventos avanzados |
| Tiempo de refresh del dashboard | Manual (<24h) | <1h automático |
| Reportes entregados a Municipio | 0 (no hay volumen) | 1/mes |
| Precisión de predicción de retención D+1 | N/A (datos sintéticos) | >70% |
| Precisión de predicción de demanda | N/A | MAPE <20% |
| Comercios que reciben dashboard activo | 0 | >50% |

---

## 10. Decisiones abiertas

1. **¿DB local (servidor fan) o nube?**
   - Local: costo bajo, control total.
   - Nube: escalabilidad, redundancia.
   - **Recomendación:** local para piloto, evaluar nube para fase 1.

2. **¿Stack Python confirmado?**
   - scikit-learn, XGBoost, Prophet son estándar.
   - ¿Alguna preferencia por PyTorch? (innecesario para el alcance actual).

3. **¿Quién opera el servicio de ML?**
   - INTERLOCUTOR mismo.
   - Fabiola contratando a un data scientist.
   - Servicio externo contratado.
   - **Recomendación:** INTERLOCUTOR para piloto, decidir para fase 1.

4. **¿El dashboard es público o restringido?**
   - Versión pública (anonimizada) para Municipio y Comercio.
   - Versión privada con más detalle para INTERLOCUTOR/Fabiola.
   - **Recomendación:** dos versiones.

5. **¿Los datos del Municipio se entregan en tiempo real o como reporte mensual?**
   - Tiempo real: requiere dashboard siempre actualizado.
   - Mensual: PDF con resumen.
   - **Recomendación:** dashboard siempre actualizado (costo bajo con vistas materializadas) + reporte mensual resumido.

6. **¿Hay un modelo de costos para el Municipio?** ¿Pagan por el dashboard? ¿Es parte del fondo?
   - Esto define si el ML es feature del producto o servicio aparte.

---

## 11. Referencias cruzadas

- **Loop del jugador:** [`_analisis/20_loop_jugador_dia_a_dia.md`](20_loop_jugador_dia_a_dia.md) — los KPIs de retención D+1/D+7/D+30 se miden con el ML descrito aquí.
- **World Events:** [`_analisis/21_world_events_d014.md`](21_world_events_d014.md) — el ML mide el ROI de cada World Event para el comercio.
- **Sistema multi-moneda:** [`_analisis/23_sistema_monedas_minerales.md`](23_sistema_monedas_minerales.md) — los modelos miden comportamiento con cobre/oro/estaño, no Carboncillos.
- **D-006:** `docs/decisiones.md` — PostgreSQL + PostGIS como backend, fuente de datos del ML.
- **D-007:** `docs/decisiones.md` — Vue 3 PWA como cliente; emite los eventos que el ML consume.
- **D-014:** `docs/decisiones.md` — el ML refuerza D-014 al entregar datos accionables para Municipios.
- **Postulación al fondo:** `_analisis/11_borrador_propuesta_fondo.md` — el ML es un argumento de venta adicional para el Municipio.
