"""Los análisis del Registro General.

Cada función recibe tablas de `leer.py` y devuelve (tablas, métricas):
- tablas: dict nombre -> DataFrame (van al Excel)
- métricas: dict con los números clave (van a metricas.json y al resumen del asesor)

Montos en USD = promedio neto ((Debe + Haber) / 2) pasado a USD con config.json.
"""
import re
import unicodedata
from collections import defaultdict

import numpy as np
import pandas as pd

USD_FAM = {"USD", "CAMBIO", "CARA CHICA", "MALOS"}
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


# ----------------------------------------------------------------------------- base
class Base:
    def __init__(self, ops, cz, cfg, semana_actual, cz_usdt):
        self.cfg, self.cz, self.actual, self.cz_usdt = cfg, cz, semana_actual, cz_usdt
        self.mon_caja = cfg["moneda_por_caja"]
        ops = ops.copy()
        ops["mon_debe"] = ops.caja_debe.map(self.moneda)
        ops["mon_haber"] = ops.caja_haber.map(self.moneda)
        ops["debe_usd"] = [self.usd(m, a, s) for m, a, s in zip(ops.mon_debe, ops.debe, ops.semana_n)]
        ops["haber_usd"] = [self.usd(m, a, s) for m, a, s in zip(ops.mon_haber, ops.haber, ops.semana_n)]
        ops["prom_usd"] = (ops.debe_usd.fillna(0) + ops.haber_usd.fillna(0)) / 2
        ops["cliente_g"] = ops.cliente.map(grupo_cliente)
        ops["mes"] = ops.fecha.dt.to_period("M").astype(str)
        ops["producto"] = [producto(r) for r in ops.itertuples()]
        principales = set(cfg["operadores_principales"])
        ops["operador_g"] = ops.operador.where(ops.operador.isin(principales), "Otros")
        self.ops = ops
        excl = set(cfg["excluir_clientes_de_volumen"])
        self.vol = ops[ops.fin & ops.detalle.isin(cfg["detalles_que_son_volumen"]) & ~ops.cliente.isin(excl)
                       & ops.mon_debe.notna() & ops.mon_haber.notna()
                       & (ops.mon_debe != "Otra") & (ops.mon_haber != "Otra")].copy()
        self.ultima_completa = semana_actual - 1

    def moneda(self, caja):
        if not isinstance(caja, str) or not caja:
            return None
        return self.mon_caja.get(caja.upper(), "Otra")

    def usd(self, mon, monto, semana):
        if monto is None or (isinstance(monto, float) and np.isnan(monto)) or not isinstance(mon, str) or mon == "Otra":
            return np.nan
        c = self.cfg["cotizaciones"]
        return {"USD": monto, "USD Exterior": monto * c["usd_exterior_en_usd"], "USDT": monto * self.cz_usdt[semana],
                "ARS": monto / self.cz[semana], "EUR": monto * c["eur_en_usd"], "BRL": monto / c["brl_por_usd"],
                "GBP": monto * c["gbp_en_usd"]}[mon]


def _norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", s).strip()


_display = {}


def grupo_cliente(nombre):
    """Agrupa variantes: saca lo que va entre paréntesis y normaliza acentos/mayúsculas."""
    base = re.sub(r"\(.*?\)", "", str(nombre)).strip() or str(nombre)
    k = _norm(base)
    _display.setdefault(k, base)
    return _display[k]


def producto(r):
    if r.detalle == "Recaudadora":
        return "Recaudación"
    m = {r.mon_debe, r.mon_haber}
    cajas = {r.caja_debe, r.caja_haber}
    if "CHEQUES" in cajas:
        return "Cheques"
    if "USDT" in m:
        return "USDT"
    if "USD Exterior" in m:
        return "USD exterior"
    if m & {"EUR", "BRL", "GBP"}:
        return "Divisas (EUR/BRL)"
    if m == {"USD", "ARS"}:
        return "USD ↔ Transferencia" if "TRANSFER" in cajas else "USD ↔ Pesos billete"
    if m == {"USD"}:
        return "Canje de billetes USD"
    if m == {"ARS"}:
        return "Pesos ↔ Transferencia"
    return "Otros"


def _share(df, col, total):
    df[f"% {col}"] = df[col] / total if total else 0
    return df


# ----------------------------------------------------------------------------- 1
def ranking_clientes(b):
    v = b.vol
    g = v.groupby("cliente_g").agg(operaciones=("fila", "size"), volumen_usd=("prom_usd", "sum"),
                                   ticket_promedio_usd=("prom_usd", "mean"), primera_semana=("semana_n", "min"),
                                   ultima_semana=("semana_n", "max"))
    op_top = v.groupby(["cliente_g", "operador"]).prom_usd.sum().reset_index().sort_values("prom_usd", ascending=False)
    g["operador_principal"] = op_top.drop_duplicates("cliente_g").set_index("cliente_g").operador
    g = g.sort_values("volumen_usd", ascending=False)
    tot = g.volumen_usd.sum()
    g["% del total"] = g.volumen_usd / tot
    g["% acumulado"] = g["% del total"].cumsum()
    g = g.reset_index().rename(columns={"cliente_g": "cliente"})
    g.insert(0, "puesto", range(1, len(g) + 1))
    sh = g["% del total"]
    met = dict(clientes_activos=int(len(g)), volumen_total_usd=float(tot),
               top1_pct=float(sh.iloc[0]), top10_pct=float(sh.head(10).sum()), top20_pct=float(sh.head(20).sum()),
               clientes_para_80pct=int((g["% acumulado"] < 0.8).sum() + 1),
               hhi=float((sh ** 2).sum() * 10000),
               top10=[dict(cliente=r.cliente, volumen_usd=round(r.volumen_usd), pct=round(r.pct, 4), ops=int(r.operaciones))
                      for r in g.head(10).rename(columns={'% del total': 'pct'}).itertuples()])
    return {"01 Ranking clientes": g}, met


# ----------------------------------------------------------------------------- 2
def altas_bajas(b, semanas_perdido):
    v = b.vol
    c = v.groupby("cliente_g").agg(primera_semana=("semana_n", "min"), ultima_semana=("semana_n", "max"),
                                   primer_mes=("mes", "min"), operaciones=("fila", "size"),
                                   volumen_usd=("prom_usd", "sum"), ultima_fecha=("fecha", "max")).reset_index()
    meses = sorted(v.mes.unique())
    filas = []
    for m in meses:
        act = set(v.loc[v.mes == m, "cliente_g"])
        nuevos = set(c.loc[c.primer_mes == m, "cliente_g"])
        filas.append(dict(mes=m, clientes_activos=len(act), nuevos=len(nuevos), recurrentes=len(act - nuevos),
                          volumen_usd=v.loc[v.mes == m, "prom_usd"].sum(),
                          volumen_nuevos_usd=v.loc[(v.mes == m) & v.cliente_g.isin(nuevos), "prom_usd"].sum()))
    mens = pd.DataFrame(filas)
    mens["% volumen de nuevos"] = mens.volumen_nuevos_usd / mens.volumen_usd
    corte = b.ultima_completa - semanas_perdido
    perd = c[(c.operaciones >= 3) & (c.ultima_semana <= corte)].sort_values("volumen_usd", ascending=False)
    perd = perd.rename(columns={"cliente_g": "cliente"})
    c = c.rename(columns={"cliente_g": "cliente"}).sort_values("primera_semana")
    met = dict(clientes_nuevos_por_mes={r.mes: int(r.nuevos) for r in mens.itertuples()},
               clientes_activos_por_mes={r.mes: int(r.clientes_activos) for r in mens.itertuples()},
               clientes_perdidos=int(len(perd)), volumen_historico_perdidos_usd=float(perd.volumen_usd.sum()),
               top_perdidos=[dict(cliente=r.cliente, volumen_usd=round(r.volumen_usd), ultima_semana=int(r.ultima_semana))
                             for r in perd.head(10).itertuples()])
    return {"02 Altas y bajas (mes)": mens, "02 Clientes perdidos": perd, "02 Clientes (alta-baja)": c}, met


# ----------------------------------------------------------------------------- 3
def cliente_operador(b, top=40):
    v = b.vol
    piv = v.pivot_table(index="cliente_g", columns="operador_g", values="prom_usd", aggfunc="sum", fill_value=0)
    piv["Total"] = piv.sum(axis=1)
    piv = piv.sort_values("Total", ascending=False)
    ops_cols = [c for c in piv.columns if c != "Total"]
    piv["operadores que lo atienden"] = (piv[ops_cols] > 0).sum(axis=1)
    piv["% del operador principal"] = piv[ops_cols].max(axis=1) / piv.Total
    tabla = piv.head(top).reset_index().rename(columns={"cliente_g": "cliente"})
    resumen = []
    for op in ops_cols:
        s = piv[op][piv[op] > 0]
        exclusivos = piv[(piv[op] > 0) & (piv["operadores que lo atienden"] == 1)]
        resumen.append(dict(operador=op, clientes=int(len(s)), clientes_exclusivos=int(len(exclusivos)),
                            volumen_usd=float(s.sum()),
                            volumen_de_exclusivos_usd=float(exclusivos[op].sum()),
                            top3_clientes=", ".join(s.sort_values(ascending=False).head(3).index)))
    res = pd.DataFrame(resumen).sort_values("volumen_usd", ascending=False)
    met = dict(clientes_compartidos=int((piv["operadores que lo atienden"] > 1).sum()),
               por_operador={r.operador: dict(clientes=r.clientes, exclusivos=r.clientes_exclusivos) for r in res.itertuples()})
    return {"03 Operador resumen": res, "03 Cliente x operador": tabla}, met


# ----------------------------------------------------------------------------- 4
def spread_billete(b):
    lo, hi = b.cfg["rango_cotizacion_ars"]
    o = b.ops[b.ops.fin & (b.ops.detalle == "Cajas") & b.ops.cotizacion.between(lo, hi)].copy()
    canal_de = {"PESOS": "Pesos billete", "TRANSFER": "Transferencia"}
    rows = []
    for r in o.itertuples():
        if r.caja_debe == "USD" and r.caja_haber in canal_de and r.debe:
            rows.append((r.Index, "compra", canal_de[r.caja_haber], r.debe))
        elif r.caja_haber == "USD" and r.caja_debe in canal_de and r.haber:
            rows.append((r.Index, "venta", canal_de[r.caja_debe], r.haber))
    t = pd.DataFrame(rows, columns=["idx", "lado", "canal", "usd"]).set_index("idx")
    o = o.join(t, how="inner")
    o = o[~o.cliente.isin(b.cfg["excluir_clientes_de_volumen"])]
    o["k_x_usd"] = o.cotizacion * o.usd
    d = o.groupby(["fecha", "canal", "lado"]).agg(usd=("usd", "sum"), kx=("k_x_usd", "sum")).unstack("lado")
    d.columns = [f"{a}_{b_}" for a, b_ in d.columns]
    d = d.reset_index()
    for lado in ("compra", "venta"):
        d[f"cot_{lado}"] = d[f"kx_{lado}"] / d[f"usd_{lado}"]
    d["spread_pesos"] = d.cot_venta - d.cot_compra
    d["usd_calzados"] = d[["usd_compra", "usd_venta"]].min(axis=1)
    sem = o.drop_duplicates("fecha").set_index("fecha").semana_n
    d["semana_n"] = d.fecha.map(sem)
    d["cot_ref"] = d.semana_n.map(b.cz)
    d["ganancia_spread_usd"] = (d.spread_pesos * d.usd_calzados / d.cot_ref).where(d.usd_calzados > 0)
    d["spread_%"] = d.spread_pesos / ((d.cot_venta + d.cot_compra) / 2)
    # ganancia por operación respecto del precio medio del día y canal
    mid = d.set_index(["fecha", "canal"])[["cot_compra", "cot_venta"]].mean(axis=1)
    o["ref"] = [mid.get((f, c), np.nan) for f, c in zip(o.fecha, o.canal)]
    o["gan_op_usd"] = np.where(o.lado == "compra", (o.ref - o.cotizacion), (o.cotizacion - o.ref)) * o.usd / o.semana_n.map(b.cz)
    por_op = o.groupby(["operador_g", "lado"]).agg(usd=("usd", "sum"), cot_media=("k_x_usd", "sum"),
                                                    ganancia_vs_medio_usd=("gan_op_usd", "sum")).reset_index()
    por_op["cot_media"] = por_op.cot_media / por_op.usd
    por_op["ganancia_cada_1000_usd"] = por_op.ganancia_vs_medio_usd / por_op.usd * 1000
    por_cli = o.groupby("cliente_g").agg(usd=("usd", "sum"), ganancia_vs_medio_usd=("gan_op_usd", "sum")).reset_index()
    por_cli["ganancia_cada_1000_usd"] = por_cli.ganancia_vs_medio_usd / por_cli.usd * 1000
    por_cli = por_cli[por_cli.usd >= 5000].sort_values("ganancia_cada_1000_usd")
    d["mes"] = pd.to_datetime(d.fecha).dt.to_period("M").astype(str)
    mens = d.groupby(["mes", "canal"]).agg(usd_compra=("usd_compra", "sum"), usd_venta=("usd_venta", "sum"),
                                           usd_calzados=("usd_calzados", "sum"),
                                           ganancia_spread_usd=("ganancia_spread_usd", "sum")).reset_index()
    mens["ganancia_cada_1000_calzados"] = mens.ganancia_spread_usd / mens.usd_calzados * 1000
    met = dict(ganancia_spread_total_usd=float(d.ganancia_spread_usd.sum()),
               spread_mediano_pesos={c: float(d.loc[d.canal == c, "spread_pesos"].median()) for c in canal_de.values()},
               spread_mediano_pct={c: float(d.loc[d.canal == c, "spread_%"].median()) for c in canal_de.values()},
               usd_calzados_total=float(d.usd_calzados.sum()),
               usd_comprados=float(o.loc[o.lado == "compra", "usd"].sum()),
               usd_vendidos=float(o.loc[o.lado == "venta", "usd"].sum()),
               dias_con_spread_negativo=int((d.spread_pesos < 0).sum()),
               ganancia_mensual_usd={m: float(x) for m, x in mens.groupby("mes").ganancia_spread_usd.sum().items()},
               por_operador={f"{r.operador_g} {r.lado}": dict(usd=round(r.usd), cot_media=round(r.cot_media, 1),
                                                              gan_cada_1000=round(r.ganancia_cada_1000_usd, 2))
                             for r in por_op.itertuples()})
    d = d.drop(columns=["kx_compra", "kx_venta"])
    return {"04 Spread diario": d, "04 Spread mensual": mens, "04 Spread por operador": por_op,
            "04 Spread por cliente": por_cli}, met


# ----------------------------------------------------------------------------- 5
def circuito_usdt(b):
    o = b.ops[b.ops.fin].copy()
    ug = o[(o.cliente == "USDT General")]
    pares = []
    for r in ug.itertuples():
        # fila USDT General con TRANSFER de un lado y USDT del otro
        if {r.caja_debe, r.caja_haber} != {"TRANSFER", "USDT"} or r.debe is None or r.haber is None \
                or np.isnan(r.debe) or np.isnan(r.haber):
            continue
        tr_monto = r.debe if r.caja_debe == "TRANSFER" else r.haber
        tr_entra = r.caja_debe == "TRANSFER"
        cand = o[(o.semana == r.semana) & (o.fila < r.fila) & (o.fila >= r.fila - 3) & (o.cliente != "USDT General")]
        for c in cand.sort_values("fila", ascending=False).itertuples():
            lado_tr = ("haber" if tr_entra else "debe")
            caja = c.caja_haber if lado_tr == "haber" else c.caja_debe
            monto = c.haber if lado_tr == "haber" else c.debe
            if caja == "TRANSFER" and monto and abs(monto - tr_monto) <= max(1, tr_monto * 0.005):
                otro_mon = c.mon_debe if lado_tr == "haber" else c.mon_haber
                otro_usd = c.debe_usd if lado_tr == "haber" else c.haber_usd
                usdt_usd = r.haber_usd if tr_entra else r.debe_usd
                if otro_mon not in ("USD", "USD Exterior") or np.isnan(otro_usd) or np.isnan(usdt_usd):
                    break
                # cliente entrega USD y recibe transferencia -> pagamos USDT; o al revés
                gan = (otro_usd - usdt_usd) if tr_entra else (usdt_usd - otro_usd)
                k_cli = c.cotizacion
                pares.append(dict(semana=r.semana, semana_n=r.semana_n, fecha=r.fecha, mes=r.mes, fila_cliente=c.fila,
                                  fila_usdt=r.fila, cliente=c.cliente_g, operador=c.operador_g,
                                  sentido="Cliente da USD, recibe transferencia" if tr_entra else "Cliente da transferencia, recibe USD",
                                  transferencia_ars=tr_monto, usd_cliente=otro_usd, usdt=usdt_usd,
                                  cot_cliente=k_cli, cot_usdt=r.cotizacion, ganancia_usd=gan))
                break
    p = pd.DataFrame(pares)
    if p.empty:
        return {"05 Circuito USDT": p}, {}
    p["margen_%"] = p.ganancia_usd / p.usd_cliente
    mens = p.groupby("mes").agg(operaciones=("fila_usdt", "size"), usd=("usd_cliente", "sum"),
                                ganancia_usd=("ganancia_usd", "sum")).reset_index()
    mens["margen_%"] = mens.ganancia_usd / mens.usd
    por_op = p.groupby("operador").agg(operaciones=("fila_usdt", "size"), usd=("usd_cliente", "sum"),
                                       ganancia_usd=("ganancia_usd", "sum")).reset_index()
    por_op["margen_%"] = por_op.ganancia_usd / por_op.usd
    usdt_g = b.ops[b.ops.fin & (b.ops.cliente == "USDT General")]
    met = dict(pares_encontrados=int(len(p)), filas_usdt_general=int(len(usdt_g)),
               usd_operados=float(p.usd_cliente.sum()), ganancia_usd=float(p.ganancia_usd.sum()),
               margen_medio=float(p.ganancia_usd.sum() / p.usd_cliente.sum()),
               margen_mediano=float(p["margen_%"].median()),
               pares_con_perdida=int((p.ganancia_usd < 0).sum()),
               ganancia_mensual_usd={r.mes: float(r.ganancia_usd) for r in mens.itertuples()})
    return {"05 Circuito USDT": p, "05 Circuito mensual": mens, "05 Circuito por operador": por_op}, met


# ----------------------------------------------------------------------------- 6
def comisiones(b):
    o = b.ops[b.ops.fin & b.ops.detalle.isin(["Cajas", "Recaudadora"]) & (b.ops.cliente != "USDT General")].copy()
    o = o[o.cotizacion.between(0.01, b.cfg["max_comision_pct"])]
    tipos = []
    for r in o.itertuples():
        m = {r.mon_debe, r.mon_haber}
        cajas = {r.caja_debe, r.caja_haber}
        if r.detalle == "Recaudadora" or (m == {"ARS"} and "CHEQUES" not in cajas):
            t = "Recaudación / pesos↔transfer"
        elif "CHEQUES" in cajas:
            t = None  # descuento de cheques: se analiza aparte
        elif m == {"USD", "USD Exterior"}:
            t = "USD exterior ↔ billete"
        elif m == {"USD", "USDT"}:
            t = "USDT ↔ billete"
        elif m == {"USD"} and cajas != {"USD"}:
            t = "Canje billetes (BsAs, cara chica, malos)"
        elif m == {"USD Exterior", "USDT"}:
            t = "USD exterior ↔ USDT"
        else:
            t = None
        tipos.append(t)
    o["tipo"] = tipos
    o = o[o.tipo.notna() & o.debe_usd.notna() & o.haber_usd.notna()]
    o["comision_usd"] = o.debe_usd - o.haber_usd
    o["volumen_usd"] = o.debe_usd
    res = o.groupby("tipo").agg(operaciones=("fila", "size"), volumen_usd=("volumen_usd", "sum"),
                                comision_usd=("comision_usd", "sum"), pct_pactado_mediano=("cotizacion", "median")).reset_index()
    res["% efectivo"] = res.comision_usd / res.volumen_usd
    cli = o.groupby(["tipo", "cliente_g"]).agg(operaciones=("fila", "size"), volumen_usd=("volumen_usd", "sum"),
                                               comision_usd=("comision_usd", "sum"),
                                               pct_pactado_medio=("cotizacion", "mean")).reset_index()
    cli["% efectivo"] = cli.comision_usd / cli.volumen_usd
    cli = cli.sort_values("volumen_usd", ascending=False)
    op = o.groupby(["tipo", "operador_g"]).agg(volumen_usd=("volumen_usd", "sum"), comision_usd=("comision_usd", "sum")).reset_index()
    op["% efectivo"] = op.comision_usd / op.volumen_usd
    mens = o.groupby("mes").comision_usd.sum()
    met = dict(comision_total_usd=float(o.comision_usd.sum()),
               por_tipo={r.tipo: dict(volumen_usd=round(r.volumen_usd), comision_usd=round(r.comision_usd),
                                      pct_efectivo=round(r.pct_ef, 4), pct_pactado_mediano=round(r.pct_pactado_mediano, 3))
                         for r in res.rename(columns={'% efectivo': 'pct_ef'}).itertuples()},
               comision_mensual_usd={m: float(x) for m, x in mens.items()})
    return {"06 Comisiones por tipo": res, "06 Comisiones por cliente": cli, "06 Comisiones por operador": op}, met


# ----------------------------------------------------------------------------- 7
def cheques(ch, resumen, cz_actual, hoy, cot_mes):
    if ch.empty:
        return {}, {}
    ch = ch.copy()
    ch["vencimiento"] = pd.to_datetime(ch.vencimiento)
    ch["estado"] = np.where(ch.cobrado, "Cobrado", np.where(ch.colocado, "Colocado (pasado a terceros)", "En cartera"))
    cart = ch[ch.estado == "En cartera"].copy()
    cart["vencido"] = cart.vencimiento < pd.Timestamp(hoy)
    cart["mes_venc"] = cart.vencimiento.dt.to_period("M").astype(str)
    por_tit = ch.groupby("titular").agg(cheques=("monto", "size"), monto=("monto", "sum"),
                                        en_cartera=("monto", lambda s: s[ch.loc[s.index, "estado"] == "En cartera"].sum())).reset_index()
    por_tit["% del total"] = por_tit.monto / por_tit.monto.sum()
    por_tit = por_tit.sort_values("monto", ascending=False)
    venc = cart.groupby(["mes_venc", "vencido"]).monto.sum().reset_index()
    tasa = ch.loc[ch.tasa_mensual.notna() & (ch.tasa_mensual > 0), "tasa_mensual"]
    ch["mes"] = pd.to_datetime(ch.fecha, errors="coerce").dt.to_period("M").astype(str)
    gan = ch[ch.comision.notna() & (ch.comision > 0)]
    gan_mes = gan.groupby("mes").comision.sum()
    gan_mes_usd = {m: float(x / cot_mes.get(m, cz_actual)) for m, x in gan_mes.items() if m != "NaT"}
    met = dict(resumen_hoja_CQ=resumen,
               resumen_hoja_CQ_usd={k: (v / cz_actual if isinstance(v, (int, float)) else v) for k, v in resumen.items()},
               cheques_listados=int(len(ch)), monto_total_ars=float(ch.monto.sum()),
               en_cartera_ars=float(cart.monto.sum()), en_cartera_usd=float(cart.monto.sum() / cz_actual),
               en_cartera_vencidos_ars=float(cart.loc[cart.vencido, "monto"].sum()),
               tasa_mensual_mediana=float(tasa.median()) if len(tasa) else None,
               dias_mediano=float(ch.dias.median()) if ch.dias.notna().any() else None,
               top_titulares=[dict(titular=r.titular, pct=round(r.pct, 4), monto_ars=round(r.monto))
                              for r in por_tit.head(5).rename(columns={'% del total': 'pct'}).itertuples()],
               top3_titulares_pct=float(por_tit["% del total"].head(3).sum()),
               ganancia_mensual_usd=gan_mes_usd,
               nota="'En cartera' = ni cobrado ni colocado según las tildes de la hoja. Si figuran vencidos, verificar si ya se cobraron o rebotaron.")
    return {"07 Cheques detalle": ch, "07 Cheques por titular": por_tit, "07 Cheques vencimientos": venc}, met


# ----------------------------------------------------------------------------- 8
def evolucion(b):
    v = b.vol
    sem = v.pivot_table(index=["semana_n", "semana"], columns="producto", values="prom_usd", aggfunc="sum", fill_value=0)
    sem["Total"] = sem.sum(axis=1)
    sem = sem.reset_index()
    mes = v.pivot_table(index="mes", columns="producto", values="prom_usd", aggfunc="sum", fill_value=0)
    mes["Total"] = mes.sum(axis=1)
    ops_mes = v.groupby("mes").size()
    mes["operaciones"] = ops_mes
    mes = mes.reset_index()
    tot = v.groupby("producto").prom_usd.sum().sort_values(ascending=False)
    completas = sem[sem.semana_n <= b.ultima_completa]
    ult4 = completas.tail(4).Total.mean()
    prev4 = completas.iloc[-8:-4].Total.mean() if len(completas) >= 8 else np.nan
    met = dict(volumen_por_producto_usd={k: float(x) for k, x in tot.items()},
               participacion_producto={k: float(x / tot.sum()) for k, x in tot.items()},
               volumen_mensual_usd={r.mes: float(r.Total) for r in mes.itertuples()},
               promedio_semanal_ult4_usd=float(ult4), promedio_semanal_4_previas_usd=float(prev4),
               variacion_ult4_vs_previas=float(ult4 / prev4 - 1) if prev4 else None,
               mejor_semana=dict(semana=sem.loc[sem.Total.idxmax(), "semana"], usd=float(sem.Total.max())),
               peor_semana_completa=dict(semana=completas.loc[completas.Total.idxmin(), "semana"], usd=float(completas.Total.min())))
    return {"08 Evolución semanal": sem, "08 Evolución mensual": mes}, met


# ----------------------------------------------------------------------------- 9
def dia_semana(b):
    v = b.vol.copy()
    v["dia"] = v.fecha.dt.dayofweek.map(dict(enumerate(DIAS)))
    dias_distintos = v.groupby("dia").fecha.nunique()
    t = v.groupby("dia").agg(operaciones=("fila", "size"), volumen_usd=("prom_usd", "sum")).reindex(DIAS).dropna(how="all")
    t["días con actividad"] = dias_distintos
    t["volumen promedio por día_usd"] = t.volumen_usd / t["días con actividad"]
    t["operaciones promedio por día"] = t.operaciones / t["días con actividad"]
    po = v.pivot_table(index="dia", columns="operador_g", values="prom_usd", aggfunc="sum", fill_value=0).reindex(DIAS).dropna(how="all")
    po = po.div(dias_distintos.reindex(po.index), axis=0)
    met = dict(volumen_promedio_por_dia_usd={d: float(x) for d, x in t["volumen promedio por día_usd"].items()},
               nota="Fecha por día inferida de los Cierre diarios; aproximada cuando la hoja no tiene fecha.")
    return {"09 Día de la semana": t.reset_index(), "09 Día x operador (prom)": po.reset_index()}, met


# ----------------------------------------------------------------------------- 10
def tamano(b):
    v = b.vol.copy()
    bins = [0, 500, 1000, 5000, 20000, 50000, np.inf]
    labels = ["< 500", "500 – 1.000", "1.000 – 5.000", "5.000 – 20.000", "20.000 – 50.000", "> 50.000"]
    v["tramo"] = pd.cut(v.prom_usd, bins=bins, labels=labels, right=False)
    t = v.groupby("tramo", observed=False).agg(operaciones=("fila", "size"), volumen_usd=("prom_usd", "sum")).reset_index()
    t["% operaciones"] = t.operaciones / t.operaciones.sum()
    t["% volumen"] = t.volumen_usd / t.volumen_usd.sum()
    po = v.pivot_table(index="operador_g", columns="tramo", values="fila", aggfunc="size", fill_value=0, observed=False)
    po = po.div(po.sum(axis=1), axis=0)
    st = v.groupby("operador_g").prom_usd.describe(percentiles=[.5, .9])[["count", "mean", "50%", "90%", "max"]]
    st.columns = ["operaciones", "ticket promedio", "mediana", "percentil 90", "máxima"]
    grandes = v.sort_values("prom_usd", ascending=False).head(30)[["semana", "fila", "operador", "cliente", "debe", "caja_debe",
                                                                    "haber", "caja_haber", "prom_usd"]]
    met = dict(por_tramo={str(r.tramo): dict(ops_pct=round(r.po, 4), vol_pct=round(r.pv, 4)) for r in t.rename(columns={'% operaciones': 'po', '% volumen': 'pv'}).itertuples()},
               ticket_mediano_usd=float(v.prom_usd.median()), ticket_promedio_usd=float(v.prom_usd.mean()),
               ops_mayores_20k_pct_volumen=float(t.loc[t.tramo.isin(labels[4:]), "% volumen"].sum()))
    return {"10 Tamaño ops": t, "10 Tamaño x operador (% ops)": po.reset_index(),
            "10 Ticket por operador": st.reset_index(), "10 Operaciones más grandes": grandes}, met


# ----------------------------------------------------------------------------- 11
def calidad_carga(b):
    """Diferencias entre lo imputado en las columnas de caja y lo que dicen Debe/Haber."""
    o = b.ops[(b.ops.semana_n < b.actual)].copy()
    fam_ancha = lambda m: "ARS" if m == "ARS" else m
    col_mon = lambda c: ("USD" if c.upper() in USD_FAM or c.upper() == "USD BSAS" else b.moneda(c))
    problemas = []
    for r in o.itertuples():
        imp = r.imputado or {}
        tipo = None
        dif_usd = 0.0
        if r.can and imp:
            tipo = "Cancelada con imputación"
        elif not (r.fin or r.pen or r.can) and imp:
            tipo = "Sin estado con imputación"
        elif r.fin and imp and r.mon_debe and r.mon_haber and r.mon_debe != r.mon_haber \
                and "Otra" not in (r.mon_debe, r.mon_haber) and not np.isnan(r.debe if r.debe is not None else np.nan) \
                and not np.isnan(r.haber if r.haber is not None else np.nan):
            act = defaultdict(float)
            for k, x in imp.items():
                act[col_mon(k)] += x
            dd = act[r.mon_debe] - r.debe
            dh = act[r.mon_haber] + r.haber
            if r.mon_haber == "USDT" and -1.6 <= dh <= -1.4:
                dh = 0
            if r.mon_debe == "USDT" and -1.6 <= dd <= -1.4:
                dd = 0
            tol_d, tol_h = max(1, abs(r.debe) * 0.001), max(1, abs(r.haber) * 0.001)
            if abs(dd) > tol_d or abs(dh) > tol_h:
                tipo = "Imputación ≠ Debe/Haber"
                dif_usd = abs(b.usd(r.mon_debe, dd, r.semana_n) or 0) + abs(b.usd(r.mon_haber, dh, r.semana_n) or 0)
        if tipo:
            problemas.append(dict(semana=r.semana, semana_n=r.semana_n, fila=r.fila, operador=r.operador_g,
                                  cliente=r.cliente, tipo=tipo, dif_usd=dif_usd, signo=_sig(imp)))
    p = pd.DataFrame(problemas)
    # pares/grupos vecinos que se compensan (cliente + USDT General) no son errores reales
    p["compensado"] = False
    if not p.empty:
        for sem, g in p.groupby("semana"):
            filas = dict(zip(g.fila, g.index))
            for f, i in filas.items():
                for df_ in (1, -1, 2, -2):
                    j = filas.get(f + df_)
                    if j is not None and _compensan(p.at[i, "signo"], p.at[j, "signo"]):
                        p.loc[[i, j], "compensado"] = True
    reales = p[~p.compensado].copy()
    reales["severidad"] = np.where(reales.dif_usd >= 100, "Alta", np.where(reales.dif_usd >= 10, "Media", "Baja"))
    reales.loc[reales.tipo != "Imputación ≠ Debe/Haber", "severidad"] = "Alta"
    tot_ops = b.ops[b.ops.fin & (b.ops.semana_n < b.actual)].groupby("operador_g").size()
    t = reales.pivot_table(index="operador_g" if "operador_g" in reales else "operador", columns="severidad",
                           values="fila", aggfunc="size", fill_value=0)
    t = t.reindex(columns=["Alta", "Media", "Baja"], fill_value=0)
    t["operaciones del período"] = tot_ops
    t["Alta+Media cada 100 ops"] = (t.Alta + t.Media) / t["operaciones del período"] * 100
    t = t.sort_values("Alta+Media cada 100 ops", ascending=False).reset_index().rename(columns={"index": "operador"})
    met = dict(problemas_reales=int(len(reales)), compensados=int(p.compensado.sum()),
               por_operador={r[0]: dict(alta=int(r[1]), media=int(r[2]), baja=int(r[3]),
                                        alta_media_cada_100=round(float(r[5]), 2)) for r in t.itertuples(index=False)})
    reales = reales.drop(columns=["signo"]).sort_values(["severidad", "dif_usd"], ascending=[True, False])
    return {"11 Calidad por operador": t, "11 Filas a revisar": reales}, met


def _sig(imp):
    return {k.upper(): round(v, 2) for k, v in (imp or {}).items()}


def _compensan(a, b_):
    keys = set(a) | set(b_)
    return bool(keys) and all(abs(a.get(k, 0) + b_.get(k, 0)) < 2 for k in keys if k not in ("USDT",)) \
        and any(k in a and k in b_ for k in keys)


# ----------------------------------------------------------------------------- 12
def posicion(saldos, cfg, cz, cz_usdt):
    s = saldos.copy()
    mon = cfg["moneda_por_caja"]
    inv = set(cfg["columnas_inversiones_garantias"])
    pyg = set(cfg["columnas_pyg"])
    s["grupo"] = [("Inversiones / garantías" if c in inv else ("PyG (no es saldo)" if c in pyg else mon.get(c, "Otra")))
                  for c in s.caja]
    invg = s[s.grupo == "Inversiones / garantías"].pivot_table(index=["semana_n", "semana"], columns="caja",
                                                                values="saldo_real", aggfunc="sum", fill_value=0).reset_index()
    s = s[~s.grupo.isin(["PyG (no es saldo)", "Inversiones / garantías", "Otra"])]
    c = cfg["cotizaciones"]
    conv = {"USD": 1, "USD Exterior": c["usd_exterior_en_usd"], "EUR": c["eur_en_usd"],
            "BRL": 1 / c["brl_por_usd"], "GBP": c["gbp_en_usd"]}
    s["cot"] = s.semana_n.map(cz)
    s["par_usdt"] = s.semana_n.map(cz_usdt)
    for col in ("saldo_real", "caja_real"):
        s[col + "_usd"] = [x / k if g == "ARS" else (x * p if g == "USDT" else x * conv[g])
                           for x, g, k, p in zip(s[col], s.grupo, s.cot, s.par_usdt)]
    nat = s.pivot_table(index=["semana_n", "semana"], columns="grupo", values="saldo_real", aggfunc="sum", fill_value=0)
    usd = s.pivot_table(index=["semana_n", "semana"], columns="grupo", values="saldo_real_usd", aggfunc="sum", fill_value=0)
    caja_usd = s.pivot_table(index=["semana_n", "semana"], columns="grupo", values="caja_real_usd", aggfunc="sum", fill_value=0)
    usd["Total USD"] = usd.sum(axis=1)
    caja_usd["Total USD"] = caja_usd.sum(axis=1)
    usd["% en pesos"] = usd.get("ARS", 0) / usd["Total USD"]
    nat = nat.reset_index()
    nat["cot_ars"] = nat.semana_n.map(cz)
    nat["efecto_tipo_cambio_usd"] = nat.ARS.shift(1) * (1 / nat.cot_ars - 1 / nat.cot_ars.shift(1))
    usd = usd.reset_index()
    caja_usd = caja_usd.reset_index()
    pend_usd = usd[["semana_n", "semana", "Total USD"]].copy()
    pend_usd["caja_real_usd"] = caja_usd["Total USD"]
    pend_usd["pendientes_netos_usd"] = pend_usd["Total USD"] - pend_usd.caja_real_usd
    pend_usd = pend_usd.rename(columns={"Total USD": "saldo_real_usd"})
    ult = usd.iloc[-1]
    met = dict(semana=ult.semana, saldo_real_usd_por_moneda={k: float(ult[k]) for k in usd.columns if k not in ("semana_n", "semana")},
               ars_en_pesos=float(nat.iloc[-1].ARS), cotizacion=float(nat.iloc[-1].cot_ars),
               efecto_tipo_cambio_acumulado_usd=float(nat.efecto_tipo_cambio_usd.sum()),
               efecto_tipo_cambio_por_semana={r.semana: round(float(r.efecto_tipo_cambio_usd), 0)
                                              for r in nat.dropna(subset=["efecto_tipo_cambio_usd"]).itertuples()},
               pendientes_netos_usd_actual=float(pend_usd.iloc[-1].pendientes_netos_usd),
               nota="Saldos de apertura (Balance) de cada semana. Sin columnas de PyG ni inversiones/garantías.")
    met["inversiones_garantias_actual_moneda_original"] = {k: float(invg.iloc[-1][k]) for k in invg.columns
                                                         if k not in ("semana_n", "semana")}
    met["nota_inversiones"] = ("Columnas de inversiones/garantías en su unidad original (POLIGONO en USD; PROMAR parece estar "
                               "en pesos; confirmar unidades). No están sumadas al total en USD.")
    return {"12 Posición USD (saldo real)": usd, "12 Posición moneda original": nat, "12 Saldo vs caja real": pend_usd,
            "12 Inversiones y garantías": invg}, met


# ----------------------------------------------------------------------------- 13
def pendientes(p, b):
    if p.empty:
        return {}, {}
    p = p.copy()
    cot = b.cz[b.actual]
    mon_col = lambda c: ("USD" if c.upper() in USD_FAM or c.upper() == "USD BSAS" else b.moneda(c))
    filas = []
    for r in p.itertuples():
        tot = 0.0
        det = {}
        for k, x in (r.imputado or {}).items():
            m = mon_col(k)
            u = b.usd(m, x, b.actual) if m != "Otra" else np.nan
            det[k] = x
            if not np.isnan(u):
                tot += u
        filas.append(dict(fila=r.fila, codigo=r.codigo, detalle=r.detalle, cliente=r.cliente,
                          cliente_g=grupo_cliente(r.cliente), ope=r.ope, semana_origen_n=r.semana_origen_n,
                          semanas_abierto=r.semanas_abierto, con_signo_pregunta=r.con_signo_pregunta,
                          neto_usd=tot, imputado=", ".join(f"{k}: {v:,.2f}" for k, v in det.items()),
                          lectura=("Nos entregaron (les debemos)" if tot > 0 else "Les entregamos (nos deben)") if tot else "Sin importe"))
    d = pd.DataFrame(filas)
    g = d.groupby("cliente_g").agg(items=("fila", "size"), neto_usd=("neto_usd", "sum"),
                                   max_semanas_abierto=("semanas_abierto", "max")).reset_index().sort_values("neto_usd")
    d["antigüedad"] = pd.cut(d.semanas_abierto, [-1, 1, 4, 12, 100], labels=["0-1 sem", "2-4 sem", "5-12 sem", "+12 sem"])
    ant = d.groupby("antigüedad", observed=False).agg(items=("fila", "size"), neto_usd=("neto_usd", "sum")).reset_index()
    usdtq = d[(d.cliente == "USDT General") & d.con_signo_pregunta]
    met = dict(items=int(len(d)), nos_deben_usd=float(-d.loc[d.neto_usd < 0, "neto_usd"].sum()),
               les_debemos_usd=float(d.loc[d.neto_usd > 0, "neto_usd"].sum()), neto_usd=float(d.neto_usd.sum()),
               mayores_deudores=[dict(cliente=r.cliente_g, usd=round(-r.neto_usd)) for r in g.head(8).itertuples() if r.neto_usd < 0],
               mayores_acreedores=[dict(cliente=r.cliente_g, usd=round(r.neto_usd)) for r in g.tail(8).iloc[::-1].itertuples() if r.neto_usd > 0],
               usdt_general_signo_pregunta=dict(items=int(len(usdtq)), usd=float(usdtq.neto_usd.sum()),
                                                mas_de_4_semanas=int((usdtq.semanas_abierto >= 4).sum())),
               items_mas_de_4_semanas=int((d.semanas_abierto >= 4).sum()),
               convencion_signo="Positivo = la contraparte nos entregó valor (lo debemos). Negativo = le entregamos valor (nos debe). A confirmar con el dueño.")
    return {"13 Pendientes por cliente": g, "13 Pendientes detalle": d, "13 Pendientes antigüedad": ant}, met


# ----------------------------------------------------------------------------- 14
def fondeo(inv, b, ingresos_mensuales):
    o = b.ops[b.ops.fin & (b.ops.detalle == "Intereses")].copy()
    o["interes_usd"] = o.haber_usd
    pag = o.groupby("mes").interes_usd.sum()
    capital = float(inv.monto_usd.sum()) if not inv.empty else 0
    mensual = float(inv.interes_mensual_usd.sum()) if not inv.empty else 0
    meses = sorted(set(ingresos_mensuales) | set(pag.index))
    comp = pd.DataFrame(dict(mes=meses))
    comp["ingresos_operativos_estimados_usd"] = comp.mes.map(ingresos_mensuales).fillna(0)
    comp["intereses_pagados_registrados_usd"] = comp.mes.map(pag).fillna(0)
    comp["intereses_comprometidos_usd (hoja Inversores)"] = mensual
    comp["cobertura (ingresos / intereses comprometidos)"] = comp.ingresos_operativos_estimados_usd / mensual if mensual else np.nan
    met = dict(capital_inversores_usd=capital, interes_mensual_comprometido_usd=mensual,
               tasa_mensual_promedio=mensual / capital if capital else None,
               tasa_anual_equivalente=(1 + mensual / capital) ** 12 - 1 if capital else None,
               intereses_pagados_registrados_usd=float(pag.sum()))
    return {"14 Inversores": inv, "14 Fondeo vs ingresos": comp, "14 Intereses registrados": o[
        ["semana", "fila", "cliente", "debe", "caja_debe", "haber", "caja_haber", "interes_usd"]]}, met


# ----------------------------------------------------------------------------- 15
CATS = [("Movilidad (nafta, uber, traslados, cochera)", r"nafta|uber|traslado|cochera|peaje|remis|taxi|combustible"),
        ("Comidas y reuniones", r"reuni|havanna|chipa|almuerzo|panader|pedidos ya|cena|cafe|comida|factura|medialuna"),
        ("Limpieza", r"limpieza|marta"),
        ("Servicios e impuestos (luz, agua, expensas, internet)", r"edes|agua|simes|cimes|expensa|wi-?fi|internet|luz|gas|abl|bvc|telef"),
        ("Costos operativos / fijos", r"costo|fijo|operativ|alquiler|oficina"),
        ("Sueldos y personas", r"sueldo|dante|macre|aguinaldo")]


def gastos(b):
    g = b.ops[b.ops.fin & (b.ops.detalle == "Gastos")].copy()
    g["gasto_usd"] = np.where(g.caja_debe == "GASTOS", g.debe, g.haber_usd)
    g = g[g.gasto_usd.notna()]
    def cat(c):
        n = _norm(c)
        for nombre, pat in CATS:
            if re.search(pat, n):
                return nombre
        return "Otros"
    g["categoria"] = g.cliente.map(cat)
    g["concepto"] = g.cliente.map(lambda c: _norm(c).capitalize())
    sem = g.pivot_table(index=["semana_n", "semana"], columns="categoria", values="gasto_usd", aggfunc="sum", fill_value=0)
    sem["Total"] = sem.sum(axis=1)
    sem = sem.reset_index()
    cat_t = g.groupby("categoria").gasto_usd.agg(["size", "sum"]).rename(columns={"size": "items", "sum": "usd"}).sort_values("usd", ascending=False)
    cat_t["%"] = cat_t.usd / cat_t.usd.sum()
    conc = g.groupby("concepto").gasto_usd.agg(["size", "sum"]).rename(columns={"size": "items", "sum": "usd"}).sort_values("usd", ascending=False).head(40)
    mens = g.groupby("mes").gasto_usd.sum()
    completas = sem[sem.semana_n < b.actual]
    met = dict(gasto_total_usd=float(g.gasto_usd.sum()), gasto_semanal_promedio_usd=float(completas.Total.mean()),
               gasto_ult4_semanas_promedio_usd=float(completas.Total.tail(4).mean()),
               por_categoria={k: float(v) for k, v in cat_t.usd.items()},
               gasto_mensual_usd={m: float(x) for m, x in mens.items()},
               nota="Solo filas con Detalle = Gastos. Sueldos, alquileres o comisiones registrados con otro Detalle no están incluidos.")
    return {"15 Gastos semanales": sem, "15 Gastos por categoría": cat_t.reset_index(), "15 Gastos por concepto": conc.reset_index()}, met


# ----------------------------------------------------------------------------- resultado
def resultado_estimado(m_spread, m_circ, m_com, m_cheq, m_gastos, m_fondeo):
    meses = sorted(set(m_spread.get("ganancia_mensual_usd", {})) | set(m_circ.get("ganancia_mensual_usd", {}))
                   | set(m_com.get("comision_mensual_usd", {})))
    filas = []
    for m in meses:
        sp = m_spread.get("ganancia_mensual_usd", {}).get(m, 0)
        ci = m_circ.get("ganancia_mensual_usd", {}).get(m, 0)
        co = m_com.get("comision_mensual_usd", {}).get(m, 0)
        cq = m_cheq.get("ganancia_mensual_usd", {}).get(m, 0)
        ga = m_gastos.get("gasto_mensual_usd", {}).get(m, 0)
        it = m_fondeo.get("interes_mensual_comprometido_usd", 0)
        filas.append(dict(mes=m, spread_billete_usd=sp, circuito_usdt_usd=ci, comisiones_usd=co, cheques_usd=cq,
                          ingresos_operativos_usd=sp + ci + co + cq, gastos_usd=-ga,
                          intereses_inversores_usd=-it, resultado_estimado_usd=sp + ci + co + cq - ga - it))
    return pd.DataFrame(filas)
