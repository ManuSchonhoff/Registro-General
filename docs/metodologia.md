# Metodología de los análisis

Todos los montos en USD salen de `config.json`. Si se cambian las cotizaciones, hay que volver a
correr `correr.py`.

## Base común

- **Operaciones consideradas:** filas con `Fin` marcado, dentro del bloque de operaciones de cada
  semana (sin los bloques de pendientes de arriba y de abajo).
- **Volumen** (análisis 1, 2, 3, 8, 9, 10): solo `Detalle` = Cajas y Recaudadora; sin clientes
  `USDT General` ni `Cambio General`; sin filas con cajas que no son divisas (garantías, gastos).
- **Promedio neto USD** = (Debe en USD + Haber en USD) / 2. Una operación de 1.000 USD contra pesos
  cuenta como 1.000.
- **Cotizaciones:**
  - ARS: mediana semanal de las cotizaciones USD↔Pesos operadas, o el valor fijado en config.
  - USDT: **paridad semanal observada** = cotización en pesos del USDT (filas USDT General) dividida
    la del USD billete. Ronda 1,02–1,05: el USDT vale más que el billete.
  - EUR 1,23 USD (mediana operada; mercado ~1,17). BRL 4,8. USD exterior 1:1.
- **Clientes:** se agrupan quitando lo que va entre paréntesis y normalizando acentos
  ("Cliente (detalle)" → "Cliente").

## Por análisis

1. **Ranking:** volumen por cliente, % del total, % acumulado, HHI (índice de concentración: menos de
   1.500 es baja, de 1.500 a 2.500 moderada, más de 2.500 alta).
2. **Altas y bajas:** primer mes de cada cliente. "Perdido" = 3 o más operaciones y sin operar hace
   más de 4 semanas completas.
3. **Cliente ↔ operador:** volumen por par; clientes exclusivos de un operador.
4. **Spread billete:** operaciones USD↔Pesos billete y USD↔Transferencia con cotización entre 900 y
   2.500. Por día y canal: cotización media de venta − de compra. Ganancia = spread × USD calzados
   (el mínimo entre lo comprado y lo vendido ese día). Por operador: ganancia de cada operación frente
   al precio medio del día.
5. **Circuito USDT:** se emparejan la fila del cliente y la fila `USDT General` que mueve la misma
   transferencia (hasta 3 filas antes). Ganancia = USD del cliente − USDT pagados × paridad. **Es muy
   sensible a la paridad USDT/billete.**
6. **Comisiones:** operaciones con cotización entre 0,01 y 15 (porcentaje), por tipo. Comisión = valor
   que entra − valor que sale, en USD. Excluye cheques (análisis 7) y euros (su cotización no es un %).
7. **Cheques:** hojas CQ y Donato – Poligono, sin duplicados. "En cartera" = ni cobrado ni colocado.
   Ganancia = columna Comisión, solo cuando la fila tiene tasa y el valor es menor al 60% del monto.
8. **Evolución:** volumen por semana y mes y por producto (billete, transferencia, USDT, exterior,
   cheques, divisas, canje de billetes, recaudación).
9. **Día de la semana:** fecha inferida de los Cierre diarios. Es aproximada.
10. **Tamaño:** tramos de USD por operación y ticket por operador.
11. **Calidad de carga:** imputación ≠ Debe/Haber (descontando la comisión de 1,5 USDT), canceladas
    con imputación y filas sin estado con imputación. Se descartan pares vecinos que se compensan.
    Severidad por USD: Alta ≥ 100, Media ≥ 10.
12. **Posición:** Balance (saldo real) y Balance + Apertura (caja real) al inicio de cada semana del
    formato actual (desde el 11/05), por moneda. Efecto del tipo de cambio = pesos de la semana
    anterior × variación de 1/cotización. Inversiones y garantías van aparte, en su unidad original.
13. **Pendientes:** bloque de arriba de la semana actual. Antigüedad por número de Ope. Signo según
    `contexto_negocio.md` (a confirmar).
14. **Fondeo:** hoja Inversores (capital, tasa, interés mensual comprometido) frente a los ingresos
    operativos estimados.
15. **Gastos:** `Detalle` = Gastos, por categoría (palabras clave) y por semana.

**Resultado estimado** = spread + circuito USDT + comisiones + cheques − gastos − intereses
comprometidos. **No** incluye resultados de inversiones, diferencias de cambio sobre la posición,
spread de euros y reales ni ajustes. Es una aproximación para comparar contra la ganancia
semanal del archivo de patrimonio, no la reemplaza.
