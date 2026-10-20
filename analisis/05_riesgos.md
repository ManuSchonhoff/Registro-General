# 05 — Riesgos: cómo un dashboard sobre estos datos puede inducir a error

Rol: escéptico. Este informe lista las formas en que un tablero armado con la Calculadora Semanal y el Value CG
puede mostrar algo que no es cierto, cuantifica cada una con los datos de la planilla y propone cómo mitigarla en la
interfaz. Los riesgos están ordenados por gravedad: primero los que pueden cambiar la conclusión principal ("¿ganamos
plata?, ¿cuánto?, ¿vamos mejor o peor?").

**Fuentes.** `datos/value/2026-10-20a_Calculo_Semanal.xlsx` (33 hojas semanales, de `2302 - 0103` a `1210 - 1810`),
`2026-10-20b_Calculo_Semanal_1210-1810.xlsx` (reemplaza la última hoja) y `2026-10-20_Value_CG_2026.xlsx`. No se
modificó ningún archivo.

**Cómo se calcularon los números.**
- *Neto* de cada hoja = el que guarda la planilla, recalculado con `value/leer.py` (evalúa la fórmula del bloque como
  suma de cajas; coincide con lo guardado en las 33 hojas). Para `1210 - 1810` se usa el archivo `b`: Neto 359.107,17.
- *Ganancia de la semana* = Neto de la hoja − Neto de la hoja anterior (lo mismo que hace la fila "Ganancia Neta"
  desde fines de marzo). Hay 32 variaciones, de `0203 - 0803` a `1210 - 1810`: 231 días (33 semanas, porque
  `1008 - 2308` vale por dos).
- *Fila 2 / fila 3*: las dos filas que se pegan por caja arriba de la hoja; `value/leer.py` las llama "saldo" y
  "pendiente". La fila de sumas (4 o 5) es fila 2 + fila 3.
- *Efecto cambiario estimado* de una semana = posición en pesos de la semana anterior (PESOS + TRANSFER + CHEQUES +
  RECAUDACION BX, filas 2+3) × (1/cotización nueva − 1/cotización anterior). Es una aproximación: no ve los movimientos
  dentro de la semana.
- Montos en USD salvo que se diga ARS o EUR. Punto de miles, coma decimal.

---

## Resumen

| # | Riesgo | Gravedad | Cuánto mueve (dato real) | Mitigación principal |
|---|---|---|---|---|
| 1 | Ajuste de USDT General acumulado cargado en una sola semana | Crítica | 15.855,49 = 87,6 % de la ganancia de 12–18/10 (18.103,33). Antes: +10.900 (73 % de 13–19/04) y +4.021 (67 % de 25–31/05) | Serie aparte "Participación USDT General"; fuera de la ganancia semanal por defecto |
| 2 | Saltos de ganancia sin explicar | Crítica | 24–30/08: +42.940 (22,5 % de toda la ganancia desde marzo). 10–23/08: +18.349, casi todo por cheques pendientes (+18.361) | Marca "sin explicar"; la tendencia se muestra con y sin estas semanas |
| 3 | El Neto es la resta de dos números enormes (saldos y pendientes) y el signo de los pendientes no está confirmado | Crítica | Fila 2 y fila 3 se mueven ±100.000–500.000 por semana en sentido contrario; la ganancia típica es ±5.000 | Descomponer la ganancia en saldos vs. pendientes; alerta de saltos; nada de decimales |
| 4 | Más de la mitad del Neto no es plata disponible | Crítica | Al 18/10: inversiones a costo 183.532 (51 %) + constantes a mano 45.536 (13 %). El renglón "Dólares" (193.328) tiene solo 8.530 líquidos | Patrimonio apilado por naturaleza; nunca mostrar "Dólares" del bloque |
| 5 | El criterio del Neto cambió en el tiempo (columnas que entran y salen, etiquetas corridas, euros) | Alta | Polígono entra en 08–14/06 (+7.412; otra versión de esa semana da 704); WISE pasa de 1:1 a ×1,25 y el euro de 1,2 a 1,25 (+1.716 en 25–31/05) | Recalcular con un criterio fijo y documentado; anotaciones en el gráfico |
| 6 | Retiros de socios tratados como pérdida, y dividendos cargados como intereses | Alta | 34.398 de retiros bajaron el Neto (dividendos 18.176 + liquidación de un ex socio 16.222). 16–22/03 tiene cuatro "ganancias" distintas: −4.425, −5.353, 17.319 y 18.247 | Métrica principal "ganancia antes de retiros"; retiros en barra aparte |
| 7 | Efecto del tipo de cambio mezclado con la ganancia, y cotización cargada a mano | Alta | Efecto cambiario estimado −12.318 desde marzo. Hoy, 10 pesos de cotización = ±765 (34 % de la ganancia operativa de la última semana) | Barra separada "efecto dólar"; mostrar la cotización usada y marcar las repetidas |
| 8 | Semana doble y meses de 4 y de 5 semanas | Alta | `1008 - 2308` son 14 días. "Abril" del Value CG tiene 5 semanas: 52.367 contra 29.747 de mayo (4) | Normalizar a "por semana de 7 días"; mostrar cuántas semanas tiene cada mes |
| 9 | Fuentes desactualizadas o que no coinciden | Alta | Value CG llega al 28/06 (15 hojas sin pasar); su Dashboard dice capital 266.648 al 21/06, contra 359.107 al 18/10. Dos versiones de 12–18/10 (343.252 y 359.107), una con #REF! | Una sola fuente (la Calculadora, última versión de cada hoja); cartel "datos al 18/10" |
| 10 | KPIs heredados del Dashboard del Value CG mal armados | Media | "Ganancia prom. semanal" 10.339 incluye dos períodos de varios meses (sin ellos: 8.192); "máx. semanal" 37.660 no es una semana; "mín. mensual" 28.122 no es un mes | No copiarlos: recalcular desde la tabla semanal, con N y período a la vista |
| 11 | Cheques a valor nominal y cambio fuerte de composición | Media | En 23–29/03 los cheques eran el 94 % del Neto (170.767 de 180.927); hoy el 1,9 % (6.764) | Mostrar la composición en el tiempo; rotular "cheques a valor nominal" |
| 12 | Volumen, operaciones y renta sobre volumen con datos copiados | Media | "Operaciones" = 338 en 12 hojas seguidas (20/07–18/10); volumen de 10/05 = 499.476 en la Calculadora y 686.864 en el Value CG | No mostrar operaciones ni ticket; renta sobre volumen solo con volumen del Registro |
| 13 | Porcentajes sobre aportes o sobre una base chica | Media | "Ganancia sobre aportes" 274,97 %; en el Value CG un error de fórmula le suma 69.985 al P&L de 15/02–01/03 | Montos en USD primero; % solo sobre patrimonio promedio del período |
| 14 | Gastos fijos de principio de mes que generan semanas negativas | Media | 6 de las 10 semanas negativas son semanas con gastos de 5.700 a 9.000 | Media móvil de 4 semanas; marca "semana de costos fijos" |
| 15 | Períodos incompletos y carga retroactiva | Media | Octubre tiene 3 hojas (13.501, que sin el ajuste USDT son −2.354); ago–oct se completó toda junta en octubre | Barra rayada "parcial"; indicador de calidad de carga por semana |
| 16 | Reparto por socio no es Neto × % | Baja | 28,13 % × 3 + 15,62 % = 100,01 %; en junio la Tenencia da 78.209 por socio principal, no 28,13 % × 264.330 = 74.356 | Vista por socio solo desde Tenencia, con fecha de actualización |
| 17 | Saldos que no se mueven, unidades dudosas y valuaciones a la par | Baja | TRX 1.734 idéntico en 26 hojas; LLC 6.144 igual 11 hojas y a 0 en la última; PROMAR 87.000.000 rotulado USD | Panel "saldos sin movimiento"; validar moneda; garantías con control fila 2 + fila 3 = 0 |
| 18 | Errores de fórmula latentes y notas que contradicen la fórmula | Baja | Hoy en cero, pero USD BsAs y DEUDA USD se dividen por la cotización; alquiler 3.600 con nota "NO CONTAR" que igual suma | Chequeos automáticos al actualizar |
| 19 | Nombres que se leen al revés | Baja | "Deuda" +4.000 es plata que nos deben; "BRUTO" del Value CG es acumulado (468.691), no un saldo; "INVERSION" es un egreso | Glosario y renombrar en la interfaz |

**La conclusión que más depende de estos riesgos.** Con la ganancia tal como sale de la planilla, marzo–junio y
julio–octubre se ven iguales: 5.761 y 5.826 por semana. Si se sacan los ajustes a mano, se suman los retiros y se
saca el efecto del dólar (anexo), queda 7.335 por semana en marzo–junio y 5.106 en julio–octubre. Si además las dos
semanas sin explicar de agosto no son ganancia del negocio, julio–octubre baja a **1.527 por semana**. La diferencia
entre "estamos igual" y "ganamos cinco veces menos" está en tres semanas. El dashboard no puede esconder eso.

---

## 1. Ajuste de USDT General acumulado cargado en una sola semana — Crítica

**Qué pasa.** La fila "USDT" del bloque de cálculo no es la caja USDT: es una constante escrita a mano que representa
la parte de Cambio General (2/3) en las ganancias de USDT General. Se actualiza cada tanto y todo el acumulado cae en
la semana en que se escribe.

**Evidencia.**

| Hoja | Fórmula de la fila USDT | Salto | Ganancia de la semana | Peso del salto |
|---|---|---|---|---|
| `1304 - 1904` | `=10760+10900` | +10.900 | 14.902,51 | 73,1 % |
| `2505 - 3105` | `=10760+10900+4021` | +4.021 | 5.992,47 | 67,1 % |
| `1210 - 1810` (archivo b) | `=…+1608.48+1608.48+994.02+…+2121.373333` | +15.855,49 | 18.103,33 | 87,6 % |

- El ajuste de octubre suma seis liquidaciones de mayo a septiembre (I15:J21 de la hoja: 1.608,48, 994,02, 1.237,97,
  1.983,67 y 1.042,92, dos veces cada una, más `=3182.06/3*2` = 2.121,37). Sin el ajuste, la semana 12–18/10 ganó
  2.247,83 (lo que dice el archivo a).
- La línea USDT vale hoy 41.536,49: el 11,6 % del Neto. Entre un ajuste y otro no se mueve, así que la ganancia de
  USDT General aparece como cero durante meses y después de golpe.
- **Posible doble conteo, a confirmar.** La nota de la hoja dice "Es ganancia repartida". Si esas liquidaciones se
  cobraron y entraron a alguna caja de Cambio General, ya están en el Neto y sumarlas en la fila USDT las cuenta dos
  veces. Tampoco está claro si los 4.021 de fines de mayo se superponen con la primera liquidación "desde mayo" de la
  lista nueva.

**Por qué engaña.** Un gráfico semanal muestra un pico en octubre que no pasó en octubre, y un hueco de mayo a
septiembre. Un "promedio de las últimas 4 semanas" sube 3.964 por semana nada más que por esto.

**Mitigación en la interfaz.**
- **Separar:** serie propia "Participación en USDT General (2/3)", en otro color, fuera de la ganancia semanal del
  negocio. Por defecto el gráfico de ganancia **la excluye**, con un interruptor "incluir ajustes".
- **Reasignar** cuando se sepa la fecha de cada liquidación (lista en `config.json`, no en el código), repartiendo
  cada una en su mes. Mientras no se sepa, la barra de octubre lleva la nota "incluye 15.855 generados entre mayo y
  septiembre".
- **Advertencia** en la tarjeta de patrimonio: "41.536 de USDT General son un valor escrito a mano, no un saldo de caja".

## 2. Saltos de ganancia sin explicar — Crítica

**Qué pasa.** Dos semanas de agosto explican casi un tercio de toda la ganancia desde marzo, y ninguna tiene una
operación que la justifique en la Calculadora.

**Evidencia.**
- **24–30/08 (`2408 - 3008`): +42.940,48.** Es el 22,5 % de la ganancia de todo el período (191.162). Casi todo sale
  de los pendientes en dólares: la fila 3 de la caja USD pasa de −45.347 a +14.119 (+59.466), mientras la fila 2 baja
  19.900. No hay ajuste ni inversión que lo explique. Su "renta sobre volumen" da 12,9 %, contra −1 % a 3 % en las
  demás semanas con dato.
- **10–23/08 (`1008 - 2308 (Dos Semanas)`): +18.349,05.** El pendiente de CHEQUES pasa de −27,2 M a +0,8 M ARS
  (+18.361 a 1.525), casi exactamente la ganancia de las dos semanas. En la misma hoja sale Almafuerte (50.000) y
  entra Polígono 20+13 (75.466), y la caja PESOS baja 40.049 en la fila 2 mientras el pendiente de TRANSFER sube
  18.963.
- Las cuatro mejores semanas (24–30/08, 20–26/04, 10–23/08, 12–18/10) suman 97.857: el **51,2 %** de la ganancia
  del período. Tres de ellas tienen una explicación pendiente o un ajuste a mano.
- Las hojas de agosto a octubre se completaron todas juntas en octubre (lo dijo el dueño): es esperable que haya
  pendientes mal cerrados o arrastrados.

**Por qué engaña.** Con estas semanas, julio–octubre gana lo mismo que marzo–junio. Sin ellas, la ganancia semanal
"limpia" cae de 7.335 a 1.527 (ver el resumen y el anexo). Un promedio, un total o una tendencia que las incluya sin
marca da la conclusión opuesta a la que daría si fueran errores de carga.

**Mitigación en la interfaz.**
- **Marcar** esas semanas con un ícono "sin explicar" y un texto al pasar el mouse con lo que se sabe (qué caja se
  movió y cuánto). La marca se saca solo cuando el dueño anota la explicación (campo de notas por semana en la
  configuración).
- En las tarjetas de promedio y tendencia, **mostrar las dos cifras**: "con todas las semanas" y "sin semanas sin
  explicar".
- Usar **mediana** al lado del promedio: la mediana por hoja es 5.039; el promedio, 5.974.
- Tabla "Semanas que más pesan": las 5 que más aportan, con su % del total.

## 3. El Neto es la resta de dos números enormes, y el signo de los pendientes no está confirmado — Crítica

**Qué pasa.** Por cada caja se pegan dos filas a mano: la 2 ("saldo") y la 3 ("pendientes"), que salen del cierre del
Registro General. El Neto las suma. En muchas semanas las dos filas se mueven en sentido contrario por cientos de miles,
y la ganancia es la diferencia chiquita que queda.

**Evidencia.**
- En `0405 - 1005`, las cajas en dólares (USD, USDT, cuentas del exterior) aportan +453.537 por la fila 2 y −502.526
  por la fila 3. La ganancia de esa semana fue 5.156.
- La variación semanal de lo que aportan los pendientes (sin inversiones) va de −229.841 (`0405 - 1005`) a +189.068
  (`1105 - 1705`), y hasta +298.921 en `0806 - 1406`: esa semana aparece el pendiente del Polígono en su columna
  (−261.592) y el pendiente de la caja USD sube 253.702. Parece una reclasificación, pero no se puede confirmar sin el
  Registro.
- `config.json` dice `"signo_pendientes_confirmado": false` y `docs/contexto_negocio.md` deja abierta la pregunta de
  si los pendientes positivos son deudas con terceros. La hoja `CONTROL` muestra que dos pegados de la misma semana
  difieren en +100.000 y −300.000 ARS en PESOS (el −200.000 recurrente que también aparece en el Registro).
- El chequeo del Registro (contexto) reporta 41 pendientes de USDT General con "?" de más de 4 semanas, imputaciones
  con signo invertido y filas canceladas con imputación. Todo eso entra al Neto a través de la fila 3.

**Por qué engaña.** Un error del 1 % en la fila 3 de una sola semana (≈ 3.000–5.000) es tan grande como la ganancia
de una semana normal. El tablero va a mostrar el patrimonio con una precisión que el dato no tiene, y una ganancia
semanal que puede ser ruido de carga.

**Mitigación en la interfaz.**
- **Descomponer** la ganancia de cada semana en "movimiento de saldos" y "movimiento de pendientes" (al pasar el
  mouse o en el detalle de la semana). Si los pendientes explican más de la mitad, la semana se marca.
- **Alerta** cuando la fila 3 de una caja cambia más de un umbral configurable (por ejemplo, 20.000) de una semana a
  la otra.
- **Redondear** patrimonio y ganancias a miles en las tarjetas (sin decimales). El detalle exacto queda en la tabla.
- **Nota al pie fija** mientras no se confirme el signo: "Los pendientes se suman tal como vienen del Registro; su
  signo está a confirmar".

## 4. Más de la mitad del Neto no es plata disponible — Crítica

**Qué pasa.** El Neto suma cajas líquidas, pendientes, inversiones valuadas a lo que costaron y dos constantes
escritas a mano. Además, el renglón "Dólares" del bloque mete adentro las inversiones.

**Evidencia (al 18/10, Neto 359.107,17).**

| Componente | USD | % del Neto |
|---|---|---|
| Saldos de cajas (fila 2, sin inversiones) | 138.001 | 38,4 % |
| Pendientes netos (fila 3, sin inversiones) | −7.961 | −2,2 % |
| Inversiones a costo: Polígono (332.157,57 − 261.592 de pendiente = 70.565,57) + columna AH sin encabezado (112.966) | 183.532 | 51,1 % |
| Constantes a mano: USDT General (41.536,49) + "Deuda" (4.000) | 45.536 | 12,7 % |

- El renglón "Dólares" (B7 = 193.328,16) suma `AG4:AN4`, que incluye Almafuerte, la columna AH, Polígono y las
  columnas de egresos. Plata líquida en dólares ahí adentro: **8.529,51** (caja chica + USD billete + USDT + cuentas
  del exterior). El resto son 183.531,57 de inversiones y 1.267,08 de egresos que el bloque resta después.
- La columna AH (112.966) **no tiene encabezado** desde `2408 - 3008` (antes decía "POLIGONO 20+13"). Un lector que
  arme las cajas por nombre la pierde, y el Neto deja de cerrar por 112.966 (31 %).
- La caja USDT está en −18.867,90 (debemos USDT) y la fila "USDT" del bloque vale +41.536,49: dos cosas distintas con
  el mismo nombre.

**Por qué engaña.** "Patrimonio 359.107" se lee como "tenemos 359.107". Una tarjeta "Dólares 193.328" se lee como
liquidez. Las inversiones a costo no cambian de valor nunca, lo que también hace que el patrimonio parezca más estable
de lo que es.

**Mitigación en la interfaz.**
- **Patrimonio apilado** por naturaleza: líquido, pendientes, inversiones a costo y ajustes a mano. La tarjeta
  principal dice "Patrimonio contable" y debajo "de los cuales líquidos: X".
- **No mostrar** nunca los renglones del bloque ("Dólares", "Pesos", "Euros", "Poligono 09", "Almafuerte") como tales:
  recalcular desde las cajas con un mapeo caja → grupo.
- **Rotular** las inversiones "a costo, no a valor de mercado" y mostrar la columna AH como "Inversión sin nombre
  (columna AH)" con advertencia hasta que el dueño le ponga nombre.
- Renombrar la fila USDT del bloque como "Participación USDT General (valor a mano)".

## 5. El criterio del Neto cambió en el tiempo — Alta

**Qué pasa.** Las fórmulas del bloque se reescribieron muchas veces: columnas que entran y salen, rangos que se corren,
etiquetas que quedaron apuntando a otra columna. La serie de Neto no se armó siempre con la misma regla.

**Evidencia.**
- **Polígono** entra al Neto en `0806 - 1406` con 7.412,22 (pago de 10.525.348,57 ARS convertido a 1.420, con la nota
  "Nos debe el Polígono"). Esa semana tiene dos versiones: la hoja `Semanales` da 254.204,96 y +704,03 (sin Polígono);
  la Calculadora y el Value CG, 261.617,18 y +8.116,25. Diferencia: 7.412,22. La semana siguiente pasa a 67.607,33.
- **Almafuerte** entra en `1307 - 1907` (50.000) y sale en `1008 - 2308`; **Polígono 20+13** entra en `1008 - 2308`
  (75.466); la columna AH sube 37.500 en `0510 - 1110`. Si la plata salió de caja la misma semana, el efecto es
  neutro, pero eso no se puede verificar sin el Registro.
- **Euros:** hasta `1805 - 2405` WISE (en euros) se sumaba a "Dólares" a 1:1. Desde `2505 - 3105` pasa al renglón
  Euros a ×1,25, y el factor de EUROS sube de 1,2 a 1,25. Efecto sobre esa semana: 3.406,69 EUR × 0,25 + 17.280 EUR ×
  0,05 ≈ **1.716**. Con el ajuste USDT de esa semana (+4.021), el 95,7 % de los 5.992,47 son cambios hechos a mano.
- **Etiquetas corridas:** desde `2707 - 0208`, "Poligono 09" (B10 = AD4) apunta a GOL TREND y "Almafuerte"
  (B11 = AC4) a JEEP. El Almafuerte y el Polígono verdaderos están adentro de "Dólares". En `2707 - 0208` y
  `0308 - 0908` el bloque muestra "Almafuerte 0" cuando Almafuerte valía 50.000. JEEP (12.000/−12.000) y GOL TREND
  (5.000/−5.000) pasaban por esas etiquetas, neutralizados.
- **REALES** nunca entra al Neto (máximo 1.114 BRL ≈ 232 USD).
- **Celdas "Ganancia" de las primeras hojas:** en `0903 - 1503` es Bruto menos Neto anterior (9.633,75); en
  `1603 - 2203`, Bruto menos Bruto anterior (−5.353,06). Recién desde `2303 - 2903` es Neto menos Neto.

**Por qué engaña.** Una línea de patrimonio continua sugiere que cada punto se midió igual. Cada cambio de criterio
mete un escalón que parece ganancia o pérdida.

**Mitigación en la interfaz.**
- **Recalcular** el Neto desde las cajas con un mapeo fijo y documentado (caja → grupo → moneda → entra o no entra) y
  mostrar al lado el "Neto según la planilla". Si difieren, se ve la diferencia y su motivo.
- **Anotaciones** sobre el gráfico de patrimonio en las semanas de cambio ("entra Polígono", "WISE pasa a euros",
  "sale Almafuerte").
- **Nunca leer las etiquetas del bloque.** Leer siempre las cajas por columna y encabezado, con un chequeo que avise si
  aparece una columna con números y sin encabezado.
- Recalcular la ganancia de todas las semanas como Neto menos Neto anterior, sin usar las celdas "Ganancia" guardadas.

## 6. Retiros de socios tratados como pérdida, y dividendos cargados como intereses — Alta

**Qué pasa.** Cuando se pagan dividendos o se liquida a un socio, la plata sale de caja y el Neto baja. Eso no es una
pérdida del negocio. La Calculadora lo trata de tres formas distintas y el Value CG lo corrige solo a veces.

**Evidencia.**
- **Columna DIVIDENDOS de la Calculadora** (resta del Neto): 4.719 en `0405 - 1005` y 2.510 en `0106 - 0706`. El
  Value CG los devuelve con sus filas "Dividendos" (B27 = B26 − 4.719): ganancia 9.874,55 contra 5.155,55 de la
  Calculadora, y −2.310,60 contra −4.820,60.
- **Dividendos cargados en INTERESES:** en `2704 - 0305` INTERESES = 5.152, de los cuales el Value CG anota 3.573
  como dividendos (R25 = 5152 − T25), sin devolverlos a la ganancia semanal. En `0607 - 1207` INTERESES = 924,16, que
  es exactamente el dividendo de junio del Value CG (T39). Un panel de "intereses pagados" los mostraría como costo
  financiero.
- **16–22/03:** salieron 22.672 (dividendos 6.450 + liquidación de un ex socio 16.222). Para esa semana hay cuatro
  "ganancias": −4.424,77 (Neto − Neto), −5.353,06 (celda B17), 17.318,94 (celda C17, "sin contar liquidación") y
  18.247,23 (Value CG y `Semanales`).
- La Tenencia fija el dividendo en el 10 % de la ganancia del mes. El Value CG registra solo el 84,37 % (lo que cobran
  Manuel, Jose y Francisco; Alejo figura con "No"). Desde `0806 - 1406` la columna DIVIDENDOS está en cero: no hay
  dividendos registrados de julio a octubre, o están cargados en otra columna.
- En total, entre marzo y octubre bajaron el Neto 34.398,16 de retiros: el 18 % de la ganancia del período.

**Por qué engaña.** Las semanas de pago de dividendos parecen malas. Los meses con retiros grandes parecen peores. Un
"costo de intereses" queda inflado con plata que fue a los socios.

**Mitigación en la interfaz.**
- La métrica principal es **"Ganancia antes de retiros"** = variación del Neto + retiros de la semana. Los retiros se
  muestran como **barra aparte, debajo del eje**, rotulada "Retiros de socios (no es pérdida)".
- Lista de retiros en la configuración (fecha, monto, tipo: dividendo, liquidación o aporte), incluidos los que están
  dentro de INTERESES, para que el cálculo no dependa de en qué columna se cargó cada uno.
- **Advertencia** visible: "No hay dividendos registrados desde julio".
- Los **aportes de capital** van en la misma lista, con signo contrario. Un aporte que entra a caja no es ganancia.

## 7. Efecto del tipo de cambio mezclado con la ganancia, y cotización cargada a mano — Alta

**Qué pasa.** Los pesos (efectivo, transferencias, cheques) se pasan a dólares con una cotización que se escribe a mano
en C8 (en las primeras cinco hojas, adentro de la fórmula). Como la financiera tiene siempre una posición grande en
pesos, cada cambio de cotización mueve la ganancia, y una cotización vieja o mal tipeada pasa directo al patrimonio.

**Evidencia.**
- **Sensibilidad hoy:** 180.147.333 ARS a 1.535 = 117.359,83. Cada peso de cotización mueve ≈ 76,5 USD: 10 pesos
  son ±765 (el 34 % de la ganancia "sin ajuste" de la última semana, 2.247,83) y un 1 % son ±1.170. En
  `1105 - 1705`, con 429,5 M ARS, cada peso movía ≈ 221 USD.
- **Efecto estimado acumulado desde marzo:** −12.318 (el dólar pasó de 1.410 a 1.535). Por semana va de −3.285
  (`0806 - 1406`) a +3.122 (`2704 - 0305`). En `2206 - 2806` la pérdida de la semana (−758) es toda cambiaria: sin
  ese efecto, la semana gana 1.930. En `1409 - 2009` pasa algo parecido (−276 → +302).
- **Cotizaciones repetidas:** 1.490 en tres hojas seguidas (22/06–12/07), 1.525 en cuatro hojas (20/07–23/08, cinco
  semanas), 1.535 y 1.540 en dos hojas cada una. Hay subas y bajas de 5 pesos que parecen de carga (1.535 → 1.530 →
  1.525 → 1.535).
- En la misma hoja se usan dos cotizaciones: en `0806 - 1406` el pago del Polígono se convierte a 1.420 y C8 dice
  1.440.
- **Otras monedas a cotización fija:** euro a 1,25 (`config.json` dice 1,23 operado, mercado ~1,17; hoy hay 3.320 EUR,
  ±266). USDT a 1:1, cuando la paridad observada es 1,02–1,05 (`docs/metodologia.md`): con −17.134 de posición son
  ≈ ±500, y con los 77.399 de la semana 04–10/05 llegaban a ±2.300.

**Por qué engaña.** Una semana "mala" puede ser solo que subió el dólar, y una "buena", que se cargó una cotización
vieja. Si la cotización se actualiza tarde, el efecto de varias semanas cae en una sola.

**Mitigación en la interfaz.**
- **Barra separada "efecto del tipo de cambio"** en el gráfico de ganancia, para que se vea qué parte es negocio y
  qué parte es dólar.
- **Mostrar la cotización usada** en cada semana (línea fina bajo el gráfico o en la tabla) y **marcar** las iguales a
  la semana anterior ("cotización repetida").
- **Sensibilidad** en la tarjeta de patrimonio: "si el dólar estaba 10 pesos más alto, el patrimonio es X menor".
- Cotizaciones en `config.json` (por semana), nunca en el código; si una semana no tiene cotización, avisar en lugar
  de usar la anterior en silencio.

## 8. Semana doble y meses de 4 y de 5 semanas — Alta

**Evidencia.**
- `1008 - 2308 (Dos Semanas)` cubre 14 días: 18.349 son 9.175 por semana. Graficada como una barra más, duplica.
- Por fecha de cierre, mayo y agosto tienen 35 días (5 semanas); marzo a septiembre, 28; octubre va por 21. El Value CG asigna los meses a su
  manera: su "Abril" suma 5 semanas (del 05/04 al 03/05) y da 52.366,61, contra 29.747,29 de mayo (4 semanas). Por
  semana son 10.473 y 7.437. Con la regla "mes de la fecha de cierre", abril da 46.814.
- La Tenencia mueve 873 de mayo a junio (`G11 = 258321.53-873`): mayo 29.748,99 y junio 10.951,04, contra 29.747,29 y
  10.077,82 en el Value CG.

**Mitigación en la interfaz.**
- Toda comparación entre períodos, **por semana de 7 días**. Los totales mensuales llevan debajo "N semanas".
- La hoja doble se dibuja como una barra **el doble de ancha** (o dos medias barras), con la nota "dato de dos
  semanas".
- Una sola regla para asignar semanas a meses (por fecha de cierre, el domingo), escrita en el glosario. Si el dueño
  prefiere la del Value CG, que quede en la configuración.

## 9. Fuentes desactualizadas o que no coinciden — Alta

**Evidencia.**
- El **Value CG** llega al 28/06. Las 15 hojas siguientes de la Calculadora (16 semanas, hasta el 18/10) no están.
- Su hoja **Dashboard** está más atrasada: "Capital actual" = `'Value CG'!B36` = 266.647,58 (21/06), no el 28/06
  (265.889,35) ni el último dato (359.107,17). La tabla "últimas 6 semanas" va del 17/05 al 21/06.
- La **Tenencia** llega a los dividendos de junio y toma un dato de la hoja oculta `Value 2026` (G7 =
  `'Value 2026'!B11`). La hoja oculta `Value 2025` tiene 136 celdas con #REF!.
- La hoja **`Semanales`** llega al 14/06 y difiere en 07/06 (−4.820,60 contra −2.310,60) y en 14/06 (704,03 contra
  8.116,25). Su título lo dice: "Es lo generado, no lo 'real'".
- La primera hoja (`2302 - 0103`, Neto 167.944,79) no coincide con el 01/03 del Value CG (167.896,05): 48,74 de
  diferencia.
- `1210 - 1810` existe en los dos archivos de la Calculadora: 343.251,68 (a) y 359.107,17 (b). En b, "Ganancia Neta"
  y "Ganancia Bruta" dan #REF! porque la fórmula apunta a `'05/10 - 11/10'`, que no existe. Recalculadas contra
  `'0510 - 1110'!B16`: 18.103,33 y 19.370,41 (lo que espera el dueño).
- En el Value CG, la semana del 01/03 aparece dos veces (filas 11 y 14, con 9.191,70 cada una), y las filas
  "Dividendos" y "Balance Actual" no tienen fecha: quien lea solo las filas con fecha cuenta dos veces esa semana y no
  ve los retiros.

**Mitigación en la interfaz.**
- **Una sola fuente** para el patrimonio y la ganancia: la Calculadora, tomando de cada hoja la última versión (el
  archivo más nuevo gana, como ya hace `value/leer.py`). Las celdas con error se recalculan, no se muestran.
- El Value CG se usa solo para lo que la Calculadora no tiene (historia anterior a marzo, retiros, aportes,
  Tenencia), siempre con su fecha de corte a la vista.
- **Cartel fijo arriba:** "Datos al 18/10/2026 (semana 12–18 oct). Value CG actualizado al 28/06".
- Cuando llegue el Value CG nuevo, una pantalla de conciliación semana por semana (Calculadora contra Value CG) que
  muestre las diferencias en lugar de elegir una en silencio.

## 10. KPIs heredados del Dashboard del Value CG mal armados — Media

Si el dashboard nuevo copia los indicadores de la hoja `Dashboard`, hereda estos problemas.

| KPI de la hoja | Valor | Problema | Recalculado |
|---|---|---|---|
| Ganancia prom. semanal (F30) | 10.339,49 | Promedia E5 (28.122, ganancia de varios meses de 2025) y E7 (37.660,15, del 01/07/2025 al 01/02/2026) como si fueran semanas | Sin esas dos: 8.191,72 (mediana 8.393,60, 21 semanas) |
| Máx. ganancia semanal (K39) | 37.660,15 | Es E7: siete meses en una fila | Máximo real: 23.558,44 (08/02) |
| Mín. ganancia mensual (I39) | 28.122,00 | Es E5, que no es un mes; además no incluye junio | Mínimo real: junio, 10.077,82 |
| Ganancia prom. mensual (E30) | 40.487,05 | Promedia feb–may y deja afuera junio; abril tiene 5 semanas | Feb–jun: 34.405,20. Por semana: 11.033 / 8.926 / 10.473 / 7.437 / 2.519 |
| Renta sobre capital prom. mensual (B39) | 27,82 % | Incluye F5 (40,18 %, varios meses) y excluye junio (3,94 %) | Feb–jun: 20,57 % |
| Renta sobre capital prom. semanal (C39) | 4,80 % | Arrastra las semanas de febrero (19,03 % el 08/02) con base chica | Mar–jun: 3,72 % (mediana 3,20 %) |
| Columna "Ganancia" de la tabla de 6 semanas | 176.170–195.536 | Es el P&L acumulado sobre aportes (columna C), no la ganancia de la semana | — |
| Capital actual (B29) | 266.647,58 | Apunta al 21/06 | 359.107,17 al 18/10 |

**Mitigación.** No copiar ninguno. Recalcular todo desde la tabla semanal con filtros explícitos y poner debajo de cada
promedio **cuántas semanas tiene y de qué fecha a qué fecha** ("promedio de 32 semanas, 02/03–18/10").

## 11. Cheques a valor nominal y cambio fuerte de composición — Media

**Evidencia.**
- Los cheques en pesos se suman a valor nominal, a la cotización del día, sin descontar el plazo. En `2303 - 2903`
  eran 170.767 de 180.927 (94 % del Neto); en `0405 - 1005`, 65 %; desde `0806 - 1406`, entre 1 % y 7 %; hoy, 6.764
  (1,9 %).
- Si el plazo promedio fuera de 30 días, a la tasa de ~8 % mensual de la cartera de cheques del Registro
  (`docs/contexto_negocio.md`), el valor actual sería ~7 % menor: en `2303 - 2903`, unos 12.600 menos, más que la
  ganancia de esa semana. Es un ejemplo de orden de magnitud: los plazos no están en esta planilla.
- La posición en pesos pasó de 240–430 M ARS (marzo–mayo) a 86–180 M (agosto–octubre). El patrimonio de marzo era
  mucho más sensible al dólar y al cobro de cheques que el de hoy.

**Por qué engaña.** Comparar el patrimonio de marzo con el de octubre es comparar una cartera casi toda de cheques con
otra de caja e inversiones. La línea es continua, pero lo que mide cambió.

**Mitigación.** Gráfico de **composición en el tiempo** (área apilada: caja, pesos, cheques, inversiones, ajustes) al
lado del de patrimonio total. Rótulo "cheques a valor nominal" en la leyenda.

## 12. Volumen, operaciones y renta sobre volumen con datos copiados — Media

**Evidencia.**
- "Operaciones" vale 338 en 12 hojas seguidas (`2007 - 2607` a `1210 - 1810`), 348 en dos y 407 en una. El "volumen
  por operación" de C22 (B21/B22) no significa nada.
- "Volumen Prom": Debe 479.840,65 y Haber 474.180 se repiten en 4 hojas (`2004 - 2604` a `1105 - 1705`). El Promedio
  499.476,13 está escrito a mano en `2704 - 0305` y en `0405 - 1005`. Para el 10/05 la Calculadora dice 499.476,13 y
  el Value CG, 686.863,60.
- La "RENTA" del Value CG mezcla definiciones: J14 y J15 usan BRUTOxSEM; desde J16, la ganancia neta. Además, divide
  ganancias que no salen del volumen (efecto dólar, ajustes, entrada de inversiones): por eso 24–30/08 da 12,9 %.
- La hoja `Volumen Mayo` tiene volumen por operador de solo tres semanas de mayo y excluye a un cliente grande.
  Mostrarla como "volumen de mayo por operador" sería incompleto.

**Mitigación.**
- **No mostrar** operaciones, ticket promedio ni volumen por operación de la Calculadora.
- El volumen, si se muestra, tiene que salir del Registro General con la metodología del pipeline (sin USDT General,
  `docs/metodologia.md`), con su fuente rotulada.
- Renta sobre volumen solo sobre la ganancia "limpia" (sin ajustes, sin efecto dólar, antes de retiros), o no
  mostrarla.

## 13. Porcentajes sobre aportes o sobre una base chica — Media

**Evidencia.**
- "VARxCAP" del Value CG: 274,97 % (P&L 195.536,47 sobre aportes 71.111,11). Ese P&L no descuenta los retiros (34.398
  en 2026) y usa aportes que cambiaron (69.985,48 en 2025, 71.111,11 en 2026), además de otros movimientos de capital
  de la Tenencia (una liquidación, el capital del período anterior).
- **Error de fórmula:** C9:C11 del Value CG hacen `=B9-$B$2` (B2 está vacía) en lugar de restar los aportes. El
  "P&L sobre aportes" del 15/02 al 01/03 sale igual al capital (156.684,69, 158.704,35, 167.896,05) y el % da 223 %
  a 240 %. La hoja oculta `Value 2025` lo tenía bien (86.699,21 para el 15/02).
- El % semanal sobre capital no es comparable en el tiempo: 5.000 eran el 3 % del patrimonio en marzo (167.000) y son
  el 1,4 % hoy (359.000). Las primeras semanas de febrero dan 43,74 % y 19,03 %.

**Mitigación.** Montos en USD como dato principal. Si se muestra un %, que sea sobre el **patrimonio promedio del
período**, con el rótulo de la base. Nada de % sobre aportes en la vista principal; si el dueño lo quiere, en un
detalle con la explicación de qué incluye.

## 14. Gastos fijos de principio de mes que generan semanas negativas — Media

**Evidencia.** Los gastos se cargan casi todos en una semana por mes: 5.694 (`0203 - 0803`), 7.966 (`0106 - 0706`),
5.828 (`0607 - 1207`), 7.447 (`0308 - 0908`), 8.972 (`3108 - 0609`) y 8.111 (`0510 - 1110`), contra 100–1.300 en una
semana común. De las 10 semanas con ganancia negativa, 6 son esas.

**Por qué engaña.** El gráfico semanal es un serrucho. Una alerta de "dos semanas negativas seguidas" o "racha de
pérdidas" salta por el calendario y no por el negocio.

**Mitigación.** Media móvil de 4 semanas sobre las barras semanales; marca "semana de costos fijos" (gastos mayores a
un umbral configurable). Para la ganancia, que la vista mensual normalizada sea la principal.

## 15. Períodos incompletos y carga retroactiva — Media

**Evidencia.**
- Hoy es martes 20/10: la semana 19–25/10 está en curso y no está cargada. El último dato es el domingo 18/10.
- Octubre tiene 3 hojas por fecha de cierre (una con 4 días de septiembre): suma 13.501, que sin el ajuste USDT son
  −2.354. Una barra de octubre al lado de meses completos no es comparable.
- El dueño no hizo el cierre desde agosto y completó las hojas juntas en octubre. Las señales de carga retroactiva
  están ahí: operaciones fijas en 338, CHEQUES idénticos en 4 hojas, LLC idéntica en 11 hojas y a cero de golpe en
  la última, y los saltos del riesgo 2.

**Mitigación.**
- El mes en curso se dibuja con barra **rayada** y el rótulo "parcial: 3 de ~4 semanas"; se compara siempre por semana.
- **Indicador de calidad de carga** por semana (por ejemplo, ✓ normal / ⚠ con alertas), alimentado por los chequeos de
  este informe: cotización repetida, saldos sin movimiento, columnas sin nombre, cargada a posteriori.

## 16. Reparto por socio no es Neto × % — Baja

**Evidencia.**
- Tenencia: Manuel, Jose y Francisco con 28,13 % y Alejo con 15,62 %. Suman 100,01 %, y el encabezado de Alejo dice
  15,63 %.
- El capital de cada socio no es Neto × %: en junio la Tenencia da 78.208,65 para cada socio principal y 29.715,55
  para Alejo (suman 264.341,50 contra 264.329,57 de capital), mientras 28,13 % × 264.329,57 = 74.356. La diferencia
  viene de la historia (aportes, una liquidación, Alejo no retira dividendos).
- La Tenencia llega a junio y depende de una hoja oculta.

**Mitigación.** La vista por socio sale solo de la Tenencia, con su fecha de actualización. Nunca se calcula como
porcentaje del Neto actual. Si se muestra la ganancia repartida, se reparte con los porcentajes de la configuración y
se avisa que suman 100,01 %.

## 17. Saldos que no se mueven, unidades dudosas y valuaciones a la par — Baja

**Evidencia.**
- **TRX = 1.734 en las 26 hojas** en que aparece, sumado a 1:1 como dólares. Si son tokens TRX y no USD, el valor
  está inflado (a ~0,3 USD por TRX serían ~520, no 1.734). A confirmar.
- PayPal Ruso 218 en 25 hojas; REALES 100 en 14; GRABIFI 287,62 en 9; **LLC 6.144,11 en 11 hojas** y a cero en la
  última: los −6.144 caen en 12–18/10 aunque pueden ser de antes.
- **PROMAR 87.000.000** tiene "USD" en la fila de moneda: parecen pesos. Está neutralizado (fila 2 = −fila 3) y fuera
  del Neto, pero si se mostraran saldos de la fila 2 por moneda, aparecerían 87 millones de dólares. MILLAMAPU
  (200.000) y LIBRAS no tienen moneda.
- **Garantías con criterio mixto:** MILLAMAPU, CHARCAS y PROMAR (y antes JEEP y GOL TREND) se neutralizan con su
  pendiente; el Polígono, solo en parte (332.157,57 contra 261.592); AH y Almafuerte, nada. Si alguien borra un
  pendiente de garantía, el Neto salta por el valor de la garantía (200.000 en el caso de MILLAMAPU).
- **Cara chica y Malos** se suman a la par, aunque se canjean con descuento (`docs/contexto_negocio.md`): hoy 8.070.

**Mitigación.** Panel "saldos sin movimiento hace N semanas" (para preguntar, no para alarmar). Validar la moneda de
cada caja contra `config.json` (`moneda_por_caja`) y no contra la fila 5. Control automático "fila 2 + fila 3 = 0"
para las garantías neutralizadas, con alerta si se rompe.

## 18. Errores de fórmula latentes y notas que contradicen la fórmula — Baja

Hoy no cambian el número, pero pueden hacerlo en cualquier semana:
- "Pesos" divide por la cotización las columnas G a I, que incluyen **USD BsAs** y **DEUDA USD** (cajas en dólares).
  Hoy están en cero; un saldo de 1.000 USD entraría como 0,65.
- En `1307 - 1907` y `2007 - 2607`, ALQUILERES entra con coeficiente −1 (suma en Dólares y resta en Egresos e
  Ingresos). Valía cero.
- En `0806 - 1406`, el alquiler de 3.600 tiene al lado la nota "NO CONTAR", pero la fórmula lo suma al Neto. Esa
  semana, sin el alquiler y sin la entrada del Polígono, daría −2.896 en lugar de +8.116. Al lado de la Ganancia Bruta
  dice "REVISAR".
- Hay cotizaciones escritas adentro de fórmulas (`/1410`, `*1.2`) y en hojas auxiliares (`/1300` en `Comisiones`).

**Mitigación.** Que la actualización corra chequeos y los muestre en una pestaña "Control": columnas sin encabezado,
coeficientes raros, cajas en USD divididas por la cotización, notas como "NO CONTAR" o "REVISAR" en el bloque, celdas
con error. Si un chequeo falla, el tablero se publica igual pero con un aviso arriba.

## 19. Nombres que se leen al revés — Baja

| En la planilla | Qué es | Cómo se lee mal | Nombre sugerido |
|---|---|---|---|
| Deuda (+4.000, fija) | Plata que le deben a Cambio General | Como una deuda nuestra | "Deuda a cobrar (fija)" |
| USDT (fila del bloque, 41.536,49) | Participación 2/3 en las ganancias de USDT General, escrita a mano | Como la caja USDT (que está en −18.868) | "Participación USDT General" |
| BRUTO (Value CG, 468.691) | Ganancia bruta acumulada desde 2025 | Como un saldo más grande que el capital | No mostrar el acumulado |
| Ganancia Bruta | Ganancia antes de gastos, comisiones, inversión, intereses y dividendos de la semana | Como facturación o ingresos | "Ganancia antes de gastos" |
| INVERSION (columna de egresos) | Un egreso (34.103 acumulados en el Value CG) | Como las inversiones del activo (Polígono, Almafuerte) | Preguntar al dueño y renombrar |
| Poligono 09 / Almafuerte (bloque) | Hoy apuntan a GOL TREND y JEEP | Como el valor del Polígono y de Almafuerte | No usar |
| Grabify BORRAR | Caja a eliminar, en cero | — | Ocultar si está en cero |

---

## Qué no mostraría

1. Los renglones del bloque de cálculo como tales ("Dólares", "Pesos", "Poligono 09", "Almafuerte").
2. Operaciones, ticket promedio y volumen por operación de la Calculadora.
3. Los KPIs de la hoja `Dashboard` del Value CG.
4. % sobre aportes en la vista principal.
5. El "BRUTO" acumulado y los acumulados de egresos del Value CG como si fueran saldos.
6. Saldos de la fila 2 sueltos (sin su pendiente): ahí aparecen los 87 millones de PROMAR como dólares.
7. Decimales en patrimonio y ganancia.

## Reglas de cálculo para quien construya el tablero

1. Cada hoja sale de la última versión que traiga cualquier archivo (`1210 - 1810` del archivo b). Las celdas con
   error se recalculan.
2. Ganancia = Neto − Neto anterior, en todas las semanas. No se usan las celdas "Ganancia" guardadas.
3. El Neto se recalcula desde las cajas con un mapeo fijo, y se compara con el de la planilla. La diferencia se
   muestra.
4. Capas separadas en `config.json`: ajustes a mano (USDT General, Deuda, cambios de criterio), retiros y aportes,
   notas por semana, cotizaciones. Nada de eso va en el código.
5. Por defecto: ganancia **antes de retiros y sin ajustes a mano**, con el efecto del dólar en barra aparte.
6. Toda comparación entre períodos, por semana de 7 días; la hoja doble cuenta por dos.
7. Cada promedio lleva N y período; al lado, la mediana.
8. Banderas por semana: dos semanas, ajuste a mano, sin explicar, cotización repetida, costos fijos, cargada a
   posteriori, saldos sin movimiento.

## Preguntas para el dueño (cierran riesgos)

1. ¿Qué es la columna AH (112.966, sin encabezado) y de dónde salen los 37.500 que sumó en 05–11/10?
2. Las liquidaciones de USDT General (15.855,49): ¿se cobraron a alguna caja o quedaron en USDT General? ¿De qué fecha
   es cada una? ¿Los 4.021 de fines de mayo son parte de la misma ganancia?
3. ¿Qué explica los +42.940 de 24–30/08 (pendientes en USD +59.466) y los +18.361 del pendiente de cheques en
   10–23/08?
4. Las filas 2 y 3 que pega por caja: ¿qué son exactamente (saldo con o sin pendientes) y qué signo tienen los
   pendientes?
5. ¿Qué cotización usa cada semana (la del cierre, la operada)? ¿Se pueden cargar las de las semanas repetidas?
6. ¿Pagaron dividendos de julio a octubre? ¿En qué columna los cargó?
7. Polígono: ¿por qué cuenta 70.565,57 de 332.157,57? ¿Qué criterio separa las garantías que se neutralizan de las
   que no?
8. ¿TRX 1.734 son dólares o tokens? ¿Cuándo se vació la LLC (6.144)?
9. El alquiler de 3.600 de 08–14/06 con "NO CONTAR": ¿se cuenta o no?
10. "Deuda" 4.000: ¿quién debe y se cobra? ¿Qué es la columna INVERSION de egresos?

---

## Anexo — Ganancia semanal descompuesta

Para el SPEC y el auditor. **Ajustes a mano** = saltos de las constantes (USDT General, Deuda) y el cambio de criterio
del euro. **Retiros** = dividendos y liquidaciones que bajaron el Neto esa semana (se suman). **Efecto dólar** =
estimado, como se explicó arriba. **Ganancia limpia** = planilla − ajustes + retiros − efecto dólar. Es una referencia
para dimensionar, no una cifra para publicar como "la ganancia real". **Δ pendientes** = variación de lo que aportan
las filas 3 sin inversiones. **Δ inversiones** = variación de inversiones y garantías netas (a costo).

| Hoja | Días | Cotiz. | Neto | Ganancia planilla | Ajustes a mano | Retiros | Efecto dólar | Ganancia limpia | Δ pendientes | Δ inversiones | Marca |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `0203 - 0803` | 7 | 1.405 | 167.541 | -404 | — | — | 417 | -821 | -153.263 | — | gastos 5.694 |
| `0903 - 1503` | 7 | 1.405 | 175.934 | 8.394 | — | — | 0 | 8.394 | 170.883 | — |  |
| `1603 - 2203` | 7 | 1.415 | 171.510 | -4.425 | — | 22.672 | -1.215 | 19.463 | -71.023 | — | retiro 22.672 (dividendos 6.450 + liquidación de un ex socio 16.222) |
| `2303 - 2903` | 7 | 1.405 | 180.927 | 9.417 | — | — | 1.285 | 8.132 | -52.783 | — |  |
| `3003 - 0504` | 7 | 1.390 | 185.123 | 4.197 | — | — | 1.901 | 2.296 | 71.891 | — |  |
| `0604 - 1204` | 7 | 1.380 | 194.374 | 9.251 | — | — | 1.695 | 7.556 | -80.976 | — |  |
| `1304 - 1904` | 7 | 1.385 | 209.277 | 14.903 | 10.900 | — | -1.041 | 5.044 | -67.991 | — | USDT +10.900 a mano |
| `2004 - 2604` | 7 | 1.400 | 227.740 | 18.464 | — | — | -1.985 | 20.449 | -35.054 | — |  |
| `2704 - 0305` | 7 | 1.380 | 233.293 | 5.553 | — | 3.573 | 3.122 | 6.004 | 175.939 | — | 3.573 de dividendos cargados en INTERESES |
| `0405 - 1005` | 7 | 1.380 | 238.449 | 5.156 | — | 4.719 | 0 | 9.875 | -229.841 | — | dividendos 4.719 |
| `1105 - 1705` | 7 | 1.395 | 247.281 | 8.832 | -1.000 | — | -2.754 | 12.586 | 189.068 | — | Deuda 5.000 → 4.000 |
| `1805 - 2405` | 7 | 1.405 | 252.329 | 5.048 | — | — | -2.191 | 7.240 | 39.398 | — |  |
| `2505 - 3105` | 7 | 1.410 | 258.322 | 5.992 | 5.737 | — | -673 | 929 | -61.924 | — | USDT +4.021; WISE pasa de 1:1 a ×1,25 y EUR de 1,2 a 1,25 |
| `0106 - 0706` | 7 | 1.415 | 253.501 | -4.821 | — | 2.510 | -601 | -1.709 | -93.022 | — | dividendos 2.510; gastos fijos 7.966 |
| `0806 - 1406` | 7 | 1.440 | 261.617 | 8.116 | — | — | -3.285 | 11.401 | 298.921 | 7.412 | entra Polígono (otra versión de la semana da 704); alquiler 3.600 "NO CONTAR" |
| `1506 - 2106` | 7 | 1.455 | 266.648 | 5.030 | — | — | -893 | 5.923 | 48.529 | 60.195 | Polígono 7.412 → 67.607 |
| `2206 - 2806` | 7 | 1.490 | 265.889 | -758 | — | — | -2.688 | 1.930 | -5.621 | — | la pérdida es toda por la suba del dólar |
| `2906 - 0507` | 7 | 1.490 | 277.291 | 11.401 | — | — | 0 | 11.401 | -4.202 | — | cotización repetida |
| `0607 - 1207` | 7 | 1.490 | 275.748 | -1.543 | — | 924 | 0 | -619 | -67.409 | — | 924,16 de dividendos en INTERESES; gastos fijos 5.828; cotización repetida |
| `1307 - 1907` | 7 | 1.510 | 283.106 | 7.358 | — | — | -1.687 | 9.046 | 15.092 | 50.000 | entra Almafuerte 50.000 |
| `2007 - 2607` | 7 | 1.525 | 284.975 | 1.869 | — | — | -1.173 | 3.042 | -50.680 | 2.278 |  |
| `2707 - 0208` | 7 | 1.525 | 286.442 | 1.467 | — | — | 0 | 1.467 | 108.977 | — | cotización repetida |
| `0308 - 0908` | 7 | 1.525 | 283.874 | -2.568 | — | — | 0 | -2.568 | 11.793 | — | gastos fijos 7.447; cotización repetida |
| `1008 - 2308 (Dos Semanas)` | 14 | 1.525 | 302.223 | 18.349 | — | — | 0 | 18.349 | -29.325 | 25.466 | 14 días; cheques pendientes −27,2 M → +0,8 M ARS (+18.361); sale Almafuerte, entra Polígono 20+13; cotización repetida |
| `2408 - 3008` | 7 | 1.535 | 345.164 | 42.940 | — | — | -556 | 43.496 | 56.083 | — | sin explicar: pendientes USD +59.466 |
| `3108 - 0609` | 7 | 1.530 | 340.096 | -5.067 | — | — | 257 | -5.325 | -13.818 | — | gastos fijos 8.972 |
| `0709 - 1309` | 7 | 1.525 | 343.954 | 3.858 | — | — | 267 | 3.590 | -116.580 | — |  |
| `1409 - 2009` | 7 | 1.535 | 343.678 | -276 | — | — | -579 | 302 | 35.144 | 680 |  |
| `2109 - 2709` | 7 | 1.535 | 345.606 | 1.928 | — | — | 0 | 1.928 | 6.839 | — | cotización repetida |
| `2809 - 0410` | 7 | 1.540 | 344.888 | -719 | — | — | -183 | -536 | -38.784 | — |  |
| `0510 - 1110` | 7 | 1.540 | 341.004 | -3.884 | — | — | 0 | -3.884 | -6.995 | 37.500 | columna AH (sin nombre) +37.500; gastos fijos 8.111; cotización repetida |
| `1210 - 1810` | 7 | 1.535 | 359.107 | 18.103 | 15.855 | — | 241 | 2.007 | 66.445 | — | USDT +15.855,49 (may–sep); LLC 6.144 → 0 |

**Totales del período (02/03–18/10, 231 días):** ganancia planilla 191.162; ajustes a mano 31.492; retiros 34.398;
efecto dólar −12.318; ganancia limpia 206.387 (6.254 por semana).

| Período | Hojas | Días | Planilla por semana | Limpia por semana |
|---|---|---|---|---|
| Marzo–junio (`0203 - 0803` a `2206 - 2806`) | 17 | 119 | 5.761 | 7.335 |
| Julio–octubre (`2906 - 0507` a `1210 - 1810`) | 15 | 112 | 5.826 | 5.106 |
| Julio–octubre sin `1008 - 2308` ni `2408 - 3008` | 13 | 91 | 2.456 | 1.527 |
