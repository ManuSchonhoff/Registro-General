# Registro USDT General: cómo funciona la planilla

Documento de referencia del Excel del libro propio de **USDT General**, la mesa que compra y vende USDT contra pesos
por transferencia. En el Registro General de Cambio General, USDT General aparece como contraparte; acá está su lado
del negocio. Solo describe la lógica: los montos y los hallazgos concretos van en `salidas/`, que no se versiona.

## Quién es dueño de qué

- **Libro principal** (hojas `Registro USDT General-(MES)`): la ganancia se reparte en **tercios** entre los dos
  socios y Cambio General.
- **Libro Coco** (hojas `MES-COCO`): operaciones de Coco. La ganancia se reparte entre USDT General y el referente
  que trae clientes (hoja `CLIENTES MARIANO`).

## Hojas

| Hoja | Qué es |
|---|---|
| `Registro USDT General (Mes)` (formato viejo, 2025 a feb-2026) | Libro mensual, rangos de 500 o 1.000 filas |
| `Registro USDT General-(MES)` (desde mar-2026) | Libro mensual principal, rango 3:2000 |
| `MES - COCO` / `MES-COCO` | Libro mensual de Coco, misma estructura |
| `CLIENTES MARIANO` | Ventas a clientes del referente y su comisión |
| `RESULTADO USDT GENERAL` | Resultado mensual, impuestos, gastos, reparto y retiros |
| `Intercambio USDT General - Camb` | Cuenta corriente con Cambio General (histórica, 2025) |
| `Caja USDT- GENERAL ` | Caja diaria de USDT (histórica, abandonada) |

## Hoja mensual (principal y Coco)

Dos listas independientes en la misma hoja. Las filas de la izquierda y la derecha **no se corresponden** entre sí.

**Ventas de USDT (A–I):** `A` fecha (solo en la primera fila de cada día), `B` ID (orden de Binance, hash de la
transacción o, a veces, un ID arrastrado con el sufijo incrementado), `C` USDT bruto, `D` comisión, `E = C + D` USDT
que salen, `F = G / E` precio, `G` ARS que entran, `H` canal, `I` banco.

**Compras de USDT (K–S):** `K` fecha, `L` ID, `M` USDT bruto, `N` comisión, `O = M − N` USDT que entran,
`P = Q / O` precio, `Q` ARS que salen, `R` canal, `S` banco.

**Fila 2 (totales):** sumas de `C`, `E`, `G`, `M`, `O` y `Q`; `F2 = G2/E2` precio medio de venta; `P2 = Q2/O2`
precio medio de compra; `D2 = N2 = 0,0016` es una tasa de referencia que no se usa en las sumas.

- `U2` **Restan** `= G2 − Q2`: pesos cobrados por ventas menos pesos pagados por compras.
- `V2` **Ganancia (USDT)** `= O2 − E2`: USDT comprados menos USDT vendidos.
- `W2 = V2 / E2` margen; `X2 = V2 × P2` ganancia en pesos.

**Lógica:** se vende USDT caro y se recompra barato con los mismos pesos. Cuando el ciclo de pesos cierra
(`U2 = 0`), los USDT que sobran son la ganancia. **`V2` solo es correcta si `U2 = 0`.**
**Ganancia ajustada = `V2 + U2 / P2`.** El mes se "cierra" cuando los pesos cuadran, aunque eso pase unos días dentro
del mes siguiente. Un mes abierto (`U2` grande) muestra una ganancia sin sentido, a veces negativa.

**Comisión:** en las ventas por Binance se suma la comisión (~0,14%) a los USDT que salen; en las compras se resta de
los que entran. Las filas de wallet, transferencias y OTC van sin comisión. No se registra el costo de red.

**Restos y notas:** el bloque `U4:X40` ("Fecha / Inicio / Final / Ganancia") es un resto vacío del formato viejo.
Las columnas `J`, `T`, `Y` y `Z` tienen cuentas sueltas de control (copias de montos, asteriscos de revisado).

## CLIENTES MARIANO

Una fila por venta a un cliente del referente: `A` FIN (casilla), `B` fecha, `D` ARS recibidos, `G` USDT enviados,
`F = D/G` precio, `I = F − 30` "cotización de compra" (en algunas filas ±25) y `J = D/I − G`, la ganancia en USDT de
ese margen. Se reparte **50% para el referente** y 50% para el libro que hizo la operación. Las liquidaciones se
anotan a mano en `K:Q` por bloques de filas, no por mes calendario.

## RESULTADO USDT GENERAL

- **Bloques del libro principal (2025 y 2026):** `B` BRUTO cargado **a mano** y redondeado desde `V2` de cada hoja;
  `C` impuestos = 15% del bruto; `D` gastos operativos (a mano); `E` NETO = B − C − D; `F:H` tercio de cada socio;
  `I:K` retiros; `DISPONIBLE` = acumulado − retiros.
- **Bloque 2026 de Coco:** `B` bruto (= `V2` de la hoja Coco), `C` 15%, `D` gastos, `E` neto, `G` parte del
  referente (mitad de su `J`), `F = E − G` parte de USDT General, `I:J` retiros.

## Chequeos que conviene automatizar

- `U2 ≠ 0` en un mes cerrado: corregir con `V2 + U2/P2`.
- Bloques de filas repetidos (misma secuencia de USDT y ARS) y repeticiones exactas de ID, USDT, ARS y canal.
- Precios de una fila lejos de la mediana del día (ventas por debajo del precio de compra).
- Fórmulas de NETO en RESULTADO que no restan los gastos, y BRUTO distinto del `V2` de la hoja.
- Fechas fuera de orden dentro de una hoja.
- Parte del referente que no se reproduce sumando `J` del período.
