# Subastas digitales de cosas reales — Lota Indómito

> **Documento de diseño conceptual — decisión D-017 propuesta.**
> **Fecha:** 2026-08-10.
> **Destinatario:** INTERLOCUTOR (Jaime), para discusión antes de bajar a mecánica.
> **Encuadre:** D-014 (turismo + comercio local) + D-016 propuesta (sistema multi-moneda de minerales, ver [`_analisis/23_sistema_monedas_minerales.md`](23_sistema_monedas_minerales.md)) + D-006 (PostgreSQL + PostGIS).
> **Decisión propuesta:** sistema de **subastas digitales de cosas reales** integrado al juego, donde los usuarios pueden listar productos o servicios del comercio local para subastar, otros pujan usando **únicamente minerales del juego** (cobre, oro, estaño), el juego cobra una comisión y la entrega se coordina localmente en Lota.

---

## 0. Tesis central

Las subastas digitales convierten a Lota Indómito en un **marketplace soberano**: el juego es el medio por el cual los usuarios intercambian valor real (productos, servicios) usando valor del juego (minerales). Esto:

1. **Refuerza el ecosistema interno del juego.** Los minerales dejan de ser "puntos de juego" y pasan a tener **poder adquisitivo real**, lo que aumenta su valor percibido.
2. **Activa D-014 (autofinanciamiento) por otra vía.** El juego cobra comisión por cada subasta completada — un nuevo flujo de ingresos además del canje de minerales.
3. **Diferencia la propuesta.** No hay otra plataforma en Chile que mezcle turismo + patrimonio + economía interna de juego + subastas reales. Esto es argumento único de postulación al fondo.
4. **Crea un mercado líquido para los minerales.** El estaño (rara) gana demanda si hay productos caros que lo requieren para pujar.

---

## 1. Por qué subastas puras con solo minerales

El usuario eligió tres restricciones que delimitan el alcance:

1. **Subastas puras (pujas).** Sin "comprar ya" a precio fijo. Esto simplifica el modelo y mantiene la tensión de la puja.
2. **Solo minerales del juego.** Sin CLP, sin Webpay, sin MercadoPago. Esto evita la integración con sistemas de pago externos y mantiene la economía cerrada en el juego.
3. **Productos/servicios locales.** Sin antigüedades (alta regulación del Consejo de Monumentos), sin NFTs (consideraciones de cripto), sin objetos fuera del comercio local.

**Lo que esto habilita:** un sistema de subastas donde la única "moneda dura" son los minerales del juego. Los productos listados tienen un **precio en minerales** definido por el vendedor.

---

## 2. Catálogo de objetos subastables (MVP)

### 2.1 Productos del comercio local

| Categoría | Ejemplos | Rango de precio esperado |
|---|---|---|
| **Gastronomía** | Vino local, pan de mina, conservas, mermeladas artesanales | 50-500 cobre |
| **Artesanía** | Cerámica, textiles, joyería de cobre, cestería | 100-2.000 cobre |
| **Souvenirs del juego** | Camisetas, posters, pines, llaveros | 30-300 cobre |
| **Libros / material cultural** | Libros sobre Lota, mapas, postales históricas | 50-1.000 cobre |
| **Edición limitada** | Objetos numerados del juego (skins raras, diplomas físicos) | 5-50 oro |

### 2.2 Servicios

| Servicio | Mecánica | Rango |
|---|---|---|
| **Tour guiado** | Persona local ofrece tour temático (carbón, fantasmas, etc.) | 200-2.000 cobre |
| **Cena en restaurant** | Cupón para una cena en restaurant asociado | 500-5.000 cobre |
| **Hospedaje** | Noche en hostal local | 1.000-10.000 cobre |
| **Clase / taller** | Taller de cocina, cestería, etc. | 300-3.000 cobre |

### 2.3 Lo que NO entra (decidido)

- **Antigüedades / patrimonio:** regulación del Consejo de Monumentos Nacionales es muy compleja. Si el modelo funciona, evaluar en fase 2 con asesoría legal.
- **NFTs / objetos virtuales puros:** requieren considerar cripto y la decisión D-014 sobre "sin Google/float" se complica. Mejor en fase 3.
- **Productos importados / no locales:** rompe el espíritu del juego.
- **Servicios ilegales o no regulados.**

---

## 3. Mecánica de subasta

### 3.1 Flujo completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. VENDEDOR LISTA                                          │
│    - Nombre del producto / servicio                        │
│    - Descripción + fotos                                    │
│    - Precio base (mínimo) en minerales                     │
│    - Duración de la subasta (1-7 días)                      │
│    - Método de entrega (local, envío, punto de recogida)   │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PUJA ABIERTA                                            │
│    - Mínimo 1 puja para activar el cierre                  │
│    - Pujas en incrementos mínimos (ej. 10 cobre)            │
│    - Anti-sniping: si hay puja en últimos 5 min,           │
│      se extiende 5 min más                                  │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. CIERRE                                                  │
│    - Gana el mejor postor                                   │
│    - Si no hay pujas, el vendedor puede relistar o retirar │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PAGO + ESCROW                                           │
│    - Los minerales del ganador se RETIENEN en escrow       │
│    - No se transfieren al vendedor hasta confirmar entrega │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. ENTREGA + CONFIRMACIÓN                                  │
│    - Vendedor y comprador coordinan entrega                │
│    - Comprador confirma recepción en la app                │
│    - Sistema libera escrow → vendedor recibe minerales    │
│    - Sistema cobra comisión del juego                      │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. REPUTACIÓN                                              │
│    - Ambos dejan rating (1-5) + comentario                 │
│    - La reputación afecta futuras subastas                 │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Detalles clave

**Puja mínima:** configurable por el vendedor (ej. mínimo 50 cobre).
**Incremento:** configurable (ej. 10 cobre, 1 oro, según rango de precio).
**Anti-sniping:** si una puja llega en los últimos 5 minutos, el cierre se extiende 5 min más. Evita el "ganar en el último segundo" malicioso.
**Reserva de precio:** opcional — el vendedor puede fijar un mínimo por debajo del cual no vende.
**Relist automático:** si no hay pujas, el vendedor puede relistar sin costo.

---

## 4. Sistema de escrow

**Mecánica:** los minerales del ganador se **retienen en una cuenta de custodia del juego** (no se transfieren al wallet del vendedor) hasta que el comprador confirme la recepción.

**Implementación:** el wallet multi-moneda de cada usuario tiene un campo `escrowed_amounts` por mineral. El sistema mueve los minerales del ganador a escrow al cerrar la subasta, y los libera al vendedor al confirmar.

**Si no hay confirmación:**

- **Plazo de auto-liberación:** 7 días después de la fecha prometida de entrega, el escrow se libera automáticamente al vendedor (asume que entregó bien).
- **Disputa abierta:** si el comprador abre disputa antes del plazo, el escrow queda congelado hasta resolución manual.

**Anti-fraude en escrow:**

- Verificación de identidad obligatoria para vendedores que superan cierto volumen.
- Límite de subastas simultáneas por usuario.
- Patrones de fraude detectados → congelamiento preventivo.

---

## 5. Sistema de reputación

**Cada usuario tiene:**

- **Rating global** (1-5 estrellas, promedio ponderado de sus transacciones).
- **Rating como vendedor** (cuenta separada).
- **Rating como comprador** (cuenta separada).
- **Historial público** de transacciones (anónimas, pero visibles).

**Efectos:**

| Reputación | Efectos |
|---|---|
| <2.5 estrellas | Restricciones: no puede subastar >1000 cobre, debe confirmar entrega con foto. |
| 2.5-4.0 estrellas | Normal. |
| >4.0 estrellas | Insignia "Vendedor Confiable", puede subastar sin límite, escrow reducido. |

**Manipulación:** para evitar rating bombing, sólo cuentan ratings de usuarios que completaron transacciones con la persona.

---

## 6. Resolución de disputas

Si el comprador abre disputa:

1. **Plazo de 7 días** desde la apertura.
2. **El equipo de cliente / INTERLOCUTOR** media.
3. **Evidencia:** fotos del producto, comunicación, tracking de envío.
4. **Resolución:** escrow se libera al vendedor, se devuelve al comprador, o se reparte.

**Complejidad operativa:** cliente/INTERLOCUTOR debe tener un canal de soporte. Esto es operacional, no técnico.

---

## 7. Comisión del juego

**Modelo:** el juego cobra un **% del precio final** de cada subasta completada.

| Tipo de subasta | Comisión |
|---|---|
| Producto local | 5% |
| Servicio local | 8% |
| Edición limitada (juego) | 10% |

**Cobro:** la comisión se deduce del escrow antes de transferir al vendedor. Ejemplo:

- Precio final: 1.000 cobre.
- Comisión (5%): 50 cobre.
- Vendedor recibe: 950 cobre.
- Juego recibe: 50 cobre.

**Qué financia la comisión:** operación del sistema de subastas, soporte de disputas, ML para detección de fraude.

**Decisión abierta:** ¿la comisión se cobra en el mismo mineral o en una mezcla? Por simplicidad, en el mismo mineral.

---

## 8. Logística de entrega (Lota es local-first)

Tres modalidades:

| Modalidad | Mecánica | Cuándo |
|---|---|---|
| **Entrega en punto de recogida** | El vendedor deposita en un local asociado (café, restaurant). El comprador retira con un código. | Por defecto para turistas de paso. |
| **Entrega personal** | Vendedor y comprador coordinan encuentro en zona del juego. | Para subastas entre turistas. |
| **Envío** | Solo para vendedores fuera de Lota. Costo aparte (CLP, no minerales). | Para expansión regional (fase 1). |

**Por qué local-first:** Lota es la prueba de concepto. La mayoría de transacciones serán locales, lo que refuerza el D-014.

**Punto de recogida oficial:** puede ser un local asociado del juego (un café emblemático, por ejemplo). Esto refuerza el comercio.

---

## 9. Implicaciones para docs y código existentes

| Archivo | Cambio |
|---|---|
| `docs/concepto-juego.md` | Agregar §10 "Subastas digitales" con resumen |
| `_analisis/23_sistema_monedas_minerales.md` | Referenciar el uso de minerales en subastas |
| `_analisis/22_ml_analytics_d014.md` | El ML mide comportamiento de subastas |
| `piloto-a/` | Frontend: vista de subastas, puja, escrow, reputación |
| Backend (nuevo) | Servicio de subastas: listings, pujas, escrow, comisión, reputación |
| `docs/decisiones.md` | Agregar D-017 |
| `CHANGELOG.md` | Entrada con justificación |
| Material del fondo | Argumento adicional para el Municipio: marketplace soberano |

---

## 10. Implicaciones para el piloto de 30 días

El piloto **no implementa el sistema completo**. Sí puede demostrar un **listings demo**:

### 10.1 Alcance piloto

| Componente | Alcance piloto |
|---|---|
| **Listings** | 1-3 productos demo del comercio local real. Precio fijo en minerales (no subasta todavía). |
| **Pago** | Transferencia directa entre wallets del comprador y vendedor. Sin escrow. |
| **Entrega** | Coordinación manual via chat in-app o presencial. |
| **Reputación** | No se mide en el piloto. |
| **Comisión** | No se cobra en el piloto. |
| **ML** | Solo se loggean eventos de listing, puja simulada, compra. |

**Versión piloto:** "venta directa con precio fijo, sin puja" — más simple. La mecánica de puja + escrow + reputación se difiere a fase 1.

**Por qué en el piloto:** validar que los usuarios están dispuestos a **comprar productos reales con minerales del juego**. Si nadie puja en fase 1, no tiene sentido el sistema completo.

### 10.2 Por qué esto vale para la postulación al fondo

El pitch al fondo se enriquece:

> "Lota Indómito no es solo un juego — es una **plataforma económica soberana** donde los usuarios acumulan minerales explorando el patrimonio, y luego pueden **comprar productos reales del comercio local** en una subasta digital. El juego coordina oferta y demanda turística, genera ingresos por comisión y crea un mercado líquido para una economía interna sin Google ni floats."

Esa propuesta es difícil de rechazar para un Municipio.

---

## 11. Decisiones de diseño abiertas

### 11.1 Sobre el sistema

1. **¿Subastas o ventas a precio fijo?**
   - El usuario eligió subastas. Mantener.
2. **¿Hay un precio de "compra inmediata" para subastas?** (eBay tiene "Buy It Now".)
   - **Recomendación:** NO en MVP. Esto complica el modelo.
3. **¿Las pujas son públicas o selladas?**
   - Públicas (todos ven quién pujó cuánto). Estilo eBay.
   - Selladas (se revelan al cerrar). Más complejo.
   - **Recomendación:** públicas para MVP.

### 11.2 Sobre la comisión

4. **¿% de comisión fijo o por categoría?**
   - Por categoría (ver §7). **Recomendación.**
5. **¿La comisión se cobra en minerales o en CLP al vendedor cuando canjea?**
   - **Recomendación:** en minerales, automático al cerrar la transacción.

### 11.3 Sobre reputación y disputas

6. **¿Quién media las disputas?**
   - cliente/INTERLOCUTOR inicialmente. Escalar a equipo dedicado si crece.
7. **¿Sistema de arbitraje automático por ML?**
   - Posible en fase 2. MVP requiere humano en el loop.

### 11.4 Sobre regulación

8. **¿Necesitamos asesoría legal chilena para subastas?**
   - La Ley del Consumidor (SERNAC) aplica si hay transacciones.
   - **Recomendación:** sí, antes de fase 1. Evaluación inicial: probablemente no hay regulación especial para subastas digitales entre particulares, pero hay que confirmar.

---

## 12. Referencias cruzadas

- **Sistema multi-moneda:** [`_analisis/23_sistema_monedas_minerales.md`](23_sistema_monedas_minerales.md) — los minerales son el medio de pago de las subastas.
- **ML externo:** [`_analisis/22_ml_analytics_d014.md`](22_ml_analytics_d014.md) — el ML mide comportamiento de subastas, predice qué productos se venden, detecta fraude.
- **World Events:** [`_analisis/21_world_events_d014.md`](21_world_events_d014.md) — los World Events pueden activar subastas temáticas (ej. subasta de arte carbonero en Fiestas Patrias).
- **Loop del jugador:** [`_analisis/20_loop_jugador_dia_a_dia.md`](20_loop_jugador_dia_a_dia.md) — las subastas son parte del vector de retorno (D+30): "vuelve a Lota para recoger tu compra".
- **D-014:** `docs/decisiones.md` — la comisión por subasta refuerza el autofinanciamiento.
- **D-016 propuesta:** sistema multi-moneda de minerales, base de las subastas.
- **D-006:** PostgreSQL + PostGIS — backend para listings, pujas, escrow.
