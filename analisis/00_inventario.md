# 00 — Inventario de datos (Value · Cambio General)

Generado por `analisis/inventario.py` el 2026-10-20 a partir de `datos/value/`. Este archivo registra **solo hechos** (estructura, tipos, rangos, fórmulas, referencias); no interpreta. Montos tal como están en las celdas (sin convertir). Formato numérico: punto de miles, coma decimal.

En las hojas con listas de operaciones de clientes (Comisiones, Dante) los valores de texto se reemplazan por su cantidad: `CLAUDE.md` prohíbe versionar información de clientes.

## Archivos

| Archivo | Tamaño | SHA-256 (12) | Hojas | Visibles | Ocultas |
|---|---|---|---|---|---|
| `2026-10-20_Value_CG_2026.xlsx` | 369 KB | 29d4a5c77b2a | 10 | 5 | 5 |
| `2026-10-20a_Calculo_Semanal.xlsx` | 1.535 KB | da7bf443b852 | 36 | 36 | 0 |
| `2026-10-20b_Calculo_Semanal_1210-1810.xlsx` | 13 KB | fb11eae37f91 | 1 | 1 | 0 |

**Hojas con el mismo nombre en más de un archivo:** `1210 - 1810` en `2026-10-20a_Calculo_Semanal.xlsx`, `2026-10-20b_Calculo_Semanal_1210-1810.xlsx`.

## Archivo `2026-10-20_Value_CG_2026.xlsx`

### Hojas

`Dimensión` es el rango que declara el archivo (incluye celdas con formato sin datos). `Filas con datos` cuenta filas con al menos una celda no vacía.

| Hoja | Estado | Dimensión | Filas con datos | Celdas no vacías | Fórmulas | Fórmulas con error | Celdas combinadas | Formatos condicionales | Validaciones |
|---|---|---|---|---|---|---|---|---|---|
| `Dashboard` | visible | A1:M53 | 22 | 83 | 46 | 0 | 55 | 0 | 0 |
| `Value CG` | visible | A1:X79 | 78 | 628 | 354 | 0 | 7 | 0 | 1 |
| `Tenencia` | visible | A1:Q129 | 25 | 169 | 96 | 0 | 5 | 0 | 0 |
| `Value 2025` | hidden | A1:N70 | 70 | 365 | 187 | 136 | 0 | 0 | 0 |
| `Value 2026` | hidden | A1:T71 | 70 | 273 | 72 | 0 | 6 | 0 | 1 |
| `Vago` | hidden | A1:Z1002 | 10 | 54 | 13 | 0 | 2 | 0 | 0 |
| `Liquidacion Seven` | hidden | A1:F17 | 13 | 32 | 5 | 0 | 2 | 0 | 0 |
| `Dante` | hidden | A1:Z995 | 69 | 579 | 13 | 0 | 0 | 0 | 0 |
| `Comisiones` | visible | A1:Z1368 | 391 | 3321 | 186 | 0 | 0 | 0 | 5 |
| `Poligono 00-09` | visible | A1:Z1000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Hoja `Dashboard` (visible)

Celdas combinadas: K27:L28, I30:I31, E39:E40, K30:K31, H36:I37, B3:F3, D46:E46, E27:F28, H50:I50, D45:E45, H27:I28, F30:F31, B39:B40, B36:C37, H39:H40, L30:L31, E36:F37, H46:I46, D49:E49, F51:G51, B2:L2, F45:G45, H49:I49, H51:I51, J49:K49, J45:K45, F50:G50, K39:K40, D48:E48, L39:L40 ….

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–1 | texto 1 | 0 | 0 | 0 | — | DASHBOARD CAMBIO GENERAL |
| B | 2–43 | texto 10, número 2 | 2 | 30 | 0 | 27,82 a 266.647,58 | CAPITALES, Capital Actual, DASHBOARD - PATRIMONIO, DETALLE SEMANAL (Ulitmas 6 Semanas), Evolucion Balance Real (USD), Evolucion de Capital, Mensual , RENTABILIDAD Y EFICIENCIA, Renta Sobre Capital Prom., Resumen General - Datos de la Hoja "Value CG" |
| C | 38–51 | fecha 6, texto 2, número 1 | 7 | 5 | 0 | 2026-05-17 a 2026-06-21; números 4,80 a 4,80 | Fecha, Semanal |
| D | 45–51 | número 6, texto 1 | 6 | 0 | 0 | 247.280,96 a 266.647,58 | Capital |
| E | 27–39 | texto 4, número 2 | 2 | 7 | 0 | 40.487,05 a 195.536,47 | Capital, Ganancia Neta Total, Ganancia Prom., Mensual  |
| F | 29–51 | número 8, texto 3 | 8 | 12 | 0 | 274,97 a 195.536,47 | Ganancia, Renta, Semanal |
| H | 3–51 | número 8, texto 6 | 8 | 35 | 0 | -0,90 a 54.527,86 | Bruto Prom., Ganancia Semanal (USD), Max / Min Ganancia Mensual, Maxima, Mensual , Var |
| I | 29–39 | texto 2, número 2 | 2 | 7 | 0 | 12.196,11 a 28.122,00 | Minima, Semanal |
| J | 45–51 | número 6, texto 1 | 6 | 0 | 0 | 6.372,72 a 10.760,66 | Bruto |
| K | 27–39 | texto 5, número 2 | 2 | 6 | 0 | 37.660,15 a 2.185.525,51 | Max / Min Ganancia Semanal, Maxima, Mensual , Renta Sobre Vol., Volumen Prom. |
| L | 29–39 | número 3, texto 2 | 3 | 6 | 0 | -2.310,60 a 498.502,56 | Minima, Semanal |

Textos de la columna A: A1 `DASHBOARD CAMBIO GENERAL`.

Fórmulas: 46. Muestra (hasta 25): B29 `='Value CG'!B36` → 266.647,58; E30 `=AVERAGE('Value CG'!E32,'Value CG'!E26,'Value CG'!F20,'Value CG'!E12)` → 40.487,05; F30 `=AVERAGE('Value CG'!E5,'Value CG'!E7:E11,'Value CG'!E15:E19,'Value ...` → 10.339,49; H30 `=AVERAGE('Value CG'!H12,'Value CG'!H20,'Value CG'!H26,'Value CG'!H32)` → 54.527,86; I30 `=AVERAGE('Value CG'!H8:H11,'Value CG'!H15:H19,'Value CG'!H21:H25,'V...` → 12.196,11; K30 `=AVERAGE('Value CG'!I20,'Value CG'!I26,'Value CG'!I32)` → 2.185.525,51; L30 `=AVERAGE('Value CG'!I15:I19,'Value CG'!I21:I25,'Value CG'!I28:I31,'...` → 498.502,56; L32 `=AVERAGE('Value CG'!J15:J19,'Value CG'!J21:J25,'Value CG'!J28:J31)` → 1,93; B39 `=AVERAGE('Value CG'!F5,'Value CG'!F12,'Value CG'!G20,'Value CG'!F26...` → 27,82; C39 `=AVERAGE('Value CG'!F8:F11,'Value CG'!F15:F19,'Value CG'!F21:F25,'V...` → 4,80; E39 `='Value CG'!C36` → 195.536,47; F39 `='Value CG'!D36` → 274,97; H39 `=MAX('Value CG'!E5,'Value CG'!E12,'Value CG'!F20,'Value CG'!E26,'Va...` → 52.366,61; I39 `=MIN('Value CG'!E5,'Value CG'!E12,'Value CG'!F20,'Value CG'!E26,'Va...` → 28.122,00; K39 `=MAX('Value CG'!E5,'Value CG'!E7:E11,'Value CG'!E15:E19,'Value CG'!...` → 37.660,15; L39 `=MIN('Value CG'!E7:E11,'Value CG'!E5,'Value CG'!E15:E19,'Value CG'!...` → -2.310,60; C46 `='Value CG'!A29` → 2026-05-17; D46 `='Value CG'!B29` → 247.280,96; F46 `='Value CG'!C29` → 176.169,85; H46 `='Value CG'!F29` → 3,70; J46 `='Value CG'!H29` → 10.436,68; C47 `='Value CG'!A30` → 2026-05-24; D47 `='Value CG'!B30` → 252.329,06; F47 `='Value CG'!C30` → 181.217,95; H47 `='Value CG'!F30` → 2,04.

Referencias a otras hojas en fórmulas: `Value CG` (46).

### Hoja `Value CG` (visible)

Celdas combinadas: G1:H2, I1:J2, W1:X2, U1:V2, C1:F2, A1:B2, K1:T2.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–79 | fecha 51, texto 27 | 0 | 1 | 0 | 2025-07-01 a 2027-01-03 | 17 valores distintos (primeros: Abril, Agosto, Anual, Aportes, Balance Actual, …) |
| B | 3–39 | número 36, texto 1 | 13 | 0 | 0 | 69.985,48 a 266.647,58 | CAPITAL |
| C | 1–38 | número 29, texto 2 | 29 | 7 | 0 | -5.456,00 a 195.536,47 | NETO, P&L APORTE |
| D | 3–38 | número 28, texto 1 | 28 | 7 | 0 | 40,18 a 274,97 | VARxCAP |
| E | 3–38 | número 29, texto 1 | 26 | 6 | 0 | -2.310,60 a 52.366,61 | GANxCORTE |
| F | 3–38 | número 29, texto 1 | 28 | 6 | 0 | -0,90 a 35.702,58 | VARxCORTE |
| G | 1–38 | número 29, texto 2 | 24 | 7 | 0 | 21,31 a 468.691,27 | BRUTO |
| H | 3–38 | número 27, texto 1 | 27 | 8 | 0 | 1.250,62 a 71.150,27 | BRUTOxSEM |
| I | 1–38 | número 22, texto 2 | 4 | 14 | 0 | 311.721,47 a 2.407.541,90 | VOLUMEN |
| J | 3–38 | número 22, texto 1 | 22 | 13 | 0 | -0,48 a 3,87 | RENTA |
| K | 1–38 | número 28, texto 2 | 26 | 8 | 0 | 38.499,06 a 120.928,32 | EGRESOS, GASTOS |
| L | 3–38 | número 27, texto 1 | 6 | 8 | 0 | 67,28 a 9.047,99 | GxSEMANA |
| M | 3–38 | número 10, texto 1 | 10 | 25 | 0 | 86,33 a 3.046,57 | COMISIONES |
| N | 3–38 | número 10, texto 1 | 2 | 25 | 0 | -71,86 a 1.966,35 | COMI x Sem |
| O | 3–38 | número 28, texto 1 | 25 | 7 | 0 | 16.109,44 a 34.103,47 | INVERSION |
| P | 3–38 | número 27, texto 1 | 6 | 8 | 0 | 0 a 4.083,67 | IxSEMANA |
| Q | 3–38 | número 18, texto 1 | 18 | 17 | 0 | 4.752,00 a 16.249,56 | INTERESES |
| R | 3–38 | número 17, texto 1 | 4 | 18 | 0 | 0 a 6.585,56 | IxSem |
| S | 3–39 | número 22, texto 1 | 22 | 14 | 0 | 22.672,00 a 34.398,16 | DIVIDENDOS |
| T | 3–39 | número 21, texto 1 | 4 | 15 | 0 | 0 a 22.672,00 | DIVxSem |
| U | 1–38 | número 5, texto 2 | 5 | 31 | 0 | 900,00 a 4.500,00 | ALQUILERES, INGRESOS |
| V | 3–38 | número 5, texto 1 | 1 | 30 | 0 | 0 a 4.500,00 | ALQxSEM |
| W | 1–38 | número 27, texto 2 | 16 | 9 | 0 | 10.760,00 a 25.681,00 | COMPLEMENTOS, USDT General |
| X | 3–38 | número 25, texto 1 | 8 | 10 | 0 | 4.000,00 a 5.000,00 | Deuda |

Textos de la columna A: A1 `PATRIMONIO`; A3 `GLOBAL`; A4 `Aportes`; A6 `Dividendos`; A12 `Febrero`; A13 `Aportes`; A18 `Balance Actual`; A20 `Marzo`; A26 `Abril`; A27 `Dividendos`; A32 `Mayo`; A33 `Dividendos`; A38 `Junio`; A39 `Dividendos`; A44 `Julio`; A45 `Dividendos`; A51 `Agosto`; A52 `Dividendos`; A57 `Septiembre`; A58 `Dividendos`; A63 `Octubre`; A64 `Dividendos`; A70 `Noviembre`; A71 `Dividendos`; A77 `Diciembre`; A78 `Dividendos`; A79 `Anual`.

Primera fila con 4 o más textos (fila 1): `PATRIMONIO`, `NETO`, `BRUTO`, `VOLUMEN`, `EGRESOS`, `INGRESOS`, `COMPLEMENTOS`.

Fórmulas: 354. Muestra (hasta 25): C5 `=B5-63438` → 28.122,18; D5 `=C5*100/B4` → 40,18; B6 `=B5+C6` → 86.104,18; C6 `=-1680-1750-1174-852` → -5.456,00; B7 `=116962.09-117.35-4846.95+W7+5300-4294` → 123.764,33; C7 `=SUM(B7-B4)` → 53.778,85; D7 `=C7*100/B4` → 76,84; E7 `=B7-B6` → 37.660,15; F7 `=E7*100/B6` → 43,74; K7 `=117.35+608.96+(83224.23-40996.88)+K5` → 81.452,72; O7 `=4846.95+595.04+17644-15894+O5` → 23.301,43; W7 `=5205.27+5555.27` → 10.760,54; B8 `=135556.23+W8+5300-4294` → 147.322,77; C8 `=B8-B4` → 77.337,29; D8 `=C8*100/B4` → 110,50; E8 `=B8-B7` → 23.558,44; F8 `=E8*100/B7` → 19,03; H8 `=E8+L8` → 28.976,82; K8 `=5418.38+K7` → 86.871,10; L8 `=K8-K7` → 5.418,38; P8 `=O8-O7` → 0; W8 `=W7` → 10.760,54; B9 `=140924.15+W9+X9` → 156.684,69; C9 `=B9-$B$2` → 156.684,69; D9 `=C9*100/$B$4` → 223,88.

Referencias a otras hojas en fórmulas: `Value 2025` (1).

### Hoja `Tenencia` (visible)

Celdas combinadas: O2:P2, M2:N2, K2:L2, I2:J2, B2:D2.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| B | 2–17 | texto 7, número 6 | 0 | 3 | 0 | -76.143,00 a 151.673,07 | Alejo*, Aportes y Tenencia, Francisco, Jose, Manuel, Socio, Total |
| C | 3–17 | texto 7, número 5 | 1 | 3 | 0 | 11.111,11 a 71.111,11 | Aportes, C/U, Capital, Capital Triunvi a Julio, Decimo, Ganancia Periodo Triunvi, Vago |
| D | 3–8 | número 5, texto 1 | 1 | 0 | 0 | 0,16 a 1,00 | Tenencia |
| F | 2–26 | texto 25 | 1 | 0 | 0 | — | Abril, Agosto, Cierre, Diciembre, Dividendos, Febrero, Julio, Julio 2025, Junio, Liquidacion Cura, Marzo, Mayo, Noviembre, Octubre, Septiembre |
| G | 2–14 | número 12, texto 1 | 9 | 0 | 0 | 86.104,18 a 265.424,68 | Capital |
| H | 2–14 | número 11, texto 2 | 10 | 0 | 0 | -16.222,98 a 81.791,87 | -, Ganancia Periodo |
| I | 2–14 | número 12, texto 1 | 10 | 0 | 0 | -2.150,00 a 78.516,70 | Manuel (28,13%) |
| J | 7–14 | número 8 | 8 | 0 | 0 | -1.573,51 a 15.735,07 | — |
| K | 2–14 | número 12, texto 1 | 10 | 0 | 0 | -2.150,00 a 78.516,70 | Jose (28,13%) |
| L | 7–14 | número 8 | 8 | 0 | 0 | -1.573,51 a 15.735,07 | — |
| M | 2–14 | número 12, texto 1 | 11 | 0 | 0 | -2.150,00 a 78.516,70 | Francisco (28,13%) |
| N | 7–14 | número 8 | 8 | 0 | 0 | -1.573,51 a 15.735,07 | — |
| O | 2–14 | número 11, texto 2 | 11 | 0 | 0 | 9.961,18 a 29.886,60 | Alejo (15,63%), Liquidado |
| P | 7–14 | número 8 | 8 | 0 | 0 | -873,74 a 8.737,35 | — |
| Q | 10–14 | texto 3 | 0 | 2 | 0 | — | No |

Primera fila con 4 o más textos (fila 2): `Aportes y Tenencia`, `Cierre`, `Capital`, `Ganancia Periodo`, `Manuel (28,13%)`, `Jose (28,13%)`, `Francisco (28,13%)`, `Alejo (15,63%)`.

Fórmulas: 96. Muestra (hasta 25): F3 `=("Julio 2025")` → Julio 2025; M3 `=K3` → 25.381,00; O3 `=G3-I3-K3-M3` → 9.961,18; H4 `=G4-G3` → 81.791,87; I4 `=(G4-O4)/3` → 46.853,99; K4 `=I4` → 46.853,99; M4 `=K4` → 46.853,99; O4 `=11111.11+13118.09+3104.89` → 27.334,09; G5 `=G4-16222.98` → 151.673,07; H5 `=G5-G4` → -16.222,98; I5 `=(G5-O5)/3` → 46.853,99; K5 `=I5` → 46.853,99; M5 `=K5` → 46.853,99; O5 `=11111.11` → 11.111,11; G6 `=G5+SUM(I6:M6)` → 145.223,07; G7 `='Value 2026'!B11` → 180.926,63; H7 `=G7-G6` → 35.703,56; I7 `=SUM(I5:I6)+J7` → 54.747,40; J7 `=H7*28.13/100` → 10.043,41; K7 `=I7` → 54.747,40; L7 `=J7` → 10.043,41; M7 `=K7` → 54.747,40; N7 `=L7` → 10.043,41; O7 `=O5+(15.62*H7/100)` → 16.688,01; P7 `=H7*15.62/100` → 5.576,90.

Referencias a otras hojas en fórmulas: `Value 2026` (1).

### Hoja `Value 2025` (hidden)

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–70 | fecha 51, texto 19 | 0 | 0 | 0 | 2025-07-01 a 2027-01-03 | 19 valores distintos (primeros: Abril, Agosto, Anual, Aportes, Cura, …) |
| B | 1–70 | texto 47, número 13 | 51 | 10 | 46 | 12.577,48 a 167.896,05 | #REF!, CAPITAL |
| C | 1–68 | texto 51, número 7 | 52 | 10 | 45 | -5.456,00 a 97.910,57 | #REF!, -, GANxCAP |
| D | 1–68 | texto 51, número 6 | 51 | 11 | 45 | 40,18 a 139,90 | #REF!, -, VARxCAP |
| E | 1–14 | texto 7, número 7 | 5 | 0 | 0 | 2.019,66 a 44.131,72 | -, GANxCORTE |
| F | 1–14 | texto 7, número 7 | 6 | 0 | 0 | 1,29 a 43,74 | -, VARxCORTE |
| G | 1–13 | número 6, texto 1 | 2 | 6 | 0 | 146.168,68 a 279.098,96 | BRUTO |
| H | 1–14 | texto 9, número 5 | 5 | 0 | 0 | 4.970,69 a 55.580,48 | -, BRUTOxSEM |
| I | 1–13 | texto 7, número 6 | 5 | 0 | 0 | 38.499,06 a 88.933,16 | -, GASTOS |
| J | 1–14 | texto 9, número 5 | 2 | 0 | 0 | 67,28 a 7.480,44 | -, GxSEMANA |
| K | 1–13 | texto 7, número 6 | 4 | 0 | 0 | 16.109,44 a 27.269,75 | -, INVERSION |
| L | 1–14 | texto 9, número 5 | 2 | 0 | 0 | 0 a 3.968,32 | -, IxSEMANA |
| M | 1–13 | texto 8, número 5 | 2 | 0 | 0 | 10.760,54 a 10.760,54 | -, USDT General |
| N | 1–13 | número 3, texto 1 | 0 | 9 | 0 | 5.000,00 a 5.000,00 | Deuda |

Textos de la columna A: A1 `GLOBAL`; A2 `Aportes`; A3 `Francisco`; A4 `Jose`; A5 `Manuel`; A6 `Cura`; A8 `Dividendos`; A14 `Febrero`; A20 `Marzo`; A25 `Abril`; A31 `Mayo`; A36 `Junio`; A41 `Julio`; A47 `Agosto`; A52 `Septiembre`; A57 `Octubre`; A63 `Noviembre`; A69 `Diciembre`; A70 `Anual`.

Primera fila con 4 o más textos (fila 1): `GLOBAL`, `CAPITAL`, `GANxCAP`, `VARxCAP`, `GANxCORTE`, `VARxCORTE`, `BRUTO`, `BRUTOxSEM`, `GASTOS`, `GxSEMANA`, `INVERSION`, `IxSEMANA`, `USDT General`, `Deuda`.

Fórmulas: 187. Muestra (hasta 25): C7 `=B7-63438` → 28.122,18; D7 `=C7*100/B2` → 40,18; B8 `=B7+C8` → 86.104,18; C8 `=-1680-1750-1174-852` → -5.456,00; B9 `=116962.09-117.35-4846.95+M9+5300-4294` → 123.764,33; C9 `=SUM(B9-B2)` → 53.778,85; D9 `=C9*100/B2` → 76,84; E9 `=B9-B8` → 37.660,15; F9 `=E9*100/B8` → 43,74; I9 `=117.35+608.96+(83224.23-40996.88)+I7` → 81.452,72; K9 `=4846.95+595.04+17644-15894+K7` → 23.301,43; M9 `=5205.27+5555.27` → 10.760,54; B10 `=135556.23+M10+5300-4294` → 147.322,77; C10 `=B10-B2` → 77.337,29; D10 `=C10*100/B2` → 110,50; E10 `=B10-B9` → 23.558,44; F10 `=E10*100/B9` → 19,03; H10 `=E10+J10` → 28.976,82; I10 `=5418.38+I9` → 86.871,10; J10 `=I10-I9` → 5.418,38; L10 `=K10-K9` → 0; M10 `=M9` → 10.760,54; B11 `=140924.15+M11+N11` → 156.684,69; C11 `=B11-$B$2` → 86.699,21; D11 `=C11*100/$B$2` → 123,88.

Referencias a otras hojas en fórmulas: `REF` (46).

Celdas con error: 136 (por ejemplo B15 #REF!, C15 #REF!, D15 #REF!, B16 #REF!, C16 #REF!, D16 #REF!, B17 #REF!, C17 #REF!).

### Hoja `Value 2026` (hidden)

Celdas combinadas: G1:H2, S1:T2, I1:J2, K1:R2, C1:F2, A1:B2.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–71 | fecha 45, texto 25 | 0 | 1 | 0 | 2026-03-01 a 2027-01-03 | 17 valores distintos (primeros: Abril, Agosto, Anual, Aportes, Balance Actual, …) |
| B | 3–15 | número 12, texto 1 | 2 | 0 | 0 | 71.111,11 a 209.276,60 | CAPITAL |
| C | 1–13 | número 8, texto 3 | 7 | 2 | 0 | 96.429,76 a 123.070,59 | -, NETO, P&L APORTE |
| D | 3–13 | número 8, texto 2 | 7 | 1 | 0 | 135,60 a 173,07 | -, VARxCAP |
| E | 3–13 | número 8, texto 3 | 6 | 0 | 0 | -355,18 a 18.247,23 | -, GANxCORTE |
| F | 3–13 | número 7, texto 4 | 6 | 0 | 0 | -0,21 a 10,37 | (+$35.702,58 Neto), -, VARxCORTE |
| G | 1–13 | número 8, texto 2 | 6 | 3 | 0 | 279.098,96 a 331.603,00 | BRUTO |
| H | 3–13 | número 8, texto 3 | 7 | 0 | 0 | 4.522,77 a 47.981,27 | -, BRUTOxSEM |
| I | 1–13 | número 7, texto 5 | 1 | 1 | 0 | 330.226,94 a 1.770.220,29 | -, VOLUMEN |
| J | 3–13 | número 7, texto 4 | 7 | 0 | 0 | 1,33 a 3,84 | -, RENTA |
| K | 1–13 | número 8, texto 3 | 6 | 2 | 0 | 88.933,16 a 95.692,66 | -, EGRESOS, GASTOS |
| L | 3–13 | número 8, texto 3 | 1 | 0 | 0 | 138,30 a 6.433,38 | -, GxSEMANA |
| M | 3–13 | número 8, texto 2 | 6 | 1 | 0 | 27.269,75 a 28.363,06 | -, INVERSION |
| N | 3–13 | número 8, texto 3 | 1 | 0 | 0 | 0 a 1.093,31 | -, IxSEMANA |
| O | 3–13 | texto 8, número 3 | 3 | 0 | 0 | 4.752,00 a 4.752,00 | -, Intereses |
| P | 3–13 | texto 8, número 2 | 0 | 1 | 0 | 0 a 4.752,00 | -, IxSem |
| Q | 3–13 | texto 5, número 4 | 3 | 2 | 0 | 0 a 22.672,00 | -, DIVIDENDOS |
| R | 3–13 | texto 5, número 4 | 1 | 2 | 0 | 0 a 22.672,00 | -, DIVxSem |
| S | 1–13 | número 8, texto 3 | 1 | 2 | 0 | 10.760,00 a 10.760,54 | -, COMPLEMENTOS, USDT General |
| T | 3–13 | número 8, texto 2 | 1 | 1 | 0 | 5.000,00 a 5.000,00 | -, Deuda |

Textos de la columna A: A1 `PATRIMONIO`; A3 `GLOBAL`; A4 `Febrero`; A5 `Aportes`; A10 `Balance Actual`; A12 `Marzo`; A17 `Abril`; A18 `Dividendos`; A24 `Mayo`; A25 `Dividendos`; A30 `Junio`; A31 `Dividendos`; A36 `Julio`; A37 `Dividendos`; A43 `Agosto`; A44 `Dividendos`; A49 `Septiembre`; A50 `Dividendos`; A55 `Octubre`; A56 `Dividendos`; A62 `Noviembre`; A63 `Dividendos`; A69 `Diciembre`; A70 `Dividendos`; A71 `Anual`.

Primera fila con 4 o más textos (fila 1): `PATRIMONIO`, `NETO`, `BRUTO`, `VOLUMEN`, `EGRESOS`, `COMPLEMENTOS`.

Fórmulas: 72. Muestra (hasta 25): C6 `=B6-B5` → 96.784,94; D6 `=C6*100/$B$5` → 136,10; F6 `=E6*100/'Value 2025'!B12` → 5,79; H6 `=E6+L6+N6` → 10.372,07; J6 `=H6*100/I6` → 1,77; C7 `=B7-$B$5` → 96.429,76; D7 `=C7*100/$B$5` → 135,60; E7 `=B7-B6` → -355,18; F7 `=E7*100/B6` → -0,21; G7 `=G6+H7` → 284.580,16; H7 `=E7+L7+N7` → 5.481,20; J7 `=H7*100/I7` → 1,33; K7 `=K6+L7` → 94.627,19; M7 `=M6+N7` → 27.412,10; C8 `=B8-$B$5` → 104.823,36; D8 `=C8*100/$B$5` → 147,41; E8 `=B8-B7` → 8.393,60; F8 `=E8*100/B7` → 5,01; G8 `=G7+H8` → 294.213,91; H8 `=E8+L8+N8` → 9.633,75; J8 `=H8*100/I8` → 2,03; K8 `=K7+L8` → 94.960,35; M8 `=M7+N8` → 28.319,09; C9 `=B9-$B$5` → 123.070,59; D9 `=C9*100/$B$5` → 173,07.

Referencias a otras hojas en fórmulas: `Value 2025` (1).

### Hoja `Vago` (hidden)

Celdas combinadas: G2:I2, B2:D2.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| B | 2–11 | texto 10 | 0 | 0 | 0 | — | Alejo*, Aportes y Tenencia, Cura, Eduardo, Francisco, Jose, Manuel, Marcelo, Socio, Total |
| C | 3–11 | número 8, texto 1 | 4 | 0 | 0 | 10.000,00 a 80.000,00 | Aportes |
| D | 3–11 | número 8, texto 1 | 1 | 0 | 0 | 0,12 a 1,00 | Tenencia |
| G | 2–10 | texto 9 | 0 | 0 | 0 | — | Alejo*, Aportes y Tenencia, Eduardo, Francisco, Jose, Manuel, Marcelo, Socio, Total |
| H | 3–10 | número 7, texto 1 | 4 | 0 | 0 | 10.000,00 a 71.111,11 | Aportes |
| I | 3–10 | número 7, texto 1 | 4 | 0 | 0 | 0,14 a 1,00 | Tenencia |
| J | 7–7 | texto 1 | 0 | 0 | 0 | — | *Alejo debe aportar esto |

Primera fila con 4 o más textos (fila 3): `Socio`, `Aportes`, `Tenencia`, `Socio`, `Aportes`, `Tenencia`.

Fórmulas: 13. Muestra (hasta 25): C4 `=40000/3` → 13.333,33; H4 `=40000/3` → 13.333,33; I4 `=(28.125%*2)/3` → 0,19; C5 `=C4` → 13.333,33; H5 `=H4` → 13.333,33; I5 `=I4` → 0,19; C6 `=C5` → 13.333,33; H6 `=H5` → 13.333,33; I6 `=I5` → 0,19; H10 `=SUM(H4:H9)` → 71.111,11; I10 `=SUM(I4:I9)` → 1,00; C11 `=SUM(C4:C10)` → 80.000,00; D11 `=SUM(D4:D10)` → 1,00.

### Hoja `Liquidacion Seven` (hidden)

Celdas combinadas: B11:E11, B2:E2.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| B | 2–15 | texto 13 | 0 | 1 | 0 | — | Alejo, Alejo V2, Aportado, Capital Total , Cura, Cura V2, Deudas, Diferencia, Liquidacion, Periodo, Real, Reinversiones, Seven |
| C | 3–15 | número 11 | 5 | 2 | 0 | -11.111,11 a 27.334,09 | — |
| D | 3–15 | texto 8 | 0 | 5 | 0 | — | *Capital Total Completo, *Cedido a Cura, *Deudas Cedidas, *Deudas de Seven, *Neto Aportado, *Total Aportado Nuevo, *Total Liquidado Cash |

Fórmulas: 5. Muestra (hasta 25): C3 `=11111.11+13118.09+3104.89` → 27.334,09; C6 `=SUM(C4:C5)` → 14.618,32; C9 `=C6+C7+C8-C5-C3` → -276,44; C14 `=-16222.98+3104.89+5381.68` → -7.736,41; C15 `=C5` → -5.381,68.

### Hoja `Dante` (hidden)

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 2–70 | texto 69 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| B | 2–70 | texto 69 | 0 | 0 | 0 | — | 26 valores (omitidos: pueden ser nombres de clientes) |
| C | 2–70 | texto 69 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| D | 2–70 | número 69 | 0 | 0 | 0 | 13,29 a 5.000.000,00 | — |
| E | 2–70 | texto 69 | 0 | 0 | 0 | — | 5 valores (omitidos: pueden ser nombres de clientes) |
| F | 2–70 | número 66, texto 3 | 0 | 0 | 0 | 0,03 a 1.480,00 | 2 valores (omitidos: pueden ser nombres de clientes) |
| G | 2–70 | número 69 | 0 | 0 | 0 | 13,50 a 4.200.000,00 | — |
| H | 2–70 | texto 69 | 0 | 0 | 0 | — | 7 valores (omitidos: pueden ser nombres de clientes) |
| K | 4–7 | texto 4 | 0 | 0 | 0 | — | 4 valores (omitidos: pueden ser nombres de clientes) |
| L | 3–7 | número 4, texto 1 | 2 | 0 | 0 | 208,00 a 17.313.238,00 | 1 valores (omitidos: pueden ser nombres de clientes) |
| M | 3–7 | número 4, texto 1 | 1 | 0 | 0 | 3.023,00 a 39.316.636,00 | 1 valores (omitidos: pueden ser nombres de clientes) |
| N | 3–7 | número 4, texto 1 | 4 | 0 | 0 | 1.615,50 a 28.314.937,00 | 1 valores (omitidos: pueden ser nombres de clientes) |
| O | 3–8 | número 5, texto 1 | 5 | 0 | 0 | 1.615,50 a 47.689,96 | 1 valores (omitidos: pueden ser nombres de clientes) |
| P | 7–8 | texto 1, número 1 | 1 | 0 | 0 | 238.449,77 a 238.449,77 | 1 valores (omitidos: pueden ser nombres de clientes) |

Fórmulas: 13 (no se transcriben).

### Hoja `Comisiones` (visible)

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–410 | texto 390 | 0 | 20 | 0 | — | 38 valores (omitidos: pueden ser nombres de clientes) |
| B | 1–407 | texto 379 | 0 | 28 | 0 | — | 84 valores (omitidos: pueden ser nombres de clientes) |
| C | 1–407 | número 190, texto 189 | 7 | 28 | 0 | -3.000,00 a 57.000.000,00 | 3 valores (omitidos: pueden ser nombres de clientes) |
| D | 1–407 | texto 192, número 187 | 0 | 28 | 0 | 100,00 a 51.625.000,00 | 12 valores (omitidos: pueden ser nombres de clientes) |
| E | 1–407 | texto 188, número 188 | 0 | 31 | 0 | 1,00 a 1.758,50 | 11 valores (omitidos: pueden ser nombres de clientes) |
| F | 1–407 | número 374, texto 3 | 20 | 30 | 1 | -4.215.000,00 a 28.905.000,00 | 3 valores (omitidos: pueden ser nombres de clientes) |
| G | 1–407 | texto 189, número 188 | 0 | 30 | 0 | 31,00 a 23.120.000,00 | 10 valores (omitidos: pueden ser nombres de clientes) |
| H | 1–407 | texto 189 | 0 | 218 | 0 | — | 15 valores (omitidos: pueden ser nombres de clientes) |
| I | 1–336 | texto 19, número 16 | 9 | 301 | 0 | 1,00 a 617.562,50 | 7 valores (omitidos: pueden ser nombres de clientes) |
| J | 1–374 | texto 40, número 26 | 12 | 308 | 0 | 0 a 4.500.000,00 | 12 valores (omitidos: pueden ser nombres de clientes) |
| K | 1–376 | número 45, texto 20 | 19 | 311 | 0 | 0 a 342.957,26 | 9 valores (omitidos: pueden ser nombres de clientes) |
| L | 1–376 | número 57, texto 18 | 27 | 301 | 0 | 0 a 196.432.500,00 | 5 valores (omitidos: pueden ser nombres de clientes) |
| M | 1–373 | número 55, texto 11 | 24 | 307 | 0 | 0 a 111.873.000,00 | 4 valores (omitidos: pueden ser nombres de clientes) |
| N | 1–335 | número 49, texto 10 | 19 | 276 | 0 | 0 a 130.995,00 | 3 valores (omitidos: pueden ser nombres de clientes) |
| O | 1–335 | número 25, texto 15 | 11 | 295 | 0 | -200.000,00 a 960.000,00 | 6 valores (omitidos: pueden ser nombres de clientes) |
| P | 1–336 | número 27, texto 16 | 24 | 293 | 0 | -100.027,83 a 4.363.440,00 | 7 valores (omitidos: pueden ser nombres de clientes) |
| Q | 1–134 | número 14, texto 3 | 14 | 117 | 0 | 32.249,00 a 4.126.500,00 | 2 valores (omitidos: pueden ser nombres de clientes) |
| R | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| S | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| T | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| U | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| V | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| W | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| X | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| Y | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |
| Z | 1–1 | texto 1 | 0 | 0 | 0 | — | 1 valores (omitidos: pueden ser nombres de clientes) |

Fórmulas: 186 (no se transcriben).

Celdas con error: 1 (por ejemplo F313 #DIV/0!).

### Hoja `Poligono 00-09` (visible)

Sin datos.

## Archivo `2026-10-20a_Calculo_Semanal.xlsx`

### Hojas

`Dimensión` es el rango que declara el archivo (incluye celdas con formato sin datos). `Filas con datos` cuenta filas con al menos una celda no vacía.

| Hoja | Estado | Dimensión | Filas con datos | Celdas no vacías | Fórmulas | Fórmulas con error | Celdas combinadas | Formatos condicionales | Validaciones |
|---|---|---|---|---|---|---|---|---|---|
| `2302 - 0103` | visible | A1:AB981 | 21 | 145 | 41 | 0 | 0 | 0 | 0 |
| `0203 - 0803` | visible | A1:AB980 | 18 | 141 | 39 | 0 | 0 | 0 | 0 |
| `0903 - 1503` | visible | A1:AC980 | 19 | 145 | 40 | 0 | 0 | 0 | 0 |
| `1603 - 2203` | visible | A1:AC980 | 23 | 164 | 47 | 0 | 0 | 0 | 0 |
| `2303 - 2903` | visible | A1:AD980 | 23 | 169 | 48 | 0 | 0 | 0 | 0 |
| `3003 - 0504` | visible | A1:AD978 | 20 | 153 | 42 | 0 | 0 | 0 | 0 |
| `0604 - 1204` | visible | A1:AD978 | 20 | 159 | 45 | 0 | 0 | 0 | 0 |
| `1304 - 1904` | visible | A1:AE978 | 21 | 159 | 45 | 0 | 0 | 0 | 0 |
| `2004 - 2604` | visible | A1:AE978 | 21 | 158 | 45 | 0 | 0 | 0 | 0 |
| `2704 - 0305` | visible | A1:AE978 | 22 | 163 | 46 | 0 | 0 | 0 | 0 |
| `0405 - 1005` | visible | A1:AF978 | 22 | 167 | 47 | 0 | 0 | 0 | 0 |
| `1105 - 1705` | visible | A1:AG978 | 22 | 170 | 47 | 0 | 0 | 0 | 0 |
| `1805 - 2405` | visible | A1:AG978 | 22 | 171 | 48 | 0 | 0 | 0 | 0 |
| `2505 - 3105` | visible | A1:AG975 | 22 | 200 | 47 | 0 | 1 | 1 | 0 |
| `0106 - 0706` | visible | A1:AH976 | 23 | 208 | 50 | 0 | 1 | 1 | 0 |
| `0806 - 1406` | visible | A1:AI977 | 24 | 223 | 53 | 0 | 1 | 1 | 0 |
| `1506 - 2106` | visible | A1:AI977 | 24 | 215 | 52 | 0 | 1 | 1 | 0 |
| `2206 - 2806` | visible | A1:AI29 | 24 | 219 | 53 | 0 | 1 | 2 | 0 |
| `2906 - 0507` | visible | A1:AI30 | 25 | 220 | 53 | 0 | 1 | 2 | 0 |
| `0607 - 1207` | visible | A1:AI30 | 25 | 217 | 53 | 0 | 1 | 2 | 0 |
| `1307 - 1907` | visible | A1:AJ31 | 26 | 226 | 55 | 0 | 1 | 2 | 0 |
| `2007 - 2607` | visible | A1:AJ31 | 26 | 226 | 55 | 0 | 1 | 2 | 0 |
| `2707 - 0208` | visible | A1:AM31 | 26 | 234 | 54 | 0 | 1 | 2 | 0 |
| `0308 - 0908` | visible | A1:AM31 | 26 | 240 | 57 | 0 | 1 | 2 | 0 |
| `1008 - 2308 (Dos Semanas)` | visible | A1:AN31 | 26 | 245 | 58 | 0 | 1 | 2 | 0 |
| `2408 - 3008` | visible | A1:AN31 | 26 | 242 | 56 | 0 | 1 | 2 | 0 |
| `3108 - 0609` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `0709 - 1309` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `1409 - 2009` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `2109 - 2709` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `2809 - 0410` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `0510 - 1110` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `1210 - 1810` | visible | A1:AN31 | 26 | 244 | 58 | 0 | 1 | 2 | 0 |
| `CONTROL` | visible | A1:AI12 | 9 | 310 | 99 | 0 | 0 | 1 | 0 |
| `Semanales` | visible | A1:I104 | 104 | 183 | 15 | 0 | 1 | 0 | 0 |
| `Volumen Mayo` | visible | A1:Z1000 | 9 | 33 | 6 | 0 | 5 | 0 | 0 |

### Hojas semanales (33: `2302 - 0103` a `1210 - 1810`)

Estructura observada: fila 1 = encabezados de texto (uno por columna), filas 2 y 3 = números cargados como valores, una fila de sumas `=SUM(x2:x3)` por columna y, en las hojas que la tienen, una fila de códigos de moneda (USD, ARS, EUR, REAL). Debajo, desde la fila 7, un bloque de cálculo en las columnas A–C.

| Desde | Hasta | Fila de sumas | Fila de moneda |
|---|---|---|---|
| `2302 - 0103` | `1805 - 2405` | 5 | — |
| `2505 - 3105` | `1210 - 1810` | 4 | 5 |

#### Encabezados de la fila 1 (cajas) y en qué hojas aparecen

| Encabezado | Hojas | Primera | Última | Columnas (letra) | Moneda (fila de moneda) |
|---|---|---|---|---|---|
| CARA CHICA | 29 | `2302 - 0103` | `1210 - 1810` | A | USD |
| CAMBIO | 33 | `2302 - 0103` | `1210 - 1810` | B | USD |
| MALOS | 33 | `2302 - 0103` | `1210 - 1810` | C | USD |
| USD | 33 | `2302 - 0103` | `1210 - 1810` | D | USD |
| PESOS | 33 | `2302 - 0103` | `1210 - 1810` | E | ARS |
| CHEQUES | 33 | `2302 - 0103` | `1210 - 1810` | F | ARS |
| BSAS | 10 | `2302 - 0103` | `2704 - 0305` | G |  |
| DEUDA USD | 33 | `2302 - 0103` | `1210 - 1810` | H | USD |
| DEUDA PESOS | 33 | `2302 - 0103` | `1210 - 1810` | I | USD |
| TRANSFER | 33 | `2302 - 0103` | `1210 - 1810` | J | ARS |
| USDT | 33 | `2302 - 0103` | `1210 - 1810` | K | USD |
| USDT General | 33 | `2302 - 0103` | `1210 - 1810` | L, M, N | USD |
| Grabrfy Manuel | 33 | `2302 - 0103` | `1210 - 1810` | M, N, O | USD |
| LLC | 33 | `2302 - 0103` | `1210 - 1810` | N, O, P | USD |
| PayPal Ruso | 33 | `2302 - 0103` | `1210 - 1810` | O, P, Q | USD |
| Grabify | 20 | `2302 - 0103` | `0607 - 1207` | P, Q, R | USD |
| GRABIFY Jose | 33 | `2302 - 0103` | `1210 - 1810` | Q, R, S | USD |
| CITY BANK | 33 | `2302 - 0103` | `1210 - 1810` | R, S, T | USD |
| GRABIFI | 33 | `2302 - 0103` | `1210 - 1810` | S, T, U | USD |
| WISE | 33 | `2302 - 0103` | `1210 - 1810` | T, U, V | EUR |
| WISE US | 33 | `2302 - 0103` | `1210 - 1810` | U, V, W | USD |
| PAYONEER | 33 | `2302 - 0103` | `1210 - 1810` | V, W, X | USD |
| EUROS | 33 | `2302 - 0103` | `1210 - 1810` | W, X, Y | EUR |
| REALES | 33 | `2302 - 0103` | `1210 - 1810` | X, Y, Z | REAL |
| LIBRAS | 33 | `2302 - 0103` | `1210 - 1810` | Y, Z, AA | None |
| GASTOS | 33 | `2302 - 0103` | `1210 - 1810` | Z, AA, AB, AC, AD, AE, AI, AJ | USD |
| FIJOS | 10 | `2302 - 0103` | `2704 - 0305` | AA, AB, AC |  |
| INVERSION | 33 | `2302 - 0103` | `1210 - 1810` | AB, AC, AD, AE, AF, AG, AK, AL | None, USD |
| 1,00 | 4 | `0903 - 1503` | `3003 - 0504` | A |  |
| bx | 8 | `0903 - 1503` | `2704 - 0305` | L, M |  |
| INTERESES | 29 | `2303 - 2903` | `1210 - 1810` | AD, AE, AF, AG, AH, AL, AM | None, USD |
| TRX | 26 | `1304 - 1904` | `1210 - 1810` | L | USD |
| USD BsAs | 23 | `0405 - 1005` | `1210 - 1810` | G | USD |
| RECAUDACION BX | 23 | `0405 - 1005` | `1210 - 1810` | M | ARS |
| COMISIONES | 23 | `0405 - 1005` | `1210 - 1810` | AC, AD, AE, AF, AJ, AK | USD |
| DIVIDENDOS | 21 | `0405 - 1005` | `1210 - 1810` | AF, AG, AI, AM, AN | None, USD |
| MILLAMAPU | 22 | `1105 - 1705` | `1210 - 1810` | AB | None |
| ALQUILERES | 8 | `0106 - 0706` | `2007 - 2607` | AH, AI | USD |
| POLIGONO | 18 | `0806 - 1406` | `1210 - 1810` | AC, AD, AH, AI | USD |
| Grabify BORRAR | 13 | `1307 - 1907` | `1210 - 1810` | R | USD |
| ALMAFUERTE | 13 | `1307 - 1907` | `1210 - 1810` | AC, AG | USD |
| Dividendos | 2 | `1307 - 1907` | `2007 - 2607` | AJ | USD |
| JEEP | 11 | `2707 - 0208` | `1210 - 1810` | AC | USD |
| GOL TREND | 11 | `2707 - 0208` | `1210 - 1810` | AD | USD |
| CHARCAS | 11 | `2707 - 0208` | `1210 - 1810` | AE | USD |
| PROMAR | 11 | `2707 - 0208` | `1210 - 1810` | AF | USD |
| POLIGONO 20+13 | 1 | `1008 - 2308 (Dos Semanas)` | `1008 - 2308 (Dos Semanas)` | AH | USD |

**Columnas con números en filas 2–3 pero sin encabezado en la fila 1:** `2408 - 3008`!AH, `3108 - 0609`!AH, `0709 - 1309`!AH, `1409 - 2009`!AH, `2109 - 2709`!AH, `2809 - 0410`!AH, `0510 - 1110`!AH, `1210 - 1810`!AH.

#### Bloque de cálculo (A7:C29) por hoja — fórmulas

Etiquetas de la columna A y fórmula o valor de la columna B en cada hoja (las fórmulas van tal cual).

| Hoja | Etiquetas (col. A) → contenido de la col. B |
|---|---|
| `2302 - 0103` | **Dolares** B7: `=SUM(A5:D5,K5:V5,Z5:AB5)`<br>**Pesos** B8: `=SUM(E5+F5+J5)/1410`<br>**Deuda** B9: `5.000,00`<br>**USDT** B10: `10.760,00`<br>**euros** B11: `=W5*1.2`<br>**Egresos** B12: `=-SUM(Z5:AB5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Debe** B18: `602.170,00`<br>**Haber** B19: `568.550,00`<br>**Promedio** B20: `=SUM(B18:B19)/2`<br>**=(B24*100/B20)/100** B24: `=G15` |
| `0203 - 0803` | **Dolares** B7: `=SUM(A5:D5,K5:V5,Z5:AB5)`<br>**Pesos** B8: `=SUM(E5+F5+J5)/1405`<br>**Deuda** B9: `5.000,00`<br>**USDT** B10: `10.760,00`<br>**Egresos** B11: `=-SUM(Z5:AB5)`<br>**Neto** B12: `=SUM(B7:B11)`<br>**Bruto** B13: `=SUM(B7:B10)`<br>**Debe** B17: `347.000,00`<br>**Haber** B18: `475.000,00`<br>**Promedio** B19: `=SUM(B17:B18)/2`<br>**=(B23*100/B19)/100** B23: `=D13` |
| `0903 - 1503` | **Dolares** B7: `=SUM(A5:D5,K5,N5:W5,AA5:AC5)`<br>**Pesos** B8: `=(SUM(E5:J5,L5))/1405`<br>**Deuda** B9: `5.000,00`<br>**USDT** B10: `10.760,00`<br>**Egresos** B11: `=-SUM(AA5:AC5)`<br>**Neto** B12: `=SUM(B7:B11)`<br>**Bruto** B13: `=SUM(B7:B10)`<br>**Ganancia** B14: `=B13-'0203 - 0803'!B12`<br>**Debe** B17: `511.186,79`<br>**Haber** B18: `436.967,89`<br>**Promedio** B19: `=SUM(B17:B18)/2`<br>**=(B23*100/B19)/100** B23: `=B14` |
| `1603 - 2203` | **Dolares** B7: `=SUM(A5:D5,K5,N5:W5,AA5:AC5)`<br>**Pesos** B8: `=(SUM(E5:J5,L5))/1415`<br>**Euros** B9: `=X5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `10.760,00`<br>**Egresos** B12: `=-SUM(AA5:AC5)`<br>**Dividendos** B13: `6.450,00`<br>**Liquidacion** B14: `16.222,00`<br>**Neto** B15: `=SUM(B7:B12)`<br>**Bruto** B16: `=SUM(B7:B11)`<br>**Ganancia** B17: `=B16-'0903 - 1503'!B13`<br>**Debe** B19: `499.219,69`<br>**Haber** B20: `466.950,20`<br>**Promedio** B21: `=SUM(B19:B20)/2`<br>**=(B25*100/B21)/100** B25: `=B17`<br>**=(B26*100/B21)/100** B26: `=C17` |
| `2303 - 2903` | **Dolares** B7: `=SUM(A5:D5,K5,N5:W5,AA5:AD5)`<br>**Pesos** B8: `=(SUM(E5:J5,L5))/1405`<br>**Euros** B9: `=X5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `10.760,00`<br>**Egresos** B12: `=-SUM(AA5:AD5)`<br>**Dividendos** B13: `6.450,00`<br>**Liquidacion** B14: `16.222,00`<br>**Neto** B15: `=SUM(B7:B12)`<br>**Bruto** B16: `=SUM(B7:B11)`<br>**Ganancia Neta** B17: `=B15-'1603 - 2203'!B15`<br>**Debe** B19: `429.791,00`<br>**Haber** B20: `374.325,00`<br>**Promedio** B21: `=SUM(B19:B20)/2`<br>**=(B25*100/B21)/100** B25: `=B17`<br>**=(B26*100/B21)/100** B26: `=C17` |
| `3003 - 0504` | **Dolares** B7: `=SUM(A5:D5,K5,N5:W5,AA5:AD5)`<br>**Pesos** B8: `=(SUM(E5:J5,L5))/C8`<br>**Euros** B9: `=X5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `10.760,00`<br>**Egresos** B12: `=-SUM(AA5:AD5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'2303 - 2903'!B15`<br>**Debe** B17: `315.162,87`<br>**Haber** B18: `345.291,01`<br>**Promedio** B19: `=SUM(B17:B18)/2`<br>**=(B23*100/B19)/100** B23: `=B15` |
| `0604 - 1204` | **Dolares** B7: `=SUM(A5:D5,K5,N5:W5,AA5:AD5)`<br>**Pesos** B8: `=(SUM(E5:J5,L5))/C8`<br>**Euros** B9: `=X5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `10.760,00`<br>**Egresos** B12: `=-SUM(AA5:AD5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'3003 - 0504'!B13`<br>**Debe** B17: `599.247,00`<br>**Haber** B18: `659.752,00`<br>**Promedio** B19: `=SUM(B17:B18)/2`<br>**=(B23*100/B19)/100** B23: `=B15` |
| `1304 - 1904` | **Dolares** B7: `=SUM(A5:D5,K5:L5,O5:X5,AB5:AE5)`<br>**Pesos** B8: `=(SUM(E5:J5,M5))/C8`<br>**Euros** B9: `=Y5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `=10760+10900`<br>**Egresos** B12: `=-SUM(AB5:AE5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'0604 - 1204'!B13`<br>**Ganancia Bruta** B16: `=B14-'0604 - 1204'!B13`<br>**Debe** B18: `511.925,00`<br>**Haber** B19: `430.733,00`<br>**Promedio** B20: `=SUM(B18:B19)/2`<br>**=(B24*100/B20)/100** B24: `=B15` |
| `2004 - 2604` | **Dolares** B7: `=SUM(A5:D5,K5:L5,O5:X5,AB5:AE5)`<br>**Pesos** B8: `=(SUM(E5:J5,M5))/C8`<br>**Euros** B9: `=Y5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `=10760+10900`<br>**Egresos** B12: `=-SUM(AB5:AE5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'1304 - 1904'!B13`<br>**Ganancia Bruta** B16: `=B14-'1304 - 1904'!B13`<br>**Debe** B18: `479.840,65`<br>**Haber** B19: `474.180,00`<br>**Promedio** B20: `=SUM(B18:B19)/2`<br>**=(B24*100/B20)/100** B24: `=B15` |
| `2704 - 0305` | **Dolares** B7: `=SUM(A5:D5,K5:L5,O5:X5,AB5:AE5)`<br>**Pesos** B8: `=(SUM(E5:J5,M5))/C8`<br>**Euros** B9: `=Y5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `=10760+10900`<br>**Egresos** B12: `=-SUM(AB5:AE5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'2004 - 2604'!B13`<br>**Ganancia Bruta** B16: `=B14-'2004 - 2604'!B13`<br>**Debe** B18: `479.840,65`<br>**Haber** B19: `474.180,00`<br>**Promedio** B20: `499.476,13`<br>**=(B24*100/B20)/100** B24: `=B15`<br>**=(B25*100/B20)/100** B25: `=B16` |
| `0405 - 1005` | **Dolares** B7: `=SUM(A5:D5,K5:L5,O5:X5,AB5:AF5)`<br>**Pesos** B8: `=(SUM(E5:J5,M5))/C8`<br>**Euros** B9: `=Y5*1.2`<br>**Deuda** B10: `5.000,00`<br>**USDT** B11: `=10760+10900`<br>**Egresos** B12: `=-SUM(AB5:AF5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'2704 - 0305'!B13`<br>**Ganancia Bruta** B16: `=B14-'2704 - 0305'!B13`<br>**Debe** B18: `479.840,65`<br>**Haber** B19: `474.180,00`<br>**Promedio** B20: `499.476,13`<br>**=(B24*100/B20)/100** B24: `=B15`<br>**=(B25*100/B20)/100** B25: `=B16` |
| `1105 - 1705` | **Dolares** B7: `=SUM(A5:D5,K5:L5,O5:X5,AC5:AG5)`<br>**Pesos** B8: `=(SUM(E5:J5,M5))/C8`<br>**Euros** B9: `=Y5*1.2`<br>**Deuda** B10: `4.000,00`<br>**USDT** B11: `=10760+10900`<br>**Egresos** B12: `=-SUM(AC5:AG5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'0405 - 1005'!B13`<br>**Ganancia Bruta** B16: `=B14-'0405 - 1005'!B13`<br>**Debe** B18: `479.840,65`<br>**Haber** B19: `474.180,00`<br>**Promedio** B20: `612.170,34`<br>**=(B24*100/B20)/100** B24: `=B15`<br>**=(B25*100/B20)/100** B25: `=B16` |
| `1805 - 2405` | **Dolares** B7: `=SUM(A5:D5,K5:L5,O5:X5,AC5:AG5)`<br>**Pesos** B8: `=(SUM(E5:J5,M5))/C8`<br>**Euros** B9: `=Y5*1.2`<br>**Deuda** B10: `4.000,00`<br>**USDT** B11: `=10760+10900`<br>**Egresos** B12: `=-SUM(AC5:AG5)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Bruto** B14: `=SUM(B7:B11)`<br>**Ganancia Neta** B15: `=B13-'1105 - 1705'!B13`<br>**Ganancia Bruta** B16: `=B14-'1105 - 1705'!B13`<br>**Debe** B18: vacía<br>**Haber** B19: vacía<br>**Promedio** B20: `605.155,10`<br>**=(B24*100/B20)/100** B24: `=B15`<br>**=(B25*100/B20)/100** B25: `=B16` |
| `2505 - 3105` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AC4:AG4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Deuda** B10: `4.000,00`<br>**USDT** B11: `=10760+10900+4021`<br>**Egresos** B12: `=-SUM(AC4:AG4)`<br>**Neto** B13: `=SUM(B7:B12)`<br>**Ganancia Neta** B14: `=B13-'1805 - 2405'!B13`; B19: `=B14`<br>**Bruto** B15: `=SUM(B7:B11)`<br>**Ganancia Bruta** B16: `=B15-'1805 - 2405'!B13`; B20: `=B16`<br>**Volumen Prom** B18: `474.625,30`<br>**Referencias** B22: vacía |
| `0106 - 0706` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AC4:AH4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Deuda** B10: `4.000,00`<br>**USDT** B11: `=10760+10900+4021`<br>**Egresos** B12: `=-SUM(AC4:AG4)`<br>**Ingresos** B13: `=-AH2`<br>**Neto** B14: `=SUM(B7:B13)`<br>**Ganancia Neta** B15: `=B14-'2505 - 3105'!B13`; B20: `=B15`<br>**Bruto** B16: `=SUM(B7:B11,B13)`<br>**Ganancia Bruta** B17: `=B16-'2505 - 3105'!B13`; B21: `=B17`<br>**Volumen Prom** B19: `482.190,71`<br>**Referencias** B23: vacía |
| `0806 - 1406` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AD4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AC4`<br>**Deuda** B11: `4.000,00`<br>**USDT** B12: `=10760+10900+4021`<br>**Egresos** B13: `=-SUM(AD4:AG4,AI4)`<br>**Ingresos** B14: `=-AH4`<br>**Neto** B15: `=SUM(B7:B14)`<br>**Ganancia Neta** B16: `=B15-'0106 - 0706'!B14`; B21: `=B16`<br>**Bruto** B17: `=SUM(B7:B12,B14)`<br>**Ganancia Bruta** B18: `=B17-'0106 - 0706'!B14`; B22: `=B18`<br>**Volumen Prom** B20: `619.283,35`<br>**Referencias** B24: vacía |
| `1506 - 2106` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AD4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AC4`<br>**Deuda** B11: `4.000,00`<br>**USDT** B12: `=10760+10900+4021`<br>**Egresos** B13: `=-SUM(AD4:AG4,AI4)`<br>**Ingresos** B14: `=-AH4`<br>**Neto** B15: `=SUM(B7:B14)`<br>**Ganancia Neta** B16: `=B15-'0806 - 1406'!B15`; B21: `=B16`<br>**Bruto** B17: `=SUM(B7:B12,B14)`<br>**Ganancia Bruta** B18: `=B17-'0806 - 1406'!B15`; B22: `=B18`<br>**Volumen Prom** B20: `317.990,38`<br>**Referencias** B24: vacía |
| `2206 - 2806` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AD4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AC4`<br>**Deuda** B11: `4.000,00`<br>**USDT** B12: `=10760+10900+4021`<br>**Egresos** B13: `=-SUM(AD4:AG4,AI4)`<br>**Ingresos** B14: `=-AH4`<br>**Neto** B15: `=SUM(B7:B14)`<br>**Ganancia Neta** B16: `=B15-'1506 - 2106'!B15`; B21: `=B16`<br>**Bruto** B17: `=SUM(B7:B12,B14)`<br>**Ganancia Bruta** B18: `=B17-'1506 - 2106'!B15`; B22: `=B18`<br>**Volumen Prom** B20: `311.721,47`<br>**Referencias** B24: vacía |
| `2906 - 0507` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AD4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AC4`<br>**Deuda** B11: `4.000,00`<br>**USDT** B12: `=10760+10900+4021`<br>**Egresos** B13: `=-SUM(AD4:AG4,AI4)`<br>**Ingresos** B14: `=-AH4`<br>**Neto** B15: `=SUM(B7:B14)`<br>**Ganancia Neta** B16: `=B15-'2206 - 2806'!B15`; B22: `=B16`<br>**Bruto** B17: `=SUM(B7:B12,B14)`<br>**Ganancia Bruta** B18: `=B17-'2206 - 2806'!B15`; B23: `=B18`<br>**Volumen Prom** B20: `463.877,70`<br>**Operaciones** B21: `348,00`<br>**Referencias** B25: vacía |
| `0607 - 1207` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AD4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AC4`<br>**Deuda** B11: `4.000,00`<br>**USDT** B12: `=10760+10900+4021`<br>**Egresos** B13: `=-SUM(AD4:AG4,AI4)`<br>**Ingresos** B14: `=-AH4`<br>**Neto** B15: `=SUM(B7:B14)`<br>**Ganancia Neta** B16: `=B15-'2906 - 0507'!B15`; B22: `=B16`<br>**Bruto** B17: `=SUM(B7:B12,B14)`<br>**Ganancia Bruta** B18: `=B17-'2906 - 0507'!B15`; B23: `=B18`<br>**Volumen Prom** B20: `282.271,73`<br>**Operaciones** B21: `348,00`<br>**Referencias** B25: vacía |
| `1307 - 1907` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AE4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AE4:AH4,AI4)`<br>**Ingresos** B15: `=-AI4`<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'0607 - 1207'!B15`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'0607 - 1207'!B15`; B24: `=B19`<br>**Volumen Prom** B21: `757.589,27`<br>**Operaciones** B22: `407,00`<br>**Referencias** B26: vacía |
| `2007 - 2607` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AE4:AI4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AE4:AH4,AI4)`<br>**Ingresos** B15: `=-AI4`<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'1307 - 1907'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'1307 - 1907'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `407.583,56`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `2707 - 0208` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AM4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AI4:AM4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'2007 - 2607'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'2007 - 2607'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `542.763,18`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `0308 - 0908` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AM4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AI4:AM4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'2707 - 0208'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'2707 - 0208'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `433.691,81`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `1008 - 2308 (Dos Semanas)` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'0308 - 0908'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'0308 - 0908'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `601.347,60`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `2408 - 3008` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: vacía<br>**Almafuerte** B11: vacía<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'1008 - 2308 (Dos Semanas)'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'1008 - 2308 (Dos Semanas)'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `332.183,67`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `3108 - 0609` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'2408 - 3008'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'2408 - 3008'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `519.500,43`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `0709 - 1309` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'3108 - 0609'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'3108 - 0609'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `628.106,46`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `1409 - 2009` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'0709 - 1309'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'0709 - 1309'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `295.339,22`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `2109 - 2709` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'1409 - 2009'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'1409 - 2009'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `270.828,03`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `2809 - 0410` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'2109 - 2709'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'2109 - 2709'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `299.362,39`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `0510 - 1110` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'2809 - 0410'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'2809 - 0410'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `495.279,46`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |
| `1210 - 1810` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'0510 - 1110'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'0510 - 1110'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `394.062,95`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |

#### Bloque de cálculo — valores calculados (los que guarda el archivo)

| Hoja | Cotización (C8) | Dólares | Pesos (USD) | Euros (USD) | Deuda | USDT | Egresos | Neto | Ganancia Neta | Bruto | Ganancia Bruta | Volumen Prom | Operaciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `2302 - 0103` | — | 35.956,75 | 117.168,41 | — | 5.000,00 | 10.760,00 | -1.180,37 | 167.944,79 | — | 169.125,16 | — | — | — |
| `0203 - 0803` | — | -74.304,34 | 231.921,60 | — | 5.000,00 | 10.760,00 | -5.836,38 | 167.540,87 | — | 173.377,25 | — | — | — |
| `0903 - 1503` | — | -10.555,66 | 171.970,28 | — | 5.000,00 | 10.760,00 | -1.240,15 | 175.934,47 | — | 177.174,62 | — | — | — |
| `1603 - 2203` | — | -35.932,26 | 180.593,82 | 11.400,00 | 5.000,00 | 10.760,00 | -311,86 | 171.509,70 | — | 171.821,56 | — | — | — |
| `2303 - 2903` | — | -19.415,67 | 176.152,59 | 13.320,00 | 5.000,00 | 10.760,00 | -4.890,30 | 180.926,63 | 9.416,93 | 185.816,93 | — | — | — |
| `3003 - 0504` | 1.390,00 | -64.539,18 | 233.868,59 | 360,00 | 5.000,00 | 10.760,00 | -326,12 | 185.123,28 | 4.196,66 | 185.449,41 | — | — | — |
| `0604 - 1204` | 1.380,00 | -109.416,27 | 288.374,09 | 360,00 | 5.000,00 | 10.760,00 | -703,72 | 194.374,09 | 9.250,81 | 195.077,82 | — | — | — |
| `1304 - 1904` | 1.385,00 | 533,20 | 185.298,40 | 2.316,00 | 5.000,00 | 21.660,00 | -5.530,99 | 209.276,60 | 14.902,51 | 214.807,60 | 20.433,51 | — | — |
| `2004 - 2604` | 1.400,00 | -10.683,81 | 215.418,65 | 312,00 | 5.000,00 | 21.660,00 | -3.966,54 | 227.740,30 | 18.463,70 | 231.706,84 | 22.430,24 | — | — |
| `2704 - 0305` | 1.380,00 | -21.602,22 | 236.179,75 | 312,00 | 5.000,00 | 21.660,00 | -8.256,29 | 233.293,24 | 5.552,94 | 241.549,53 | 13.809,23 | — | — |
| `0405 - 1005` | 1.380,00 | -32.729,70 | 256.098,89 | 702,00 | 5.000,00 | 21.660,00 | -12.282,40 | 238.448,79 | 5.155,55 | 250.731,19 | 17.437,95 | — | — |
| `1105 - 1705` | 1.395,00 | -99.415,54 | 307.905,01 | 14.736,00 | 4.000,00 | 21.660,00 | -1.604,51 | 247.280,96 | 8.832,17 | 248.885,47 | 10.436,68 | — | — |
| `1805 - 2405` | 1.405,00 | 29.458,49 | 189.718,37 | 9.936,00 | 4.000,00 | 21.660,00 | -2.443,80 | 252.329,06 | 5.048,10 | 254.772,86 | 7.491,90 | — | — |
| `2505 - 3105` | 1.410,00 | 34.633,53 | 170.189,04 | 25.858,36 | 4.000,00 | 25.681,00 | -2.040,40 | 258.321,53 | 5.992,47 | 260.361,93 | 8.032,87 | 474.625,30 | — |
| `0106 - 0706` | 1.415,00 | 30.446,25 | 189.227,04 | 16.744,61 | 4.000,00 | 25.681,00 | -13.497,97 | 253.500,93 | -4.820,60 | 266.998,90 | 8.677,37 | 482.190,71 | — |
| `0806 - 1406` | 1.440,00 | 122.009,48 | 86.577,08 | 14.981,81 | 4.000,00 | 25.681,00 | -2.644,41 | 261.617,18 | 8.116,25 | 264.261,59 | 10.760,66 | 619.283,35 | — |
| `1506 - 2106` | 1.455,00 | 52.175,76 | 114.424,00 | 4.101,81 | 4.000,00 | 25.681,00 | -1.342,32 | 266.647,58 | 5.030,40 | 267.989,90 | 6.372,72 | 317.990,38 | — |
| `2206 - 2806` | 1.490,00 | 48.379,06 | 120.566,51 | 1.664,31 | 4.000,00 | 25.681,00 | -2.008,85 | 265.889,35 | -758,22 | 267.898,20 | 1.250,63 | 311.721,47 | — |
| `2906 - 0507` | 1.490,00 | 113.625,90 | 66.568,72 | 2.363,06 | 4.000,00 | 25.681,00 | -2.555,40 | 277.290,61 | 11.401,26 | 279.846,01 | 13.956,66 | 463.877,70 | 348,00 |
| `0607 - 1207` | 1.490,00 | 51.496,14 | 127.402,00 | 6.363,06 | 4.000,00 | 25.681,00 | -6.801,65 | 275.747,88 | -1.542,73 | 282.549,53 | 5.258,92 | 282.271,73 | 348,00 |
| `1307 - 1907` | 1.510,00 | 11.034,15 | 119.229,07 | 6.472,02 | 4.000,00 | 25.681,00 | -917,58 | 283.105,99 | 7.358,11 | 284.023,57 | 8.275,69 | 757.589,27 | 407,00 |
| `2007 - 2607` | 1.525,00 | 36.971,71 | 99.424,15 | 3.347,03 | 4.000,00 | 25.681,00 | -4.334,42 | 284.975,04 | 1.869,05 | 289.309,46 | 6.203,47 | 407.583,56 | 338,00 |
| `2707 - 0208` | 1.525,00 | 190.874,77 | 63.044,83 | 3.134,53 | 4.000,00 | 25.681,00 | -293,21 | 286.441,91 | 1.466,87 | 286.735,12 | 1.760,08 | 542.763,18 | 338,00 |
| `0308 - 0908` | 1.525,00 | 169.163,65 | 87.863,50 | 4.770,77 | 4.000,00 | 25.681,00 | -7.604,89 | 283.874,04 | -2.567,87 | 291.478,93 | 5.037,02 | 433.691,81 | 338,00 |
| `1008 - 2308 (Dos Semanas)` | 1.525,00 | 189.385,27 | 85.301,48 | 3.317,94 | 4.000,00 | 25.681,00 | -5.462,60 | 302.223,09 | 18.349,05 | 307.685,69 | 23.811,65 | 601.347,60 | 338,00 |
| `2408 - 3008` | 1.535,00 | 236.367,46 | 78.785,98 | 481,20 | 4.000,00 | 25.681,00 | -152,08 | 345.163,56 | 42.940,48 | 345.315,64 | 43.092,56 | 332.183,67 | 338,00 |
| `3108 - 0609` | 1.530,00 | 235.874,60 | 81.580,47 | 1.992,45 | 4.000,00 | 25.681,00 | -9.032,16 | 340.096,35 | -5.067,21 | 349.128,51 | 3.964,95 | 519.500,43 | 338,00 |
| `0709 - 1309` | 1.525,00 | 223.382,30 | 88.816,52 | 2.367,45 | 4.000,00 | 25.681,00 | -293,35 | 343.953,91 | 3.857,56 | 344.247,26 | 4.150,91 | 628.106,46 | 338,00 |
| `1409 - 2009` | 1.535,00 | 249.525,97 | 63.206,26 | 2.742,45 | 4.000,00 | 25.681,00 | -1.477,97 | 343.677,71 | -276,20 | 345.155,68 | 1.201,77 | 295.339,22 | 338,00 |
| `2109 - 2709` | 1.535,00 | 253.348,73 | 56.308,91 | 6.742,45 | 4.000,00 | 25.681,00 | -474,92 | 345.606,17 | 1.928,46 | 346.081,09 | 2.403,38 | 270.828,03 | 338,00 |
| `2809 - 0410` | 1.540,00 | 255.541,94 | 57.005,72 | 6.329,95 | 4.000,00 | 25.681,00 | -3.671,07 | 344.887,54 | -718,63 | 348.558,61 | 2.952,44 | 299.362,39 | 338,00 |
| `0510 - 1110` | 1.540,00 | 239.721,56 | 73.905,25 | 5.962,27 | 4.000,00 | 25.681,00 | -8.266,24 | 341.003,84 | -3.883,70 | 349.270,08 | 4.382,54 | 495.279,46 | 338,00 |
| `1210 - 1810` | 1.535,00 | 193.328,16 | 117.359,83 | 4.149,77 | 4.000,00 | 25.681,00 | -1.267,08 | 343.251,68 | 2.247,83 | 344.518,76 | 3.514,91 | 394.062,95 | 338,00 |

#### Hoja contra la que compara la Ganancia Neta

| Hoja | Referencia en la fórmula | Hoja anterior en el orden del archivo |
|---|---|---|
| `2302 - 0103` | — | `—` |
| `0203 - 0803` | — | `2302 - 0103` |
| `0903 - 1503` | — | `0203 - 0803` |
| `1603 - 2203` | — | `0903 - 1503` |
| `2303 - 2903` | `1603 - 2203` | `1603 - 2203` |
| `3003 - 0504` | `2303 - 2903` | `2303 - 2903` |
| `0604 - 1204` | `3003 - 0504` | `3003 - 0504` |
| `1304 - 1904` | `0604 - 1204` | `0604 - 1204` |
| `2004 - 2604` | `1304 - 1904` | `1304 - 1904` |
| `2704 - 0305` | `2004 - 2604` | `2004 - 2604` |
| `0405 - 1005` | `2704 - 0305` | `2704 - 0305` |
| `1105 - 1705` | `0405 - 1005` | `0405 - 1005` |
| `1805 - 2405` | `1105 - 1705` | `1105 - 1705` |
| `2505 - 3105` | `1805 - 2405` | `1805 - 2405` |
| `0106 - 0706` | `2505 - 3105` | `2505 - 3105` |
| `0806 - 1406` | `0106 - 0706` | `0106 - 0706` |
| `1506 - 2106` | `0806 - 1406` | `0806 - 1406` |
| `2206 - 2806` | `1506 - 2106` | `1506 - 2106` |
| `2906 - 0507` | `2206 - 2806` | `2206 - 2806` |
| `0607 - 1207` | `2906 - 0507` | `2906 - 0507` |
| `1307 - 1907` | `0607 - 1207` | `0607 - 1207` |
| `2007 - 2607` | `1307 - 1907` | `1307 - 1907` |
| `2707 - 0208` | `2007 - 2607` | `2007 - 2607` |
| `0308 - 0908` | `2707 - 0208` | `2707 - 0208` |
| `1008 - 2308 (Dos Semanas)` | `0308 - 0908` | `0308 - 0908` |
| `2408 - 3008` | `1008 - 2308 (Dos Semanas)` | `1008 - 2308 (Dos Semanas)` |
| `3108 - 0609` | `2408 - 3008` | `2408 - 3008` |
| `0709 - 1309` | `3108 - 0609` | `3108 - 0609` |
| `1409 - 2009` | `0709 - 1309` | `0709 - 1309` |
| `2109 - 2709` | `1409 - 2009` | `1409 - 2009` |
| `2809 - 0410` | `2109 - 2709` | `2109 - 2709` |
| `0510 - 1110` | `2809 - 0410` | `2809 - 0410` |
| `1210 - 1810` | `0510 - 1110` | `0510 - 1110` |

#### Fila de sumas (fila 2 + fila 3) por caja: rango entre hojas

Mínimo, máximo y último valor de la fila de sumas de cada encabezado en las hojas donde aparece, en su moneda. `Hojas ≠ 0` cuenta hojas con valor distinto de cero (|v| > 0,01).

| Encabezado | Mínimo | Máximo | Último | Hojas ≠ 0 |
|---|---|---|---|---|
| CARA CHICA | 0 | 23.920,00 | 5.525,00 | 26 |
| CAMBIO | 1.555,00 | 16.136,00 | 9.290,00 | 33 |
| MALOS | 210,00 | 41.943,00 | 2.545,00 | 33 |
| USD | -209.413,09 | 82.302,63 | -7.229,02 | 33 |
| PESOS | 12.154.876,03 | 152.159.704,90 | 138.132.428,70 | 33 |
| CHEQUES | -15.800.000,00 | 239.927.423,10 | 10.382.849,69 | 33 |
| DEUDA USD | 0 | 0 | 0 | 0 |
| DEUDA PESOS | 0 | 0 | 0 | 0 |
| TRANSFER | -23.126.171,00 | 65.595.111,00 | 31.632.055,00 | 33 |
| USDT | -28.973,41 | 77.399,48 | -18.867,90 | 33 |
| USDT General | 0,00 | 0,00 | 0,00 | 0 |
| Grabrfy Manuel | 4.963,09 | 10.399,27 | 10.399,27 | 33 |
| LLC | 0 | 31.666,84 | 0 | 32 |
| PayPal Ruso | 190,00 | 218,00 | 218,00 | 33 |
| Grabify | 0 | 0 | 0 | 0 |
| GRABIFY Jose | 0 | 0 | 0 | 0 |
| CITY BANK | 0 | 468,00 | 0 | 3 |
| GRABIFI | 287,62 | 4.915,15 | 4.915,15 | 33 |
| WISE | -165,04 | 9.290,73 | 1.464,82 | 33 |
| WISE US | 0 | 0 | 0 | 0 |
| PAYONEER | 0 | 1.821,78 | 0 | 3 |
| EUROS | -500,00 | 17.280,00 | 1.855,00 | 32 |
| REALES | 4,00 | 1.114,00 | 4,00 | 33 |
| LIBRAS | 0 | 0 | 0 | 0 |
| GASTOS | 84,13 | 8.972,30 | 292,32 | 33 |
| FIJOS | 0 | 588,57 | 0 | 1 |
| INVERSION | 0 | 3.000,00 | 0 | 8 |
| 1,00 | 2.030,00 | 7.540,00 | 2.030,00 | 4 |
| bx | -2.179.880,00 | 0 | 0 | 2 |
| INTERESES | 0 | 5.152,00 | 750,00 | 18 |
| TRX | 1.734,00 | 1.734,00 | 1.734,00 | 26 |
| RECAUDACION BX | 0 | 0 | 0 | 0 |
| COMISIONES | -71,86 | 1.461,68 | 224,76 | 23 |
| DIVIDENDOS | 0 | 4.719,00 | 0 | 2 |
| MILLAMAPU | 0 | 0 | 0 | 0 |
| ALQUILERES | -3.600,00 | 0 | 0 | 2 |
| POLIGONO | 7.412,22 | 70.565,57 | 70.565,57 | 18 |
| Grabify BORRAR | 0 | 0 | 0 | 0 |
| ALMAFUERTE | 0 | 50.000,00 | 0 | 4 |
| Dividendos | 0 | 0 | 0 | 0 |
| JEEP | 0 | 0 | 0 | 0 |
| GOL TREND | 0 | 0 | 0 | 0 |
| CHARCAS | 0 | 0 | 0 | 0 |
| PROMAR | 0 | 0 | 0 | 0 |
| POLIGONO 20+13 | 75.466,00 | 75.466,00 | 75.466,00 | 1 |

#### Celdas fuera de las filas 1–5 y del bloque A7:C29

| Hoja | Celdas | Contenido (hasta 14) |
|---|---|---|
| `2302 - 0103` | 4 | E15: `158.704,35`<br>F15: `-167.896,05`<br>G15: `=SUM(E15:F15)` → -9.191,70<br>F16: `=169076.42-N16-P16` → 169.076,42 |
| `0203 - 0803` | 2 | D12: `167.944,79`<br>D13: `=B13-D12` → 5.432,46 |
| `1603 - 2203` | 8 | H12: `Sin contar liquidacion`<br>H13: `Neto`<br>I13: `194.181,70`<br>H14: `Bruto`<br>I14: `194.493,56`<br>H15: `Ganancia`<br>I15: `17.318,94`<br>D16: `=C16-C15` → 311,86 |
| `2303 - 2903` | 9 | H12: `Sin contar liquidacion`<br>H13: `Neto`<br>I13: `194.181,70`<br>H14: `Bruto`<br>I14: `194.493,56`<br>H15: `Ganancia`<br>I15: `17.318,94`<br>D16: `=C16-C15` → 4.890,30<br>E16: `3 dias` |
| `0604 - 1204` | 7 | D8: `=-F3/C8` → 10.414,57<br>D14: `Carbox Gol Trend`<br>E14: `4.172.100,00`<br>F14: `1.380,00`<br>G14: `=E14/F14` → 3.023,26<br>D15: `Ganancia Semanal con Carbox`<br>G15: `=B15+G14` → 12.274,07 |
| `1805 - 2405` | 3 | E12: `9.271.499,05`<br>F12: `Se le pago a [tercero] por colocarle 70 palos en cheques`<br>E13: `=E12/C8` → 6.598,93 |
| `0106 - 0706` | 1 | AG10: `2.310,00` |
| `0806 - 1406` | 6 | E11: `Poligono 00-09 Pago a [tercero]`<br>G11: `10.525.348,57`<br>H11: `1.420,00`<br>I11: `=G11/H11` → 7.412,22<br>I12: `*Nos debe el Poligono`<br>D18: `-3.600,00` |
| `2206 - 2806` | 3 | D8: `30,00`<br>D18: `=C18-B18` → 3.325,97<br>K18: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `2906 - 0507` | 2 | D8: `30,00`<br>K18: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `0607 - 1207` | 1 | K18: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `1307 - 1907` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `2007 - 2607` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `2707 - 0208` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `0308 - 0908` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `1008 - 2308 (Dos Semanas)` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `2408 - 3008` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `3108 - 0609` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `0709 - 1309` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `1409 - 2009` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `2109 - 2709` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `2809 - 0410` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `0510 - 1110` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |
| `1210 - 1810` | 1 | K19: `UNIFICAR TODO EN UNA TABLA PARA IR HACIENDO SEMANA A SEMANA` |

#### Hojas semanales con filas 1–3 idénticas

Ninguna.

### Hoja `CONTROL` (visible)

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 2.300,00 | CARA CHICA, USD |
| B | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 4.870,00 | CAMBIO, USD |
| C | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 645,00 | MALOS, USD |
| D | 1–11 | número 7, texto 2 | 3 | 2 | 0 | -22.430,21 a 44.200,00 | USD |
| E | 1–11 | número 7, texto 2 | 3 | 2 | 0 | -300.000,00 a 146.050.739,00 | ARS, PESOS |
| F | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 19.400.000,00 | ARS, CHEQUES |
| G | 1–11 | número 6, texto 2 | 2 | 3 | 0 | 0 a 0 | USD, USD BsAs |
| H | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | DEUDA USD, USD |
| I | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | DEUDA PESOS, USD |
| J | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 14.193.354,00 | ARS, TRANSFER |
| K | 1–11 | número 7, texto 2 | 3 | 2 | 0 | -26.841,12 a 15.895,30 | USD, USDT |
| L | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 1.734,00 | TRX, USD |
| M | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | ARS, RECAUDACION BX |
| N | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0,00 | USD, USDT General |
| O | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 5.791,44 | Grabrfy Manuel, USD |
| P | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 16.600,17 | LLC, USD |
| Q | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 218,00 | PayPal Ruso, USD |
| R | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | Grabify, USD |
| S | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | GRABIFY Jose, USD |
| T | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | CITY BANK, USD |
| U | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 3.387,62 | GRABIFI, USD |
| V | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 1,45 | EUR, WISE |
| W | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | USD, WISE US |
| X | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 0 | PAYONEER, USD |
| Y | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 1.330,00 | EUR, EUROS |
| Z | 1–11 | número 7, texto 2 | 3 | 2 | 0 | 0 a 164,00 | REAL, REALES |
| AA | 1–11 | número 7, texto 1 | 3 | 3 | 0 | 0 a 0 | LIBRAS |
| AB | 1–11 | número 7, texto 1 | 3 | 3 | 0 | -200.000,00 a 200.000,00 | MILLAMAPU |
| AC | 1–11 | número 7, texto 2 | 3 | 2 | 0 | -261.592,00 a 329.199,33 | POLIGONO, USD |
| AD | 1–11 | número 7, texto 2 | 2 | 2 | 0 | 0 a 294,69 | GASTOS, USD |
| AE | 1–11 | número 7, texto 2 | 2 | 2 | 0 | 0 a 315,99 | COMISIONES, USD |
| AF | 1–11 | número 7, texto 2 | 2 | 2 | 0 | 0 a 0 | INVERSION, USD |
| AG | 1–11 | número 7, texto 2 | 2 | 2 | 0 | 0 a 2.720,56 | INTERESES, USD |
| AH | 1–11 | número 7, texto 2 | 2 | 2 | 0 | 0 a 0 | ALQUILERES, USD |
| AI | 1–11 | número 5, texto 2 | 3 | 4 | 0 | 0 a 0 | DIVIDENDOS, USD |

Textos de la columna A: A1 `CARA CHICA`; A4 `=SUM(A2:A3)`; A5 `USD`; A10 `=A2-A7`; A11 `=A3-A8`.

Primera fila con 4 o más textos (fila 1): `CARA CHICA`, `CAMBIO`, `MALOS`, `USD`, `PESOS`, `CHEQUES`, `USD BsAs`, `DEUDA USD`, `DEUDA PESOS`, `TRANSFER`, `USDT`, `TRX`, `RECAUDACION BX`, `USDT General`, `Grabrfy Manuel`, `LLC`, `PayPal Ruso`, `Grabify`, `GRABIFY Jose`, `CITY BANK`, `GRABIFI`, `WISE`, `WISE US`, `PAYONEER`, `EUROS`, `REALES`, `LIBRAS`, `MILLAMAPU`, `POLIGONO`, `GASTOS`, `COMISIONES`, `INVERSION`, `INTERESES`, `ALQUILERES`, `DIVIDENDOS`.

Fórmulas: 99. Muestra (hasta 25): A4 `=SUM(A2:A3)` → 2.300,00; B4 `=SUM(B2:B3)` → 4.870,00; C4 `=SUM(C2:C3)` → 645,00; D4 `=SUM(D2:D3)` → 21.769,79; E4 `=SUM(E2:E3)` → 146.050.739,00; F4 `=SUM(F2:F3)` → 19.400.000,00; H4 `=SUM(H2:H3)` → 0; I4 `=SUM(I2:I3)` → 0; J4 `=SUM(J2:J3)` → 14.193.354,00; K4 `=SUM(K2:K3)` → -10.945,82; L4 `=SUM(L2:L3)` → 1.734,00; M4 `=SUM(M2:M3)` → 0; N4 `=SUM(N2:N3)` → 0,00; O4 `=SUM(O2:O3)` → 5.791,44; P4 `=SUM(P2:P3)` → 16.600,17; Q4 `=SUM(Q2:Q3)` → 218,00; R4 `=SUM(R2:R3)` → 0; S4 `=SUM(S2:S3)` → 0; T4 `=SUM(T2:T3)` → 0; U4 `=SUM(U2:U3)` → 3.387,62; V4 `=SUM(V2:V3)` → 1,45; W4 `=SUM(W2:W3)` → 0; X4 `=SUM(X2:X3)` → 0; Y4 `=SUM(Y2:Y3)` → 1.330,00; Z4 `=SUM(Z2:Z3)` → 164,00.

### Hoja `Semanales` (visible)

Celdas combinadas: A1:E1.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| A | 1–104 | fecha 102, texto 2 | 0 | 0 | 0 | 2026-01-18 a 2027-12-26 | Cierres, Ganancias Semanales (Es lo generado, no lo "real") |
| B | 2–24 | número 22, texto 1 | 1 | 0 | 0 | 104.238,91 a 258.321,53 | Monto |
| C | 2–24 | número 22, texto 1 | 14 | 0 | 0 | -4.820,60 a 23.558,44 | Ganancia |
| D | 2–24 | número 16, texto 1 | 0 | 6 | 0 | 3.348,44 a 22.430,24 | Bruto |
| E | 2–24 | texto 15 | 0 | 8 | 0 | — | (Promediado, ganancia del 18/01 al 01/02), 50% Menos, Bien, Costos fijos y cierre de mes, Detalle, Es una suma, Estuvo una liquidacion de 23K, neto fue -5k, MUY POCO MOVIMIENTO, Mandamos 100k de [tercero] -MUY POCO MOVIMIENTO, Normal, Pagamos 5k intereses, Pagamos Costos Fijos - MUY POCO MOVIMIENTO, Semana Corta, USD6599 se le pago a [tercero] por colocarle cheques |
| H | 12–12 | número 1 | 0 | 0 | 0 | -188.927,00 a -188.927,00 | — |

Textos de la columna A: A1 `Ganancias Semanales (Es lo generado, no lo "real")`; A2 `Cierres`.

Primera fila con 4 o más textos (fila 2): `Cierres`, `Monto`, `Ganancia`, `Bruto`, `Detalle`.

Fórmulas: 15. Muestra (hasta 25): B4 `=B3+9762.71` → 114.001,62; C4 `=B4-B3` → 9.762,71; C5 `=B5-B4` → 9.762,71; C6 `=B6-B5` → 23.558,44; C11 `=B11-B10` → 8.393,60; C14 `=B14-B13` → 4.196,66; C15 `=B15-B14` → 9.250,81; C16 `=B16-B15` → 14.902,51; C17 `=B17-B16` → 18.463,70; C18 `=B18-B17` → 5.552,94; C20 `=B20-B19` → 8.832,17; C21 `=B21-B20` → 5.048,10; C22 `=B22-B21` → 5.992,47; C23 `=B23-B22` → -4.820,60; C24 `=B24-B23` → 704,03.

### Hoja `Volumen Mayo` (visible)

Celdas combinadas: C2:D2, E2:F2, B9:F11, E8:F8, C8:D8.

| Col. | Filas usadas | Tipos (valor guardado) | Fórmulas | Vacías en el tramo | Errores (#) | Rango numérico / fechas | Valores de texto únicos |
|---|---|---|---|---|---|---|---|
| B | 3–14 | texto 5, fecha 3 | 0 | 4 | 0 | 2026-05-10 a 2026-05-24 | Cheques Colocados por Manuel, Fecha, Suma, Volumen operado durante el mes de mayo. Excluido [tercero] para amb... |
| C | 2–8 | número 5, texto 2 | 2 | 0 | 0 | 110.347,00 a 1.612.563,00 | Debe, Manuel |
| D | 3–14 | número 5, texto 1 | 1 | 6 | 0 | 265.222,00 a 305.569.114,00 | Heber |
| E | 2–8 | número 5, texto 2 | 2 | 0 | 0 | 117.578,00 a 1.170.283,59 | Debe, Francisco |
| F | 3–7 | número 4, texto 1 | 1 | 0 | 0 | 213.899,00 a 663.478,59 | Heber |

Primera fila con 4 o más textos (fila 3): `Fecha`, `Debe`, `Heber`, `Debe`, `Heber`.

Fórmulas: 6. Muestra (hasta 25): C7 `=SUM(C4:C6)` → 600.587,00; D7 `=SUM(D4:D6)` → 1.011.976,00; E7 `=SUM(E4:E6)` → 506.805,00; F7 `=SUM(F4:F6)` → 663.478,59; C8 `=D7+C7` → 1.612.563,00; E8 `=E7+F7` → 1.170.283,59.

## Archivo `2026-10-20b_Calculo_Semanal_1210-1810.xlsx`

### Hojas

`Dimensión` es el rango que declara el archivo (incluye celdas con formato sin datos). `Filas con datos` cuenta filas con al menos una celda no vacía.

| Hoja | Estado | Dimensión | Filas con datos | Celdas no vacías | Fórmulas | Fórmulas con error | Celdas combinadas | Formatos condicionales | Validaciones |
|---|---|---|---|---|---|---|---|---|---|
| `1210 - 1810` | visible | A1:AN31 | 26 | 261 | 60 | 6 | 2 | 2 | 0 |

### Hojas semanales (1: `1210 - 1810` a `1210 - 1810`)

Estructura observada: fila 1 = encabezados de texto (uno por columna), filas 2 y 3 = números cargados como valores, una fila de sumas `=SUM(x2:x3)` por columna y, en las hojas que la tienen, una fila de códigos de moneda (USD, ARS, EUR, REAL). Debajo, desde la fila 7, un bloque de cálculo en las columnas A–C.

| Desde | Hasta | Fila de sumas | Fila de moneda |
|---|---|---|---|
| `1210 - 1810` | `1210 - 1810` | 4 | 5 |

#### Encabezados de la fila 1 (cajas) y en qué hojas aparecen

| Encabezado | Hojas | Primera | Última | Columnas (letra) | Moneda (fila de moneda) |
|---|---|---|---|---|---|
| CARA CHICA | 1 | `1210 - 1810` | `1210 - 1810` | A | USD |
| CAMBIO | 1 | `1210 - 1810` | `1210 - 1810` | B | USD |
| MALOS | 1 | `1210 - 1810` | `1210 - 1810` | C | USD |
| USD | 1 | `1210 - 1810` | `1210 - 1810` | D | USD |
| PESOS | 1 | `1210 - 1810` | `1210 - 1810` | E | ARS |
| CHEQUES | 1 | `1210 - 1810` | `1210 - 1810` | F | ARS |
| USD BsAs | 1 | `1210 - 1810` | `1210 - 1810` | G | USD |
| DEUDA USD | 1 | `1210 - 1810` | `1210 - 1810` | H | USD |
| DEUDA PESOS | 1 | `1210 - 1810` | `1210 - 1810` | I | USD |
| TRANSFER | 1 | `1210 - 1810` | `1210 - 1810` | J | ARS |
| USDT | 1 | `1210 - 1810` | `1210 - 1810` | K | USD |
| TRX | 1 | `1210 - 1810` | `1210 - 1810` | L | USD |
| RECAUDACION BX | 1 | `1210 - 1810` | `1210 - 1810` | M | ARS |
| USDT General | 1 | `1210 - 1810` | `1210 - 1810` | N | USD |
| Grabrfy Manuel | 1 | `1210 - 1810` | `1210 - 1810` | O | USD |
| LLC | 1 | `1210 - 1810` | `1210 - 1810` | P | USD |
| PayPal Ruso | 1 | `1210 - 1810` | `1210 - 1810` | Q | USD |
| Grabify BORRAR | 1 | `1210 - 1810` | `1210 - 1810` | R | USD |
| GRABIFY Jose | 1 | `1210 - 1810` | `1210 - 1810` | S | USD |
| CITY BANK | 1 | `1210 - 1810` | `1210 - 1810` | T | USD |
| GRABIFI | 1 | `1210 - 1810` | `1210 - 1810` | U | USD |
| WISE | 1 | `1210 - 1810` | `1210 - 1810` | V | EUR |
| WISE US | 1 | `1210 - 1810` | `1210 - 1810` | W | USD |
| PAYONEER | 1 | `1210 - 1810` | `1210 - 1810` | X | USD |
| EUROS | 1 | `1210 - 1810` | `1210 - 1810` | Y | EUR |
| REALES | 1 | `1210 - 1810` | `1210 - 1810` | Z | REAL |
| LIBRAS | 1 | `1210 - 1810` | `1210 - 1810` | AA | None |
| MILLAMAPU | 1 | `1210 - 1810` | `1210 - 1810` | AB | None |
| JEEP | 1 | `1210 - 1810` | `1210 - 1810` | AC | USD |
| GOL TREND | 1 | `1210 - 1810` | `1210 - 1810` | AD | USD |
| CHARCAS | 1 | `1210 - 1810` | `1210 - 1810` | AE | USD |
| PROMAR | 1 | `1210 - 1810` | `1210 - 1810` | AF | USD |
| ALMAFUERTE | 1 | `1210 - 1810` | `1210 - 1810` | AG | USD |
| POLIGONO | 1 | `1210 - 1810` | `1210 - 1810` | AI | USD |
| GASTOS | 1 | `1210 - 1810` | `1210 - 1810` | AJ | USD |
| COMISIONES | 1 | `1210 - 1810` | `1210 - 1810` | AK | USD |
| INVERSION | 1 | `1210 - 1810` | `1210 - 1810` | AL | USD |
| INTERESES | 1 | `1210 - 1810` | `1210 - 1810` | AM | USD |
| DIVIDENDOS | 1 | `1210 - 1810` | `1210 - 1810` | AN | USD |

**Columnas con números en filas 2–3 pero sin encabezado en la fila 1:** `1210 - 1810`!AH.

#### Bloque de cálculo (A7:C29) por hoja — fórmulas

Etiquetas de la columna A y fórmula o valor de la columna B en cada hoja (las fórmulas van tal cual).

| Hoja | Etiquetas (col. A) → contenido de la col. B |
|---|---|
| `1210 - 1810` | **Dolares** B7: `=SUM(A4:D4,K4:L4,O4:U4,W4:X4,AG4:AN4)`<br>**Pesos** B8: `=(SUM(E4:J4,M4))/C8`<br>**Euros** B9: `=SUM(Y4+V4)*C9`<br>**Poligono 09** B10: `=AD4`<br>**Almafuerte** B11: `=AC4`<br>**Deuda** B12: `4.000,00`<br>**USDT** B13: `=10760+10900+4021+1608.48+1608.48+994.02+994.02+1237.97+1237.97+198...`<br>**Egresos** B14: `=-SUM(AJ4:AN4)`<br>**Ingresos** B15: vacía<br>**Neto** B16: `=SUM(B7:B15)`<br>**Ganancia Neta** B17: `=B16-'05/10 - 11/10'!B16`; B23: `=B17`<br>**Bruto** B18: `=SUM(B7:B13,B15)`<br>**Ganancia Bruta** B19: `=B18-'05/10 - 11/10'!B16`; B24: `=B19`<br>**Volumen Prom** B21: `394.062,95`<br>**Operaciones** B22: `338,00`<br>**Referencias** B26: vacía |

#### Bloque de cálculo — valores calculados (los que guarda el archivo)

| Hoja | Cotización (C8) | Dólares | Pesos (USD) | Euros (USD) | Deuda | USDT | Egresos | Neto | Ganancia Neta | Bruto | Ganancia Bruta | Volumen Prom | Operaciones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `1210 - 1810` | 1.535,00 | 193.328,16 | 117.359,83 | 4.149,77 | 4.000,00 | 41.536,49 | -1.267,08 | 359.107,17 | #REF! | 360.374,25 | #REF! | 394.062,95 | 338,00 |

#### Hoja contra la que compara la Ganancia Neta

| Hoja | Referencia en la fórmula | Hoja anterior en el orden del archivo |
|---|---|---|
| `1210 - 1810` | `05/10 - 11/10` | `—` |

#### Fila de sumas (fila 2 + fila 3) por caja: rango entre hojas

Mínimo, máximo y último valor de la fila de sumas de cada encabezado en las hojas donde aparece, en su moneda. `Hojas ≠ 0` cuenta hojas con valor distinto de cero (|v| > 0,01).

| Encabezado | Mínimo | Máximo | Último | Hojas ≠ 0 |
|---|---|---|---|---|
| CARA CHICA | 5.525,00 | 5.525,00 | 5.525,00 | 1 |
| CAMBIO | 9.290,00 | 9.290,00 | 9.290,00 | 1 |
| MALOS | 2.545,00 | 2.545,00 | 2.545,00 | 1 |
| USD | -7.229,02 | -7.229,02 | -7.229,02 | 1 |
| PESOS | 138.132.428,70 | 138.132.428,70 | 138.132.428,70 | 1 |
| CHEQUES | 10.382.849,69 | 10.382.849,69 | 10.382.849,69 | 1 |
| DEUDA USD | 0 | 0 | 0 | 0 |
| DEUDA PESOS | 0 | 0 | 0 | 0 |
| TRANSFER | 31.632.055,00 | 31.632.055,00 | 31.632.055,00 | 1 |
| USDT | -18.867,90 | -18.867,90 | -18.867,90 | 1 |
| TRX | 1.734,00 | 1.734,00 | 1.734,00 | 1 |
| RECAUDACION BX | 0 | 0 | 0 | 0 |
| USDT General | 0,00 | 0,00 | 0,00 | 0 |
| Grabrfy Manuel | 10.399,27 | 10.399,27 | 10.399,27 | 1 |
| LLC | 0 | 0 | 0 | 0 |
| PayPal Ruso | 218,00 | 218,00 | 218,00 | 1 |
| Grabify BORRAR | 0 | 0 | 0 | 0 |
| GRABIFY Jose | 0 | 0 | 0 | 0 |
| CITY BANK | 0 | 0 | 0 | 0 |
| GRABIFI | 4.915,15 | 4.915,15 | 4.915,15 | 1 |
| WISE | 1.464,82 | 1.464,82 | 1.464,82 | 1 |
| WISE US | 0 | 0 | 0 | 0 |
| PAYONEER | 0 | 0 | 0 | 0 |
| EUROS | 1.855,00 | 1.855,00 | 1.855,00 | 1 |
| REALES | 4,00 | 4,00 | 4,00 | 1 |
| LIBRAS | 0 | 0 | 0 | 0 |
| MILLAMAPU | 0 | 0 | 0 | 0 |
| JEEP | 0 | 0 | 0 | 0 |
| GOL TREND | 0 | 0 | 0 | 0 |
| CHARCAS | 0 | 0 | 0 | 0 |
| PROMAR | 0 | 0 | 0 | 0 |
| ALMAFUERTE | 0 | 0 | 0 | 0 |
| POLIGONO | 70.565,57 | 70.565,57 | 70.565,57 | 1 |
| GASTOS | 292,32 | 292,32 | 292,32 | 1 |
| COMISIONES | 224,76 | 224,76 | 224,76 | 1 |
| INVERSION | 0 | 0 | 0 | 0 |
| INTERESES | 750,00 | 750,00 | 750,00 | 1 |
| DIVIDENDOS | 0 | 0 | 0 | 0 |

#### Celdas fuera de las filas 1–5 y del bloque A7:C29

| Hoja | Celdas | Contenido (hasta 14) |
|---|---|---|
| `1210 - 1810` | 18 | I13: `USDT General Ganancia`<br>I14: `USDT General`<br>J14: `USDT General`<br>L14: `Es ganancia Repartida, tenemos el 66% del negocio, por eso hago el ...`<br>I15: `1.608,48`<br>J15: `1.608,48`<br>L15: `Cambio general desde Mayo hasta Septiembre`<br>I16: `994,02`<br>J16: `994,02`<br>I17: `1.237,97`<br>J17: `1.237,97`<br>I18: `1.983,67`<br>J18: `1.983,67`<br>I19: `1.042,92`<br>… |

#### Hojas semanales con filas 1–3 idénticas

Ninguna.

## Relaciones entre hojas y archivos

### Referencias por fórmula entre hojas (todas las hojas, todos los archivos)

| Archivo | Hoja | Hoja referenciada | Fórmulas | ¿Existe en el archivo? |
|---|---|---|---|---|
| `2026-10-20_Value_CG_2026.xlsx` | `Dashboard` | `Value CG` | 46 | sí |
| `2026-10-20_Value_CG_2026.xlsx` | `Value CG` | `Value 2025` | 1 | sí |
| `2026-10-20_Value_CG_2026.xlsx` | `Tenencia` | `Value 2026` | 1 | sí |
| `2026-10-20_Value_CG_2026.xlsx` | `Value 2025` | `REF` | 46 | **no** |
| `2026-10-20_Value_CG_2026.xlsx` | `Value 2026` | `Value 2025` | 1 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0903 - 1503` | `0203 - 0803` | 1 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1603 - 2203` | `0903 - 1503` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2303 - 2903` | `1603 - 2203` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `3003 - 0504` | `2303 - 2903` | 1 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0604 - 1204` | `3003 - 0504` | 1 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1304 - 1904` | `0604 - 1204` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2004 - 2604` | `1304 - 1904` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2704 - 0305` | `2004 - 2604` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0405 - 1005` | `2704 - 0305` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1105 - 1705` | `0405 - 1005` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1805 - 2405` | `1105 - 1705` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2505 - 3105` | `1805 - 2405` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0106 - 0706` | `2505 - 3105` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0806 - 1406` | `0106 - 0706` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1506 - 2106` | `0806 - 1406` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2206 - 2806` | `1506 - 2106` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2906 - 0507` | `2206 - 2806` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0607 - 1207` | `2906 - 0507` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1307 - 1907` | `0607 - 1207` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2007 - 2607` | `1307 - 1907` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2707 - 0208` | `2007 - 2607` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0308 - 0908` | `2707 - 0208` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1008 - 2308 (Dos Semanas)` | `0308 - 0908` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2408 - 3008` | `1008 - 2308 (Dos Semanas)` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `3108 - 0609` | `2408 - 3008` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0709 - 1309` | `3108 - 0609` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1409 - 2009` | `0709 - 1309` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2109 - 2709` | `1409 - 2009` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `2809 - 0410` | `2109 - 2709` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `0510 - 1110` | `2809 - 0410` | 2 | sí |
| `2026-10-20a_Calculo_Semanal.xlsx` | `1210 - 1810` | `0510 - 1110` | 2 | sí |
| `2026-10-20b_Calculo_Semanal_1210-1810.xlsx` | `1210 - 1810` | `05/10 - 11/10` | 2 | **no** |

### Coincidencias numéricas entre archivos (sin fórmula que las vincule)

Valores de la columna B de la hoja `Value CG` (filas con fecha en la columna A) comparados con el Neto (B de la fila 'Neto') de cada hoja semanal de la Calculadora. Se informa la hoja semanal cuyo Neto coincide (diferencia < 0,01).

| Fila Value CG | Columna A | Columna B (valor) | Hoja semanal con el mismo Neto |
|---|---|---|---|
| A4 | Aportes | 69.985,48 | ninguna |
| A5 | 2025-07-01 | 91.560,18 | ninguna |
| A6 | Dividendos | 86.104,18 | ninguna |
| A7 | 2026-02-01 | 123.764,33 | ninguna |
| A8 | 2026-02-08 | 147.322,77 | ninguna |
| A9 | 2026-02-15 | 156.684,69 | ninguna |
| A10 | 2026-02-22 | 158.704,35 | ninguna |
| A11 | 2026-03-01 | 167.896,05 | ninguna |
| A12 | Febrero | 167.896,05 | ninguna |
| A13 | Aportes | 71.111,11 | ninguna |
| A14 | 2026-03-01 | 167.896,05 | ninguna |
| A15 | 2026-03-08 | 167.540,87 | `0203 - 0803` |
| A16 | 2026-03-15 | 175.934,47 | `0903 - 1503` |
| A17 | 2026-03-22 | 194.181,70 | ninguna |
| A18 | Balance Actual | 171.509,70 | `1603 - 2203` |
| A19 | 2026-03-29 | 180.926,63 | `2303 - 2903` |
| A20 | Marzo | 180.926,63 | `2303 - 2903` |
| A21 | 2026-04-05 | 185.123,28 | `3003 - 0504` |
| A22 | 2026-04-12 | 194.374,09 | `0604 - 1204` |
| A23 | 2026-04-19 | 209.276,60 | `1304 - 1904` |
| A24 | 2026-04-26 | 227.740,30 | `2004 - 2604` |
| A25 | 2026-05-03 | 233.293,24 | `2704 - 0305` |
| A26 | Abril | 233.293,24 | `2704 - 0305` |
| A27 | Dividendos | 228.574,24 | ninguna |
| A28 | 2026-05-10 | 238.448,79 | `0405 - 1005` |
| A29 | 2026-05-17 | 247.280,96 | `1105 - 1705` |
| A30 | 2026-05-24 | 252.329,06 | `1805 - 2405` |
| A31 | 2026-05-31 | 258.321,53 | `2505 - 3105` |
| A32 | Mayo | 258.321,53 | `2505 - 3105` |
| A33 | Dividendos | 255.811,53 | ninguna |
| A34 | 2026-06-07 | 253.500,93 | `0106 - 0706` |
| A35 | 2026-06-14 | 261.617,18 | `0806 - 1406` |
| A36 | 2026-06-21 | 266.647,58 | `1506 - 2106` |
| A37 | 2026-06-28 | 265.889,35 | `2206 - 2806` |
| A38 | Junio | 265.889,35 | `2206 - 2806` |
| A39 | Dividendos | 264.965,19 | ninguna |

### Vínculos externos

Ningún archivo tiene vínculos externos (`externalLinks`): no hay fórmulas que lean de otro archivo.

