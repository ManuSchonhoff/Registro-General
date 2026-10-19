# Tablero v2: especificación

Definitiva para implementar (19/10/2026). El v1 (`registro/tablero.py`, `registro/tablero_plantilla.html`) **no se toca** y
se sigue generando y publicando igual. Implementan dos personas en paralelo: **Python** (secciones 4, 5 y 7) y **front-end**
(2, 3, 4 y 6). La única interfaz entre los dos es el contrato JSON (sección 4). El front-end carga los skills
`artifact-design` y `dataviz` antes de escribir la plantilla. Revisada el 19/10/2026 con las correcciones de la revisión
cruzada (resumen en la sección 10).

**Prioridades.** Cada módulo, paso y criterio lleva **P0** (primera entrega: completo y con los números bien) o **P1** (se
puede dejar para después). Se termina todo lo P0 antes de empezar cualquier P1.
- **P0:** Semana completa (M1.1–M1.5); Clientes M2.1, M2.2, M2.4 y M2.5; Operación M3.1, M3.2 y M3.3; Saldos M4.1–M4.5;
  Control M5.1, M5.2, M5.3, M5.5 y M5.6; `actualizar.py` con plan, notas, revisadas y publicación; los criterios de datos
  (sección 8: del 1 al 10 y del 29 al 35).
- **P1:** M2.3 (gráfico de altas), M2.6 (hoja de cliente), M3.4, M3.5 (la lista de comisiones está toda en `null`), M3.6,
  M3.7, M4.6, M5.4, el período "Desde…", el chip de puesto del ranking, `parecidos` y C14, el escaneo (C01–C04),
  `elegir`/`excluir` en `leer.py` y el modo con clave del v2 (por defecto ya se publica sin clave).
- M5.5 (Notas) no estaba en la lista de prioridades: va como P0 porque es una lista simple y el criterio 34 depende de ella.
- **El contrato se mantiene completo.** Python emite todas las claves y columnas de 4.2; las de un módulo P1 que todavía no
  calcula van como tabla vacía con sus columnas (por ejemplo, `parecidos`). El front oculta el módulo que no implementa, sin
  dejar el título ni un hueco. Si un ancla apunta a un módulo oculto, lleva al comienzo de su sección.

**Datos de prueba para trabajar en paralelo.** El front no espera al Python: arma en el scratchpad (fuera del repo) un JSON
sintético con 30 semanas o más que incluya la semana doble, una semana en curso, semanas iniciales sin saldos
(`formato_actual = 0`), una fila de `caja` con `confiable = 0` y las dos fotos de `pend` (foco y semana en curso). Sin
nombres reales: "Cliente 01", "Op 1". El ejemplo de una fila por tabla de 4.2 no alcanza para probar gráficos ni períodos.

**Notación**
- `V` = `b.vol`: filas de `operaciones.csv` con `fin`, `detalle` ∈ `detalles_que_son_volumen`, `cliente` ∉ `excluir_clientes_de_volumen`, y `mon_debe` y `mon_haber` no nulas ni "Otra".
- `w` = índice de semana en base 0 según el orden de `R.semanas` (`semana_n − 1`). Entre corridas, la semana se identifica por la fecha de inicio (`"2026-10-12"`).
- `f` = semana foco (por defecto, la última completa).
- `k_w` = `round(((fin − ini).days + 1) / 7)`: vale 2 en la hoja "Dos Semanas" y 1 en las demás.
- **Semanas de calendario.** "Las N semanas de calendario anteriores a `w`" son las semanas `j < w` más cercanas a `w`,
  tomadas hasta que `Σ k_j ≥ N` (la doble cuenta 2). Se usan en `recuperados`, `pasan_inactivos`, `inactivos` y
  `pct_recurrente` (4.3).
- `u = x / k`: normalización, solo para flujos (USD, operaciones, nuevos).
- `P4` = promedio de `u` en las semanas completas `f−4 … f−1`. Si hay menos de 2, es `null`.
- `Δsem = u_f / u_{f−1} − 1` y `Δp4 = u_f / P4 − 1`.
- `R` = período elegido: 1, 4 o 12 semanas, Año, o "Desde…" (este último es P1). Siempre termina en `f`.
- `Tend` = 12 semanas hasta `f` en el celular y 26 desde 960 px. Con período "Año", todas.

## 1. Objetivo y principios

**Para quién.** Para los dos dueños, que lo miran sobre todo en el celular, una vez por semana, después de subir la planilla.
Lo tiene que poder leer cualquier dueño de financiera: sin jerga interna y con cada número explicado a un toque.

**Preguntas que responde, por urgencia**
1. ¿Hay algo para mirar hoy?
2. ¿Cuánto operamos, y es normal?
3. ¿Quién operó? ¿Dependemos de pocos? ¿Qué clientes importantes no vinieron?
4. ¿Cuánta plata está afuera y hace cuánto? ¿Cuánta caja hay, y en qué moneda?
5. ¿A qué precio compramos y vendimos? ¿Se cobran las comisiones de lista?
6. ¿Cómo están los cheques, los inversores y los retiros previstos?
7. ¿Está todo cargado, y bien?

**Qué no muestra: ganancia, resultado, rentabilidad ni margen.** Esa cuenta la hace el dueño en su archivo de patrimonio.
Quedan afuera:
- `ganancia_*`, `resultado_*` e `ingresos_operativos*`;
- `comision_usd` y "% efectivo";
- `margen_%` y "Margen medio" del circuito USDT;
- `efecto_tipo_cambio_usd`;
- "Fondeo vs ingresos" y la cobertura;
- `resumen_hoja_CQ`;
- toda variación del total de caja en USD: la caja se compara por moneda y en su unidad.

Los textos que genera el tablero (rótulos, `AYUDA`, glosario, alertas, `control`, `metodo` y cualquier frase que arme la
plantilla) y las claves del JSON no pueden coincidir con esta regex (sin distinguir mayúsculas):
`ganancia|resultado|rentab|margen|utilidad|p[ée]rdida|perdiendo|ingresos operativos`. Por eso "clientes perdidos" pasa a ser
"dejaron de operar", y en los chequeos se habla de "estado", no de "resultado".
- **Alcance de la regex.** No se aplica a los textos que vienen tal cual de la planilla: `dic.cli`, `dic.op`, `dic.caja`,
  `pend.cli_txt`, `pend.detalle`, `revisar.cli_txt`, los titulares de cheques, `fondeo.inversores` (inversor, plazo,
  destino, detalle, `retiro_txt`), `invgar.proyecto`, `notas`, los nombres de archivo y las cajas y operadores que lista
  `control`. Hay textos de clientes en la planilla que llevan una de esas palabras entre paréntesis: no se censuran ni se
  renombran. En las pruebas (criterios 9 y 13) esos strings se reemplazan por un marcador antes de buscar.
- **Nombre del cliente en la UI.** El rótulo principal es siempre `dic.cli` (`cliente_g`, ya limpio). `cli_txt`, el texto
  crudo de la planilla, solo aparece en el detalle de la fila.
- **Método.** `METODO_V2` no copia la última línea de `METODOLOGIA` del v1 (la que menciona "resultado").
- **Diferencia × volumen.** El front nunca combina una diferencia de precio con un volumen (por ejemplo,
  `min(compra, venta) × diferencia`): ni en cifras, ni en textos, ni en la lectura de los gráficos. `precios` trae los USD de
  los dos lados y esa cuenta sería una ganancia implícita.

**Principios**
1. La semana primero, siempre comparada con la anterior y con el promedio de las 4 previas.
2. El color es de los datos y de los estados; la interfaz va en tinta. Cada estado lleva ícono y palabra.
3. Las fotos dicen su fecha ("Foto al 18/10") y los flujos, su período.
4. Si falta un dato, se muestra "—" con el motivo. Nunca un 0 inventado.
5. Lo que el dueño ya revisó no vuelve a aparecer como nuevo (7.3).

**Decisiones donde los informes discrepaban**

| Decisión | Por qué |
|---|---|
| 5 secciones: Semana · Clientes · Operación · Saldos · Control | Entran en una barra inferior. Arriba va lo urgente y abajo lo de consulta |
| Un único foco y un único período, globales, que se eligen desde el encabezado | En el v1 cinco pestañas ignoraban el filtro sin avisar |
| Arranca en la última semana **completa**; la semana en curso queda a un toque | Comparar una semana parcial contra semanas completas engaña |
| 8 indicadores: 4 con minigráfico y 4 compactos | La actividad entra en la primera pantalla; los saldos son fotos |
| Las alertas se calculan en Python, al corte | Una sola implementación, verificable contra el Excel |
| Caja y pendientes al **cierre**, con datos de la misma hoja | Quedan a la misma fecha y `saldo − caja = plata afuera` cierra exacto. El pase a la hoja siguiente se controla aparte (C08 y C09) |
| Gastos por mes | Los costos fijos se cargan en lotes |
| Ticket por mediana y p90, solo como serie semanal | No se pueden sumar entre semanas |
| Notas en `salidas/notas_manuales.json`, con copia para el v1 | Una sola fuente y nada de hallazgos reescritos a mano |
| SVG propio, sin librerías | Funciona sin internet, cambia el tema al instante y pesa poco |
| `actualizar.py` publica sin clave por defecto (`--clave` sigue disponible) | El Artifact ya es privado |

## 2. Arquitectura de información

**Elementos globales**
- **Encabezado sticky (52 px como máximo).** A la izquierda, un chip-botón: "12–18 oct · cerrada" o "19–25 oct · en curso (2 días)". A la derecha, "?" (lleva a Control › Cómo se calculó) y el botón de tema. En escritorio se agrega el título "Tablero semanal".
- **Selector.** Hoja inferior en el celular y panel en escritorio. Tiene la lista de semanas (la más nueva primero, con su estado) y un control segmentado: Semana · 4 sem · 12 sem · Año · Desde… ("Desde…" es P1). Cada sección que depende del período lo dice arriba: "Mostrando: 4 semanas al 18/10 · Cambiar".
- **Banner.** Aparece si `en_curso` no es nulo y el foco es otra semana: "Hay datos de la semana en curso (19–25 oct, 2 días). Los indicadores muestran la última cerrada. [Ver]".
- **Navegación.** En el celular, barra inferior fija de 5 botones (ícono SVG y texto de 11 px, 48 px de alto como mínimo). Desde 960 px, riel izquierdo de 200 px. Cada sección tiene chips de anclas y los hashes son `#seccion` o `#seccion-ancla`.

Cada módulo indica su prioridad y: pregunta · métrica · visual · interacción · ayuda (la línea del "?") · qué hace si falta
el dato. Las columnas son las del contrato (sección 4). Todo cliente se rotula con `dic.cli` (sección 1).

### 2.1 Semana (`#semana`) · P0
- **M1.1 Alertas** · P0 (ver 3.2).
- **M1.2 Indicadores** · P0 (ver 3.1).
- **M1.3 Volumen por semana** · P0
  - Pregunta: ¿fue una semana normal?
  - Métrica: `u` de `sem.usd` en `Tend`, más una línea con el promedio móvil de 4 semanas (incluye la semana). Se rotula
    "Tendencia: promedio móvil de 4 semanas (incluye la semana)" y en la tabla "Prom. móvil 4 sem.": "Promedio de 4
    semanas" queda solo para `P4`, que no incluye la semana (son cifras distintas).
  - Visual: columnas en `--dato`; la del foco en `--dato-foco`. La semana en curso va con trama y el rótulo "en curso"; la doble lleva la marca "2 sem.".
  - Interacción: tocar, arrastrar o usar las flechas del teclado **solo lee**: actualiza una franja de lectura fija ("29 sep–5 oct · USD 700 k · 180 ops"). Cuando la semana leída no es el foco, la franja muestra el botón "Ver esta semana", que cambia el foco. Incluye "Ver como tabla". La lectura con el dedo y el mouse es P0; con las flechas, P1.
  - Ayuda: "Lo que se movió con clientes cada semana, en USD, contando cada operación una vez."
  - Sin dato: con menos de 2 semanas, la cifra sola y "Todavía no hay historia para comparar".
- **M1.4 Qué se movió** · P0
  - Métrica: dos listas de barras, Productos y Operadores. Cada fila muestra `u_f` y un chip con su `Δp4` (desde `cubo`). Orden: `u_f` de mayor a menor, sin las filas que tienen 0 en la semana y en `P4`.
  - Ayuda: "Qué productos y operadores explican la semana, contra su promedio."
  - Sin dato: si `P4` es `null`, se omite el chip.
- **M1.5 Los 5 mayores clientes de la semana** · P0
  - Visual: igual que M2.1, con 5 filas fijas para `f` y el enlace "Ver ranking".

### 2.2 Clientes (`#clientes`): Ranking · Concentración · Altas · No vinieron · Dejaron
- **M2.1 Ranking** · P0 (el chip de puesto es P1)
  - Métrica: `Σ cubo.usd` por cliente en `R` y su % del total.
  - Visual: en cada fila, el nombre (`dic.cli`) en su propia línea y debajo la barra, "USD 120 k · 12%", un chip de puesto contra el período anterior de igual largo (▲3, ▼2, =, nuevo) y un punto con el color del operador principal (el de mayor `usd` en `R`). Muestra 10 filas más "Ver todos (n)", que pagina de a 50.
  - Interacción: buscador que ignora acentos y mayúsculas. Tocar una fila abre M2.6.
  - Ayuda: "Volumen de cada cliente en el período."
  - Sin dato: "No hubo operaciones en el período".
- **M2.2 Concentración** · P0
  - Métrica: participación del mayor, de los 5 y de los 10 mayores en `R`, más la serie `sem.top5` en `Tend`.
  - Visual: la línea lleva una referencia punteada en `top5_max`. Arriba, la frase "El mayor 12% · Los 5 mayores 40% · Los 10 mayores 60%".
  - Ayuda: "Si los 5 mayores pasan el 50%, dependemos de pocos clientes."
  - El HHI no se muestra.
- **M2.3 Altas y regresos** · P1
  - Visual: columnas por semana. Hacia arriba, `nuevos` (`--ord-2`) y `recuperados` (`--ord-1`) apilados; hacia abajo, `pasan_inactivos` (`--ink-3`). Va también la cifra "Volumen de clientes habituales: `pct_recurrente[f]`" y la lista de los nuevos del foco (clientes cuya primera `w` en `cubo` es `f`).
  - Ayuda: "Nuevos: primera operación del año. Regresaron: volvieron después de 4 semanas de calendario o más sin operar."
  - Sin dato: en las semanas con `w < historia_altas_desde_semana` (es un `w` en base 0: con 9, las semanas 0 a 8), el texto "Sin historia suficiente".
- **M2.4 Importantes que no vinieron** · P0
  - Métrica: entre los `importantes.top` clientes con más `Σ usd` en `[f−11, f]`, los que tienen `usd = 0` en `f` y en `f−1`.
  - Visual: lista ordenada por volumen de la ventana, con "Última vez: 29 sep–5 oct (hace 3 sem.) · USD 200 k en 12 semanas".
  - Ayuda: "De los 30 que más movieron en 12 semanas, los que no operaron en las últimas 2."
  - Sin dato: "Vinieron todos".
- **M2.5 Dejaron de operar** · P0
  - Métrica: `inactivos` con `w ∈ [f−3, f]` y **sin operaciones en `(w, f]`** (`vuelve_w` nulo o mayor que `f`), ordenados por `usd_hist` de mayor a menor. Con datos reales, 9 de los 67 que pasaban a inactivos en la ventana ya habían vuelto: sin esta exclusión aparecerían como "dejaron" estando activos.
  - Ayuda: "Clientes con 3 operaciones o más que cumplen 4 semanas sin operar y no volvieron."
- **M2.6 Detalle de cliente (hoja inferior)** · P1
  - Contenido: las columnas `u` de las últimas 26 semanas, sus operaciones de las últimas 8 (`det`), su plata afuera (`pend` del foco, si tiene foto) y sus operadores, con el % de cada uno.
  - Se cierra con Esc, con la X o tocando afuera.

### 2.3 Operación (`#operacion`): Operadores · Productos · Precios · USDT · Comisiones · Días · Tamaño
- **M3.1 Volumen por operador** · P0
  - Visual: columnas apiladas en `Tend`, con 3 series según `op_grupo`: `--op-1`, `--op-2` y "Resto del equipo" en `--op-resto`. La leyenda muestra el % de cada serie en `R`.
  - Interacción: tocar "Resto" despliega cada operador.
  - Ayuda: "Quién operó cada semana."
- **M3.2 Productos** · P0
  - Visual: barras con `Σ usd` y % en `R`. Con período de una semana, cada barra lleva su chip `Δp4`. La mezcla semanal en % va en "Ver como tabla".
- **M3.3 Precio del dólar** · P0
  - Interacción: control segmentado Billete | Transferencia.
  - Visual: compra (`--ink-2`) y venta (`--ink`) en `Tend`, con el área entre las dos en `--banda`. Debajo, un minigráfico con el mismo eje x de la diferencia % = `(venta − compra) / promedio`. Arriba, la frase "Compra $ 1.500,0 · Venta $ 1.510,0 · Diferencia $ 10,0 (0,7%)". Si en ese lado `n < precios_min_ops` o `usd < precios_min_usd`, el punto va hueco y se rotula "pocos datos" (las ventas por transferencia suelen ser unas 10 operaciones y pocos miles de USD por semana, así que su diferencia sale de muy poco volumen). No se muestra ninguna cifra que combine la diferencia con un volumen (sección 1).
  - Ayuda: "Precio promedio ponderado de compra y de venta, y la diferencia en pesos por dólar."
  - Sin dato: si falta un lado, la línea se corta y la tabla dice "sin ventas" o "sin compras".
- **M3.4 USDT** · P1
  - Visual: línea de `usdt.cot_med` (pesos por USDT), la frase "1 USDT = 1,035 USD billete" y "Transferencias cubiertas con USDT: `pares` (USD `usd_pares`)".
- **M3.5 Comisiones pactadas** · P1
  - Métrica: mediana de `comis.pct` por `tipo_com` en `R`, con la cantidad de operaciones y los USD.
  - Visual: barras. Si `comisiones_lista[dic.tipo_com[tipo_com]]` tiene valor, se dibuja una marca en el valor de lista y, cuando la mediana queda más de 0,1 puntos por debajo, el chip "debajo de la lista".
  - Ayuda: "El % pactado en la columna Cotización/Comisión."
  - Sin dato: "Todavía no se cargó la comisión de lista de cada tipo. Cuando esté, se va a ver si se cobra por debajo."
- **M3.6 Días de la semana foco** · P1
  - Visual: columnas por `dia.fecha`, con USD y cantidad de operaciones. Las fechas con `inferida = 1` llevan "aprox.".
- **M3.7 Tamaño** · P1
  - Visual: barras pareadas por tramo en `R` (% de operaciones contra % de volumen, desde `tramos`) y líneas de `ticket_med` y `ticket_p90` en `Tend`. Arriba, la frase "9 de cada 10 operaciones son menores a USD 10 k".
  - Ayuda: "La operación típica es la mediana; el promedio lo inflan las grandes."

### 2.4 Saldos (`#saldos`): Caja · Plata afuera · USDT sin confirmar · Cheques · Inversores · Inversiones
- **M4.1 Caja por moneda** · P0
  - Datos: la foto `caja` de `f`. Rótulo: "Al cierre del 18/10" si `momento = 0`, o "Al inicio de la semana en curso" si `momento = 1`.
  - Tabla: moneda, en su unidad, ≈ USD y %. Orden de las filas: USD billete, USD exterior, USDT, Pesos, Euros, Reales, Libras. La última fila es "Total equivalente (referencia)", sin variación. La fila de USD billete se despliega por caja.
  - Debajo: múltiplos chicos, uno por moneda **en su unidad**, en `Tend`.
  - Leyenda fija: "Los cambios incluyen aportes, retiros y movimientos con clientes."
  - Ayuda: "Caja propia al cierre de la semana. El tablero anterior mostraba el saldo al inicio de la semana, por eso las cifras pueden no coincidir."
  - Interacción: conmutador Caja propia | Saldo de la planilla (Balance) (`caja_real` o `saldo_real`). La caja propia ya
    descuenta la plata de terceros (inversores y clientes con operaciones abiertas) que está en la caja y puede dar
    negativa: en ese caso, debajo de la tabla va "Negativo: en esa caja hay más plata de terceros que saldo" (más "Depende
    del signo de los pendientes, que está a confirmar" mientras no esté confirmado).
  - Dato a revisar: si alguna caja de la moneda tiene `confiable = 0` en esa semana, el punto del múltiplo va hueco y la tabla dice "dato a revisar" (4.3). Con `null` se dibuja normal.
  - Sin dato: antes de la primera semana con `formato_actual = 1`, "El formato con saldos empieza el dd/mm", con la fecha de `ini` de esa semana (se deriva de `semanas`, no se escribe fija). La moneda "Otra" se muestra en Control.
- **M4.2 Plata afuera** · P0
  - Cifras: **Nos deben** y **Debemos** de `f`, cada una con su `Δsem` (suma de los tipos de `pend_sem`).
  - Por tipo: barras de dos lados en tintas neutras.
  - Antigüedad: una barra al 100% de `|usd|`, con los tramos 0–1, 2–4, 5–12 y más de 12 semanas en `--ord-1…4`, y "sin N° de Ope" con trama gris. Sale de `a01…a12` y `*_usd` de `pend_sem`, así que funciona con cualquier foco.
  - Evolución: dos líneas en `Tend`.
  - Lista: los ítems de `pend` con `w` = foco (`momento = 0`; `momento = 1` si el foco es la semana en curso). Muestra los 10 de mayor `|usd|`, cada uno con cliente (`dic.cli`), tipo, "abierto hace N sem.", "nos debe USD 12 k" y el chip "nuevo". Tiene buscador y "Ver todos". Si el foco no tiene foto, la lista se reemplaza por "El detalle por ítem está para la última semana cerrada (12–18 oct) y para la semana en curso". Con el foco por defecto la lista siempre se ve.
  - Ayuda: "Operaciones abiertas y cuentas corrientes." Mientras `config.signo_pendientes_confirmado` sea `false`, se agrega "El signo está a confirmar: nos deben y debemos podrían estar invertidos."
- **M4.3 Transferencias sin USDT confirmado** · P0
  - Métrica: ítems de `pend` del foco con tipo USDT General y `con_q = 1`: cantidad, USD y cuántos llevan `usdt_q_semanas` semanas o más.
  - Visual: lista ordenada por `sem_abierto` de mayor a menor.
  - Sin foto para el foco: solo las cifras, desde `pend_sem` (`con_q` y `con_q_mas4`), sin lista.
- **M4.4 Cheques** · P0
  - Banner: si pasaron más de `cheques_dias_sin_altas` días desde la última alta, "La hoja CQ no tiene cheques nuevos desde el dd/mm: puede estar sin actualizar".
  - Cifras: en cartera ($ y ≈ USD) y vencidos ($ y cantidad, con ícono y la palabra "Vencido").
  - Gráficos: vencimientos por mes y los 5 mayores titulares por cartera, con su % **sobre la cartera** (`titulares.pct` = `cartera_ars` del titular ÷ `cheques.cartera_ars`), no sobre el total histórico: para el riesgo importa lo que está en cartera.
  - Sin dato: "La base no tiene hoja CQ".
- **M4.5 Inversores** · P0
  - Cifras: capital de terceros, interés mensual comprometido, tasa promedio y retiros previstos (inversor, monto y mes).
  - Tabla: completa. El inversor propio se rotula "propio (no es fondeo de terceros)" y no suma. Debajo del retiro va el `detalle` de la hoja, tal cual: ahí hay plazos en texto libre ("antes de fin de año") que no están en la columna de retiro.
- **M4.6 Inversiones y garantías** · P1
  - Tabla: proyecto, valor en su unidad ("unidad a confirmar") y cambio contra la semana anterior. Solo las filas distintas de 0.

### 2.5 Control (`#control`): La semana · Para revisar · Hojas al día · Gastos · Notas · Cómo se calculó
- **M5.1 Control de la semana** · P0
  - Arriba, `control.resumen`.
  - Los chequeos de 7.2, agrupados en Bloqueantes, Avisos, Info y OK (este último plegado). Un aviso con todas sus claves en `revisadas` se ve atenuado, con "Revisado dd/mm".
  - La tabla de origen: semana, archivo y si está cerrada o en curso.
- **M5.2 Para revisar** · P0
  - Lista: `revisar` de `f`, con severidad, "Fila 120 · 12–18 oct" (más "Ope 15001" si tiene), operador, cliente, tipo, ≈ USD y el chip "Revisada dd/mm" (`revisada_fecha`). La `clave` no va a la vista: queda dentro del `<details>` de la fila.
  - Foco en la semana en curso: en lugar de una lista vacía, "Se revisa al cerrar la semana" (`revisar` y `calidad` solo cubren semanas completas).
  - Interacción: conmutador "Todas las no revisadas".
  - Gráficos: barras de `(alta + media) / ops × 100` por semana (desde `calidad`), rotuladas "Diferencias de carga cada
    100 filas" (`ops` cuenta las filas cargadas, con los movimientos internos: son más que las operaciones con clientes de
    la portada), y una tabla por operador en `R` (Graves, Menores, Leves, Filas).
  - Ayuda: "Lo cargado en las columnas de caja no coincide con la operación, o hay filas canceladas o sin estado con importes."
- **M5.3 Hojas al día** · P0: `frescura`, cada fecha con los días que pasaron.
- **M5.4 Gastos registrados** · P1
  - Visual: columnas por mes y un ranking de categorías en `R`.
  - Nota fija: "Solo Detalle = Gastos; sueldos, alquileres o comisiones con otro detalle no están."
- **M5.5 Notas** · P0: hallazgos y preguntas, las abiertas primero. Las resueltas van plegadas, con su fecha (`fecha_estado`).
- **M5.6 Cómo se calculó** · P0: `metodo`, el glosario y las cotizaciones por semana (`semanas.ars` y `semanas.usdt`). `metodo` incluye la línea "El tablero anterior mostraba el saldo al inicio de la semana; acá la caja es al cierre", la definición de caja propia y la primera semana con saldos, derivada de `semanas`.

## 3. Portada "de un vistazo"

### 3.1 Indicadores · P0
Van en una grilla de 2 columnas en el celular y de 4 en escritorio. Los indicadores 1 a 4 llevan un minigráfico de `Tend` con
la línea del promedio móvil de 4 semanas.

| # | Rótulo | Cifra | Sublínea | Comparación |
|---|---|---|---|---|
| 1 | Volumen operado | `sem.usd[f]` | "Promedio de 4 semanas: USD …" | `Δsem` y `Δp4` |
| 2 | Operaciones | `sem.n[f]` | "Operación típica: USD `ticket_med`" | `Δsem` y `Δp4` |
| 3 | Clientes que operaron | `clientes` | "`nuevos` nuevos · `recuperados` regresaron" | `Δp4`, sin semanas con `k ≠ 1` |
| 4 | Los 5 mayores clientes | `top5` | "El mayor: `top1`" | En puntos, contra la semana anterior y contra `P4` |
| 5 | Dólar billete | Dos líneas: "Compra $ …" y "Venta $ …" | "Diferencia $ … por dólar" | La diferencia, en $, contra la semana anterior |
| 6 | Plata afuera | Dos líneas: "Nos deben USD …" y "Debemos USD …" | "`mas4` abiertos hace 4 semanas o más"; con `signo_pendientes_confirmado = false` se agrega "· falta confirmar si nos deben y debemos están al revés" | `Δsem` de nos deben |
| 7 | Caja propia USD billete | `caja_real` del grupo USD, al cierre | "En la planilla (Balance): USD …" (`saldo_real` del grupo USD) y "Pesos $ … (≈ USD …) · USDT …". Con `confiable = 0`, "dato a revisar" | En su unidad, con la leyenda de M4.1 |
| 8 | Para revisar | Dos líneas: "`a` graves (≥ USD 100)" y "`m` menores (USD 10–100)", sin revisar, **de `f`** | "y N de semanas anteriores · Ver lista" (N = graves y menores sin revisar de semanas anteriores; si es 0, solo "Ver lista") | — |

- **Formato de la comparación:** "▲ 24% vs prom. 4 sem.", en tinta neutra. Si `|x| < 0,5%`, va "=".
- **Color:** solo se colorea el indicador 8 (`--crit` si hay alguna fila Alta de `f` sin revisar).
- **Indicadores 6 y 8:** en lugar de la cifra de 24 px llevan dos líneas apiladas de 17 px, para que entren en los ~165 px de
  cada tarjeta a 390 px.
- **Indicador 7:** su ayuda explica que es la caja propia (sin la plata de terceros), que puede dar negativa y que el
  tablero anterior mostraba el saldo al inicio de la semana.
- **Palabras.** En la interfaz, las severidades de `revisar` se muestran como "grave" (Alta), "menor" (Media) y "leve"
  (Baja), para no confundirlas con las altas de clientes; en el JSON siguen siendo `Alta`, `Media` y `Baja`. Nada de
  jerga de diseño ("chip") ni de archivos ("config.json", "v1") en los textos visibles.
- **Foco en la semana en curso:** sin % ni flechas, con el texto "en curso · N días; se compara al cerrar".
- **Semana doble:** "valores por semana".
- **Sin `P4`:** "Sin semanas para comparar".

### 3.2 Alertas · P0
- **Cálculo.** Python las calcula al corte. Si se cambia el foco, el bloque se mantiene con el rótulo "Alertas al 18/10".
- **Orden.** Primero las críticas, después las de atención y al final las informativas; dentro de cada grupo, por id.
- **Cuántas se ven.** En el celular 3 y en escritorio 5, más "Ver todas (n)".
- **Formato.** Cada alerta lleva una franja de color de 4 px, ícono, palabra, una frase con el número y un enlace a su ancla.
- **Revisadas.** Las que tienen la clave en `revisadas` (7.3) salen de la portada y se ven atenuadas en "Ver todas".
- **Agrupadas.** A01 y A11 juntan varias claves: `clave` es `null` y `claves` trae la lista. Python cuenta solo las no
  revisadas; si no queda ninguna, la alerta se emite con `revisada = 1`: sale de la portada y se ve atenuada en "Ver todas".
- **Claves a la vista.** Las claves son jerga: no se muestran en la alerta sino dentro de su `<details>`. A la vista va el dato
  legible ("Fila 120 · 12–18 oct"). Claude traduce cuando el dueño dice "la fila 120 del 12/10 ya está".
- **Fotos.** A04 y A08 usan la foto de pendientes de `foco` (`momento = 0`), la misma que M4.2 y M4.3 muestran por defecto.
- **Sin alertas.** Se muestra un check con "Nada urgente esta semana".

| id | Regla (umbral en `tablero_v2.umbrales`) | Severidad | `clave` | Ancla |
|---|---|---|---|---|
| A01 | Filas Alta sin revisar. Es crítica si alguna es de `f`; si no, de atención | Crít. / Aten. | En `claves`, una por fila: `<ini>#<fila>#<ope>` (sin N° de Ope, `<ini>#<fila>`) | `#control-revisar` |
| A02 | Retiro de un inversor de terceros en el mes del corte o en el siguiente. Es crítica si el total del mes es ≥ `retiro_critico_pct_caja` (0,5) × el saldo de la planilla (Balance, `saldo_real`) en USD billete: la caja propia ya descuenta el capital de los inversores y compararla con un retiro lo contaría dos veces. Texto (cifras inventadas): "{inversor} tiene previsto retirar USD 50 k en noviembre. En USD billete hay USD 80 k según la planilla (USD 20 k sin la plata de terceros)." (la segunda frase, solo si es crítica) | Aten. / Crít. | `retiro:<inversor>:<AAAA-MM>` | `#saldos-inversores` |
| A03 | Cheques en cartera vencidos. Si pasaron más de `cheques_dias_sin_altas` (30) días sin altas, la frase **empieza** por eso: "La hoja de cheques no se actualiza desde el 02/03: figuran 3 cheques vencidos entre abril y junio por $ 10 M (≈ USD 6,7 k). Confirmar si se cobraron, se colocaron o rebotaron." (cifras inventadas) | Aten. | `cheques:<vencidos_ars÷1000>:<ultima_alta>` | `#saldos-cheques` |
| A04 | Ítems de USDT General con "?" y `sem_abierto ≥ usdt_q_semanas` (4) | Aten. | `usdtq:<cantidad>` | `#saldos-usdt` |
| A05 | Uno de los `top_alerta` (10) mayores de 12 semanas lleva `ausente_semanas` (2) sin operar: una alerta de atención por cliente. Si los ausentes son 5 o más de los `importantes.top` (30), en lugar de las alertas por cliente va **una sola** alerta resumen informativa ("7 de los 30 mayores no operaron en 2 semanas; 3 están entre los 10 mayores"), porque es algo general de la semana | Aten. / Info | Por cliente, `ausente:<cliente>:<ini última semana>`; la resumen, `ausentes:<ini f>` | `#clientes-novinieron` |
| A06 | `|Δp4| ≥ volumen_var_pct` (0,25). Es de atención si baja e informativa si sube | Aten. / Info | `vol:<ini f>` | `#semana` |
| A07 | `top1 > top1_max` (0,25) o `top5 > top5_max` (0,5) | Aten. | `conc:<ini f>` | `#clientes-concentracion` |
| A08 | Ítems con `sem_abierto > pend_semanas_viejo` (12). Aparte, una informativa con los ítems sin N° de Ope | Aten. / Info | `pendviejos:<n>` / `sinope:<n>` | `#saldos-afuera` |
| A09 | Pasaron más de `costos_fijos_dias` (35) días desde el último costo fijo | Info | `fijos:<fecha>` | `#control-gastos` |
| A10 | `caja_real` de una moneda por debajo de `caja_minima[mon]`, o % en pesos por encima de `pesos_max_pct`. Con umbral `null` o con `confiable = 0` no se evalúa | Aten. / Info | `caja:<mon>:<ini f>` | `#saldos-caja` |
| A11 | Chequeos bloqueantes de 7.2 (crítica, siempre) o avisos con alguna clave que no está en `revisadas` (de atención) | Crít. / Aten. | En `claves`, una por chequeo y contenido: `control:<id>:<contenido>` (7.2), por ejemplo `control:C12:<caja>` o `control:C09:PESOS:-200000`. Nunca lleva la fecha de corte | `#control` |

- **A01** sale de la portada cuando todas sus filas están revisadas (queda atenuada en "Ver todas").
- **Texto:** una frase con el número y sin jerga. Por ejemplo: "3 transferencias sin USDT confirmado hace 4 semanas o más (USD 12 k)."
  En el celular cada alerta de la portada se corta a 3 líneas: lo esencial tiene que estar en los primeros ~90 caracteres.
- **A11 con un solo chequeo pendiente:** el texto dice qué es ("Caja CAJA NUEVA sin moneda asignada: no se suma al total."); con
  varios, "2 avisos del control de carga sin revisar: …" con una frase corta por chequeo.
- **Revisadas en "Ver todas":** sin la palabra de severidad, con el ícono de OK y "Revisada dd/mm". En A01 y A11,
  `revisada_fecha` es la fecha más reciente de sus claves.

## 4. Contrato de datos JSON (`"v": 2`)

### 4.1 Reglas
- **Formato de tabla.** Cada tabla es `{"c": [columnas], "f": [[fila], …]}`. El front-end busca las columnas por nombre e ignora las claves y columnas que no conoce.
- **Versión.** Si un cambio solo agrega, se mantiene `v: 2`. Si cambia o quita algo, pasa a `v: 3`. Con un `v` distinto de 2 se muestra "Versión de datos no compatible".
- **Índices.** `w` (y también `w_origen`, `ult_w` y `vuelve_w`) apunta a `semanas.f` y siempre es ≥ 0. `cli`, `op`, `prod`,
  `tipo_com`, `cat`, `caja`, `mon`, `tipo_pend` y `tramo` apuntan a la lista de `dic` con el mismo nombre. `revisar.tipo`
  **no** es un índice: es texto literal ("Imputación ≠ Debe/Haber", "Cancelada con imputación", "Sin estado con imputación").
- **Operador en `revisar` y `calidad`.** `T["11 Filas a revisar"]` guarda `operador_g` (con "Otros"), que no está en `dic.op`.
  Para `revisar.op` y `calidad.op` se toma el operador crudo con un join por `semana_n` + `fila` contra `b.ops` (todas las filas
  de revisar salen de ahí). Si alguna fila no encontrara operador crudo, se agrega "Otros" al final de `dic.op` (con
  `op_grupo` 2) y se usa ese índice. `cubo` nunca usa "Otros".
- **Semanas de historia.** `config.historia_altas_desde_semana` es un `w` (base 0): con 9, las semanas `w = 0…8` muestran
  "Sin historia suficiente".
- **Unidades.**
  - `usd`: 2 decimales.
  - `ars`: enteros.
  - `cot`: pesos por USD o por USDT, con 2 decimales.
  - `pct`, `top*` y `ratio`: fracción con 4 decimales. Excepción: `comis.pct` y `comisiones_lista` van en puntos porcentuales (2.5 es 2,5%).
  - `tasa_mensual` (inversores): fracción. Es `interes_mensual_usd / monto_usd` cuando los dos son > 0; si no,
    `tasa_hoja / 100` **siempre**. La columna de la hoja Inversores está en puntos porcentuales (1,0 = 1%; también hay 1,5,
    1,25 y 0,5625), como el formato `pct100` del v1. Nunca se decide por el tamaño del valor.
  - Fechas `AAAA-MM-DD` y meses `AAAA-MM`. Los booleanos van como 0 o 1 y lo faltante como `null`.
- **Serialización.** Compacta (`separators=(",", ":")` y `ensure_ascii=False`), con `</` reemplazado por `<\/`.

### 4.2 Claves

| Clave | Columnas / forma | Cómo se arma |
|---|---|---|
| `v`, `generado`, `fecha_corte`, `titulo` | int, `AAAA-MM-DDTHH:MM`, fecha, "Tablero semanal" | — |
| `fuentes` | `[{archivo, rol: "base" o "actualizacion", hojas}]` | Rutas y `R.origen` (no `R.wf.path`) |
| `foco`, `en_curso` | int, e int o `null` | `foco` = última `w` completa; `en_curso` = última `w` si no está cerrada |
| `semanas` | `ini, fin, k, completa, dias_ops, pct_fecha_inferida, ars, usdt, formato_actual, archivo` | `completa` = 0 solo en la última, si está abierta. `pct_fecha_inferida` = cierres diarios sin fecha válida en Q ÷ cierres diarios |
| `dic` | `{cli, op, prod, tipo_com, cat, caja, mon, tipo_pend, tramo}` | `cli` = `cliente_g`, también los de `pend`; `op` = operadores crudos (y "Otros" al final solo si hace falta, 4.1); `mon` = USD, USD Exterior, USDT, ARS, EUR, BRL, GBP, Otra |
| `op_grupo` | En paralelo a `dic.op`: 0, 1 o 2 | Según `operadores_destacados`; el resto es 2 |
| `cubo` | `w, cli, op, prod, n, usd` | `V` agrupado por `semana_n`, `cliente_g`, `operador` (**sin** "Otros") y `producto`; `usd` = `Σ prom_usd` |
| `sem` | `w, usd, n, clientes, nuevos, usd_nuevos, recuperados, pasan_inactivos, usd_hist_inactivos, pct_recurrente, top1, top5, top10, ticket_med, ticket_p90` | 4.3 |
| `inactivos` | `w, cli, ops_hist, usd_hist, ult_w, vuelve_w` | Solo de las últimas 12 semanas (4.3). `vuelve_w` = primera semana posterior a `w` en la que el cliente volvió a operar, o `null` |
| `parecidos` | `w, cli, cli_parecido, ratio` | Clientes nuevos de las últimas 4 semanas con `difflib` ≥ `similitud_clientes` contra uno existente |
| `dia` | `w, fecha, n, usd, inferida` | `V` por `semana_n` y `fecha`; `inferida` = la fecha no sale de Q |
| `tramos` | `w, tramo, n, usd` | Los tramos de `A.tamano` |
| `precios` | `w, canal (0 = billete, 1 = transferencia), lado (0 = compra, 1 = venta), usd, cot, n` | 4.3 |
| `usdt` | `w, cot_med, paridad, n, pares, usd_pares` | Filas de USDT General `{TRANSFER, USDT}` dentro del rango; `paridad` = `cz_usdt`; `pares` y `usd_pares` salen de `T["05 Circuito USDT"]` (cantidad y `Σ usd_cliente`) |
| `comis` | `w, tipo_com, pct, usd`, una fila **por operación** | La selección y la clasificación de `A.comisiones`, copiada igual en `tipo_comision()`; `usd` = `debe_usd` |
| `caja` | `w, momento (0 = cierre, 1 = inicio en curso), caja, mon, saldo_real, caja_real, saldo_real_usd, caja_real_usd, confiable` | 4.3. Sin `columnas_pyg` ni inversiones. Para `mon` = Otra, los USD van en `null`. `confiable`: 0 si falla C08 en esa caja y esa `w`, 1 si se cumple, `null` si no hay `w+1` para comparar |
| `invgar` | `w, proyecto, valor` | `columnas_inversiones_garantias`, con el mismo momento |
| `pend_sem` | `w, momento, tipo_pend, items, nos_deben, debemos, mas4, sin_ope, con_q, con_q_mas4, nuevos, a01, a24, a512, a12, a01_usd, a24_usd, a512_usd, a12_usd, sin_ope_usd` | 4.3. Las cifras en USD van positivas. `a01…a12`: ítems con N° de Ope por antigüedad (0–1, 2–4, 5–12 y más de 12 semanas); `*_usd`: su `Σ |usd|`. `a01 + a24 + a512 + a12 + sin_ope = items` |
| `pend` | `w, momento, cli, cli_txt, tipo_pend, detalle, codigo, ope, w_origen, sem_abierto, con_q, usd, nuevo, fila` | Dos fotos por ítem: la del bloque de abajo de `foco` (`momento = 0`, la misma base que `pend_sem` de `foco`) y, si hay `en_curso`, la del bloque de arriba de `en_curso` (`momento = 1`). `usd` > 0 es "debemos" y < 0, "nos deben". Sin N° de Ope, `w_origen` y `sem_abierto` van en `null` |
| `cheques` | `{ultima_alta, cartera_n, cartera_ars, vencidos_n, vencidos_ars, cot, tasa_mensual_mediana, venc{mes, vencido, n, ars}, titulares{titular, n, ars, pct, cartera_ars}}` | `R.cheques()`, `T["07 …"]` y `M["07_cheques"]`, sin comisión ni ganancia. `titulares` = los 10 mayores por `cartera_ars`, con `pct` = `cartera_ars` del titular ÷ `cartera_ars` total |
| `fondeo` | `{capital_terceros_usd, interes_mensual_usd, tasa_promedio, inversores{inversor, plazo, destino, detalle, monto_usd, tasa_mensual, interes_mensual_usd, retiro_txt, retiro_mes, propio}}` | `R.inversores()`. `detalle` = la columna de la hoja, tal cual. `tasa_mensual` según 4.1. `retiro_mes`: si es el nombre de un mes, su primera aparición en un mes ≥ el mes del corte (**el mes del corte cuenta**: "Octubre" con corte 2026-10-18 da 2026-10); si es una fecha, ese mes; si no, `null` |
| `gastos` | `mes, w, cat, n, usd` | `Detalle = Gastos`, con `gasto_usd` y `A.CATS` como en `A.gastos` |
| `calidad` | `w, op, alta, media, baja, ops` | `T["11 Filas a revisar"]` más las operaciones `fin` por semana y operador; `op` es el operador crudo (4.1) |
| `revisar` | `w, fila, ope, op, cli_txt, tipo, dif_usd, sev, clave, revisada, revisada_fecha` | Solo Alta y Media; `clave` = `<ini>#<fila>#<ope>` (sin N° de Ope, `<ini>#<fila>`); `tipo` es texto; `op` crudo (4.1); `revisada` y `revisada_fecha` según 7.3 |
| `det` | `w, fecha, cli, op, prod, usd, fila, ope` | `V` de las últimas 8 semanas |
| `frescura` | `{ultima_operacion, ultima_alta_cheques, ultimo_costo_fijo, base_archivo}` | `max(V.fecha)`, `max(cheques.fecha)` y la última fecha de "Costos operativos / fijos" |
| `alertas` | `[{id, sev ("critico", "atencion" o "info"), texto, ancla, clave, claves, revisada, revisada_fecha}]` | 3.2. `claves` (lista) solo en A01 y A11, con `clave` en `null`; en las demás, `claves` es `null` |
| `control` | `{resumen, checks[{id, nivel ("bloqueante", "aviso", "info", "ok" o "no_evaluado"), titulo, detalle, n, claves, revisada}], origen{w, archivo, estado}, cajas_sin_moneda{caja, saldo, w}, operadores_otros{op, n}}` | 7.2. `revisada` = 1 si todas las `claves` del chequeo están en `revisadas` |
| `notas` | `{hallazgos[{id, semana, texto, estado ("abierta" o "resuelta"), fecha, fecha_estado}], preguntas[{id, texto, estado ("abierta" o "respondida")}], revisadas[{clave, fecha, nota}]}` | `notas_manuales.json` (7.3). `revisadas` va completa para poder reconstruir las notas si se pierde el archivo |
| `config` | `{umbrales, comisiones_lista, operadores_destacados, semanas_tendencia, historia_altas_desde_semana, importantes, signo_pendientes_confirmado, eur, brl, gbp}` | `config.json` |
| `metodo` | Lista de textos | `METODO_V2` más las cotizaciones fijas |

**Ejemplo mínimo inventado** (una fila por tabla):

```json
{"v":2,"generado":"2026-10-19T09:30","fecha_corte":"2026-10-18","titulo":"Tablero semanal",
 "fuentes":[{"archivo":"Registro_General_2026.xlsx","rol":"base","hojas":36}],"foco":1,"en_curso":null,
 "semanas":{"c":["ini","fin","k","completa","dias_ops","pct_fecha_inferida","ars","usdt","formato_actual","archivo"],
  "f":[["2026-10-05","2026-10-11",1,1,5,0.0,1500.0,1.035,1,"Registro_General_2026.xlsx"],
       ["2026-10-12","2026-10-18",1,1,4,0.2,1510.0,1.04,1,"Registro_General_2026.xlsx"]]},
 "dic":{"cli":["Cliente A","Cliente B"],"op":["Op 1","Op 2","Op 3"],"prod":["USD ↔ Pesos billete","USDT"],
  "tipo_com":["USDT ↔ billete"],"cat":["Otros"],"caja":["USD","PESOS"],
  "mon":["USD","USD Exterior","USDT","ARS","EUR","BRL","GBP","Otra"],"tipo_pend":["USDT General","Clientes y cuentas corrientes"],
  "tramo":["< 500","500 – 1.000","1.000 – 5.000","5.000 – 20.000","20.000 – 50.000","> 50.000"]},
 "op_grupo":[0,1,2],
 "cubo":{"c":["w","cli","op","prod","n","usd"],"f":[[1,0,0,0,3,12000.5]]},
 "sem":{"c":["w","usd","n","clientes","nuevos","usd_nuevos","recuperados","pasan_inactivos","usd_hist_inactivos","pct_recurrente","top1","top5","top10","ticket_med","ticket_p90"],
  "f":[[1,50000.0,40,20,2,1500.0,1,1,8000.0,0.85,0.2,0.55,0.8,900.0,4000.0]]},
 "inactivos":{"c":["w","cli","ops_hist","usd_hist","ult_w","vuelve_w"],"f":[[1,1,5,8000.0,0,null]]},
 "parecidos":{"c":["w","cli","cli_parecido","ratio"],"f":[]},
 "dia":{"c":["w","fecha","n","usd","inferida"],"f":[[1,"2026-10-13",12,15000.0,0]]},
 "tramos":{"c":["w","tramo","n","usd"],"f":[[1,1,10,7000.0]]},
 "precios":{"c":["w","canal","lado","usd","cot","n"],"f":[[1,0,0,20000.0,1505.5,9],[1,0,1,18000.0,1514.0,7]]},
 "usdt":{"c":["w","cot_med","paridad","n","pares","usd_pares"],"f":[[1,1567.0,1.04,15,6,9000.0]]},
 "comis":{"c":["w","tipo_com","pct","usd"],"f":[[1,0,2.5,3000.0]]},
 "caja":{"c":["w","momento","caja","mon","saldo_real","caja_real","saldo_real_usd","caja_real_usd","confiable"],
  "f":[[1,0,0,0,40000.0,35000.0,40000.0,35000.0,null],[1,0,1,3,9000000,9500000,5960.26,6291.39,null]]},
 "invgar":{"c":["w","proyecto","valor"],"f":[[1,"PROYECTO X",10000.0]]},
 "pend_sem":{"c":["w","momento","tipo_pend","items","nos_deben","debemos","mas4","sin_ope","con_q","con_q_mas4","nuevos",
   "a01","a24","a512","a12","a01_usd","a24_usd","a512_usd","a12_usd","sin_ope_usd"],
  "f":[[1,0,0,4,2500.0,0.0,2,0,4,2,1,1,3,0,0,500.0,2000.0,0.0,0.0,0.0]]},
 "pend":{"c":["w","momento","cli","cli_txt","tipo_pend","detalle","codigo","ope","w_origen","sem_abierto","con_q","usd","nuevo","fila"],
  "f":[[1,0,1,"Cliente B (cta)",1,"Cajas","XX",1234,0,2,0,-1200.0,0,9]]},
 "cheques":{"ultima_alta":"2026-05-01","cartera_n":1,"cartera_ars":1000000,"vencidos_n":1,"vencidos_ars":1000000,"cot":1510.0,
  "tasa_mensual_mediana":0.08,"venc":{"c":["mes","vencido","n","ars"],"f":[["2026-07",1,1,1000000]]},
  "titulares":{"c":["titular","n","ars","pct","cartera_ars"],"f":[["TITULAR Z",1,1000000,1.0,1000000]]}},
 "fondeo":{"capital_terceros_usd":100000.0,"interes_mensual_usd":2000.0,"tasa_promedio":0.02,
  "inversores":{"c":["inversor","plazo","destino","detalle","monto_usd","tasa_mensual","interes_mensual_usd","retiro_txt","retiro_mes","propio"],
   "f":[["Inversor 1","Largo","Proyecto X","Aviso con 30 días",100000.0,0.02,2000.0,"Noviembre","2026-11",0]]}},
 "gastos":{"c":["mes","w","cat","n","usd"],"f":[["2026-10",1,0,2,45.0]]},
 "calidad":{"c":["w","op","alta","media","baja","ops"],"f":[[1,0,1,0,2,120]]},
 "revisar":{"c":["w","fila","ope","op","cli_txt","tipo","dif_usd","sev","clave","revisada","revisada_fecha"],
  "f":[[1,120,15001,0,"Cliente A","Imputación ≠ Debe/Haber",350.0,"Alta","2026-10-12#120#15001",0,null]]},
 "det":{"c":["w","fecha","cli","op","prod","usd","fila","ope"],"f":[[1,"2026-10-13",0,0,0,5000.0,40,15001]]},
 "frescura":{"ultima_operacion":"2026-10-17","ultima_alta_cheques":"2026-05-01","ultimo_costo_fijo":"2026-09-01","base_archivo":"Registro_General_2026.xlsx"},
 "alertas":[{"id":"A04","sev":"atencion","texto":"4 transferencias sin USDT confirmado; 2 hace 4 semanas o más (USD 2,5 k).",
  "ancla":"#saldos-usdt","clave":"usdtq:2","claves":null,"revisada":0,"revisada_fecha":null}],
 "control":{"resumen":"12–18 oct cerrada · 2 semanas · 0 bloqueantes · 1 aviso",
  "checks":[{"id":"C12","nivel":"aviso","titulo":"Cajas sin moneda asignada","detalle":"1 columna con saldo no suma al total","n":1,
   "claves":["control:C12:CAJA NUEVA"],"revisada":0}],
  "origen":{"c":["w","archivo","estado"],"f":[[1,"Registro_General_2026.xlsx","cerrada"]]},
  "cajas_sin_moneda":{"c":["caja","saldo","w"],"f":[["CAJA NUEVA",100.0,1]]},
  "operadores_otros":{"c":["op","n"],"f":[["Sin operador",3]]}},
 "notas":{"hallazgos":[{"id":"h1","semana":"2026-10-12","texto":"Texto de ejemplo.","estado":"abierta","fecha":"2026-10-18","fecha_estado":null}],
  "preguntas":[{"id":"p1","texto":"¿Pregunta de ejemplo?","estado":"abierta"}],
  "revisadas":[{"clave":"2026-10-05#88#14800","fecha":"2026-10-19","nota":"error de carga ya resuelto"}]},
 "config":{"umbrales":{"top5_max":0.5,"precios_min_ops":5,"precios_min_usd":10000},"comisiones_lista":{"USDT ↔ billete":null},"operadores_destacados":["Op 1","Op 2"],
  "semanas_tendencia":{"movil":12,"escritorio":26},"historia_altas_desde_semana":9,
  "importantes":{"top":30,"ventana_semanas":12,"ausente_semanas":2,"top_alerta":10},"signo_pendientes_confirmado":false,
  "eur":1.23,"brl":4.8,"gbp":1.33},
 "metodo":["Volumen: …"]}
```

En el ejemplo todos los índices son válidos (≥ 0), pero las ventanas no son realistas: tiene solo 2 semanas. Para probar el
front se usa el JSON sintético de 30 semanas o más (ver el comienzo del documento).

### 4.3 Qué se calcula en Python

**`sem`**, para cada `w`, sobre `V`:
- `usd` y `n`: totales sin normalizar.
- `nuevos`: clientes cuya primera semana es `w`.
- `recuperados`: operan en `w`, no operaron en las 4 semanas de calendario anteriores a `w` y sí antes.
- `pasan_inactivos`: tienen 3 operaciones o más hasta `w`, y `w` es la primera semana en la que suman
  `semanas_cliente_perdido` (4) semanas de calendario sin operar, contando `w`. Es la definición del v1, pero en semanas de
  calendario: con índices, la semana posterior a la ventana que incluye la hoja "Dos Semanas" juntaba dos tandas (33 contra
  unos 13 de una semana normal). Solo difiere del v1 alrededor de la doble. Dentro de la doble, la última semana de
  calendario en que operó un cliente sale de la fecha de su última operación en esa hoja (así la tanda se reparte entre
  las dos semanas siguientes en lugar de caer toda en una).
- `pct_recurrente`: volumen de `w` de los clientes que operaron en las 4 semanas de calendario anteriores a `w`, dividido por
  el volumen de `w`.
- `top*`: participación en `w`.
- `ticket_med` y `ticket_p90`: mediana y percentil 90 de `prom_usd`.

**`precios`**: filas `fin`, `detalle = Cajas`, `cotizacion` en `rango_cotizacion_ars` y cliente no excluido.
- Compra: `caja_debe = USD` y `caja_haber` ∈ {PESOS, TRANSFER}; los USD son `debe`.
- Venta: `caja_haber = USD` y `caja_debe` ∈ {PESOS, TRANSFER}; los USD son `haber`.
- El canal es billete si la otra caja es PESOS.
- `cot = Σ(cotizacion × usd) / Σ usd`, agrupado por `semana_n`, canal y lado. `n` cuenta solo las filas con USD > 0 (una
  fila con el importe vacío no cambia ni el precio ni los USD).

**`caja` y `pend_sem`**, solo en las hojas con `formato_actual`:
- **Semana completa (`momento = 0`):**
  - El bloque de abajo va de `estructura()["ini_pend"] + 1` a la primera fila Balance con "cierre" en G que esté después de `ini_pend`. Si no hay ninguna, va hasta `fin_pend`. Es la rama "cerrada" de `R.pendientes_actuales`, generalizada a cualquier hoja.
  - `cierre_final` = la fila del **Cierre Semanal** que viene después de `ini_pend` (la primera fila Balance con "cierre"
    que tiene saldos; en la hoja real, la fila «Cierre Pendientes» que la precede está vacía y daría saldo 0); si no hay
    ninguna, el último Cierre de la hoja. El código usa el Cierre Semanal y el resultado está verificado contra el Balance de
    la semana siguiente (criterio 29): no "corregirlo" para tomar la fila vacía.
  - **Formato habitual** (`cierre_final > ini_pend`): `saldo_real[caja] = s.val(cierre_final, col)` y
    `caja_real = saldo_real − Σ` de las imputaciones del bloque de abajo en esa caja.
  - **Cierre antes del bloque** (`cierre_final < ini_pend`): pasa en la primera semana con saldos (hoja 1105–1705: el último
    Cierre es la fila 614, `ini_pend` es la 615 y no hay Cierre después del bloque de abajo). Ese Cierre todavía no incluye
    los pendientes, así que `caja_real[caja] = s.val(cierre_final, col)` y `saldo_real = caja_real + Σ` del bloque de abajo
    en esa caja. Verificado en USD billete: con esta rama `saldo_real` es igual al Balance de la semana siguiente; con la
    regla habitual daba negativo, y ese punto se veía en los múltiplos de 26 semanas y en "Año".
  - **Confiabilidad.** Para cada `w` cuya `w+1` tiene `formato_actual`, si en esa caja falla C08
    (`saldo_real(w) ≠ Balance(w+1)`, tolerancia 1, sin PyG), la fila de `caja` lleva `confiable = 0`; si se cumple, 1; sin
    `w+1` (la última semana y `momento = 1`), `null`. Se evalúa en todas las transiciones, no solo en las 3 últimas que avisa
    C08. El front dibuja ese punto hueco con "dato a revisar", y A10 y el indicador 7 no lo usan como dato firme.
- **Semana en curso (`momento = 1`):** la fila 5 es `saldo_real`, la fila 5 más la 6 es `caja_real`, y los pendientes salen del bloque de arriba (rama "en curso"). El rótulo dice "parcial: no incluye los pendientes nuevos de la semana".
- **Conversión a USD:** como `A.posicion` y `b.usd`, con `cz` y `cz_usdt` de **esa** semana.
- **`sem_abierto`:** `idx + 1 − semana_origen` en una semana completa, o `idx − semana_origen` en curso. `semana_origen` es la primera aparición del N° de Ope.
- `mas4` cuenta los ítems con 4 semanas o más; `nuevos`, los que tienen `semana_origen = idx`.
- **Tramos de antigüedad** (`a01`, `a24`, `a512`, `a12` y sus `*_usd`): por `sem_abierto` del ítem, 0–1, 2–4, 5–12 y más
  de 12 semanas. Los ítems sin N° de Ope van solo en `sin_ope` (y `sin_ope_usd`). Las cifras USD son `Σ |usd|`.
- **Fotos por ítem (`pend`).** Se exportan dos: la de `foco` (bloque de abajo, `momento = 0`) y, si hay `en_curso`, la de
  `en_curso` (bloque de arriba, `momento = 1`). Cada foto suma exactamente lo mismo que las filas de `pend_sem` de su `w` y su `momento`.
- `tipo_pend` es la primera regla de `pendientes_tipos` que coincide.

**`inactivos`, `parecidos`, `alertas` y `control`**: también en Python, con las mismas definiciones de M2.4 y M2.5.
- `inactivos`: para cada `w` de las últimas 12, los clientes que pasan a inactivos en `w` (la misma regla que
  `pasan_inactivos`), con `vuelve_w`. La exclusión de los que volvieron se hace con `vuelve_w` y no al exportar, así sirve
  para cualquier foco: un cliente de `inactivos` se muestra en M2.5 solo si `vuelve_w` es `null` o mayor que `f`.
- `parecidos` es P1: hasta que se implemente, va vacía con sus columnas.

### 4.4 Qué se calcula en el navegador
Todo lo que se filtra con `w ∈ R`:
- sumas de `cubo` por cliente, operador y producto;
- ranking y puesto anterior;
- concentración y mezcla del período;
- clientes distintos, y nuevos como `Σ sem.nuevos`. Un cliente cuenta si tiene alguna fila en `cubo` (`n > 0`), aunque sume
  USD 0, igual que `sem.clientes` y `sem.nuevos`: así la lista de nuevos, el ranking y las cifras coinciden;
- mediana de `comis.pct`;
- tramos en %;
- gastos por mes y por categoría;
- calidad por operador;
- `Δsem`, `Δp4` y los promedios móviles, siempre sobre `u`;
- M2.4 para cualquier foco. Con el foco por defecto tiene que coincidir con A05;
- M2.5 para cualquier foco, con la exclusión por `vuelve_w`;
- la barra de antigüedad de M4.2 para cualquier foco, desde los tramos de `pend_sem`.

Reglas:
- Los promedios por semana de un período se dividen por `Σ k`.
- Los promedios de clientes y de concentración excluyen las semanas con `k ≠ 1`.
- Las semanas con `completa = 0` no entran en `P4`.
- Los índices por `w` y por `cli` se arman una sola vez, al cargar.
- Cada sección se recalcula solo cuando está visible.

## 5. Archivos e integración

| Archivo | Contenido |
|---|---|
| `registro/tablero_v2.py` (nuevo) | Exporta `construir_datos_v2(R, b, T, M, cz, cz_usdt, fecha, notas) -> dict`, donde `notas = {"manuales": …, "control": [...], "fuentes": [...], "plan": {...}}`, y `generar_v2(datos, clave, ruta, artifact=False) -> ruta`. Importa `cifrar`, `version_artifact`, `clave_aleatoria` y `_v` de `registro.tablero` sin tocarlo. El paquete es `cifrar(datos, clave)` o `{"plano": datos}`, y se inyecta en `/*__PAQUETE__*/null`. Además define `METODO_V2` y las funciones de 4.3 |
| `registro/tablero_v2_plantilla.html` (nuevo) | `const PAQUETE = /*__PAQUETE__*/null;`. Con `plano` abre directo. Con `ct` pide la clave en un formulario dentro de la página (PBKDF2-SHA256 con `it` y AES-GCM, como el v1) y muestra los errores en línea. Con `null` muestra "Sin datos: generalo con correr.py --tablero-v2" |
| `registro/actualizacion.py` (nuevo) | `planificar`, `escanear`, `fecha_corte`, `validar(R, b, T, M, cfg, plan, previo)`, las notas (`cargar`, `migrar`, `arrastrar_v1`), `publicar_fijo` y `estado_publicacion` |
| `actualizar.py` (nuevo, en la raíz) | Línea de comando de la sección 7 |
| `correr.py` | `main()` pasa a llamar a `pipeline(rutas, fecha, salida, cfg, *, tablero, tablero_v2, artifact, clave, elegir=None, excluir=(), plan=None)`. La línea de comando no cambia y se agrega `--tablero-v2`, que convive con `--tablero` y comparte la clave |
| `registro/leer.py` (P1) | Solo un cambio compatible: `Registro(rutas, cfg, elegir=None, excluir=())`. `elegir` es `{hoja: archivo}` y define qué versión de cada hoja se usa, sin importar el orden; `excluir` saltea hojas. Con los valores por defecto se comporta igual que hoy. Hasta que esté, `actualizar.py` pasa la base primero y las actualizaciones en orden de fecha (7.1) |
| `config.json` | Un bloque nuevo, `tablero_v2`. Las claves existentes no cambian |

**Salidas**
- En `salidas/<fecha>/`: `Tablero_v2_<fecha>.html`, `tablero_v2_artifact_<fecha>.html` (con `--artifact`), `tablero_v2_datos.json` (en claro, para pruebas) y `validaciones.json`.
- Rutas fijas para republicar: `salidas/tablero_v2_artifact.html`, y `salidas/tablero_v1_artifact.html` (solo desde `actualizar.py`). Se copian con `--artifact` y sin bloqueantes, o con `--forzar`.
- `salidas/estado_publicacion.json`: `{"v1": {...}, "v2": {"url", "fecha_corte", "semana", "semanas", "sha256", "generado"}}`. Python nunca borra `url`.
- `salidas/notas_manuales.json` (7.3).

```json
"tablero_v2": {
  "operadores_destacados": ["Francisco", "Manuel"],
  "semanas_tendencia": {"movil": 12, "escritorio": 26},
  "historia_altas_desde_semana": 9,
  "importantes": {"top": 30, "ventana_semanas": 12, "ausente_semanas": 2, "top_alerta": 10},
  "signo_pendientes_confirmado": false,
  "cajas_ignoradas": [],
  "umbrales": {"volumen_var_pct": 0.25, "top1_max": 0.25, "top5_max": 0.5, "usdt_q_semanas": 4,
    "pend_semanas_viejo": 12, "cheques_dias_sin_altas": 30, "costos_fijos_dias": 35, "retiro_critico_pct_caja": 0.5,
    "caja_minima": {"USD": null, "USDT": null}, "pesos_max_pct": null, "precios_min_ops": 5, "precios_min_usd": 10000,
    "formulas_sin_valor_max": 0.05, "volumen_min_vs_mediana8": 0.3, "similitud_clientes": 0.9},
  "comisiones_lista": {"Recaudación / pesos↔transfer": null, "USD exterior ↔ billete": null, "USDT ↔ billete": null,
    "Canje billetes (BsAs, cara chica, malos)": null, "USD exterior ↔ USDT": null},
  "fondeo_excluir_inversores": ["Cambio General"],
  "pendientes_tipos": [
    {"tipo": "USDT General", "cliente": ["USDT General"]},
    {"tipo": "Préstamos y deudas", "detalle": ["Prestamos", "Deuda"]},
    {"tipo": "Garantías y dividendos", "detalle": ["Garantias", "Dividendos"]},
    {"tipo": "Inversores", "inversores": true},
    {"tipo": "Clientes y cuentas corrientes", "resto": true}]
}
```

- `historia_altas_desde_semana` es un `w` en base 0 (4.1).
- `signo_pendientes_confirmado`: mientras sea `false`, el indicador 6 y M4.2 dicen "signo a confirmar". Pasa a `true` cuando
  el dueño confirme el signo de los pendientes.
- `cajas_ignoradas`: columnas de caja que C12 no cuenta (por ejemplo, una caja vieja sin moneda que quedó con un saldo fijo).
  Las columnas con saldo 0 tampoco cuentan.
- `precios_min_usd`: con menos USD en un lado, el punto de M3.3 va hueco con "pocos datos" (se suma a `precios_min_ops`).

La regla `"inversores": true` coincide cuando `grupo_cliente(cliente)` es igual al de un inversor de la hoja Inversores. Los
códigos de la columna E (DD, II, CC…) no se usan porque su significado no está confirmado; queda como pregunta en las notas.

## 6. Sistema visual

**Tokens.** Se definen en `:root`. El tema oscuro va en `@media (prefers-color-scheme: dark)` con
`:root:not([data-theme="light"])`, y se repite en `:root[data-theme="dark"]`. `body { background: var(--bg) }`.

| Token | Claro | Oscuro |
|---|---|---|
| `--bg` `--surface` `--surface-2` | `#f6f6f3` `#fdfdfc` `#efeee9` | `#0f0f0e` `#1a1a19` `#232321` |
| `--ink` `--ink-2` `--ink-3` | `#121211` `#4f4e4a` `#6b6a65` | `#f0efec` `#c3c2b7` `#a3a29b` |
| `--hair` `--axis` `--focus` | `#e3e2db` `#c3c2b7` `#2a78d6` | `#2c2c2a` `#383835` `#5b9be6` |
| `--op-1` `--op-2` `--op-resto` | `#eb6834` `#2a78d6` `#199e70` | `#d95926` `#3987e5` `#199e70` |
| `--dato` `--dato-foco` `--banda` | `#848fa3` `#2f4466` `rgba(18,18,17,.10)` | `#6b7890` `#c9d6ea` `rgba(240,239,236,.14)` |
| `--ord-1…4` | `#86b6ef` `#3987e5` `#256abf` `#104281` | `#184f95` `#2a6fc4` `#5b9be6` `#9ec5f4` |
| `--ok-ink` `--warn-ink` `--crit` | `#006300` `#8a5a00` `#d03b3b` | `#0ca30c` `#fab219` `#e66767` |
| `--warn-bg` `--crit-bg` | `rgba(250,178,25,.12)` `rgba(208,59,59,.08)` | `rgba(250,178,25,.14)` `rgba(230,103,103,.14)` |

**Validación de la paleta** (validador del skill `dataviz`, corrido el 19/10):
- `--op-1`, `--op-2` y `--op-resto` como paleta categórica pasan todos los chequeos en los dos temas, con `--op-resto` claro
  en `#199e70` (antes `#1baf7a`, 2,8:1 contra `--surface`).
- `--dato` claro pasa a `#848fa3`: 3,2:1 contra `--surface` y 3,0:1 contra `--dato-foco` (antes `#8a97ab`, 2,9:1).
- `--ord-1…4` pasa como rampa ordinal (un solo tono, luminosidad monótona, saltos ≥ 0,06 y el extremo claro ≥ 2:1).
  `--ord-1` queda en 2,1:1 en los dos temas, que la regla ordinal admite, siempre que la barra de antigüedad lleve los % a la
  vista o en la lectura y "Ver como tabla".
- Si se cambia un token de datos, se vuelve a correr el validador (`--ordinal` para la rampa).

**Tipografía.** `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`, en 11, 13, 15, 17 y 28 px (24 px en las tarjetas
compactas; los indicadores 6 y 8 usan dos líneas de 17 px). Los rótulos de 11 px van en mayúscula con +0,04em. `tabular-nums` solo en tablas y ejes.

**Componentes**
- **Tarjeta:** fondo `--surface`, borde de 1 px `--hair`, radio de 12 px y padding de 12 px (16 en escritorio).
- **Gráficos:** 180 px de alto en el celular y 220 en escritorio, ejes de 11 px en `--ink-3`, grilla `--hair` y barras con radio de 2 px.
- **Tablas:** por debajo de 600 px se ocultan las columnas `.p3`. La columna clave nunca se oculta, no hay scroll horizontal y tocar una fila abre su detalle completo.
  Las tablas anchas que en escritorio caen en un módulo angosto (mezcla de productos, altas por semana, diferencias por
  operador) se compactan igual según el ancho del módulo (container query), así en escritorio tampoco hay desplazamiento lateral.
- **Hojas inferiores:** `div` con `role="dialog"` y `aria-modal`, foco atrapado y cierre con Esc.
- **Ayuda:** cada tarjeta y cada módulo tiene un botón "?" de 32 px o más que abre un `<details>` con **Qué es / Cómo se calcula / De dónde sale**. Esos textos y el glosario (caja, plata afuera, saldo con pendientes, paridad USDT, cara chica, malos, semana doble) son fijos en la constante `AYUDA` de la plantilla.

**Diseño de página**
- Gutter: `padding-inline: max(16px, env(safe-area-inset-left)) max(16px, env(safe-area-inset-right))`.
- Encabezado: `position: sticky; top: env(safe-area-inset-top, 0px)`.
- Barra inferior: `fixed`, con `padding-bottom: env(safe-area-inset-bottom)`. El `body` reserva su alto.
- Desde 960 px: riel izquierdo, contenido de 1200 px como máximo, tarjetas en 4 columnas y módulos en 2.

**Números.** Una sola función `fmt` en es-AR, con el signo "−" (U+2212):
- **Cifras:** "USD 850", "USD 42,5 k" (menos de 100 k), "USD 850 k", "USD 1,25 M".
- **Pesos:** "$ 20,5 M", con "≈ USD …" debajo. Otras monedas: "USDT 250", "€ 1,2 k".
- **Tablas:** "850.123" con la unidad en el encabezado; precios con un decimal ("1.500,5").
- **Ejes:** paso de 1, 2, 2,5 o 5 × 10ⁿ, con los decimales necesarios para no repetir marcas ("2,5 k").
- **Porcentajes y puntos:** "24%", o "4,7%" por debajo del 10%; diferencias en puntos: "+6 pts".
- **Semanas y fechas:** "12–18 oct", "29 sep–5 oct", "10–23 ago (2 sem.)"; fechas "16/10".

**Accesibilidad**
- Cada gráfico es un `<svg role="img">` con `aria-label` (su lectura principal) y "Ver como tabla".
- La lectura funciona con el dedo (puntero), con mouse y con las flechas del teclado.
- Foco visible de 2 px en `--focus`; las áreas táctiles miden 44 px o más.
- Con `prefers-reduced-motion`, sin animaciones.
- Contraste AA.

**Contrato de Artifact**
- Sin librerías ni pedidos de red.
- Sin `window.print`, descargas, `alert`, `confirm` ni `prompt`.
- `<title>Tablero semanal</title>`.
- `localStorage` solo para `rg2.tema`, `rg2.seccion` y `rg2.rango`, dentro de `try/catch`. Sin él, la página funciona igual.
- Funciona también abierto como `file://`.

## 7. Flujo semanal de un paso

### 7.1 `actualizar.py`

```
python3 actualizar.py [--dry-run] [--fecha AAAA-MM-DD] [--datos datos/] [--archivos A.xlsx …] [--clave X] [--sin-v1]
                      [--forzar] [--excluir-hoja "DDMM - DDMM"]… [--sembrar-revisadas] [--guardar-url {v1,v2} URL]
```

`--excluir-hoja` depende de `excluir` en `leer.py`, así que es P1; el resto de las opciones es P0 (`--clave` funciona, pero el
modo con clave del v2 es P1).

1. **Plan** (P0). Entran todos los `*.xlsx` de `datos/` (o los de `--archivos`, en cualquier orden). La fecha de cada uno es
   la `AAAA-MM-DD` del nombre. La de modificación se usa solo si el nombre no tiene fecha, y solo como último desempate: es
   frágil, porque cambia cada vez que se vuelve a subir el archivo.
   - La **base** es el archivo más reciente que tiene las hojas CQ e Inversores. Va primero, porque `Registro` toma de ahí
     las hojas auxiliares.
   - Las **actualizaciones** son los archivos posteriores a la base, en orden de fecha.
   - **Archivos anteriores a la base.** En P0 se listan como ignorados: `Registro` aplica los archivos en orden y uno viejo
     puesto después de la base pisaría hojas más nuevas. En P1, con `elegir`, todos los archivos (también los anteriores)
     pasan por la regla de elección por hoja del paso 2, que ya resuelve los conflictos.
2. **Escaneo** (P1). Para que el plan y el pipeline no diverjan, el estado de cada hoja sale de `Registro`/`Semana` (la misma
   lógica del pipeline; la carga completa tarda unos 30 s por archivo) y no de una relectura `read_only` aparte. De cada hoja
   se obtiene:
   - si está cerrada (`Semana.cerrada()`);
   - el Ope máximo;
   - si tiene algún Cierre;
   - el % de fórmulas sin valor calculado (comparando el libro con fórmulas y el de valores, que `Registro` ya carga).

   Las hojas se reconocen con `^\d{4}\s*-\s*\d{4}` y el nombre se normaliza a `DDMM - DDMM`. Para cada semana se queda la
   versión cerrada antes que la que está en curso; si empatan, la de Ope máximo mayor; si siguen empatadas, la del archivo más
   nuevo. Esa elección es el `elegir` que recibe `Registro`. Las hojas sin ningún Cierre se excluyen, con aviso.
3. **Fecha de corte** (P0). Si la última semana está cerrada, es su domingo. Si no, es el último Cierre con fecha, o hoy, sin
   pasar el fin de la semana. `--fecha` tiene prioridad. En P0 sale de `R.actual` y `R.actual_cerrada`.
4. **`--dry-run`** (P0). Imprime el plan (archivo → base, actualización o ignorado; la última semana y si está cerrada; con el
   escaneo P1, también semana → archivo) y los chequeos que ya se pueden evaluar. No escribe nada.
5. **Notas** (P0).
   - Si no existe `salidas/notas_manuales.json`, se reconstruye desde la fuente más reciente: primero `notas` del último
     `salidas/*/tablero_v2_datos.json` (trae hallazgos, preguntas y `revisadas`); si no hay, se migra con `migrar` (7.3)
     desde el `notas_tablero.json` más reciente.
   - Se escribe `salidas/<fecha>/notas_tablero.json` (si no existe) para el v1, con los textos de los hallazgos y las
     preguntas en estado "abierta", como strings. Ese es el arrastre: lo resuelto no vuelve al v1.
   - Si en esa carpeta ya hay un `notas_tablero.json` escrito a mano (sin la marca `_nota` de la copia), sus textos se
     suman a las notas como abiertos **solo** si se escribió después del último guardado de `notas_manuales.json` (o si
     `notas_manuales.json` no existía). Uno anterior (por ejemplo, el de una carpeta de antes del v2) no se suma: sus notas
     ya pasaron por `notas_manuales.json` y pueden estar resueltas; se guarda una vez como `notas_tablero_original.json` y
     se reemplaza por la copia. El script imprime los textos que suma.
6. **Proceso** (P0). Llama a `pipeline(..., tablero=not sin_v1, tablero_v2=True, artifact=True, clave=args.clave, elegir,
   excluir, plan)` (`elegir` y `excluir` son P1; en P0 van con sus valores por defecto), con una sola lectura del Excel para
   el v1 y el v2.
7. **Publicación** (P0). Sin bloqueantes (o con `--forzar`), copia los dos artifacts a las rutas fijas y actualiza
   `estado_publicacion.json`.
8. **Salida** (P0). Imprime "12–18 oct cerrada · 38 semanas · 0 bloqueantes · 3 avisos · listo para publicar". Código de
   salida: 0 si todo está bien; 2 si hay bloqueantes (las salidas con fecha se escriben igual, pero no las rutas fijas); 1 si
   hubo un error.
9. **`--guardar-url`** (P0). Graba la URL en `estado_publicacion.json`.
10. **`--sembrar-revisadas`** (P0, una sola vez). El 19/10 el dueño confirmó que los errores marcados eran errores de carga ya
    resueltos ("ya están cocinados"). Con esta opción:
    - se agregan a `revisadas` todas las filas Alta y Media hasta la última semana cerrada, con `fecha` 2026-10-19 (el día en
      que se siembra) y `nota` "error de carga ya resuelto". Nunca después de la semana que contiene
      `tablero_v2.sembrar_revisadas_hasta` (2026-10-18, lo que el dueño confirmó): si se pierden las notas y se vuelve a
      sembrar más adelante, no se dan por revisadas filas que nadie confirmó;
    - todos los hallazgos que existen en ese momento (con `semana` ≤ ese mismo tope, o `semana` nula) pasan a
      `estado: "resuelta"`, con `fecha_estado` 2026-10-19;
    - las preguntas no se tocan.

`correr.py --tablero-v2` corre las validaciones de C05 en adelante. Las del escaneo quedan como `no_evaluado` ("Chequeo
todavía no disponible"). Lee `notas_manuales.json` si existe y, si no, `notas_tablero.json`.

### 7.2 Validaciones (`validaciones.json` y M5.1)

| id | Chequeo | Nivel si falla | Contenido de la clave `control:<id>:…` | P |
|---|---|---|---|---|
| C01 | Hojas no reconocidas | aviso | `<hoja>` | P1 |
| C02 | Semana cerrada reemplazada por una en curso (con `elegir` no pasa, pero se informa la elección) | bloqueante | `<hoja>` | P1 |
| C03 | Fórmulas sin valor en las 2 últimas hojas: bloqueante si superan `formulas_sin_valor_max`; aviso si hay al menos una | bloq. / aviso | `<hoja>` | P1 |
| C04 | Hoja sin ningún Cierre (excluida) | aviso | `<hoja>` | P1 |
| C05 | La base no tiene CQ o Inversores | bloqueante | `<archivo>` | P0 |
| C06 | Menos semanas que en `estado_publicacion.json` | bloqueante | `<semanas>` | P0 |
| C07 | Volumen de la semana foco cerrada por debajo de `volumen_min_vs_mediana8` × la mediana de las 8 anteriores | bloqueante | `<ini f>` | P0 |
| C08 | `saldo_real(w)` (4.3) distinto de `Balance(w+1)` (sin PyG, tolerancia 1), en las últimas 3 transiciones | aviso | `<caja>:<diferencia>` | P0 |
| C09 | `−Σ` bloque de abajo`(w)` distinto de `Apertura(w+1)` (tolerancia 1), en las últimas 3 transiciones | aviso | `<caja>:<diferencia>` | P0 |
| C10 | Cierres diarios vacíos en la última semana **cerrada** (`foco`): a mitad de semana es normal que la hoja en curso los tenga, y se controla al cerrar | aviso | `<ini>` | P0 |
| C11 | Operaciones de la última semana **cerrada** sin Fin, Pen ni Can (misma razón que C10) | aviso | `<ini>:<n>` | P0 |
| C12 | Columnas de caja con saldo ≠ 0 que no están en `moneda_por_caja`, PyG, inversiones ni `cajas_ignoradas`. Texto: "La caja CAJA NUEVA tiene un saldo de 100 y no sabemos en qué moneda está, así que no se suma al total. Decile a Claude en qué moneda está, o que es una caja vieja, y deja de avisar." | aviso | `<caja>` | P0 |
| C13 | Operadores fuera de `operadores_principales` en las últimas 4 semanas | info | `<operador>` | P0 |
| C14 | Clientes nuevos parecidos a uno existente | info | `<cliente>` | P1 |
| C15 | Semanas sin cotización observada (se usó la anterior) | aviso | `<ini>` | P0 |
| C16 | `config.anio` distinto del año de corte, o una hoja que cruza el año | aviso | `<anio>` | P0 |
| C17 | Filas Alta o Media de la semana foco sin revisar | info | — | P0 |
| C18 | Notas migradas o arrastradas | info | — | P0 |

- **Claves.** Cada hallazgo de un chequeo lleva `control:<id>:<contenido>`, sin la fecha de corte: lo que el dueño revisó una
  vez no vuelve la semana siguiente si no cambió. Un chequeo con varios hallazgos (por ejemplo, dos cajas sin moneda) tiene
  varias claves. Las diferencias se redondean al entero (`control:C09:PESOS:-200000`).
- **Revisados.** Un aviso con todas sus claves en `revisadas` se ve en M5.1 como "Revisado dd/mm" y no cuenta para A11. Los
  bloqueantes no se dan por revisados: se resuelven en la planilla o se publica con `--forzar`.
- Antes de esta revisión, C12 saltaba todas las semanas por una caja sin moneda con saldo fijo y por columnas en cero, y A11
  usaba `control:<fecha_corte>`: quedaba una alerta de atención permanente en la portada.

### 7.3 `salidas/notas_manuales.json`

```json
{"hallazgos": [{"id": "h1", "semana": "2026-10-12", "texto": "…", "estado": "abierta", "fecha": "2026-10-18", "fecha_estado": null}],
 "preguntas": [{"id": "p1", "texto": "…", "estado": "abierta"}],
 "revisadas": [{"clave": "2026-10-12#120#15001", "fecha": "2026-10-19", "nota": "error de carga corregido"}]}
```

- Los hallazgos automáticos no se guardan acá: se recalculan en cada corrida.
- El tablero no escribe estado. El dueño dice por chat "la fila 120 del 12/10 ya está" y Claude busca la clave (en el
  `<details>` de la fila o en `revisar`) y la agrega a `revisadas`. A la vista se muestra "Fila 120 · 12–18 oct"; la clave
  queda en el detalle de cada alerta y de cada fila.
- **Coincidencia en `revisar`.** La clave es `<ini>#<fila>#<ope>` (sin N° de Ope, `<ini>#<fila>`). Una fila está revisada
  si en `revisadas` hay una clave con el mismo `ini` y el mismo Ope; si alguna de las dos no tiene Ope, se compara por `ini`
  y fila. Así, si el dueño inserta una fila en una hoja cerrada, las marcas no se corren. Las claves `<ini>#<fila>` que ya
  existan siguen valiendo.
- Si `revisadas` trae strings sueltas, se leen como `{"clave": s}`.
- **Estados.** Hallazgos: "abierta" o "resuelta"; `fecha` es la de alta y `fecha_estado`, la del último cambio de estado
  (`null` mientras siga abierta). Preguntas: "abierta" o "respondida".
- **`migrar`.** Convierte un `notas_tablero.json` del v1, que trae listas de strings:
  - cada hallazgo pasa a `{id: "hN", semana, texto, estado: "abierta", fecha, fecha_estado: null}`, con `N` correlativo
    (después del mayor que ya exista); `semana` es el `ini` de la semana si el texto nombra una sola semana sin ambigüedad
    (una fecha dd/mm o un nombre de hoja "DDMM - DDMM") y `null` si no; `fecha` es la fecha de corte de la carpeta de origen
    (`salidas/<fecha>/`);
  - cada pregunta pasa a `{id: "pN", texto, estado: "abierta"}`;
  - un texto que ya existe (igual, sin contar espacios) no se duplica.
- **Arrastre al v1.** Solo lleva los hallazgos y las preguntas "abierta". Después de `--sembrar-revisadas`, los hallazgos
  que describían los errores de carga ya resueltos no aparecen ni en M5.5 ni en el v1.

### 7.4 Skill `informe-semanal` y README

El skill reemplaza los pasos 1, 3, 4 y 6 por estos:

1. Copiar lo que se subió a `datos/AAAA-MM-DD_<nombre>.xlsx`, sin borrar lo anterior. Pedir el Registro completo solo si cambiaron los cheques o los inversores.
2. Correr `python3 actualizar.py --dry-run` y mostrar el plan. Si hay algo bloqueante, frenar y preguntar.
3. Correr `python3 actualizar.py` (la primera vez, con `--sembrar-revisadas`).
4. Resumir `validaciones.json` en una línea. Lo que el dueño dé por resuelto va a `revisadas` (Claude traduce "la fila 120
   del 12/10" o "lo de la caja sin moneda" a su clave).
5. Publicar a partir de `salidas/estado_publicacion.json`. Para cada tablero que ya tenga `url`, primero `Artifact read` y después publicar la ruta fija con ese `url`. La primera vez, el v2 se publica como un Artifact **nuevo** (sin pisar el v1) y se guarda su URL con `--guardar-url`.
   - **Respaldos** (`datos/` y `salidas/` no están en git y la sesión puede arrancar vacía). Si falta la URL de un tablero,
     antes de crear uno nuevo se busca con `Artifact list` por título: "Tablero semanal" (v2) y "Tablero Registro General"
     (v1); si aparece, se guarda con `--guardar-url`. Si falta `notas_manuales.json` y no hay ningún
     `tablero_v2_datos.json` local, antes de correr `actualizar.py` se reconstruyen las notas y `revisadas` desde `notas` del
     JSON del último v2 publicado (`Artifact read`; sin clave, el paquete está en claro).
6. El asesor es opcional y corre solo si piden "el informe". El chequeo del "Resultado estimado" aplica al informe, no al tablero.
7. `--clave` deja de ser el camino por defecto.

En el README, agregar:
- la sección "Actualización semanal (un paso)", con las opciones de `actualizar.py`, las salidas y rutas fijas del v2, `notas_manuales.json` y `estado_publicacion.json`;
- los archivos nuevos, en la estructura.

En `docs/metodologia.md`, una sección corta "Tablero v2" que remita a este documento.

## 8. Criterios de aceptación

Se verifican con Playwright (`/opt/pw-browsers/chromium`), tanto en el artifact como en `Tablero_v2_<fecha>.html` abierto con
`file://`. Los datos se verifican contra `tablero_v2_datos.json`, con una tolerancia de ±1 USD. Las capturas van solo al
scratchpad. Cada criterio lleva su prioridad. Los números no se corren: los agregados en la revisión van del 29 al 35.

**v1**
1. (P0) `git diff --quiet registro/tablero.py registro/tablero_plantilla.html` no muestra cambios.
2. (P0) `correr.py` con los tres archivos y `--fecha 2026-10-18 --tablero --artifact --sin-clave`, corrido con el código anterior a los cambios (un `git worktree` del commit base) y con el código nuevo, sobre salidas temporales con el mismo `notas_tablero.json`, genera artifacts v1 idénticos byte a byte.

**Datos**
3. (P0) `v == 2` y están todas las claves y columnas de 4.2, también las de módulos P1 (aunque vengan vacías).
4. (P0) Para cada semana, `Σ cubo.usd` y `Σ n` coinciden con `operaciones.csv` filtrado como `V`. En particular, en 12/10–18/10.
5. (P0) La semana doble conserva `sem.usd` y su `u` se divide por `k = 2`.
6. (P0) Con la última semana cerrada, la suma de `pend_sem` en esa semana es igual a `M["13_pendientes"]` (`items`, `nos_deben_usd`, `les_debemos_usd`).
7. (P0) En cada semana, `saldo_real_usd − caja_real_usd` (sumado) es igual a `debemos − nos_deben` de `pend_sem`.
8. (P0) `precios` del foco coincide con el promedio ponderado recalculado desde `operaciones.csv`. Las filas de `comis` por `tipo_com` suman lo mismo que `T["06 Comisiones por tipo"].operaciones`.
9. (P0) Ninguna clave del JSON coincide con la regex prohibida. Tampoco los textos de `alertas`, `control` y `metodo`, después de reemplazar por un marcador los strings que vienen de la planilla (sección 1, "Alcance de la regex"). `metodo` no trae la línea del v1 que menciona "resultado".
10. (P0) El HTML pesa menos de 800 KB: el payload real ronda los 90 KB, y antes de cada republicación hay que leer el archivo completo.
29. (P0) En USD, `saldo_real(w) = Balance(w+1)` (sin PyG, tolerancia 1) en todas las transiciones con `formato_actual`, salvo las filas con `confiable = 0`. En particular, en 11/05–17/05 (Cierre antes del bloque de abajo), el USD billete coincide con el Balance de la semana siguiente gracias a la rama de 4.3.
30. (P0) Para cada inversor, `|tasa_mensual × monto_usd − interes_mensual_usd| ≤ 1`, y ninguna `tasa_mensual` pasa de 0,1 (10% mensual).
31. (P0) `pend` con `w = foco` y `momento = 0` suma lo mismo que `pend_sem` de `foco` (ítems, nos deben, debemos, `mas4`, `sin_ope` y cada tramo de antigüedad); si hay `en_curso`, lo mismo con `momento = 1`. En cada fila de `pend_sem`, `a01 + a24 + a512 + a12 + sin_ope = items`.
32. (P0) `retiro_mes`: "Octubre" con corte 2026-10-18 da "2026-10" (y A02 salta); "Septiembre" con el mismo corte da "2027-09".
33. (P0) Ningún cliente que muestra M2.5 tiene operaciones en `(w, f]`, ni con el foco por defecto ni con un foco anterior. Todos los `w`, `w_origen`, `ult_w` y `vuelve_w` no nulos del JSON son ≥ 0.
34. (P0) Después de `--sembrar-revisadas`, M5.5 no muestra hallazgos abiertos de antes del 19/10, el `notas_tablero.json` arrastrado al v1 no los trae y las preguntas quedan igual.
35. (P0) Dos corridas con los mismos datos y distinta fecha de corte dan las mismas `claves` en A11; al agregarlas a `revisadas`, A11 de atención sale de la portada. C12 no cuenta columnas con saldo 0 ni las de `cajas_ignoradas`.

**Pantalla**
11. (P0) A 390×844 no hay scroll horizontal (`scrollWidth ≤ 390`) en ninguna sección, en ninguno de los dos temas, ni con las hojas inferiores abiertas.
12. (P0) El encabezado mide 52 px o menos. Los botones de la barra inferior miden 48 px o más. La primera pantalla de Semana muestra las alertas y los indicadores 1 a 4.
13. (P0) `innerText` de cada sección, con todos los `<details>` abiertos y con los strings de la planilla reemplazados por un marcador (sección 1), no coincide con la regex prohibida.
14. (P0) Por defecto el foco es la última semana completa y la lista de M4.2 se ve. Con Registro + Act. 15/10, la última está en curso: aparece el banner y, al elegirla, se ve "en curso", sin %; M4.2 muestra la lista de la semana en curso y M5.2 dice "Se revisa al cerrar la semana".
15. (P0) Con los tres archivos, el indicador 1 muestra el volumen del criterio 4 con el formato `USD … k`.
16. (P0) Con el período "4 sem", el ranking coincide con pandas. En la primera carga, M2.4 coincide con A05. (El chip de puesto es P1.)
17. Un toque (con `hasTouch`) actualiza la franja de lectura sin cambiar el foco, y "Ver esta semana" sí lo cambia (P0). Las flechas del teclado también actualizan la franja (P1).
18. (P0) El botón de tema cambia `--bg`. Con `prefers-color-scheme: dark`, la página arranca oscura.
19. (P0) Con `localStorage` lanzando excepciones, la página carga igual. No hay errores en la consola ni pedidos de red.
20. (P1) Con `--clave`: la clave se pide dentro de la página, una incorrecta muestra un aviso en línea y la correcta carga los datos. No aparece ningún `alert`.
21. (P0) El artifact no tiene doctype, `html`, `head` ni `body`, y conserva `<title>Tablero semanal</title>`.
22. (P0) Cada gráfico tiene `role="img"`, `aria-label` y "Ver como tabla".

**Flujo**
23. (P0) `--dry-run` no escribe nada.
24. (P0) Con los tres archivos en `datos/`, la base es el Registro y la fecha de corte es 2026-10-18. Pasar los archivos con `--archivos` en orden inverso da el mismo resultado.
25. (P0) Con la Act. 19/10 sola, C05 o C06 bloquean, el código de salida es 2 y la ruta fija no cambia.
26. (P1) Una hoja sin Cierres no corta el proceso y aparece C04.
27. (P0) Una clave agregada a `revisadas` se ve como "Revisada dd/mm" y deja de contar en A01 y en el indicador 8. Una clave vieja `<ini>#<fila>` también vale, y una clave con Ope sigue valiendo si se inserta una fila más arriba (cambia la fila, no el Ope).
28. (P0) `notas_tablero.json` se arrastra, solo con lo abierto, y el v1 lo muestra.

## 9. Fuera de alcance

- Estimaciones de ganancia, resultado o rentabilidad, y la conciliación con el archivo de patrimonio.
- Marcar revisadas o editar datos desde el tablero: se hace por chat (más adelante se puede evaluar guardar ese estado en el Artifact).
- Confirmar el signo de los pendientes, los códigos de la columna E y las unidades de inversiones y garantías. Quedan como preguntas.
- Unificar clientes parecidos y asignar moneda a las cajas nuevas: solo se avisa (C12 y C14).
- Feriados.
- Cambio de año: por ahora solo el aviso C16 (las claves por fecha ya lo preparan).
- Cambios en los análisis, el Excel, `metricas.json`, el asesor o el v1.
- Descargas, impresión, exportación y librerías de gráficos.
- Cualquier cifra que combine una diferencia de precio con un volumen (sección 1).

## 10. Cambios de la revisión del 19/10

- **Caja (4.3):** rama para el Cierre antes del bloque de abajo (primera semana con saldos) y columna `caja.confiable`.
- **Inversores (4.1):** `tasa_mensual` = interés ÷ monto, o `tasa_hoja / 100` siempre; nunca según el tamaño del valor.
- **Pendientes (4.2, M4.2, M4.3):** `pend` trae `w` y `momento`, con la foto del foco y la de la semana en curso;
  `pend_sem` trae los tramos de antigüedad.
- **Índices (4.1):** `comis.tipo_com`; `revisar.tipo` es texto; operador crudo en `revisar` y `calidad`;
  `historia_altas_desde_semana` es un `w`; ningún índice negativo en el ejemplo.
- **Definiciones:** M2.5 excluye a los que volvieron (`vuelve_w`); el indicador 8 cuenta las filas de `f`; `retiro_mes`
  cuenta el mes del corte; ventanas de clientes en semanas de calendario.
- **Regex (1):** se aplica a los textos que genera el tablero, no a los que vienen de la planilla; nada de diferencia ×
  volumen.
- **Notas (7.1, 7.3):** `migrar` definido; `--sembrar-revisadas` también resuelve los hallazgos existentes; el arrastre al
  v1 lleva solo lo abierto; respaldos si se pierden `estado_publicacion.json` o `notas_manuales.json`.
- **Control (3.2, 7.2):** claves `control:<id>:<contenido>` sin fecha de corte; C12 sin columnas en 0 y con
  `cajas_ignoradas`; A11 de atención solo con avisos sin revisar.
- **Revisadas:** clave `<ini>#<fila>#<ope>`, coincidencia por Ope con respaldo por fila; a la vista, "Fila 120 · 12–18 oct".
- **Alcance:** P0 y P1 en cada módulo, paso y criterio; contrato completo y módulos ocultos si no están.
- **Visual (6):** `--op-resto` y `--dato` claros corregidos con el validador de `dataviz`; encabezado de 52 px en todos lados;
  indicadores 6 y 8 en dos líneas de 17 px; HTML de menos de 800 KB.

## 11. Cambios de la revisión del panel (19/10, después de la primera entrega)

- **Caja propia (3.1, M4.1, A02, glosario):** el indicador 7 y M4.1 muestran `caja_real` como "Caja propia" y suman la cifra
  que el dueño reconoce, "En la planilla (Balance)". El conmutador es Caja propia | Saldo de la planilla (Balance). Una caja
  propia negativa lleva una nota que la explica. A02 compara el retiro contra el Balance (la caja propia ya descuenta el
  capital del inversor) y dice las dos cifras.
- **Textos de las alertas (3.2):** lo esencial en los primeros ~90 caracteres (A02, A03); A11 dice qué aviso es; las
  revisadas van con OK y fecha.
- **Promedios (M1.3, glosario):** la línea del gráfico es la "Tendencia: promedio móvil de 4 semanas (incluye la semana)";
  "Promedio de 4 semanas" queda para `P4`.
- **Severidades (indicador 8, M5.2, C17, A01):** "graves" y "menores" en lugar de "Altas" y "Medias".
- **Clientes (4.4):** se cuentan por presencia en `cubo`, también los de USD 0, como en Python.
- **Control (7.2):** C10 y C11 sobre la última semana cerrada; C12 en lenguaje llano; nada de `config.json` a la vista.
- **Notas (7.1, 7.3):** `notas_tablero.json` viejos no reabren notas; el sembrado tiene tope; los campos que no son del
  contrato se conservan.
- **Visual (6):** espacio duro entre unidad, número y k/M; tablas sin desplazamiento lateral a 390 px (columnas `.p3` y,
  en la mezcla de productos, una columna "Resto" cuando el módulo es angosto, también en escritorio); campos de búsqueda de 16 px; `--crit-ink` para el
  texto crítico y nada de `opacity` en lo revisado (contraste AA); controles de 44 px.
