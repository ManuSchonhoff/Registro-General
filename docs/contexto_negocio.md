# Contexto del negocio y del Registro General

Documento de referencia para cualquier análisis o agente que trabaje sobre el registro.
Resume cómo funciona la planilla. Si algo cambia en el proceso, actualizarlo acá.

## Qué es

Financiera / casa de cambio ("Cambio General"). Opera compra y venta de USD billete, pesos en
efectivo y por transferencia, USDT, USD en cuentas del exterior (LLC, Grabify/Grabifi, Wise,
Payoneer), euros y reales. También hace recaudación (convierte transferencias en efectivo con
comisión), descuento de cheques, préstamos, y administra dinero de inversores a los que les paga
interés mensual. Parte del capital está invertido en proyectos (Polígono, Almafuerte, Carbox) o
tomado en garantía (Millamapu, Charcas, Promar, Jeep, Gol Trend).

**Operadores:** Manuel y Francisco (los principales), Jose, Dante, Coco y Vago.

## La planilla

- Un Google Sheet con **una pestaña por semana** (`DDMM - DDMM`), de lunes a domingo. La semana
  `1008 - 2308 (Dos Semanas)` abarca dos.
- Cada fila es una operación: `Fin / Pen / Can` (finalizada, pendiente, cancelada), `Ope` (número
  correlativo de todo el año), `Detalle` (Cajas, Recaudadora, Préstamos, Deuda, Gastos, Comisión,
  Intereses, Ajuste…), `Cliente`, `Operador`, `Debe (Entra)` + caja, `Cotización / Comisión`,
  `Haber (Sale)` + caja.
- **Cotización / Comisión** puede ser una cotización (pesos por USD, ~1.400–1.600), una
  cotización EUR/USD (~1,2), reales por USD (~4,8) o un porcentaje de comisión (0–15).
- Columnas R en adelante: **una por caja**. Ahí se imputa a mano el efecto de cada operación (+ entra,
  − sale). Grupos: Caja chica USD (Cara chica, Cambio, Malos), Billete (USD, Pesos, Cheques, USD
  BsAs, Deudas), Transferencias (Transfer, USDT, TRX, USDT General), USD exterior, Divisas,
  Garantías, Inversiones, Egresos (Gastos, Comisiones) e Ingresos (Inversión, Intereses, Alquileres).
- **Cara chica** = billetes de USD viejos; **Malos** = billetes dañados; **Cambio** = billetes chicos.
  Se canjean con descuento.
- **USDT General** = la contraparte con la que se compran o venden USDT contra transferencias. El
  circuito típico es este: el cliente entrega USD billete, se le transfieren pesos, y esa transferencia
  la hace la contraparte a cambio de USDT. Las filas de USDT General **no son volumen de clientes**,
  porque duplicarían la misma operación.

## Cierre semanal (proceso del dueño)

1. Cierre semanal.
2. Se abren pendientes: las operaciones abiertas se pasan **abajo del todo** (las filas originales
   quedan en cero).
3. Se cierran una a una, pasando el saldo a la **cuenta corriente** de cada uno.
4. Se cierra la hoja y se abre la nueva.
5. Los pendientes vuelven **arriba del todo**.

En la hoja nueva:
- Fila 5 `Balance – Cambio General` = **saldo real** (= último `Cierre` de la semana anterior, que
  incluye los pendientes). Se pega como valores.
- Fila 6 `Apertura Pendientes` = −(suma de pendientes). Se pega a mano.
- Filas 7 a `Cierre Pendientes`: los pendientes y cuentas corrientes, uno por fila.
- Después, las operaciones del día y una fila `Cierre` por día (`=SUM` desde el Cierre anterior).

**Saldo real = caja real + pendientes.** El dueño convierte los saldos a USD en **otro archivo
(análisis de patrimonio)** y compara semana a semana para obtener la ganancia semanal.

### Signo de los pendientes (a confirmar con el dueño)

Positivo en una caja = la contraparte nos entregó valor (por ejemplo, el inversor depositó: lo
debemos). Negativo = le entregamos valor (nos debe: préstamos, gastos de Carbox, transferencias de
USDT General sin USDT confirmado). Se dedujo de ejemplos como Dardo Fava (préstamos +, retiros "España" −).

**Pregunta abierta importante:** si los pendientes positivos son deudas con terceros, el patrimonio
propio es la **caja real** (sin pendientes) más lo que nos deben, menos lo que debemos. Hay que
confirmar cómo lo calcula el archivo de patrimonio.

## Hojas auxiliares

- **CQ, Donato – Poligono, CQ – Rossi, CQ – Hipoteca:** cartera de cheques (cobrado/colocado,
  vencimiento, tasa mensual ~8%, débitos y créditos 1,2%, comisión, destino).
- **Inversores:** capital por inversor, destino (Bankz, Donato, Polígono, Caja CG), tasa mensual.
- **Lorena, Marco, Marchi, Brandon, Dardo, Pato, Rossi – 15k:** cuentas de inversores con interés compuesto.
- **Datos:** listas de los desplegables.

## Problemas conocidos de los datos (ver chequeo general)

- Algunos `Cierre` quedaron vacíos o con rangos cortos (por ejemplo, la semana actual al 02/10).
- La `Apertura Pendientes` de PESOS no coincidió con la suma de pendientes en 6 semanas (−200.000
  recurrente; coincide con una pendiente de Ana Victoria Brazzola).
- Imputaciones que no coinciden con Debe/Haber, filas canceladas con imputación y signos invertidos.
- 41 pendientes de `USDT General` con "?" (transferencias sin USDT confirmado) de más de 4 semanas.
- La hoja `Brandon` está copiada de `Lorena`. Hay fechas mal cargadas.
- Los `Cierre` diarios no siempre tienen fecha: el día de cada operación es aproximado.
