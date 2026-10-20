# 03 — Visualización: qué vistas construir y cómo

Rol: visualización. Insumos: `analisis/00_inventario.md`, las tres planillas de `datos/value/` y lo que contó el dueño. Los
números de este informe los recalculé desde las planillas con `openpyxl` (valores guardados). La hoja `1210 - 1810` sale
del archivo corregido (`2026-10-20b_…`), que reemplaza a la del archivo semanal. Montos en USD, salvo que diga otra
moneda. No hay nombres de clientes.

---

## 0. En cinco líneas

1. El dashboard cuenta una historia de **stock y flujo**: cuánto vale la financiera (el patrimonio neto, en una línea) y
   cuánto ganó por semana y por mes (en barras). Lo demás es detalle o contexto.
2. **Arriba y sin scroll** van el patrimonio de hoy, la ganancia de la semana, la del mes y cuánto está metido en
   proyectos, más una franja "Para tener en cuenta" con lo raro de los datos.
3. Las semanas raras **no se esconden ni se corrigen**: se marcan con un vocabulario fijo de cinco marcas (ajuste, sin
   explicar, semana doble, retiro de socios, dato dudoso) y se explican al tocarlas.
4. El drill-down tiene tres niveles: **mes → semana → grupo de cajas → caja**. Siempre usa la planilla como fuente y nunca
   inventa un dato.
5. **No se muestran** el volumen, la cantidad de operaciones ni la "renta sobre aportes": son datos cargados a mano,
   copiados de semana en semana o números que engañan.

---

## 1. Qué datos hay para graficar (verificado)

### 1.1 Series base

| Serie | De dónde sale | Período | Puntos | Notas para la visualización |
|---|---|---|---|---|
| **Patrimonio neto** ("Neto") | Calculadora, bloque A7:C29 de cada hoja | 23/02–01/03 a 12–18/10/2026 | 33 hojas → 32 variaciones | Es la serie madre. La semana `1008 - 2308` dura dos semanas |
| **Antes de egresos** ("Bruto") | ídem | ídem | 33 | `Bruto − Neto` = egresos de la semana (gastos, intereses, comisiones, inversión y, a veces, dividendos) |
| **Saldo por caja** | Calculadora, fila de sumas (4 o 5) | ídem | ~40 cajas | En su moneda (USD, ARS, EUR, REAL). Incluye pendientes, así que puede dar negativo |
| **Cotización $/USD** (C8) | Calculadora | desde 30/03–05/04 | 29 | Antes de esa semana va fija dentro de la fórmula (1.405–1.415). Se carga a mano |
| **Histórico previo** | Value CG, col. B | 01/07/2025 y 01/02–01/03/2026 | 6 | Cargado a mano. Entre julio de 2025 y febrero de 2026 hay un hueco de 7 meses |
| **Retiros de socios** | Value CG col. T y Calculadora | marzo a julio | 5 | Suman 34.398,16 (Value CG `S39`) |
| **Capital por socio** | Tenencia | julio de 2025 a junio de 2026 | por mes | No se actualiza desde junio |

**La composición cierra.** Reconstruí el Neto de cada hoja sumando caja por caja según las fórmulas de su bloque (pesos
÷ C8, euros × C9 y los fijos de Deuda y USDT). La diferencia con el Neto de la planilla es **0,00 en las 34 hojas** (33,
más la corregida). Por eso el gráfico de composición y la cascada por grupo de la sección 4 se pueden construir sin
supuestos.

### 1.2 Hechos que condicionan cómo graficar

| # | Hecho (verificado) | Consecuencia visual |
|---|---|---|
| H1 | El patrimonio pasó de **167.944,79** (01/03) a **359.107,17** (18/10): +191.162,38 (+114%) | Con eje en 0, la línea muestra a simple vista que "se duplicó". Un eje que no arranca en 0 lo exagera (ver 10) |
| H2 | 32 variaciones semanales, **10 negativas**. Mediana 5.039 (4.614 sin el ajuste de USDT General). Máxima +42.940,48 (24–30/08), mínima −5.067,21 (31/08–06/09) | Barras con cero visible. La referencia es la mediana, no el promedio, que sesgan las semanas extremas |
| H3 | Las 6 semanas del 31/08 al 11/10 suman **−4.160**. Si se agrega el 12–18/10 sin el ajuste, −1.912. Agosto suma **+58.722** (+42.940 en una sola semana) | La línea de patrimonio sola lo disimula ("está arriba"). Hace falta mostrar barras por semana y por mes |
| H4 | En 8 semanas hubo gastos de más de USD 5.000 (02–08/03, 13–19/04, 04–10/05, 01–07/06, 06–12/07, 03–09/08, 31/08–06/09 y 05–11/10). Caen a principio de mes y **6 de las 10 semanas negativas son de esas** | La comparación justa es el **mes**. Conviene el corte "antes de gastos" y una marca de "semana de gastos grandes" |
| H5 | Al 18/10, **183.532 (51,1%)** del patrimonio está en proyectos (Polígono y la columna sin título AH). A principios de junio era 0%, a fines de junio 25% y desde el 13–19/07, 41,5% o más | La pregunta "¿cuánto es líquido?" gana peso y merece un indicador propio |
| H6 | En algunas semanas la caja de dólares billete da negativa (hasta −154.612 en 11–17/05) porque incluye pendientes. Ese mes el grupo Pesos representó **más del 100%** del patrimonio (148% en 06–12/04) | **No hay torta ni barra al 100%** de la composición. Hay que usar barras divergentes desde cero |
| H7 | Al 18/10, 180,1 M ARS (117.360 USD, el 32,7% del patrimonio) están en pesos. Si el dólar sube $ 10 (de 1.535 a 1.545), el patrimonio baja **~760 USD** | La cotización usada tiene que verse en el detalle de la semana. Que el dólar se mueva no es ganar ni perder plata operando |
| H8 | El efecto estimado de la cotización sobre los pesos de la semana anterior suma **−14.707** en 27 semanas (de −3.285 a +3.122 por semana). La cotización quedó igual que la semana anterior en **8 semanas** | Se muestra como dato aproximado (P1) en el detalle, nunca como serie principal |
| H9 | El ajuste de USDT General (+15.855,49) entra todo en 12–18/10: la ganancia de esa semana es 18.103,33, de la que 2.247,84 viene de la semana | La marca de "ajuste" y un interruptor para verlo con o sin ajuste son obligatorios |
| H10 | Value CG y Calculadora no coinciden en el cierre del 01/03 (167.896,05 contra 167.944,79: 48,74 de diferencia). La hoja Semanales tiene otros valores (14/06: 254.204,96 contra 261.617,18) | Una sola fuente por tramo: la Calculadora desde el 01/03 y el Value CG solo para lo anterior. Semanales no se usa |

---

## 2. Preguntas del dueño → vista que la responde

Ordené las preguntas por importancia según lo que dijo el dueño ("saber el patrimonio neto en USD" y "la ganancia de la
financiera"). El informe de negocio va a traer su propia lista; la síntesis las cruza.

| # | Pregunta | Vista (sección 4) | Forma | Prioridad |
|---|---|---|---|---|
| Q1 | ¿Cuánto vale hoy la financiera y cuánto creció? | V2 KPI 1 + V3 | Número principal + línea con área | P0 |
| Q2 | ¿Cuánto ganamos esta semana y este mes? ¿Es normal? | V2 KPI 2 y 3 + V4 + V5 | Indicadores + barras semanales con mediana + barras mensuales | P0 |
| Q3 | Esa ganancia, ¿viene de la operación o de ajustes, movimientos raros o el dólar? | Marcas (sección 8) + interruptor de ajustes + V7 | Segmento de ajuste en la barra, cascada por grupo | P0 |
| Q4 | ¿Dónde está la plata? ¿Cuánto es líquido y cuánto está en proyectos? | V2 KPI 4 + V6 | Barras horizontales divergentes + área apilada de 3 series | P0 |
| Q5 | ¿Por qué cambió el patrimonio esta semana? | V7 (detalle de semana) | Cascada (waterfall) por grupo + tabla de cajas | P0 |
| Q6 | ¿Cuánto se va en gastos, intereses a inversores y comisiones? | V8 | Barras mensuales apiladas por tipo | P1 |
| Q7 | ¿Cuánto retiramos los socios y cuánto le toca a cada uno? | Marca de retiro + V9 | Marcadores en el eje + tabla de socios | P1 |
| Q8 | ¿Cuánto nos mueve el dólar? | V7 › Pesos | Lectura de la cotización usada, efecto estimado y sensibilidad | P1 |
| Q9 | ¿Puedo confiar en estos números? | V1 franja + V11 | Lista de chequeos con ícono y palabra | P0 (franja) / P1 (sección) |

---

## 3. Jerarquía visual y disposición

**Regla:** de arriba hacia abajo, de lo que responde "¿cómo estamos?" a lo que responde "¿por qué?" y, al final, "¿le
creo?". Arriba, los números grandes y una sola línea. En el medio, la ganancia. Abajo, el detalle y la consulta.

### 3.1 Celular (390 px; lo que se ve sin scroll está arriba de la línea ═══)

```
┌──────────────────────────────────────────┐
│ Patrimonio · 12–18 oct ▾        ?   ◐    │  encabezado fijo (≤ 52 px): semana foco, ayuda y tema
│ [Todo ▾]  [Con ajustes ▾]                │  fila de filtros: período y ajustes
├──────────────────────────────────────────┤
│ PATRIMONIO NETO                          │
│ USD 359.107                    (≥ 48 px) │  V2 · número principal
│ +191.162 desde el 1/3 · incluye ajuste ◆ │
│ ┌──────────────────┐┌──────────────────┐ │
│ │GANANCIA SEMANA   ││GANANCIA OCTUBRE  │ │  V2 · 3 indicadores compactos
│ │USD 18.103        ││USD 13.501        │ │
│ │sin ajuste 2.248  ││3 de 5 sem · parc.│ │
│ └──────────────────┘└──────────────────┘ │
│ ┌──────────────────────────────────────┐ │
│ │EN PROYECTOS  USD 183.532 · 51%       │ │
│ └──────────────────────────────────────┘ │
│ ⚠ Para tener en cuenta (3)            ›  │  V1 · franja
│ ┌──────────────────────────────────────┐ │
│ │ Patrimonio semana a semana       ▁▃▅▇│ │  V3 · línea, 180 px
│ └──────────────────────────────────────┘ │
╞══════════════════════════════════════════╡  ~740 px útiles en un iPhone con el navegador abierto
│ Ganancia  [Por semana | Por mes]         │  V4 / V5
│           [Después de gastos | Antes]    │
│ ¿Dónde está la plata?                    │  V6
│ Gastos e intereses por mes               │  V8
│ Socios                                   │  V9
│ Todas las semanas (tabla)                │  V10
│ ¿Le creo a estos números? · Cómo se calcula │  V11
└──────────────────────────────────────────┘
```

### 3.2 Escritorio (≥ 960 px, contenido de 1.200 px como máximo)

```
┌ encabezado: título · semana foco ▾ · período · ajustes · ? · tema ───────────────────────────┐
│ [PATRIMONIO 359.107] [GANANCIA SEMANA 18.103] [GANANCIA OCTUBRE 13.501] [EN PROYECTOS 51%] │ V2: 4 tarjetas
│ ⚠ Para tener en cuenta: ajuste USDT General · +42.940 sin explicar · Value CG al 28/06      │ V1
│ ┌ Patrimonio semana a semana (2/3) ─────────────┐ ┌ ¿Dónde está la plata? (1/3) ─┐            │ V3 + V6 foco
│ └───────────────────────────────────────────────┘ └──────────────────────────────┘            │
│ ┌ Ganancia por semana / por mes (ancho completo) ───────────────────────────────────┐         │ V4 / V5
│ ┌ Disponible vs proyectos (1/2) ┐ ┌ Gastos e intereses por mes (1/2) ┐                         │ V6 evolución + V8
│ ┌ Socios (1/2) ┐ ┌ ¿Le creo a estos números? (1/2) ┐                                           │ V9 + V11
│ ┌ Todas las semanas (tabla, ancho completo) ┐                                                  │ V10
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

El detalle de una semana (V7) se abre como **hoja inferior** en el celular y como **panel lateral** de 420 px en
escritorio, sin perder de vista el gráfico desde el que se abrió.

**Por qué este orden**
- El patrimonio es lo primero porque es lo que el dueño dice que quiere saber. Va como número grande (no como gráfico)
  porque es un solo valor. La línea de abajo le da el contexto.
- La ganancia va segunda y al lado del patrimonio, en otro gráfico (nunca en el mismo con dos ejes). La línea dice
  "cuánto hay" y las barras, "cuánto se sumó".
- "En proyectos" está entre los cuatro indicadores porque es el cambio de estructura más grande del año (de 0% a 51%
  en cuatro meses, H5) y porque sin él el patrimonio parece todo plata disponible.
- La franja "Para tener en cuenta" va antes de cualquier gráfico. Si el número grande incluye un ajuste de 15.855, el
  lector se tiene que enterar antes de sacar conclusiones.

---

## 4. Vistas en detalle

Para cada vista: pregunta · forma · medida exacta · marcas · interacción · ayuda ("?") · qué pasa si falta el dato ·
por qué esta forma.

### V1. Encabezado y franja "Para tener en cuenta" · P0

- **Encabezado fijo:** chip-botón con la semana foco ("12–18 oct ▾"). Al tocarlo se abre la lista de semanas, la más
  nueva primero, cada una con sus marcas. Debajo va la fecha de los datos: "Calculadora al 18/10 · Value CG al 28/06".
- **Franja:** muestra hasta 3 ítems en el celular y 5 en escritorio, más "Ver todos". Cada ítem lleva ícono, una frase
  con el número y un enlace a la semana. Contenido al 18/10:
  1. ◆ "Esta semana incluye +15.855 de ganancia de USDT General de mayo a septiembre, cargada toda junta. Sin eso, la
     semana dio +2.248."
  2. ? "La semana del 24 al 30/08 sumó +42.940 y no está explicada (vino casi toda de la caja de dólares billete:
     +43.532)."
  3. ⏸ "El Value CG y la Tenencia de socios llegan hasta el 28/06. La parte de socios está desactualizada."
- **Por qué:** el dueño no es analista. Si la advertencia queda en un "?" escondido, no la ve. Si está en una franja con
  el número, sí.

### V2. Indicadores (tarjetas) · P0

| # | Rótulo | Cifra | Sublínea | Comparación |
|---|---|---|---|---|
| 1 | **Patrimonio neto** (número principal) | Neto de la semana foco: 359.107 | "+191.162 desde el 1/3 (+114%)". Si la foco tiene ajuste: "incluye +15.855 de ajuste ◆" | Contra el 1/3 y contra la semana anterior (+18.103) |
| 2 | **Ganancia de la semana** | Variación del patrimonio + retiros de socios de la semana (sección 12, D1): 18.103 | "Sin ajustes: 2.248" (solo si hay ajuste). "Semana de gastos grandes" si corresponde | "Semana típica: 826" (mediana de las 8 semanas anteriores; sección 12, D3) |
| 3 | **Ganancia del mes** | Suma de las semanas del mes de la foco (regla del jueves, sección 5): 13.501 | "3 de 5 semanas · mes en curso" · "Sin ajustes: −2.354" | Contra el mes anterior **por semana** (septiembre: 111 por semana) cuando el mes está incompleto |
| 4 | **En proyectos** | Polígono + Almafuerte + columna sin título: 183.532 | "51% del patrimonio · disponible 130.039" | Contra 4 semanas antes (146.032; +37.500) |

- **Formato de la comparación:** "▲ 18.103 vs semana anterior", en tinta neutra. No va en rojo ni en verde: una semana
  negativa por gastos del mes o por el dólar no es una alarma (H4, H8).
- **Mes incompleto:** no se compara el total contra un mes completo. Se compara el promedio por semana.
- **Semana doble como foco:** "18.349 en 2 semanas (9.175 por semana)".
- **Por qué tarjetas y no gráficos:** cada indicador es un número. Un gráfico de una barra no dice nada que no diga el
  número. El indicador 1 no lleva minigráfico porque la línea completa (V3) está justo abajo.

### V3. Patrimonio semana a semana · P0

- **Pregunta:** Q1. ¿Cuánto vale y cómo creció?
- **Forma:** **línea** de 2 px con un área suave abajo (10% de opacidad), eje Y **desde 0** y eje X de tiempo real (una
  semana = un paso; la semana doble ocupa dos).
- **Medida:** Neto de cada hoja, al cierre de la semana (domingo). La serie empieza el 01/03 (167.944,79).
  - **"Ver desde julio 2025"** (P1) agrega los 6 puntos del Value CG (01/07/2025 y 01/02–01/03/2026). En el hueco de 7
    meses no se dibuja línea: va una banda gris con "sin datos semanales". Esos puntos llevan el rótulo "Value CG (cargado
    a mano)".
- **Marcas:** rótulos directos selectivos (no un número en cada punto): el valor inicial, el final y el salto de 24–30/08.
  Los eventos van como íconos chicos en una franja de 16 px debajo del eje X: ▼ retiros de socios, ◆ ajuste, ⧉ semana
  doble y ? sin explicar (sección 8).
- **Con el interruptor "sin ajustes":** el último punto pasa a 343.252 y el rótulo dice "sin el ajuste de USDT General".
- **Interacción:** una línea vertical sigue al dedo o al mouse y se pega a la semana más cercana. La **lectura** queda
  fija arriba del gráfico (no flota bajo el dedo): "12–18 oct · USD 359.107 · +18.103 vs semana anterior". Al tocar,
  esa semana pasa a ser la foco; un segundo toque o "Ver semana" abre V7.
- **Ayuda (?):** "Qué es: lo que vale Cambio General en dólares, sumando todas las cajas (los pesos pasados a dólar con
  la cotización de esa semana), los proyectos y la participación en USDT General. Cómo se calcula: es el 'Neto' de cada
  hoja de la Calculadora Semanal. De dónde sale: Calculadora Semanal, una hoja por semana."
- **Por qué línea y no barras:** el patrimonio es un stock (cuánto hay) y no un flujo. La línea muestra continuidad y la
  pendiente se lee como velocidad. Las barras de la planilla actual (sección 10) invitan a compararlas como si cada una
  fuera una ganancia.
- **Por qué eje en 0:** la pregunta es "¿cuánto creció?", y con eje en 0 "se duplicó" se ve como se duplicó. Las
  variaciones semanales casi no se notan en esta escala, y está bien: para eso está V4.

### V4. Ganancia por semana · P0

- **Pregunta:** Q2 y Q3. ¿Cuánto ganamos cada semana, es normal y de dónde vino?
- **Forma:** **columnas** con base en cero, en eje de tiempo real. Negativas hacia abajo, del mismo color.
- **Medida (por defecto, "después de gastos"):** `Neto_t − Neto_{t−1} + retiros de socios_t`. Con "antes de gastos":
  `Bruto_t − Neto_{t−1} + retiros que no estén ya en egresos` (sección 12, D1 y D2).
- **Marcas dentro de la barra:**
  - **Ajuste extraordinario (◆):** la parte del ajuste es un segmento apilado en un tono más claro del mismo color, con
    rótulo directo "ajuste USDT +15,9 k". La barra del 12–18/10 muestra 2.248 sólido y 15.855 claro encima.
  - **Semana doble (⧉):** ocupa dos semanas de ancho y su **alto es la ganancia por semana** (9.175), así el área
    representa el total (18.349). El rótulo dice "2 sem.".
  - **Sin explicar (?):** la barra va con un contorno punteado alrededor y un "?" arriba (24–30/08).
  - **Semana de gastos grandes:** un punto chico bajo el eje (gastos ≥ USD 5.000; umbral en la configuración).
- **Línea de referencia:** horizontal, sólida y fina, en la **mediana** del período elegido ("semana típica"), con su
  rótulo a la derecha. Es una sola línea. No hay promedio móvil.
- **Interacción:** cada barra es su propia zona táctil y ocupa todo el ancho de su semana más el espacio entre barras.
  La lectura fija muestra: "24–30 ago · Ganancia +42.940 · gastos 152 · patrimonio 345.164 · ? sin explicar". Tocar
  la barra cambia la semana foco y "Ver semana" abre V7.
- **Interruptor de vista (en la cabecera de la sección):** [Por semana | Por mes] y [Después de gastos | Antes de
  gastos]. Van en la sección y no en la fila global porque cambian **qué se mide**, no qué período se mira.
- **Ayuda:** "Ganancia de la semana = lo que creció el patrimonio respecto de la semana anterior, más lo que retiraron
  los socios esa semana (no es un gasto del negocio). 'Antes de gastos' suma lo que se pagó en gastos, intereses a
  inversores y comisiones."
- **Por qué columnas:** es un flujo con signo, y la columna desde cero es la forma más leída para eso. **Por qué un solo
  color para positivas y negativas:** el signo ya lo dice la posición. El rojo alarmaría por semanas que son normales
  (H4). El color de estado queda para los datos dudosos.

### V5. Ganancia por mes · P0

- **Pregunta:** Q2. Es la comparación justa: los gastos grandes caen a principio de mes (H4).
- **Forma:** columnas, una por mes, con el **mismo vocabulario de marcas** que V4.
- **Medida:** suma de las semanas del mes según la regla del jueves (sección 5). Valores al 18/10, después de gastos y
  sumando los retiros de socios:

| Mes | Semanas | Variación del patrimonio | Retiros de socios | Ganancia | Por semana |
|---|---|---|---|---|---|
| Mar | 4 | 12.981,84 | 22.672,00 | 35.653,84 | 8.913 |
| Abr | 5 | 52.366,61 | 3.573,00 | 55.939,61 | 11.188 |
| May | 4 | 25.028,29 | 4.719,00 | 29.747,29 | 7.437 |
| Jun | 4 | 7.567,83 | 2.510,00 | 10.077,83 | 2.519 |
| Jul | 5 | 20.552,55 | 924,16 (a confirmar) | 21.476,71 | 4.295 |
| Ago | 4 (3 hojas) | 58.721,65 | — | 58.721,65 | 14.680 |
| Sep | 4 | 442,61 | — | 442,61 | 111 |
| Oct | 3 de 5 | 13.501,00 (−2.354,49 sin ajuste) | — | 13.501,00 | 4.500 |

- **Mes incompleto:** la barra va **solo con contorno** (sin relleno) y lleva "3 de 5 sem." encima. Con [Por semana] se
  compara de igual a igual.
- **Selector [Total del mes | Por semana]:** abril y julio tienen 5 semanas y los demás 4. Sin este selector, abril
  "gana" en parte porque tiene una semana más.
- **Drill-down:** tocar un mes filtra V4 a sus semanas (las demás quedan en gris, sin desaparecer) y abre un resumen del
  mes: patrimonio al inicio y al final, ganancia, egresos y retiros.
- **Ayuda:** "Cada semana se cuenta en el mes que tiene la mayoría de sus días (el del jueves), igual que en el Value CG."

### V6. ¿Dónde está la plata? · P0 (foto) / P1 (evolución)

**V6a. Foto de la semana foco: barras horizontales divergentes**
- **Forma:** una barra por grupo, ordenadas de mayor a menor, con cero al medio. Las negativas van a la izquierda, con su
  número y "(debemos)". Todas van del mismo color porque el rótulo de la fila ya dice qué es cada una.
- **Grupos** (6, todos recalculados y verificados con cierre 0,00). Valores al 18/10:

| Grupo | Cajas que incluye | 18/10 | % del patrimonio |
|---|---|---|---|
| Proyectos | POLIGONO, ALMAFUERTE, columna sin título AH ("POLIGONO 20+13") | 183.532 | 51,1% |
| Pesos (en USD) | PESOS + CHEQUES + TRANSFER (+ RECAUDACION BX) ÷ cotización | 117.360 | 32,7% |
| USDT General y deuda a favor | Fijos del bloque: USDT 41.536 (incluye el ajuste) y Deuda 4.000 | 45.536 | 12,7% |
| Cuentas en el exterior y euros | LLC, Grabify/Grabifi, PayPal, Wise, Payoneer, City; euros × 1,25 | 19.682 | 5,5% |
| Dólares billete | CARA CHICA, CAMBIO, MALOS, USD | 10.131 | 2,8% |
| Cripto | USDT, TRX | −17.134 | (debemos) |
| **Patrimonio neto** | | **359.107** | 100% |

- Los gastos, comisiones, intereses e ingresos de la semana entran y salen dentro del mismo cálculo (suman 0). Reales,
  libras y garantías (Millamapu, Jeep, Gol Trend, Charcas, Promar) **no suman** al patrimonio en la planilla. No se
  dibujan; aparecen en la tabla de cajas (V7) con la etiqueta "no suma".
- **Por qué barras divergentes y no torta:** hay grupos negativos (cripto en 15 de las 34 hojas y dólares billete también en 15).
  Con negativos, una torta o una barra al 100% no tienen sentido: en 06–12/04 el grupo Pesos equivalía al 148% del
  patrimonio. Seis barras rotuladas se comparan mejor que seis porciones.

**V6b. Evolución: "Disponible / Proyectos / USDT General y deuda" (área apilada)**
- **Forma:** área apilada de **3 series**, todas positivas en las 34 hojas (lo verifiqué: la menor es "Disponible",
  127.190 en 10–23/08). La suma de las tres es el patrimonio, así que el borde de arriba coincide con V3.
- **Disponible** = dólares billete + pesos + cripto + exterior y euros.
- **Lo que muestra de un vistazo:** entre el 14/06 y el 21/06 el disponible cayó 55.165 (de 224.524 a 169.359) y los
  proyectos pasaron de 7.412 a 67.607, **con el patrimonio casi igual** (+5.030). La plata se movió de caja a proyecto,
  no se perdió. Lo mismo pasó en 05–11/10: +37.500 en la columna sin título y −41.384 en disponible.
- **Por qué 3 series y no 6:** las 6 apiladas no se pueden dibujar porque hay grupos negativos. Además, la pregunta del
  dueño es "¿cuánto es líquido?", y para eso alcanzan tres. El detalle de los 6 grupos queda en V6a y en V7.
- **Interacción:** igual que V3 (línea vertical y lectura con las 3 series y el total). Tocar una banda abre el grupo
  (sección 6).

### V7. Detalle de una semana (hoja inferior o panel) · P0

Se abre al tocar una semana en cualquier gráfico o en la tabla. Contenido, en este orden:

1. **Cabecera:** "24–30 ago · cerrada", con flechas ‹ › para ir a la semana anterior o siguiente sin cerrar el panel.
2. **Tres números:** patrimonio al cierre, ganancia de la semana (separando la parte de ajustes) y egresos.
3. **"¿De dónde salió?": cascada por grupo.** Arranca en el patrimonio de la semana anterior, suma o resta la variación
   de cada grupo y termina en el de esta semana. Ejemplos verificados:
   - **24–30/08:** 302.223 → dólares billete **+43.532** · cripto +6.181 · exterior y euros −257 · pesos −6.515 ·
     proyectos 0 → 345.164. Se ve enseguida que el +42.940 "sin explicar" está en la caja de dólares billete.
   - **12–18/10:** 341.004 → pesos +43.455 · dólares billete −42.409 · USDT General **+15.855 ◆** · cripto +7.321 ·
     exterior y euros −6.119 → 359.107.
   - **Ayuda obligatoria en esta vista:** "Si una caja sube y otra baja casi lo mismo, es plata que se movió de una caja
     a otra (por ejemplo, se compraron pesos con dólares). No es ganancia. La ganancia es el total del final."
   - **Por qué cascada:** es la única forma que muestra a la vez las partes y el total que cierra. Una tabla de
     diferencias dice lo mismo, pero no se lee de un vistazo.
4. **Marcas de la semana**, cada una con su explicación en una frase (sección 8).
5. **Tabla de cajas:** caja · saldo en su moneda · USD · variación contra la semana anterior. Va agrupada como V6a y
   colapsada por grupo. Las cajas en cero se ocultan detrás de "ver todas (n)". Las que no suman llevan la etiqueta "no
   suma".
6. **Cotización usada** (P1): "1.535 $/USD (la semana anterior: 1.540)". Si es igual a la anterior: "⚠ igual que la
   semana anterior: confirmar". Debajo: "Efecto aproximado del cambio de cotización sobre los pesos: +241" y "Si el
   dólar sube $ 10, el patrimonio baja ~760".
7. **Notas del dueño** (si las hay, sin nombres de terceros): por ejemplo, "Semana corta", "Muy poco movimiento".

### V8. Gastos, intereses y comisiones por mes · P1

- **Forma:** columnas mensuales **apiladas por tipo**, con 4 categorías: Gastos · Intereses a inversores · Comisiones
  pagadas · Inversión. Leyenda y rótulos directos en el último mes.
- Los **retiros de socios no van acá**: no son un gasto del negocio. Hay casos donde la planilla los mezcla (3.573 dentro
  de INTERESES en 27/04–03/05 según el Value CG, 924,16 en INTERESES en 06–12/07), así que la vista los separa y avisa
  "separado de intereses: posible retiro de socios".
- **Por mes y no por semana:** los costos fijos se cargan en una sola semana del mes (H4). Por semana, el gráfico
  parecería un serrucho.
- Egresos totales por mes, con dividendos incluidos, como figuran en la Calculadora: mar 12.279 · abr 18.784 · may
  18.371 · jun 19.494 · jul 14.902 · ago 13.220 · sep 11.278 · oct (3 sem.) 13.204.

### V9. Socios · P1

- **Forma:** una **tabla** (socio · % de tenencia · aporte · capital al 28/06 · ganancia asignada por mes) y, arriba, una
  barra horizontal única al 100% con los 4 segmentos de tenencia (28,13% × 3 y 15,62%). Es una relación parte-todo de
  4 partes, todas positivas y fijas.
- **Fecha bien visible:** "Tenencia al 28/06: el Value CG no se actualizó después". Si el Value CG no tiene datos
  posteriores, la tabla no proyecta nada y muestra "Se actualiza cuando se cargue el Value CG".
- **Retiros:** lista con fecha y monto (22.672 en marzo, que incluye 16.222 de liquidación de un ex socio; 3.573; 4.719;
  2.510; 924,16). Total 34.398,16.
- **Por qué tabla:** son 4 personas y pocos números exactos que cada socio va a querer leer con todos los decimales. Un
  gráfico agrega poco.

### V10. Todas las semanas (tabla) · P0

- Es "la planilla limpia": una fila por semana, la más nueva arriba.
- Columnas: Semana · Patrimonio · Ganancia · Antes de gastos · Egresos · Retiros · Ajustes · Cotización · Marcas.
- En el celular se ven Semana, Patrimonio y Ganancia, y al tocar la fila se abre V7. No hay scroll horizontal.
- Cada gráfico tiene además su botón "Ver como tabla", que muestra los mismos números del gráfico.
- **Por qué:** el auditor y el dueño necesitan poder comparar contra la planilla celda por celda, y una tabla es la única
  forma de hacerlo sin pasar el dedo por cada barra.

### V11. ¿Le creo a estos números? · Cómo se calcula · P1

Lista de chequeos, cada uno con ícono y palabra (OK / Revisar / Info) y una frase:
- Hoja 12–18/10 tomada del archivo corregido. La original tenía `#REF!` en la ganancia (Info).
- Cotización igual que la semana anterior en 8 semanas: 04–10/05, 29/06–05/07, 06–12/07, 27/07–02/08, 03–09/08,
  10–23/08, 21–27/09 y 05–11/10 (Revisar).
- Rótulos "Poligono 09" y "Almafuerte" del bloque apuntan, desde 27/07–02/08, a las columnas JEEP y GOL TREND (en 0).
  Los proyectos se suman igual, dentro de "Dólares" (Info: no cambia el total).
- Columna AH: 75.466 desde 10–23/08 (con título "POLIGONO 20+13" solo en esa hoja; después, sin título) y 112.966 desde 05–11/10 (Revisar).
- "Operaciones" = 338 copiado igual en 12 hojas seguidas (20–26/07 a 12–18/10): no se usa (Info).
- Value CG y Tenencia sin actualizar desde el 28/06 (Revisar).
- Cierre del 01/03: Value CG 167.896,05 y Calculadora 167.944,79 (Info: se usa la Calculadora).
- Además: el glosario (sección 11) y "Cómo se calcula" con las fórmulas de la sección 12.

---

## 5. Filtros y cortes

**Una sola fila de filtros**, arriba de todo y fija con el encabezado. Afecta a todos los gráficos, indicadores y tablas
que tiene debajo.

| Control | Opciones | Por defecto | Por qué |
|---|---|---|---|
| **Período** | Últimas 8 semanas · Últimos 3 meses · Todo (desde mar) · un mes (al tocarlo en V5) | Todo | La historia es corta (8 meses, 33 semanas) y entra en un gráfico, incluso en el celular |
| **Ajustes extraordinarios** | Con ajustes · Sin ajustes | Con ajustes | "Con" coincide con la planilla (el auditor la puede comparar) y el ajuste igual se ve como segmento aparte. "Sin" sirve para "¿cómo viene la operación?" |
| **Semana foco** (en el encabezado) | Lista de semanas con sus marcas | La última cargada | Define los indicadores, V6a y V7. "Volver a la última" siempre visible si la foco no es la última |

**Cortes dentro de una sección** (cambian la medida, no el período): Por semana / Por mes (V4–V5), Después / Antes de
gastos (V4–V5) y Total / Por semana (V5).

**Regla de mes:** cada semana va al mes que contiene su jueves (la mayoría de sus días). Coincide con cómo arma los
meses el Value CG (abril = semanas que terminan entre el 05/04 y el 03/05). La semana doble 10–23/08 va a agosto.

**Qué NO se ofrece como filtro:** las cajas (son ~40 y la mayoría están en 0; el corte por grupo de V6 y V7 alcanza) y
los operadores (la Calculadora no los tiene; eso está en el Tablero semanal del Registro).

---

## 6. Drill-down

```
Período (todo) ──► Mes (V5, tocar barra) ──► Semana (V4/V3/V10, tocar) ──► Grupo (V6/V7, tocar) ──► Caja
  línea + barras     semanas del mes            cascada + cajas              cajas del grupo           su saldo semana
  mensuales          resaltadas                  + marcas + cotización         en su moneda              a semana (línea)
```

- **Nivel grupo → caja (P1):** una línea por caja en **su moneda** (ARS en millones, USD y EUR), una por gráfico (small
  multiples con el mismo eje dentro de cada moneda), nunca dos monedas en el mismo eje. Ejemplo que lo justifica: en
  10–23/08, CHEQUES pasó de −14,15 M a +13,99 M ARS (+28,1 M, ≈ +18.450 USD a 1.525). Es el salto de cheques sin aclarar
  que ya había visto el dueño.
- **Siempre se puede volver:** una miga de pan ("Todo › Agosto › 24–30 ago › Dólares billete") y la flecha atrás del
  celular cierra el panel.
- **Lo que no se hace:** no se baja al nivel de operación. La Calculadora no tiene operaciones. Eso queda para el
  Registro General y su tablero.

---

## 7. Interacciones

| Interacción | Dónde | Comportamiento |
|---|---|---|
| **Lectura fija** | V3, V4, V5, V6b | Una línea de texto arriba de cada gráfico con los valores de la semana o el mes señalado. Por defecto muestra la foco. En el celular reemplaza al tooltip flotante, que tapa el dedo |
| **Tooltip** | escritorio | Al pasar el mouse; mismo contenido que la lectura. El valor va en negrita y el rótulo después |
| **Línea vertical que sigue al puntero** | V3, V6b | Se pega a la semana más cercana: no hay que acertarle a la línea de 2 px |
| **Tocar o clic en una barra o semana** | V3–V6, V10 | Cambia la semana foco (y se actualizan los indicadores). "Ver semana" abre V7 |
| **Tocar un mes** | V5 | Filtra V4 a ese mes y abre el resumen del mes |
| **Tocar un grupo** | V6a, cascada de V7 | Abre las cajas del grupo |
| **‹ ›** | V7 | Semana anterior o siguiente sin cerrar el panel |
| **Teclado** | todo | Flechas para recorrer semanas, Enter para abrir y Esc para cerrar. Foco visible de 2 px |
| **"Ver como tabla"** | cada gráfico | La misma información en una tabla, para quien no quiere pasar el dedo y para lectores de pantalla |

El estado (período, ajustes, foco y sección) se guarda en la URL (`#…`) para poder mandar "mirá esta semana" por
WhatsApp. Las preferencias (tema, último período) se guardan solo localmente y, si no se pueden guardar, la página
funciona igual.

---

## 8. Cómo marcar semanas anómalas, datos dudosos y ajustes

### 8.1 Vocabulario visual (fijo para todo el dashboard)

| Marca | Significa | En barras | En la línea | Color |
|---|---|---|---|---|
| ◆ **Ajuste** | Algo real pero que no es de esa semana (se generó antes y se cargó todo junto) | Segmento apilado claro + rótulo "ajuste +15,9 k" | Ícono bajo el eje + rótulo en el punto | Tono claro del color de datos |
| ? **Sin explicar** | Variación grande que nadie explicó todavía | Contorno punteado + "?" arriba | Ícono bajo el eje | Tinta de advertencia (`--warn-ink`) |
| ⧉ **Semana doble** | La hoja abarca dos semanas | Barra de doble ancho y alto por semana + "2 sem." | La línea cruza dos pasos | Neutro |
| ▼ **Retiro de socios** | Dividendos o liquidación de un ex socio | Punto bajo el eje con el monto | Ícono bajo el eje | Neutro |
| ⚠ **Dato dudoso** | Cotización repetida, columna sin título, dato copiado | Punto chico bajo el rótulo de la semana | ídem | `--warn-ink` |
| ○ **Incompleto** | Mes en curso o con semanas faltantes | Solo contorno, sin relleno, + "3 de 5 sem." | — | Color de datos, solo el contorno |
| • **Gastos grandes** | Semana con gastos ≥ USD 5.000 (costos fijos) | Punto gris bajo el eje | — | `--ink-3` |

Reglas:
- **Cada marca lleva ícono + palabra**, nunca solo color. La explicación completa aparece al tocar.
- **Como máximo una marca de color por semana.** Si hay varias, se muestra la más grave (? > ⚠ > ◆) y el resto queda en
  el detalle.
- Las marcas **no se calculan en el navegador**: vienen de una tabla de eventos que se arma al procesar la planilla. Si
  el dueño explica una semana, la marca ? pasa a ◆ o desaparece, con su nota.

### 8.2 Semanas marcadas al 18/10 (verificadas)

| Semana | Marca | Qué dice el panel |
|---|---|---|
| 23/02–01/03 | — | Primera hoja: no tiene semana anterior, así que no tiene ganancia |
| 02–08/03 | • | Gastos 5.694 |
| 16–22/03 | ▼ | Retiros 22.672 (dividendos 6.450 y liquidación de un ex socio 16.222). El patrimonio bajó 4.425; sumando los retiros, ganancia 18.247 |
| 23–29/03 y 30/03–05/04 | nota | "Semana corta", según las notas del dueño |
| 13–19/04 | • | Gastos 5.531 |
| 27/04–03/05 | ▼ | 3.573 de dividendos dentro de INTERESES (5.152), según el Value CG |
| 04–10/05 | ▼ • ⚠ | Dividendos 4.719 · gastos 6.872 · cotización igual a la semana anterior (1.380) |
| 01–07/06 | ▼ • | Dividendos 2.510 · gastos 7.966 · patrimonio −4.821 |
| 22–28/06 | — | Efecto aproximado del dólar −2.688 (cotización de 1.455 a 1.490) contra una variación de −758 |
| 29/06–05/07 | ⚠ | Cotización repetida (1.490) |
| 06–12/07 | ▼? • ⚠ | 924,16 en INTERESES = dividendos de junio según el Value CG (a confirmar) · gastos 5.828 · cotización repetida |
| 13–19/07 | — | Entra Almafuerte 50.000 (de disponible a proyectos) |
| 27/07–02/08 | ⚠ | Cotización repetida (1.525). Rótulos del bloque corridos desde esta hoja |
| 03–09/08 | • ⚠ | Gastos 7.447 · cotización repetida |
| 10–23/08 | ⧉ ? ⚠ | Dos semanas: +18.349 (9.175 por semana). Sale Almafuerte y entra Polígono 20+13 (75.466). CHEQUES de −14,15 M a +13,99 M ARS sin aclarar. Cotización repetida |
| 24–30/08 | ? | +42.940 sin explicar; +43.532 en dólares billete |
| 31/08–06/09 | • | Gastos 8.972 · la semana más baja (−5.067) |
| 21–27/09 | ⚠ | Cotización repetida (1.535) |
| 05–11/10 | • ⚠ | Gastos 8.111 · columna sin título +37.500 · cotización repetida (1.540) |
| 12–18/10 | ◆ | Ajuste USDT General +15.855,49 (mayo a septiembre, 2/3 de cada liquidación). Sin el ajuste, +2.247,84. Hoja tomada del archivo corregido |

**El ajuste de USDT General no se reparte por mes.** Las 6 liquidaciones que lo forman no tienen fecha (la nota dice
"desde mayo hasta septiembre"). Repartirlo sería inventar en qué mes se ganó. Se muestra como ◆ en la semana en que se
cargó, con la explicación, y el interruptor "sin ajustes" lo saca.

---

## 9. Celular

- **Una columna, sin scroll horizontal**, con 16 px de margen lateral (o el del área segura) y áreas táctiles de 44 px
  como mínimo.
- **Gráficos de 180 px de alto** (220 px en escritorio), contando la banda del eje X. Con 33 semanas, cada barra mide
  ~7 px. No hace falta tocarla justo, porque la selección se pega a la semana más cercana. En el eje X van solo los meses.
- **Lectura fija en lugar de tooltip** (sección 7).
- **Indicadores en 2 × 2.** El número principal tiene 48 px y los compactos, 24 px. Las sublíneas se cortan en 1 línea.
- **Filtros:** dos chips ("Todo ▾", "Con ajustes ▾") que abren una hoja inferior con las opciones.
- **V7 como hoja inferior** a pantalla casi completa, con un tirador para cerrarla y las flechas ‹ ›.
- **Tablas:** 3 columnas visibles y el resto al tocar la fila.
- **Rótulos directos:** como máximo 3 por gráfico (inicio, fin y el extremo que importa). El resto queda en la lectura y
  en "Ver como tabla".
- **Formato corto en ejes y rótulos:** "359 k", "18,1 k", "−5,1 k". En lecturas y tablas, la cifra completa ("USD
  359.107").

---

## 10. Qué NO mostraría y por qué

| No mostrar | Por qué | En su lugar |
|---|---|---|
| **Barras de patrimonio con el eje desde 100.000** (como el gráfico "Evolución Balance Real" del Dashboard del Value CG) | Exagera el crecimiento: 123.764 contra 266.647 se ven 7 veces más altas cuando en realidad son 2,2 veces | Línea con eje en 0 (V3) |
| **Eje de fechas por categoría** que pone 01/07/2025 al lado de 01/02/2026 (mismo gráfico) | Oculta un hueco de 7 meses y la primera "semana" parece una semana más | Eje de tiempo real con la banda "sin datos" |
| **"Bruto" apilado arriba del "Neto"** (gráfico "Ganancia Semanal" del Dashboard) | El bruto ya incluye al neto (`H = E + L + P + R + T + N`): se cuenta dos veces. El 08/02 se ve en ~52 k cuando el bruto es 28.977 | Interruptor después / antes de gastos (V4) |
| **Líneas de tendencia exponenciales** (las dos del Dashboard) | Sugieren una proyección que nadie hizo y que los datos no sostienen (desde septiembre la ganancia ronda cero, H3) | Mediana del período como referencia |
| **Torta o barra al 100% de la composición** | Hay grupos negativos; con negativos los % pasan del 100% (pesos al 148% en abril) | Barras divergentes (V6a) y área de 3 series positivas (V6b) |
| **Volumen** ("Volumen Prom") y **"Renta sobre volumen"** | Se carga a mano, no se sabe cómo se calcula y tiene valores repetidos entre hojas (Debe 479.840,65 y Haber 474.180,00 iguales en 4 hojas de abril y mayo) | El volumen bien calculado está en el Tablero semanal del Registro. Acá, como mucho, una fila "cargado a mano" en V7 (P1) |
| **"Operaciones"** | Vale 338 en 12 hojas seguidas (20–26/07 a 12–18/10): está copiado | Nada |
| **"VARxCAP" (274,97%) o "renta sobre aportes"** como titular | Compara el patrimonio de hoy, con ganancias reinvertidas, contra los 71.111 aportados. Parece una rentabilidad y no lo es | Si la síntesis lo quiere, que vaya en Socios, con su definición |
| **"Renta sobre capital promedio mensual" (27,82%)** del Dashboard | Promedia como si fuera un mes el tramo julio 2025–enero 2026 | Ganancia del mes / patrimonio al inicio del mes, solo en la lectura de V5 (P1) |
| **Tablas de máximo y mínimo** | Sin contexto, el máximo (42.940) es justamente la semana sin explicar | Las marcas ? y ◆ sobre las barras |
| **Variación semanal caja por caja como gráfico principal** | Las cajas incluyen pendientes; la de dólares billete va de −154.612 a +115.529. Casi todo es plata que se mueve de una caja a otra | Cascada por grupo en V7, que cierra con el total |
| **Dos ejes Y** (patrimonio y ganancia, o pesos y dólares, en un mismo gráfico) | Inventa relaciones entre las series según dónde caiga cada escala | Gráficos separados con el mismo eje X, uno debajo del otro |
| **Garantías, reales y libras como patrimonio** | La planilla no las suma al Neto | Fila "no suma" en la tabla de cajas |
| **La hoja "Semanales"** | Tiene valores viejos que no coinciden con la Calculadora (14/06: 254.204,96 contra 261.617,18) | Calculadora |
| **Rojo y verde para semanas negativas o positivas** | 6 de las 10 negativas son semanas de gastos grandes: el rojo alarmaría sin motivo | Posición respecto de cero, y el color reservado para datos dudosos |
| **Promedio móvil, bandas de confianza o pronósticos** | Son 32 puntos con ajustes y saltos sin explicar, y los dueños no son analistas | Una sola mediana de referencia |

---

## 11. Sistema visual y textos

- **La misma familia que el Tablero semanal** (`docs/tablero_v2_spec.md` §6): los mismos tokens claro y oscuro,
  tipografía de sistema, tarjetas y función de formato es-AR con "−". Ya están validados con el validador de paleta y los
  dueños ya los conocen.
  - Barras y líneas en `--dato`, con la semana foco en `--dato-foco`.
  - Las 3 series de V6b (Disponible · Proyectos · USDT General y deuda), en orden fijo, con `--op-2`, `--op-1` y
    `--op-resto`, que ya pasan como paleta categórica en los dos temas. Llevan leyenda y rótulo directo, porque son ≤ 4.
  - Las 4 categorías de V8 usan las mismas tres más `--dato`. **Hay que volver a correr el validador** con ese cuarteto
    antes de cerrarlo.
  - `--warn-ink` solo para ? y ⚠, siempre con ícono y palabra.
  - El ajuste ◆ es el color de datos al ~40% de opacidad. La textura rayada queda como alternativa solo para el modo de
    alto contraste o la impresión.
- **Marcas:** barras de 24 px de ancho como máximo, extremo redondeado de 4 px, cuadradas en la base y 2 px de separación
  entre barras y segmentos. Líneas de 2 px, puntos de 8 px como mínimo y grilla de 1 px sólida y tenue (nunca punteada,
  porque se lee como "proyección"). El único punteado es el contorno de "? sin explicar", a propósito.
- **Números:** "USD 359.107" en indicadores y tablas; "359 k" en ejes; "18,1 k" en rótulos. Pesos: "$ 180,1 M (≈ USD
  117.360)". Semanas: "12–18 oct" o "10–23 ago (2 sem.)". Porcentajes sin decimales salvo debajo del 10%.
- **Palabras de la interfaz** (sugeridas; las decide el informe de usuario):
  - "Patrimonio neto" y no "Capital" ni "Balance real".
  - "Ganancia de la semana" y no "GANxCORTE".
  - "Antes de gastos" y no "Bruto".
  - "Retiros de socios" y no "Dividendos" a secas, porque incluye una liquidación.
  - "Proyectos" y no "Inversiones", porque INVERSION en la planilla es un egreso.
  - "Disponible" para cajas y monedas.
- **Glosario mínimo**, en el "?" de cada vista: patrimonio neto, ganancia de la semana, antes de gastos, retiros de
  socios, ajuste extraordinario, semana doble, cotización usada, proyectos, USDT General (participación del 66%), cara
  chica / malos / cambio y "no suma".

---

## 12. Decisiones que tomé y que la síntesis tiene que confirmar

| # | Decisión | Alternativa | Por qué elegí esta |
|---|---|---|---|
| D1 | **Ganancia = variación del patrimonio + retiros de socios de esa semana** | La "Ganancia Neta" tal cual la calcula cada hoja | Así arma la ganancia el Value CG (`E28 = B28 − B27`, con `B27 = B26 − 4.719`). Si no, una semana de reparto parece una pérdida: la de 16–22/03 daría −4.425 en vez de +18.247. La tabla V10 muestra las dos columnas para que el auditor concilie |
| D2 | La ganancia se **recalcula como `Neto_t − Neto_{t−1}`** en todas las semanas | Usar la celda "Ganancia" de cada hoja | En las primeras hojas esa celda mide cosas distintas (en `0903 - 1503` es Bruto − Neto anterior; en `1603 - 2203` es Bruto − Bruto anterior). En `1210 - 1810` es `#REF!`. La diferencia simple da 18.103,33, el valor que espera el dueño |
| D3 | Referencia "semana típica" = **mediana de las 8 semanas anteriores** (en V4, mediana del período elegido) | Promedio; promedio de 4 semanas | Con 42.940 y 18.349 en la ventana, el promedio no representa una semana normal. Hoy la mediana de las 8 anteriores es 826: honesta y bajita, y refleja que desde septiembre la ganancia ronda cero |
| D4 | El **ajuste USDT General se marca y no se reparte** | Prorratear 15.855 entre mayo y septiembre | Las liquidaciones no tienen fecha y repartir sería inventar |
| D5 | **"Con ajustes" por defecto** | "Sin ajustes" por defecto | Coincide con la planilla, y el ajuste se ve igual como segmento aparte y en la franja |
| D6 | La serie arranca el **01/03 (Calculadora)**; el Value CG anterior es opcional | Empezar en julio de 2025 | Hueco de 7 meses, carga a mano y diferencia de 48,74 en el 01/03 |
| D7 | **Retiros posibles dentro de INTERESES** (3.573 y 924,16) se tratan como retiros con "a confirmar" | Dejarlos como egresos | Los montos coinciden exactamente con los dividendos del Value CG (`T25`, `T39`) |
| D8 | **Grupos de composición fijos** (6) definidos por el **nombre de la caja** en la fila 1, no por los rótulos del bloque | Usar "Dólares", "Pesos", "Poligono 09", "Almafuerte" del bloque | Los rótulos del bloque apuntan a columnas corridas desde 27/07, y "Dólares" llega a incluir 183.532 de proyectos |
