"""Tablero interactivo cifrado (un solo HTML) para compartir el análisis.

Los datos van cifrados con AES-256-GCM; la clave se deriva de la contraseña con
PBKDF2-SHA256 (600.000 iteraciones). El navegador descifra localmente: el archivo
no se conecta a ningún servidor ni carga librerías externas.

Por pedido de los dueños, el tablero NO incluye estimaciones de ganancia ni de
resultado: solo datos y métricas operativas.
"""
import base64
import json
import math
import os
import secrets

import numpy as np
import pandas as pd
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERACIONES = 600_000
PLANTILLA = os.path.join(os.path.dirname(__file__), "tablero_plantilla.html")


def _v(x):
    if x is None:
        return None
    if isinstance(x, (np.floating, float)):
        return None if (math.isnan(x) or math.isinf(x)) else round(float(x), 4)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, pd.Timestamp):
        return x.strftime("%Y-%m-%d")
    if hasattr(x, "isoformat"):
        return x.isoformat()[:10]
    if isinstance(x, pd.Interval):
        return str(x)
    return x if isinstance(x, (int, str)) else str(x)


def tabla(df, columnas):
    """columnas: lista de (columna_origen, titulo, formato). formato: usd|ars|pct|pct100|num|int|txt|fecha"""
    if df is None or df.empty:
        return {"cols": [], "rows": []}
    presentes = [(c, t, f) for c, t, f in columnas if c in df.columns]
    return {"cols": [{"t": t, "f": f} for _, t, f in presentes],
            "rows": [[_v(x) for x in fila] for fila in df[[c for c, _, _ in presentes]].itertuples(index=False)]}


def construir_datos(R, b, T, M, cz, cz_usdt, fecha, notas):
    v = b.vol
    semanas = [dict(n=s.idx, nombre=s.nombre, inicio=s.inicio.isoformat(), ars=round(cz[s.idx], 2),
                    usdt=round(cz_usdt[s.idx], 4)) for s in R.semanas]
    vol_ops = v.groupby(["semana_n", "operador_g", "producto"]).agg(
        ops=("fila", "size"), debe=("debe_usd", "sum"), haber=("haber_usd", "sum")).reset_index()
    vol_cli = v.groupby(["semana_n", "cliente_g", "operador_g"]).agg(ops=("fila", "size"), usd=("prom_usd", "sum")).reset_index()
    sp = T["04 Spread diario"]
    sp = sp[sp.canal == "Pesos billete"].sort_values("fecha")
    pos = T["12 Posición USD (saldo real)"]
    monedas = [c for c in ["USD", "USDT", "ARS", "USD Exterior", "EUR", "BRL", "GBP"] if c in pos.columns]
    sc = T["12 Saldo vs caja real"]
    mch = M.get("07_cheques", {})
    d = dict(
        fecha=fecha, archivo=os.path.basename(R.wf.path) if hasattr(R.wf, "path") else "",
        semanas=semanas, actual=R.actual.idx, operadores=b.cfg["operadores_principales"] + ["Otros"],
        productos=list(v.groupby("producto").prom_usd.sum().sort_values(ascending=False).index),
        volOps=[[int(r.semana_n), r.operador_g, r.producto, int(r.ops), _v(r.debe), _v(r.haber)] for r in vol_ops.itertuples()],
        volCli=[[int(r.semana_n), r.cliente_g, r.operador_g, int(r.ops), _v(r.usd)] for r in vol_cli.itertuples()],
        altas=tabla(T["02 Altas y bajas (mes)"], [("mes", "Mes", "txt"), ("clientes_activos", "Clientes activos", "int"),
                                                 ("nuevos", "Nuevos", "int"), ("recurrentes", "Recurrentes", "int"),
                                                 ("volumen_usd", "Volumen USD", "usd"), ("% volumen de nuevos", "% volumen de nuevos", "pct")]),
        perdidos=tabla(T["02 Clientes perdidos"], [("cliente", "Cliente", "txt"), ("operaciones", "Operaciones", "int"),
                                                   ("volumen_usd", "Volumen histórico USD", "usd"), ("ultima_semana", "Última semana", "int"),
                                                   ("ultima_fecha", "Última operación", "fecha")]),
        spreadDiario=[[_v(r.fecha), _v(r.cot_compra), _v(r.cot_venta), _v(r.usd_compra), _v(r.usd_venta)] for r in sp.itertuples()],
        spreadMensual=tabla(T["04 Spread mensual"], [("mes", "Mes", "txt"), ("canal", "Canal", "txt"),
                                                      ("usd_compra", "USD comprados", "usd"), ("usd_venta", "USD vendidos", "usd")]),
        spreadMes=_spread_mes(T["04 Spread diario"]),
        spreadOp=tabla(T["04 Spread por operador"], [("operador_g", "Operador", "txt"), ("lado", "Lado", "txt"),
                                                      ("usd", "USD", "usd"), ("cot_media", "Cotización media", "num")]),
        comisiones=tabla(T["06 Comisiones por tipo"], [("tipo", "Tipo", "txt"), ("operaciones", "Operaciones", "int"),
                                                        ("volumen_usd", "Volumen USD", "usd"),
                                                        ("pct_pactado_mediano", "% pactado (mediana)", "pct100"),
                                                        ("% efectivo", "% efectivo", "pct")]),
        circuito=tabla(T["05 Circuito mensual"], [("mes", "Mes", "txt"), ("operaciones", "Operaciones", "int"),
                                                   ("usd", "USD operados", "usd"), ("margen_%", "Margen medio", "pct")]),
        posicion=dict(semanas=[r for r in pos.semana], monedas=monedas,
                      valores={m: [_v(x) for x in pos[m]] for m in monedas},
                      total=[_v(x) for x in pos["Total USD"]], caja_real=[_v(x) for x in sc.caja_real_usd],
                      pendientes=[_v(x) for x in sc.pendientes_netos_usd]),
        invGar=tabla(T["12 Inversiones y garantías"], [("semana", "Semana", "txt")] +
                     [(c, c.title(), "num") for c in T["12 Inversiones y garantías"].columns if c not in ("semana_n", "semana")]),
        pendCli=tabla(T["13 Pendientes por cliente"], [("cliente_g", "Cliente", "txt"), ("items", "Ítems", "int"),
                                                        ("neto_usd", "Neto USD (+ les debemos / − nos deben)", "usd"),
                                                        ("max_semanas_abierto", "Máx. semanas abierto", "int")]),
        pendAnt=tabla(T["13 Pendientes antigüedad"], [("antigüedad", "Antigüedad", "txt"), ("items", "Ítems", "int"),
                                                       ("neto_usd", "Neto USD", "usd")]),
        pendDet=tabla(T["13 Pendientes detalle"], [("fila", "Fila", "int"), ("cliente", "Cliente", "txt"), ("detalle", "Detalle", "txt"),
                                                    ("semanas_abierto", "Semanas abierto", "int"),
                                                    ("con_signo_pregunta", "Con ?", "txt"), ("neto_usd", "Neto USD", "usd"),
                                                    ("imputado", "Imputado", "txt")]),
        pendKpi={k: _v(M["13_pendientes"].get(k)) for k in ("items", "nos_deben_usd", "les_debemos_usd", "neto_usd", "items_mas_de_4_semanas")},
        usdtQ=M["13_pendientes"].get("usdt_general_signo_pregunta", {}),
        chequesTit=tabla(T.get("07 Cheques por titular"), [("titular", "Titular", "txt"), ("cheques", "Cheques", "int"),
                                                           ("monto", "Monto ARS", "ars"), ("% del total", "% del total", "pct"),
                                                           ("en_cartera", "En cartera ARS", "ars")]),
        chequesVenc=tabla(T.get("07 Cheques vencimientos"), [("mes_venc", "Mes de vencimiento", "txt"), ("vencido", "Vencido", "txt"),
                                                             ("monto", "Monto ARS", "ars")]),
        chequesKpi={k: _v(mch.get(k)) for k in ("cheques_listados", "monto_total_ars", "en_cartera_ars", "en_cartera_vencidos_ars",
                                                "tasa_mensual_mediana", "dias_mediano", "top3_titulares_pct")},
        inversores=tabla(T.get("14 Inversores"), [("inversor", "Inversor", "txt"), ("plazo", "Plazo", "txt"),
                                                  ("destino", "Destino", "txt"), ("monto_usd", "Monto USD", "usd"),
                                                  ("tasa_mensual_pct", "Tasa mensual", "pct100"),
                                                  ("interes_mensual_usd", "Interés mensual USD", "usd"), ("retiro", "Retiro", "txt"),
                                                  ("detalle", "Detalle", "txt")]),
        dias=tabla(T["09 Día de la semana"], [("dia", "Día", "txt"), ("operaciones promedio por día", "Operaciones por día", "num"),
                                               ("volumen promedio por día_usd", "Volumen por día USD", "usd"),
                                               ("días con actividad", "Días con actividad", "int")]),
        tamano=tabla(T["10 Tamaño ops"], [("tramo", "Tramo USD", "txt"), ("operaciones", "Operaciones", "int"),
                                          ("% operaciones", "% operaciones", "pct"), ("volumen_usd", "Volumen USD", "usd"),
                                          ("% volumen", "% volumen", "pct")]),
        ticket=tabla(T["10 Ticket por operador"], [("operador_g", "Operador", "txt"), ("operaciones", "Operaciones", "int"),
                                                   ("ticket promedio", "Ticket promedio USD", "usd"), ("mediana", "Mediana USD", "usd"),
                                                   ("percentil 90", "Percentil 90 USD", "usd"), ("máxima", "Máxima USD", "usd")]),
        grandes=tabla(T["10 Operaciones más grandes"], [("semana", "Semana", "txt"), ("fila", "Fila", "int"), ("operador", "Operador", "txt"),
                                                        ("cliente", "Cliente", "txt"), ("debe", "Debe", "num"), ("caja_debe", "Caja", "txt"),
                                                        ("haber", "Haber", "num"), ("caja_haber", "Caja", "txt"), ("prom_usd", "USD", "usd")]),
        calidad=tabla(T["11 Calidad por operador"], [("operador_g", "Operador", "txt"), ("operador", "Operador", "txt"), ("Alta", "Alta", "int"), ("Media", "Media", "int"),
                                                     ("Baja", "Baja", "int"), ("operaciones del período", "Operaciones", "int"),
                                                     ("Alta+Media cada 100 ops", "Alta+Media cada 100 ops", "num")]),
        revisar=tabla(T["11 Filas a revisar"].head(150), [("severidad", "Severidad", "txt"), ("semana", "Semana", "txt"), ("fila", "Fila", "int"),
                                                         ("operador", "Operador", "txt"), ("cliente", "Cliente", "txt"),
                                                         ("tipo", "Tipo", "txt"), ("dif_usd", "Diferencia ≈ USD", "usd")]),
        gastosSem=_gastos_sem(T["15 Gastos semanales"]),
        gastosCat=tabla(T["15 Gastos por categoría"], [("categoria", "Categoría", "txt"), ("items", "Ítems", "int"),
                                                       ("usd", "USD", "usd"), ("%", "%", "pct")]),
        gastosConc=tabla(T["15 Gastos por concepto"], [("concepto", "Concepto", "txt"), ("items", "Ítems", "int"), ("usd", "USD", "usd")]),
        notas=notas,
        cotizaciones=dict(eur=b.cfg["cotizaciones"]["eur_en_usd"], brl=b.cfg["cotizaciones"]["brl_por_usd"],
                          ars_unica=b.cfg["cotizaciones"].get("ars_unica")),
    )
    return d


def _spread_mes(diario):
    d = diario.copy()
    d["mes"] = pd.to_datetime(d.fecha).dt.to_period("M").astype(str)
    g = d.groupby(["mes", "canal"]).agg(compra=("cot_compra", "median"), venta=("cot_venta", "median"),
                                        spread=("spread_pesos", "median"), spread_pct=("spread_%", "median")).reset_index()
    return tabla(g, [("mes", "Mes", "txt"), ("canal", "Canal", "txt"), ("compra", "Cotiz. compra (mediana)", "num"),
                     ("venta", "Cotiz. venta (mediana)", "num"), ("spread", "Spread $ (mediana)", "num"),
                     ("spread_pct", "Spread % (mediana)", "pct")])


def _gastos_sem(df):
    cats = [c for c in df.columns if c not in ("semana_n", "semana", "Total")]
    return dict(semanas=list(df.semana), categorias=cats, valores={c: [_v(x) for x in df[c]] for c in cats})


def cifrar(datos, clave):
    sal, iv = secrets.token_bytes(16), secrets.token_bytes(12)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=sal, iterations=ITERACIONES)
    llave = kdf.derive(clave.encode("utf-8"))
    texto = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ct = AESGCM(llave).encrypt(iv, texto, None)
    return dict(v=1, it=ITERACIONES, s=base64.b64encode(sal).decode(), iv=base64.b64encode(iv).decode(),
                ct=base64.b64encode(ct).decode())


def generar(datos, clave, ruta):
    paquete = cifrar(datos, clave)
    html = open(PLANTILLA, encoding="utf-8").read()
    html = html.replace("/*__PAQUETE__*/null", json.dumps(paquete))
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    return ruta


def clave_aleatoria():
    alf = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "-".join("".join(secrets.choice(alf) for _ in range(4)) for _ in range(4))
