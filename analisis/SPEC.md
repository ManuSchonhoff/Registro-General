# SPEC — Tablero "Value · Cambio General"

Síntesis de `00_inventario.md` (hechos), `01_negocio.md`, `02_datos.md`, `03_visualizacion.md`, `04_usuario.md` y
`05_riesgos.md`. Donde los informes se contradicen, la decisión y su motivo están en la sección 8. Montos en USD salvo
que se indique otra moneda. Fecha de los datos: cierre del domingo 18/10/2026.

---

## 1. Para quién es y qué responde

**Usuarios.** Los cuatro socios de Cambio General: el dueño que hace el cierre (carga la Calculadora todas las semanas),
Francisco y Jose (operan) y Alejo (no opera; es el que menos contexto tiene: los textos se escriben para él). No son
analistas. Lo miran sobre todo en el celular, después del cierre del domingo y al cierre de cada mes, cuando se decide
el dividendo.

**Su trabajo con el tablero.** Saber cuánto vale la financiera, cuánto ganó y si esa ganancia es "de verdad" (operación)
o viene de ajustes, saltos sin explicar o del dólar; dónde está la plata; si la operación cubre los costos; y cuánto le
toca a cada socio. Es la "tabla única para ir haciendo semana a semana" que el dueño pidió en la propia planilla (nota
`K18`/`K19` de las hojas desde junio).

**Preguntas, en orden de prioridad** (las P1–P8 son las de `01_negocio.md`; el usuario de prueba las tiene que poder
responder mirando el tablero):

| # | Pregunta | Dónde se responde |
|---|---|---|
| P1 | ¿Cuánto vale hoy la financiera y cuánto creció? | Tarjeta "Patrimonio neto" + gráfico de patrimonio |
| P2 | ¿Cuánto ganamos la última semana y cómo vienen las últimas? | Tarjeta "Ganancia de la semana" (con la cuenta de la semana) + barras semanales |
| P3 | ¿Cuánto ganamos en cada mes y cómo viene contra los anteriores? | Tarjeta "Ganancia del mes" + barras por mes + tabla de meses |
| P4 | ¿Cuánto es operación y cuánto son cosas extraordinarias? | Interruptor "Con ajustes / Sin ajustes", marcas ◆ ? ▼, franja "Para tener en cuenta", detalle de semana |
| P5 | ¿Cuánto le toca a cada socio y cuánto hay que repartir? | Sección "Socios" |
| P6 | ¿Dónde está la plata? ¿Cuánto está disponible? | Tarjeta "Disponible" + sección "¿Dónde está la plata?" |
| P7 | ¿La operación cubre los costos? ¿Cuánto gastamos por mes? | Sección "Gastos" |
| P8 | ¿Cuánto nos pega el dólar? | Bloque "Pesos y dólar" dentro de "¿Dónde está la plata?" + detalle de semana |
| P13 | ¿Cuál fue la mejor y la peor semana, y por qué? | Barras semanales con marcas + tabla de semanas ordenable |
| P15 | ¿Están bien cargados los números? | Sección "¿Le creo a estos números?" |

Fuera de alcance (lo responde el Registro General y su tablero, no esta planilla): clientes, resultado por operador,
spread, cheques en cartera, capital de inversores, detalle de cada gasto. El tablero lo dice cuando corresponde.

---

## 2. Fuentes

| Fuente | Uso | Regla |
|---|---|---|
| Calculadora Semanal (`datos/value/*.xlsx`, hojas `DDMM - DDMM`) | **Única fuente** de patrimonio, ganancia, cajas, egresos y cotización desde el 23/02/2026 | Cada hoja sale del **último archivo** (por nombre) que la trae. Hoy `1210 - 1810` sale del archivo `b` |
| Value CG, hoja `Tenencia` | Socios: % y capital al último mes cargado (junio) | Se lee tal cual, con su fecha a la vista |
| `config.json`, bloque `value` | Grupos de cajas, alias de encabezados, retiros que no están en la columna DIVIDENDOS, semanas a revisar, socios | Lo que no está en la planilla se carga acá, nunca en el código |
| Value CG, hojas `Value CG`, `Dashboard`, `Semanales` | **No se usan** como fuente (atrasadas, con valores que no coinciden, KPIs mal armados) | Ver 05_riesgos §9–10 |

---

## 3. Métricas (definición exacta y fórmula)

Notación: *t* = hoja semanal (orden cronológico); *t−1* = la hoja inmediatamente anterior; *d(t)* = días de la hoja (7;
14 en `1008 - 2308`).

### 3.1 Base (sale de la planilla)

| Métrica | Definición | Fórmula |
|---|---|---|
| **Patrimonio neto** `neto(t)` | Lo que vale Cambio General al cierre del domingo, todo en USD. Es el "Neto" de la hoja | Se **recalcula** evaluando la fórmula del renglón "Neto" de la hoja (`value/leer.py`) y se exige que coincida con el valor guardado (tolerancia 0,05). Si la celda guardada tiene error (`#REF!`), manda el recalculado |
| **Antes de egresos (planilla)** `bruto(t)` | El "Bruto" de la hoja | Igual que el Neto |
| **Egresos de la planilla** `egr(t)` | Lo que la hoja resta en "Egresos" (positivo) | `−` valor del renglón "Egresos" |
| **Cotización** `cot(t)` | Pesos por dólar usados en la hoja | `C8` si la fórmula de Pesos lo usa; si no, el divisor escrito en la fórmula (`/1410`) |
| **Aporte de cada caja** | Cuánto suma cada caja (fila 2 y fila 3 por separado) al Neto, en USD | Coeficiente de la caja en la fórmula del Neto × su valor. Cierra con el Neto en las 33 hojas |

### 3.2 Ganancia

| Métrica | Definición | Fórmula |
|---|---|---|
| Variación del patrimonio `var(t)` | Cuánto cambió el patrimonio contra el domingo anterior | `neto(t) − neto(t−1)`. La primera hoja no tiene |
| Ganancia según la planilla | La celda "Ganancia Neta" | = `var(t)` desde `2303 - 2903` (en las primeras hojas medía otra cosa; se muestra solo en el detalle de cada semana, en "Para el que arma la planilla"; las hojas sin "Ganancia Neta" muestran su celda "Ganancia", si la tienen, aclarando que medía otra cosa) |
| **Retiros de socios** `ret(t)` | Plata que sacaron los socios (dividendos, liquidación de un ex socio). No es pérdida | Columna DIVIDENDOS de la hoja (lo que la fórmula de Egresos resta de ella) **+** retiros cargados en `config.value.retiros` para esa semana (los que no están en DIVIDENDOS: marzo 22.672; 3.573 y 924,16 que la planilla tiene dentro de INTERESES) |
| **Ajustes a mano** `aj(t)` | Cambios de los valores fijos escritos a mano en el bloque (USDT General, Deuda): se generaron en otro período o son correcciones | `Σ` sobre los renglones fijos (los que la fórmula del Neto suma como constante): `valor(t) − valor(t−1)`. Hoy: +10.900 (13–19/04), −1.000 (11–17/05), +4.021 (25–31/05), +15.855,49 (12–18/10) |
| **Ganancia de la semana** (la principal) `gan(t)` | Lo que ganó el negocio en la semana | `var(t) + ret(t) − aj(t)` ("sin ajustes") |
| Ganancia con ajustes | Lo mismo, incluyendo los ajustes a mano | `var(t) + ret(t)` |
| **Egresos del negocio** `gas(t)` | Gastos, comisiones pagadas, intereses a inversores e inversión de la semana | `egr(t) − ret_dentro_de_egresos(t)`, desglosado por tipo según el coeficiente de cada columna en la fórmula de Egresos (GASTOS y FIJOS → Gastos; COMISIONES; INTERESES menos lo reclasificado como retiro; INVERSION) |
| **Antes de gastos** | Lo que dejó la operación antes de pagar gastos, comisiones, intereses e inversión | `gan(t) + gas(t)`, **siempre sin ajustes a mano** (el interruptor solo suma los ajustes a la ganancia después de gastos) |
| **Por semana** | Para comparar semanas de distinto largo | valor ÷ (`d(t)` ÷ 7). Solo cambia la hoja doble |
| **Semana típica** | Referencia para decir si una semana estuvo arriba o abajo de lo habitual | Mediana de la misma medida que se muestra (ganancia o antes de gastos, con o sin ajustes, por semana) de las **8 hojas anteriores** a cada semana (con al menos 3). La tarjeta compara la semana foco contra la suya; el gráfico semanal la dibuja como línea escalonada. Es una sola definición |

Control: `gan_con_ajustes(t) + gas(t)` = Ganancia Bruta de la planilla + retiros que no están en Egresos. El auditor lo
verifica semana por semana.

### 3.3 Mes

- **Regla de mes:** cada hoja va al mes de su **jueves** (= el mes con más días de la semana). Para la hoja doble, el
  jueves de su segunda semana (20/08 → agosto). Agrupa las mismas semanas que los meses cerrados del Value CG. Los
  montos difieren donde la definición de 3.2 suma retiros que el Value CG no sumó (abril: +3.573 de INTERESES; julio:
  +924,16): con ajustes, abril da 55.939,62 (Value CG 52.366,61) y mayo 29.747,29 (igual).
- **Ganancia del mes** = `Σ gan(t)` de las hojas del mes (o con ajustes). **Semanas del mes** = `Σ d(t)/7`.
- **Mes completo** si está cargada la hoja que contiene el último jueves del mes. Si no, el mes es "en curso": barra
  solo con contorno y "N de M semanas"; se compara por semana, nunca el total.
- **Por semana del mes** = ganancia del mes ÷ semanas del mes.

### 3.4 Composición del patrimonio

Cada caja se asigna a un grupo **por su encabezado** (`config.value.grupos`; alias en `config.value.alias`). El aporte
de la caja al Neto (3.1) se suma en su grupo. Los renglones fijos van a su propio grupo según la etiqueta.

| Grupo (orden fijo) | Cajas / renglones | Tipo |
|---|---|---|
| Proyectos (al costo) | POLIGONO, POLIGONO 20+13, ALMAFUERTE, columna sin título que heredó uno de estos nombres | Inmovilizado |
| Pesos | PESOS, TRANSFER, CHEQUES, RECAUDACION BX, bx, DEUDA PESOS | Disponible |
| Dólares billete | CARA CHICA, CAMBIO, MALOS, USD, USD BsAs, DEUDA USD | Disponible |
| Cripto | USDT (caja), TRX, USDT General (columna) | Disponible |
| Exterior y euros | LLC, Grabify y variantes, PayPal Ruso, CITY BANK, WISE US, PAYONEER, WISE, EUROS, REALES, LIBRAS | Disponible |
| Participación USDT General | renglón "USDT" del bloque (valor fijo a mano) | Inmovilizado (USDT General y deuda) |
| Deuda a cobrar | renglón "Deuda" del bloque (valor fijo a mano) | Inmovilizado (USDT General y deuda) |
| Garantías | MILLAMAPU, JEEP, GOL TREND, CHARCAS, PROMAR | Netean 0: no se dibujan |
| Egresos e ingresos de la semana | GASTOS, FIJOS, COMISIONES, INVERSION, INTERESES, DIVIDENDOS, ALQUILERES | Netean 0 en el Neto: no se dibujan |

- **Disponible** = Pesos + Dólares billete + Cripto + Exterior y euros. **USDT General y deuda** (antes "cargado a
  mano") = USDT General + Deuda. **Inmovilizado** = Proyectos + USDT General y deuda. Disponible + Inmovilizado =
  patrimonio.
- **Moneda de cada caja:** la de la fila de monedas; si la hoja no la tiene, `config.moneda_por_caja` o la del grupo.
  Si la caja es en euros pero la fórmula del Neto la suma 1 a 1 (WISE hasta 18–24 may), se muestra en USD con la
  aclaración "euros que la hoja suma 1 a 1". La semana en que la planilla pasa a convertirla (25–31 may, × 1,25) lleva
  ⚠ con el efecto (+852): no es movimiento de plata.
- **Columna sin título:** hereda el nombre de la misma columna de la hoja anterior si allí tenía uno (hoy `AH` →
  "POLIGONO 20+13") y queda marcada para revisar. Si no tiene de dónde heredar, va a "Sin nombre" (Disponible) y
  dispara un chequeo.
- **Pesos en ARS** `ars(t)` = aporte del grupo Pesos × `cot(t)`.
- **Efecto estimado del dólar** = `ars(t−1) × (1/cot(t) − 1/cot(t−1))`. Es una aproximación (supone que los pesos
  quedaron quietos toda la semana): se muestra en el detalle, en el bloque "Pesos y dólar" y como renglón de la cascada
  del período; nunca se resta de la ganancia de la semana.
- **Sensibilidad** = `ars(t)/cot(t) − ars(t)/(cot(t)+10)`: cuánto baja el patrimonio si el dólar sube $ 10. Con
  una suba del 10 %: pesos en USD × (1 − 1/1,1).

### 3.5 Socios

- % y aporte de cada socio: `config.value.socios` (de la hoja Tenencia: Manuel, Francisco y Jose 28,13 % y 20.000;
  Alejo 15,62 % y 11.111,11).
- **Capital al último cierre de Tenencia** (30/06): se lee de la hoja Tenencia (última fila con capital por socio). Se
  muestra con su fecha; **no** se proyecta como Neto × %.
- **Lo ganado por cada socio** = % del socio × ganancia con ajustes desde la Tenencia (es lo que suma al capital
  estimado). La "parte de la ganancia del período elegido" por socio ya no se muestra: el usuario de prueba la confundía
  con lo que se cobra. La sección Socios no cambia con los filtros.
- **Capital estimado a la última semana** = capital de la Tenencia + % × ganancia con ajustes de las semanas cuyo mes
  (regla del jueves) es posterior al último mes de la Tenencia (hoy, desde 29 jun–5 jul). No descuenta dividendos
  pagados después (hay uno: 924,16 de 6–12 jul, dividendos de junio dentro de INTERESES). Su total difiere del patrimonio en lo que la Tenencia descontó por su cuenta;
  la diferencia se muestra.
- **Dividendo según la regla de la Tenencia** = 10 % de la ganancia **sin ajustes** de cada mes posterior al último
  cierre de Tenencia (un mes con pérdida no reparte). Los ajustes a mano de esos meses (ganancia de USDT General de
  otros meses cargada de golpe) van en una fila aparte con su 10 %. Rotulado "lo que daría la regla, no lo que se
  pagó". Así octubre no sugiere repartir una ganancia que es de mayo a septiembre.

---

## 4. Estructura

Una sola página que se recorre de arriba abajo (no hay pestañas): resumen arriba, después el porqué y al final la
consulta. Encabezado fijo con el nombre, la semana foco y una fila de chips que salta a cada sección.

### 4.1 Encabezado y filtros (fijos)

- Botón **≡** que abre el período, los ajustes y la lista de secciones (el encabezado queda fijo, así se llega a cualquier sección desde
  cualquier lugar, también en el celular).
- **Título** "Value · Cambio General" y **chip de semana foco** ("12–18 oct ▾"): abre la lista de semanas (la más nueva
  arriba, con sus marcas). Elegir una cambia la foco (tarjetas, composición, detalle).
- **Línea de estado:** "Cierre del domingo 18/10 · Dólar $ 1.535 · Euro USD 1,25 · Tenencia al 30/06".
- **Filtros globales** (una fila): **Período** [Todo · Últimos 3 meses · Últimas 8 semanas · Desde… ] (el "Desde" deja
  elegir la semana de inicio y la de fin; "Últimos 3 meses" = las hojas que terminan después de la fecha del último
  domingo menos 3 meses; "Últimas 8 semanas" = las últimas 8 hojas; elegir un período vuelve la semana foco a la
  última) y **Ajustes** [Sin ajustes · Con ajustes], con sus rótulos visibles también
  en el celular. Afectan a gráficos, tarjetas de período y tabla (Socios y Gastos no cambian con el interruptor de
  ajustes). Por defecto: Todo y Sin ajustes.

### 4.2 Secciones

1. **Resumen** (primera pantalla)
   - Si la semana foco no es la última: franja "Estás mirando la semana X (dólar $ Y)" con "Volver a la última".
   - **Cómo venimos** (veredicto en una frase, sigue el interruptor de ajustes y lo dice): un número principal con su
     signo, la ganancia por semana de las últimas 8 hojas hasta la foco sin las semanas a revisar, y "antes venía en"
     las 8 hojas anteriores sin las semanas a revisar; contándolas, en letra chica. Los tramos se nombran por sus semanas reales (una hoja doble
     cuenta dos). Fondo de advertencia si es negativa o menos de la mitad que la de las anteriores.
   - Cuatro tarjetas: **Patrimonio neto** (número principal) · **Ganancia de la semana** · **Ganancia del mes** ·
     **Disponible**. Cada una con una sublínea que evita el error más común y su "?".
     - Patrimonio: "+X desde el 01/03 · N veces lo aportado (71.111)" (con otro período, desde el patrimonio de la
       semana anterior al inicio del período); sublínea "La mitad está en proyectos: ver Disponible".
     - Ganancia de la semana: la **cuenta de la semana** en renglones (antes de gastos → total pagado → ganancia →
       ajustes y retiros → el patrimonio subió; sin retiros, el último total dice "= lo que subió el patrimonio" y no se
       repite). Comparación con la semana típica en palabras ("mejor que / parecida a / peor que
       la semana típica"), sin rojo ni verde.
     - Ganancia del mes: total del mes de la foco, "N de M semanas" si está en curso, y "por semana" contra el mes
       anterior por semana.
     - Disponible: monto y % del patrimonio; "Inmovilizado X (%): proyectos X y USDT General y deuda X".
   - **Franja "Para tener en cuenta"**: una franja con las semanas a revisar (un botón por semana que abre su detalle) y
     otra con el total de puntos para revisar en la planilla (el mismo número que la lista de "¿Le creo…?", que abre). El ajuste a mano de la última semana ya está
     en la tarjeta de la semana y no se repite.
   - **Lo que ganamos en el período y de dónde salió** (cascada, sigue al período, no depende del interruptor):
     patrimonio al inicio + **operación** (ganancia de las semanas normales, ya descontado el total pagado)
     + semanas a revisar (su ganancia, el mismo número de los avisos) + ajustes a mano − retiros = patrimonio al final,
     con la operación partida en **operación sin el dólar** (= ganancia de las semanas normales − efecto del dólar del
     período) y **efecto del dólar** (el de todo el período, el mismo de Pesos y dólar). No hay un renglón "antes de
     gastos" (el único "antes de gastos" del período es el de Gastos). Debajo, una nota: la operación y las semanas a
     revisar ya tienen restado el total pagado del período (el mismo de Gastos). Arriba, una frase: cuánto pasó el patrimonio y cuánto dejó la operación, por
     semana, por mes y como % por mes del **patrimonio promedio** del período (promedio simple del Neto de sus hojas; la hoja
     doble cuenta una vez). **Por mes = semanas normales × 12 ÷ 52** (las mismas semanas que el total). Los ajustes se
     rotulan por renglón ("USDT General +30.776, deuda −1.000").
   - **Patrimonio semana a semana**: línea con área suave, eje en 0, eje X de tiempo real. Rótulos solo en el inicio,
     el final y el mayor salto de una semana. Arranca en la semana base del período (la anterior a su primera
     semana, la misma del "desde el…" de la tarjeta y de la cascada); lo mismo el gráfico de evolución. (Anillo en el punto y "mayor salto: +42,9 k (24–30 ago)" arriba a la
     izquierda, que entra también en el celular). "Ver como tabla" con patrimonio y cambio por semana. Sin íconos de eventos (están en el gráfico de
     ganancia). Lectura fija arriba del gráfico (semana, patrimonio, variación). Tocar = cambiar foco; "Ver semana"
     abre el detalle.

2. **Ganancia**
   - Cortes propios: [Por semana | Por mes] y [Después de gastos | Antes de gastos].
   - Barras con base en 0 (un solo color; negativas hacia abajo). Ajuste ◆ como segmento claro apilado (solo con
     "Con ajustes"; con "Sin ajustes" queda el ícono). Semana doble con doble ancho y alto por semana. Línea escalonada
     con la semana típica (3.2), rotulada en la leyenda con su último valor. Mes en curso solo con contorno. Meses con
     semanas a revisar: contorno punteado y "?".
   - Promedios "por mes" (rendimiento, gastos): total ÷ (semanas × 12 ÷ 52), nunca por meses calendario.
   - Encabezado de la sección: "Ganancia del año (desde 2–8 mar; enero y febrero no están)" con el período "Todo", o
     "Ganancia del período (…)": total, por semana, semanas, cuánto es de semanas a revisar (en la medida elegida) y
     cuánto da por semana sin ellas.
   - Tocar una barra o un punto abre el detalle de esa semana (la lectura lo dice); en la vista por mes, fija la lectura del mes (que dice
     cuánto da el mes sin las semanas a revisar; la tabla por mes tiene esa columna).
   - En el gráfico solo van las marcas ? y ◆; ▼, ⧉ y ⚠ están en la tabla de semanas.
   - La cascada del período está en el Resumen.
   - **Cómo venimos**: tabla corta que compara tramos por semana (todas y sin las semanas a revisar), dentro del
     período y según los interruptores. Con 10 hojas o más en el período: las últimas 8 hojas, las 8 anteriores (o las
     que haya en el período) y el resto; si no, el período contra todas las semanas anteriores. Cada tramo se nombra por
     sus semanas reales. Con el período "Todo" y la última semana como foco, los dos primeros tramos son los del
     veredicto del Resumen.
   - **Rendimiento y volumen**: por tramo (período y, con 10 hojas o más, las últimas 8 hojas, nombradas por sus
     semanas reales): ganancia de las semanas
     normales por mes (semanas × 12 ÷ 52) y ese monto como % del patrimonio promedio y de lo disponible promedio de las
     semanas del tramo. Lo operado en el período: suma del "Volumen Prom" de cada hoja (en las hojas de marzo a mayo,
     que no lo tienen, el renglón "Promedio": en general (Debe + Haber) ÷ 2, en algunas hojas un número pegado), y por
     semana. Cada 100 USD operados, **solo en las
     semanas normales**: antes de gastos y después de gastos (sin ajustes). Cuántas semanas repiten el volumen de la
     anterior.
   - Tocar un mes filtra las barras semanales a ese mes.

3. **¿Dónde está la plata?** (semana foco)
   - Barras horizontales divergentes por grupo (orden fijo de 3.4), con monto y %. Las negativas, a la izquierda con
     "(debemos)".
   - Evolución: área apilada de 3 series (Disponible · Proyectos · USDT General y deuda). Si en alguna semana una serie es
     negativa, se dibujan líneas en vez de área apilada.
   - **Pesos y dólar**: "$ 180,1 M ≈ USD 117.360 (33 %) · si el dólar sube $ 10, el patrimonio baja ≈ USD 760 · efecto
     estimado del dólar en el período: X".
   - **Proyectos** (monto, composición y semanas en que cambiaron, con qué proyecto cambió) y **USDT General** (monto,
     total cargado y semanas en que se cargó; la planilla no tiene lo invertido ni fechas de liquidación, así que no se
     calcula rendimiento y se dice qué dato falta).

4. **Gastos** (siempre sin ajustes a mano: es la operación contra los costos; no cambia con el botón)
   - Tabla por mes con la ganancia en la segunda columna (se ve sin deslizar en el celular) y el promedio por mes de
     los gastos fijos y varios en la nota.
   - Barras por mes agrupadas, mismo eje: "Antes de gastos" y "Total pagado" (gastos fijos y varios + comisiones +
     intereses + inversión). "Total pagado" es el nombre único de esa suma en todo el tablero.
     La diferencia es la ganancia del mes, rotulada.
   - Tabla por mes con el desglose por tipo. Retiros de socios en una fila aparte ("no es gasto").

5. **Socios**
   - Primero, **"Para repartir según la regla del 10 %"**: el número principal es **"Para repartir ya"** = seguro + del
     ajuste de USDT General, con una ficha por socio (entra en el celular sin deslizar) y "y X más si se aclara agosto";
     debajo, el total si se aclaran las semanas a revisar. Las tres partes: **seguro** (meses sin las semanas a revisar), **del ajuste de USDT General**
     (10 % de los ajustes de esos meses) y **depende de las semanas a revisar** = Σ por mes de [10 % × máx(0, ganancia
     del mes) − 10 % × máx(0, ganancia del mes sin las semanas a revisar)] (hoy agosto entero: 5.872, porque sin esas
     semanas agosto pierde y no reparte). Dice si se pagó según la planilla: no hay retiros de socios registrados
     después del cierre de la Tenencia salvo los que se listan (hoy, solo 924 en 6–12 jul, dividendos de junio). La tabla mes · 10 % ·
     ganancia sin ajustes · por socio (con la fila aparte de ajustes, 3.5) queda en "Ver mes por mes".
   - Después, **"Capital de cada socio (no es plata para cobrar)"**: una ficha por socio que cierra a la vista: capital
     estimado al último domingo = capital al 30/06 (Tenencia; el total es la suma de los 4 socios, con sus centavos) +
     ganado desde la Tenencia (con ajustes y con las semanas a revisar). Notas: que lo ganado queda en el capital, los
     aportes y que los % suman 100,01 %. Un desplegable explica por qué el capital estimado no da igual al patrimonio: (Neto al
     cierre de la Tenencia − capital de la Tenencia) − retiros posteriores − el 0,01 % de más sobre la ganancia.
   - Retiros registrados: fecha, monto, detalle, "a confirmar" cuando corresponde.

6. **Todas las semanas**: tabla (la más nueva arriba; en el celular se repiten los títulos cada 8 filas): semana con sus marcas al lado · patrimonio · ganancia · antes
   de gastos · total pagado · retiros · ajustes · cotización, con la leyenda de las seis marcas abajo. La primera
   columna queda fija al deslizar. La celda de ganancia de la planilla se ve en el detalle de cada semana.

7. **¿Le creo a estos números?**: arriba, "¿La última semana está bien cargada?" en criollo y los chequeos OK; los de
   "Revisar" van plegados en "Lo que hay que revisar en la planilla" y los "Info" en el detalle técnico. Incluye que REALES
   (y LIBRAS) nunca entran en la fórmula del Neto, con el máximo y su semana. Más "Cómo se calcula"
   (las fórmulas de la sección 3, en palabras) y el **glosario**.

**Detalle de una semana** (hoja inferior en el celular, panel lateral en escritorio): cabecera con ‹ ›; tres números
(patrimonio, ganancia, total pagado); "Por qué:" en una línea (antes de gastos contra lo típico, si fue semana de
costos fijos, el dólar si movió más de USD 1.000, los ajustes); la cuenta de la semana; "¿De dónde salió?" (cascada por grupo, del patrimonio
anterior al actual, y cuánto vino de saldos, de pendientes y de USDT General y deuda; las garantías suman cero y no
entran en ese reparto); marcas con su explicación; tabla de cajas (caja con su monto en moneda original debajo, USD,
cambio; cajas en cero escondidas detrás de "ver todas"); cotización (y si se repitió), efecto estimado del dólar; lo
operado (volumen pegado a mano), antes de gastos **sin ajustes** cada 100 USD operados y las referencias 2 % / 1 % /
0,5 % **leídas de las celdas de la planilla** (si la hoja las calcula sobre otra base, se avisa), sin veredicto; "En la
planilla: hoja X, patrimonio en B16; la celda de ganancia dice Y / da error".

### 4.3 Interacciones

- Lectura fija arriba de cada gráfico (no tooltip flotante en el celular; tooltip en escritorio con el mismo texto).
- Tocar/clic una barra o punto: cambia la semana foco; botón "Ver semana" abre el detalle. Abrir el detalle (desde una
  fila, un aviso o "Ver semana") **no** cambia la semana foco del tablero. Teclado: flechas
  recorren semanas, Enter abre, Esc cierra.
- Cada gráfico tiene "Ver como tabla".
- `#semana-AAAA-MM-DD` en la URL abre esa semana; las preferencias (filtros) se recuerdan en el navegador si se puede.

---

## 5. Marcas (vocabulario fijo)

| Marca | Significa | Cómo se detecta |
|---|---|---|
| ◆ Ajuste a mano | Cambió un valor fijo del bloque (USDT General, Deuda) | `aj(t) ≠ 0` |
| ? A revisar | Salto sin explicar | `config.value.semanas_a_revisar`, o ganancia por semana a más de 2,5 desvíos robustos de la mediana (MAD × 1,4826) |
| ⧉ Dos semanas | La hoja abarca 14 días | `d(t) = 14` |
| ▼ Retiro de socios | Hubo retiros | `ret(t) > 0` |
| ⚠ Dato dudoso | Solo lo que **puede cambiar los números**: cotización igual a la de la hoja anterior, valores que no entran en la fórmula (sin garantías, REALES ni LIBRAS, que tienen su chequeo global), una caja en euros que cambia de criterio (1 a 1 ↔ × euro), cambio de la cotización del euro (revalúa los euros de la semana anterior), nota "NO CONTAR"/"REVISAR" en el bloque | Chequeos automáticos |
| • Gastos grandes | Semana de costos fijos | columnas GASTOS + FIJOS de la semana ≥ `config.value.umbral_gastos_grandes` (5.000) |

Cada marca va con ícono y palabra, nunca solo color. Color de estado (`--warn`) solo para ? y ⚠. Lo que es solo para
corregir la planilla y no cambia los números (celda de ganancia con error, hoja en dos archivos, columna sin título) no
lleva ⚠: va con ✎ en "Para el que arma la planilla" del detalle de la semana y en "¿Le creo…?". El control de cada
semana responde "¿Está bien cargada?" con "sí" (los números coinciden con la planilla) o "a medias" (salto sin explicar
o ⚠).

---

## 6. Textos de ayuda y glosario

**Ayuda de cada tarjeta y gráfico** (botón "?"): *Qué es · Cómo se calcula · De dónde sale* (hoja y celda). Textos
base (el código los completa con los números):

- **Patrimonio neto.** Qué es: lo que vale Cambio General al cierre del domingo, todo pasado a dólares: cajas (con
  sus pendientes), proyectos al costo, la parte de USDT General y lo que nos deben. No es todo plata disponible. Cómo se
  calcula: pesos ÷ cotización de la semana, euros × 1,25. De dónde sale: Calculadora, "Neto" (la celda cambia según la hoja; el detalle de cada semana la muestra); en el Value CG se
  llama CAPITAL.
- **Ganancia de la semana.** Qué es: cuánto creció el patrimonio contra el domingo anterior, sumando lo que retiraron
  los socios (no es una pérdida) y sin los ajustes a mano. No es plata que entró: también la mueven el dólar y los
  pendientes. Cómo se calcula: patrimonio − patrimonio anterior + retiros − ajustes. De dónde sale: Calculadora
  ("Ganancia Neta", celda según la hoja) y los retiros cargados en la configuración.
- **Antes de gastos.** Lo que dejó la operación antes de pagar gastos, comisiones, intereses a inversores e inversión.
  En la planilla: "Ganancia Bruta" (sin los dividendos).
- **Ajustes a mano.** Cambios en los valores fijos del bloque (USDT General y Deuda). Ejemplo: +15.855 de USDT General
  ganados de mayo a septiembre y cargados el 18/10.
- **Semana típica.** La mediana de la ganancia por semana de las 8 hojas anteriores (la hoja de dos semanas cuenta una
  vez, con su promedio semanal; en el tablero se dice "las 8 semanas anteriores"): la mitad ganó más y la mitad menos.
  No la mueve una semana extraordinaria.
- **Disponible.** Pesos, dólares billete, cripto y cuentas del exterior, con sus pendientes. Sin lo inmovilizado:
  proyectos, USDT General y deuda.
- **Mes.** Cada semana se cuenta en el mes de su jueves (el que tiene más días de esa semana), como en el Value CG.

**Glosario** (en "¿Le creo…?", con buscador; cada término dice cómo aparece en la planilla): Patrimonio neto (Neto,
CAPITAL), Ganancia de la semana (Ganancia Neta, GANxCORTE), Antes de gastos (Ganancia Bruta, BRUTOxSEM), Egresos,
Retiros de socios (DIVIDENDOS), Ajuste a mano, Pendientes (fila 3), Cotización (C8), Proyectos (POLIGONO, Almafuerte,
columna sin título), Participación USDT General (renglón USDT) vs. caja USDT, Deuda a cobrar, Cara chica, Malos,
Cambio, TRX, Garantías, Semana doble, Semana típica, Lo operado (Volumen Prom).

---

## 7. Stack y actualización

- **Mismo patrón que el tablero v2 del Registro**: Python arma un JSON con todos los números (`value/tablero.py`) y lo
  inserta en una plantilla HTML sin datos (`value/tablero_plantilla.html`), con JavaScript sin dependencias y gráficos
  en SVG dibujados a mano. Misma familia visual (tokens claro/oscuro, tipografía de sistema). Un solo archivo HTML,
  sin pedidos a la red.
- **Comando:** `python3 value.py` (opciones `--datos`, `--salidas`, `--fecha`). Lee todos los `.xlsx` de
  `datos/value/` (cada hoja sale del archivo más nuevo que la trae), aplica `config.json` → `value` y escribe:
  - `salidas/value/<fecha>/tablero_value.html` y `tablero_value_datos.json` (los números, para auditar);
  - `salidas/value/tablero_value_artifact.html` (ruta fija para republicar el mismo Artifact).
  - Código de salida 0; 2 si el Neto recalculado no coincide con el guardado en alguna hoja o una fórmula no se pudo
    evaluar (igual escribe, con el aviso adentro); 1 si hubo un error.
- **Publicación:** como Artifact privado, siempre a la misma URL (se guarda en `salidas/value/estado_publicacion.json`).
- **Cuando cambia la planilla:** copiar la Calculadora nueva (completa o la hoja suelta) a `datos/value/` con la fecha
  adelante (`AAAA-MM-DD_<nombre>.xlsx`), correr `python3 value.py` y republicar. Si cambia algo que la planilla no
  tiene (un retiro cargado en otra columna, una semana explicada, la fecha de una liquidación de USDT General), se
  edita `config.json` → `value`.
- `datos/` y `salidas/` no se versionan (`CLAUDE.md`).

---

## 8. Decisiones tomadas sin confirmación (y contradicciones resueltas)

| # | Tema | Decisión | Por qué |
|---|---|---|---|
| D1 | Qué es "ganancia" | Variación del patrimonio + retiros − ajustes a mano | Así arma la ganancia el Value CG (suma de vuelta los dividendos). Sin sacar los ajustes, la semana del 18/10 parece la mejor desde agosto (riesgo 1, crítico) |
| D2 | **Ajustes por defecto** (viz: con; usuario y riesgos: sin) | **Sin ajustes** por defecto, con el ajuste siempre visible (ícono ◆ y renglón en la cuenta de la semana) y el interruptor para incluirlo | El error más caro es repartir dividendos sobre una ganancia inflada. "Con ajustes" queda a un toque y el detalle de cada semana trae la celda de ganancia de la planilla para conciliar |
| D3 | **Mes de cada semana** (datos/viz/negocio: jueves; riesgos: domingo) | Mes del jueves | Agrupa las mismas semanas que los meses cerrados del Value CG (los montos difieren solo por los retiros que el Value CG no sumó; ver 3.3) |
| D4 | **Veredicto por volumen** (usuario lo pide; datos y riesgos dicen que el volumen es poco confiable) | Sin veredicto en la primera pantalla: se compara con la semana típica. El volumen se muestra en el detalle y en "Rendimiento y volumen" como referencia; las referencias del dueño (2 / 1 / 0,5 %), en la parte plegada del detalle | El volumen pegado a mano ("Volumen Prom") existe desde mayo y está copiado en varias hojas; antes, la hoja tiene el "Promedio" de Debe y Haber. Un veredicto sobre él daría una conclusión falsa con aspecto de precisa |
| D5 | **Agrupar el patrimonio** (viz: 6 grupos; usuario: 4 partes; riesgos: por naturaleza) | 7 grupos por caja para la foto y 3 (Disponible · Proyectos · USDT General y deuda) para la evolución; la tarjeta dice Disponible e Inmovilizado | Cubre las tres miradas: dónde está cada peso y cuánto es plata disponible |
| D6 | **Semanas sin explicar** (usuario: sacarlas del promedio; viz: marcarlas; riesgos: mostrar ambas cifras) | Se marcan con ? y se incluyen en los totales; "Cómo venimos" muestra los tramos con y sin ellas; la semana típica usa mediana | No se puede afirmar que no sean ganancia; tampoco que lo sean |
| D7 | Efecto del dólar (riesgos: barra aparte; viz: solo detalle) | En el detalle, en "Pesos y dólar" y como renglón propio de la cascada del período, siempre rotulado "estimado"; nunca se resta de la ganancia de la semana | Es una aproximación: restarlo de la ganancia mezclaría un número estimado con los de la planilla; en la cascada solo separa una parte de la operación |
| D8 | Retiros dentro de INTERESES (3.573 el 27/04–03/05; 924,16 el 06–12/07) | Se tratan como retiros, marcados "a confirmar" | Coinciden exacto con los dividendos del Value CG (`T25`, `T39`) |
| D9 | Ajuste de USDT General (15.855,49) | Queda en la semana en que se cargó (12–18/10) como ◆; no se reparte por mes | Las liquidaciones no tienen fecha; repartirlo sería inventar |
| D10 | Saltos de los valores fijos de abril y mayo (+10.900, +4.021, −1.000) | Se tratan como ajustes a mano igual que el de octubre | Mismo mecanismo; no hay forma de saber si fueron ganancia de esa semana |
| D11 | Columna `AH` sin título | Hereda "POLIGONO 20+13" de la hoja anterior y va a Proyectos; queda en "Revisar" | Es la misma columna con el mismo saldo; sacarla rompería el cierre con el Neto |
| D12 | Serie | Empieza el 23/02–01/03 (primera hoja). La historia anterior del Value CG no se muestra | Hueco de 7 meses, carga a mano y 48,74 de diferencia el 01/03 |
| D13 | Socios | Capital solo de Tenencia (al 30/06); la parte de cada socio se calcula sobre la ganancia del período, no sobre el Neto | El capital por socio no es Neto × % (riesgo 16) |
| D14 | Pendientes | Se suman como los suma la planilla; nota fija de que su signo está a confirmar; el detalle muestra cuánto de la variación vino de pendientes | No hay base para corregirlos (`signo_pendientes_confirmado: false`) |
| D15 | Ganancias de las primeras hojas | Se recalculan como diferencia de Netos (la celda guardada medía otra cosa) | Una sola definición para toda la serie |

**Cambios después de la primera verificación (fase 5).** El auditor no encontró montos mal calculados (2.845 números
comparados). Se corrigieron: la tarjeta del mes con una semana foco que no es la última (sumaba hasta la foco), las dos
"ganancias" de la tarjeta con ajustes (ahora "sin ajustes" y "con ajustes"), el reparto saldos / pendientes / cargado a
mano del detalle, el cambio de las cajas que no estaban en la fórmula de la semana anterior, la moneda de las cajas en
las hojas sin fila de monedas, el chequeo de renglones corridos y los textos que no seguían los interruptores. Por el
usuario de prueba: cascada del período (P4), capital estimado y totales en socios (P5), dividendos sin ajustes,
bloques de Proyectos y USDT General, tabla de semanas ordenable, tablas con primera columna fija en el celular, panel
de semana que entra en 390 px, filtros fuera del encabezado fijo y los chequeos técnicos en un desplegable aparte.

**Cambios después de la segunda verificación.** El capital estimado de los socios ahora cuenta desde la primera semana
de julio (29 jun–5 jul); el rendimiento conserva el signo; los promedios por mes usan semanas × 12 ÷ 52; la semana
típica es una sola (tarjeta y gráfico); los meses con semanas a revisar se marcan; la ⚠ de columna sin título, la
celda con error y la hoja repetida aparecen en el control de cada semana; los gráficos muestran solo las marcas
principales (? ◆ ▼ ⧉) y los datos dudosos quedan en la tabla y en el detalle.

**Cambios después de la tercera verificación.** El auditor no encontró montos mal calculados (unos 7.700 números) y el
usuario de prueba respondió P1–P8. Se corrigieron: el "% por mes" de la cascada (divide por los meses de las semanas
normales, las mismas del total); WISE en USD en las hojas que lo suman 1 a 1 y ⚠ en el cambio de criterio de 25–31 may;
las referencias 2 / 1 / 0,5 % leídas de la planilla; "cada 100 USD operados" siempre sin ajustes; chequeo global de
REALES; rótulo del mayor salto del patrimonio. Por el usuario de prueba: veredicto "Cómo venimos" arriba, cascada del
período en el Resumen con el dólar como renglón propio, "Mejor / peor que la semana típica", Inmovilizado explícito,
"USDT General y deuda" en lugar de "cargado a mano", "Total pagado" como nombre único, socios con lo que hay para
repartir primero, marcas al lado de la semana, botón ≡ de secciones, rótulos de los filtros en el celular, tabla de
cajas del detalle en 3 columnas, franja "Estás mirando la semana…", rendimiento y volumen del período (P9, P14), total
cargado de USDT General (P10) y qué proyecto cambió cada semana (P11).

**Cambios después de la cuarta verificación.** El auditor no encontró montos mal calculados (unos 4.750 números); el
usuario de prueba respondió P4 y P5 "a medias" porque había números que debían coincidir y no coincidían. Se
corrigieron: en la cascada, total pagado y dólar de todas las semanas (los mismos de Gastos y de Pesos y dólar) y la
operación como resto; lo que depende de semanas a revisar en los dividendos (5.872, no 6.129); el veredicto y la tabla
"Cómo venimos" con los mismos tramos y nombres por semanas reales; el veredicto sigue el interruptor; el rendimiento
sobre el patrimonio promedio; cada 100 USD operados antes y después de gastos, en semanas normales; el rótulo del mayor
salto también en el celular; "Ver como tabla" en patrimonio y evolución; "si el dólar sube 10 %"; socios con el capital
estimado primero y "su parte" aclarada; "¿Está bien cargada?" con un sí o no claro (el ⚠ dice si puede cambiar los
números); lo técnico del detalle plegado; aviso de deslizar arriba de la tabla de semanas; nombres de cajas legibles.

**Cambios después de la quinta verificación.** El auditor no encontró montos mal calculados (unos 3.000 números); el
usuario de prueba respondió P5 "a medias" (no quedaba claro cuánto se reparte de verdad). Se corrigieron: el signo de
"cada 100 USD operados"; la explicación de los 614 de socios (incluye el retiro de 924 de julio); "Polígono"; el
glosario del rendimiento; la celda "Ganancia" de las primeras hojas en el detalle técnico; el cambio de una caja que sale
de la fórmula (Euros −240 en 2–8 mar). Por el usuario de prueba: lo que hay para repartir separado en seguro / del ajuste
/ depende de semanas a revisar, por socio; "Ganó en el período" en vez de "su parte"; ⚠ solo cuando puede cambiar los
números; "¿Está bien cargada?" con sí / a medias; abrir el detalle no cambia la semana del tablero; ganancia "del año";
ajustes desglosados en la cascada y por qué el antes de gastos de Gastos es otro; la ganancia segunda en la tabla de
Gastos; las tablas se desvanecen a la derecha cuando hay más columnas; los meses del eje empiezan en marzo.

**Cambios después de la sexta verificación.** El auditor no encontró montos mal calculados (unos 12.500 números); el
usuario de prueba respondió P4 y P5 "a medias" (tres "antes de gastos" distintos; la tabla de capital no cerraba a la
vista). Se corrigieron: la cascada sin renglón "antes de gastos" (operación = ganancia de las semanas normales); el
capital como 30/06 + ganó desde entonces = capital estimado; lo que hay para repartir en fichas por socio y "según la
planilla, no se pagó"; "Cómo venimos" con un número principal; agosto sin las semanas a revisar; tocar un gráfico abre
el detalle y no cambia la semana del tablero; el chip "Semana ▾"; ⚠ por el cambio del euro 1,20 → 1,25 (+414); el eje
de evolución sin "feb"; "Por qué" en el detalle; ¿Le creo? con lo de la planilla plegado; títulos repetidos en la tabla
de semanas en el celular.

**Cambios después de la séptima verificación.** El auditor no encontró montos mal calculados (unos 15.800 números); el
usuario de prueba respondió P1–P8 salvo P5, "a medias" porque no había un número único de cuánto se reparte ya. Se
corrigieron: "Para repartir ya" (3.777) como número principal, con lo que depende de agosto aparte; el capital en fichas
que cierran a la vista y aclaran que incluyen las semanas a revisar; patrimonio y evolución arrancan en la semana base del
período; el primer mes de una sola hoja no se rotula; el tramo del rendimiento por sus semanas reales; "Por qué" en la
misma unidad en la hoja doble y "lo típico antes de gastos"; Gastos siempre sin ajustes; elegir un período vuelve a la
última semana; período y ajustes también en el menú ≡; el aviso de puntos a revisar con el mismo número que la lista, que
abre; la ayuda "?" como hoja abajo en el celular; los gráficos dicen que se pueden tocar.

**Cambios después de la octava verificación.** El auditor no encontró montos mal calculados (unos 24.000 números); el
usuario de prueba respondió P1–P8 salvo P4, "a medias" porque el dólar no tenía renglón propio en la cascada y porque,
con "Con ajustes", el "antes de gastos" del gráfico (19.370) no era el de la cuenta de la semana (3.515). Se
corrigieron: el dólar con renglón propio (operación sin el dólar 146.813 − 12.318 = 134.495); "antes de gastos" siempre
sin ajustes; la tabla de evolución desde la semana base; el rótulo de inicio que no se pisa con el anillo y el mayor
salto también cuando es el último punto; "—" en el mes sin semanas normales; la ayuda con "i" para no confundirla con
la marca "?"; el rótulo del interruptor ("Ajustes a mano (USDT General y deuda)"); "desde el cierre del…"; "Ganancia del
año, desde marzo"; el gasto por mes como número principal en Gastos; el redondeo de las fichas de socios; qué falta para
el rendimiento de USDT General; "Elegir…" en el menú.

**Preguntas para el dueño** (cambiarían números del tablero): qué es la columna `AH` y los +37.500 del 05–11/10; fecha
de cada liquidación de USDT General y si se cobraron a alguna caja; qué explica +42.940 (24–30/08) y el pendiente de
cheques (10–23/08); si se pagaron dividendos de julio a octubre y en qué columna; si los 3.573 y 924,16 de INTERESES son
dividendos; qué es la columna INVERSION; si "Deuda" 4.000 sigue vigente; si el alquiler de 3.600 con "NO CONTAR" se
cuenta.

---

## 9. Qué no se muestra (y por qué)

Renglones del bloque como categorías ("Dólares", "Pesos", "Poligono 09", "Almafuerte"); Operaciones y ticket promedio
(338 copiado); renta sobre volumen y sobre aportes como titular; KPIs del Dashboard del Value CG; "BRUTO" acumulado;
garantías como patrimonio; la hoja Semanales; rojo/verde para semanas negativas; promedio móvil, tendencias o
pronósticos; dos ejes Y; torta o barra al 100 % de la composición.
