"""Inventario factual de las planillas del Value (Calculadora Semanal + Value CG).

Uso: python3 analisis/inventario.py [carpeta]   (por defecto datos/value)
Escribe analisis/00_inventario.md. Solo registra hechos: estructura, tipos, rangos, fórmulas y
referencias entre hojas. No escribe nombres de clientes: en las hojas con operaciones de clientes
informa cantidades de valores únicos, no los valores.
"""
import datetime as dt
import hashlib
import os
import re
import sys
from collections import Counter, defaultdict

import openpyxl
from openpyxl.utils import get_column_letter

CARPETA = sys.argv[1] if len(sys.argv) > 1 else "datos/value"
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "00_inventario.md")
SEMANAL = re.compile(r"^\d{4} - \d{4}")
HOJAS_CON_CLIENTES = {"Comisiones", "Dante"}   # listas de operaciones con nombres de clientes
MAX_UNICOS = 15
# Nombres de terceros que aparecen en notas sueltas: se reemplazan por "[tercero]". La lista vive fuera de git.
_ARCH_OCULTAR = os.path.join(CARPETA, "nombres_a_ocultar.txt")
OCULTAR = sorted({l.strip() for l in open(_ARCH_OCULTAR, encoding="utf-8") if l.strip()}, key=len, reverse=True) \
    if os.path.exists(_ARCH_OCULTAR) else []

out = []
w = out.append


def fmt(v):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float)):
        if abs(v) < 1e-6:
            return "0"
        return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    if isinstance(v, (dt.datetime, dt.date)):
        return v.strftime("%Y-%m-%d")
    s = str(v).replace("|", "\\|").replace("\n", " ")
    for nombre in OCULTAR:
        s = re.sub(re.escape(nombre), "[tercero]", s, flags=re.IGNORECASE)
    return s if len(s) <= 70 else s[:67] + "..."


def tipo(v):
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, (int, float)):
        return "número"
    if isinstance(v, (dt.datetime, dt.date)):
        return "fecha"
    if isinstance(v, str):
        return "texto"
    return type(v).__name__


def es_formula(v):
    return isinstance(v, str) and v.startswith("=")


def refs_externas(f):
    """Hojas referenciadas en una fórmula ('Hoja'!A1 o Hoja!A1)."""
    hojas = set(re.findall(r"'([^']+)'!", f))
    hojas |= {h for h in re.findall(r"(?<![A-Za-z0-9_'])([A-Za-z_][A-Za-z0-9_]*)!", f)}
    return hojas


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def perfil_columnas(wsf, wsv, ocultar_valores):
    """Perfil por columna (letra) del rango usado: tipos, nulos, rango, únicos."""
    filas = []
    max_r, max_c = wsf.max_row, wsf.max_column
    for c in range(1, max_c + 1):
        vals_f, vals_v = [], []
        for r in range(1, max_r + 1):
            vals_f.append(wsf.cell(r, c).value)
            vals_v.append(wsv.cell(r, c).value)
        ocupadas = [i for i, v in enumerate(vals_f) if v is not None]
        if not ocupadas:
            continue
        primera, ultima = ocupadas[0] + 1, ocupadas[-1] + 1
        tramo_f = vals_f[primera - 1:ultima]
        tramo_v = vals_v[primera - 1:ultima]
        n_form = sum(es_formula(v) for v in tramo_f)
        tipos = Counter(tipo(v) for v in tramo_v if v is not None)
        nums = [v for v in tramo_v if isinstance(v, (int, float)) and not isinstance(v, bool)]
        textos = [v for v in tramo_v if isinstance(v, str)]
        fechas = [v for v in tramo_v if isinstance(v, (dt.datetime, dt.date))]
        nulos = sum(1 for v in tramo_f if v is None)
        errores = sum(1 for v in tramo_v if isinstance(v, str) and v.startswith("#"))
        unicos = sorted(set(textos))
        if ocultar_valores and len(unicos) > 0:
            unicos_txt = f"{len(unicos)} valores (omitidos: pueden ser nombres de clientes)"
        elif len(unicos) == 0:
            unicos_txt = "—"
        elif len(unicos) <= MAX_UNICOS:
            unicos_txt = ", ".join(fmt(u) for u in unicos)
        else:
            unicos_txt = f"{len(unicos)} valores distintos (primeros: " + ", ".join(fmt(u) for u in unicos[:5]) + ", …)"
        rango = "—"
        if nums:
            rango = f"{fmt(min(nums))} a {fmt(max(nums))}"
        if fechas:
            rango = f"{fmt(min(fechas))} a {fmt(max(fechas))}" + (f"; números {rango}" if nums else "")
        filas.append([get_column_letter(c), f"{primera}–{ultima}", ", ".join(f"{k} {n}" for k, n in tipos.most_common()),
                      str(n_form), str(nulos), str(errores), rango, unicos_txt])
    return filas


def fila_suma(ws):
    """Fila con las sumas =SUM(x2:x3) de las cajas (4 en la mayoría; 5 en las primeras hojas)."""
    for r in range(3, 8):
        n = sum(1 for c in range(1, ws.max_column + 1)
                if isinstance(ws.cell(r, c).value, str) and ws.cell(r, c).value.upper().startswith("=SUM("))
        if n >= 5:
            return r
    return None


def fila_moneda(ws):
    for r in range(3, 8):
        n = sum(1 for c in range(1, ws.max_column + 1) if ws.cell(r, c).value in ("USD", "ARS", "EUR", "REAL"))
        if n >= 5:
            return r
    return None


def tabla(headers, filas):
    w("| " + " | ".join(headers) + " |")
    w("|" + "|".join("---" for _ in headers) + "|")
    for f in filas:
        w("| " + " | ".join(str(x) for x in f) + " |")
    w("")


def bloque_resumen_semanal(wsf, wsv):
    """Celdas con contenido en A6:L40 (bloque de cálculo debajo de las cajas)."""
    filas = []
    for r in range(6, min(wsf.max_row, 40) + 1):
        for c in range(1, min(wsf.max_column, 12) + 1):
            f = wsf.cell(r, c).value
            if f is None:
                continue
            v = wsv.cell(r, c).value
            filas.append((wsf.cell(r, c).coordinate, f, v))
    return filas


# ---------------------------------------------------------------- archivos
archivos = sorted(os.path.join(CARPETA, f) for f in os.listdir(CARPETA) if f.endswith(".xlsx"))
libros = {}
for p in archivos:
    libros[p] = (openpyxl.load_workbook(p), openpyxl.load_workbook(p, data_only=True))

w("# 00 — Inventario de datos (Value · Cambio General)")
w("")
w(f"Generado por `analisis/inventario.py` el {dt.date.today():%Y-%m-%d} a partir de `{CARPETA}/`. "
  "Este archivo registra **solo hechos** (estructura, tipos, rangos, fórmulas, referencias); no interpreta. "
  "Montos tal como están en las celdas (sin convertir). Formato numérico: punto de miles, coma decimal.")
w("")
w("En las hojas con listas de operaciones de clientes (" + ", ".join(sorted(HOJAS_CON_CLIENTES)) +
  ") los valores de texto se reemplazan por su cantidad: `CLAUDE.md` prohíbe versionar información de clientes.")
w("")
w("## Archivos")
w("")
tabla(["Archivo", "Tamaño", "SHA-256 (12)", "Hojas", "Visibles", "Ocultas"],
      [[f"`{os.path.basename(p)}`", f"{os.path.getsize(p)/1024:,.0f} KB".replace(",", "."), sha(p),
        len(wb.worksheets), sum(ws.sheet_state == "visible" for ws in wb.worksheets),
        sum(ws.sheet_state != "visible" for ws in wb.worksheets)] for p, (wb, _) in libros.items()])

# Hojas presentes en más de un archivo
presencia = defaultdict(list)
for p, (wb, _) in libros.items():
    for ws in wb.worksheets:
        presencia[ws.title].append(os.path.basename(p))
repetidas = {h: fs for h, fs in presencia.items() if len(fs) > 1}
if repetidas:
    w("**Hojas con el mismo nombre en más de un archivo:** " +
      "; ".join(f"`{h}` en " + ", ".join(f"`{f}`" for f in fs) for h, fs in repetidas.items()) + ".")
    w("")

for p, (wbf, wbv) in libros.items():
    nombre = os.path.basename(p)
    w(f"## Archivo `{nombre}`")
    w("")
    # ---- resumen de hojas
    filas = []
    for ws in wbf.worksheets:
        wv = wbv[ws.title]
        n_cel = n_form = n_err = 0
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                n_cel += 1
                if es_formula(c.value):
                    n_form += 1
                    v = wv[c.coordinate].value
                    if isinstance(v, str) and v.startswith("#"):
                        n_err += 1
        filas_datos = sum(1 for row in ws.iter_rows() if any(c.value is not None for c in row))
        filas.append([f"`{ws.title}`", ws.sheet_state, ws.dimensions, filas_datos, n_cel, n_form, n_err,
                      len(ws.merged_cells.ranges), len(ws.conditional_formatting), len(ws.data_validations.dataValidation)])
    w("### Hojas")
    w("")
    w("`Dimensión` es el rango que declara el archivo (incluye celdas con formato sin datos). "
      "`Filas con datos` cuenta filas con al menos una celda no vacía.")
    w("")
    tabla(["Hoja", "Estado", "Dimensión", "Filas con datos", "Celdas no vacías", "Fórmulas", "Fórmulas con error",
           "Celdas combinadas", "Formatos condicionales", "Validaciones"], filas)

    semanales = [ws for ws in wbf.worksheets if SEMANAL.match(ws.title)]
    otras = [ws for ws in wbf.worksheets if not SEMANAL.match(ws.title)]

    if semanales:
        w(f"### Hojas semanales ({len(semanales)}: `{semanales[0].title}` a `{semanales[-1].title}`)")
        w("")
        w("Estructura observada: fila 1 = encabezados de texto (uno por columna), filas 2 y 3 = números cargados como "
          "valores, una fila de sumas `=SUM(x2:x3)` por columna y, en las hojas que la tienen, una fila de códigos de "
          "moneda (USD, ARS, EUR, REAL). Debajo, desde la fila 7, un bloque de cálculo en las columnas A–C.")
        w("")
        filas_sm = [[f"`{ws.title}`", fila_suma(ws) or "—", fila_moneda(ws) or "—"] for ws in semanales]
        grupos = []
        for t, fs, fm in filas_sm:
            if grupos and grupos[-1][2:] == [fs, fm]:
                grupos[-1][1] = t
            else:
                grupos.append([t, t, fs, fm])
        tabla(["Desde", "Hasta", "Fila de sumas", "Fila de moneda"], grupos)
        # ---- encabezados por hoja
        enc_hoja = {}
        for ws in semanales:
            enc_hoja[ws.title] = [ws.cell(1, c).value for c in range(1, ws.max_column + 1)]
        todos = []
        for ws in semanales:
            for h in enc_hoja[ws.title]:
                if h is not None and h not in todos:
                    todos.append(h)
        w("#### Encabezados de la fila 1 (cajas) y en qué hojas aparecen")
        w("")
        filas = []
        for h in todos:
            hojas = [t for t in enc_hoja if h in enc_hoja[t]]
            letras = sorted({get_column_letter(enc_hoja[t].index(h) + 1) for t in hojas},
                            key=lambda x: (len(x), x))
            monedas = sorted({str(wbf[t].cell(fila_moneda(wbf[t]), enc_hoja[t].index(h) + 1).value)
                              for t in hojas if fila_moneda(wbf[t])})
            filas.append([fmt(h), len(hojas), f"`{hojas[0]}`", f"`{hojas[-1]}`", ", ".join(letras), ", ".join(monedas)])
        tabla(["Encabezado", "Hojas", "Primera", "Última", "Columnas (letra)", "Moneda (fila de moneda)"], filas)
        sin_enc = [(ws.title, get_column_letter(c)) for ws in semanales for c in range(1, ws.max_column + 1)
                   if ws.cell(1, c).value is None and any(ws.cell(r, c).value is not None for r in (2, 3))]
        if sin_enc:
            w("**Columnas con números en filas 2–3 pero sin encabezado en la fila 1:** " +
              ", ".join(f"`{t}`!{l}" for t, l in sin_enc) + ".")
            w("")

        # ---- bloque de cálculo
        w("#### Bloque de cálculo (A7:C29) por hoja — fórmulas")
        w("")
        w("Etiquetas de la columna A y fórmula o valor de la columna B en cada hoja (las fórmulas van tal cual).")
        w("")
        etiquetas = []
        for ws in semanales:
            for r in range(6, 41):
                a = ws.cell(r, 1).value
                if isinstance(a, str) and (a, r) not in etiquetas:
                    pass
        filas = []
        for ws in semanales:
            celdas = {}
            for r in range(6, 41):
                a = ws.cell(r, 1).value
                if isinstance(a, str):
                    b = ws.cell(r, 2).value
                    celdas.setdefault(a.strip(), []).append(f"B{r}: `{fmt(b)}`" if b is not None else f"B{r}: vacía")
            filas.append([f"`{ws.title}`", "<br>".join(f"**{k}** " + "; ".join(v) for k, v in celdas.items())])
        tabla(["Hoja", "Etiquetas (col. A) → contenido de la col. B"], filas)

        w("#### Bloque de cálculo — valores calculados (los que guarda el archivo)")
        w("")
        claves = ["Dolares", "Pesos", "Euros", "Poligono 09", "Almafuerte", "Deuda", "USDT", "euros", "Egresos",
                  "Ingresos", "Neto", "Ganancia Neta", "Bruto", "Ganancia Bruta", "Volumen Prom", "Operaciones"]
        filas = []
        for ws in semanales:
            wv = wbv[ws.title]
            vals = {}
            for r in range(6, 26):
                a = ws.cell(r, 1).value
                if isinstance(a, str) and a.strip() in claves and a.strip() not in vals:
                    vals[a.strip()] = wv.cell(r, 2).value
            cot = None
            for r in range(6, 12):
                if ws.cell(r, 3).value == "Cotizacion":
                    cot = ws.cell(r + 1, 3).value
            if cot is None and isinstance(ws["C8"].value, (int, float)):
                cot = ws["C8"].value
            filas.append([f"`{ws.title}`", fmt(cot)] + [fmt(vals.get(k)) for k in
                         ["Dolares", "Pesos", "Euros", "Deuda", "USDT", "Egresos", "Neto", "Ganancia Neta", "Bruto",
                          "Ganancia Bruta", "Volumen Prom", "Operaciones"]])
        tabla(["Hoja", "Cotización (C8)", "Dólares", "Pesos (USD)", "Euros (USD)", "Deuda", "USDT", "Egresos", "Neto",
               "Ganancia Neta", "Bruto", "Ganancia Bruta", "Volumen Prom", "Operaciones"], filas)

        # ---- referencia de la ganancia
        w("#### Hoja contra la que compara la Ganancia Neta")
        w("")
        filas = []
        orden = [ws.title for ws in semanales]
        for i, ws in enumerate(semanales):
            ref = "—"
            for r in range(6, 26):
                if ws.cell(r, 1).value == "Ganancia Neta" and es_formula(ws.cell(r, 2).value):
                    f = ws.cell(r, 2).value
                    hs = refs_externas(f)
                    ref = ", ".join(f"`{h}`" for h in hs) if hs else f"`{f}` (misma hoja)"
                    break
            anterior = orden[i - 1] if i else "—"
            filas.append([f"`{ws.title}`", ref, f"`{anterior}`"])
        tabla(["Hoja", "Referencia en la fórmula", "Hoja anterior en el orden del archivo"], filas)

        # ---- saldos por caja (fila 4)
        w("#### Fila de sumas (fila 2 + fila 3) por caja: rango entre hojas")
        w("")
        w("Mínimo, máximo y último valor de la fila de sumas de cada encabezado en las hojas donde aparece, en su moneda. "
          "`Hojas ≠ 0` cuenta hojas con valor distinto de cero (|v| > 0,01).")
        w("")
        filas = []
        for h in todos:
            vs = []
            for ws in semanales:
                if h in enc_hoja[ws.title]:
                    c = enc_hoja[ws.title].index(h) + 1
                    fsum = fila_suma(ws)
                    v = wbv[ws.title].cell(fsum, c).value if fsum else None
                    vs.append(v)
            nums = [v for v in vs if isinstance(v, (int, float))]
            if not nums:
                continue
            filas.append([fmt(h), fmt(min(nums)), fmt(max(nums)), fmt(nums[-1]), sum(abs(v) > 0.01 for v in nums)])
        tabla(["Encabezado", "Mínimo", "Máximo", "Último", "Hojas ≠ 0"], filas)

        # ---- celdas fuera del bloque estándar
        w("#### Celdas fuera de las filas 1–5 y del bloque A7:C29")
        w("")
        filas = []
        for ws in semanales:
            wv = wbv[ws.title]
            extra = []
            for row in ws.iter_rows(min_row=6):
                for c in row:
                    if c.value is None:
                        continue
                    if c.column <= 3 and c.row <= 29:
                        continue
                    v = wv[c.coordinate].value
                    extra.append(f"{c.coordinate}: `{fmt(c.value)}`" + (f" → {fmt(v)}" if es_formula(c.value) else ""))
            if extra:
                filas.append([f"`{ws.title}`", len(extra), "<br>".join(extra[:14]) + ("<br>…" if len(extra) > 14 else "")])
        if filas:
            tabla(["Hoja", "Celdas", "Contenido (hasta 14)"], filas)
        else:
            w("Ninguna.")
            w("")

        # ---- hojas semanales idénticas (filas 1-3)
        firmas = defaultdict(list)
        for ws in semanales:
            firma = hashlib.md5(repr([[c.value for c in r] for r in ws.iter_rows(min_row=1, max_row=3)]).encode()).hexdigest()
            firmas[firma].append(ws.title)
        dup = [v for v in firmas.values() if len(v) > 1]
        w("#### Hojas semanales con filas 1–3 idénticas")
        w("")
        w("; ".join(" = ".join(f"`{t}`" for t in g) for g in dup) + "." if dup else "Ninguna.")
        w("")

    # ---- otras hojas: perfil por columna
    for ws in otras:
        wv = wbv[ws.title]
        w(f"### Hoja `{ws.title}` ({ws.sheet_state})")
        w("")
        ocultar = ws.title in HOJAS_CON_CLIENTES
        if ws.merged_cells.ranges:
            w("Celdas combinadas: " + ", ".join(str(r) for r in list(ws.merged_cells.ranges)[:30]) +
              (" …" if len(ws.merged_cells.ranges) > 30 else "") + ".")
            w("")
        perfil = perfil_columnas(ws, wv, ocultar)
        if not perfil:
            w("Sin datos.")
            w("")
            continue
        tabla(["Col.", "Filas usadas", "Tipos (valor guardado)", "Fórmulas", "Vacías en el tramo", "Errores (#)",
               "Rango numérico / fechas", "Valores de texto únicos"], perfil)
        # textos de la columna A y fila de encabezados aparentes (solo si no son de clientes)
        if not ocultar:
            etiquetas = [(c.coordinate, c.value) for c in ws["A"] if isinstance(c.value, str)]
            if etiquetas:
                w("Textos de la columna A: " + "; ".join(f"{k} `{fmt(v)}`" for k, v in etiquetas[:60]) +
                  (" …" if len(etiquetas) > 60 else "") + ".")
                w("")
            fila_textos = None
            for r in range(1, 6):
                txt = [ws.cell(r, c).value for c in range(1, ws.max_column + 1) if isinstance(ws.cell(r, c).value, str)]
                if len(txt) >= 4:
                    fila_textos = (r, txt)
                    break
            if fila_textos:
                w(f"Primera fila con 4 o más textos (fila {fila_textos[0]}): " + ", ".join(f"`{fmt(t)}`" for t in fila_textos[1]) + ".")
                w("")
        # fórmulas: muestra y referencias a otras hojas
        formulas = [(c.coordinate, c.value) for row in ws.iter_rows() for c in row if es_formula(c.value)]
        refs = Counter()
        for _, f in formulas:
            for h in refs_externas(f):
                refs[h] += 1
        if formulas:
            if ocultar:
                w(f"Fórmulas: {len(formulas)} (no se transcriben).")
            else:
                w(f"Fórmulas: {len(formulas)}. Muestra (hasta 25): " +
                  "; ".join(f"{k} `{fmt(f)}` → {fmt(wv[k].value)}" for k, f in formulas[:25]) + ".")
            w("")
        if refs:
            w("Referencias a otras hojas en fórmulas: " + ", ".join(f"`{h}` ({n})" for h, n in refs.most_common()) + ".")
            w("")
        errores = [(c.coordinate, wv[c.coordinate].value) for row in ws.iter_rows() for c in row
                   if isinstance(wv[c.coordinate].value, str) and wv[c.coordinate].value.startswith("#")]
        if errores:
            w(f"Celdas con error: {len(errores)} (por ejemplo " + ", ".join(f"{k} {v}" for k, v in errores[:8]) + ").")
            w("")

# ---------------------------------------------------------------- relaciones entre archivos
w("## Relaciones entre hojas y archivos")
w("")
w("### Referencias por fórmula entre hojas (todas las hojas, todos los archivos)")
w("")
filas = []
for p, (wbf, _) in libros.items():
    for ws in wbf.worksheets:
        refs = Counter()
        for row in ws.iter_rows():
            for c in row:
                if es_formula(c.value):
                    for h in refs_externas(c.value):
                        refs[h] += 1
        for h, n in refs.items():
            existe = h in wbf.sheetnames
            filas.append([f"`{os.path.basename(p)}`", f"`{ws.title}`", f"`{h}`", n, "sí" if existe else "**no**"])
tabla(["Archivo", "Hoja", "Hoja referenciada", "Fórmulas", "¿Existe en el archivo?"], filas)

w("### Coincidencias numéricas entre archivos (sin fórmula que las vincule)")
w("")
w("Valores de la columna B de la hoja `Value CG` (filas con fecha en la columna A) comparados con el Neto (B de la fila "
  "'Neto') de cada hoja semanal de la Calculadora. Se informa la hoja semanal cuyo Neto coincide (diferencia < 0,01).")
w("")
netos = {}
for p, (wbf, wbv) in libros.items():
    for ws in wbf.worksheets:
        if SEMANAL.match(ws.title):
            for r in range(6, 26):
                if ws.cell(r, 1).value == "Neto":
                    v = wbv[ws.title].cell(r, 2).value
                    if isinstance(v, (int, float)):
                        netos[(os.path.basename(p), ws.title)] = v
filas = []
for p, (wbf, wbv) in libros.items():
    if "Value CG" not in wbf.sheetnames:
        continue
    ws, wv = wbf["Value CG"], wbv["Value CG"]
    for r in range(1, ws.max_row + 1):
        a = ws.cell(r, 1).value
        b = wv.cell(r, 2).value
        if not isinstance(b, (int, float)):
            continue
        hits = [f"`{h}`" for (f, h), n in netos.items() if abs(n - b) < 0.01]
        filas.append([f"A{r}", fmt(a), fmt(b), ", ".join(sorted(set(hits))) or "ninguna"])
tabla(["Fila Value CG", "Columna A", "Columna B (valor)", "Hoja semanal con el mismo Neto"], filas)

w("### Vínculos externos")
w("")
ext = []
for p in archivos:
    import zipfile
    with zipfile.ZipFile(p) as z:
        ext += [f"`{os.path.basename(p)}`: {n}" for n in z.namelist() if "externalLink" in n]
w(", ".join(ext) + "." if ext else "Ningún archivo tiene vínculos externos (`externalLinks`): no hay fórmulas que lean de otro archivo.")
w("")

with open(SALIDA, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print(f"OK {SALIDA}: {len(out)} líneas")
