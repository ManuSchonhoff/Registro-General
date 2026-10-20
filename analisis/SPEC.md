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
| Ganancia según la planilla | La celda "Ganancia Neta" | = `var(t)` desde `2303 - 2903` (en las primeras hojas medía otra cosa; se muestra solo en la tabla, para conciliar) |
| **Retiros de socios** `ret(t)` | Plata que sacaron los socios (dividendos, liquidación de un ex socio). No es pérdida | Columna DIVIDENDOS de la hoja (lo que la fórmula de Egresos resta de ella) **+** retiros cargados en `config.value.retiros` para esa semana (los que no están en DIVIDENDOS: marzo 22.672; 3.573 y 924,16 que la planilla tiene dentro de INTERESES) |
| **Ajustes a mano** `aj(t)` | Cambios de los valores fijos escritos a mano en el bloque (USDT General, Deuda): se generaron en otro período o son correcciones | `Σ` sobre los renglones fijos (los que la fórmula del Neto suma como constante): `valor(t) − valor(t−1)`. Hoy: +10.900 (13–19/04), −1.000 (11–17/05), +4.021 (25–31/05), +15.855,49 (12–18/10) |
| **Ganancia de la semana** (la principal) `gan(t)` | Lo que ganó el negocio en la semana | `var(t) + ret(t) − aj(t)` ("sin ajustes") |
| Ganancia con ajustes | Lo mismo, incluyendo los ajustes a mano | `var(t) + ret(t)` |
| **Egresos del negocio** `gas(t)` | Gastos, comisiones pagadas, intereses a inversores e inversión de la semana | `egr(t) − ret_dentro_de_egresos(t)`, desglosado por tipo según el coeficiente de cada columna en la fórmula de Egresos (GASTOS y FIJOS → Gastos; COMISIONES; INTERESES menos lo reclasificado como retiro; INVERSION) |
| **Antes de gastos** | Lo que dejó la operación antes de pagar gastos, comisiones, intereses e inversión | `gan(t) + gas(t)` (con o sin ajustes según el interruptor) |
| **Por semana** | Para comparar semanas de distinto largo | valor ÷ (`d(t)` ÷ 7). Solo cambia la hoja doble |
| **Semana típica** | Referencia para decir si una semana estuvo arriba o abajo de lo habitual | Mediana de la ganancia por semana (sin ajustes) de las **8 hojas anteriores** a la semana foco |

Control: `gan_con_ajustes(t) + gas(t)` = Ganancia Bruta de la planilla + retiros que no están en Egresos. El auditor lo
verifica semana por semana.

### 3.3 Mes

- **Regla de mes:** cada hoja va al mes de su **jueves** (= el mes con más días de la semana). Para la hoja doble, el
  jueves de su segunda semana (20/08 → agosto). Reproduce los meses cerrados del Value CG (abril 52.366,61 y mayo
  29.747,29 de variación + dividendos de la columna).
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
| Dólares billete | CARA CHICA, CAMBIO, MALOS, USD, USD BsAs | Disponible |
| Cripto | USDT (caja), TRX, USDT General (columna) | Disponible |
| Exterior y euros | LLC, Grabify y variantes, PayPal Ruso, CITY BANK, WISE US, PAYONEER, WISE, EUROS, REALES, LIBRAS | Disponible |
| Participación USDT General | renglón "USDT" del bloque (valor fijo a mano) | Fijo a mano |
| Deuda a cobrar | renglón "Deuda" del bloque (valor fijo a mano) | Fijo a mano |
| Garantías | MILLAMAPU, JEEP, GOL TREND, CHARCAS, PROMAR | Netean 0: no se dibujan |
| Egresos e ingresos de la semana | GASTOS, FIJOS, COMISIONES, INVERSION, INTERESES, DIVIDENDOS, ALQUILERES | Netean 0 en el Neto: no se dibujan |

- **Disponible** = Pesos + Dólares billete + Cripto + Exterior y euros. **Inmovilizado** = Proyectos. **Fijo a mano** =
  USDT General + Deuda. Las tres suman el patrimonio.
- **Columna sin título:** hereda el nombre de la misma columna de la hoja anterior si allí tenía uno (hoy `AH` →
  "POLIGONO 20+13") y queda marcada para revisar. Si no tiene de dónde heredar, va a "Sin nombre" (Disponible) y
  dispara un chequeo.
- **Pesos en ARS** `ars(t)` = aporte del grupo Pesos × `cot(t)`.
- **Efecto estimado del dólar** = `ars(t−1) × (1/cot(t) − 1/cot(t−1))`. Es una aproximación (supone que los pesos
  quedaron quietos toda la semana): se muestra solo en el detalle y en el bloque "Pesos y dólar", nunca se resta de la
  ganancia.
- **Sensibilidad** = `ars(t)/cot(t) − ars(t)/(cot(t)+10)`: cuánto baja el patrimonio si el dólar sube $ 10.

### 3.5 Socios

- % y aporte de cada socio: `config.value.socios` (de la hoja Tenencia: Manuel, Francisco y Jose 28,13 % y 20.000;
  Alejo 15,62 % y 11.111,11).
- **Capital al último cierre de Tenencia** (30/06): se lee de la hoja Tenencia (última fila con capital por socio). Se
  muestra con su fecha; **no** se proyecta como Neto × %.
- **Parte de la ganancia del período** = ganancia del período (con ajustes, porque la ganancia de USDT General es de la
  sociedad) × % del socio. Responde "¿cuánto gané yo desde tal fecha?". Se avisa que los % suman 100,01 %.
- **Dividendo según la regla de la Tenencia** = 10 % de la ganancia del mes (con ajustes), para los meses posteriores al
  último cierre de Tenencia. Rotulado "sugerido por la regla; no registrado".

---

## 4. Estructura

Una sola página que se recorre de arriba abajo (no hay pestañas): resumen arriba, después el porqué y al final la
consulta. Encabezado fijo con el nombre, la semana foco y una fila de chips que salta a cada sección.

### 4.1 Encabezado y filtros (fijos)

- **Título** "Value · Cambio General" y **chip de semana foco** ("12–18 oct ▾"): abre la lista de semanas (la más nueva
  arriba, con sus marcas). Elegir una cambia la foco (tarjetas, composición, detalle).
- **Línea de estado:** "Cierre del domingo 18/10 · Dólar $ 1.535 · Euro USD 1,25 · Tenencia al 30/06".
- **Filtros globales** (una fila): **Período** [Todo · Últimos 3 meses · Últimas 8 semanas · Desde… ] (el "Desde" deja
  elegir la semana de inicio y la de fin) y **Ajustes** [Sin ajustes · Con ajustes]. Afectan a gráficos, tarjetas de
  período, socios y tabla. Por defecto: Todo y Sin ajustes.

### 4.2 Secciones

1. **Resumen** (primera pantalla)
   - Cuatro tarjetas: **Patrimonio neto** (número principal) · **Ganancia de la semana** · **Ganancia del mes** ·
     **Disponible**. Cada una con una sublínea que evita el error más común y su "?".
     - Patrimonio: "+X desde el 01/03 · N veces lo aportado (71.111)"; sublínea "La mitad está en proyectos: ver
       Disponible".
     - Ganancia de la semana: la **cuenta de la semana** en renglones (antes de gastos → gastos → ganancia → ajustes y
       retiros → el patrimonio subió). Comparación con la semana típica en palabras ("por encima / en línea / por
       debajo de lo habitual"), sin rojo ni verde.
     - Ganancia del mes: total del mes de la foco, "N de M semanas" si está en curso, y "por semana" contra el mes
       anterior por semana.
     - Disponible: monto y % del patrimonio; "Proyectos X (al costo) · Fijos a mano X".
   - **Franja "Para tener en cuenta"**: hasta 3 avisos (5 en escritorio), con ícono, frase y número, cada uno abre su
     semana. Se arman solos con los chequeos y las marcas.
   - **Patrimonio semana a semana**: línea con área suave, eje en 0, eje X de tiempo real. Rótulos solo en el inicio,
     el final y el máximo salto. Íconos de eventos bajo el eje. Lectura fija arriba del gráfico (semana, patrimonio,
     variación). Tocar = cambiar foco; "Ver semana" abre el detalle.

2. **Ganancia**
   - Cortes propios: [Por semana | Por mes] y [Después de gastos | Antes de gastos].
   - Barras con base en 0 (un solo color; negativas hacia abajo). Ajuste ◆ como segmento claro apilado (solo con
     "Con ajustes"; con "Sin ajustes" queda el ícono). Semana doble con doble ancho y alto por semana. Línea fina en la
     mediana del período ("semana típica"). Mes en curso solo con contorno.
   - Encabezado de la sección: "En el período: X (Y por semana, N semanas)".
   - **Cómo venimos**: tabla corta que compara tramos por semana: últimas 8 semanas, el resto del período, y lo mismo
     sin las semanas a revisar.
   - Tocar un mes filtra las barras semanales a ese mes.

3. **¿Dónde está la plata?** (semana foco)
   - Barras horizontales divergentes por grupo (orden fijo de 3.4), con monto y %. Las negativas, a la izquierda con
     "(debemos)".
   - Evolución: área apilada de 3 series (Disponible · Proyectos · Fijos a mano). Si en alguna semana una serie es
     negativa, se dibujan líneas en vez de área apilada.
   - **Pesos y dólar**: "$ 180,1 M ≈ USD 117.360 (33 %) · si el dólar sube $ 10, el patrimonio baja ≈ USD 765 · efecto
     estimado del dólar en el período: X".

4. **Gastos**
   - Barras por mes agrupadas, mismo eje: "Antes de gastos" y "Gastos" (gastos + comisiones + intereses + inversión).
     La diferencia es la ganancia del mes, rotulada.
   - Tabla por mes con el desglose por tipo. Retiros de socios en una fila aparte ("no es gasto").

5. **Socios**
   - Barra de tenencia (4 segmentos) y tabla: socio · % · aporte · capital al 30/06 · parte de la ganancia del período.
   - "Meses sin repartir": mes · ganancia (con ajustes) · 10 % según la regla · por socio.
   - Retiros registrados: fecha, monto, detalle, "a confirmar" cuando corresponde.

6. **Todas las semanas**: tabla (la más nueva arriba): semana · patrimonio · ganancia · antes de gastos · gastos ·
   retiros · ajustes · según la planilla · cotización · marcas. En el celular, 3 columnas y el resto al tocar.

7. **¿Le creo a estos números?**: lista de chequeos con ícono y palabra (OK · Revisar · Info). Más "Cómo se calcula"
   (las fórmulas de la sección 3, en palabras) y el **glosario**.

**Detalle de una semana** (hoja inferior en el celular, panel lateral en escritorio): cabecera con ‹ ›; tres números
(patrimonio, ganancia, gastos); la cuenta de la semana; "¿De dónde salió?" (cascada por grupo, del patrimonio anterior
al actual, con la parte de pendientes); marcas con su explicación; tabla de cajas (moneda original, saldo, pendiente,
USD, variación; cajas en cero escondidas detrás de "ver todas"); cotización (y si se repitió), efecto estimado del
dólar; lo operado (volumen pegado a mano) contra las referencias 2 % / 1 % / 0,5 % de la planilla, sin veredicto;
"Ver en la planilla: hoja X, celda B16".

### 4.3 Interacciones

- Lectura fija arriba de cada gráfico (no tooltip flotante en el celular; tooltip en escritorio con el mismo texto).
- Tocar/clic una barra o punto: cambia la semana foco; botón "Ver semana" abre el detalle. Teclado: flechas
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
| ⚠ Dato dudoso | Cotización igual a la de la hoja anterior, columna sin título, valores que no entran en la fórmula, nota "NO CONTAR"/"REVISAR" en el bloque | Chequeos automáticos |
| • Gastos grandes | Semana de costos fijos | gastos ≥ `config.value.umbral_gastos_grandes` (5.000) |

Cada marca va con ícono y palabra, nunca solo color. Color de estado (`--warn`) solo para ? y ⚠.

---

## 6. Textos de ayuda y glosario

**Ayuda de cada tarjeta y gráfico** (botón "?"): *Qué es · Cómo se calcula · De dónde sale* (hoja y celda). Textos
base (el código los completa con los números):

- **Patrimonio neto.** Qué es: lo que vale Cambio General al cierre del domingo, todo pasado a dólares: cajas (con
  sus pendientes), proyectos al costo, la parte de USDT General y lo que nos deben. No es todo plata disponible. Cómo se
  calcula: pesos ÷ cotización de la semana, euros × 1,25. De dónde sale: Calculadora, "Neto" (B16); en el Value CG se
  llama CAPITAL.
- **Ganancia de la semana.** Qué es: cuánto creció el patrimonio contra el domingo anterior, sumando lo que retiraron
  los socios (no es una pérdida) y sin los ajustes a mano. No es plata que entró: también la mueven el dólar y los
  pendientes. Cómo se calcula: patrimonio − patrimonio anterior + retiros − ajustes. De dónde sale: Calculadora
  ("Ganancia Neta", B17) y los retiros cargados en la configuración.
- **Antes de gastos.** Lo que dejó la operación antes de pagar gastos, comisiones, intereses a inversores e inversión.
  En la planilla: "Ganancia Bruta" (sin los dividendos).
- **Ajustes a mano.** Cambios en los valores fijos del bloque (USDT General y Deuda). Ejemplo: +15.855 de USDT General
  ganados de mayo a septiembre y cargados el 18/10.
- **Semana típica.** La mediana de la ganancia de las 8 semanas anteriores: la mitad de las semanas ganó más y la mitad
  menos. No la mueve una semana extraordinaria.
- **Disponible.** Pesos, dólares billete, cripto y cuentas del exterior, con sus pendientes. Sin proyectos ni valores
  fijos a mano.
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
| D2 | **Ajustes por defecto** (viz: con; usuario y riesgos: sin) | **Sin ajustes** por defecto, con el ajuste siempre visible (ícono ◆ y renglón en la cuenta de la semana) y el interruptor para incluirlo | El error más caro es repartir dividendos sobre una ganancia inflada. "Con ajustes" queda a un toque y la tabla trae la ganancia según la planilla para conciliar |
| D3 | **Mes de cada semana** (datos/viz/negocio: jueves; riesgos: domingo) | Mes del jueves | Reproduce exacto los meses cerrados del Value CG |
| D4 | **Veredicto por volumen** (usuario lo pide; datos y riesgos dicen que el volumen es poco confiable) | Sin veredicto en la primera pantalla: se compara con la semana típica. El volumen y las referencias del dueño (2 / 1 / 0,5 %) se muestran en el detalle, rotulados "cargado a mano" | El volumen está copiado en varias hojas y solo existe en la Calculadora desde mayo; un veredicto sobre él daría una conclusión falsa con aspecto de precisa |
| D5 | **Agrupar el patrimonio** (viz: 6 grupos; usuario: 4 partes; riesgos: por naturaleza) | 7 grupos por caja para la foto y 3 (Disponible · Proyectos · Fijos a mano) para la evolución y la tarjeta | Cubre las tres miradas: dónde está cada peso y cuánto es plata disponible |
| D6 | **Semanas sin explicar** (usuario: sacarlas del promedio; viz: marcarlas; riesgos: mostrar ambas cifras) | Se marcan con ? y se incluyen en los totales; "Cómo venimos" muestra los tramos con y sin ellas; la semana típica usa mediana | No se puede afirmar que no sean ganancia; tampoco que lo sean |
| D7 | Efecto del dólar (riesgos: barra aparte; viz: solo detalle) | Solo en el detalle y en "Pesos y dólar", rotulado "estimado" | Es una aproximación: restarlo de la ganancia mezclaría un número estimado con los de la planilla |
| D8 | Retiros dentro de INTERESES (3.573 el 27/04–03/05; 924,16 el 06–12/07) | Se tratan como retiros, marcados "a confirmar" | Coinciden exacto con los dividendos del Value CG (`T25`, `T39`) |
| D9 | Ajuste de USDT General (15.855,49) | Queda en la semana en que se cargó (12–18/10) como ◆; no se reparte por mes | Las liquidaciones no tienen fecha; repartirlo sería inventar |
| D10 | Saltos de los valores fijos de abril y mayo (+10.900, +4.021, −1.000) | Se tratan como ajustes a mano igual que el de octubre | Mismo mecanismo; no hay forma de saber si fueron ganancia de esa semana |
| D11 | Columna `AH` sin título | Hereda "POLIGONO 20+13" de la hoja anterior y va a Proyectos; queda en "Revisar" | Es la misma columna con el mismo saldo; sacarla rompería el cierre con el Neto |
| D12 | Serie | Empieza el 23/02–01/03 (primera hoja). La historia anterior del Value CG no se muestra | Hueco de 7 meses, carga a mano y 48,74 de diferencia el 01/03 |
| D13 | Socios | Capital solo de Tenencia (al 30/06); la parte de cada socio se calcula sobre la ganancia del período, no sobre el Neto | El capital por socio no es Neto × % (riesgo 16) |
| D14 | Pendientes | Se suman como los suma la planilla; nota fija de que su signo está a confirmar; el detalle muestra cuánto de la variación vino de pendientes | No hay base para corregirlos (`signo_pendientes_confirmado: false`) |
| D15 | Ganancias de las primeras hojas | Se recalculan como diferencia de Netos (la celda guardada medía otra cosa) | Una sola definición para toda la serie |

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
