# 01 — Negocio: qué es esta planilla y qué preguntas tiene que responder el dashboard

Rol: **Negocio**. Insumos: `analisis/00_inventario.md`, las tres planillas de `datos/value/` (leídas con y sin
`data_only`), `docs/contexto_negocio.md`, `docs/metodologia.md` y lo que contó el dueño. Todos los montos son en USD salvo
que diga otra cosa. Cada número que aparece abajo lo recalculé desde las celdas; cuando cito una celda va entre
paréntesis (hoja!celda).

---

## 0. En pocas palabras

- **Qué es.** Es el **análisis de patrimonio** de Cambio General. Una vez por semana, el dueño pega en la *Calculadora
  Semanal* los saldos de cada caja que salen del cierre del Registro General. La hoja los pasa a dólares y calcula el
  **Neto** (lo que vale la financiera). La diferencia contra la semana anterior es la **ganancia**. El *Value CG* es el
  libro histórico de esos cierres. De ahí salen el reparto entre socios (hoja *Tenencia*) y un tablero viejo (hoja
  *Dashboard*).
- **Para qué la usan.** Para saber cuánto vale la financiera, cuánto ganó en la semana y en el mes, cuánto le toca a cada
  socio y **cuánto dividendo se reparte**: la regla es el 10% de la ganancia del mes. También sirve para ver dónde está
  la plata (Polígono, pesos, USDT General) y si la operación cubre los costos.
- **Foto al 18/10/2026** (hoja corregida 12–18/10). El Neto es **359.107,17**, unas 5,05 veces los aportes (71.111,11).
  La semana dio **+18.103,33**, pero 15.855,49 de eso es el ajuste de USDT General de mayo a septiembre: la operación de
  la semana dejó **≈ 2.248**.
- **El mensaje que tiene que dar el dashboard.** Entre el 28/06 y el 18/10 el Neto subió 93.218. De eso, unos 77.000
  vienen de tres movimientos: el ajuste USDT, el salto sin explicar del 24–30/08 (+42.940) y los cheques del 10–23/08
  (≈ +18.400). Sin ellos, quedan **≈ 16.000 en 16 semanas** (≈ 1.000 por semana), contra 6.000 a 8.000 por semana en
  abril y mayo. **Desde el 31/08 la operación no cubre los costos.** En esas 7 semanas, la ganancia bruta fue 22.571, los
  egresos 24.483 y la neta −1.912.
- **La mitad del patrimonio no es plata disponible.** El 51% (183.532) está en Polígono y otro 12% (41.536) es la
  participación en USDT General.
- **El Value CG y la Tenencia están parados en junio.** Julio, agosto y septiembre no tienen ganancia mensual cerrada ni
  dividendos calculados. Esa es justo la decisión que los socios tienen pendiente.

---

## 1. Qué es cada planilla

| Archivo / hoja | Qué registra | Quién la carga | Cada cuánto | Estado al 20/10/2026 |
|---|---|---|---|---|
| **Calculadora Semanal** (`2026-10-20a_…`), hojas `DDMM - DDMM` | Una hoja por semana, de lunes a domingo. Fila 1: una columna por caja. Filas 2 y 3: los saldos de cada caja pegados como valores desde el cierre del Registro General. Fila 4: la suma. Fila 5: la moneda. Abajo, el bloque que calcula Dólares, Pesos, Euros, Deuda, USDT, Egresos, **Neto, Ganancia Neta, Bruto y Ganancia Bruta**, más Volumen y Operaciones. | El dueño que hace el cierre | Semanal. Hubo atraso: no se cerró desde agosto y se completó todo de una vez hasta el 12–18/10 | 33 hojas, del 23/02 al 18/10 (34 semanas: la del 10–23/08 es doble) |
| **Calculadora, hoja corregida** (`2026-10-20b_…`) | La misma hoja `1210 - 1810`, con la fila USDT actualizada (+15.855,49 de USDT General, mayo–sep). **Reemplaza** a la del archivo anterior. | El dueño | Una vez | La Ganancia Neta y la Bruta dan `#REF!`, porque se copió sola a otro archivo. Valores correctos según el dueño: Neto 359.107,17, GN 18.103,33, Bruto 360.374,25, GB 19.370,41 (los recalculé y coinciden) |
| Calculadora, `Semanales` | Lista de cierres con monto, ganancia, bruto y una **nota de qué pasó** cada semana ("Pagamos costos fijos", "MUY POCO MOVIMIENTO"). El título dice: *"Es lo generado, no lo 'real'"*. | El dueño | Semanal hasta el 14/06; después, abandonada | Desactualizada y con montos que no coinciden con las hojas semanales desde junio |
| Calculadora, `CONTROL` y `Volumen Mayo` | Una hoja de control de saldos (fila menos fila) y el volumen de mayo de Manuel y Francisco | El dueño | Puntual | Auxiliares, no se mantienen |
| **Value CG** (`2026-10-20_Value_CG_2026.xlsx`), hoja `Value CG` | El **histórico**: una fila por semana con CAPITAL (= Neto), P&L sobre aportes, ganancia semanal y %, bruto, volumen, renta y egresos acumulados por tipo (gastos, comisiones, inversión, intereses, dividendos, alquileres), más los "complementos" (USDT General, Deuda). También tiene un cierre por mes y una fila de dividendos después de cada mes. | El dueño, **a mano** | Semanal o mensual | Cargado hasta el **28/06**. De julio en adelante solo están las fechas |
| Value CG, `Tenencia` | El reparto entre socios: aportes y % de cada uno, ganancia del mes, la parte de cada socio, el dividendo del 10% y el capital de cada socio | El dueño | Mensual | Hasta **junio** |
| Value CG, `Dashboard` | El tablero que ya existía: capital actual, ganancia promedio mensual y semanal, bruto y volumen promedio, renta sobre volumen y sobre capital, máximos y mínimos, las últimas 6 semanas y dos gráficos (pegados como imagen desde Google Sheets) | Fórmulas sobre Value CG | — | El "Capital Actual" apunta al **21/06** (Value CG!B36), no a la última fila cargada |
| Value CG, `Comisiones` (visible) y `Dante` (oculta) | Liquidación de comisiones por operación para los operadores externos Coco y Dante | El dueño | Mensual | `Comisiones` llega hasta junio. No entra en el cálculo del patrimonio |
| Value CG, ocultas `Value 2025`, `Value 2026`, `Vago`, `Liquidacion Seven` | Versiones viejas del histórico (una con 136 `#REF!`) y la composición de socios anterior | — | — | No usar: son historia |

**De dónde sale cada cosa.** El Registro General es "el cerebro": ahí están las operaciones, los pendientes y las
cuentas corrientes. Ese archivo no está en `datos/value/`. La Calculadora toma **solo los saldos por caja** de su cierre.
Por eso todo lo que sea clientes, operadores, spread o cheques en cartera no se puede contestar con estas planillas (ver
§8).

---

## 2. La actividad que hay detrás

Cambio General es una financiera y casa de cambio. Compra y vende USD billete y pesos, en efectivo y por transferencia.
También opera USDT, USD en cuentas del exterior (LLC, Grabify/Grabifi, Wise, Payoneer, PayPal), euros y reales. Además
hace recaudación, descuento de cheques y préstamos, y toma plata de inversores a los que les paga interés. Parte del
capital está en **inversiones**: Polígono, Almafuerte (comprada y vendida a 50.000 entre julio y agosto) y Carbox. Otra
parte figura como **garantías** (Millamapu, Charcas, Promar, Jeep, Gol Trend): en las hojas aparecen con +X y −X, así que
no suman al patrimonio.

- **Socios** (Tenencia): Manuel, Francisco y Jose, con 20.000 de aporte y 28,13% cada uno, y Alejo, con 11.111,11 y
  15,62%. En total, **71.111,11**. Alejo no figura entre los operadores: es un socio que no opera.
- **Operadores:** Manuel y Francisco (los principales), Jose, Dante, Coco y Vago. Coco y Dante cobran comisión por lo que
  operan (hojas `Comisiones` y `Dante`).
- **USDT General.** Es un negocio aparte del que Cambio General tiene **2/3 (≈ 66%)**. Sus resultados entran en el
  patrimonio como un **monto fijo escrito en la fórmula** de la fila USDT (`=10760+10900+4021+…`), no como una caja.
- **Costos de la estructura.** GASTOS (los costos fijos se pagan en general la primera semana del mes, entre 5.500 y
  9.000), COMISIONES (a operadores y colocadores), INTERESES (a inversores), INVERSIÓN (no está claro qué incluye) y
  DIVIDENDOS (a socios).
- **Ingresos aparte de la operación:** ALQUILERES (900 y 3.600 en junio).

---

## 3. El ciclo semanal

```
Registro General (Google Sheet, una pestaña por semana, operación por operación)
   │  Cierre semanal: se abren los pendientes, se pasan a cuenta corriente, cierra la hoja y abre la nueva
   ▼
Saldo de cada caja al cierre  ──(se pega como valores)──►  Calculadora Semanal, hoja nueva "DDMM - DDMM"
                                                            · se copia la hoja anterior
                                                            · se pegan las filas 2 y 3 de cada caja
                                                            · se escribe la cotización del dólar (C8) y la del euro (C9)
                                                            · se pegan Volumen Prom y Operaciones
                                                            · las fórmulas dan Neto y Ganancia
   ▼
Value CG: se anota a mano una fila por semana (CAPITAL = Neto, ganancia, bruto, volumen, egresos)
   │  Al cerrar el mes: ganancia del mes, fila "Dividendos" (lo que se repartió) y nuevo punto de partida
   ▼
Tenencia: ganancia del mes → parte de cada socio → dividendo del 10% → capital de cada socio
   ▼
Dashboard (hoja): promedios, máximos y mínimos, últimas 6 semanas
```

Algunas cosas del ciclo que importan para el dashboard:

- **La Calculadora es la única fuente al día.** El Value CG depende de que el dueño copie a mano y tiene 16 semanas de
  atraso. Un dashboard que lea solo el Value CG muestra la financiera de junio.
- **La semana doble** (10–23/08) tiene una sola hoja. Su ganancia (18.349,05) es de dos semanas: para compararla con las
  demás hay que dividirla por 2 (9.174,53 por semana).
- **El dueño ya pidió esto.** Desde el 22/06, todas las hojas semanales tienen escrito en K18/K19: *"UNIFICAR TODO EN UNA
  TABLA PARA IR HACIENDO SEMANA A SEMANA"*. El dashboard tiene que ser esa tabla única.
- **Cómo llegan las actualizaciones.** Esta vez la corrección vino como una hoja suelta en otro archivo, y eso rompió la
  fórmula que compara contra la semana anterior. Conviene recibir la Calculadora completa, igual que se pide para el
  Registro General.

---

## 4. Cómo se calcula la ganancia (verificado con fórmulas)

### 4.1 En la Calculadora, hoja de la semana *t*

| Línea | Fórmula (hoja 12–18/10) | Qué es |
|---|---|---|
| Dólares (B7) | `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)` | Cajas en USD: billete (cara chica, cambio, malos, USD), USDT y TRX, cuentas del exterior, más Almafuerte, Polígono, la columna AH sin encabezado y los egresos de la semana |
| Pesos (B8) | `=(SUM(E4:J4,M4))/C8` | Pesos en efectivo, cheques y transferencias divididos por **una sola cotización** (C8, escrita a mano: 1.535) |
| Euros (B9) | `=SUM(Y4+V4)*C9` | Euros y Wise a C9 (1,25) |
| Deuda (B12) | `4000` fijo | Una deuda a cobrar, fija desde el 11/05 (antes era 5.000) |
| USDT (B13) | `=10760+10900+4021[+15.855,49]` | La participación acumulada en USDT General, escrita a mano |
| Egresos (B14) | `=-SUM(AJ4:AN4)` | Gastos, comisiones, inversión, intereses y dividendos **de la semana**. Se restan porque ya estaban sumados en Dólares, así que en el Neto no pesan dos veces |
| **Neto** (B16) | `=SUM(B7:B15)` | **Patrimonio en USD** |
| **Ganancia Neta** (B17) | `=B16 - Neto de la hoja anterior` | Variación del patrimonio en la semana |
| **Bruto** (B18) | `=SUM(B7:B13,B15)` | El Neto más los egresos de la semana |
| **Ganancia Bruta** (B19) | `=B18 - Neto de la hoja anterior` | Lo que habría ganado la semana **antes de pagar** gastos, comisiones, intereses, inversión y dividendos (= Ganancia Neta + egresos) |

**Ejemplo, semana 12–18/10 (hoja corregida):**

| | USD |
|---|---|
| Dólares | 193.328,16 |
| Pesos (180.147.333 ARS / 1.535) | 117.359,83 |
| Euros | 4.149,77 |
| Deuda | 4.000,00 |
| USDT General | 41.536,49 |
| Egresos | −1.267,08 |
| **Neto** | **359.107,17** |
| Neto de 05–11/10 | 341.003,84 |
| **Ganancia Neta** | **18.103,33** (sin el ajuste USDT: 2.247,83) |
| **Ganancia Bruta** | **19.370,41** (sin el ajuste: 3.514,91) |

### 4.2 En el Value CG (la regla del dueño)

- **Ganancia de la semana = Neto(t) − Neto(t−1) + lo que se les pagó a los socios esa semana** (dividendos y
  liquidaciones). El Value CG lo resuelve restando el dividendo del capital del mes anterior. Por ejemplo, la fila 27
  "Dividendos" `=B26-4719` hace que la ganancia del 04–10/05 sea 9.874,55, mientras la Calculadora muestra 5.155,55,
  porque el dividendo pagado esa semana le baja el Neto. En marzo pasa lo mismo: se suman los 22.672 que salieron (6.450
  de dividendos y 16.222 de liquidación de socios salientes) y la semana del 16–22/03 da +18.247,23. La Calculadora, en
  cambio, da un Neto de 171.509,70.
- **Ganancia del mes = suma de sus semanas** (Value CG!E26 `=SUM(E21:E25)`).
- **Asignación de semanas partidas.** En los meses cargados, cada semana va al mes que tiene más días de esa semana: el
  23/02–01/03 va a febrero, y el 30/03–05/04 y el 27/04–03/05 van a abril. En cambio, las filas vacías que ya están
  armadas desde julio siguen la fecha del domingo, y con eso el 27/07–02/08 caería en agosto. En este informe uso **la
  mayoría de días**.
- **Bruto, Renta y P&L.** Bruto de la semana (H) = ganancia + gastos + inversión + intereses + dividendos + comisiones.
  Renta (J) = ganancia / volumen. P&L APORTE (C) = Neto − 71.111,11.

### 4.3 Qué es "ganancia" para esta planilla (y qué no)

Es **todo lo que cambió el patrimonio**: el resultado de la operación, la suba o baja del dólar sobre los pesos que hay,
los cambios de valor o de carga de inversiones, los ajustes de otros períodos (como el de USDT General) y los errores de
carga (por ejemplo, una cotización vieja). El dueño lo sabe y lo dice en la hoja *Semanales*: *"Es lo generado, no lo
'real'"*. El dashboard tiene que mostrar la ganancia **y** lo que la explica. Si muestra solo el número, alcanza con
**una sola semana rara** (+42.940 el 24–30/08) para que los promedios y el reparto de dividendos salgan mal.

---

## 5. Quién la consulta y qué decisiones se toman

**Quiénes.** La miran los cuatro socios, que no son analistas: el dueño que hace el cierre, los otros dos fundadores que
operan (Manuel/Francisco/Jose) y Alejo, que no opera y le interesa sobre todo su capital y su dividendo. La miran en el
cierre de cada semana y, sobre todo, en el **cierre de mes**, cuando se reparte.

| Decisión | Cada cuánto | Qué dato usa hoy | Regla que se ve en la planilla |
|---|---|---|---|
| **Cuánto dividendo repartir** | Mensual | Ganancia del mes (Tenencia, columna H) | **10% de la ganancia del mes** (el "Décimo": Tenencia!H8 `=H7/-10`; también el "Decimo" 6.441,90 del período jul-2025 a feb-2026). El resto se reinvierte |
| Cómo se reparte | Mensual | % de tenencia | 28,13% para Manuel, Jose y Francisco y 15,62% para Alejo (suman 99,99%). Alejo **no cobra en efectivo**: la columna Q dice "No" en abril, mayo y junio, y lo pagado coincide con 3 partes (4.719 ≈ 3 × 1.573,51; 2.510 ≈ 3 × 836,84; 924,16 ≈ 3 × 308,05). Su parte se descuenta del capital al mes siguiente (Tenencia!G11 `=258321.53-873`) |
| Cuánto capital tiene cada socio y cuánto pagarle si se va | Mensual o cuando pasa | Tenencia, columnas I–P | Capital del socio = el anterior + su % de la ganancia del mes − su dividendo. En marzo se liquidó a socios salientes por **16.222** |
| Si entrar o salir de una inversión (Polígono, Almafuerte) | Cuando se presenta | Columnas POLIGONO, AH, ALMAFUERTE | Se cargan al costo: la plata sale de una caja y entra en la columna de la inversión, así que el Neto no cambia |
| Si conviene seguir con una línea (USDT General, recaudación, cheques, alquileres) | Cuando se revisa | Fila USDT y egresos/ingresos por tipo | USDT General: 2/3 de cada liquidación |
| Cuánto gastar o recortar | Mensual | GASTOS, COMISIONES, INTERESES | Los costos fijos se pagan la primera semana del mes ("Pagamos costos fijos") |
| Cuántos pesos tener | Semanal | Pesos y cotización C8 | Todo se valúa con una sola cotización escrita a mano |
| Si los datos de la semana están bien | Semanal | CONTROL, notas | A mano y sin método fijo |

---

## 6. La foto actual (números de referencia verificados)

**Patrimonio (Neto)**

| Fecha | Neto | Fuente |
|---|---|---|
| 01/03/2026 | 167.896,05 (Value CG) / 167.944,79 (Calculadora 23/02–01/03) | Value CG!B14, Calculadora |
| 28/06/2026 (último en Value CG) | 265.889,35 | Value CG!B37 = hoja 22–28/06 |
| 18/10/2026 | **359.107,17** (con ajuste USDT) / 343.251,68 (hoja original) | Hoja corregida y archivo a |

**En qué está el patrimonio al 18/10** (hoja corregida):

| Bloque | USD | % |
|---|---|---|
| Polígono: columna POLIGONO 70.565,57 + columna AH sin encabezado 112.966 | 183.531,57 | 51,1% |
| Pesos (180,1 M ARS a 1.535): efectivo 89.989, transferencias 20.607, cheques 6.764 | 117.359,83 | 32,7% |
| Participación en USDT General | 41.536,49 | 11,6% |
| Cajas en USD, neto: billete 10.131, exterior 15.532, USDT/TRX −17.134 | 8.529,50 | 2,4% |
| Euros (euros + Wise, a 1,25) | 4.149,77 | 1,2% |
| Deuda a cobrar (fija) | 4.000,00 | 1,1% |

**Ganancia por mes** (ganancia neta según la regla del dueño; las semanas van al mes con más días)

| Mes | Semanas | Ganancia neta | Ganancia bruta | Gastos | Intereses | Comisiones | Fuente |
|---|---|---|---|---|---|---|---|
| Marzo | 4 | 35.702,58 | 47.981,27 | 6.433 | 4.752 | — | Value CG!F20 (incluye los 22.672 repartidos) |
| Abril | 5 | 52.366,61 (Tenencia: 55.936,97) | 71.150,27 | 9.048 | 5.652 (de esto, 3.573 era dividendo) | — | Value CG!E26; incluye +10.900 de USDT General |
| Mayo | 4 | 29.747,29 | 43.399,40 | 8.082 | 2.833 | 1.544 | Value CG!E32; incluye +4.021 de USDT General |
| Junio | 4 | 10.077,82 (Tenencia: 10.951,04) | 27.061,37 | 8.432 | 6.586 | 1.966 | Value CG!E38 |
| Julio | 5 | 20.552,55 | 35.454,81 | 8.099 | 5.964 | 839 | Calculadora (29/06–02/08); no está en Value CG |
| Agosto | 4 (3 hojas) | 58.721,65 | 71.941,22 | 7.967 | 2.028 | 225 | Calculadora; incluye +42.940 sin explicar y ≈ +18.400 de cheques |
| Septiembre | 4 | 442,61 | 11.721,01 | 9.273 | 1.350 | 655 | Calculadora (31/08–27/09) |
| Octubre (al 18/10) | 3 | −2.354,49 sin ajuste / **13.501,00 con ajuste USDT** | 10.849,90 | 8.531 | 4.290 | 383 | Calculadora (28/09–18/10) |

Las diferencias entre Value CG y Tenencia en abril y junio salen del manejo de los dividendos: el de marzo se pagó dentro
de INTERESES y la parte de Alejo se descuenta solo un mes. Las anoto porque **cambian el dividendo**. Las decide el SPEC.

**Últimas 7 semanas** (ganancia neta según la Calculadora, sin ajuste USDT):

| 31/08–06/09 | 07–13/09 | 14–20/09 | 21–27/09 | 28/09–04/10 | 05–11/10 | 12–18/10 |
|---|---|---|---|---|---|---|
| −5.067,21 | 3.857,56 | −276,20 | 1.928,46 | −718,63 | −3.883,70 | 2.247,83 |

Suman −1.911,88. La ganancia bruta suma 22.570,91 y los egresos 24.482,79.

**Socios (último cierre hecho: junio, Tenencia fila 14)**: Manuel, Jose y Francisco tienen 78.208,65 cada uno y Alejo
29.715,55, en total 264.329,57. El dividendo de junio fue de 1.095,10 (10% de 10.951,04): 308,05 para cada fundador y
171,06 para Alejo, que no se le pagó. Lo pagado fueron 924,16 (Value CG!T39), y ese pago no aparece en la columna
DIVIDENDOS de la Calculadora.

**Dividendos y retiros de 2026 que se ven en la planilla:**

| Semana | Monto | Detalle |
|---|---|---|
| 16–22/03 | 6.450 + 16.222 | Décimo de jul-2025 a feb-2026 y liquidación de socios salientes |
| 27/04–03/05 | 3.573 | 10% de marzo, cargado dentro de INTERESES |
| 04–10/05 | 4.719 | 10% de abril sin la parte de Alejo |
| 01–07/06 | 2.510 | 10% de mayo sin la parte de Alejo |
| Después de junio | 924,16 | No figura en ninguna hoja semanal |
| Julio, agosto y septiembre | — | Sin calcular |

---

## 7. Las preguntas que le haría un socio, por importancia

**Prioritarias (P1–P8):** el dashboard las tiene que responder sí o sí, a simple vista y sin abrir el Excel. Cada una
tiene una **respuesta esperada con los datos al 18/10/2026** para poder probar el dashboard con un usuario de prueba.
"¿Hoy se puede?" dice si la planilla original la responde **bien**, **a medias** o **no**, y por qué.

### P1 ⭐ — "¿Cuánto vale hoy la financiera y cuánto creció?"
- **Por qué importa.** Es el número que mira todo socio primero. Con él se calcula cuánto vale su parte y cuánto
  multiplicó lo que puso.
- **Dato que la responde.** El Neto (B16) de la última hoja semanal. Para el corte, la hoja corregida 12–18/10. Los
  aportes salen de Tenencia!C8.
- **Respuesta esperada.** **359.107,17 USD al 18/10/2026**, que son 343.251,68 sin el ajuste USDT General. Es **5,05
  veces los aportes** (71.111,11): +287.996 sobre lo aportado. Contra el 28/06, último dato del Value CG, subió +93.217,82.
- **¿Hoy se puede?** **Bien.** Hay dos reparos: el valor depende de la cotización escrita a mano (C8) y de que se use la
  hoja corregida. Con la vieja da 15.855,49 menos.

### P2 ⭐ — "¿Cuánto ganamos la última semana y cómo vienen las últimas semanas?"
- **Por qué importa.** Es el pulso del negocio. Un socio quiere saber si la semana fue buena, mala o normal.
- **Dato que la responde.** La Ganancia Neta (B17) y la Ganancia Bruta (B19) de cada hoja, más los dividendos pagados
  esa semana. La semana doble se divide por 2.
- **Respuesta esperada.** La semana del 12–18/10 dio **+18.103,33**, de los cuales **15.855,49 es el ajuste USDT
  General de mayo–septiembre**: la operación de la semana dejó **≈ 2.248**. Las 7 semanas desde el 31/08 suman
  **−1.912**, con 3 positivas y 4 negativas (detalle en §6).
- **¿Hoy se puede?** **Bien** semana por semana en la Calculadora, pero hay que saber tres cosas: la hoja corregida da
  `#REF!`; en las semanas con dividendos la Calculadora subestima la ganancia (por ejemplo, 04–10/05 da 5.155,55 y no
  9.874,55); y la del 16–22/03 compara bruto contra bruto.

### P3 ⭐ — "¿Cuánto ganamos en cada mes y cómo viene comparado con los anteriores?"
- **Por qué importa.** **El dividendo se calcula sobre la ganancia del mes**, y los meses alisan el efecto de los costos
  fijos, que se pagan una vez por mes.
- **Dato que la responde.** La suma de las semanas de cada mes más los dividendos o retiros. Hasta junio está en Value
  CG, columna E de las filas de mes. De julio en adelante sale de la Calculadora.
- **Respuesta esperada.** La tabla de §6: marzo 35.702,58 · abril 52.366,61 · mayo 29.747,29 · junio 10.077,82 · julio
  20.552,55 · agosto 58.721,65 · septiembre **442,61** · octubre, al 18/10 y con 3 semanas, −2.354,49, o 13.501,00 con
  el ajuste.
- **¿Hoy se puede?** **A medias.** De julio a octubre no hay cierre mensual. No está escrito a qué mes va cada semana
  partida. Y el dividendo de marzo pagado dentro de INTERESES y la parte de Alejo hacen que Value CG y Tenencia den
  distinto en abril (52.367 contra 55.937) y en junio (10.078 contra 10.951).

### P4 ⭐ — "¿Cuánto de esa ganancia es de la operación y cuánto son cosas extraordinarias?"
- **Por qué importa.** Repartir dividendos o decidir con una ganancia inflada por un ajuste de otros meses, o por un
  salto que nadie sabe explicar, es el error más caro que puede inducir el dashboard.
- **Dato que la responde.** Comparar caja por caja contra la semana anterior, más lo que se sabe de cada movimiento: la
  nota de la hoja corregida (I13:L24), las columnas de inversiones y la cotización.
- **Respuesta esperada.** Del 28/06 al 18/10 el Neto subió **+93.218**. De eso:
  - **+15.855,49** es el ajuste de USDT General, que es de mayo a septiembre pero cae todo en la semana del 12–18/10;
  - **+42.940,48** es la semana del 24–30/08, **sin explicación** (la caja de USD billete sube +39.566);
  - **≈ +18.400** son los cheques del 10–23/08: +28,1 M ARS que todavía no están aclarados;
  - **≈ +130** es el efecto neto de Almafuerte (vendida a 50.000) y de Polígono 20+13 (75.466).
  
  Sin esos movimientos quedan **≈ 16.000 en 16 semanas (≈ 1.000 por semana)**, contra ≈ 8.300 por semana en abril y ≈
  6.400 en mayo, ya sin USDT General. Lo mismo pasó antes: el +10.900 del 13–19/04 y el +4.021 del 25–31/05 también son
  USDT General cargado de golpe.
- **¿Hoy se puede?** **A medias o no.** La planilla no separa nada de esto: hay que mostrarlo con notas y con la
  comparación caja por caja.

### P5 ⭐ — "¿Cuánto le toca a cada socio y cuánto hay que repartir de dividendos?"
- **Por qué importa.** Es la decisión mensual que más le importa a cada socio, y la única que le importa a Alejo.
- **Dato que la responde.** La hoja Tenencia (ganancia del mes, %, el 10% y el capital de cada socio), más la regla de
  que Alejo no cobra en efectivo.
- **Respuesta esperada.** Al cierre de **junio**: Manuel, Jose y Francisco **78.208,65 cada uno** y Alejo
  **29.715,55**. El dividendo de junio fue de **1.095,10**: 308,05 para cada fundador y 171,06 para Alejo, que no se le
  pagó. **Julio, agosto y septiembre no están repartidos.** Si se aplicara la regla, julio daría ≈ 2.055 (10% de
  20.552,55), pero agosto incluye el +42.940 sin explicar (ver P4).
- **¿Hoy se puede?** **A medias.** La Tenencia llega a junio, la regla de Alejo no está escrita en ningún lado y su parte
  impaga no se acumula (ver §9).

### P6 ⭐ — "¿Dónde está la plata? ¿Cuánto está disponible y cuánto está inmovilizado?"
- **Por qué importa.** Que la financiera valga 359.000 no quiere decir que tenga 359.000 para operar. Esto define si se
  puede pagar un dividendo, devolverle a un inversor o entrar en otra inversión.
- **Dato que la responde.** La fila 4 de la última hoja, agrupada por tipo de caja.
- **Respuesta esperada.** Al 18/10:
  - **Polígono 183.531,57 (51%)**: 70.565,57 en la columna POLIGONO y 112.966 en una columna sin encabezado;
  - **pesos 117.359,83 (33%)**: 180,1 M ARS;
  - **USDT General 41.536,49 (12%)**;
  - **cajas en USD netas 8.529,50 (2%)**: la caja de USD billete está en −7.229 y la de USDT en −18.868;
  - **euros 4.149,77** y **deuda a cobrar 4.000**.
- **¿Hoy se puede?** **A medias.** Hay etiquetas del bloque que apuntan a otra columna ("Poligono 09" lee GOL TREND y
  "Almafuerte" lee JEEP, las dos en 0). La columna AH, la segunda parte de Polígono, no tiene encabezado. Y las garantías
  entran y salen con +X y −X.

### P7 ⭐ — "¿La operación cubre los costos? ¿Cuánto gastamos por mes?"
- **Por qué importa.** Sirve para decidir si recortar, si subir comisiones o márgenes, o si una línea deja de convenir.
- **Dato que la responde.** Las columnas GASTOS, COMISIONES, INTERESES, INVERSIÓN y DIVIDENDOS de cada semana, más la
  Ganancia Bruta.
- **Respuesta esperada.** Los gastos están estables en **≈ 8.000–9.300 por mes desde abril** (septiembre 9.273). En
  **septiembre**, la ganancia bruta fue de 11.721 y los egresos de 11.278 (gastos 9.273, intereses 1.350 y comisiones
  655), con lo que la neta quedó en **443**. En las 7 semanas desde el 31/08, la bruta suma **22.571** y los egresos
  **24.483**.
- **¿Hoy se puede?** **Bien** para los totales por tipo, que ya están en USD. **No** para el detalle de qué gasto es cada
  uno: eso está en el Registro General.

### P8 ⭐ — "¿Cuánto nos pega el dólar? ¿Cuántos pesos tenemos expuestos?"
- **Por qué importa.** Un tercio del patrimonio está en pesos. Una suba del dólar baja el Neto y parece una pérdida de la
  operación.
- **Dato que la responde.** El total de pesos (E4:J4 + M4), la cotización C8 de cada hoja y la diferencia entre semanas.
- **Respuesta esperada.** Al 18/10 hay **180,1 M ARS (≈ 117.360 USD a 1.535)**. **Cada 10 pesos de suba del dólar son
  ≈ −760 USD.** Desde abril, el efecto de la cotización sobre los pesos que había en cada momento acumula **≈ −14.700**
  (la cotización fue de 1.380 a 1.535).
- **¿Hoy se puede?** **A medias.** C8 se escribe a mano y quedó igual varias semanas: 1.525 del 20/07 al 23/08 y 1.490
  durante tres hojas en junio y julio. Así, una parte de la "ganancia" de una semana puede ser una cotización vieja.

### Resto de las preguntas (importantes, no bloqueantes)

| # | Pregunta | Por qué importa | Dato | Respuesta con los datos actuales | ¿Hoy se puede? |
|---|---|---|---|---|---|
| P9 | "¿Cuánto volumen movimos y cuánto ganamos por cada 100 USD operados?" | Dice si el negocio cae por menos clientes o por menos margen | Volumen Prom (B21, pegado del Registro General) y ganancia | En 12–18/10 el volumen fue de 394.063, con margen neto de 0,57% y bruto de 0,89%. **El volumen no se cayó** (septiembre 1,71 M contra junio 1,73 M), pero **el margen bruto sí** (septiembre 0,68% contra abril 2,96%) | A medias: el volumen se pega a mano y "Operaciones" está **congelado en 338** desde el 20/07 |
| P10 | "¿Cuánto rinde USDT General? ¿Conviene seguir?" | Es el 12% del patrimonio y se carga de golpe | Fila USDT (B13) y la nota de la hoja corregida | Acumulado 41.536,49 = 10.760 (antes de feb) + 10.900 (13–19/04) + 4.021 (25–31/05) + 15.855,49 (12–18/10). Lo último son 2/3 de 6 liquidaciones de mayo a septiembre (el negocio entero ganó ≈ 23.783) | A medias: no se sabe de qué mes es cada liquidación ni si el 4.021 se superpone con mayo |
| P11 | "¿Cuánto tenemos puesto en Polígono y cuánto pusimos últimamente?" | Es la mitad del patrimonio, valuada a lo pagado | POLIGONO, POLIGONO 20+13 y columna AH | 7.412 (08–14/06) → 67.607 (15–21/06) → 69.886 (20–26/07) → 145.352 (10–23/08, +75.466) → 146.032 (14–20/09) → **183.532** (05–11/10, +37.500 en la columna sin encabezado). Almafuerte: 50.000 del 13/07 al 09/08 | A medias: columna sin encabezado y etiquetas corridas |
| P12 | "¿Cuánto ganamos en el año?" | Para el balance anual y para el ánimo de los socios | Neto y retiros | Del 01/03 al 18/10, el Neto más los dividendos y retiros registrados dan **≈ 221.112**, o **≈ 224.685** si se suma el dividendo de 3.573 pagado dentro de INTERESES | A medias: depende de cómo se traten los dividendos y el ajuste USDT |
| P13 | "¿Cuál fue la mejor y la peor semana, y por qué?" | Para entender qué hace una semana buena | Ganancia semanal y notas | La mejor fue el 24–30/08 con +42.940,48, **sin explicación**. La peor, el 31/08–06/09 con −5.067,21: semana de costos fijos, con 8.972 de gastos. El Dashboard viejo marca como "máxima semanal" 37.660,15, que en realidad son 7 meses (jul-2025 a feb-2026) | A medias: las notas de *Semanales* llegan al 14/06 |
| P14 | "¿Cuánto rinde el capital?" | Para comparar contra otras inversiones | Ganancia del mes / Neto al inicio | Abril 28,94%, mayo 13,01%, junio 3,94% (Value CG, columna F), septiembre 0,13% (443 / 345.164). El "27,82% mensual promedio" del Dashboard está inflado por los primeros meses | Bien, con la definición escrita |
| P15 | "¿Están bien cargados los números de esta semana?" | Para no decidir sobre un error | Cotización, referencias a la hoja anterior, columnas sin encabezado, constantes | Hoy: `#REF!` en la hoja corregida, cotización repetida, Operaciones = 338, "Deuda" fija en 4.000 desde mayo, etiquetas corridas | A medias: no hay control sistemático |
| P16 | "¿Cuánto pagamos de intereses a inversores?" | Es el costo de la plata de terceros | INTERESES | Septiembre 1.350 y octubre (3 semanas) 4.290; junio 6.586 | A medias: el capital de los inversores **no está** en estas planillas |
| P17 | "¿Qué garantías tenemos tomadas?" | Riesgo y respaldo de préstamos | MILLAMAPU, CHARCAS, PROMAR, JEEP, GOL TREND | Aparecen con +X y −X (Millamapu 200.000/−200.000, Charcas 40.000/−40.000, Promar 87 M/−87 M), así que suman 0 | A medias: la unidad es dudosa y no suman al Neto, como corresponde |
| P18 | "¿Cuánto mueve y cuánto deja cada operador?" | Comisiones y quién sostiene el negocio | `Volumen Mayo`, `Comisiones`, `Dante` | Solo hay mayo para Manuel (1,61 M Debe + Haber) y Francisco (1,17 M), y las liquidaciones de Coco y Dante | **No**: hace falta el Registro General |

---

## 8. Qué no responden estas planillas

Lo siguiente está en el Registro General, y en parte en su tablero v2, que **no muestra ganancia**. Este dashboard no
lo puede contestar con `datos/value/`: clientes (ranking, altas, bajas), resultado por operador, spread por producto,
cheques en cartera, pendientes y cuentas corrientes, capital de cada inversor y detalle de cada gasto. Si alguien lo
pregunta, el dashboard tiene que decir dónde mirarlo, y no inventarlo.

---

## 9. Preguntas para el dueño (supuestos que el SPEC tiene que decidir)

1. **Ajuste USDT General (15.855,49).** ¿A qué mes va cada una de las 6 liquidaciones? ¿El +4.021 del 25–31/05 ya era
   parte de mayo? *Supuesto razonable:* mostrarlo aparte como "ajuste de períodos anteriores" y no mezclarlo con la
   ganancia de octubre.
2. **+42.940 (24–30/08) y ≈ +18.400 de cheques (10–23/08).** ¿Son ganancia real o carga? Mientras no se aclaren, el
   dashboard los tiene que marcar como "sin explicar".
3. **Dividendos de junio a septiembre.** ¿Se pagaron los 924,16 de junio? ¿Desde qué caja? ¿Se aplica el 10% a julio,
   agosto y septiembre?
4. **La parte de Alejo ("No").** ¿Se acumula como deuda con él? La Tenencia descuenta solo la del mes anterior: en junio
   resta 464,68 y no los 873 de abril, y por eso la ganancia de junio difiere en 873 entre Tenencia y Value CG.
5. **Semanas partidas.** ¿Van al mes con más días, que es como se cargaron febrero a junio, o al mes del domingo, como
   están armadas las filas vacías?
6. **Columna AH sin encabezado (112.966).** ¿Es Polígono 20+13? ¿El +37.500 del 05–11/10 es una cuota nueva? ¿Polígono
   se valúa a lo pagado?
7. **"Deuda" de 4.000.** ¿Sigue vigente? Está fija desde el 11/05.
8. **INVERSIÓN como egreso.** ¿Qué incluye? Acumula 34.103 a junio.
9. **Cotización C8.** ¿Qué dólar se usa (compra, venta o el promedio operado de la semana)? ¿Conviene sacarlo del
   Registro General en vez de escribirlo a mano?
10. **Filas 2 y 3 de cada caja.** Por las garantías (+X en una y −X en la otra), parecen ser "lo que hay" y "lo
    pendiente o en cuenta corriente", y el Neto usa la suma. Si se confirma, eso responde la duda que deja abierta
    `docs/contexto_negocio.md`: el patrimonio de la Calculadora **incluye los pendientes**.
