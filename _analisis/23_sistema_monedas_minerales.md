# Sistema de monedas minerales — Lota Indómito

> **Documento de diseño conceptual — decisión D-016 propuesta.**
> **Fecha:** 2026-08-10.
> **Destinatario:** INTERLOCUTOR (Jaime), para discusión antes de bajar a mecánica y antes de actualizar el GDD.
> **Encuadre:** D-014 (turismo + comercio local, motor/Sentinel como centro) + D-007 (Vue 3 + TS PWA).
> **Decisión propuesta:** reemplazar el **Carboncillo** (`₡`) como moneda única del juego por un **sistema multi-moneda de minerales** (cobre, oro, estaño) con tipo de cambio relativo, transferible entre usuarios y comercianteable en el comercio local. **Carboncillos desaparece como moneda**, aunque el "carbón" se mantiene como identidad narrativa del juego (Isidora Goyenechea, el Ciego de la Mina, etc.).

---

## 0. Por qué este cambio

El "Carboncillo" como moneda única funcionaba como gamificación tradicional pero desaprovechaba el potencial social y económico de Lota:

1. **El carbón no es un metal precioso.** Es combustible, no es ahorro. La moneda del juego debería resonar con la identidad minera metálica de Chile (cobre sobre todo) y con la lógica de un sistema económico interno.
2. **Una moneda única no incentiva interacción social.** No hay razón para que un jugador haga trueque con otro si todo tiene el mismo valor nominal.
3. **Un sistema multi-moneda crea economía emergente.** El tipo de cambio, el mercado P2P y la especulación convierten el juego en un ecosistema con vida propia.
4. **Cobre, oro, estaño son símbolos fuertes.** Cobre es símbolo patrio chileno. Oro es universalmente valioso. Estaño es raro y estratégico — encaja con la "rareza S60" del concepto.

**Tesis:** un sistema multi-moneda mineral convierte al juego en un **ecosistema económico** que potencia la interacción social y refuerza D-014 (autofinanciamiento por comercio local).

---

## 1. Catálogo de minerales (MVP)

| Mineral | Símbolo | Valor relativo | Identidad | Rareza |
|---|---|---|---|---|
| **Cobre** | Cu | 1 unidad (base) | Metal del trabajo y del comercio diario | Común |
| **Oro** | Au | 100 cobre | Metal del cielo, de los eventos, de la historia | Media |
| **Estaño** | Sn | 10.000 cobre (= 100 oro) | Metal de los portales S60, de las rarezas, del juego completo | Rara |

**Notas:**
- Los ratios propuestos son **arbitrarios para MVP**. Se afinan con telemetría real del piloto.
- Cada mineral tiene un **lore** asociado en el pasaporte:
  - **Cobre:** "el metal del trueque honrado. Forjado en el calor del comercio de Lota."
  - **Oro:** "el metal del cielo. Aparece cuando la luna, el sol y la historia convergen."
  - **Estaño:** "el metal de la convergencia. Solo aparece cuando los dos carriles del mundo se tocan."

**Decisión abierta:** ¿3 minerales o más? El usuario mencionó cobre, oro, estaño. Otros candidatos: plata (intermedio, complementario al oro), carbón negro (residual, decorativo — ver §10).

---

## 2. Cómo se gana cada mineral

| Acción | Mineral ganado | Cantidad |
|---|---|---|
| Micro-sesión de POI fijo completada | Cobre | 10-50 |
| Reporte ciudadano validado | Cobre | 75 |
| World Event: 1 misión temática completada | Cobre + Oro | 30 cobre + 5 oro |
| World Event: ruta completa del evento | Oro | 100-500 |
| Evento del cielo (astronómico, climático, temporal) | Oro | 20-100 |
| Evento raro (portal S60 — convergencia lattice) | Estaño | 1 |
| Pasaporte digital al 100% completado | Estaño + Diploma | 10 |
| Logro "Leyenda Indómita" (rango máximo) | Estaño + Título | 5 |

**Regla de fuente:** los **portales S60** (diferenciador central del concepto D-014) son la **única fuente consistente de estaño**. Esto ata la rareza del estaño al diferenciador del juego.

**Decisión abierta:** ¿hay límite de estaño total en circulación (deflación) o se genera infinito (inflación)? Recomendación: límite suave para preservar escasez.

---

## 3. Mecánica P2P (entre usuarios)

### 3.1 Modalidades

| Modalidad | Mecánica | Complejidad |
|---|---|---|
| **Transferencia directa** | Jugador A envía X cobre a Jugador B por nickname o QR. Sin intermediario. | Baja |
| **Regalo** | Similar a transferencia, con animación + tarjeta de dedicatoria. | Baja |
| **Trueque bilateral** | Jugador A ofrece X cobre + Y oro a cambio de Z estaño de Jugador B. Aceptación manual. | Media |
| **Mercado abierto** | Libro de órdenes (orden de compra/venta de cada par). Matching automático. | Alta |
| **Subastas** | Puja abierta por una cantidad de mineral. | Alta |

**Recomendación para piloto:** transferencia directa + regalos + trueque bilateral. Mercado abierto y subastas para fase 1.

### 3.2 Canales de transferencia

- **QR**: Jugador A escanea QR de Jugador B → envía. Sin fricción.
- **Nickname/ID**: Jugador A escribe el ID de Jugador B → envía. Fricción leve (typos).
- **Proximidad (Bluetooth/NFC)**: requiere cercanía física. Refuerza el turismo presencial.

**Recomendación para piloto:** QR + nickname. Proximidad para fase 2.

### 3.3 Límites y anti-abuso

- **Límite diario de transferencia** configurable (ej. máximo 1.000 cobre/día por jugador para evitar lavado).
- **Cooldown entre transferencias** (ej. 5 min entre envíos al mismo jugador).
- **Reporte de estafa** con moderación manual.
- **Historial público** en el perfil del jugador (auditoría).
- **Verificación de identidad** opcional (email, teléfono) para levantar límites.

---

## 4. Cómo potencia la interacción social

| Mecánica | Lazo social creado |
|---|---|
| Regalos entre jugadores | Amistad, reciprocidad |
| Trueque bilateral | Cooperación, confianza |
| Mercado abierto | Competencia sana, especulación compartida |
| Misiones en equipo | Trabajo en equipo, coordinación |
| Logros compartidos | Comunidad, identidad grupal |
| Conversión de monedas entre jugadores | Economía emergente |

**El efecto compuesto:** el sistema multi-moneda convierte al juego de "experiencia individual con leaderboard" a "ecosistema social con economía interna". Esto cambia fundamentalmente la retención y el efecto red.

**Ejemplo narrativo:** un turista consigue 1 estaño de un portal S60 → como es raro, otros jugadores le ofrecen trueques interesantes → el estaño circula → el turista termina visitando comercios locales para canjearlo → D-014 activado.

---

## 5. Canje en comercio local (D-014 con multi-moneda)

### 5.1 Cómo acepta el comercio

| Modalidad | Mecánica |
|---|---|
| **Comercio acepta múltiples minerales** | El local define: "acepto cobre, oro. No acepto estaño". |
| **Tipo de cambio del comercio vs del juego** | El juego dice "1 oro = 100 cobre". El comercio puede ofrecer "pago 1 oro = 80 cobre en mi local" — el jugador decide. |
| **Cupón QR multi-moneda** | El cupón especifica: "10% off pagando con oro", "5% off pagando con cobre". |
| **Promociones temáticas** | En Fiestas Patrias, "doble oro en consumos en restaurant X". |

### 5.2 Cómo recibe el comercio

El comercio recibe minerales como **crédito de juego**. Decisión clave: **¿cómo se traduce ese crédito a dinero real?**

| Modelo | Pro | Contra |
|---|---|---|
| **Acumulación → liquidación mensual** | Simple para el comercio | Costo de tesorería para INTERLOCUTOR/Fabiola |
| **Cashback inmediato en CLP** | Sin riesgo para el comercio | Requiere capital de trabajo |
| **Canjes internos** (producto por mineral) | Simple, sin dinero de por medio | Limita flexibilidad |

**Recomendación:** acumulación → liquidación mensual para el piloto. Cashback para fase 1.

### 5.3 Implicaciones para D-014

El sistema multi-moneda refuerza D-014 de formas nuevas:

1. **El comercio no compite solo por "carboncillos gastados"** sino por "mezcla de monedas". Esto crea segmentación: un comercio de café puede preferir cobre (transacciones diarias); un restaurant puede preferir oro (eventos); una panadería puede preferir ambos.
2. **Los jugadores acumulan antes de ir al comercio**, lo que genera tráfico planeado.
3. **El tipo de cambio del comercio crea dinámica de mercado.** Los comercios pueden ajustar su "precio" en cada moneda según la temporada.
4. **Los World Events temáticos dan el mineral que el comercio quiere recibir.** Esto coordina oferta y demanda.

---

## 6. Decisiones de diseño abiertas

Estas son las decisiones que estructuran el sistema. Cada una requiere OK explícito antes de bajar a mecánica.

### 6.1 Ratios y tipo de cambio

1. **¿Ratio fijo o fluctuante en piloto?**
   - Fijo: simple, predecible, menos emergente.
   - Fluctuante: emergent, especulativo, más rico pero más complejo.
   - **Recomendación:** fijo en piloto, fluctuante en fase 1.

2. **¿Quién define el ratio?**
   - Sentinel automático.
   - INTERLOCUTOR/Fabiola manual.
   - Híbrido.
   - **Recomendación:** INTERLOCUTOR manual para piloto, Sentinel automático para fase 1.

### 6.2 Stock y emisión

3. **¿Hay límite total de cada mineral en circulación?**
   - **Recomendación:** estaño con límite suave (1.000 unidades totales en circulación, ajustable). Cobre y oro sin límite.

4. **¿Se pueden comprar minerales con dinero real?**
   - **Recomendación:** NO. Rompe el modelo de "el juego es el medio". Si alguien quiere donar al proyecto, hay otros canales.

### 6.3 Mercado

5. **¿Mercado abierto en piloto o solo trueque bilateral?**
   - **Recomendación:** trueque bilateral en piloto, mercado abierto en fase 1.

6. **¿El mercado es solo entre jugadores, o también se comercia con el sistema (NPC del juego)?**
   - **Recomendación:** NPC del juego (banco central) en piloto — da precio piso y techo, evita volatilidad extrema.

### 6.4 Identidad narrativa

7. **¿Carboncillos desaparece por completo o queda como algo decorativo?**
   - **Recomendación:** desaparece como moneda. Queda como elemento narrativo (logros, medallas, lore). La mina y el carbón siguen siendo identidad del juego.

8. **¿Hay un mineral "carbón negro" decorativo?**
   - Algo así como una reliquia, no convertible, solo para coleccionistas.
   - **Recomendación:** opcional. No agrega mucho al MVP.

### 6.5 Técnicas

9. **¿El wallet requiere backend desde el piloto o se puede hacer local-first?**
   - Local-first: cada cliente maneja su wallet, las transferencias son firmadas y broadcast a un servidor centralizado cuando hay conexión.
   - **Recomendación:** local-first con servidor de sincronización simple. No blockchain.

10. **¿Los minerales son transferibles entre Lota y la futura expansión regional (Curanilahue, Lebu, etc.)?**
    - **Recomendación:** sí — una sola economía para toda la red de comunas. Esto refuerza el corredor patrimonial D-014.

---

## 7. Implicaciones para docs y código existentes

| Archivo | Cambio necesario |
|---|---|
| `docs/concepto-juego.md` §4 (economía) | Reescritura completa |
| `docs/concepto-juego.md` §5 (rangos — actualmente basados en ₡) | Actualizar: ¿rangos por moneda individual o portafolio total? |
| `docs/concepto-juego.md` §3 (8 rutas con minicanjes) | Revisar qué mineral entrega cada minijuego |
| `docs/concepto-juego.md` §1 (visión general — menciona Carboncillos) | Actualizar mención |
| `docs/concepto-juego.md` §7 (HUD — `₡ 1.250 Carboncillos`) | Actualizar HUD multi-moneda |
| `docs/concepto-juego.md` §8 (MVP Carboncillos funcional) | Reescribir alcance MVP |
| `MEMORY.md` | Actualizar menciones de Carboncillos |
| `_analisis/20_loop_jugador_dia_a_dia.md` §3 (Carboncillos en micro-sesión) | Actualizar |
| `_analisis/20_loop_jugador_dia_a_dia.md` §4 (Carboncillos en vector de retorno) | Actualizar |
| `_analisis/21_world_events_d014.md` §4.4 (recompensas Carboncillos) | Actualizar |
| `_analisis/21_world_events_d014.md` §6 (cupones — mencionar mineral) | Actualizar |
| `piloto-a/` (si tiene wallet Carboncillos implementado) | Refactor a wallet multi-moneda |
| `docs/decisiones.md` | Agregar D-016 con justificación |
| `CHANGELOG.md` | Entrada con justificación del cambio |

**Decisión:** ¿se actualizan todos los docs en este mismo ciclo, o se valida primero D-016 y después se hace la propagación?

---

## 8. Implicaciones para el piloto de 30 días

El piloto puede demostrar el sistema multi-moneda con alcance mínimo:

### 8.1 Alcance piloto (mínimo viable)

| Componente | Alcance |
|---|---|
| **Wallet multi-moneda** | 3 minerales (cobre, oro, estaño) con ratios fijos. UI simple. |
| **Ganancia** | Las 3 categorías funcionan (cobre por POI, oro por evento del cielo simulado, estaño por completar pasaporte). |
| **Transferencia P2P** | QR + nickname. Sin mercado abierto. |
| **Canje real** | 1 comercio real acepta cobre (sólo cobre, para simplificar). Sin tipo de cambio del comercio. |
| **NPC del juego (banco central)** | Acepta compra/venta de cobre↔oro↔estaño a ratio fijo. Da precio piso y techo. |
| **Regalos** | Mecánica básica. |
| **Trueque bilateral** | Interfaz de propuesta + aceptación. |

### 8.2 Lo que se difiere a fase 1

- Mercado abierto (libro de órdenes).
- Tipo de cambio fluctuante.
- Tipo de cambio configurable por comercio.
- Subastas.
- Proximidad física (Bluetooth/NFC).
- Verificación de identidad y límites avanzados.

### 8.3 Por qué esto vale para la postulación al fondo

El pitch se enriquece con una capa nueva: **"el juego crea una economía interna transferible y comercianteable que potencia el comercio local"**. Esto va más allá del "carboncillo canjeable" y abre el modelo de negocio a:
- **Comercio que acumula minerales** como estrategia de fidelización.
- **Intercambio entre turistas** que potencia el boca a boca.
- **Especulación legítima** que da vida propia al juego.

---

## 9. Referencias cruzadas

- **Loop de visita + retorno:** [`_analisis/20_loop_jugador_dia_a_dia.md`](20_loop_jugador_dia_a_dia.md) — el sistema multi-moneda encaja en el loop como mecanismo de interacción social y diferenciación de retención.
- **World Events:** [`_analisis/21_world_events_d014.md`](21_world_events_d014.md) — las misiones temáticas recompensan en minerales específicos; los cupones reales se canjean en cobre/oro.
- **ML externo:** `_analisis/22_ml_analytics_d014.md` *(a crear después)* — los modelos de predicción se entrenarán sobre multi-moneda, no sobre Carboncillos.
- **D-014 corregida:** `docs/decisiones.md` — encuadre vigente; el sistema multi-moneda refuerza el autofinanciamiento.
- **D-007:** `docs/decisiones.md` — Vue 3 PWA cliente. El wallet multi-moneda se implementa en el cliente + backend de sincronización.
- **Memoria del proyecto:** `MEMORY.md` — referencias existentes a Carboncillos que requieren actualización.
