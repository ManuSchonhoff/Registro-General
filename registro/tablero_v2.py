"""Tablero v2: datos (contrato JSON "v": 2) y generación del HTML.

La especificación está en docs/tablero_v2_spec.md. Este módulo arma el contrato completo (sección 4), calcula las
alertas (3.2) y los chequeos de control desde C05 (7.2), y lee las notas manuales (7.3). El cifrado, el modo plano y
la versión para Artifact se reutilizan de registro/tablero.py (el v1), que no se toca.

Como el v1, el tablero NO incluye ganancia, resultado, rentabilidad ni margen: solo datos operativos.

API: construir_datos_v2(...) -> dict, generar_v2(datos, clave, ruta, artifact) -> ruta | None, serializar(obj),
validaciones(datos) (lo que va a validaciones.json), validar(...) (solo los chequeos), cargar_notas / migrar_notas /
normalizar_notas (7.3), Revisadas (coincidencia de claves), retiro_mes y tipo_comision.
"""
import bisect
import datetime as dt
import json
import math
import os
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from registro import analisis as A
from registro.leer import _low, _num
from registro.tablero import _v, cifrar, clave_aleatoria, version_artifact  # noqa: F401 (clave_aleatoria se reexporta)

VERSION = 2
TITULO = "Tablero semanal"
PLANTILLA_V2 = os.path.join(os.path.dirname(__file__), "tablero_v2_plantilla.html")
MONEDAS = ["USD", "USD Exterior", "USDT", "ARS", "EUR", "BRL", "GBP", "Otra"]
TRAMOS = ["< 500", "500 – 1.000", "1.000 – 5.000", "5.000 – 20.000", "20.000 – 50.000", "> 50.000"]
TRAMOS_BINS = [0, 500, 1000, 5000, 20000, 50000, np.inf]
TIPOS_COM = ["Recaudación / pesos↔transfer", "USD exterior ↔ billete", "USDT ↔ billete",
             "Canje billetes (BsAs, cara chica, malos)", "USD exterior ↔ USDT"]
CAT_FIJOS = "Costos operativos / fijos"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_LARGOS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
                "noviembre", "diciembre"]
MES_NUM = {**{m: i for i, m in enumerate(MESES_LARGOS, 1)}, "setiembre": 9}
SEV_ORDEN = {"critico": 0, "atencion": 1, "info": 2}
NIVEL_ORDEN = {"bloqueante": 0, "aviso": 1, "info": 2, "ok": 3, "no_evaluado": 4}
PROHIBIDO = re.compile(r"ganancia|resultado|rentab|margen|utilidad|p[ée]rdida|perdiendo|ingresos operativos", re.I)

# Valores por defecto del bloque tablero_v2 de config.json (sección 5): si falta una clave, se usa esta.
DEFAULTS = {
    "operadores_destacados": [],
    "semanas_tendencia": {"movil": 12, "escritorio": 26},
    "historia_altas_desde_semana": 9,
    "importantes": {"top": 30, "ventana_semanas": 12, "ausente_semanas": 2, "top_alerta": 10},
    "signo_pendientes_confirmado": False,
    "cajas_ignoradas": [],
    "umbrales": {"volumen_var_pct": 0.25, "top1_max": 0.25, "top5_max": 0.5, "usdt_q_semanas": 4,
                 "pend_semanas_viejo": 12, "cheques_dias_sin_altas": 30, "costos_fijos_dias": 35,
                 "retiro_critico_pct_caja": 0.5, "caja_minima": {"USD": None, "USDT": None}, "pesos_max_pct": None,
                 "precios_min_ops": 5, "precios_min_usd": 10000, "formulas_sin_valor_max": 0.05,
                 "volumen_min_vs_mediana8": 0.3, "similitud_clientes": 0.9},
    "comisiones_lista": {t: None for t in TIPOS_COM},
    "fondeo_excluir_inversores": ["Cambio General"],
    # --sembrar-revisadas da por revisado solo hasta esta semana: es lo que el dueño confirmó el 19/10/2026
    "sembrar_revisadas_hasta": "2026-10-18",
    "pendientes_tipos": [
        {"tipo": "USDT General", "cliente": ["USDT General"]},
        {"tipo": "Préstamos y deudas", "detalle": ["Prestamos", "Deuda"]},
        {"tipo": "Garantías y dividendos", "detalle": ["Garantias", "Dividendos"]},
        {"tipo": "Inversores", "inversores": True},
        {"tipo": "Clientes y cuentas corrientes", "resto": True}],
}

METODO_V2 = [
    "Volumen: operaciones con Fin marcado y Detalle Cajas o Recaudadora, sin USDT General ni Cambio General (duplicarían "
    "la misma operación) y sin cajas que no son divisas. Cada operación cuenta una vez: (Debe + Haber) / 2, pasado a USD.",
    "Semanas: de lunes a domingo, como las hojas de la planilla. La hoja «Dos Semanas» cuenta como dos: sus cifras por "
    "semana se dividen por 2 para comparar.",
    "Comparaciones: contra la semana anterior y contra el promedio de las 4 semanas completas previas. La semana en curso "
    "no se compara hasta que cierre.",
    "Clientes: se agrupan quitando lo que va entre paréntesis y normalizando acentos y mayúsculas.",
    "Nuevos: primera operación del año. Regresaron: volvieron después de 4 semanas de calendario o más sin operar. "
    "Dejaron de operar: clientes con 3 operaciones o más que cumplen 4 semanas de calendario sin operar y no volvieron.",
    "Pesos: cotización mediana de las operaciones USD/Pesos de cada semana. USDT: paridad semanal observada "
    "(cotización del USDT en pesos ÷ cotización del billete).",
    "Caja: saldos al cierre de cada semana, tomados de la misma hoja. Saldo de la planilla (Balance) = caja propia + "
    "plata afuera.",
    "Caja propia: el saldo de cierre de cada caja (fila Balance) menos la plata de terceros que está en esa caja "
    "(los pendientes abiertos de esa caja). Puede dar negativo si en la caja hay más plata de terceros que saldo.",
    "El tablero anterior mostraba el saldo al inicio de la semana; acá la caja es al cierre.",
    "Plata afuera: operaciones abiertas y cuentas corrientes que pasan a la semana siguiente. Positivo = debemos; "
    "negativo = nos deben. La antigüedad se cuenta desde la primera aparición del N° de Ope.",
    "Precio del dólar: promedio ponderado de compra y de venta de billete contra pesos o transferencia.",
    "Para revisar: imputaciones en las columnas de caja que no coinciden con Debe/Haber, y filas canceladas o sin estado "
    "con importes. Graves: USD 100 o más de diferencia; menores: de USD 10 a 100.",
    "La fecha de cada operación sale de los Cierres diarios; si el Cierre no tiene fecha, se infiere y el análisis por día "
    "es aproximado.",
]


# ============================================================================ utilidades
def cfg_v2(cfg):
    """Bloque tablero_v2 de config.json completado con los valores por defecto."""
    c = cfg.get("tablero_v2") or {}
    out = {}
    for k, d in DEFAULTS.items():
        v = c.get(k, d)
        if isinstance(d, dict) and isinstance(v, dict) and k != "comisiones_lista":
            v = {**d, **v}
            if k == "umbrales":
                v["caja_minima"] = {**d["caja_minima"], **(c.get("umbrales", {}).get("caja_minima") or {})}
        out[k] = v
    return out


def _f(x, nd=2):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    r = round(x, nd)
    return 0.0 if r == 0 else r


def _i(x):
    if x is None:
        return None
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return int(round(x))


def _limpio(o):
    """Convierte tipos de numpy/pandas a JSON puro y NaN a null."""
    if isinstance(o, dict):
        return {str(k): _limpio(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_limpio(v) for v in o]
    if isinstance(o, (bool, np.bool_)):
        return int(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (float, np.floating)):
        return None if (math.isnan(o) or math.isinf(o)) else float(o)
    if isinstance(o, (pd.Timestamp, dt.datetime)):
        return o.strftime("%Y-%m-%d")
    if isinstance(o, dt.date):
        return o.isoformat()
    if o is None or isinstance(o, (int, str)):
        return o
    if o is pd.NaT:
        return None
    return str(o)


def _tabla(cols, filas):
    return {"c": list(cols), "f": [list(f) for f in filas]}


def _fecha(x):
    if x is None or (isinstance(x, float) and math.isnan(x)) or x is pd.NaT:
        return None
    if isinstance(x, (pd.Timestamp, dt.datetime)):
        return x.strftime("%Y-%m-%d")
    if isinstance(x, dt.date):
        return x.isoformat()
    return str(x)[:10]


def _norm(s):
    return A._norm(str(s)) if s is not None else ""


def etiqueta_semana(ini, fin):
    """'12–18 oct', '29 sep–5 oct', '10–23 ago (2 sem.)'."""
    k = round(((fin - ini).days + 1) / 7)
    if ini.month == fin.month:
        t = f"{ini.day}–{fin.day} {MESES[fin.month - 1]}"
    else:
        t = f"{ini.day} {MESES[ini.month - 1]}–{fin.day} {MESES[fin.month - 1]}"
    return t + (" (2 sem.)" if k == 2 else "")


def _ddmm(d):
    d = pd.Timestamp(d)
    return f"{d.day:02d}/{d.month:02d}"


def _num_es(x, dec=0):
    s = f"{abs(x):,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("−" if x < 0 else "") + s


def _y(partes):
    """'a', 'a y b', 'a, b y c'."""
    partes = list(partes)
    return partes[0] if len(partes) == 1 else ", ".join(partes[:-1]) + " y " + partes[-1]


def fmt_usd(x, pref="USD "):
    """'USD 850', 'USD 42,5 k', 'USD 850 k', 'USD 1,25 M' (sección 6)."""
    if x is None:
        return "—"
    a = abs(x)
    sg = "−" if x < 0 else ""
    if a < 1000:
        t = _num_es(a, 0)
    elif a < 100_000:
        t = _num_es(a / 1000, 1).rstrip("0").rstrip(",") + " k"
    elif a < 1_000_000:
        t = _num_es(a / 1000, 0) + " k"
    else:
        t = _num_es(a / 1e6, 2).rstrip("0").rstrip(",") + " M"
    return f"{sg}{pref}{t}"


def fmt_ars(x):
    return fmt_usd(x, pref="$ ")


def fmt_pct(x):
    """Fracción → '24%' o '4,7%' por debajo del 10%."""
    p = abs(x) * 100
    t = _num_es(p, 1).rstrip("0").rstrip(",") if p < 10 else _num_es(p, 0)
    return ("−" if x < 0 else "") + t + "%"


# ============================================================================ contexto
class _Ctx:
    """Índices y tablas que comparten las distintas partes del contrato."""

    def __init__(self, R, b, T, M, cz, cz_usdt, fecha, cfg):
        self.R, self.b, self.T, self.M, self.cz, self.cz_usdt = R, b, T, M, cz, cz_usdt
        self.fecha = fecha
        self.corte = dt.date.fromisoformat(fecha)
        self.cfg = cfg
        self.c2 = cfg_v2(cfg)
        self.U = self.c2["umbrales"]
        self.sem = R.semanas
        self.nsem = len(R.semanas)
        self.k = [round(((s.fin - s.inicio).days + 1) / 7) for s in R.semanas]
        self.ini = [s.inicio.isoformat() for s in R.semanas]
        self.lbl = [etiqueta_semana(s.inicio, s.fin) for s in R.semanas]
        ultima = self.nsem - 1
        self.en_curso = None if R.actual_cerrada else ultima
        self.foco = ultima if R.actual_cerrada else ultima - 1
        self.V = b.vol.copy()
        self.V["w"] = self.V.semana_n - 1
        self.mon_caja = {k.upper(): v for k, v in cfg["moneda_por_caja"].items()}
        self.pyg = {c.upper() for c in cfg["columnas_pyg"]}
        self.invcols = {c.upper() for c in cfg["columnas_inversiones_garantias"]}
        self.dic = {}

    def moneda(self, caja):
        return self.mon_caja.get(str(caja).upper(), "Otra")

    def usd(self, mon, x, w):
        if mon == "Otra" or x is None:
            return np.nan
        return self.b.usd(mon, x, w + 1)

    def ventana_cal(self, w, n):
        """Las semanas j < w más cercanas a w, hasta que Σ k_j ≥ n (semanas de calendario)."""
        out, tot, j = [], 0, w - 1
        while j >= 0 and tot < n:
            out.append(j)
            tot += self.k[j]
            j -= 1
        return out


def _idx(lista):
    return {x: i for i, x in enumerate(lista)}


# ============================================================================ semanas, fechas y días
def _cierres_con_validez(s, e):
    """Misma lógica que Registro._fechas_cierres, pero marca si la fecha salió de la columna Q (válida) o se infirió."""
    res, prev = {}, None
    diarios = [r for r in e["cierres"] if r > e["ini_ops"] and (e["ini_pend"] is None or r <= e["ini_pend"])]
    for r in diarios:
        q = s.v.cell(r, 17).value
        if isinstance(q, dt.datetime) and s.inicio <= q.date() <= s.fin and (prev is None or q.date() >= prev):
            d, ok = q.date(), True
        elif prev is None:
            d, ok = s.inicio, False
        else:
            d, ok = min(prev + dt.timedelta(days=1), s.fin), False
        res[r] = (d, ok)
        prev = d
    return res


def _fechas_inferidas(ctx):
    """{(w, fila): 1 si la fecha de la operación no sale de Q} y % de cierres diarios sin fecha por semana."""
    infer, pct = {}, {}
    filas_por_w = ctx.V.groupby("w").fila.apply(list).to_dict()
    for w, s in enumerate(ctx.sem):
        e = s.estructura()
        cv = _cierres_con_validez(s, e)
        pct[w] = (sum(1 for _, ok in cv.values() if not ok) / len(cv)) if cv else None
        rows = sorted(cv)
        for f in filas_por_w.get(w, []):
            j = bisect.bisect_right(rows, f)
            infer[(w, f)] = 0 if (j < len(rows) and cv[rows[j]][1]) else 1
    return infer, pct


def _semanas(ctx, pct_inf):
    R, V = ctx.R, ctx.V
    dias = V.groupby("w").fecha.nunique().to_dict()
    filas = []
    for w, s in enumerate(ctx.sem):
        completa = 0 if w == ctx.en_curso else 1
        filas.append([ctx.ini[w], s.fin.isoformat(), ctx.k[w], completa, int(dias.get(w, 0)), _f(pct_inf.get(w), 4),
                      _f(ctx.cz[s.idx], 2), _f(ctx.cz_usdt[s.idx], 4), int(bool(s.estructura()["formato_actual"])),
                      R.origen.get(s.nombre)])
    return _tabla(["ini", "fin", "k", "completa", "dias_ops", "pct_fecha_inferida", "ars", "usdt", "formato_actual",
                   "archivo"], filas)


# ============================================================================ clientes por semana
def _clientes(ctx):
    """sem (columnas de clientes), inactivos y la serie por cliente."""
    V = ctx.V
    n = ctx.nsem
    por = V.groupby(["cliente_g", "w"]).agg(n=("fila", "size"), usd=("prom_usd", "sum")).reset_index()
    semanas_cli = defaultdict(dict)
    for r in por.itertuples(index=False):
        semanas_cli[r.cliente_g][int(r.w)] = (int(r.n), float(r.usd))
    activos = defaultdict(set)
    for c, d in semanas_cli.items():
        for w in d:
            activos[w].add(c)
    primera = {c: min(d) for c, d in semanas_cli.items()}
    vol_w = V.groupby("w").prom_usd.sum().to_dict()
    vol_cw = {(c, w): u for c, d in semanas_cli.items() for w, (_, u) in d.items()}

    # Semanas de calendario: cs[w] = primera semana de calendario de la hoja w (la doble ocupa dos). Dentro de una hoja
    # de más de una semana, la última semana de calendario en que operó el cliente sale de la fecha de la operación.
    cs = [0]
    for kw in ctx.k[:-1]:
        cs.append(cs[-1] + kw)
    ult_fecha = V.groupby(["cliente_g", "w"]).fecha.max().to_dict()

    def cal_ultima(c, w):
        if ctx.k[w] == 1:
            return cs[w]
        dias = (pd.Timestamp(ult_fecha[(c, w)]) - pd.Timestamp(ctx.sem[w].inicio)).days
        return cs[w] + min(ctx.k[w] - 1, max(0, dias // 7))

    def hoja_de(cal):
        for w in range(n):
            if cs[w] + ctx.k[w] - 1 >= cal:
                return w
        return None

    pasan = defaultdict(list)  # w -> [(cli, ops_hist, usd_hist, ult_w, vuelve_w)]
    lim = ctx.cfg.get("semanas_cliente_perdido", 4)
    for c, d in semanas_cli.items():
        ws = sorted(d)
        ops_acum = usd_acum = 0
        for i, L in enumerate(ws):
            ops_acum += d[L][0]
            usd_acum += d[L][1]
            sig = ws[i + 1] if i + 1 < len(ws) else None
            if ops_acum < 3:
                continue
            # w = la hoja en la que se completan `lim` semanas de calendario sin operar, contando desde la semana de
            # calendario siguiente a la última operación (con hojas de una semana: Σ k de L+1 a w ≥ lim)
            w = hoja_de(cal_ultima(c, L) + lim)
            if w is not None and w > L and (sig is None or w < sig):
                pasan[w].append((c, ops_acum, usd_acum, L, sig))

    filas = []
    for w in range(n):
        act = activos.get(w, set())
        u = vol_w.get(w, 0.0)
        ven = ctx.ventana_cal(w, lim)
        en_ven = set().union(*[activos.get(j, set()) for j in ven]) if ven else set()
        antes = set().union(*[activos.get(j, set()) for j in range(0, min(ven) if ven else 0)]) if ven else set()
        nuevos = {c for c in act if primera[c] == w}
        recup = {c for c in act if c not in en_ven and c in antes}
        rec_usd = sum(vol_cw[(c, w)] for c in act if c in en_ven)
        cuotas = sorted((vol_cw[(c, w)] for c in act), reverse=True)
        tot = sum(cuotas)
        top = lambda m: (sum(cuotas[:m]) / tot) if tot else None  # noqa: E731
        p = pasan.get(w, [])
        prom = V.loc[V.w == w, "prom_usd"]
        filas.append(dict(w=w, usd=u, n=int((V.w == w).sum()), clientes=len(act), nuevos=len(nuevos),
                          usd_nuevos=sum(vol_cw[(c, w)] for c in nuevos), recuperados=len(recup),
                          pasan_inactivos=len(p), usd_hist_inactivos=sum(x[2] for x in p),
                          pct_recurrente=(rec_usd / u) if u else None, top1=top(1), top5=top(5), top10=top(10),
                          ticket_med=float(prom.median()) if len(prom) else None,
                          ticket_p90=float(prom.quantile(0.9)) if len(prom) else None))
    return filas, pasan, semanas_cli


def _sem_tabla(filas):
    cols = ["w", "usd", "n", "clientes", "nuevos", "usd_nuevos", "recuperados", "pasan_inactivos", "usd_hist_inactivos",
            "pct_recurrente", "top1", "top5", "top10", "ticket_med", "ticket_p90"]
    out = []
    for r in filas:
        out.append([r["w"], _f(r["usd"]), r["n"], r["clientes"], r["nuevos"], _f(r["usd_nuevos"]), r["recuperados"],
                    r["pasan_inactivos"], _f(r["usd_hist_inactivos"]), _f(r["pct_recurrente"], 4), _f(r["top1"], 4),
                    _f(r["top5"], 4), _f(r["top10"], 4), _f(r["ticket_med"]), _f(r["ticket_p90"])])
    return _tabla(cols, out)


def _parecidos(ctx, semanas_cli):
    """Clientes nuevos de las últimas 4 semanas parecidos (difflib ≥ similitud_clientes) a uno que ya operaba antes."""
    import difflib
    lim = ctx.U["similitud_clientes"]
    primera = {c: min(d) for c, d in semanas_cli.items()}
    out = []
    for w in range(max(0, ctx.nsem - 4), ctx.nsem):
        viejos = [(c, _norm(c)) for c, p in primera.items() if p < w]
        for c in sorted(c for c, p in primera.items() if p == w):
            a = _norm(c)
            mejor, r_mejor = None, 0.0
            sm = difflib.SequenceMatcher(None, a, "")
            for v, nv in viejos:
                sm.set_seq2(nv)
                if sm.real_quick_ratio() < lim or sm.quick_ratio() < lim:
                    continue
                r = sm.ratio()
                if r > r_mejor:
                    mejor, r_mejor = v, r
            if mejor is not None and r_mejor >= lim:
                out.append((w, c, mejor, r_mejor))
    return out


# ============================================================================ caja y plata afuera
def _tipo_pend(ctx, cliente, detalle, inversores):
    g = _norm(A.grupo_cliente(cliente))
    d = _norm(detalle)
    for regla in ctx.c2["pendientes_tipos"]:
        if "cliente" in regla and g in {_norm(A.grupo_cliente(x)) for x in regla["cliente"]}:
            return regla["tipo"]
        if "detalle" in regla and d in {_norm(x) for x in regla["detalle"]}:
            return regla["tipo"]
        if regla.get("inversores") and g in inversores:
            return regla["tipo"]
        if regla.get("resto"):
            return regla["tipo"]
    return ctx.c2["pendientes_tipos"][-1]["tipo"]


def _items_bloque(ctx, s, w, filas, momento, sem_por_ope, inversores):
    """Ítems de un bloque de pendientes (como R.pendientes_actuales)."""
    out = []
    for r in filas:
        G, F = s.raw(r, 7), s.raw(r, 6)
        if not G or F in ("Cierre", "Balance"):
            continue
        ope = _num(s.v.cell(r, 4).value)
        sn = sem_por_ope.get(int(ope)) if ope else None
        idx = s.idx
        sem_ab = None
        if sn:
            sem_ab = (idx + 1 - sn) if momento == 0 else (idx - sn)
        imp = s.imputaciones(r)
        usd = 0.0
        for k, x in imp.items():
            u = ctx.usd(ctx.moneda(k), x, w)
            if not np.isnan(u):
                usd += u
        cod = s.raw(r, 5)
        out.append(dict(w=w, momento=momento, cli_txt=str(G).strip(), cli=A.grupo_cliente(str(G).strip()),
                        tipo_pend=_tipo_pend(ctx, str(G).strip(), F, inversores), detalle=F,
                        codigo=None if cod is None else str(cod).strip(), ope=_i(ope),
                        w_origen=(sn - 1) if sn else None, sem_abierto=sem_ab,
                        con_q=int(any(str(s.v.cell(r, c).value).strip() == "?" for c in (9, 11))),
                        usd=round(usd, 2), nuevo=int(bool(sn) and sn == idx), fila=r, imp=imp))
    return out


def _bloques(ctx):
    """Para cada semana con formato_actual: saldos por caja (4.3), ítems de plata afuera e inversiones.

    momento 0 = cierre de una semana completa (bloque de abajo); momento 1 = inicio de la semana en curso (bloque de
    arriba). Devuelve dict w -> {momento, saldo{caja: x}, caja{caja: x}, items, bloque{caja: Σ}, rama}."""
    R = ctx.R
    con_ope = ctx.b.ops[ctx.b.ops.ope.notna()].sort_values("semana_n")
    sem_por_ope = dict(zip(con_ope.ope.astype(int)[::-1], con_ope.semana_n[::-1]))  # primera aparición
    inversores = set()
    inv = getattr(ctx, "inv_df", None)
    if inv is not None and not inv.empty:
        excl = {_norm(x) for x in ctx.c2["fondeo_excluir_inversores"]}
        inversores = {_norm(A.grupo_cliente(x)) for x in inv.inversor if _norm(x) not in excl}
    out = {}
    for w, s in enumerate(ctx.sem):
        e = s.estructura()
        if not e["formato_actual"]:
            continue
        cols = defaultdict(list)
        for c, h in s.hdr.items():
            cols[h.upper()].append(c)
        val = lambda r, cs: sum(s.val(r, c) or 0 for c in cs)  # noqa: E731
        if w == ctx.en_curso:
            cp = [r for r in s.filas("Balance") if "cierre" in _low(s.raw(r, 7)) and r < e["primer_cierre"]]
            fin = cp[0] if cp else e["primer_cierre"]
            items = _items_bloque(ctx, s, w, range(7, fin), 1, sem_por_ope, inversores)
            saldo = {k: val(5, cs) for k, cs in cols.items()}
            caja = {k: val(5, cs) + val(6, cs) for k, cs in cols.items()}
            bloque = defaultdict(float)
            for it in items:
                for h, x in it["imp"].items():
                    bloque[h.upper()] += x
            out[w] = dict(momento=1, saldo=saldo, caja=caja, items=items, bloque=dict(bloque), rama="en_curso")
            continue
        ini = e["ini_pend"] + 1
        cp = [r for r in s.filas("Balance") if "cierre" in _low(s.raw(r, 7)) and r > e["ini_pend"]]
        fin = cp[0] if cp else e["fin_pend"]
        items = _items_bloque(ctx, s, w, range(ini, fin), 0, sem_por_ope, inversores)
        bloque = defaultdict(float)
        for it in items:
            for h, x in it["imp"].items():
                bloque[h.upper()] += x
        # cierre_final: el último Cierre de la hoja (el "Cierre Semanal"). La fila Balance "Cierre Pendientes" solo
        # delimita el bloque: sus celdas de caja están vacías.
        cf = e["cierre_final"]
        if cf > e["ini_pend"]:
            saldo = {k: val(cf, cs) for k, cs in cols.items()}
            caja = {k: saldo[k] - bloque.get(k, 0.0) for k in cols}
            rama = "habitual"
        else:
            caja = {k: val(cf, cs) for k, cs in cols.items()}
            saldo = {k: caja[k] + bloque.get(k, 0.0) for k in cols}
            rama = "cierre_antes"
        out[w] = dict(momento=0, saldo=saldo, caja=caja, items=items, bloque=dict(bloque), rama=rama)
    # Balance y Apertura de la semana siguiente, para C08, C09 y confiable
    for w in list(out):
        if w + 1 in out:
            s1 = ctx.sem[w + 1]
            cols1 = defaultdict(list)
            for c, h in s1.hdr.items():
                cols1[h.upper()].append(c)
            out[w]["bal_sig"] = {k: sum(s1.val(5, c) or 0 for c in cs) for k, cs in cols1.items()}
            out[w]["ap_sig"] = {k: sum(s1.val(6, c) or 0 for c in cs) for k, cs in cols1.items()}
    return out


def _es_caja(ctx, caja):
    return caja not in ctx.pyg and caja not in ctx.invcols


def _confiable(ctx, bl, w, caja):
    d = bl.get(w)
    if d is None or d["momento"] != 0 or "bal_sig" not in d:
        return None
    dif = d["saldo"].get(caja, 0.0) - d["bal_sig"].get(caja, 0.0)
    return 0 if abs(dif) > 1 else 1


def _caja_tablas(ctx, bl):
    cajas = sorted({c for d in bl.values() for c in d["saldo"] if _es_caja(ctx, c)},
                   key=lambda c: (MONEDAS.index(ctx.moneda(c)), c))
    ic = _idx(cajas)
    im = _idx(MONEDAS)
    filas, inv = [], []
    for w in sorted(bl):
        d = bl[w]
        for c in cajas:
            sr, cr = d["saldo"].get(c, 0.0), d["caja"].get(c, 0.0)
            conf = _confiable(ctx, bl, w, c)
            if abs(sr) < 0.005 and abs(cr) < 0.005 and conf != 0:
                continue
            mon = ctx.moneda(c)
            filas.append([w, d["momento"], ic[c], im[mon], _f(sr), _f(cr), _f(ctx.usd(mon, sr, w)), _f(ctx.usd(mon, cr, w)),
                          conf])
        for c in sorted(ctx.invcols):
            x = d["saldo"].get(c, 0.0)
            if abs(x) >= 0.005:
                inv.append([w, c, _f(x)])
    caja = _tabla(["w", "momento", "caja", "mon", "saldo_real", "caja_real", "saldo_real_usd", "caja_real_usd",
                   "confiable"], filas)
    return cajas, caja, _tabla(["w", "proyecto", "valor"], inv)


def _pend_tablas(ctx, bl):
    tipos = [r["tipo"] for r in ctx.c2["pendientes_tipos"]]
    it = _idx(tipos)
    q = ctx.U["usdt_q_semanas"]
    filas_sem = []
    for w in sorted(bl):
        d = bl[w]
        por = defaultdict(list)
        for x in d["items"]:
            por[x["tipo_pend"]].append(x)
        for t in tipos:
            xs = por.get(t, [])
            if not xs:
                continue
            ab = [x for x in xs if x["sem_abierto"] is not None]
            tr = {k: [x for x in ab if lo <= x["sem_abierto"] <= hi] for k, (lo, hi) in
                  {"a01": (-10 ** 6, 1), "a24": (2, 4), "a512": (5, 12), "a12": (13, 10 ** 6)}.items()}
            so = [x for x in xs if x["sem_abierto"] is None]
            cq = [x for x in xs if x["con_q"]]
            filas_sem.append([w, d["momento"], it[t], len(xs), _f(-sum(x["usd"] for x in xs if x["usd"] < 0)),
                              _f(sum(x["usd"] for x in xs if x["usd"] > 0)), sum(1 for x in ab if x["sem_abierto"] >= 4),
                              len(so), len(cq), sum(1 for x in cq if x["sem_abierto"] is not None and x["sem_abierto"] >= q),
                              sum(x["nuevo"] for x in xs), len(tr["a01"]), len(tr["a24"]), len(tr["a512"]), len(tr["a12"]),
                              _f(sum(abs(x["usd"]) for x in tr["a01"])), _f(sum(abs(x["usd"]) for x in tr["a24"])),
                              _f(sum(abs(x["usd"]) for x in tr["a512"])), _f(sum(abs(x["usd"]) for x in tr["a12"])),
                              _f(sum(abs(x["usd"]) for x in so))])
    pend_sem = _tabla(["w", "momento", "tipo_pend", "items", "nos_deben", "debemos", "mas4", "sin_ope", "con_q", "con_q_mas4",
                       "nuevos", "a01", "a24", "a512", "a12", "a01_usd", "a24_usd", "a512_usd", "a12_usd", "sin_ope_usd"],
                      filas_sem)
    fotos = []
    for w in (ctx.foco, ctx.en_curso):
        if w is not None and w in bl:
            fotos.extend(bl[w]["items"])
    return tipos, pend_sem, fotos


# ============================================================================ precios, usdt, comisiones
def _precios(ctx):
    b = ctx.b
    lo, hi = ctx.cfg["rango_cotizacion_ars"]
    o = b.ops[b.ops.fin & (b.ops.detalle == "Cajas") & b.ops.cotizacion.between(lo, hi)
              & ~b.ops.cliente.isin(ctx.cfg["excluir_clientes_de_volumen"])]
    rows = []
    for r in o.itertuples():
        if r.caja_debe == "USD" and r.caja_haber in ("PESOS", "TRANSFER"):
            usd, lado, otra = r.debe, 0, r.caja_haber
        elif r.caja_haber == "USD" and r.caja_debe in ("PESOS", "TRANSFER"):
            usd, lado, otra = r.haber, 1, r.caja_debe
        else:
            continue
        if usd is None or (isinstance(usd, float) and math.isnan(usd)) or usd == 0:
            continue
        rows.append((r.semana_n - 1, 0 if otra == "PESOS" else 1, lado, float(usd), float(r.cotizacion)))
    df = pd.DataFrame(rows, columns=["w", "canal", "lado", "usd", "cot"])
    if df.empty:
        return _tabla(["w", "canal", "lado", "usd", "cot", "n"], [])
    df["kx"] = df.cot * df.usd
    g = df.groupby(["w", "canal", "lado"]).agg(usd=("usd", "sum"), kx=("kx", "sum"), n=("usd", "size")).reset_index()
    return _tabla(["w", "canal", "lado", "usd", "cot", "n"],
                  [[int(r.w), int(r.canal), int(r.lado), _f(r.usd), _f(r.kx / r.usd), int(r.n)] for r in g.itertuples()])


def _usdt(ctx):
    b = ctx.b
    lo, hi = ctx.cfg["rango_cotizacion_ars"]
    u = b.ops[b.ops.fin & (b.ops.cliente == "USDT General") & b.ops.cotizacion.between(lo, hi)]
    u = u[[{x, y} == {"TRANSFER", "USDT"} for x, y in zip(u.caja_debe, u.caja_haber)]]
    med = u.groupby("semana_n").cotizacion.median().to_dict()
    cnt = u.groupby("semana_n").size().to_dict()
    p = ctx.T.get("05 Circuito USDT")
    pares = p.groupby("semana_n").agg(n=("fila_usdt", "size"), usd=("usd_cliente", "sum")) if p is not None and not p.empty \
        else pd.DataFrame(columns=["n", "usd"])
    filas = []
    for w, s in enumerate(ctx.sem):
        sn = s.idx
        filas.append([w, _f(med.get(sn)), _f(ctx.cz_usdt[sn], 4), int(cnt.get(sn, 0)),
                      int(pares.n.get(sn, 0)) if sn in pares.index else 0,
                      _f(pares.usd.get(sn, 0.0)) if sn in pares.index else 0.0])
    return _tabla(["w", "cot_med", "paridad", "n", "pares", "usd_pares"], filas)


def tipo_comision(r):
    """Clasificación de A.comisiones, copiada igual (r: fila con mon_debe, mon_haber, caja_debe, caja_haber, detalle)."""
    m = {r.mon_debe, r.mon_haber}
    cajas = {r.caja_debe, r.caja_haber}
    if r.detalle == "Recaudadora" or (m == {"ARS"} and "CHEQUES" not in cajas):
        return "Recaudación / pesos↔transfer"
    if "CHEQUES" in cajas:
        return None  # descuento de cheques: se analiza aparte
    if m == {"USD", "USD Exterior"}:
        return "USD exterior ↔ billete"
    if m == {"USD", "USDT"}:
        return "USDT ↔ billete"
    if m == {"USD"} and cajas != {"USD"}:
        return "Canje billetes (BsAs, cara chica, malos)"
    if m == {"USD Exterior", "USDT"}:
        return "USD exterior ↔ USDT"
    return None


def _comis(ctx, tipos):
    b = ctx.b
    o = b.ops[b.ops.fin & b.ops.detalle.isin(["Cajas", "Recaudadora"]) & (b.ops.cliente != "USDT General")]
    o = o[o.cotizacion.between(0.01, ctx.cfg["max_comision_pct"])]
    it = _idx(tipos)
    filas = []
    for r in o.itertuples():
        t = tipo_comision(r)
        if t is None or pd.isna(r.debe_usd) or pd.isna(r.haber_usd):
            continue
        filas.append([int(r.semana_n) - 1, it[t], _f(r.cotizacion), _f(r.debe_usd)])
    return _tabla(["w", "tipo_com", "pct", "usd"], filas)


# ============================================================================ cheques, fondeo, gastos
def _cheques(ctx, ch):
    vacio = dict(ultima_alta=None, cartera_n=None, cartera_ars=None, vencidos_n=None, vencidos_ars=None, cot=None,
                 tasa_mensual_mediana=None, venc=_tabla(["mes", "vencido", "n", "ars"], []),
                 titulares=_tabla(["titular", "n", "ars", "pct", "cartera_ars"], []))
    if ch is None or ch.empty:
        return vacio
    ch = ch.copy()
    ch["venc_ts"] = pd.to_datetime(ch.vencimiento)
    cart = ch[~ch.cobrado & ~ch.colocado].copy()
    cart["vencido"] = cart.venc_ts < pd.Timestamp(ctx.fecha)
    cart["mes"] = cart.venc_ts.dt.to_period("M").astype(str)
    venc = cart.groupby(["mes", "vencido"]).agg(n=("monto", "size"), ars=("monto", "sum")).reset_index()
    tot_cart = float(cart.monto.sum())
    tit = ch.groupby("titular").agg(n=("monto", "size"), ars=("monto", "sum")).join(
        cart.groupby("titular").monto.sum().rename("cartera_ars")).fillna({"cartera_ars": 0.0}).reset_index()
    tit = tit[tit.cartera_ars > 0].sort_values("cartera_ars", ascending=False).head(10)
    tasa = ch.loc[ch.tasa_mensual.notna() & (ch.tasa_mensual > 0), "tasa_mensual"]
    act = ctx.R.actual.idx
    return dict(
        ultima_alta=_fecha(pd.to_datetime(ch.fecha, errors="coerce").max()),
        cartera_n=int(len(cart)), cartera_ars=_i(tot_cart),
        vencidos_n=int(cart.vencido.sum()), vencidos_ars=_i(cart.loc[cart.vencido, "monto"].sum()),
        cot=_f(ctx.cz[act], 2), tasa_mensual_mediana=_f(tasa.median(), 4) if len(tasa) else None,
        venc=_tabla(["mes", "vencido", "n", "ars"], [[r.mes, int(r.vencido), int(r.n), _i(r.ars)] for r in venc.itertuples()]),
        titulares=_tabla(["titular", "n", "ars", "pct", "cartera_ars"],
                         [[r.titular, int(r.n), _i(r.ars), _f(r.cartera_ars / tot_cart, 4) if tot_cart else None,
                           _i(r.cartera_ars)] for r in tit.itertuples()]))


def retiro_mes(x, corte):
    """Mes de retiro (AAAA-MM) desde la columna Retiro de la hoja Inversores.

    Fecha → ese mes. Nombre de mes → su primera aparición en un mes ≥ el mes del corte (el mes del corte cuenta).
    Otro texto → None."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    if isinstance(x, (dt.datetime, dt.date, pd.Timestamp)):
        return f"{x.year:04d}-{x.month:02d}"
    t = _norm(x)
    m = re.search(r"\b(20\d\d)-(\d{1,2})(?:-\d{1,2})?\b", t)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}"
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b", t)
    if m:
        a = int(m.group(3))
        return f"{a + 2000 if a < 100 else a:04d}-{int(m.group(2)):02d}"
    hallados = [(mm.start(), MES_NUM[mm.group(1)]) for mm in re.finditer(r"\b(" + "|".join(MES_NUM) + r")\b", t)]
    if not hallados:
        return None
    mes = min(hallados)[1]
    a = re.search(r"\b(20\d\d)\b", t)
    if a:
        anio = int(a.group(1))
    else:
        anio = corte.year if mes >= corte.month else corte.year + 1
    return f"{anio:04d}-{mes:02d}"


def _retiro_txt(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    if isinstance(x, (dt.datetime, dt.date, pd.Timestamp)):
        return _fecha(x)
    return str(x).strip()


def _txt(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    return _fecha(x) if isinstance(x, (dt.datetime, dt.date, pd.Timestamp)) else str(x).strip()


def _fondeo(ctx, inv):
    cols = ["inversor", "plazo", "destino", "detalle", "monto_usd", "tasa_mensual", "interes_mensual_usd", "retiro_txt",
            "retiro_mes", "propio"]
    if inv is None or inv.empty:
        return dict(capital_terceros_usd=None, interes_mensual_usd=None, tasa_promedio=None, inversores=_tabla(cols, []))
    excl = {_norm(x) for x in ctx.c2["fondeo_excluir_inversores"]}
    filas = []
    cap = inte = 0.0
    for r in inv.itertuples():
        monto, interes, tasa_hoja = _num(r.monto_usd), _num(r.interes_mensual_usd), _num(r.tasa_mensual_pct)
        if monto and interes and monto > 0 and interes > 0:
            tasa = interes / monto
        else:
            tasa = tasa_hoja / 100 if tasa_hoja is not None else None
        propio = int(_norm(r.inversor) in excl)
        if not propio:
            cap += monto or 0
            inte += interes or 0
        filas.append([str(r.inversor).strip(), _txt(r.plazo), _txt(r.destino), _txt(r.detalle), _f(monto), _f(tasa, 6),
                      _f(interes), _retiro_txt(r.retiro), retiro_mes(r.retiro, ctx.corte), propio])
    return dict(capital_terceros_usd=_f(cap), interes_mensual_usd=_f(inte), tasa_promedio=_f(inte / cap, 6) if cap else None,
                inversores=_tabla(cols, filas))


def _cat_gasto(c):
    n = A._norm(c)
    for nombre, pat in A.CATS:
        if re.search(pat, n):
            return nombre
    return "Otros"


def _gastos(ctx, cats):
    b = ctx.b
    g = b.ops[b.ops.fin & (b.ops.detalle == "Gastos")].copy()
    g["gasto_usd"] = np.where(g.caja_debe == "GASTOS", g.debe, g.haber_usd)
    g = g[g.gasto_usd.notna()]
    g["cat"] = g.cliente.map(_cat_gasto)
    ic = _idx(cats)
    t = g.groupby(["mes", "semana_n", "cat"]).agg(n=("fila", "size"), usd=("gasto_usd", "sum")).reset_index()
    fijos = g.loc[g.cat == CAT_FIJOS, "fecha"]
    ult_fijo = _fecha(fijos.max()) if len(fijos) else None
    return _tabla(["mes", "w", "cat", "n", "usd"],
                  [[r.mes, int(r.semana_n) - 1, ic[r.cat], int(r.n), _f(r.usd)] for r in t.itertuples()]), ult_fijo


# ============================================================================ calidad y revisar
def _ope_txt(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else str(int(x))


def clave_fila(ini, fila, ope):
    o = _ope_txt(ope)
    return f"{ini}#{int(fila)}#{o}" if o else f"{ini}#{int(fila)}"


class Revisadas:
    """Índice de `revisadas` (7.3). Una fila está revisada si hay una clave con el mismo ini y el mismo Ope; si alguna
    de las dos no tiene Ope, se compara por ini y fila. Las demás claves se comparan tal cual."""

    def __init__(self, revisadas):
        self.exacta, self.por_ope, self.por_fila, self.por_fila_sin_ope = {}, {}, {}, {}
        for e in revisadas or []:
            e = {"clave": e} if isinstance(e, str) else e
            k = str(e.get("clave", "")).strip()
            if not k:
                continue
            self.exacta[k] = e
            p = k.split("#")
            if len(p) in (2, 3) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p[0]) and p[1].isdigit():
                self.por_fila[(p[0], p[1])] = e
                if len(p) == 3 and p[2]:
                    self.por_ope[(p[0], p[2])] = e
                else:
                    self.por_fila_sin_ope[(p[0], p[1])] = e

    def fila(self, ini, fila, ope):
        o = _ope_txt(ope)
        f = str(int(fila))
        if o:
            return self.por_ope.get((ini, o)) or self.por_fila_sin_ope.get((ini, f))
        return self.por_fila.get((ini, f))

    def clave(self, k):
        if k is None:
            return None
        e = self.exacta.get(k)
        if e is None:
            p = k.split("#")
            if len(p) in (2, 3) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p[0]) and p[1].isdigit():
                return self.fila(p[0], int(p[1]), float(p[2]) if len(p) == 3 and p[2] else None)
        return e


def _revisar(ctx, rev, iop):
    t = ctx.T.get("11 Filas a revisar")
    cols = ["w", "fila", "ope", "op", "cli_txt", "tipo", "dif_usd", "sev", "clave", "revisada", "revisada_fecha"]
    if t is None or t.empty:
        return _tabla(cols, []), []
    base = ctx.b.ops[["semana_n", "fila", "operador", "ope"]].drop_duplicates(["semana_n", "fila"])
    t = t[t.severidad.isin(["Alta", "Media"])].merge(base, on=["semana_n", "fila"], how="left", suffixes=("_g", ""))
    t = t.sort_values(["semana_n", "fila"])
    filas, regs = [], []
    for r in t.itertuples():
        w = int(r.semana_n) - 1
        ini = ctx.ini[w]
        k = clave_fila(ini, r.fila, r.ope)
        e = rev.fila(ini, r.fila, r.ope)
        op = r.operador if isinstance(r.operador, str) else "Otros"
        filas.append([w, int(r.fila), _i(r.ope), iop[op], str(r.cliente), r.tipo, _f(r.dif_usd), r.severidad, k,
                      int(e is not None), (e or {}).get("fecha")])
        regs.append(dict(w=w, sev=r.severidad, clave=k, revisada=e is not None, fila=int(r.fila)))
    return _tabla(cols, filas), regs


def _calidad(ctx, iop):
    t = ctx.T.get("11 Filas a revisar")
    b = ctx.b
    tot = b.ops[b.ops.fin & (b.ops.semana_n <= b.ultima_completa)].groupby(["semana_n", "operador"]).size()
    cnt = defaultdict(lambda: [0, 0, 0])
    if t is not None and not t.empty:
        base = b.ops[["semana_n", "fila", "operador"]].drop_duplicates(["semana_n", "fila"])
        t = t.merge(base, on=["semana_n", "fila"], how="left", suffixes=("_g", ""))
        for r in t.itertuples():
            op = r.operador if isinstance(r.operador, str) else "Otros"
            cnt[(int(r.semana_n), op)][{"Alta": 0, "Media": 1, "Baja": 2}[r.severidad]] += 1
    claves = sorted(set(cnt) | set(tot.index), key=lambda x: (x[0], iop.get(x[1], 999)))
    return _tabla(["w", "op", "alta", "media", "baja", "ops"],
                  [[sn - 1, iop[op], *cnt[(sn, op)], int(tot.get((sn, op), 0))] for sn, op in claves])


# ============================================================================ notas (7.3)
SEMANA_HOJA = re.compile(r"\b(\d{2})(\d{2})\s*-\s*(\d{2})(\d{2})\b")
FECHA_DDMM = re.compile(r"\b(\d{1,2})/(\d{1,2})(?:/\d{2,4})?\b")


def semana_de_texto(texto, semanas):
    """ini de la semana si el texto nombra una sola semana sin ambigüedad (dd/mm u hoja "DDMM - DDMM"); si no, None.
    semanas: lista de (ini: date, fin: date)."""
    hallado = set()
    sin_hoja = SEMANA_HOJA.sub(" ", texto)
    for m in SEMANA_HOJA.finditer(texto):
        for ini, fin in semanas:
            if ini.day == int(m.group(1)) and ini.month == int(m.group(2)):
                hallado.add(ini)
    for m in FECHA_DDMM.finditer(sin_hoja):
        d, mm = int(m.group(1)), int(m.group(2))
        if not (1 <= mm <= 12 and 1 <= d <= 31):
            continue
        for ini, fin in semanas:
            try:
                f = dt.date(ini.year, mm, d)
            except ValueError:
                continue
            if ini <= f <= fin:
                hallado.add(ini)
    return min(hallado).isoformat() if len(hallado) == 1 else None


def _sin_espacios(t):
    return re.sub(r"\s+", "", str(t))


def migrar_notas(v1, fecha_origen, semanas, existentes=None):
    """notas_tablero.json del v1 (listas de strings) → formato de notas_manuales.json (7.3), sin duplicar textos."""
    out = normalizar_notas(existentes or {})
    vistos_h = {_sin_espacios(h["texto"]) for h in out["hallazgos"]}
    vistos_p = {_sin_espacios(p["texto"]) for p in out["preguntas"]}
    nh = max([int(h["id"][1:]) for h in out["hallazgos"] if re.fullmatch(r"h\d+", str(h.get("id")))] or [0])
    npg = max([int(p["id"][1:]) for p in out["preguntas"] if re.fullmatch(r"p\d+", str(p.get("id")))] or [0])
    migradas = 0
    for t in (v1 or {}).get("hallazgos", []) or []:
        t = t.get("texto", "") if isinstance(t, dict) else str(t)
        if not t.strip() or _sin_espacios(t) in vistos_h:
            continue
        nh += 1
        out["hallazgos"].append(dict(id=f"h{nh}", semana=semana_de_texto(t, semanas), texto=t, estado="abierta",
                                     fecha=fecha_origen, fecha_estado=None))
        vistos_h.add(_sin_espacios(t))
        migradas += 1
    for t in (v1 or {}).get("preguntas", []) or []:
        t = t.get("texto", "") if isinstance(t, dict) else str(t)
        if not t.strip() or _sin_espacios(t) in vistos_p:
            continue
        npg += 1
        out["preguntas"].append(dict(id=f"p{npg}", texto=t, estado="abierta"))
        vistos_p.add(_sin_espacios(t))
        migradas += 1
    return out, migradas


def normalizar_notas(d):
    """Completa campos y convierte revisadas sueltas (strings) a {"clave": s}. Los campos que no son del contrato (por
    ejemplo, la fecha o la semana de una pregunta cargada a mano) se conservan al final: nunca se pierden en silencio."""
    d = d or {}

    def extra(x, base):
        return {k: v for k, v in x.items() if k not in base}

    hall = []
    for i, h in enumerate(d.get("hallazgos", []) or [], 1):
        h = {"texto": h} if isinstance(h, str) else dict(h)
        base = dict(id=h.get("id") or f"h{i}", semana=h.get("semana"), texto=h.get("texto", ""),
                    estado=h.get("estado") or "abierta", fecha=h.get("fecha"), fecha_estado=h.get("fecha_estado"))
        hall.append({**base, **extra(h, base)})
    preg = []
    for i, p in enumerate(d.get("preguntas", []) or [], 1):
        p = {"texto": p} if isinstance(p, str) else dict(p)
        base = dict(id=p.get("id") or f"p{i}", texto=p.get("texto", ""), estado=p.get("estado") or "abierta")
        preg.append({**base, **extra(p, base)})
    rev = []
    for e in d.get("revisadas", []) or []:
        e = {"clave": e} if isinstance(e, str) else dict(e)
        base = dict(clave=e.get("clave"), fecha=e.get("fecha"), nota=e.get("nota"))
        rev.append({**base, **extra(e, base)})
    return dict(hallazgos=hall, preguntas=preg, revisadas=rev)


def cargar_notas(salida, semanas):
    """Para correr.py --tablero-v2: lee salidas/notas_manuales.json (la carpeta madre de `salida`) si existe; si no,
    migra el notas_tablero.json de `salida` (o el más reciente de las carpetas hermanas). No escribe nada.
    Devuelve (notas, origen) con origen = {"tipo": "manuales" | "migradas" | "ninguna", "archivo", "n"}."""
    madre = os.path.dirname(os.path.abspath(salida))
    man = os.path.join(madre, "notas_manuales.json")
    if os.path.exists(man):
        return normalizar_notas(json.load(open(man, encoding="utf-8"))), dict(tipo="manuales", archivo=man, n=0)
    cands = [os.path.join(salida, "notas_tablero.json")]
    if not os.path.exists(cands[0]):
        otras = sorted((p for p in (os.path.join(madre, d, "notas_tablero.json") for d in os.listdir(madre))
                        if os.path.exists(p)), key=lambda p: os.path.basename(os.path.dirname(p)))
        cands = otras[-1:]
    for p in cands:
        if os.path.exists(p):
            v1 = json.load(open(p, encoding="utf-8"))
            carpeta = os.path.basename(os.path.dirname(os.path.abspath(p)))
            fo = carpeta if re.fullmatch(r"\d{4}-\d{2}-\d{2}", carpeta) else None
            notas, n = migrar_notas(v1, fo, semanas)
            return notas, dict(tipo="migradas", archivo=p, n=n)
    return normalizar_notas({}), dict(tipo="ninguna", archivo=None, n=0)


# ============================================================================ validaciones (7.2)
def _check(id_, nivel, titulo, detalle, claves=(), n=None):
    claves = list(claves)
    return dict(id=id_, nivel=nivel, titulo=titulo, detalle=detalle, n=len(claves) if n is None else n, claves=claves,
                revisada=0)


TITULOS = {
    "C01": "Hojas no reconocidas", "C02": "Semana cerrada reemplazada por una en curso",
    "C03": "Fórmulas sin valor calculado en las últimas hojas", "C04": "Hojas sin ningún Cierre",
    "C05": "Hojas de cheques e inversores en la base", "C06": "Cantidad de semanas contra la última publicación",
    "C07": "Volumen de la semana contra las 8 anteriores",
    "C08": "Saldo al cierre contra el Balance de la semana siguiente",
    "C09": "Plata afuera al cierre contra la Apertura de la semana siguiente",
    "C10": "Cierres diarios vacíos en la última semana cerrada",
    "C11": "Operaciones sin Fin, Pen ni Can en la última semana cerrada",
    "C12": "Cajas sin moneda asignada", "C13": "Operadores fuera de la lista principal",
    "C14": "Clientes nuevos parecidos a uno existente", "C15": "Semanas sin cotización observada",
    "C16": "Año de la planilla", "C17": "Filas de la semana para revisar", "C18": "Notas migradas o arrastradas",
}


def _validaciones(ctx, bl, sem_filas, regs, notas_info, previo, plan, parecidos=()):
    R, b, cfg = ctx.R, ctx.b, ctx.cfg
    f = ctx.foco
    out = []
    for cid in ("C01", "C02", "C03", "C04"):
        out.append(_check(cid, "no_evaluado", TITULOS[cid], "Chequeo todavía no disponible.", n=0))
    # C05
    base = os.path.basename(getattr(ctx, "base_archivo", "") or "")
    faltan = [h for h in ("CQ", "Inversores") if h not in R.wv.sheetnames]
    if faltan:
        out.append(_check("C05", "bloqueante", TITULOS["C05"], f"La base {base} no tiene la hoja {' ni la hoja '.join(faltan)}.",
                          [f"control:C05:{base}"]))
    else:
        out.append(_check("C05", "ok", TITULOS["C05"], f"La base {base} tiene las hojas CQ e Inversores.", n=0))
    # C06
    prev_n = None
    if isinstance(previo, dict):
        prev_n = (previo.get("v2") or {}).get("semanas") or (previo.get("v1") or {}).get("semanas")
    if prev_n is None:
        out.append(_check("C06", "no_evaluado", TITULOS["C06"], "No hay una publicación anterior para comparar.", n=0))
    elif ctx.nsem < int(prev_n):
        out.append(_check("C06", "bloqueante", TITULOS["C06"],
                          f"Hay {ctx.nsem} {'semana' if ctx.nsem == 1 else 'semanas'} y la última publicación tenía {prev_n}: "
                          "falta alguna hoja.",
                          [f"control:C06:{ctx.nsem}"]))
    else:
        out.append(_check("C06", "ok", TITULOS["C06"], f"{ctx.nsem} {'semana' if ctx.nsem == 1 else 'semanas'} "
                          f"(la última publicación tenía {prev_n}).", n=0))
    # C07
    u = [r["usd"] / ctx.k[r["w"]] for r in sem_filas]
    prev8 = [u[j] for j in range(max(0, f - 8), f) if j != ctx.en_curso]
    if len(prev8) >= 2:
        med = float(np.median(prev8))
        lim = ctx.U["volumen_min_vs_mediana8"] * med
        if u[f] < lim:
            out.append(_check("C07", "bloqueante", TITULOS["C07"],
                              f"La semana {ctx.lbl[f]} movió {fmt_usd(u[f])} por semana, menos del "
                              f"{fmt_pct(ctx.U['volumen_min_vs_mediana8'])} de la mediana de las 8 anteriores "
                              f"({fmt_usd(med)}). Puede faltar cargar operaciones.", [f"control:C07:{ctx.ini[f]}"]))
        else:
            out.append(_check("C07", "ok", TITULOS["C07"],
                              f"{ctx.lbl[f]}: {fmt_usd(u[f])} contra una mediana de {fmt_usd(med)}.", n=0))
    else:
        out.append(_check("C07", "no_evaluado", TITULOS["C07"], "No hay semanas anteriores para comparar.", n=0))
    # C08 y C09: últimas 3 transiciones con formato_actual
    trans = [w for w in sorted(bl) if "bal_sig" in bl[w]][-3:]
    c08, c09, det08, det09 = [], [], [], []
    for w in trans:
        d = bl[w]
        cajas = sorted({c for c in set(d["saldo"]) | set(d["bal_sig"]) if _es_caja(ctx, c)})
        for c in cajas:
            dif = d["saldo"].get(c, 0.0) - d["bal_sig"].get(c, 0.0)
            if abs(dif) > 1:
                k = f"control:C08:{c}:{int(round(dif))}"
                if k not in c08:
                    c08.append(k)
                    det08.append(f"{c} en {ctx.lbl[w]}: {_num_es(dif)}")
            dif9 = -d["bloque"].get(c, 0.0) - d["ap_sig"].get(c, 0.0)
            if abs(dif9) > 1:
                k = f"control:C09:{c}:{int(round(dif9))}"
                if k not in c09:
                    c09.append(k)
                    det09.append(f"{c} en {ctx.lbl[w]}: {_num_es(dif9)}")
    rango = (f"{ctx.lbl[trans[0]]} a {ctx.lbl[trans[-1] + 1]}" if trans else "")
    out.append(_check("C08", "aviso", TITULOS["C08"], "Diferencias (en la unidad de cada caja): " + "; ".join(det08) + ".", c08)
               if c08 else _check("C08", "ok" if trans else "no_evaluado", TITULOS["C08"],
                                  f"Coinciden en las últimas transiciones ({rango})." if trans else "No hay dos semanas con saldos.",
                                  n=0))
    out.append(_check("C09", "aviso", TITULOS["C09"], "Diferencias (en la unidad de cada caja): " + "; ".join(det09) + ".", c09)
               if c09 else _check("C09", "ok" if trans else "no_evaluado", TITULOS["C09"],
                                  f"Coinciden en las últimas transiciones ({rango})." if trans else "No hay dos semanas con saldos.",
                                  n=0))
    # C10 y C11: la última semana cerrada. A mitad de semana es normal que la hoja en curso tenga Cierres vacíos y
    # operaciones sin estado: se controla cuando cierre (como Para revisar), así no salen avisos falsos ni una clave
    # que, dada por revisada en curso, ocultaría el aviso real al cerrar.
    w_ult = ctx.foco
    s = ctx.sem[w_ult]
    e = s.estructura()
    curso = (f" La semana en curso ({ctx.lbl[ctx.en_curso]}) se controla al cerrar."
             if ctx.en_curso is not None else "")
    vacios = [r for r in e["cierres"] if r > e["ini_ops"] and all(s.raw(r, c) in (None, "") for c in s.hdr)]
    if vacios:
        out.append(_check("C10", "aviso", TITULOS["C10"],
                          f"{len(vacios)} {'Cierre diario vacío' if len(vacios) == 1 else 'Cierres diarios vacíos'} en "
                          f"{ctx.lbl[w_ult]} ({'fila' if len(vacios) == 1 else 'filas'} {', '.join(map(str, vacios))}).",
                          [f"control:C10:{ctx.ini[w_ult]}"],
                          n=len(vacios)))
    else:
        out.append(_check("C10", "ok", TITULOS["C10"], f"Todos los Cierres de {ctx.lbl[w_ult]} tienen datos.{curso}", n=0))
    sin = b.ops[(b.ops.semana_n == s.idx) & ~(b.ops.fin | b.ops.pen | b.ops.can)]
    if len(sin):
        out.append(_check("C11", "aviso", TITULOS["C11"],
                          f"{len(sin)} operaciones de {ctx.lbl[w_ult]} no tienen marcado Fin, Pen ni Can.",
                          [f"control:C11:{ctx.ini[w_ult]}:{len(sin)}"], n=len(sin)))
    else:
        out.append(_check("C11", "ok", TITULOS["C11"], f"Todas las operaciones de {ctx.lbl[w_ult]} tienen estado.{curso}",
                          n=0))
    # C12: última foto
    ign = {c.upper() for c in ctx.c2["cajas_ignoradas"]}
    sin_mon = []
    ult = max(bl) if bl else None
    if ult is not None:
        for c, x in sorted(bl[ult]["saldo"].items()):
            if abs(x) > 0.005 and c not in ctx.mon_caja and c not in ctx.pyg and c not in ctx.invcols and c not in ign:
                sin_mon.append((c, x, ult))
    if sin_mon:
        if len(sin_mon) == 1:
            c, x, _ = sin_mon[0]
            det = (f"La caja {c} tiene un saldo de {_num_es(x)} y no sabemos en qué moneda está, así que no se suma al "
                   "total. Decile a Claude en qué moneda está, o que es una caja vieja, y deja de avisar.")
        else:
            det = ("Las cajas " + _y([f"{c} (saldo {_num_es(x)})" for c, x, _ in sin_mon]) + " no tienen moneda asignada, "
                   "así que no se suman al total. Decile a Claude en qué moneda está cada una, o cuáles son cajas viejas, "
                   "y dejan de avisar.")
        out.append(_check("C12", "aviso", TITULOS["C12"], det, [f"control:C12:{c}" for c, _, _ in sin_mon]))
    else:
        out.append(_check("C12", "ok", TITULOS["C12"], "Todas las columnas con saldo tienen moneda.", n=0))
    # C13
    princ = set(cfg["operadores_principales"])
    ult4 = b.ops[b.ops.fin & (b.ops.semana_n > ctx.nsem - 4)]
    otros = Counter(o for o in ult4.operador if o not in princ)
    if otros:
        out.append(_check("C13", "info", TITULOS["C13"],
                          "En las últimas 4 semanas cargaron operaciones fuera de la lista de operadores: "
                          + ", ".join(f"{o} ({n} {'operación' if n == 1 else 'operaciones'})" for o, n in otros.most_common())
                          + ".",
                          [f"control:C13:{o}" for o, _ in otros.most_common()]))
    else:
        out.append(_check("C13", "ok", TITULOS["C13"], "Solo operaron los operadores de la lista.", n=0))
    if parecidos:
        out.append(_check("C14", "info", TITULOS["C14"],
                          "Puede ser el mismo cliente escrito distinto: "
                          + "; ".join(f"«{c}» ({ctx.lbl[w]}) se parece a «{v}»" for w, c, v, _ in parecidos) + ".",
                          [f"control:C14:{c}" for _, c, _, _ in parecidos]))
    else:
        out.append(_check("C14", "ok", TITULOS["C14"], "Ningún cliente nuevo de las últimas 4 semanas se parece a uno existente.",
                          n=0))
    # C15
    cz = cfg["cotizaciones"]
    lo, hi = cfg["rango_cotizacion_ars"]
    mon = cfg["moneda_por_caja"]
    sub = b.ops[(b.ops.detalle == "Cajas") & b.ops.cotizacion.between(lo, hi)]
    obs = {sn for sn, x, y in zip(sub.semana_n, sub.caja_debe, sub.caja_haber)
           if {mon.get(x or ""), mon.get(y or "")} == {"USD", "ARS"}}
    us = b.ops[b.ops.fin & (b.ops.cliente == "USDT General") & b.ops.cotizacion.between(lo, hi)]
    obs_u = {sn for sn, x, y in zip(us.semana_n, us.caja_debe, us.caja_haber) if {x, y} == {"TRANSFER", "USDT"}}
    falta = []
    for w, s_ in enumerate(ctx.sem):
        que = []
        if not cz.get("ars_unica") and str(s_.idx) not in cz.get("ars_por_semana", {}) and s_.idx not in obs:
            que.append("pesos")
        if not cz.get("usdt_en_usd") and s_.idx not in obs_u:
            que.append("USDT")
        if que:
            falta.append((w, que))
    if falta:
        out.append(_check("C15", "aviso", TITULOS["C15"],
                          "Se usó la cotización de la semana anterior en: "
                          + "; ".join(f"{ctx.lbl[w]} ({' y '.join(q)})" for w, q in falta) + ".",
                          [f"control:C15:{ctx.ini[w]}" for w, _ in falta]))
    else:
        out.append(_check("C15", "ok", TITULOS["C15"], "Todas las semanas tienen cotización observada.", n=0))
    # C16
    cruza = [w for w, s_ in enumerate(ctx.sem) if s_.fin.year != s_.inicio.year]
    if int(cfg["anio"]) != ctx.corte.year or cruza:
        motivo = (f"la configuración del tablero dice {cfg['anio']} y la fecha de corte es de {ctx.corte.year}"
                  if int(cfg["anio"]) != ctx.corte.year else f"la hoja {ctx.lbl[cruza[0]]} cruza el año")
        out.append(_check("C16", "aviso", TITULOS["C16"], f"Revisar el año: {motivo}.", [f"control:C16:{cfg['anio']}"]))
    else:
        out.append(_check("C16", "ok", TITULOS["C16"], f"Todas las hojas son de {cfg['anio']}.", n=0))
    # C17
    pend_f = [r for r in regs if r["w"] == f and not r["revisada"]]
    if pend_f:
        na = sum(r["sev"] == "Alta" for r in pend_f)
        nm = len(pend_f) - na
        out.append(_check("C17", "info", TITULOS["C17"],
                          f"{len(pend_f)} {'fila' if len(pend_f) == 1 else 'filas'} de {ctx.lbl[f]} sin revisar ({na} "
                          f"{'grave' if na == 1 else 'graves'} y {nm} {'menor' if nm == 1 else 'menores'}).", n=len(pend_f)))
    else:
        out.append(_check("C17", "ok", TITULOS["C17"],
                          f"No hay diferencias de carga graves ni menores sin revisar en {ctx.lbl[f]}.", n=0))
    # C18
    ni = notas_info or {}
    if ni.get("tipo") == "migradas" and ni.get("n"):
        out.append(_check("C18", "info", TITULOS["C18"],
                          f"Se recuperaron {ni['n']} notas de una corrida anterior "
                          f"({os.path.basename(os.path.dirname(ni['archivo']))}): no estaba el archivo de notas.",
                          n=ni["n"]))
    elif ni.get("arrastradas"):
        na_ = ni["arrastradas"]
        out.append(_check("C18", "info", TITULOS["C18"],
                          f"Se {'copió' if na_ == 1 else 'copiaron'} {na_} {'nota abierta' if na_ == 1 else 'notas abiertas'} "
                          "(hallazgos y preguntas) al tablero anterior.", n=na_))
    else:
        out.append(_check("C18", "ok", TITULOS["C18"],
                          "Notas leídas del archivo de notas." if ni.get("tipo") == "manuales" else "No hay notas.", n=0))
    # chequeos que vienen de afuera (actualizar.py: escaneo C01–C04, C06 con su estado de publicación)
    externos = {}
    for c in list((plan or {}).get("control") or []) + list(getattr(ctx, "control_externo", None) or []):
        if isinstance(c, dict) and c.get("id"):
            externos[c["id"]] = _check(c["id"], c.get("nivel", "info"), c.get("titulo") or TITULOS.get(c["id"], c["id"]),
                                       c.get("detalle", ""), c.get("claves") or [], n=c.get("n"))
    if externos:
        ya = {c["id"] for c in out}
        out = [externos.get(c["id"], c) for c in out] + [c for i, c in externos.items() if i not in ya]
    cajas_sin = _tabla(["caja", "saldo", "w"], [[c, _f(x), w] for c, x, w in sin_mon])
    ops_otros = _tabla(["op", "n"], [[o, n] for o, n in otros.most_common()])
    return out, cajas_sin, ops_otros


# ============================================================================ alertas (3.2)
def _fecha_rev(rev, claves):
    """La fecha más reciente en que se revisaron las claves de una alerta agrupada (A01, A11)."""
    fechas = [e.get("fecha") for e in (rev.clave(k) for k in claves) if e and e.get("fecha")]
    return max(fechas) if fechas else None


def _aviso_corto(c, rev, corto=False):
    """Qué dice un aviso de control, en una frase, para la alerta A11 (con corto=True, sin mayúscula ni punto)."""
    pend = [k for k in c["claves"] if rev.clave(k) is None]
    n = len(pend)
    if c["id"] == "C12":
        cajas = [k.split(":", 2)[2] for k in pend]
        t = (f"caja {cajas[0]} sin moneda asignada: no se suma al total" if n == 1
             else f"cajas {_y(cajas)} sin moneda asignada: no se suman al total")
    elif c["id"] == "C08":
        t = f"el saldo al cierre no coincide con el Balance de la semana siguiente en {n} {'caja' if n == 1 else 'cajas'}"
    elif c["id"] == "C09":
        t = f"la plata afuera no coincide con la Apertura de la semana siguiente en {n} {'caja' if n == 1 else 'cajas'}"
    elif c["id"] == "C10":
        t = "hay Cierres diarios vacíos en la última semana cerrada"
    elif c["id"] == "C11":
        t = "hay operaciones sin Fin, Pen ni Can en la última semana cerrada"
    elif c["id"] == "C15":
        t = "hay semanas sin cotización observada (se usó la de la semana anterior)"
    elif c["id"] == "C16":
        t = "revisar el año de la planilla"
    elif c["id"] == "C01":
        t = "hay hojas con un nombre que no se reconoce"
    else:
        t = "control de carga: " + c["titulo"][0].lower() + c["titulo"][1:]
    return t if corto else t[0].upper() + t[1:] + "."


def _alerta(id_, sev, texto, ancla, clave=None, claves=None, rev=None):
    e = rev.clave(clave) if (rev is not None and clave) else None
    return dict(id=id_, sev=sev, texto=texto, ancla=ancla, clave=clave, claves=claves,
                revisada=int(e is not None), revisada_fecha=(e or {}).get("fecha"))


def _alertas(ctx, rev, regs, sem_filas, semanas_cli, bl, cheques, fondeo, ult_fijo, checks):
    U, f = ctx.U, ctx.foco
    al = []
    # A01
    altas = [r for r in regs if r["sev"] == "Alta"]
    sin = [r for r in altas if not r["revisada"]]
    if altas:
        de_f = [r for r in sin if r["w"] == f]
        if sin:
            txt = (f"{len(sin)} {'fila' if len(sin) == 1 else 'filas'} con diferencias de carga graves (USD 100 o más) "
                   "sin revisar" + (f" ({len(de_f)} de {ctx.lbl[f]})." if de_f else f", ninguna de {ctx.lbl[f]}."))
            al.append(dict(_alerta("A01", "critico" if de_f else "atencion", txt, "#control-revisar"),
                           claves=[r["clave"] for r in sin]))
        else:
            al.append(dict(_alerta("A01", "atencion", "La fila con diferencias de carga graves está revisada." if len(altas) == 1
                                   else f"Las {len(altas)} filas con diferencias de carga graves están revisadas.",
                                   "#control-revisar"), claves=[r["clave"] for r in altas], revisada=1,
                           revisada_fecha=_fecha_rev(rev, [r["clave"] for r in altas])))
    # A02. El umbral se toma contra el saldo de la planilla (Balance) de USD billete: la caja propia ya descuenta el
    # capital de los inversores, y compararla con un retiro contaría ese capital dos veces. En el texto van las dos.
    caja_usd = bal_usd = None
    if f in bl:
        caja_usd = sum(ctx.usd("USD", x, f) for c, x in bl[f]["caja"].items() if _es_caja(ctx, c) and ctx.moneda(c) == "USD")
        bal_usd = sum(ctx.usd("USD", x, f) for c, x in bl[f]["saldo"].items() if _es_caja(ctx, c) and ctx.moneda(c) == "USD")
    mes0 = ctx.corte.strftime("%Y-%m")
    mes1 = (ctx.corte.replace(day=1) + dt.timedelta(days=32)).strftime("%Y-%m")
    invs = [dict(zip(fondeo["inversores"]["c"], r)) for r in fondeo["inversores"]["f"]]
    ret = [i for i in invs if not i["propio"] and i["retiro_mes"] in (mes0, mes1)]
    tot_mes = defaultdict(float)
    for i in ret:
        tot_mes[i["retiro_mes"]] += i["monto_usd"] or 0
    n_mes = Counter(i["retiro_mes"] for i in ret)
    for i in ret:
        m = i["retiro_mes"]
        crit = bal_usd is not None and tot_mes[m] >= U["retiro_critico_pct_caja"] * max(bal_usd, 0)
        nombre_mes = MESES_LARGOS[int(m[5:]) - 1]
        txt = f"{i['inversor']} tiene previsto retirar {fmt_usd(i['monto_usd'])} en {nombre_mes}."
        if n_mes[m] > 1:
            txt += f" Con los otros retiros de {nombre_mes}, suman {fmt_usd(tot_mes[m])}."
        if crit:
            txt += (f" En USD billete hay {fmt_usd(bal_usd)} según la planilla ({fmt_usd(caja_usd)} sin la plata de "
                    "terceros).")
        al.append(_alerta("A02", "critico" if crit else "atencion", txt, "#saldos-inversores",
                          f"retiro:{i['inversor']}:{m}", rev=rev))
    # A03
    if cheques.get("vencidos_n"):
        # lo que explica el número va primero: si la hoja CQ no se actualiza, los "vencidos" pueden estar cobrados
        nv = cheques["vencidos_n"]
        meses = sorted({r[0] for r in cheques["venc"]["f"] if r[1]})
        cuando = ""
        if meses:
            nm = [MESES_LARGOS[int(x[5:]) - 1] + (f" de {x[:4]}" if x[:4] != str(ctx.corte.year) else "") for x in meses]
            cuando = f" en {nm[0]}" if len(nm) == 1 else f" entre {nm[0]} y {nm[-1]}"
        monto = (f"por {fmt_ars(cheques['vencidos_ars'])}"
                 + (f" (≈ {fmt_usd(cheques['vencidos_ars'] / cheques['cot'])})" if cheques.get("cot") else ""))
        ua = cheques.get("ultima_alta")
        vieja = ua and (ctx.corte - dt.date.fromisoformat(ua)).days > U["cheques_dias_sin_altas"]
        if vieja:
            txt = (f"La hoja de cheques no se actualiza desde el {_ddmm(ua)}: figuran {nv} "
                   f"{'cheque vencido' if nv == 1 else 'cheques vencidos'}{cuando} {monto}.")
        else:
            txt = f"{nv} {'cheque en cartera vencido' if nv == 1 else 'cheques en cartera vencidos'}{cuando} {monto}."
        txt += f" Confirmar si {'se cobró, se colocó o rebotó' if nv == 1 else 'se cobraron, se colocaron o rebotaron'}."
        al.append(_alerta("A03", "atencion", txt, "#saldos-cheques",
                          f"cheques:{int(round((cheques['vencidos_ars'] or 0) / 1000))}:{ua}", rev=rev))
    # A04 y A08 (foto de pendientes del foco, momento 0)
    items = bl[f]["items"] if f in bl else []
    tipo_usdt = ctx.c2["pendientes_tipos"][0]["tipo"]
    q = [x for x in items if x["tipo_pend"] == tipo_usdt and x["con_q"] and x["sem_abierto"] is not None
         and x["sem_abierto"] >= U["usdt_q_semanas"]]
    if q:
        n = len(q)
        al.append(_alerta("A04", "atencion",
                          f"{n} {'transferencia' if n == 1 else 'transferencias'} sin USDT confirmado hace "
                          f"{U['usdt_q_semanas']} semanas o más ({fmt_usd(sum(abs(x['usd']) for x in q))}).",
                          "#saldos-usdt", f"usdtq:{n}", rev=rev))
    viejos = [x for x in items if x["sem_abierto"] is not None and x["sem_abierto"] > U["pend_semanas_viejo"]]
    if viejos:
        n = len(viejos)
        al.append(_alerta("A08", "atencion",
                          f"{n} {'ítem' if n == 1 else 'ítems'} de plata afuera {'abierto' if n == 1 else 'abiertos'} hace "
                          f"más de {U['pend_semanas_viejo']} semanas ({fmt_usd(sum(abs(x['usd']) for x in viejos))}).",
                          "#saldos-afuera",
                          f"pendviejos:{n}", rev=rev))
    sinope = [x for x in items if x["sem_abierto"] is None]
    if sinope:
        n = len(sinope)
        al.append(_alerta("A08", "info",
                          f"{n} {'ítem' if n == 1 else 'ítems'} de plata afuera sin N° de Ope: no se sabe hace cuánto "
                          f"{'está abierto' if n == 1 else 'están abiertos'} ({fmt_usd(sum(abs(x['usd']) for x in sinope))}).",
                          "#saldos-afuera", f"sinope:{n}", rev=rev))
    # A05
    imp = ctx.c2["importantes"]
    vent = range(max(0, f - imp["ventana_semanas"] + 1), f + 1)
    sem_cal = sum(ctx.k[w] for w in vent)  # con la hoja doble adentro, 12 hojas son 13 semanas de calendario
    tot = {c: sum(d.get(w, (0, 0.0))[1] for w in vent) for c, d in semanas_cli.items()}
    top = [c for c, x in sorted(tot.items(), key=lambda t: (-t[1], t[0])) if x > 0][:imp["top"]]
    aus_w = range(max(0, f - imp["ausente_semanas"] + 1), f + 1)
    ausentes = [c for c in top if all(semanas_cli[c].get(w, (0, 0.0))[1] == 0 for w in aus_w)]
    top_al = set(top[:imp["top_alerta"]])
    if len(ausentes) >= 5:
        n_top = sum(c in top_al for c in ausentes)
        al.append(_alerta("A05", "info",
                          f"{len(ausentes)} de los {len(top)} mayores no operaron en {imp['ausente_semanas']} semanas; "
                          f"{n_top} {'está' if n_top == 1 else 'están'} entre los {imp['top_alerta']} mayores.",
                          "#clientes-novinieron", f"ausentes:{ctx.ini[f]}", rev=rev))
    else:
        for c in ausentes:
            if c not in top_al:
                continue
            ult = max(w for w in semanas_cli[c] if w <= f)
            al.append(_alerta("A05", "atencion",
                              f"{c} no operó en las últimas {imp['ausente_semanas']} semanas. Es uno de los "
                              f"{imp['top_alerta']} mayores de las últimas {sem_cal} semanas ({fmt_usd(tot[c])}); "
                              f"la última vez fue {ctx.lbl[ult]}.", "#clientes-novinieron",
                              f"ausente:{c}:{ctx.ini[ult]}", rev=rev))
    # A06 y A07
    u = [r["usd"] / ctx.k[r["w"]] for r in sem_filas]
    p4w = [j for j in range(max(0, f - 4), f) if j != ctx.en_curso]
    p4 = (sum(u[j] for j in p4w) / len(p4w)) if len(p4w) >= 2 else None
    if p4:
        d = u[f] / p4 - 1
        if abs(d) >= U["volumen_var_pct"]:
            al.append(_alerta("A06", "atencion" if d < 0 else "info",
                              f"El volumen de {ctx.lbl[f]} {'bajó' if d < 0 else 'subió'} {fmt_pct(abs(d))} contra el "
                              f"promedio de las 4 semanas anteriores ({fmt_usd(u[f])} contra {fmt_usd(p4)}"
                              + (" por semana" if ctx.k[f] != 1 else "") + ").", "#semana", f"vol:{ctx.ini[f]}", rev=rev))
    sf = sem_filas[f]
    if (sf["top1"] or 0) > U["top1_max"] or (sf["top5"] or 0) > U["top5_max"]:
        al.append(_alerta("A07", "atencion",
                          f"Los 5 mayores clientes hicieron el {fmt_pct(sf['top5'])} del volumen de {ctx.lbl[f]} "
                          f"(el mayor, {fmt_pct(sf['top1'])}).", "#clientes-concentracion", f"conc:{ctx.ini[f]}", rev=rev))
    # A09
    if ult_fijo:
        dias = (ctx.corte - dt.date.fromisoformat(ult_fijo)).days
        if dias > U["costos_fijos_dias"]:
            al.append(_alerta("A09", "info", f"Pasaron {dias} días desde el último costo fijo cargado ({_ddmm(ult_fijo)}).",
                              "#control-gastos", f"fijos:{ult_fijo}", rev=rev))
    # A10
    if f in bl:
        d = bl[f]
        por_mon, por_mon_usd, conf_mon = defaultdict(float), defaultdict(float), defaultdict(list)
        for c, x in d["caja"].items():
            if not _es_caja(ctx, c):
                continue
            m = ctx.moneda(c)
            if m == "Otra":
                continue
            por_mon[m] += x
            por_mon_usd[m] += ctx.usd(m, x, f)
            if abs(x) > 0.005 or abs(d["saldo"].get(c, 0.0)) > 0.005:
                conf_mon[m].append(_confiable(ctx, bl, f, c))
        for m, lim in (U.get("caja_minima") or {}).items():
            if lim is None or m not in por_mon or 0 in conf_mon[m]:
                continue
            if por_mon[m] < lim:
                unidad = "USDT " if m == "USDT" else "USD "
                al.append(_alerta("A10", "atencion",
                                  f"La caja de {'USD billete' if m == 'USD' else m} quedó en {fmt_usd(por_mon[m], unidad)}, "
                                  f"por debajo del mínimo de {fmt_usd(lim, unidad)}.", "#saldos-caja",
                                  f"caja:{m}:{ctx.ini[f]}", rev=rev))
        pm = U.get("pesos_max_pct")
        tot_usd = sum(v for v in por_mon_usd.values() if not np.isnan(v))
        if pm is not None and tot_usd > 0 and 0 not in conf_mon.get("ARS", []):
            pp = por_mon_usd.get("ARS", 0.0) / tot_usd
            if pp > pm:
                al.append(_alerta("A10", "info", f"Los pesos son el {fmt_pct(pp)} de la caja, por encima del {fmt_pct(pm)}.",
                                  "#saldos-caja", f"caja:ARS:{ctx.ini[f]}", rev=rev))
    # A11
    bloq = [k for c in checks if c["nivel"] == "bloqueante" for k in (c["claves"] or [f"control:{c['id']}"])]
    avisos = [k for c in checks if c["nivel"] == "aviso" for k in c["claves"]]
    av_sin = [k for k in avisos if rev.clave(k) is None]
    # los chequeos con algo sin revisar, para decir qué es (no solo cuántos)
    ch_sin = [c for c in checks if c["nivel"] == "aviso" and any(rev.clave(k) is None for k in c["claves"])]
    if bloq:
        nb = sum(c["nivel"] == "bloqueante" for c in checks)
        al.append(dict(_alerta("A11", "critico",
                               f"{nb} {'chequeo bloqueante' if nb == 1 else 'chequeos bloqueantes'} en la carga de datos"
                               + (f" y {len(av_sin)} {'aviso' if len(av_sin) == 1 else 'avisos'} sin revisar" if av_sin else "")
                               + ": revisá Control antes de publicar.", "#control"), claves=bloq + av_sin))
    elif av_sin:
        if len(ch_sin) == 1:
            txt = _aviso_corto(ch_sin[0], rev)
        else:
            txt = (f"{len(ch_sin)} avisos del control de carga sin revisar: "
                   + "; ".join(_aviso_corto(c, rev, corto=True) for c in ch_sin) + ".")
        al.append(dict(_alerta("A11", "atencion", txt, "#control"), claves=av_sin))
    elif avisos:
        al.append(dict(_alerta("A11", "atencion", "El aviso del control de carga está revisado." if len(avisos) == 1 else
                               f"Los {len(avisos)} avisos del control de carga están revisados.", "#control"),
                       claves=avisos, revisada=1, revisada_fecha=_fecha_rev(rev, avisos)))
    al.sort(key=lambda a: (SEV_ORDEN[a["sev"]], a["id"]))
    return al


# ============================================================================ armado
def construir_datos_v2(R, b, T, M, cz, cz_usdt, fecha, notas):
    """Contrato JSON "v": 2 (sección 4.2). notas = {"manuales": {...}, "control": [...], "fuentes": [rutas],
    "plan": {...}} y, opcionales, "previo" (estado_publicacion.json), "origen_notas" (de cargar_notas), "cheques" e
    "inversores" (DataFrames de R.cheques() y R.inversores(), para no releerlos)."""
    notas = notas or {}
    cfg = b.cfg
    ctx = _Ctx(R, b, T, M, cz, cz_usdt, fecha, cfg)
    rutas = list(notas.get("fuentes") or [])
    ctx.base_archivo = rutas[0] if rutas else ""  # R.wf.path es una ruta interna de openpyxl: no sirve
    ctx.control_externo = notas.get("control") or []
    ch = notas.get("cheques")
    if ch is None:
        ch = R.cheques()[0]
    inv = notas.get("inversores")
    if inv is None:
        inv = R.inversores()
    ctx.inv_df = inv
    manuales = normalizar_notas(notas.get("manuales") or {})
    rev = Revisadas(manuales["revisadas"])
    V = ctx.V

    # diccionarios
    vol_cli = V.groupby("cliente_g").prom_usd.sum().sort_values(ascending=False)
    bl = _bloques(ctx)
    cli_extra = sorted({x["cli"] for w in (ctx.foco, ctx.en_curso) if w is not None and w in bl for x in bl[w]["items"]}
                       - set(vol_cli.index))
    dic_cli = list(vol_cli.index) + cli_extra
    icli = _idx(dic_cli)
    dest = list(ctx.c2["operadores_destacados"])
    princ = [o for o in cfg["operadores_principales"] if o not in dest]
    cuenta_ops = Counter(b.ops.loc[b.ops.fin, "operador"])
    todos_op = set(b.ops.operador)
    resto = sorted((o for o in todos_op if o not in dest and o not in princ), key=lambda o: (-cuenta_ops.get(o, 0), o))
    dic_op = [o for o in dest + princ + resto if o in todos_op]
    t11 = T.get("11 Filas a revisar")
    if t11 is not None and not t11.empty:
        base = b.ops[["semana_n", "fila", "operador"]].drop_duplicates(["semana_n", "fila"])
        falta_op = t11.merge(base, on=["semana_n", "fila"], how="left", suffixes=("_g", "")).operador.isna().any()
        if falta_op and "Otros" not in dic_op:
            dic_op.append("Otros")
    iop = _idx(dic_op)
    op_grupo = [dest.index(o) if o in dest[:2] else 2 for o in dic_op]
    dic_prod = list(V.groupby("producto").prom_usd.sum().sort_values(ascending=False).index)
    iprod = _idx(dic_prod)
    tipos_com = list(ctx.c2["comisiones_lista"].keys()) or list(TIPOS_COM)
    tipos_com += [t for t in TIPOS_COM if t not in tipos_com]
    cats = [c for c, _ in A.CATS] + ["Otros"]

    # semanas y clientes
    infer, pct_inf = _fechas_inferidas(ctx)
    sem_filas, pasan, semanas_cli = _clientes(ctx)

    cubo = V.groupby(["w", "cliente_g", "operador", "producto"]).agg(n=("fila", "size"), usd=("prom_usd", "sum")).reset_index()
    cubo_t = _tabla(["w", "cli", "op", "prod", "n", "usd"],
                    [[int(r.w), icli[r.cliente_g], iop[r.operador], iprod[r.producto], int(r.n), _f(r.usd)]
                     for r in cubo.itertuples()])
    desde = max(0, ctx.nsem - 12)
    inact = []
    for w in range(desde, ctx.nsem):
        for c, ops_h, usd_h, L, sig in sorted(pasan.get(w, []), key=lambda x: -x[2]):
            inact.append([w, icli[c], ops_h, _f(usd_h), L, sig])
    inactivos = _tabla(["w", "cli", "ops_hist", "usd_hist", "ult_w", "vuelve_w"], inact)

    Vd = V.assign(inf=[infer.get((w, f_), 1) for w, f_ in zip(V.w, V.fila)])
    dia = Vd.groupby(["w", "fecha"]).agg(n=("fila", "size"), usd=("prom_usd", "sum"), inf=("inf", "max")).reset_index()
    dia_t = _tabla(["w", "fecha", "n", "usd", "inferida"],
                   [[int(r.w), _fecha(r.fecha), int(r.n), _f(r.usd), int(r.inf)] for r in dia.itertuples()])
    Vt = V.assign(tramo=pd.cut(V.prom_usd, bins=TRAMOS_BINS, labels=TRAMOS, right=False))
    tr = Vt.groupby(["w", "tramo"], observed=True).agg(n=("fila", "size"), usd=("prom_usd", "sum")).reset_index()
    itr = _idx(TRAMOS)
    tramos = _tabla(["w", "tramo", "n", "usd"], [[int(r.w), itr[r.tramo], int(r.n), _f(r.usd)] for r in tr.itertuples()])

    cajas, caja_t, invgar = _caja_tablas(ctx, bl)
    tipos_pend, pend_sem, fotos = _pend_tablas(ctx, bl)
    itp = _idx(tipos_pend)
    pend_t = _tabla(["w", "momento", "cli", "cli_txt", "tipo_pend", "detalle", "codigo", "ope", "w_origen", "sem_abierto",
                     "con_q", "usd", "nuevo", "fila"],
                    [[x["w"], x["momento"], icli[x["cli"]], x["cli_txt"], itp[x["tipo_pend"]], x["detalle"], x["codigo"],
                      x["ope"], x["w_origen"], x["sem_abierto"], x["con_q"], x["usd"], x["nuevo"], x["fila"]] for x in fotos])

    cheques = _cheques(ctx, ch)
    fondeo = _fondeo(ctx, inv)
    gastos, ult_fijo = _gastos(ctx, cats)
    revisar, regs = _revisar(ctx, rev, iop)
    calidad = _calidad(ctx, iop)
    ult8 = V[V.w >= ctx.nsem - 8].sort_values(["w", "fila"])
    det = _tabla(["w", "fecha", "cli", "op", "prod", "usd", "fila", "ope"],
                 [[int(r.w), _fecha(r.fecha), icli[r.cliente_g], iop[r.operador], iprod[r.producto], _f(r.prom_usd),
                   int(r.fila), _i(r.ope)] for r in ult8.itertuples()])

    parecidos = _parecidos(ctx, semanas_cli)
    checks, cajas_sin, ops_otros = _validaciones(ctx, bl, sem_filas, regs, notas.get("origen_notas"), notas.get("previo"),
                                                 notas.get("plan"), parecidos)
    for c in checks:
        c["revisada"] = int(c["nivel"] in ("aviso", "info") and bool(c["claves"])
                            and all(rev.clave(k) is not None for k in c["claves"]))
    checks.sort(key=lambda c: (NIVEL_ORDEN.get(c["nivel"], 9), c["id"]))
    alertas = _alertas(ctx, rev, regs, sem_filas, semanas_cli, bl, cheques, fondeo, ult_fijo, checks)

    nb = sum(c["nivel"] == "bloqueante" for c in checks)
    na = sum(c["nivel"] == "aviso" and not c["revisada"] for c in checks)
    estado_ult = "cerrada" if ctx.en_curso is None else "en curso"
    resumen = (f"{ctx.lbl[ctx.nsem - 1]} {estado_ult} · {ctx.nsem} {'semana' if ctx.nsem == 1 else 'semanas'} · {nb} "
               f"{'bloqueante' if nb == 1 else 'bloqueantes'} · {na} {'aviso' if na == 1 else 'avisos'}")
    origen = _tabla(["w", "archivo", "estado"],
                    [[w, R.origen.get(s.nombre), "en curso" if w == ctx.en_curso else "cerrada"] for w, s in enumerate(ctx.sem)])

    fmt_w = next((w for w, s in enumerate(ctx.sem) if s.estructura()["formato_actual"]), None)
    c = cfg["cotizaciones"]
    metodo = list(METODO_V2)
    if fmt_w is not None:
        metodo.append(f"El formato con saldos empieza el {_ddmm(ctx.sem[fmt_w].inicio)} ({ctx.lbl[fmt_w]}): antes no hay "
                      "caja ni plata afuera por semana.")
    lo, hi = cfg["rango_cotizacion_ars"]
    metodo.append(f"Precios: solo operaciones con cotización entre {_num_es(lo)} y {_num_es(hi)} pesos por dólar.")
    metodo.append(f"Cotizaciones fijas: 1 EUR = {_num_es(c['eur_en_usd'], 2)} USD; 1 USD = {_num_es(c['brl_por_usd'], 2)} "
                  f"reales; 1 GBP = {_num_es(c['gbp_en_usd'], 2)} USD; 1 USD exterior = {_num_es(c['usd_exterior_en_usd'], 2)} "
                  "USD billete.")

    vfecha = V.fecha.max()
    datos = {
        "v": VERSION,
        "generado": dt.datetime.now().strftime("%Y-%m-%dT%H:%M"),
        "fecha_corte": fecha,
        "titulo": TITULO,
        "fuentes": [dict(archivo=os.path.basename(p), rol="base" if i == 0 else "actualizacion",
                         hojas=sum(1 for o in R.origen.values() if o == os.path.basename(p))) for i, p in enumerate(rutas)],
        "foco": ctx.foco,
        "en_curso": ctx.en_curso,
        "semanas": _semanas(ctx, pct_inf),
        "dic": dict(cli=dic_cli, op=dic_op, prod=dic_prod, tipo_com=tipos_com, cat=cats, caja=cajas, mon=MONEDAS,
                    tipo_pend=tipos_pend, tramo=TRAMOS),
        "op_grupo": op_grupo,
        "cubo": cubo_t,
        "sem": _sem_tabla(sem_filas),
        "inactivos": inactivos,
        "parecidos": _tabla(["w", "cli", "cli_parecido", "ratio"], [[w, icli[c], icli[v], _f(r, 4)] for w, c, v, r in parecidos]),
        "dia": dia_t,
        "tramos": tramos,
        "precios": _precios(ctx),
        "usdt": _usdt(ctx),
        "comis": _comis(ctx, tipos_com),
        "caja": caja_t,
        "invgar": invgar,
        "pend_sem": pend_sem,
        "pend": pend_t,
        "cheques": cheques,
        "fondeo": fondeo,
        "gastos": gastos,
        "calidad": calidad,
        "revisar": revisar,
        "det": det,
        "frescura": dict(ultima_operacion=_fecha(vfecha), ultima_alta_cheques=cheques["ultima_alta"],
                         ultimo_costo_fijo=ult_fijo, base_archivo=os.path.basename(ctx.base_archivo) or None),
        "alertas": alertas,
        "control": dict(resumen=resumen, checks=checks, origen=origen, cajas_sin_moneda=cajas_sin,
                        operadores_otros=ops_otros),
        "notas": manuales,
        "config": dict(umbrales=ctx.U, comisiones_lista=ctx.c2["comisiones_lista"],
                       operadores_destacados=ctx.c2["operadores_destacados"],
                       semanas_tendencia=ctx.c2["semanas_tendencia"],
                       historia_altas_desde_semana=ctx.c2["historia_altas_desde_semana"],
                       importantes=ctx.c2["importantes"], signo_pendientes_confirmado=ctx.c2["signo_pendientes_confirmado"],
                       eur=c["eur_en_usd"], brl=c["brl_por_usd"], gbp=c["gbp_en_usd"]),
        "metodo": metodo,
    }
    return _limpio(datos)


def validar(R, b, T, M, cfg=None, plan=None, previo=None, notas=None, fecha=None, rutas=None):
    """Chequeos de 7.2 (C05 en adelante; C01–C04 vienen en plan["control"]) sin generar archivos, para actualizar.py.
    Usa b.cfg (cfg se acepta por compatibilidad con la firma de la spec). fecha: por defecto, el domingo de la última hoja."""
    fecha = fecha or R.actual.fin.isoformat()
    d = construir_datos_v2(R, b, T, M, b.cz, b.cz_usdt, fecha,
                           {"manuales": notas or {}, "plan": plan, "previo": previo, "fuentes": rutas or []})
    return d["control"]["checks"]


def validaciones(datos):
    """Lo que se escribe en validaciones.json: el bloque control más el contexto mínimo para leerlo."""
    ctl = datos["control"]
    return dict(v=datos["v"], generado=datos["generado"], fecha_corte=datos["fecha_corte"], resumen=ctl["resumen"],
                bloqueantes=sum(c["nivel"] == "bloqueante" for c in ctl["checks"]),
                avisos=sum(c["nivel"] == "aviso" and not c["revisada"] for c in ctl["checks"]),
                checks=ctl["checks"], cajas_sin_moneda=ctl["cajas_sin_moneda"], operadores_otros=ctl["operadores_otros"])


def serializar(obj):
    """JSON compacto, sin escapar acentos y con </ reemplazado por <\\/ (4.1)."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")


def generar_v2(datos, clave, ruta, artifact=False):
    """Inyecta el paquete en la plantilla v2: cifrar(datos, clave) con clave, {"plano": datos} sin clave.
    Devuelve la ruta, o None si todavía no existe la plantilla."""
    if not os.path.exists(PLANTILLA_V2):
        return None
    paquete = cifrar(datos, clave) if clave else {"plano": datos}
    html = open(PLANTILLA_V2, encoding="utf-8").read()
    marca = "/*__PAQUETE__*/null"
    if marca not in html:
        raise ValueError(f"La plantilla {PLANTILLA_V2} no tiene {marca}")
    html = html.replace(marca, serializar(paquete), 1)
    if artifact:
        html = version_artifact(html)
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write(html)
    return ruta
