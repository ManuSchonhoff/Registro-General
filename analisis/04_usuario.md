# 04 — Usuario: qué tiene que entender, qué quiere ver primero y cómo leer una semana

Rol: **usuario**. Me pongo en el lugar del dueño o de un socio que mira estos números todas las semanas pero no es analista.
Insumos: `analisis/00_inventario.md` y las tres planillas de `datos/value/`. Las cifras salen de los valores guardados en las
celdas. Para 12–18 oct uso la versión corregida (`2026-10-20b_…1210-1810.xlsx`) con los valores que dio el dueño. Montos en USD
salvo aclaración. Marco como **(cuenta mía)** las cifras que no están en ninguna celda y que calculé a partir de ellas.

---

## 0. Resumen

1. El usuario mira dos números: **cuánto vale hoy Cambio General** y **cuánto ganó esta semana**. Todo lo demás sirve para
   explicar esos dos.
2. Hoy los dos necesitan una aclaración al lado para no engañar. Del patrimonio de 359.107, **el 51% es Polígono** y no es plata
   para operar. La ganancia de 18.103 de la última semana son **2.248 de la operación + 15.855 de un ajuste de USDT General**
   ganado entre mayo y septiembre.
3. **Un mismo número tiene cinco nombres** (Neto, CAPITAL, Capital Actual, Balance Real, Monto) y **un mismo nombre tiene dos
   números** ("Bruto" es un patrimonio en la Calculadora y una ganancia acumulada en el Value CG). El dashboard tiene que usar
   un solo vocabulario y traducir el de la planilla.
4. Para decir si una semana fue buena, el dueño ya tiene **su propia vara**: las "Referencias" de 2%, 1% y 0,5% del volumen
   que están en cada hoja desde 25–31/05. También tiene sus propias etiquetas ("Bien", "Normal", "Semana corta", "Muy poco
   movimiento", "Costos fijos"). El dashboard tiene que usar esa vara y esas palabras, no inventar otras.
5. Lo que más confunde: dos ganancias que no coinciden entre archivos, porcentajes sin base, saltos por ajustes, pesos pasados
   a dólares con una cotización cargada a mano, semanas nombradas por rango y meses de 4 o 5 semanas, cajas negativas, columnas
   que no suman y datos viejos presentados como "actuales".

---

## 1. Quién lo usa y cómo

| Perfil | Qué conoce | Qué quiere saber | Cuándo lo mira |
|---|---|---|---|
| **El dueño que arma el cierre** | Todo: carga la Calculadora, sabe qué es cada caja y cada ajuste | Si la semana fue buena, por qué, y si quedó algo mal cargado | Una vez por semana, después del cierre del domingo |
| **Francisco, Jose** (socios y operadores) | Las cajas y la operación diaria | Cómo viene el negocio y cuánto les toca | Semanal o mensual, cuando se reparten dividendos |
| **Alejo** (socio, 15,62%; no figura entre los operadores) | Es el que menos contexto tiene | Cuánto vale su parte y si el negocio crece | Mensual. **Los textos hay que escribirlos para él** |

Qué hace hoy el usuario, según las planillas:

- En la **Calculadora** mira dos celdas: `Neto` (B16) y `Ganancia Neta` (B17). El resto del bloque lo usa para chequear.
- Las pasa al **Value CG**: columna B (`CAPITAL`) y columna E (`GANxCORTE`). Este archivo está cargado hasta el **28/06**.
- En el Value CG armó su propio **Dashboard**, y eso muestra qué le importa: capital actual, ganancia promedio mensual y
  semanal, bruto promedio, volumen promedio, renta sobre volumen, renta sobre capital, máximos y mínimos, y las últimas 6
  semanas.
- En la hoja `Semanales` le pone **una nota a cada semana**: "Bien", "Normal", "50% Menos", "Semana Corta", "MUY POCO
  MOVIMIENTO", "Costos fijos y cierre de mes", "Pagamos 5k intereses". Arriba de todo escribió: *"Ganancias Semanales (Es lo
  generado, no lo 'real')"*. Él mismo sabe que la ganancia es una variación del patrimonio y no plata que entró.
- Según el tablero v2 del Registro General (`docs/tablero_v2_spec.md`), los dueños lo miran **sobre todo en el celular**. Ese
  tablero, a propósito, **no muestra ganancia**: deja esa cuenta para el archivo de patrimonio. Este dashboard es justamente el
  que responde lo que el otro no. Conviene usar las mismas convenciones de escritura ("12–18 oct", "10–23 ago (2 sem.)",
  "USD 42,5 k", botón "?" con *Qué es / Cómo se calcula / De dónde sale*) para que los dos se lean igual.

---

## 2. Qué querría ver primero (primera pantalla)

Cinco cosas, en este orden. En el celular van apiladas y en escritorio entran en una fila de tarjetas más un gráfico.

| # | Pregunta del usuario | Qué mostrar | Por qué va arriba |
|---|---|---|---|
| 0 | "¿De cuándo son estos números?" | Una línea fija: **cierre del domingo 18/10 (semana 12–18 oct) · Dólar $ 1.535 · Euro USD 1,25 · Value CG cargado hasta el 28/06** | Cada archivo llega hasta una fecha distinta: la Calculadora, al 18/10; el Value CG, al 28/06; Semanales, al 14/06. El Dashboard del Value CG dice "Capital Actual" y muestra el 21/06 |
| 1 | "¿Cuánto vale Cambio General?" | **Patrimonio neto USD 359,1 k**, ▲ USD 18,1 k contra 5–11 oct, y debajo "Incluye USD 15,9 k de USDT General de mayo a septiembre" | Es el número que el dueño ya mira (B16) |
| 2 | "¿Cuánto ganamos esta semana, y estuvo bien?" | La **cuenta de la semana** en tres renglones (ver abajo), con un veredicto en palabras | Una sola cifra no alcanza: la ganancia neta salta por los gastos del mes y por los ajustes |
| 3 | "¿Cómo venimos?" | Barras de las últimas 12 semanas (con y sin ajustes), la línea "Tendencia: promedio de 4 semanas" y una frase: "Últimas 4 semanas: −USD 0,4 k. Marzo–junio: USD 6,7 k por semana" | Una semana suelta engaña. La tendencia es la noticia: desde septiembre la operación casi no deja ganancia |
| 4 | "¿Dónde está la plata?" | Una barra apilada: **Cajas para operar 36% · Polígono 51% · USDT General 12% · Deuda a cobrar 1%** | Sin esto, "359 mil" se lee como "tenemos 359 mil para operar" |
| 5 | "¿Hay algo raro?" | Hasta 3 avisos en llano, con la semana y la celda | Hay partidas grandes sin explicar que cambian la lectura de todo lo anterior |

**La cuenta de la semana (tarjeta 2), con los números de 12–18 oct:**

```
La operación dejó          USD 3.515   antes de gastos   · FLOJA
                                       0,89% de lo operado (USD 394 k). Tu vara del 1%: USD 3.941
Gastos, comisiones e int.  − USD 1.267
Quedó                      USD 2.248
Ajuste USDT General        + USD 15.855  (ganado de mayo a septiembre, cargado esta semana)
El patrimonio subió        USD 18.103
```

Cómo se arma: "dejó" = Ganancia Bruta sin el ajuste (19.370,41 − 15.855,49 = 3.514,91). "Gastos…" = Egresos (B14:
gastos 292,32 + comisiones 224,76 + intereses 750). "Quedó" = Ganancia Neta sin el ajuste (18.103,33 − 15.855,49 = 2.247,83).
"Lo operado" = Volumen Prom (B21). "Tu vara" = Referencias (B27:B29).

**Composición del patrimonio al 18/10 (tarjeta 4)** (cuenta mía, sumando las columnas de la hoja corregida):

| Parte | USD | % | Qué incluye |
|---|---:|---:|---|
| Cajas para operar | 130.039 | 36% | Pesos + cheques + transferencias: $ 180.147.333 / 1.535 = 117.360 · USD billete (cara chica, cambio, malos, USD) 10.131 · USD en el exterior 15.532 · euros 4.150 · USDT −18.868 · TRX 1.734 |
| Polígono | 183.532 | 51% | Columna `POLIGONO` 70.566 + columna AH **sin título** 112.966 |
| USDT General | 41.536 | 12% | Renglón `USDT` del bloque: la parte de Cambio General (2/3) en ese negocio |
| Deuda a cobrar | 4.000 | 1% | Renglón `Deuda`, cargado a mano |
| **Patrimonio neto** | **359.107** | | Coincide con B16 (los egresos de la semana se suman dentro de "Dólares" y se restan en "Egresos") |

**Lo que no va en la primera pantalla:** la tenencia por socio (el último dato es del 30/06; va en una segunda sección con su
fecha bien visible), el detalle caja por caja, el volumen mensual, los porcentajes acumulados sobre aportes y las garantías.

---

## 3. Cómo leer una semana: buena, normal, floja o mala

### 3.1 La regla, en tres preguntas

1. **¿La operación dejó plata?** Se mira la **ganancia bruta** (antes de gastos) contra **lo operado**, con la vara del
   dueño. Uso la bruta porque los gastos fijos se pagan todos juntos la primera semana del mes: con la neta, esa semana
   siempre parecería mala.

   | Ganancia bruta / volumen | Veredicto | Ejemplo real |
   |---|---|---|
   | 2% o más | **Muy buena** | 29/06–05/07: 13.957 / 463.878 = 3,0% |
   | entre 1% y 2% | **Normal** | 25–31/05: 8.033 / 474.625 = 1,7% (el dueño anotó "muy poco movimiento") |
   | entre 0,5% y 1% | **Floja** | 12–18/10: 3.515 / 394.063 = 0,9% |
   | menos de 0,5% | **Mala** | 14–20/09: 1.202 / 295.339 = 0,4% |
   | más de 5%, o con partidas sin explicar | **No comparable: revisar** | 24–30/08: 43.093 / 332.184 = 13,0% |

   El volumen recién está en la Calculadora desde 25–31/05. Antes de esa semana el veredicto se da en USD, contra la mediana
   (ver 3.3), y se avisa.

2. **¿Qué se pagó?** Egresos de la semana. Si fue **semana de costos fijos** (gastos de 5.500 a 9.000), una ganancia neta
   negativa es esperable y hay que mirar el mes completo. **5 de las 8 semanas con ganancia neta negativa** fueron semanas de
   costos fijos:

   | Semana | Ganancia neta | Gastos | Ganancia bruta |
   |---|---:|---:|---:|
   | 01–07/06 | −4.820,60 | 7.966,29 (+ dividendos 2.510) | 8.677,37 |
   | 06–12/07 | −1.542,73 | 5.827,66 | 5.258,92 |
   | 03–09/08 | −2.567,87 | 7.447,29 | 5.037,02 |
   | 31/08–06/09 | −5.067,21 | 8.972,30 | 3.964,95 |
   | 05–11/10 | −3.883,70 | 8.110,94 | 4.382,54 |

3. **¿Hubo algo que no es operación?** Si lo hubo, se muestra aparte y la semana se marca:
   - **Cotización.** Con $ 180 M en pesos y cheques, cada peso que se mueve el dólar cambia el patrimonio en unos **USD 76**
     (180.147.333 / 1.535², cuenta mía). En mayo, con $ 430 M, eran unos USD 218 por peso. Ejemplo: en 22–28/06 el dólar pasó
     de 1.455 a 1.490 y eso restó unos 2.700. La semana dio −758, pero la operación había dejado unos 3.900 (cuenta mía).
   - **Ajustes de otros períodos:** USDT General +15.855,49 (12–18/10).
   - **Compra o venta de inversiones:** Almafuerte y Polígono 20+13 en 10–23/08 (efecto neto ~+130, según el dueño). Los
     +37.500 de la columna AH en 05–11/10.
   - **Movimientos de los socios:** dividendos (4.719 en mayo, 2.510 en junio) y la liquidación de un ex socio en marzo
     (16.222).
   - **Saltos sin explicar:** +42.940 en 24–30/08 y el pendiente de cheques de 10–23/08 (≈ +18.360).
   - **Semana doble:** 10–23/08. Para comparar se cuenta como dos semanas de 9.175 cada una.

### 3.2 La frase que lee el usuario

El veredicto va siempre **con una palabra, un ícono y la razón**, nunca solo con un color. Ejemplos con datos reales:

- 12–18 oct: **"Floja.** La operación dejó USD 3.515 (0,9% de lo operado; tu vara del 1% era USD 3.941). Aparte entró un
  ajuste de USDT General de USD 15.855 que corresponde a mayo–septiembre."
- 05–11 oct: **"Floja, y con costos fijos.** La operación dejó USD 4.383 (0,9%). Se pagaron USD 8.111 de gastos del mes, por
  eso el patrimonio bajó USD 3.884."
- 24–30 ago: **"No comparable.** El patrimonio subió USD 42.940, diez veces lo habitual, y no hay explicación cargada. Revisar
  antes de sacar conclusiones."

### 3.3 Números de referencia para "lo normal"

Hojas con ganancia neta: 29 (30 semanas, una doble), del 23/03 al 18/10. Para las medianas saco el ajuste de USDT y divido
la semana doble por 2 (cuenta mía):

| | Ganancia neta por semana | Ganancia bruta por semana |
|---|---:|---:|
| Mediana del año | 5.030 | 6.932 |
| Una de cada cuatro semanas, menos de | −497 | 3.852 |
| Una de cada cuatro semanas, más de | 9.003 | 12.382 |
| Mediana de las últimas 12 semanas | 1.668 | 4.058 |
| Semanas negativas | 8 de 29 | **ninguna** (mínimo 1.201,77, 14–20/09) |

**La noticia del período**, que el usuario tiene que poder ver sin buscarla (sin el ajuste de USDT):

| Período | Semanas | Ganancia neta total | Por semana |
|---|---:|---:|---:|
| 23/03–28/06 | 14 | 94.380 | 6.741 |
| 29/06–30/08 | 9 (8 hojas) | 79.274 | — (42.940 son de una sola semana sin explicar y ≈ 18.360 del salto de cheques) |
| 31/08–18/10 | 7 | **−1.912** | −273 |

Hay que tener en cuenta lo que el dueño llamaba "normal" en abril: anotó **"Normal" con 14.902** (13–19/04) y **"Bien" con
18.464** (20–26/04). Hoy una semana normal es mucho menos. Por eso conviene que el veredicto use su vara proporcional al
volumen, que sigue valiendo aunque el volumen cambie, y no un monto fijo en USD.

### 3.4 Semana contra mes

El dueño piensa por mes (dividendos, tenencia), y un mes con costos fijos se lee mejor entero. Ganancia neta por mes, sin el
ajuste de USDT, con cada semana partida asignada al mes donde cae la mayoría de sus días (cuenta mía):

| Mes | Semanas | Ganancia neta | Nota |
|---|---:|---:|---|
| Abril | 5 | 52.366,62 | Coincide con el Value CG (52.366,61) |
| Mayo | 4 | 25.028,29 | El Value CG dice 29.747,29 porque vuelve a sumar los 4.719 de dividendos |
| Junio | 4 | 7.567,83 | El Value CG dice 10.077,82 (suma de vuelta 2.510 de dividendos) |
| Julio | 5 | 20.552,56 | |
| Agosto | 4 (3 hojas) | 58.721,66 | Sin las dos partidas sin explicar (42.940 y ≈18.360) queda en ≈ −2.600 |
| Septiembre | 4 | 442,61 | |
| Octubre (parcial) | 3 | −2.354,50 | Con el ajuste de USDT: +13.500,99 |

**Los meses tienen 4 o 5 semanas.** Comparar abril (5) con mayo (4) sin avisar exagera la caída. El gráfico mensual tiene que
mostrar cuántas semanas tiene cada mes y ofrecer "promedio por semana".

---

## 4. Glosario: términos que no se entienden sin contexto

Formato: **cómo aparece en la planilla** → qué es, en criollo → de dónde sale → **ojo**. Las definiciones cortas (la segunda
columna) son las que van en el "?" y en el glosario del dashboard. Lo marcado "a confirmar" se lo tiene que confirmar el dueño
(sección 9).

### 4.1 Mismo número, nombres distintos (y al revés)

| Lo que el usuario quiere decir | Cómo aparece | Dónde |
|---|---|---|
| **Patrimonio neto** | `Neto` | Calculadora B16 |
| | `CAPITAL` | Value CG, columna B |
| | `Capital Actual`, `Evolucion Balance Real (USD)`, `Capital` (tabla de 6 semanas) | Dashboard del Value CG |
| | `Monto` | Semanales, columna B |
| **Ganancia neta de la semana** | `Ganancia Neta` | Calculadora B17 |
| | `GANxCORTE` | Value CG, columna E (no siempre igual: suma de vuelta los dividendos) |
| | `Ganancia` | Semanales, columna C |
| **Ganancia bruta de la semana** | `Ganancia Bruta` | Calculadora B19 |
| | `BRUTOxSEM` | Value CG, columna H |
| | `Bruto` | Semanales D y tabla de 6 semanas del Dashboard |

| Mismo nombre | Significado 1 | Significado 2 |
|---|---|---|
| **Bruto** | Calculadora B18: patrimonio antes de restar los egresos de la semana (360.374,25) | Value CG G: ganancia bruta **acumulada** desde jul-2025 (468.691,27 al 28/06) |
| **USDT** | Columna K: la caja de USDT, hoy −18.867,90, que va dentro de "Dólares" | Renglón B13 del bloque: la parte en el negocio USDT General, hoy 41.536,49 |
| **Ganancia** | Semanales C: la de la semana | Tabla de 6 semanas del Dashboard: la **acumulada** sobre aportes (`P&L APORTE`), 176.169,85 al 17/05 cuando esa semana ganó 8.832,17 |
| **Capital** | Value CG B: patrimonio | Dashboard E38:E39, bajo "Ganancia Neta Total": la ganancia acumulada sobre aportes (195.536,47) |
| **Deuda** | Renglón B12: lo que nos deben (4.000) | Columnas `DEUDA USD` y `DEUDA PESOS`: siempre en 0 |

**Decisión para el dashboard:** un solo nombre por concepto: *Patrimonio neto*, *Ganancia de la semana*, *Lo que dejó la
operación (antes de gastos)*. Cada "?" dice cómo se llama en la planilla: "En la Calculadora: Neto (B16). En el Value CG:
CAPITAL".

### 4.2 Los números grandes (bloque de cálculo de la Calculadora)

| Término | Qué es | De dónde sale | Ojo |
|---|---|---|---|
| **Neto** → *Patrimonio neto* | Lo que vale Cambio General al cierre del domingo, todo pasado a dólares: cajas, inversiones, la parte de USDT General y lo que nos deben, menos lo que se fue en la semana | B16 = suma de B7:B15 | **No es plata disponible**: hoy el 51% es Polígono |
| **Bruto** | El patrimonio antes de restar los egresos de la semana | B18 = Neto + egresos | Solo sirve para calcular la ganancia bruta. No mostrarlo solo |
| **Dolares** | Todas las cajas en USD, más Polígono y la columna AH | B7 | De los 193.328 que la hoja llama "Dólares", **solo 8.530 son cajas** (billete, USDT, TRX y cuentas del exterior; cuenta mía). Hay 183.532 de Polígono y 1.267 de egresos que se restan dos renglones más abajo |
| **Pesos** | Todas las cajas en pesos (efectivo, cheques, transferencias, recaudación) divididas por la cotización | B8 = (E4:J4 + M4) / C8 | Los cheques entran por su valor nominal |
| **Euros** | Euros billete más la cuenta Wise en euros, por 1,25 | B9 = (Y4 + V4) × C9 | Hasta 18–24/05 el 1,2 estaba escrito dentro de la fórmula |
| **Deuda** | Plata que le deben a la financiera | B12, número fijo | Cargado a mano: 5.000 hasta el 10/05 y 4.000 desde el 11/05. Quién debe: a confirmar |
| **USDT** (renglón) | La parte de Cambio General (2/3) en el negocio USDT General | B13, número fijo | Va subiendo a mano: 10.760 → 21.660 (13–19/04) → 25.681 (25–31/05) → 41.536,49 (12–18/10). No es la caja USDT |
| **Egresos** | Lo que salió en la semana: gastos, comisiones pagadas, inversión, intereses y dividendos | B14 = −(GASTOS…DIVIDENDOS) | **Incluye dividendos**, que no son un gasto del negocio sino un retiro de los socios |
| **Ingresos** | Alquileres cobrados | B15 | Vacío desde 27/07 |
| **Poligono 09**, **Almafuerte** (renglones B10 y B11) | Deberían mostrar esas inversiones | B10 = AD4, B11 = AC4 | **Apuntan a otras columnas** (GOL TREND y JEEP) y dan 0. Polígono entra por "Dólares". No mostrar estos renglones |
| **Cotización** (C8) | Cuántos pesos vale un dólar. Con ese número se pasan los pesos a USD | Cargado a mano | Hoy cada peso de diferencia mueve el patrimonio ≈ USD 76. Quedó igual varias semanas seguidas: 1.525 en las cuatro hojas del 20/07 al 23/08 |
| **Euro** (C9) | Cuántos dólares vale un euro | 1,25 fijo desde 25–31/05 | config.json usa 1,23 para el Registro General |
| **Volumen Prom** → *Lo operado* | Cuánta plata se movió con clientes en la semana, en USD: el promedio entre lo que entró y lo que salió | B21, pegado como valor | En la Calculadora está desde 25–31/05; en el Value CG (VOLUMEN), desde el 01/03 |
| **Operaciones** | Cantidad de operaciones de la semana | B22 | **338 copiado igual en las 12 hojas desde 20–26/07.** No mostrarlo, ni tampoco el "ticket" C22 = volumen / operaciones (1.165,87) |
| **Referencias** → *Tu vara* | Lo que sería ganar el 2%, el 1% y el 0,5% de lo operado | A27:B29 (desde 25–31/05) | Hoy: 7.881 / 3.941 / 1.970. Si es una vara para la neta o para la bruta: a confirmar |
| **Ganancia Neta** / C23 | Cuánto subió o bajó el patrimonio contra el domingo anterior. C23 es lo mismo dividido por lo operado | B17 = Neto − Neto anterior | No es plata que entró: también la mueven la cotización, los ajustes y las compras o ventas de inversiones. C23 está en fracción (0,006 = 0,6%) |
| **Ganancia Bruta** / C24 | Lo que dejó la semana antes de pagar gastos, comisiones, intereses y dividendos | B19 = Bruto − Neto anterior | Nunca fue negativa en 2026 |

### 4.3 Value CG y su Dashboard

| Término | Qué es | Ojo |
|---|---|---|
| **CAPITAL** | El patrimonio neto de cada domingo | Es el mismo número que el Neto de la Calculadora; no es capital aportado |
| **Aportes** | Lo que pusieron los socios: 71.111,11 (Manuel, Francisco y Jose 20.000 cada uno; Alejo 11.111,11) | Antes de marzo había otra base: 69.985,48 |
| **P&L APORTE** | Cuánto creció el patrimonio por encima de lo aportado (CAPITAL − Aportes). 194.778,24 al 28/06 | Ya tiene restados los dividendos retirados: no es "toda la ganancia histórica" |
| **VARxCAP** | P&L APORTE como % de lo aportado. 273,91 al 28/06 = la ganancia acumulada es 2,7 veces lo aportado | Es un % escrito sin el signo. En el Dashboard aparece como "Renta 274,97" |
| **GANxCORTE** | Ganancia de la semana (corte = cierre del domingo) | Después de un renglón "Dividendos", compara contra el patrimonio ya sin los dividendos. Por eso 04–10/05 da 9.874,55 acá y 5.155,55 en la Calculadora |
| **VARxCORTE** | GANxCORTE como % del patrimonio de la semana anterior | Se lee "−0,28" (28/06) sin el signo % |
| **BRUTOxSEM** | Ganancia bruta de la semana | Coincide con la Ganancia Bruta de la Calculadora |
| **BRUTO** | Suma de todas las ganancias brutas semanales desde jul-2025 | No es un patrimonio. No mostrar |
| **VOLUMEN** | Lo operado en la semana (en los renglones de mes, la suma del mes) | |
| **RENTA** | Ganancia de la semana por cada 100 USD operados | En 01/03 y 08/03 usa la bruta; desde 15/03, la neta |
| **GASTOS / GxSEMANA** | Gastos acumulados / gastos de la semana | |
| **COMISIONES / COMI x Sem** | Comisiones que **pagó** la financiera (acumuladas / de la semana) | **No son las comisiones cobradas a clientes**, que van dentro de la ganancia. En 18–24/05 la Calculadora tiene comisiones 1.051,74 e inversión 587,88, y el Value CG las tiene al revés |
| **INVERSION / IxSEMANA** | Plata que se fue a "inversión" (acumulada / de la semana) | Qué es: a confirmar. Se resta como egreso. Si es algo que queda (una compra), achica el patrimonio de más |
| **INTERESES / IxSem** | Intereses pagados a los inversores que le prestan plata a la financiera | **IxSem (intereses) e IxSEMANA (inversión) se escriben casi igual.** En 06–12/07 la columna INTERESES tiene 924,16, el mismo número que el Value CG anota como dividendos de junio |
| **DIVIDENDOS / DIVxSem** | Lo que retiran los socios cada mes | Value CG: 4.719 (abril), 2.510 (mayo), 924,16 (junio). En marzo, 22.672 = 6.450 de dividendos + 16.222 de la liquidación de un ex socio |
| **ALQUILERES / ALQxSEM** | Alquileres cobrados | 900 (01–07/06) y 3.600 (08–14/06). La columna dejó de aparecer después de 20–26/07 |
| **COMPLEMENTOS** | Renglones fijos que se suman al patrimonio: USDT General y Deuda | |
| **Renglones de mes** ("Marzo", "Abril"…) | Totales del mes | **Las columnas cambian de significado**: en "Marzo", E es la ganancia menos los dividendos, F (que en las semanas es un %) es la suma de ganancias y G (que es BRUTO) es un % |
| **Balance Actual** | El patrimonio del 22/03 después de restar dividendos y liquidación: 171.509,70 | |
| **Renta Sobre Capital Prom.** (Dashboard) | Promedio de los % semanales (4,80) o mensuales (27,82) | Promedia desde febrero, cuando el patrimonio era más chico (19,03% el 08/02). **No es lo que rinde hoy** |
| **Ganancia Prom. / Max / Min Ganancia Semanal** (Dashboard) | Promedio, máximo y mínimo semanal | Incluyen tramos que no son semanas: el "máximo semanal" de 37.660,15 es la variación desde los dividendos de 2025 hasta el 01/02/2026. El promedio semanal de 10.339,49 incluye un tramo de 28.122 que termina en jul-2025 |

### 4.4 Cajas (encabezados de la fila 1 de cada hoja semanal)

| Caja | Qué es | Hoy (12–18/10) | Ojo |
|---|---|---|---|
| **CARA CHICA** | Billetes de dólar viejos (la serie de "cara chica"). Se canjean con descuento | 5.525 | Suman a valor nominal |
| **CAMBIO** | Billetes de dólar chicos | 9.290 | |
| **MALOS** | Billetes de dólar dañados. Se canjean con descuento | 2.545 | Suman a valor nominal |
| **USD** | Dólar billete | **−7.229,02** | Una caja negativa no es en sí un error: el saldo viene del cierre del Registro General, que incluye pendientes y plata de terceros |
| **PESOS** | Pesos en efectivo | $ 138.132.428,70 | |
| **CHEQUES** | Cheques en cartera, en pesos | $ 10.382.849,69 | Valor nominal, sin descontar |
| **TRANSFER** | Pesos en cuentas bancarias | $ 31.632.055 | |
| **USD BsAs** | Dólares en la caja de Buenos Aires | vacía | La fórmula la divide por la cotización, como si fueran pesos |
| **DEUDA USD / DEUDA PESOS** | — | 0 en las 33 hojas | Ocultar |
| **USDT** | Caja de USDT (dólar digital) | **−18.867,90** | No confundir con el renglón USDT del bloque |
| **TRX** | Saldo en TRX, la cripto de la red TRON que se usa para mandar USDT | 1.734 | El mismo valor en las 26 hojas donde aparece. Si son USD o unidades de TRX: a confirmar |
| **RECAUDACION BX** | Pesos de la recaudación (cobrar transferencias y entregar efectivo, con comisión) | 0 | Qué es "BX": a confirmar |
| **USDT General** (columna) | Caja de la contraparte con la que se compran y venden USDT | ≈ 0 | No es el renglón USDT ni el "negocio USDT General" |
| **Grabrfy Manuel, GRABIFI, GRABIFY Jose, Grabify, Grabify BORRAR** | Cuentas en dólares en el exterior en una plataforma; el nombre dice de quién es la cuenta | 10.399,27 y 4.915,15 (el resto, 0) | La misma plataforma escrita de cinco formas. Mostrar "Cuentas en el exterior" con el detalle al tocar |
| **LLC** | Cuenta de una sociedad en EE. UU. | 0 (llegó a 31.666,84) | |
| **PayPal Ruso** | Cuenta PayPal | 218 | |
| **CITY BANK, PAYONEER, WISE US** | Cuentas en dólares en el exterior | 0 | |
| **WISE** | Cuenta Wise **en euros** | € 1.464,82 | Está en euros aunque esté entre las cuentas en dólares |
| **EUROS** | Euros billete | € 1.855 | |
| **REALES, LIBRAS** | Billetes de esas monedas | R$ 4 · £ 0 | **No se suman al patrimonio** (hoy casi no hay) |

### 4.5 Inversiones y garantías

| Término | Qué es | Ojo |
|---|---|---|
| **POLIGONO** | Inversión de la financiera en el proyecto Polígono, valuada por lo pagado | 70.565,57. Va dentro de "Dólares" |
| **Columna AH, sin título** | En 10–23/08 se llamaba `POLIGONO 20+13` (cuotas que paga la financiera, 75.466). Desde 24–30/08 no tiene título | Hoy 112.966: subió 37.500 en 05–11/10. Va dentro de "Dólares". Mostrarla como "Polígono 20+13 (columna sin título)" hasta que el dueño confirme |
| **ALMAFUERTE** | Inversión que se compró y se vendió a 50.000 | 50.000 entre 13/07 y 09/08; desde 10–23/08, 0 |
| **Carbox** | Proyecto vinculado a autos (aparece en 06–12/04 como "Ganancia Semanal con Carbox") | |
| **MILLAMAPU, CHARCAS, PROMAR, JEEP, GOL TREND** | Bienes tomados en garantía | En la última hoja, la fila 2 y la fila 3 se cancelan (Promar: 87.000.000 y −87.000.000) y no suman al patrimonio. Una cifra de 87 millones asusta: mostrarlas solo en una lista de "garantías en custodia" |

### 4.6 Fechas, períodos y socios

| Término | Qué es | Ojo |
|---|---|---|
| **"1210 - 1810"** | La semana del lunes 12/10 al domingo 18/10 | El nombre no tiene año. El Value CG anota la misma semana con el domingo (18/10). En el dashboard: "12–18 oct" |
| **"(Dos Semanas)"** | La hoja de 10–23/08 cubre dos semanas | Sus montos son de dos semanas: para comparar, se dividen por 2 |
| **Corte / cierre** | El domingo en que se toma la foto de las cajas | |
| **Mes de una semana partida** | En el Value CG, 27/04–03/05 quedó en abril y 23/02–01/03 en febrero (el mes con más días). La plantilla de los meses que vienen, en cambio, pone el 02/08 en agosto | Elegir una regla, decirla en el "?" y aplicarla siempre (propuesta: el mes con más días) |
| **Pendientes** | Operaciones que quedaron abiertas al cierre. El saldo de cada caja que sale del Registro General las incluye | Por eso una caja puede dar negativa |
| **Tenencia** | Qué parte del negocio es de cada socio: Manuel, Francisco y Jose 28,13% cada uno; Alejo 15,62% | El título dice 15,63% y la fórmula usa 15,62. Las cuatro partes suman 100,01% |
| **Capital de cada socio** | Su parte del patrimonio (hoja Tenencia): al cierre de junio, después de dividendos, 78.208,65 cada uno y Alejo 29.715,55 | Está cargado solo hasta junio |
| **Dividendos (en Tenencia)** | El 10% de la ganancia del mes (H8 = H7 / −10) | El Value CG anota ≈ 84% de ese 10% (4.719 de 5.593,70 en abril): casi la parte de Manuel, Francisco y Jose (3 × 28,13% = 84,39%) |
| **Liquidación** | Pago de salida a un ex socio (16.222,98 en marzo) | |
| **"Es lo generado, no lo real"** | La nota del dueño en Semanales: la ganancia es cuánto cambió el patrimonio, no plata que entró | Ponerla, con otras palabras, en el "?" de la ganancia |

---

## 5. Qué le confundiría de un dashboard, y cómo evitarlo

| # | Confusión | Ejemplo real | Qué hacer en la interfaz |
|---|---|---|---|
| 1 | **Dos ganancias que no coinciden** | 04–10/05: la Calculadora da 5.155,55 y el Value CG 9.874,55 (dividendos de 4.719). 01–07/06: −4.820,60 contra −2.310,60 | Una sola ganancia protagonista, con los dividendos **aparte** ("Retiros de socios") y no como gasto. En el "?": "En el Value CG puede figurar distinto porque…" |
| 2 | **Ganancia neta contra bruta** | Siempre hay dos números y no se sabe cuál mirar | La "cuenta de la semana" en tres renglones (dejó → se pagó → quedó). Nunca dos tarjetas que digan "Ganancia" |
| 3 | **Porcentajes sin base** | "Renta 274,97", "VARxCORTE 1,92", "4,80 semanal", "0,006" | Todo % con su base en palabras y el monto al lado: "0,9% de lo operado (USD 394 k) = USD 3.515". Un solo formato (4,7%), nunca fracciones |
| 4 | **Saltos por ajustes y partidas no operativas** | 12–18/10 +15.855 (USDT General); 24–30/08 +42.940; 10–23/08 cheques ≈ +18.360; marzo −22.672 (dividendos y liquidación) | Botón "Con ajustes / Sin ajustes" (por defecto, **sin**). Ícono en la barra de la semana y una línea que explica qué se sacó. El patrimonio siempre es el real |
| 5 | **El crecimiento parece todo ganancia** | Del 28/06 al 18/10 el patrimonio subió 93.218. De eso, 77.156 vienen de tres partidas: 42.940 sin explicar, ≈18.360 de cheques sin aclarar y 15.855 de USDT de meses anteriores (cuenta mía) | En la curva del patrimonio, marcar los saltos con su etiqueta. Al lado, la frase "de esto, operación: USD 16 k" |
| 6 | **Monedas mezcladas y cotización a mano** | $ 180 M pasados con 1.535; euros por 1,25; cara chica y malos al 100%; Promar 87.000.000 en una columna marcada "USD" | Todo en USD con la cotización a la vista. Botón "ver en moneda original" en el detalle de cajas. Avisar cuando la cotización es igual a la de la semana anterior |
| 7 | **"Dólares" que no son dólares; patrimonio que no es plata** | "Dólares 193.328", pero 183.532 son Polígono | No usar los renglones del bloque como categorías. Usar las cuatro partes de la tarjeta 4 |
| 8 | **Fechas por rango, sin año, y la semana doble** | "1210 - 1810", "1008 - 2308 (Dos Semanas)" | "12–18 oct"; "10–23 ago (2 sem.)" con barra doble de ancho o un rayado, y comparación dividida por 2 |
| 9 | **Meses de 4 y de 5 semanas** | Abril (5) contra mayo (4) | Mostrar "(5 sem.)" en cada mes y ofrecer "promedio por semana" |
| 10 | **Signos** | Egresos −1.267,08; en sus columnas, los gastos son positivos | Los egresos se muestran en positivo con el verbo: "Se pagaron USD 1.267". Nunca dos negativos seguidos |
| 11 | **Cajas negativas** | USD −7.229; USDT −18.868 | Una nota: "Negativo: según el cierre del Registro General, salió más de lo que había. Suele ser plata de terceros o pendientes" |
| 12 | **Datos fijos que parecen datos** | Operaciones 338 (12 hojas), TRX 1.734 (26 hojas), Deuda 4.000, USDT 25.681 (19 hojas seguidas, 25–31/05 a 05–11/10), cotización 1.525 (4 hojas) | No mostrar Operaciones. Lo que es fijo por diseño lleva "valor fijo, cargado a mano". Lo repetido entra en "Para revisar" |
| 13 | **Datos viejos llamados "actuales"** | "Capital Actual 266.647,58" es del 21/06; Semanales termina el 14/06 con 254.204,96 cuando la Calculadora dice 261.617,18 | Cada cifra con su fecha ("Foto al 18/10"). No traer números del Dashboard viejo ni de Semanales |
| 14 | **Promedios y máximos que mezclan períodos** | "Máxima ganancia semanal 37.660" que no es una semana | Calcular promedios y extremos solo sobre semanas reales, decir el período ("desde el 23/03") y marcar las excluidas |
| 15 | **Columnas con nombres casi iguales o al revés** | IxSEMANA (inversión) contra IxSem (intereses); comisiones e inversión invertidas entre archivos en 18–24/05; Grabify escrito de cinco formas | Nombres en llano: "Intereses a inversores", "Inversiones", "Cuentas en el exterior" |
| 16 | **Comisiones que parecen ingresos** | La columna COMISIONES es lo que **se pagó** | Llamarla "Comisiones pagadas" |
| 17 | **Renglones que apuntan a otra columna** | "Poligono 09" lee GOL TREND; "Almafuerte" lee JEEP | No mostrar esos renglones. Polígono sale de sus columnas |
| 18 | **Garantías con cifras enormes** | Promar 87 M, Millamapu 200 k | Fuera de la vista del patrimonio; lista aparte con la leyenda "no suman" |

---

## 6. Textos de ayuda: dónde van y qué dicen

### 6.1 Dónde

1. **Línea de estado fija** arriba de todo: la fecha del cierre, la cotización, el euro y hasta cuándo está cargado el Value CG.
2. **Subtítulo fijo** debajo de cada número grande, de una línea y siempre visible. Ahí va lo que evita el error más común, no
   la fórmula.
3. **Botón "?"** en cada tarjeta y en cada gráfico, con tres partes: *Qué es / Cómo se calcula / De dónde sale* (hoja y celda,
   por ejemplo "Calculadora, hoja 1210 - 1810, celda B16"). Es el mismo patrón del tablero v2.
4. **Aviso en la semana** (franja amarilla con ícono y palabra) cuando tiene un ajuste, es doble o tiene una partida sin
   explicar.
5. **Marcas en los gráficos**: un ícono sobre la barra o el punto, con la explicación al tocarlo.
6. **"Cómo leer este tablero"**, desplegable y abierto solo la primera vez (si no se puede recordar, cerrado con un toque):
   tres renglones.
7. **Glosario** en un panel con buscador. Cada término dice cómo se llama en la planilla, para que el usuario lo encuentre
   aunque lo busque por "Neto" o por "GANxCORTE".
8. **Datos que faltan**: "—" con el motivo ("El volumen se carga desde 25–31/05"), nunca un 0.

### 6.2 Qué dicen (propuesta de textos)

| Lugar | Texto |
|---|---|
| Línea de estado | "Cierre del domingo 18/10 (semana 12–18 oct) · Dólar $ 1.535 · Euro USD 1,25 · Value CG cargado hasta el 28/06" |
| Cómo leer este tablero | "1. El patrimonio es lo que vale Cambio General, todo pasado a dólares; no es todo plata disponible. 2. La ganancia de la semana es cuánto creció el patrimonio, sin ajustes de otros períodos. 3. Para saber si la semana fue buena, mirá lo que dejó la operación contra lo operado." |
| Patrimonio (subtítulo) | "Todo pasado a dólares. La mitad es Polígono: no se puede usar para operar." |
| Patrimonio (?) | "Qué es: cajas + inversiones + la parte de USDT General + lo que nos deben, menos lo que se pagó en la semana. Cómo se calcula: los pesos se pasan a dólares con la cotización del domingo y los euros por 1,25. De dónde sale: Calculadora, Neto (B16); en el Value CG se llama CAPITAL." |
| La operación dejó (?) | "Lo que ganó la semana antes de pagar gastos, comisiones, intereses y dividendos. En la planilla: Ganancia Bruta (B19)." |
| Veredicto (?) | "Comparamos lo que dejó la operación con lo operado, usando tu vara de la Calculadora: 2% o más, muy buena; de 1% a 2%, normal; de 0,5% a 1%, floja; menos de 0,5%, mala." |
| Quedó (?) | "Cuánto creció el patrimonio contra el domingo anterior, sin ajustes. No es plata que entró: también la mueven el dólar y las compras o ventas de inversiones. En la planilla: Ganancia Neta (B17)." |
| Aviso de ajuste | "Esta semana incluye USD 15.855 de USDT General ganados entre mayo y septiembre. Los mostramos aparte para no inflar la semana." |
| Aviso de costos fijos | "Semana de costos fijos: los gastos del mes se pagan juntos. Mirá el mes completo." |
| Aviso de semana doble | "Esta hoja cubre dos semanas (10–23 ago). Para comparar, la contamos como dos semanas de USD 9.175." |
| Aviso de salto sin explicar | "El patrimonio subió USD 42.940 en una semana, diez veces lo habitual, y no tiene explicación cargada. Revisar antes de sacar conclusiones." |
| Cotización (?) | "Con el dólar a $ 1.535, cada peso que se mueve cambia el patrimonio en unos USD 76. Si la cotización quedó vieja, la ganancia de la semana está mal." |
| Polígono (?) | "Inversión en el proyecto Polígono, valuada por lo pagado. Hay una parte en una columna sin título de la planilla (USD 112.966)." |
| USDT General (?) | "La parte de Cambio General (2/3) en el negocio USDT General. Se actualiza a mano; no es la caja de USDT." |
| Caja negativa | "Negativo: según el cierre del Registro General, salió más de lo que había. Suele ser plata de terceros o pendientes." |
| Retiros de socios | "Dividendos: lo que retiran los socios. No es un gasto del negocio; por eso no lo restamos de la ganancia." |
| Tenencia | "Parte de cada socio al 30/06 (último mes cargado en la hoja Tenencia)." |

---

## 7. Qué le sobra

- **Las 15 columnas que están en cero en todas las hojas**: DEUDA USD, DEUDA PESOS, USDT General, Grabify, GRABIFY Jose, WISE US,
  LIBRAS, RECAUDACION BX, MILLAMAPU, Grabify BORRAR, Dividendos, JEEP, GOL TREND, CHARCAS y PROMAR. También las cajas que hoy
  están en 0 (LLC, City Bank, Payoneer): se ven solo en el detalle y con un "mostrar cajas en cero".
- **Operaciones y ticket promedio** (dato copiado).
- **BRUTO acumulado** del Value CG.
- **VARxCAP y la renta sobre capital promedio** como indicadores principales. Si se muestran, que sea en la sección de socios
  y en palabras: "la ganancia acumulada es 2,7 veces lo aportado (al 28/06)".
- **Volumen mensual sumado** (2.378.814 en mayo): al usuario le dice más el semanal.
- **Las garantías** dentro de la vista del patrimonio.
- **Decimales** en las tarjetas: "USD 359,1 k". El número exacto va en la tabla y en el "?".

---

## 8. Interacciones que un no analista sí va a usar

1. **Tocar una semana** abre su cuenta en escalones: patrimonio del domingo anterior → + lo que dejó la operación → − gastos,
   comisiones e intereses → − retiros de socios → ± efecto del dólar (estimado) → ± ajustes e inversiones → patrimonio de este
   domingo. Al pie: "Ver en la planilla: hoja 1210 - 1810, B16 y B17".
2. **Con ajustes / Sin ajustes**: un solo botón, global, que diga a la vista qué se está sacando.
3. **Semana / Mes**: el mes muestra cuántas semanas tiene y el promedio por semana.
4. **Comparar** solo contra la semana anterior y contra el promedio de las 4 previas (como el tablero v2). Nada de selectores
   de período libres en la primera pantalla.
5. **Ver en moneda original** dentro del detalle de cajas (pesos en "$ 180,1 M").
6. **Las notas del dueño** (Semanales!E) sobre cada semana. Esas notas pueden tener nombres de terceros: se muestran tal cual
   dentro del tablero privado, y nunca en el código ni en un archivo versionado.

---

## 9. Lo que el dueño tiene que confirmar para que los textos sean ciertos

1. **Columna AH sin título** (112.966): ¿es Polígono 20+13? ¿Qué fueron los +37.500 de 05–11/10?
2. **Tu vara (Referencias 2%, 1% y 0,5%)**: ¿es para la ganancia neta o para la bruta? ¿Qué porcentaje considerás una semana
   normal?
3. **INVERSION** como egreso: ¿qué es? ¿Queda algo a cambio?
4. **Dividendos**: ¿se restan de la ganancia (como hace la Calculadora) o no (como hace el Value CG)? Propuesta: no se restan
   y se muestran aparte.
5. **Mes de las semanas partidas**: propuesta, el mes con más días (como en febrero y abril del Value CG).
6. **Deuda 4.000**: ¿quién debe y sigue vigente?
7. **TRX 1.734**: ¿son dólares o unidades de TRX? ¿Por qué no cambia nunca?
8. **"BX"** en Recaudación BX.
9. **Cara chica y malos**: ¿se valúan al 100% o con el descuento del canje?
10. **Alejo**: ¿15,62% o 15,63%?
11. **24–30/08 (+42.940) y cheques de 10–23/08 (≈ +18.360)**: hasta que se aclaren, el dashboard los muestra como "a revisar"
    y fuera del promedio.
