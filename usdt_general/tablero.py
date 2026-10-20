"""Tablero USDT General: métricas, chequeos de control y HTML autocontenido.

Uso:
    python3 -m usdt_general.tablero [datos/archivo.xlsx] [--salidas salidas/usdt_general]

Sin archivo, toma el .xlsx más reciente de datos/ que tenga hojas "Registro USDT General". Escribe datos.json y
tablero_usdt.html. Las definiciones de cada número están en analisis/SPEC.md §4.
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys
from collections import defaultdict

from .leer import Libro

AQUI = os.path.dirname(os.path.abspath(__file__))
TOL_CERRADO_USDT = 50        # |pesos sin recomprar| / precio de compra por debajo de esto = mes cerrado
DIA_CARGADO = 150            # filas de un mismo lado en un día: la fecha probablemente quedó arrastrada
BLOQUE_MIN = 4               # filas consecutivas repetidas para marcar un bloque
TASA_BINANCE_MIN = 0.001     # comisión registrada en Binance por debajo del 0,10%
IMPUESTO = 0.15
DIF_MIN = 2                  # diferencia de BRUTO (USDT) a partir de la cual se marca: RESULTADO trunca o redondea
AVISOS = ["incompleta", "usdt_del_id", "sin_formula_neto", "fecha_corregida", "sin_fecha", "precio_raro",
          "bloque_repetido", "dos_libros", "dia_cargado"]
NOMBRE_MES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
NOMBRE_MES_L = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
                "octubre", "noviembre", "diciembre"]


def _r(x, n=2):
    return None if x is None else round(x, n)


def etiqueta(clave, larga=False):
    a, m = clave.split("-")
    return f"{(NOMBRE_MES_L if larga else NOMBRE_MES)[int(m)]} {a}"


def _suma(fs):
    s = {"usdt": 0.0, "ars": 0.0, "usdt_c": 0.0, "ars_c": 0.0, "com": 0.0, "n": 0, "bin_bruto": 0.0, "bin_com": 0.0}
    for f in fs:
        s["usdt"] += f["usdt"]
        s["ars"] += f["ars"]
        s["com"] += f["comision"]
        s["n"] += 1
        if f["usdt"] and f["ars"]:
            s["usdt_c"] += f["usdt"]
            s["ars_c"] += f["ars"]
        if f["canal"] == "Binance" and f["bruto"]:
            s["bin_bruto"] += f["bruto"]
            s["bin_com"] += f["comision"]
    return s


def metricas_mes(fv, fc):
    """Métricas de un libro en un mes a partir de sus filas de ventas (fv) y compras (fc). SPEC §4."""
    V, C = _suma(fv), _suma(fc)
    pv = V["ars_c"] / V["usdt_c"] if V["usdt_c"] else None
    pc = C["ars_c"] / C["usdt_c"] if C["usdt_c"] else None
    u = V["ars"] - C["ars"]
    g_hoja = C["usdt"] - V["usdt"]
    faltan = u / pc if pc else None
    incompletas = sum(1 for f in fv + fc if "incompleta" in f["avisos"])
    cerrado = faltan is not None and abs(faltan) < TOL_CERRADO_USDT
    g_mes = g_hoja + faltan if (cerrado and faltan is not None) else None
    bin_b = V["bin_bruto"] + C["bin_bruto"]
    fechas = {f["fecha"] for f in fv + fc if f["fecha"]}
    return {
        "vendidos": _r(V["usdt"]), "comprados": _r(C["usdt"]), "cobrados": _r(V["ars"]), "pagados": _r(C["ars"]),
        "vend_c": _r(V["usdt_c"], 4), "cob_c": _r(V["ars_c"], 2), "comp_c": _r(C["usdt_c"], 4), "pag_c": _r(C["ars_c"], 2),
        "precio_venta": _r(pv, 4), "precio_compra": _r(pc, 4),
        "dif_precio": _r(pv - pc, 4) if pv and pc else None, "dif_pct": _r(pv / pc - 1, 6) if pv and pc else None,
        "sin_recomprar": _r(u), "faltan_usdt": _r(faltan), "ganancia_hoja": _r(g_hoja),
        "ganancia": _r(g_mes), "margen": _r(g_mes / V["usdt"], 6) if g_mes is not None and V["usdt"] else None,
        "estado": "cerrado" if cerrado else "abierto", "incompletas": incompletas,
        "comision": _r(V["com"] + C["com"]), "tasa_binance": _r((V["bin_com"] + C["bin_com"]) / bin_b, 6) if bin_b else None,
        "filas_v": V["n"], "filas_c": C["n"], "dias": len(fechas),
        "ultima_fecha": max(fechas).isoformat() if fechas else None,
    }


def _bloques_repetidos(fs):
    """Pares de tramos de >= BLOQUE_MIN filas consecutivas con los mismos (USDT, pesos) en el mismo orden."""
    k = [(round(f["usdt"], 2), round(f["ars"])) for f in fs]
    n, usados, out = len(k), set(), []
    pos = defaultdict(list)
    for i, x in enumerate(k):
        pos[x].append(i)
    for i in range(n):
        for j in pos[k[i]]:
            if j <= i or (i, j) in usados:
                continue
            L = 0
            while j + L < n and i + L < j and k[i + L] == k[j + L]:
                L += 1
            if L >= BLOQUE_MIN and len(set(k[i:i + L])) >= 2:
                out.append((i, j, L))
                for t in range(L):
                    usados.add((i + t, j + t))
    return out


def construir(ruta):
    L = Libro(ruta)
    filas = L.filas
    for i, f in enumerate(filas):
        f["i"] = i
    claves = sorted({h["clave"] for h in L.hojas})
    por_hoja = defaultdict(list)
    for f in filas:
        por_hoja[(f["mes"], f["libro"], f["lado"])].append(f)

    # ---- chequeos que marcan filas
    for (mes, libro, lado), fs in por_hoja.items():
        for i, j, n in _bloques_repetidos(fs):
            for t in range(n):
                for f in (fs[i + t], fs[j + t]):
                    if "bloque_repetido" not in f["avisos"]:
                        f["avisos"].append("bloque_repetido")
            fs[j]["bloque"] = {"orig": [fs[i]["fila"], fs[i + n - 1]["fila"]], "copia": [fs[j]["fila"], fs[j + n - 1]["fila"]]}
        cuenta = defaultdict(int)
        for f in fs:
            if f["fecha"]:
                cuenta[f["fecha"]] += 1
        for f in fs:
            if f["fecha"] and cuenta[f["fecha"]] > DIA_CARGADO:
                f["avisos"].append("dia_cargado")
    idx = defaultdict(list)
    for f in filas:
        if f["usdt"] and f["ars"]:
            idx[(f["mes"], f["lado"], f["fecha"], round(f["usdt"], 2), round(f["ars"]))].append(f)
    for grupo in idx.values():
        if len({f["libro"] for f in grupo}) > 1:
            for f in grupo:
                f["avisos"].append("dos_libros")

    # ---- métricas por mes y libro
    meses = []
    for c in claves:
        m = {"clave": c, "etiqueta": etiqueta(c), "larga": etiqueta(c, True), "libros": {}, "hojas": {}}
        for h in L.hojas:
            if h["clave"] != c:
                continue
            fv, fc = por_hoja[(c, h["libro"], "V")], por_hoja[(c, h["libro"], "C")]
            met = metricas_mes(fv, fc)
            met["v2_hoja"] = _r(h["hoja_dice"]["V2"])
            m["libros"][h["libro"]] = met
            m["hojas"][h["libro"]] = h["nombre"]
        m["parcial"] = c == claves[0]
        meses.append(m)

    # ---- agregados diarios y por canal / banco (por mes, libro, lado)
    diario, canales, bancos = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0]), defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0]), \
        defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0])
    for f in filas:
        for tabla, k in ((diario, f["fecha"].isoformat() if f["fecha"] else "s/f"), (canales, f["canal"]), (bancos, f["banco"])):
            a = tabla[(f["mes"], f["libro"], f["lado"], k)]
            a[0] += f["usdt"]
            a[1] += f["ars"]
            if f["usdt"] and f["ars"]:
                a[2] += f["usdt"]
                a[3] += f["ars"]
            a[4] += 1

    def _tabla(t):
        out = defaultdict(list)
        for (mes, libro, lado, k), a in t.items():
            out[f"{mes}|{libro}|{lado}"].append([k, _r(a[0]), _r(a[1]), _r(a[2], 4), _r(a[3]), a[4]])
        return out

    # ---- reparto
    recalc = {(c, lib): met for m in meses for lib, met in m["libros"].items() for c in [m["clave"]]}
    reparto = []
    ajustes = []
    for b in L.resultado:
        meses_b = []
        for mm in b["meses"]:
            met = recalc.get((mm["clave"], b["libro"]))
            hay = met is not None
            g = met["ganancia"] if hay else None
            fila = dict(mm)
            fila["etiqueta"] = etiqueta(mm["clave"])
            fila["con_hoja"] = hay
            fila["estado"] = met["estado"] if hay else None
            fila["bruto_recalc"] = round(g) if g is not None else None
            fila["neto_formula"] = _r(mm["bruto"] - mm["impuestos"] - mm["gastos"])
            vacio = not any([mm["bruto"], mm["impuestos"], mm["gastos"], mm["neto"], *mm["partes"], *mm["retiros"]])
            if vacio and not hay:
                continue
            meses_b.append(fila)
            d_bruto = (fila["bruto_recalc"] - mm["bruto"]) if fila["bruto_recalc"] is not None else 0
            if abs(d_bruto) < DIF_MIN:
                d_bruto = 0
            d_neto = fila["neto_formula"] - mm["neto"]
            if abs(d_bruto) >= DIF_MIN or abs(d_neto) >= 0.5:
                efecto = d_bruto * (1 - IMPUESTO) + d_neto
                motivo = []
                if abs(d_bruto) >= DIF_MIN:
                    motivo.append(f"la hoja de operaciones da {fila['bruto_recalc']:,} y RESULTADO tiene {mm['bruto']:,.0f}".replace(",", "."))
                if abs(d_neto) >= 0.5:
                    motivo.append(f"el NETO no resta los gastos ({mm['gastos']:,.2f})".replace(",", "X").replace(".", ",").replace("X", "."))
                ajustes.append({"clave": mm["clave"], "etiqueta": etiqueta(mm["clave"], True), "libro": b["libro"],
                                "fila": mm["fila"], "d_bruto": d_bruto, "d_neto": _r(d_neto), "efecto_neto": _r(efecto),
                                "por_socio": _r(efecto / 3) if b["libro"] == "principal" else None,
                                "motivo": "; ".join(motivo)})
        reparto.append({"anio": b["anio"], "libro": b["libro"], "socios": b["socios"], "meses": meses_b})

    saldos = defaultdict(lambda: {"partes": 0.0, "retiros": 0.0})
    for b in reparto:
        for mm in b["meses"]:
            for k, nombre in enumerate(b["socios"]):
                if nombre:
                    s = saldos[(b["libro"], nombre)]
                    s["partes"] += mm["partes"][k]
                    s["retiros"] += mm["retiros"][k]
    saldos_l = [{"libro": lib, "nombre": n, "partes": _r(s["partes"]), "retiros": _r(s["retiros"]),
                 "saldo": _r(s["partes"] - s["retiros"])} for (lib, n), s in saldos.items()]
    ultimo_res = max((mm["clave"] for b in reparto if b["libro"] == "principal" for mm in b["meses"] if mm["bruto"]), default=None)

    # ---- referente
    dev = defaultdict(float)
    for x in L.referente:
        dev[x["mes"]] += x["ganancia"]
    coco = next((b for b in reparto if b["libro"] == "coco"), None)
    referente = []
    for c in sorted(set(dev) | {mm["clave"] for mm in (coco["meses"] if coco else [])}):
        mm = next((x for x in (coco["meses"] if coco else []) if x["clave"] == c), None)
        referente.append({"clave": c, "etiqueta": etiqueta(c), "devengado": _r(dev.get(c, 0) / 2),
                          "planilla": _r(mm["partes"][1]) if mm else None, "pagado": _r(mm["retiros"][1]) if mm else None})

    # ---- chequeos de control
    def ref(fs):
        return [f["i"] for f in fs]

    chequeos = []

    def chk(cid, titulo, que, filas_c=None, detalle=None, grave=True):
        chequeos.append({"id": cid, "titulo": titulo, "que": que, "filas": ref(filas_c or []),
                         "detalle": detalle or [], "estado": "revisar" if (filas_c or detalle) else "ok", "grave": grave})

    abiertos = [f"{m['larga']} ({'principal' if lib == 'principal' else 'Coco'}): faltan recomprar "
                f"$ {met['sin_recomprar']:,.0f} ≈ {met['faltan_usdt']:,.0f} USDT".replace(",", ".")
                for m in meses for lib, met in m["libros"].items() if met["estado"] == "abierto" and met["faltan_usdt"] is not None
                and abs(met["faltan_usdt"]) >= TOL_CERRADO_USDT]
    chk("abierto", "Meses abiertos", "Meses con pesos sin recomprar. Su ganancia todavía no se puede calcular.",
        detalle=abiertos, grave=False)
    sel = lambda a: [f for f in filas if a in f["avisos"]]
    chk("incompleta", "Operaciones con pesos y sin USDT", "Tienen pesos cargados pero no USDT (o al revés). Suman en "
        "pesos y quedan fuera de los precios. Hasta completarlas, el mes no cierra.", sel("incompleta"))
    chk("usdt_del_id", "USDT escrito en la columna del comprobante", "La columna de USDT está vacía y el número está "
        "en la del ID (por ejemplo, =pesos/1662). El tablero lo toma como USDT.", sel("usdt_del_id"))
    dif_hoja = [f"{m['larga']} ({'principal' if lib == 'principal' else 'Coco'}): la hoja dice {met['v2_hoja']:,.2f} y "
                f"recalculando cada fila da {met['ganancia_hoja']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                for m in meses for lib, met in m["libros"].items()
                if met["v2_hoja"] is not None and abs(met["v2_hoja"] - met["ganancia_hoja"]) >= 1]
    chk("sin_formula", "Ganancia de la hoja distinta de la recalculada", "La fila 2 del Excel no coincide con la suma "
        "de las filas: faltan fórmulas de USDT neto o la comisión no se sumó.", sel("sin_formula_neto"), dif_hoja)
    chk("resultado", "RESULTADO distinto de las hojas", "El BRUTO de la hoja RESULTADO se carga a mano. Diferencias "
        "contra la ganancia recalculada y NETO que no resta los gastos.",
        detalle=[f"{a['etiqueta']} ({'principal' if a['libro'] == 'principal' else 'Coco'}, fila {a['fila']}): {a['motivo']}" for a in ajustes])
    chk("fecha_corregida", "Fechas corregidas", "La fecha cargada cae en otro mes (día y mes invertidos o mes "
        "equivocado). El tablero usa el mismo día en el mes de la hoja.", sel("fecha_corregida"))
    chk("sin_fecha", "Operaciones sin fecha", "Están antes de la primera fecha de su columna. Cuentan en el mes, pero no "
        "en ningún día.", sel("sin_fecha"), grave=False)
    chk("dia_cargado", f"Días con más de {DIA_CARGADO} operaciones", "Probablemente la fecha no se actualizó y quedó "
        "arrastrada: el detalle por día de esas fechas no es confiable.", sel("dia_cargado"), grave=False)
    chk("precio_raro", "Precios raros", "Precio a más de 4% del de las operaciones vecinas. Puede ser un error de tipeo "
        "en USDT o en pesos.", sel("precio_raro"))
    chk("bloque_repetido", "Bloques de filas repetidos", f"{BLOQUE_MIN} o más filas seguidas con los mismos USDT y pesos, "
        "en el mismo orden, que aparecen dos veces en la hoja. Puede ser una copia o pagos reales iguales.",
        sel("bloque_repetido"),
        detalle=[f"{f['hoja']}: filas {f['bloque']['orig'][0]}–{f['bloque']['orig'][1]} = {f['bloque']['copia'][0]}–{f['bloque']['copia'][1]}"
                 for f in filas if f.get("bloque")])
    chk("dos_libros", "Operaciones cargadas en los dos libros", "Misma fecha, mismos USDT y mismos pesos en el libro "
        "principal y en Coco. En \"Todo\" se cuentan dos veces.", sel("dos_libros"))
    tasas = [f"{m['larga']} ({'principal' if lib == 'principal' else 'Coco'}): {met['tasa_binance'] * 100:.3f}%".replace(".", ",")
             for m in meses for lib, met in m["libros"].items() if met["tasa_binance"] is not None and met["tasa_binance"] < TASA_BINANCE_MIN]
    chk("comision", "Comisión de Binance baja", "Comisión registrada sobre las operaciones de Binance por debajo de "
        "0,10% (lo habitual es 0,14%). Si faltó cargarla, la ganancia de ese mes está inflada.", detalle=tasas, grave=False)

    # ---- operaciones (en columnas, para que el HTML pese menos)
    hojas = sorted({f["hoja"] for f in filas})
    canal_l = sorted({f["canal"] for f in filas})
    banco_l = sorted({f["banco"] for f in filas})
    ops = {"hoja": [], "lado": [], "fila": [], "fecha": [], "id": [], "usdt": [], "ars": [], "com": [], "canal": [],
           "banco": [], "av": []}
    for f in filas:
        ops["hoja"].append(hojas.index(f["hoja"]))
        ops["lado"].append(f["lado"])
        ops["fila"].append(f["fila"])
        ops["fecha"].append(f["fecha"].isoformat() if f["fecha"] else "")
        ops["id"].append(f["id"])
        ops["usdt"].append(_r(f["usdt"]))
        ops["ars"].append(_r(f["ars"]))
        ops["com"].append(_r(f["comision"], 4))
        ops["canal"].append(canal_l.index(f["canal"]))
        ops["banco"].append(banco_l.index(f["banco"]))
        ops["av"].append(sum(1 << AVISOS.index(a) for a in set(f["avisos"])))
    hoja_info = []
    for h in hojas:
        hh = next(x for x in L.hojas if x["nombre"] == h)
        hoja_info.append({"nombre": h, "mes": hh["clave"], "libro": hh["libro"]})

    return {
        "meta": {"corte": L.corte.isoformat() if L.corte else None, "archivo": os.path.basename(ruta),
                 "generado": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "tol_cerrado": TOL_CERRADO_USDT,
                 "dia_cargado": DIA_CARGADO, "impuesto": IMPUESTO, "ultimo_resultado": ultimo_res,
                 "ultimo_referente": max(x["fecha"] for x in L.referente).isoformat() if L.referente else None},
        "meses": meses, "diario": _tabla(diario), "canales": _tabla(canales), "bancos": _tabla(bancos),
        "reparto": reparto, "saldos": saldos_l, "ajustes": ajustes, "referente": referente, "chequeos": chequeos,
        "hojas": hoja_info, "canal_l": canal_l, "banco_l": banco_l, "avisos": AVISOS, "ops": ops,
    }


def _ruta_por_defecto():
    import openpyxl
    cands = sorted(glob.glob("datos/*.xlsx"), key=os.path.getmtime, reverse=True)
    for c in cands:
        try:
            wb = openpyxl.load_workbook(c, read_only=True)
            if any(n.startswith("Registro USDT General") for n in wb.sheetnames):
                return c
        except Exception:
            continue
    sys.exit("No encontré en datos/ un Excel con hojas 'Registro USDT General'. Pasá la ruta como argumento.")


def main():
    ap = argparse.ArgumentParser(description="Genera el tablero USDT General")
    ap.add_argument("archivo", nargs="?")
    ap.add_argument("--salidas", default="salidas/usdt_general")
    a = ap.parse_args()
    ruta = a.archivo or _ruta_por_defecto()
    datos = construir(ruta)
    os.makedirs(a.salidas, exist_ok=True)
    js = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(a.salidas, "datos.json"), "w", encoding="utf-8") as fh:
        fh.write(js)
    with open(os.path.join(AQUI, "plantilla.html"), encoding="utf-8") as fh:
        html = fh.read()
    html = html.replace("/*__DATOS__*/null", js.replace("</", "<\\/"))
    with open(os.path.join(a.salidas, "tablero_usdt.html"), "w", encoding="utf-8") as fh:
        fh.write(html)
    m = datos["meses"]
    print(f"Libro: {ruta} · corte {datos['meta']['corte']} · {len(m)} meses · {len(datos['ops']['fila'])} operaciones")
    for c in datos["chequeos"]:
        n = len(c["filas"]) or len(c["detalle"])
        print(f"  [{'OK' if c['estado'] == 'ok' else 'REVISAR'}] {c['titulo']}: {n}")
    print(f"Tablero: {os.path.join(a.salidas, 'tablero_usdt.html')}")


if __name__ == "__main__":
    main()
