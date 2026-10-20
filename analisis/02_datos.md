# 02 — Datos: qué representa cada fila, qué tan confiable es y qué se puede medir

Rol: **Datos**. Insumos: `analisis/00_inventario.md` y las planillas de `datos/value/` (sin modificarlas). Todos los
números de este informe salen de leer los Excel con `openpyxl` (fórmulas y valores guardados) y de un evaluador propio
de las fórmulas del bloque de cálculo. Montos en USD salvo que se indique otra moneda. Formato: punto de miles, coma
decimal. No se nombran clientes ni terceros (sí socios, operadores, cajas y proyectos).

---

## 0. Resumen en 10 puntos

1. **La unidad de análisis es el cierre semanal.** En la Calculadora, una hoja = una foto de saldos al domingo de cierre.
   Hay 33 hojas que cubren **34 semanas sin huecos ni solapamientos** (lunes 23/02/2026 → domingo 18/10/2026); una hoja
   (`1008 - 2308 (Dos Semanas)`) abarca 14 días.
2. **La serie reconstruida cierra al centavo.** Reevalué las fórmulas de las 33 hojas y los 33 Neto, Bruto y ganancias
   coinciden con los valores guardados. La hoja `1210 - 1810` corregida (archivo b) da exactamente lo que espera el dueño:
   Neto **359.107,17**, Ganancia Neta **18.103,33**, Bruto **360.374,25**, Ganancia Bruta **19.370,41**.
3. **Neto = caja + pendientes + inversiones + dos renglones fijos.** La Calculadora suma la fila 2 (saldo) y la fila 3
   (pendientes) de cada caja con el mismo signo. Al 18/10, **el 51,1 % del Neto son inversiones cargadas al costo**
   (Polígono 70.565,57 + una columna sin encabezado de 112.966), el 12,7 % son renglones fijos tipeados (USDT General
   41.536,49 y "Deuda" 4.000) y sólo el 36,2 % es caja más pendientes.
4. **La "Ganancia Neta" es una diferencia de stocks, no un resultado operativo.** Mete en la misma bolsa: distribuciones
   a socios (−22.672 el 22/03, −4.719 el 10/05, −2.510 el 07/06), ajustes retroactivos (+15.855,49 de USDT General el
   18/10), cambios de criterio (+1.265,67 el 31/05 por revaluar euros) y el efecto de la cotización (acumulado ≈ −12.318).
5. **Un outlier claro:** la semana 24–30/08 (+42.940,48) está casi 6 desvíos robustos arriba de la mediana (≈ 5.039 por
   semana). Se explica por la fila de **pendientes en USD**, que pasó de −45.347 a +14.119 (+59.466), mientras la caja
   en USD bajó 19.900. No hay en la planilla nada que lo justifique.
6. **Las columnas se mueven entre hojas** (GASTOS ocupa 8 letras distintas: Z, AA, AB, AC, AD, AE, AI, AJ). Cualquier
   lectura automática tiene que ir **por encabezado, nunca por letra**. Hay un encabezado reemplazado por el número 1
   (`A1` en 4 hojas) y una columna con 75.466–112.966 USD **sin encabezado** (`AH`, últimas 8 hojas).
7. **Dos etiquetas del bloque apuntan a la columna equivocada** desde `2707 - 0208`: "Poligono 09" lee GOL TREND y
   "Almafuerte" lee JEEP. Hoy no cambia el Neto (las garantías netean 0 y las inversiones reales entran por "Dólares"),
   pero hace que el renglón "Dólares" incluya ~180 mil de inversiones.
8. **Varios datos son constantes copiadas:** Operaciones = 338 en 13 hojas seguidas; Debe/Haber idénticos en 4 hojas;
   el Volumen de `0405 - 1005` es copia del de `2704 - 0305`; TRX = 1.734 fijo en 26 hojas; la cotización se repite
   en 6 rachas (1.525 en 4 hojas = 5 semanas); el euro está fijo en 1,20 y después en 1,25.
9. **Value CG coincide con la Calculadora del 08/03 al 28/06**, salvo diferencias explicables: −48,74 el 01/03,
   +22.672 el 22/03 (Value CG muestra el capital antes de la distribución), +4.719 y +2.510 en la ganancia de las semanas
   con dividendos (Value CG los suma de vuelta) y el volumen del 10/05 (686.863,60 contra 499.476,13 copiado).
10. **Métricas confiables:** Neto, ganancia semanal normalizada por días, ganancia mensual, egresos por tipo,
    composición del patrimonio, posición en pesos y efecto cotización. **Engañosas:** % de renta sobre volumen,
    promedio por operación, ganancia de la última semana sin separar el ajuste de USDT, "rentabilidad sobre aportes"
    (VARxCAP) y cualquier suma de garantías.

---

## 1. Fuentes y cuál manda

| Archivo / hoja | Qué tiene | Período | Rol para el dashboard |
|---|---|---|---|
| `2026-10-20a_Calculo_Semanal.xlsx`, 33 hojas `DDMM - DDMM` | Saldos por caja de cada cierre y bloque de conversión a USD | 23/02 → 18/10/2026 | **Fuente principal** |
| `2026-10-20b_Calculo_Semanal_1210-1810.xlsx`, hoja `1210 - 1810` | Versión corregida de la última hoja (renglón USDT + notas) | 12–18/10 | **Reemplaza** a la hoja homónima del archivo a |
| `2026-10-20_Value_CG_2026.xlsx` → `Value CG` | Histórico semanal tipeado: capital, ganancia, bruto, volumen, egresos acumulados | 01/07/2025, 01/02 → 28/06/2026 | Historia previa al 01/03 y control cruzado |
| Value CG → `Tenencia` | Aportes y participación de socios; dividendos = 10 % de la ganancia mensual | feb → jun 2026 | Datos de socios (aportes 71.111,11) |
| Value CG → `Dashboard` | Tablero viejo, apunta a Value CG | hasta 21/06 | No usar (ver §7, problemas 25–26) |
| Calculadora → `Semanales` | Copia vieja de cierres y ganancias con notas | 18/01 → 14/06 | Sólo por las notas ("Semana Corta", etc.) |
| Calculadora → `CONTROL` | Compara dos versiones de la fila 2 de `2206 - 2806` (35/35 columnas coinciden) | — | Hoja de trabajo, ignorar |
| Calculadora → `Volumen Mayo` | Debe/Haber de Manuel y Francisco en 3 cierres de mayo | 10–24/05 | Auxiliar, no conciliable con la serie |
| Value CG → 5 hojas ocultas (`Value 2025`, `Value 2026`, `Vago`, `Dante` y una hoja de liquidación) | Versiones viejas y liquidaciones | — | Ignorar (`Value 2025` tiene 136 `#REF!`) |

**Regla de versión:** cuando una hoja semanal aparece en más de un archivo, manda la del archivo más nuevo (sufijo `b`).
Verifiqué que en `1210 - 1810` las filas 1 a 5 de ambos archivos son idénticas celda por celda; cambian sólo `B13`
(USDT: `=10760+10900+4021` → `=10760+10900+4021+1608.48+…+2121.373333` = 41.536,49), las notas `I13:L24` y las
fórmulas de ganancia, que en el archivo b apuntan a `'05/10 - 11/10'!B16`, una hoja que no existe (6 celdas con `#REF!`:
B17, B19, B23, B24, C23, C24). La referencia correcta es `'0510 - 1110'!B16`.

---

## 2. Granularidad: qué representa cada fila

### 2.1 Calculadora Semanal (una hoja por cierre)

| Fila | Contenido | Tipo |
|---|---|---|
| 1 | Encabezado: una caja o cuenta por columna (CARA CHICA, CAMBIO, MALOS, USD, PESOS, CHEQUES, … GASTOS, INTERESES, DIVIDENDOS) | texto |
| 2 | **Saldo** de cada caja al cierre, pegado como valor desde el Registro General | número, moneda de la caja |
| 3 | **Pendientes** de esa caja (operaciones abiertas), pegados como valor | número, moneda de la caja |
| 4 | `=SUM(x2:x3)` en las hojas desde `2505 - 3105` | fórmula |
| 5 | En hojas viejas (`2302 - 0103` a `1805 - 2405`): la suma. En las nuevas: **código de moneda** (USD, ARS, EUR, REAL) | fórmula / texto |
| 7–29, columnas A–C | Bloque de cálculo: Dólares, Pesos, Euros, (Poligono 09, Almafuerte), Deuda, USDT, Egresos, (Ingresos), **Neto**, Ganancia Neta, **Bruto**, Ganancia Bruta, Volumen, Operaciones, % sobre volumen, referencias 2 % / 1 % / 0,5 % | fórmulas y valores |

Entonces el "hecho" básico es **(cierre, caja) → saldo, pendiente, moneda**, y a nivel hoja **(cierre) → cotización
ARS, cotización EUR, Deuda, USDT, Volumen, Operaciones, Neto, Bruto**.

**Stocks y flujos conviven en la misma fila.** Las cajas (USD, PESOS, CHEQUES, POLIGONO…) son saldos acumulados. Las
columnas GASTOS, FIJOS, COMISIONES, INVERSION, INTERESES, DIVIDENDOS y ALQUILERES son **flujos de esa semana** (se
reinician cada semana; por ejemplo, GASTOS de `0405 - 1005` = 6.872,07, igual al "GxSEMANA" de Value CG del 10/05).
El bloque suma esos flujos dentro de "Dólares" y los resta en "Egresos": en el Neto se cancelan; en el Bruto quedan.

**Fila 2 y fila 3 no son independientes.** Semana a semana se compensan casi exactamente (por ejemplo, `0806 - 1406`:
caja −298.217, pendientes +298.921; `0405 - 1005`: +234.997 / −229.841). Cuando una operación pasa de abierta a
cerrada, el monto se mueve de una fila a la otra. **Sólo la suma tiene sentido económico estable.**

### 2.2 Value CG (una fila por semana, con filas de texto intercaladas)

- Columna A: fecha del **domingo de cierre** (2026-03-08 ↔ hoja `0203 - 0803`) o un texto: nombre del mes (fila de
  subtotal), "Dividendos" (resta la distribución del capital), "Aportes", "Balance Actual".
- Columnas: B CAPITAL (= Neto), C P&L APORTE (= B − aportes 71.111,11), D VARxCAP (%), E GANxCORTE (ganancia semanal),
  F VARxCORTE (%), G BRUTO acumulado, H BRUTOxSEM, I VOLUMEN, J RENTA (%), K–T egresos acumulados y semanales
  (gastos, comisiones, inversión, intereses, dividendos), U–V alquileres, W USDT General, X Deuda.
- Cargado hasta el **28/06**; las filas de julio a diciembre tienen sólo la fecha.
- **La fecha 2026-03-01 está dos veces** (fila 11, cierre de febrero; fila 14, base de marzo).

### 2.3 Tenencia

Una fila por mes (y otra por su dividendo) con el capital y la cuenta de cada socio: Manuel, Jose y Francisco 28,13 %,
Alejo 15,62 % (el encabezado dice 15,63 %). Aportes: 20.000 × 3 + 11.111,11 = **71.111,11**. Dividendo mensual = 10 %
de la ganancia del mes (`H8 = H7/-10`). Cargada hasta junio.

---

## 3. Dimensión temporal

### 3.1 Cómo se deduce la fecha

- El nombre de la hoja es `DDMM - DDMM` = **lunes de inicio – domingo de cierre**, sin año. El año (2026) sale del nombre
  del archivo y de `config.json` (`"anio": 2026`). Las 33 hojas empiezan en lunes y terminan en domingo.
- **Clave temporal recomendada: la fecha de cierre (domingo) en ISO**, por ejemplo `2026-10-18`. Es la que usa Value CG
  en la columna A y no depende del texto de la hoja.
- Sufijos: `(Dos Semanas)` en `1008 - 2308`. Si algún día cruza fin de año (`2912 - 0401`), el año del lunes y del
  domingo difieren: hay que deducirlo con el orden de las hojas.

### 3.2 Cobertura

- 33 hojas → 34 semanas, del **23/02/2026 al 18/10/2026**. Cada hoja empieza el día siguiente al cierre de la anterior:
  **cero huecos, cero solapamientos**.
- **Hoja doble:** `1008 - 2308 (Dos Semanas)`, 14 días (10–23/08). Su ganancia (18.349,05) equivale a 9.174,52 por
  semana. No se puede partir en dos con los datos disponibles.
- **Semanas cortas (por feriados):** la hoja `Semanales` marca 23–29/03 y 30/03–05/04 como "Semana Corta", y
  `3003 - 0504` tiene la nota `C15 = "3 dias"`. Además caen feriados nacionales en las semanas de 27/04–03/05 (1/5),
  25–31/05 (25/5), 06–12/07 (9/7), 10–23/08 (17/8) y 12–18/10 (12/10). La planilla no registra días hábiles.
- **Antes del 01/03 sólo hay Value CG** (01/07/2025 y cierres del 01/02, 08/02, 15/02 y 22/02). Ojo: la "ganancia"
  del 01/02 (37.660,15) es la variación **desde julio de 2025**, no de una semana.
- **Período abierto:** octubre tiene 3 cierres (04/10, 11/10, 18/10); el mes no terminó. Value CG está cargado hasta el
  28/06.

### 3.3 A qué mes pertenece cada semana

Value CG agrupa los meses cerrados así: el cierre del 01/03 va a febrero, el del 05/04 y el del 03/05 van a abril y el
del 05/07 va a julio. **La regla que reproduce exactamente los cuatro meses cerrados (marzo a junio) es "el mes del
jueves de la semana"** (equivale a "el mes que tiene más días de la semana"). Con esa regla, la suma de ganancias de la
Calculadora da abril 52.366,61, igual que `Value CG!E26`, y mayo 29.747,29, igual que `E32`. Las filas de plantilla de
Value CG para meses futuros no respetan la regla (ponen el 02/08 en agosto y el 01/11 en noviembre): **recomiendo la
regla del jueves** y mostrar siempre cuántas semanas tiene cada mes (abril y julio tienen 5).

---

## 4. Claves y jerarquías

### 4.1 Claves

| Tabla | Clave | Observaciones |
|---|---|---|
| Hoja semanal | fecha de cierre (domingo) | El nombre de hoja no es único entre archivos (`1210 - 1810` está en a y en b) |
| Saldo por caja | (fecha de cierre, caja normalizada) | La caja se identifica **por encabezado**, no por letra (ver 4.3) |
| Value CG | fecha en col. A | Filtrar filas con fecha; deduplicar 01/03; descartar subtotales y filas "Dividendos"/"Aportes" |

### 4.2 Jerarquía caja → grupo → moneda → bloque → Neto

| Grupo | Cajas (encabezado) | Moneda real | Cómo entra al Neto en la Calculadora |
|---|---|---|---|
| Billete USD | CARA CHICA (en 4 hojas el encabezado es el número 1), CAMBIO, MALOS, USD | USD | "Dólares", 1:1 |
| Billete USD en Bs. As. | BSAS → USD BsAs | USD | Dentro de **"Pesos"**, dividido por la cotización (siempre 0 o sin fórmula de suma; ver §7) |
| Pesos | PESOS, TRANSFER, RECAUDACION BX, bx, DEUDA PESOS | ARS | "Pesos" = suma ÷ cotización (C8) |
| Cheques | CHEQUES | ARS | "Pesos" ÷ cotización |
| USDT / cripto | USDT, TRX | USDT | "Dólares", 1:1 (sin paridad USDT/billete) |
| USDT General (columna) | USDT General | USD | Fuera del cálculo; siempre 0,0021 (residuo idéntico en todas las hojas) |
| USD exterior | Grabrfy Manuel, LLC, PayPal Ruso, Grabify, GRABIFY Jose, CITY BANK, GRABIFI, WISE US, PAYONEER, Grabify BORRAR | USD | "Dólares", 1:1 |
| Euros | EUROS, WISE | EUR | "Euros" = (EUROS + WISE) × C9. **WISE se sumó como USD 1:1 hasta `1805 - 2405`** |
| Reales / libras | REALES, LIBRAS | BRL / GBP | **No entran** (LIBRAS siempre 0; REALES entre 4 y 1.114 BRL) |
| Garantías | MILLAMAPU, JEEP, GOL TREND, CHARCAS, PROMAR | varias | Fila 2 = +monto, fila 3 = −monto: **netean 0** siempre |
| Inversiones | POLIGONO, ALMAFUERTE, POLIGONO 20+13, columna `AH` sin encabezado | USD | Hasta `2007 - 2607` por los renglones "Poligono 09"/"Almafuerte"; desde `2707 - 0208`, **dentro de "Dólares"** |
| Egresos (flujo) | GASTOS, FIJOS, COMISIONES, INVERSION, INTERESES, DIVIDENDOS | USD | Se suman en "Dólares" y se restan en "Egresos": netean en el Neto, quedan en el Bruto |
| Ingresos (flujo) | ALQUILERES | USD | Renglón "Ingresos" (sólo `0106 - 0706` = 900 y `0806 - 1406` = 3.600) |
| Renglones fijos | "Deuda" (B, 5.000 → 4.000) y "USDT" (B, 10.760 → 41.536,49) | USD | Tipeados en la columna B del bloque |

Bloques: **Neto = Dólares + Pesos + Euros + (Poligono 09 + Almafuerte) + Deuda + USDT + Egresos (+ Ingresos)**.
**Bruto = lo mismo sin Egresos**. Por lo tanto **Bruto − Neto = −Egresos** en todas las hojas.

### 4.3 Columnas que cambian de lugar

| Encabezado | Letras por tramo de hojas |
|---|---|
| GASTOS | Z (2302–0203) · AA (0903–0604) · AB (1304–0405) · AC (1105–0106) · AD (0806–0607) · AE (1307–2007) · AI (2707–0308) · AJ (1008–1210) |
| INTERESES | AD · AE · AF · AG · AH · AL · AM (desde 2303) |
| DIVIDENDOS | AF · AG · AI · AJ ("Dividendos", minúscula) · AM · AN (desde 0405) |
| POLIGONO | AC (0806–0607) · AD (1307–2007) · AH (2707–0308) · AI (1008–1210) |
| ALMAFUERTE | AC (1307–2007) · AG (2707–1210) |
| Fila de sumas | fila 5 hasta `1805 - 2405`; fila 4 desde `2505 - 3105` (más fila 5 de monedas) |

---

## 5. Unidades, monedas y conversión a USD

| Moneda | Cómo la convierte la planilla | Observaciones |
|---|---|---|
| ARS | ÷ cotización de la hoja. Hasta `2303 - 2903` el divisor está dentro de la fórmula (`/1410`, `/1405`, `/1415`); desde `3003 - 0504`, en `C8` | Cargada a mano. Rango 1.380–1.540. Rachas repetidas: 1.405 (2 hojas), 1.380 (2), **1.490 (3)**, **1.525 (4 hojas = 5 semanas)**, 1.535 (2), 1.540 (2) |
| EUR | × 1,20 dentro de la fórmula hasta `1805 - 2405`; × `C9` = **1,25** desde `2505 - 3105` | Fijo, no sigue al mercado. El Registro General usa 1,23 (`config.json`) |
| USDT | 1:1 | La metodología del Registro valúa el USDT con la paridad observada (1,02–1,05) |
| BRL | No se convierte (queda afuera) | Máximo 1.114 BRL (`2007 - 2607`) ≈ 232 USD a 4,8 |
| GBP | — | Siempre 0 |
| PROMAR | Fila de moneda dice **USD**, pero los montos son 600.000.000 y 87.000.000 | Netea 0; si alguien suma garantías, el total explota |

**Exposición a la cotización al 18/10:** 180,15 millones de ARS = 117.359,83 USD (el 32,7 % del Neto). Una suba del 1 %
del dólar baja el Neto en ≈ 1.160 USD, el equivalente a una cuarta parte de una semana típica.

---

## 6. Serie semanal reconstruida

### 6.1 Método

1. Para cada hoja semanal (la del archivo b en `1210 - 1810`) leo las fórmulas del bloque A7:C29 por **etiqueta** de la
   columna A (Dolares, Pesos, Euros, Poligono 09, Almafuerte, Deuda, USDT, Egresos, Ingresos, Neto, Ganancia Neta, Bruto,
   Ganancia Bruta, Debe, Haber, Promedio, Volumen Prom, Operaciones).
2. Evalúo cada fórmula con un evaluador propio (SUM de rangos, + − × ÷, referencias a otras hojas). Las referencias
   rotas `'05/10 - 11/10'` se resuelven a `'0510 - 1110'`.
3. **Ganancia Neta homogénea** = Neto(hoja) − Neto(hoja anterior); **Ganancia Bruta homogénea** = Bruto(hoja) −
   Neto(hoja anterior). Es la definición que usan las fórmulas desde `2303 - 2903`.
4. Cotización = `C8` o el divisor escrito en la fórmula de Pesos; EUR = `C9` o el multiplicador de la fórmula de Euros.
5. Volumen = "Promedio" (Debe/Haber) hasta `1805 - 2405`; "Volumen Prom" desde `2505 - 3105`.

### 6.2 Verificación

- **33 de 33 hojas:** Neto, Bruto, Dólares, Pesos, Euros, Egresos y las ganancias guardadas coinciden con lo evaluado
  (diferencia < 0,005). Las únicas diferencias son los `#REF!` del archivo b, que evaluados dan **18.103,33** y
  **19.370,41**, los valores que espera el dueño.
- Cada Ganancia Neta guardada (desde `2303 - 2903`) apunta al Neto de la hoja inmediatamente anterior, así que la serie
  "telescopea": Σ ganancias (08/03 → 18/10) = **191.162,38** = Neto 18/10 (359.107,17) − Neto 01/03 (167.944,79).
- Las primeras hojas definían la ganancia distinto: `0903 - 1503!B14` "Ganancia" = Bruto − Neto anterior (9.633,75,
  es una ganancia bruta); `1603 - 2203!B17` = Bruto − **Bruto** anterior (−5.353,06). `2302 - 0103` y `0203 - 0803` no
  tienen renglón de ganancia. En la tabla uso la definición homogénea.
- La descomposición por grupo (§6.4) suma exactamente el Neto en las 33 hojas.

### 6.3 Tabla principal

"Ganancia Neta" y "Ganancia Bruta" en versión homogénea. "Egresos" con el signo de la planilla. (b) = archivo corregido.
Mes = regla del jueves.

| # | Hoja | Cierre (domingo) | Días | Mes | Cot. ARS | EUR→USD | Neto | Ganancia Neta | Bruto | Ganancia Bruta | Egresos | Volumen | Oper. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `2302 - 0103` | 01/03 | 7 | feb | 1.410 | 1,20 | 167.944,79 | — | 169.125,16 | — | -1.180,37 | 585.360,00 | — |
| 2 | `0203 - 0803` | 08/03 | 7 | mar | 1.405 | — | 167.540,87 | -403,92 | 173.377,25 | 5.432,46 | -5.836,38 | 411.000,00 | — |
| 3 | `0903 - 1503` | 15/03 | 7 | mar | 1.405 | — | 175.934,47 | 8.393,60 | 177.174,62 | 9.633,75 | -1.240,15 | 474.077,34 | — |
| 4 | `1603 - 2203` | 22/03 | 7 | mar | 1.415 | 1,20 | 171.509,70 | -4.424,77 | 171.821,56 | -4.112,91 | -311,86 | 483.084,95 | — |
| 5 | `2303 - 2903` | 29/03 | 7 | mar | 1.405 | 1,20 | 180.926,63 | 9.416,93 | 185.816,93 | 14.307,23 | -4.890,30 | 402.058,00 | — |
| 6 | `3003 - 0504` | 05/04 | 7 | abr | 1.390 | 1,20 | 185.123,28 | 4.196,66 | 185.449,41 | 4.522,78 | -326,12 | 330.226,94 | — |
| 7 | `0604 - 1204` | 12/04 | 7 | abr | 1.380 | 1,20 | 194.374,09 | 9.250,81 | 195.077,82 | 9.954,53 | -703,72 | 629.499,50 | — |
| 8 | `1304 - 1904` | 19/04 | 7 | abr | 1.385 | 1,20 | 209.276,60 | 14.902,51 | 214.807,60 | 20.433,51 | -5.530,99 | 471.329,00 | — |
| 9 | `2004 - 2604` | 26/04 | 7 | abr | 1.400 | 1,20 | 227.740,30 | 18.463,70 | 231.706,84 | 22.430,24 | -3.966,54 | 477.010,33 | — |
| 10 | `2704 - 0305` | 03/05 | 7 | abr | 1.380 | 1,20 | 233.293,24 | 5.552,94 | 241.549,53 | 13.809,23 | -8.256,29 | 499.476,13 | — |
| 11 | `0405 - 1005` | 10/05 | 7 | may | 1.380 | 1,20 | 238.448,79 | 5.155,55 | 250.731,19 | 17.437,95 | -12.282,40 | 499.476,13 | — |
| 12 | `1105 - 1705` | 17/05 | 7 | may | 1.395 | 1,20 | 247.280,96 | 8.832,17 | 248.885,47 | 10.436,68 | -1.604,51 | 612.170,34 | — |
| 13 | `1805 - 2405` | 24/05 | 7 | may | 1.405 | 1,20 | 252.329,06 | 5.048,10 | 254.772,86 | 7.491,90 | -2.443,80 | 605.155,10 | — |
| 14 | `2505 - 3105` | 31/05 | 7 | may | 1.410 | 1,25 | 258.321,53 | 5.992,47 | 260.361,93 | 8.032,87 | -2.040,40 | 474.625,30 | — |
| 15 | `0106 - 0706` | 07/06 | 7 | jun | 1.415 | 1,25 | 253.500,93 | -4.820,60 | 266.998,90 | 8.677,37 | -13.497,97 | 482.190,71 | — |
| 16 | `0806 - 1406` | 14/06 | 7 | jun | 1.440 | 1,25 | 261.617,18 | 8.116,25 | 264.261,59 | 10.760,66 | -2.644,41 | 619.283,35 | — |
| 17 | `1506 - 2106` | 21/06 | 7 | jun | 1.455 | 1,25 | 266.647,58 | 5.030,40 | 267.989,90 | 6.372,72 | -1.342,32 | 317.990,38 | — |
| 18 | `2206 - 2806` | 28/06 | 7 | jun | 1.490 | 1,25 | 265.889,35 | -758,22 | 267.898,20 | 1.250,63 | -2.008,85 | 311.721,47 | — |
| 19 | `2906 - 0507` | 05/07 | 7 | jul | 1.490 | 1,25 | 277.290,61 | 11.401,26 | 279.846,01 | 13.956,66 | -2.555,40 | 463.877,70 | 348 |
| 20 | `0607 - 1207` | 12/07 | 7 | jul | 1.490 | 1,25 | 275.747,88 | -1.542,73 | 282.549,53 | 5.258,92 | -6.801,65 | 282.271,73 | 348 |
| 21 | `1307 - 1907` | 19/07 | 7 | jul | 1.510 | 1,25 | 283.105,99 | 7.358,11 | 284.023,57 | 8.275,69 | -917,58 | 757.589,27 | 407 |
| 22 | `2007 - 2607` | 26/07 | 7 | jul | 1.525 | 1,25 | 284.975,04 | 1.869,05 | 289.309,46 | 6.203,47 | -4.334,42 | 407.583,56 | 338 |
| 23 | `2707 - 0208` | 02/08 | 7 | jul | 1.525 | 1,25 | 286.441,91 | 1.466,87 | 286.735,12 | 1.760,08 | -293,21 | 542.763,18 | 338 |
| 24 | `0308 - 0908` | 09/08 | 7 | ago | 1.525 | 1,25 | 283.874,04 | -2.567,87 | 291.478,93 | 5.037,02 | -7.604,89 | 433.691,81 | 338 |
| 25 | `1008 - 2308 (Dos Semanas)` | 23/08 | 14 | ago | 1.525 | 1,25 | 302.223,09 | 18.349,05 | 307.685,69 | 23.811,65 | -5.462,60 | 601.347,60 | 338 |
| 26 | `2408 - 3008` | 30/08 | 7 | ago | 1.535 | 1,25 | 345.163,56 | 42.940,48 | 345.315,64 | 43.092,56 | -152,08 | 332.183,67 | 338 |
| 27 | `3108 - 0609` | 06/09 | 7 | sep | 1.530 | 1,25 | 340.096,35 | -5.067,21 | 349.128,51 | 3.964,95 | -9.032,16 | 519.500,43 | 338 |
| 28 | `0709 - 1309` | 13/09 | 7 | sep | 1.525 | 1,25 | 343.953,91 | 3.857,56 | 344.247,26 | 4.150,91 | -293,35 | 628.106,46 | 338 |
| 29 | `1409 - 2009` | 20/09 | 7 | sep | 1.535 | 1,25 | 343.677,71 | -276,20 | 345.155,68 | 1.201,77 | -1.477,97 | 295.339,22 | 338 |
| 30 | `2109 - 2709` | 27/09 | 7 | sep | 1.535 | 1,25 | 345.606,17 | 1.928,46 | 346.081,09 | 2.403,38 | -474,92 | 270.828,03 | 338 |
| 31 | `2809 - 0410` | 04/10 | 7 | oct | 1.540 | 1,25 | 344.887,54 | -718,63 | 348.558,61 | 2.952,44 | -3.671,07 | 299.362,39 | 338 |
| 32 | `0510 - 1110` | 11/10 | 7 | oct | 1.540 | 1,25 | 341.003,84 | -3.883,70 | 349.270,08 | 4.382,54 | -8.266,24 | 495.279,46 | 338 |
| 33 | `1210 - 1810` (b) | 18/10 | 7 | oct | 1.535 | 1,25 | 359.107,17 | 18.103,33 | 360.374,25 | 19.370,41 | -1.267,08 | 394.062,95 | 338 |

Notas por fila:
- **#1:** Value CG tiene 167.896,05 para el 01/03 (−48,74; ver problema 23).
- **#2 y #3:** EUROS no entra al cálculo (200 y −500 EUR); no hay renglón Euros.
- **#4:** salieron 22.672 (6.450 de dividendos + 16.222 de una liquidación a un ex aportante). Antes de eso la ganancia
  fue 18.247,23.
- **#8:** el renglón USDT sube 10.900 (10.760 → 21.660; nota `C11 = "(+$10,900)"`).
- **#10 y #11:** el volumen es el mismo número (499.476,13); Debe/Haber copiados.
- **#11:** incluye 4.719 de dividendos pagados (columna DIVIDENDOS).
- **#12:** "Deuda" baja 5.000 → 4.000 (−1.000 en la ganancia).
- **#14:** USDT +4.021; euro 1,20 → 1,25 y WISE pasa de USD 1:1 a EUR × 1,25 (+1.265,67 sólo por revaluar).
- **#15:** incluye 2.510 de dividendos.
- **#16:** "Ingresos" 3.600 con nota "NO CONTAR" en `C14`; Polígono entra por primera vez (7.412,22).
- **#23:** INTERESES 2.317,44 sin fórmula de suma (Bruto subestimado).
- **#25:** dos semanas; cheques pendientes −27,175 M → +0,825 M ARS (+18.361 USD); sale Almafuerte (−50.000) y entra
  Polígono 20+13 (+75.466).
- **#26:** outlier (§8).
- **#32:** la columna `AH` sin encabezado sube 75.466 → 112.966 (+37.500, financiado con caja).
- **#33:** incluye +15.855,49 del ajuste retroactivo de USDT General (mayo–septiembre).

### 6.4 Composición del Neto (USD)

"Caja" y "Pendientes" = filas 2 y 3 de todas las cajas líquidas convertidas (billete, pesos, cheques, USDT, exterior,
euros). "Inversiones" = POLIGONO + ALMAFUERTE + POLIGONO 20+13 + `AH`. "Renglones fijos" = Deuda + USDT. Las columnas de
egresos y las garantías netean 0. Efecto cotización = ARS de la semana anterior × (1/cot actual − 1/cot anterior).

| Hoja | Caja (fila 2) | Pendientes (fila 3) | Inversiones | Renglones fijos | Neto | % inversiones | Efecto cotización ARS |
|---|---|---|---|---|---|---|---|
| `2302 - 0103` | 275.855 | -123.670 | 0 | 15.760 | 167.945 | 0,0 % | — |
| `0203 - 0803` | 428.714 | -276.934 | 0 | 15.760 | 167.541 | 0,0 % | 417 |
| `0903 - 1503` | 266.225 | -106.051 | 0 | 15.760 | 175.934 | 0,0 % | 0 |
| `1603 - 2203` | 332.824 | -177.074 | 0 | 15.760 | 171.510 | 0,0 % | -1.215 |
| `2303 - 2903` | 395.024 | -229.858 | 0 | 15.760 | 180.927 | 0,0 % | 1.285 |
| `3003 - 0504` | 327.330 | -157.966 | 0 | 15.760 | 185.123 | 0,0 % | 1.901 |
| `0604 - 1204` | 417.557 | -238.943 | 0 | 15.760 | 194.374 | 0,0 % | 1.695 |
| `1304 - 1904` | 489.550 | -306.934 | 0 | 26.660 | 209.277 | 0,0 % | -1.041 |
| `2004 - 2604` | 543.069 | -341.988 | 0 | 26.660 | 227.740 | 0,0 % | -1.985 |
| `2704 - 0305` | 372.683 | -166.050 | 0 | 26.660 | 233.293 | 0,0 % | 3.122 |
| `0405 - 1005` | 607.680 | -395.891 | 0 | 26.660 | 238.449 | 0,0 % | 0 |
| `1105 - 1705` | 428.444 | -206.823 | 0 | 25.660 | 247.281 | 0,0 % | -2.754 |
| `1805 - 2405` | 394.094 | -167.425 | 0 | 25.660 | 252.329 | 0,0 % | -2.191 |
| `2505 - 3105` | 457.990 | -229.349 | 0 | 29.681 | 258.322 | 0,0 % | -673 |
| `0106 - 0706` | 546.191 | -322.371 | 0 | 29.681 | 253.501 | 0,0 % | -601 |
| `0806 - 1406` | 247.975 | -23.451 | 7.412 | 29.681 | 261.617 | 2,8 % | -3.285 |
| `1506 - 2106` | 144.281 | 25.078 | 67.607 | 29.681 | 266.648 | 25,4 % | -893 |
| `2206 - 2806` | 149.143 | 19.458 | 67.607 | 29.681 | 265.889 | 25,4 % | -2.688 |
| `2906 - 0507` | 164.746 | 15.256 | 67.607 | 29.681 | 277.291 | 24,4 % | 0 |
| `0607 - 1207` | 230.612 | -52.152 | 67.607 | 29.681 | 275.748 | 24,5 % | 0 |
| `1307 - 1907` | 172.878 | -37.061 | 117.607 | 29.681 | 283.106 | 41,5 % | -1.687 |
| `2007 - 2607` | 223.149 | -87.741 | 119.886 | 29.681 | 284.975 | 42,1 % | -1.173 |
| `2707 - 0208` | 132.639 | 4.236 | 119.886 | 29.681 | 286.442 | 41,9 % | 0 |
| `0308 - 0908` | 118.278 | 16.030 | 119.886 | 29.681 | 283.874 | 42,2 % | 0 |
| `1008 - 2308` | 123.486 | 3.704 | 145.352 | 29.681 | 302.223 | 48,1 % | 0 |
| `2408 - 3008` | 110.344 | 59.787 | 145.352 | 29.681 | 345.164 | 42,1 % | -556 |
| `3108 - 0609` | 119.095 | 45.969 | 145.352 | 29.681 | 340.096 | 42,7 % | 257 |
| `0709 - 1309` | 239.532 | -70.611 | 145.352 | 29.681 | 343.954 | 42,3 % | 267 |
| `1409 - 2009` | 203.432 | -35.467 | 146.032 | 29.681 | 343.678 | 42,5 % | -579 |
| `2109 - 2709` | 198.521 | -28.628 | 146.032 | 29.681 | 345.606 | 42,3 % | 0 |
| `2809 - 0410` | 236.586 | -67.411 | 146.032 | 29.681 | 344.888 | 42,3 % | -183 |
| `0510 - 1110` | 202.197 | -74.406 | 183.532 | 29.681 | 341.004 | 53,8 % | 0 |
| `1210 - 1810` | 138.001 | -7.962 | 183.532 | 45.536 | 359.107 | 51,1 % | 241 |

Lectura: entre junio y octubre el patrimonio pasó de ser casi todo caja a tener **más de la mitad inmovilizada en
proyectos valuados al costo y cargados a mano**. Las subas del Neto en esas semanas (Polígono +60.195 el 21/06,
Almafuerte +50.000 el 19/07, `AH` +37.500 el 11/10) no son ganancia: se financiaron con caja (la caja cae lo mismo).

### 6.5 Ganancia comparable

**Ganancia comparable = Ganancia Neta + distribuciones a socios o aportantes de esa semana − ajustes retroactivos**,
dividida por el número de semanas de la hoja. Es lo que hace Value CG (sumarle de vuelta los dividendos) y lo que pide
separar el dueño (el ajuste de USDT General).

| Hoja | Ganancia Neta | + distribuciones | − ajuste USDT | Comparable | Por semana | Efecto cotización | GN / volumen |
|---|---|---|---|---|---|---|---|
| `0203 - 0803` | -403,92 | — | — | -403,92 | -403,92 | 417 | -0,10 % |
| `0903 - 1503` | 8.393,60 | — | — | 8.393,60 | 8.393,60 | 0 | 1,77 % |
| `1603 - 2203` | -4.424,77 | 22.672,00 | — | 18.247,23 | 18.247,23 | -1.215 | -0,92 % |
| `2303 - 2903` | 9.416,93 | — | — | 9.416,93 | 9.416,93 | 1.285 | 2,34 % |
| `3003 - 0504` | 4.196,66 | — | — | 4.196,66 | 4.196,66 | 1.901 | 1,27 % |
| `0604 - 1204` | 9.250,81 | — | — | 9.250,81 | 9.250,81 | 1.695 | 1,47 % |
| `1304 - 1904` | 14.902,51 | — | — | 14.902,51 | 14.902,51 | -1.041 | 3,16 % |
| `2004 - 2604` | 18.463,70 | — | — | 18.463,70 | 18.463,70 | -1.985 | 3,87 % |
| `2704 - 0305` | 5.552,94 | — | — | 5.552,94 | 5.552,94 | 3.122 | 1,11 % |
| `0405 - 1005` | 5.155,55 | 4.719,00 | — | 9.874,55 | 9.874,55 | 0 | 1,03 % |
| `1105 - 1705` | 8.832,17 | — | — | 8.832,17 | 8.832,17 | -2.754 | 1,44 % |
| `1805 - 2405` | 5.048,10 | — | — | 5.048,10 | 5.048,10 | -2.191 | 0,83 % |
| `2505 - 3105` | 5.992,47 | — | — | 5.992,47 | 5.992,47 | -673 | 1,26 % |
| `0106 - 0706` | -4.820,60 | 2.510,00 | — | -2.310,60 | -2.310,60 | -601 | -1,00 % |
| `0806 - 1406` | 8.116,25 | — | — | 8.116,25 | 8.116,25 | -3.285 | 1,31 % |
| `1506 - 2106` | 5.030,40 | — | — | 5.030,40 | 5.030,40 | -893 | 1,58 % |
| `2206 - 2806` | -758,22 | — | — | -758,22 | -758,22 | -2.688 | -0,24 % |
| `2906 - 0507` | 11.401,26 | — | — | 11.401,26 | 11.401,26 | 0 | 2,46 % |
| `0607 - 1207` | -1.542,73 | — | — | -1.542,73 | -1.542,73 | 0 | -0,55 % |
| `1307 - 1907` | 7.358,11 | — | — | 7.358,11 | 7.358,11 | -1.687 | 0,97 % |
| `2007 - 2607` | 1.869,05 | — | — | 1.869,05 | 1.869,05 | -1.173 | 0,46 % |
| `2707 - 0208` | 1.466,87 | — | — | 1.466,87 | 1.466,87 | 0 | 0,27 % |
| `0308 - 0908` | -2.567,87 | — | — | -2.567,87 | -2.567,87 | 0 | -0,59 % |
| `1008 - 2308` | 18.349,05 | — | — | 18.349,05 | 9.174,52 | 0 | 3,05 % |
| `2408 - 3008` | 42.940,48 | — | — | 42.940,48 | 42.940,48 | -556 | 12,93 % |
| `3108 - 0609` | -5.067,21 | — | — | -5.067,21 | -5.067,21 | 257 | -0,98 % |
| `0709 - 1309` | 3.857,56 | — | — | 3.857,56 | 3.857,56 | 267 | 0,61 % |
| `1409 - 2009` | -276,20 | — | — | -276,20 | -276,20 | -579 | -0,09 % |
| `2109 - 2709` | 1.928,46 | — | — | 1.928,46 | 1.928,46 | 0 | 0,71 % |
| `2809 - 0410` | -718,63 | — | — | -718,63 | -718,63 | -183 | -0,24 % |
| `0510 - 1110` | -3.883,70 | — | — | -3.883,70 | -3.883,70 | 0 | -0,78 % |
| `1210 - 1810` | 18.103,33 | — | 15.855,49 | 2.247,83 | 2.247,83 | 241 | 4,59 % |

Estadísticos de la ganancia comparable por semana (32 hojas): **mediana 5.039**, media 6.126, desvío robusto (MAD ×
1,4826) 6.367; **9 semanas negativas** (08/03, 07/06, 28/06, 12/07, 09/08, 06/09, 20/09, 04/10, 11/10).

**Puente del Neto, 01/03 → 18/10:**

| Concepto | USD |
|---|---|
| Neto al 01/03 | 167.944,79 |
| + Ganancia de las semanas "normales" (todas menos 24–30/08, sin el ajuste USDT y sin restar distribuciones) | 162.267,41 |
| + Semana 24–30/08 (sin explicar) | 42.940,48 |
| + Ajuste retroactivo USDT General (mayo–septiembre, cargado el 18/10) | 15.855,49 |
| − Distribuciones registradas (22/03, 10/05 y 07/06) | −29.901,00 |
| **= Neto al 18/10** | **359.107,17** |

Dentro de esas ganancias está el efecto cotización de todo el período, estimado en ≈ −12.318 (−11.762 sin la semana
del 30/08).

### 6.6 Agregado mensual (regla del jueves)

| Mes | Hojas | Semanas | Ganancia Neta | Ganancia comparable | Ganancia Bruta | Egresos | Efecto cotización | Volumen (suma) |
|---|---|---|---|---|---|---|---|---|
| mar | 4 (0203…2303) | 4 | 12.981,84 | 35.653,84 | 25.260,53 | -12.278,69 | 487 | 1.770.220 |
| abr | 5 (3003…2704) | 5 | 52.366,61 | 52.366,61 | 71.150,28 | -18.783,67 | 3.691 | 2.407.542 |
| may | 4 (0405…2505) | 4 | 25.028,29 | 29.747,29 | 43.399,40 | -18.371,11 | -5.618 | 2.191.427 |
| jun | 4 (0106…2206) | 4 | 7.567,83 | 10.077,83 | 27.061,38 | -19.493,55 | -7.467 | 1.731.186 |
| jul | 5 (2906…2707) | 5 | 20.552,55 | 20.552,55 | 35.454,81 | -14.902,26 | -2.860 | 2.454.085 |
| ago | 3 (0308…2408) | 4 | 58.721,65 | 58.721,65 | 71.941,22 | -13.219,57 | -556 | 1.367.223 |
| sep | 4 (3108…2109) | 4 | 442,61 | 442,61 | 11.721,01 | -11.278,40 | -54 | 1.713.774 |
| oct (incompleto) | 3 (2809…1210) | 3 | 13.501,00 | -2.354,49 | 26.705,39 | -13.204,39 | 58 | 1.188.705 |

Control contra Value CG: marzo comparable 35.653,84 = `F20` (35.702,58) − 48,74; marzo neto 12.981,84 = `E20`
(13.030,58) − 48,74; abril = `E26` 52.366,61; mayo = `E32` 29.747,29; junio = `E38` 10.077,82 (diferencia 0,01).
Agosto incluye la semana outlier (sin ella: 15.781,17). El volumen de agosto suma la hoja doble una sola vez.

### 6.7 Historia anterior al 01/03 (sólo Value CG)

| Fecha | Capital (B) | Ganancia (E) | Observación |
|---|---|---|---|
| 01/07/2025 | 91.560,18 | 28.122,00 | Ganancia contra aportes de 63.438; después se restan dividendos (−5.456) → 86.104,18 |
| 01/02/2026 | 123.764,33 | 37.660,15 | **Variación desde jul-2025**, no semanal; fórmula tipeada `=116962.09-117.35-4846.95+W7+5300-4294` |
| 08/02 | 147.322,77 | 23.558,44 | `=135556.23+W8+5300-4294` |
| 15/02 | 156.684,69 | 9.361,92 | `Semanales` tiene 156.614,22 (−70,47) |
| 22/02 | 158.704,35 | 2.019,66 | |
| 01/03 | 167.896,05 | 9.191,70 | La Calculadora dice 167.944,79 |

---

## 7. Problemas de calidad (con evidencia)

Severidad: **Alta** = cambia una cifra que el dashboard mostraría o rompe la lectura automática; **Media** = distorsiona
una comparación; **Baja** = hoy no cambia nada, pero puede hacerlo.

### A. Estructura y lectura

| # | Problema | Evidencia | Impacto | Sev. |
|---|---|---|---|---|
| 1 | Las columnas cambian de letra entre hojas | GASTOS en 8 letras; INTERESES en 7; POLIGONO en 4 (tabla 4.3) | Leer por letra mezcla cajas | Alta |
| 2 | Columna con saldo y **sin encabezado** | `AH` de `2408 - 3008` a `2809 - 0410` = 75.466; `0510 - 1110` y `1210 - 1810` = 112.966 (en `1008 - 2308` se llamaba "POLIGONO 20+13") | 31 % del Neto actual sin nombre | Alta |
| 3 | Encabezado reemplazado por un número | `A1` = 1 en `0903 - 1503`, `1603 - 2203`, `2303 - 2903`, `3003 - 0504` (es CARA CHICA) | Lectura por nombre pierde la caja | Media |
| 4 | La fila de sumas cambia de lugar | Fila 5 hasta `1805 - 2405`; fila 4 + fila 5 de monedas desde `2505 - 3105` | Leer siempre la fila 4 da texto o vacío en las viejas | Media |
| 5 | Etiquetas del bloque que apuntan a otra columna | Desde `2707 - 0208`: "Poligono 09" `B10 = AD4` (GOL TREND) y "Almafuerte" `B11 = AC4` (JEEP). En `2408 - 3008` ambas están vacías | Hoy 0; las inversiones reales entran en "Dólares" (POLIGONO en `AH`/`AI`, ALMAFUERTE en `AG`) | Media |
| 6 | Rangos desalineados después de insertar columnas | `1307 - 1907` y `2007 - 2607`: Egresos `=-SUM(AE4:AH4,AI4)` incluye ALQUILERES (`AI`) y además "Ingresos" `=-AI4`; DIVIDENDOS (`AJ`) no entra en ninguna fórmula | Hoy 0; doble conteo latente | Baja |
| 7 | Valores con saldo y sin fórmula de suma (no computan) | `2707 - 0208!AL2` INTERESES = 2.317,44 sin `AL4`; `2303 - 2903!G3` = 1.000 y `2704 - 0305!G3` = 3.000 (BSAS, sin `G5`); MILLAMAPU `1105 - 1705` a `0106 - 0706` | Bruto y Egresos de `2707 - 0208` subestimados en 2.317,44; 1.000 y 3.000 de BsAs fuera del Neto (si son USD, el Neto de esas semanas está bajo en esos montos) | Media |
| 8 | Residuos de punto flotante | `T2` = −2,7·10⁻¹²; `W2` = −2,3·10⁻¹³; `N2` = 0,0021433691 idéntico en todas las hojas | Cajas "con saldo" que son 0 | Baja |

### B. Monedas y valuación

| # | Problema | Evidencia | Impacto | Sev. |
|---|---|---|---|---|
| 9 | Cotización ARS manual y repetida | 1.490 en 3 hojas (22/06–12/07); 1.525 en 4 hojas (20/07–23/08 = 5 semanas); otras 4 rachas de 2 | Con 180 M ARS, cada 1 % de error en la cotización mueve ≈ 1.160 USD | Alta |
| 10 | Euro fijo y cambio de criterio en WISE | ×1,20 hasta `1805 - 2405`; `C9` = 1,25 desde `2505 - 3105`; WISE contado como USD 1:1 hasta `1805 - 2405` y como EUR × 1,25 después | +1.265,67 en la ganancia del 31/05 sólo por revaluar (414 de EUROS + 851,67 de WISE) | Media |
| 11 | Cajas que no entran al cálculo | REALES nunca (máx. 1.114 BRL en `2007 - 2607`); EUROS en `0203 - 0803` (200) y `0903 - 1503` (−500) | < 600 USD | Baja |
| 12 | USD dentro del bloque Pesos | `B8 = SUM(E4:J4,M4)/C8` incluye G (USD BsAs, USD), H (DEUDA USD) e I (DEUDA PESOS, moneda "USD") | Hoy 0; un USD en G valdría 1/1.535 | Baja |
| 13 | Unidades imposibles en garantías | PROMAR 600.000.000 / −600.000.000 (`2707 - 0208` a `3108 - 0609`) y 87.000.000 (desde `0709 - 1309`) con moneda "USD" | Netea 0; sumar garantías da cifras absurdas | Media |
| 14 | USDT a 1:1 | Columnas USDT y TRX entran como USD | Distinto del Registro General (paridad 1,02–1,05) | Baja |
| 15 | Inversiones al costo y tipeadas | POLIGONO 7.412,22 → 67.607,33 → 69.885,57 → 70.565,57; `AH` 75.466 → 112.966 | 51 % del Neto sin valuación de mercado | Alta |

### C. Valores constantes o copiados

| # | Problema | Evidencia | Impacto | Sev. |
|---|---|---|---|---|
| 16 | Operaciones fijas | `B22` = 338 en las 13 hojas de `2007 - 2607` a `1210 - 1810`; 348 en `2906 - 0507` y `0607 - 1207`; 407 en `1307 - 1907`; vacío antes | Promedio por operación inservible | Alta |
| 17 | Volumen copiado o mal calculado | Debe 479.840,65 / Haber 474.180 idénticos en `2004 - 2604`, `2704 - 0305`, `0405 - 1005`, `1105 - 1705`; Promedio 499.476,13 en `2704 - 0305` y `0405 - 1005`, que **no es** (Debe+Haber)/2 = 477.010,33; Debe/Haber vacíos en `1805 - 2405`; Value CG usa 686.863,60 para el 10/05 | % sobre volumen de esas semanas no confiable | Media |
| 18 | Cambio de definición del volumen | Hasta `1805 - 2405`: Debe, Haber, Promedio. Desde `2505 - 3105`: "Volumen Prom" pegado como valor con 11 decimales | Serie no homogénea | Media |
| 19 | Renglones fijos tipeados que mueven la ganancia | Deuda 5.000 → 4.000 en `1105 - 1705`, con nota "restar aca" (`C10`, de `2004 - 2604` a `1805 - 2405`) aunque se suma; USDT 10.760 → 21.660 (`1304 - 1904`), → 25.681 (`2505 - 3105`), → 41.536,49 (`1210 - 1810`) | Los saltos (−1.000, +10.900, +4.021, +15.855,49) entran en la ganancia de esa semana | Alta |
| 20 | Saldo congelado | TRX = 1.734 en 26 hojas seguidas (`1304 - 1904` a `1210 - 1810`) | Caja sin movimiento real o sin actualizar | Baja |

### D. Hechos que distorsionan la ganancia semanal

| # | Problema | Evidencia | Impacto | Sev. |
|---|---|---|---|---|
| 21 | Distribuciones tratadas como pérdida | `1603 - 2203`: 6.450 + 16.222 fuera del Neto (`B13`, `B14`); `0405 - 1005!AF5` DIVIDENDOS = 4.719 (formato viejo, sumas en fila 5); `0106 - 0706!AG4` = 2.510 | Ganancias semanales subestimadas en esos montos | Alta |
| 22 | Dividendos que no aparecen | Value CG resta 924,16 después de junio (`B39`); Tenencia calcula 10 % mensual; desde `2906 - 0507` la columna DIVIDENDOS está en 0 | Si se pagaron, están escondidos en la caída de caja | Media |
| 23 | Ajuste retroactivo en una sola semana | `1210 - 1810 (b)!B13` suma 6 liquidaciones de USDT General × 2/3 (`I15:J19`, `I21`) = 15.855,49 | Ganancia del 18/10: 18.103,33, de la cual operativa 2.247,83 | Alta |
| 24 | Semana sin explicación | `2408 - 3008`: USD fila 3 −45.347 → +14.119 (+59.466); caja USD 84.000 → 64.100 (−19.900); pendientes totales +56.083 | +42.940,48, 8,5 veces la mediana | Alta |
| 25 | Saltos en la hoja doble | `1008 - 2308`: CHEQUES fila 3 −27.175.000 → +825.000 ARS (+18.361 USD); ALMAFUERTE 50.000 → 0; POLIGONO 20+13 +75.466 | 18.349,05 en 2 semanas, en buena parte por pendientes | Media |
| 26 | Efecto cotización mezclado con el resultado | `0806 - 1406` −3.285; `2206 - 2806` −2.688 (explica casi toda la pérdida de −758); junio −7.467 | Semanas "malas" que son revaluación | Media |
| 27 | Costos mensuales concentrados | Un único pago de GASTOS de 5.500 a 9.000 por mes, casi siempre en la primera o segunda semana: 5.694 (08/03), 5.531 (19/04), 6.872 (10/05), 7.966 (07/06), 5.828 (12/07), 7.447 (09/08), 8.972 (06/09), 8.111 (11/10). El resto de las semanas, GASTOS queda entre 84 y 1.916 | Esa semana del mes siempre se ve peor | Media |

### E. Duplicados e inconsistencias entre archivos

| # | Problema | Evidencia | Impacto | Sev. |
|---|---|---|---|---|
| 28 | Hoja duplicada en dos archivos | `1210 - 1810` en a y b; filas 1–5 iguales; difieren `B13` y notas; b tiene 6 `#REF!` | Si se lee la de a, el Neto es 343.251,68 (−15.855,49) | Alta |
| 29 | Neto de la Calculadora ≠ Capital de Value CG | 01/03: 167.896,05 vs 167.944,79 (−48,74); 22/03: 194.181,70 vs 171.509,70 (+22.672, antes de la distribución; la fila "Balance Actual" vuelve a 171.509,70). Ganancia: +4.719 (10/05) y +2.510 (07/06). Volumen 10/05: 686.863,60 vs 499.476,13. Fuera de eso, el capital coincide al centavo del 08/03 al 28/06 y la ganancia del 08/03 difiere en los mismos 48,74 de la base | Dos fuentes de "ganancia" con definiciones distintas | Media |
| 30 | Definición de "ganancia mensual" distinta según el mes en Value CG | Marzo `E20 = SUM(E15:E19)-S19` (descuenta las distribuciones); abril `E26 = SUM(E21:E25)` (no las descuenta); `RENTA` usa `H/I` en filas 14–15 y `E/I` desde la 16 | Meses no comparables | Media |
| 31 | Fecha duplicada y filas de texto intercaladas | Value CG 2026-03-01 en filas 11 y 14; filas "Febrero", "Dividendos", "Aportes", "Balance Actual" | Hay que filtrar y deduplicar | Media |
| 32 | Copias viejas con otros valores | `Semanales`: 14/06 = 254.204,96 (la Calculadora dice 261.617,18; faltan los 7.412,22 de Polígono); 15/02 = 156.614,22 (Value CG 156.684,69) | No usar `Semanales` como fuente | Media |
| 33 | Dashboard viejo con referencias erróneas | "Capital actual" = `'Value CG'!B36` (21/06, no 28/06); "máxima ganancia semanal" 37.660,15 es la variación jul-2025 → feb-2026; los promedios semanales incluyen `E5` y `E7` (multimes) | Cifras de referencia equivocadas | Baja |
| 34 | Dependencias frágiles en Tenencia | `G7 = 'Value 2026'!B11` (hoja oculta); 3 × 28,13 % + 15,62 % = 100,01 %; encabezado "15,63 %" | Reparte 0,01 % de más | Baja |
| 35 | Restos copiados en el bloque | `2303 - 2903` conserva "Dividendos 6.450" / "Liquidacion 16.222" y "Sin contar liquidacion" de la hoja anterior (fuera del Neto) | Confunde a quien lee la hoja | Baja |
| 36 | Notas sin resolver | `0806 - 1406`: `C14` "NO CONTAR" junto a Ingresos 3.600, `C18` "REVISAR" y `D18` −3.600; `0405 - 1005!C16` = −18.042; `2206 - 2806!C18` = 4.576,60 junto a la Ganancia Bruta 1.250,63; "UNIFICAR TODO EN UNA TABLA…" en `K18`/`K19` de 16 hojas | Decisiones pendientes del dueño | Baja |
| 37 | Definiciones distintas en las primeras hojas | `0903 - 1503!B14` = Bruto − Neto anterior; `1603 - 2203!B17` = Bruto − Bruto anterior; sin ganancia en las dos primeras | No tomar la ganancia guardada: recalcular | Media |

---

## 8. Outliers y semanas que hay que explicar

Criterio: desvío robusto = (x − mediana) / (1,4826 × MAD) sobre la ganancia comparable por semana (mediana 5.039,25;
1,4826 × MAD = 6.367,20). **Outlier = más de 2,5.** Sólo una semana lo supera; abajo agrego las que pasan de 2 o que
sin ajustar parecerían anómalas.

| Semana | Ganancia | Desvío robusto | Explicación disponible |
|---|---|---|---|
| **24–30/08** | **+42.940,48** | **5,95** | Ninguna en la planilla. Mecánicamente: pendientes en USD +59.466, USDT pendientes +7.669, caja USD −19.900. Le sigue una semana de −5.067,21 |
| 18/10 (sin ajustar) | +18.103,33 | 2,05 | Ajuste USDT retroactivo (+15.855,49); sin él, +2.247,83 |
| 22/03 (sin ajustar) | −4.424,77 | — | Distribución de 22.672; comparable +18.247,23 (z = 2,07) |
| 26/04 | +18.463,70 | 2,11 | Sin nota; semana con volumen normal (477.010) |
| 10–23/08 | +18.349,05 | — | Dos semanas (9.174,52 por semana); cheques pendientes +18.361 |

Ninguna semana está abajo del umbral; la peor (06/09, −5.067,21) coincide con el pago de gastos del mes (8.972).

---

## 9. Métricas

### 9.1 Confiables (con fórmula exacta)

| Métrica | Fórmula | Notas |
|---|---|---|
| **Patrimonio neto (Neto)** | Valor de la celda con etiqueta "Neto" de cada hoja; en hojas con `#REF!` o duplicadas, recalcular el bloque. Equivale a Σ cajas (fila 2 + fila 3) convertidas + Deuda + USDT | Reproducible al centavo. Mostrar siempre con su cotización |
| **Ganancia Neta semanal** | Neto(t) − Neto(t−1), con t−1 = la hoja inmediatamente anterior | Ignorar la ganancia guardada en las 4 primeras hojas |
| **Ganancia por semana** | Ganancia Neta(t) ÷ (días de la hoja ÷ 7) | Sólo cambia `1008 - 2308` (÷ 2) |
| **Ganancia comparable** | Ganancia Neta(t) + Distribuciones(t) − Ajustes retroactivos(t) | Distribuciones y ajustes salen de una **tabla de eventos** cargada a mano (hoy: 22/03 22.672; 10/05 4.719; 07/06 2.510; 18/10 −15.855,49). No se puede automatizar: `2303 - 2903` tiene renglones de dividendos copiados que no son eventos |
| **Ganancia mensual** | Σ ganancia comparable de las hojas cuyo jueves cae en el mes | Mostrar cuántas semanas tiene y marcar el mes en curso como incompleto |
| **Egresos de la semana** | Bruto(t) − Neto(t); desglose por encabezado: GASTOS + FIJOS, COMISIONES, INVERSION, INTERESES, y DIVIDENDOS aparte | DIVIDENDOS es una distribución, no un gasto. Sumar `AL2` de `2707 - 0208` (2.317,44) si se quiere el egreso real |
| **Composición del patrimonio** | Líquido = Σ (fila 2 + fila 3) de billete, pesos, cheques, USDT, exterior y euros; Inversiones = POLIGONO + ALMAFUERTE + POLIGONO 20+13 + `AH`; Fijos = Deuda + USDT | Cierra con el Neto en las 33 hojas |
| **Posición en pesos** | ARS(t) = PESOS + CHEQUES + TRANSFER + RECAUDACION BX + bx (fila 4/5); en USD = ARS ÷ cot(t); % = ÷ Neto | Al 18/10: 180,15 M ARS = 117.359,83 USD = 32,7 % |
| **Efecto cotización** | ARS(t−1) × (1/cot(t) − 1/cot(t−1)) | Aproximado: supone la posición quieta toda la semana. Acumulado 08/03–18/10 ≈ −12.318 |
| **Ganancia sin efecto cotización** | Ganancia comparable − efecto cotización | Para ver la parte "operativa" |
| **Patrimonio contra aportes** | Neto − 71.111,11; múltiplo = Neto ÷ 71.111,11 | 18/10: 287.996,06; 5,05 veces |
| **Variación acumulada** | Neto(t) − Neto(fecha elegida) | 01/03 → 18/10: +191.162,38 |

### 9.2 Usables con aclaración

| Métrica | Por qué hay que aclarar |
|---|---|
| Ganancia Bruta | Suma de vuelta los dividendos (son parte de Egresos); falta el interés de `2707 - 0208`; antes de `2303 - 2903` se definía distinto. Mejor mostrar "Ganancia + Egresos" desglosado |
| Volumen semanal | Tipeado; `0405 - 1005` es copia; la hoja doble no dice si es total o promedio; cambió de definición en `2505 - 3105`. Sirve como orden de magnitud |
| Saldo por caja | La fila 2 y la fila 3 se compensan; mostrar caja + pendientes juntos, y caja sola sólo como dato secundario |
| Gastos semanales | Hay un pago grande por mes (5.500–9.000) y el resto son montos chicos: comparar meses, no semanas |

### 9.3 Engañosas (no mostrar, o sólo con advertencia)

| Métrica | Por qué engaña |
|---|---|
| **% de renta sobre volumen** (`C23` = GN ÷ Volumen; Value CG `RENTA`) | El numerador incluye inversiones, revaluaciones, ajustes y distribuciones; el denominador es tipeado y a veces copiado. Da 12,93 % el 30/08 y 4,59 % el 18/10 por razones que no tienen nada que ver con el volumen |
| **Promedio por operación** (`C22` = Volumen ÷ Operaciones) | Operaciones = 338 fijo en 13 hojas: el "promedio" sólo refleja el volumen |
| **Ganancia de la última semana sin separar el ajuste** | 18.103,33 aparenta la mejor semana desde agosto; la parte del período es 2.247,83 |
| **Rentabilidad sobre aportes** (Value CG `VARxCAP`, 273,91 % al 28/06) | Divide el patrimonio acumulado (con ganancias retenidas) por los aportes originales; no es una tasa por período |
| **Variación % semanal sobre capital** (`VARxCORTE`) | Hereda todo el ruido de la ganancia semanal |
| **Renglón "Dólares" de la planilla como "efectivo en dólares"** | Incluye pendientes, USDT, cuentas del exterior, inversiones (desde `2707 - 0208`) y flujos de egresos; llegó a −109.416,27 el 12/04 (`0604 - 1204!B7`) |
| **Suma de garantías** | PROMAR 600 M con moneda "USD"; las garantías netean 0 en el patrimonio |
| **Máximos y mínimos semanales sin normalizar** | La hoja doble y las semanas con distribuciones o ajustes salen primeras |
| **Promedios que mezclan meses de 4 y 5 semanas o el mes en curso** | Abril y julio tienen 5; octubre tiene 3 |
| **Participación por socio = Neto × %** | No coincide con las cuentas de Tenencia (descuentan dividendos y Alejo no los cobra); Tenencia no está cargada después de junio |
| **Comparar ganancia de Value CG con la de la Calculadora sin normalizar** | Value CG suma de vuelta los dividendos y muestra el 22/03 antes de la distribución |

---

## 10. Recomendaciones para el modelo de datos del dashboard

1. **Leer por encabezado, con un diccionario de alias**: `1`/`1,00` → CARA CHICA; BSAS → USD BsAs; Grabify BORRAR →
   Grabify; Dividendos → DIVIDENDOS; columna sin encabezado con saldo → "Inversión sin nombre (AH)" y una alerta.
2. **Detectar la fila de sumas** (la que tiene `=SUM(x2:x3)`) y la de monedas; si una columna tiene valores en filas 2–3
   pero no tiene suma, marcarla (hoy: INTERESES `2707 - 0208`, BSAS `2303 - 2903` y `2704 - 0305`).
3. **Tomar el Neto y el Bruto de la planilla** (son la verdad del dueño) y **recalcular sólo las ganancias** como
   diferencia contra la hoja anterior. Validar que la composición reclasificada cierre con el Neto (tolerancia 0,01).
4. **Versión por hoja:** si el mismo nombre aparece en varios archivos, usar el más nuevo; avisar si las filas 1–5
   difieren.
5. **Tabla de eventos** mantenida a mano (fecha, tipo, monto, nota): distribuciones, ajustes retroactivos, aportes,
   compras y ventas de inversiones, cambios de criterio (euro 1,20 → 1,25). El dashboard la usa para la ganancia
   comparable y para anotar los gráficos.
6. **Guardar la cotización de cada hoja** y la posición en ARS para mostrar el efecto cotización; alertar si la
   cotización se repite dos semanas seguidas.
7. **Redondear a 0** los saldos con |x| < 0,01 y ocultar cajas siempre en 0 (GRABIFY Jose, WISE US, LIBRAS,
   DEUDA USD, DEUDA PESOS, RECAUDACION BX, Grabify, JEEP/GOL TREND/CHARCAS netos).
8. **Value CG sólo para la historia anterior al 01/03** y como control; desde el 01/03 manda la Calculadora.

---

## 11. Preguntas abiertas para el dueño (los datos no las resuelven)

1. **Pendientes (fila 3):** la Calculadora los suma al patrimonio con su signo. ¿Positivo es "nos deben" o "debemos"?
   Si son deudas con terceros, el Neto está mal en esos montos (al 18/10, −7.962 neto; el 30/08, +59.787).
2. **Columna `AH` sin encabezado (75.466 → 112.966):** ¿son las cuotas de Polígono 20+13? ¿qué fueron los +37.500 del
   11/10?
3. **Renglón USDT:** ¿los +10.900 (19/04) y +4.021 (31/05) fueron aportes al negocio USDT General pagados con caja
   (neutros) o ganancias? ¿En qué fecha fue cada una de las 6 liquidaciones (para imputar los 15.855,49 a su mes)?
4. **"Deuda" 4.000:** ¿nos deben o debemos? La nota "restar aca" sugiere restar, pero la fórmula suma.
5. **Semana 24–30/08 (+42.940,48):** ¿qué pendiente en USD se cerró o cambió de signo?
6. **Dividendos después de junio:** ¿se pagaron? ¿dónde están registrados?
7. **Volumen de la hoja doble** (601.347,60): ¿total de dos semanas o promedio?
8. **Cotización C8:** ¿de dónde sale? ¿Conviene tomar la mediana semanal operada del Registro General?
9. **"NO CONTAR"** en `0806 - 1406` (Ingresos 3.600): ¿hay que sacarlo del Neto?
