"""Lectura del Registro General (Excel exportado de Google Sheets).

Convierte las hojas semanales y auxiliares en tablas planas (pandas) que usan
los análisis. No modifica el archivo original.
"""
import datetime as dt
import re
import statistics
import warnings
from collections import defaultdict

import openpyxl
import pandas as pd
from openpyxl.utils import column_index_from_string as col_idx

warnings.filterwarnings("ignore")

ARITH = re.compile(r"^=[0-9+\-*/. ()]+$")
SUMR = re.compile(r"^=SUM\(([A-Z]+)(\d+):([A-Z]+)(\d+)\)$")
SEMANA = re.compile(r"^(\d{2})(\d{2}) - (\d{2})(\d{2})")


def _low(x):
    return x.strip().lower() if isinstance(x, str) else ""


def _num(x):
    return float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else None


class Semana:
    """Una hoja semanal: encabezados, valores (evaluando fórmulas simples) y bloques."""

    def __init__(self, nombre, ws_f, ws_v, anio, idx):
        self.nombre, self.f, self.v, self.idx = nombre, ws_f, ws_v, idx
        fin = [r for r in range(1, 8) if self.f.cell(r, 1).value == "Fin"][0]
        self.fila_hdr, self.d0 = fin - 1, fin + 1
        self.hdr = {}
        for c in range(18, self.f.max_column + 1):
            h = self.f.cell(self.fila_hdr, c).value
            if h == "Data":
                break
            if h and str(h).strip() not in ("1.0", "1"):
                self.hdr[c] = str(h).strip()
        self.col = {v.upper(): k for k, v in self.hdr.items()}
        self.maxr = self.f.max_row
        self._cache = {}
        m = SEMANA.match(nombre)
        self.inicio = dt.date(anio, int(m.group(2)), int(m.group(1)))
        fin_d = dt.date(anio, int(m.group(4)), int(m.group(3)))
        if fin_d < self.inicio:
            fin_d = dt.date(anio + 1, fin_d.month, fin_d.day)
        self.fin = fin_d

    # -- valores ---------------------------------------------------------
    def raw(self, r, c):
        return self.f.cell(r, c).value

    def val(self, r, c):
        k = (r, c)
        if k in self._cache:
            return self._cache[k]
        fv = self.f.cell(r, c).value
        out = _num(fv)
        if isinstance(fv, str) and fv.startswith("="):
            g = fv.replace("\n", "").replace(" ", "")
            if ARITH.match(g):
                try:
                    out = float(eval(g[1:]))  # solo dígitos y operadores (validado por regex)
                except Exception:
                    out = None
            else:
                m = SUMR.match(g)
                if m and m.group(1) == m.group(3):
                    cc = col_idx(m.group(1))
                    out = sum(self.val(rr, cc) or 0 for rr in range(int(m.group(2)), int(m.group(4)) + 1))
            if out is None:
                out = _num(self.v.cell(r, c).value)
        self._cache[k] = out
        return out

    def etiqueta(self, r, c):
        v = self.raw(r, c)
        if isinstance(v, str) and v.startswith("="):
            v = self.v.cell(r, c).value
        return v.strip() if isinstance(v, str) else v

    def imputaciones(self, r):
        d = {}
        for c, h in self.hdr.items():
            x = self.val(r, c)
            if x and abs(x) > 1e-6:
                d[h] = d.get(h, 0) + x
        return d

    def filas(self, F=None):
        return [r for r in range(self.d0, self.maxr + 1) if F is None or self.raw(r, 6) == F]

    # -- estructura ------------------------------------------------------
    def estructura(self):
        cier = self.filas("Cierre")
        primero = cier[0]
        bal = self.filas("Balance")
        aps = [r for r in bal if _low(self.raw(r, 7)).startswith("apertura") and r > primero]
        if aps:
            ini_pend = aps[-1]
            ult_ops = max(r for r in cier if r < ini_pend)
        elif self.raw(5, 7) == "Cambio General" and len(cier) > 1:
            # formato actual sin rótulo de Apertura abajo: los pendientes arrancan tras el anteúltimo Cierre
            ini_pend = cier[-2]
            ult_ops = ini_pend
        else:
            # formato viejo sin bloque de pendientes abajo
            ini_pend = self.maxr + 1
            ult_ops = cier[-1]
        fin_cierre = cier[-1]
        fin_pend = fin_cierre if (ini_pend and fin_cierre > ini_pend) else self.maxr + 1
        bal_antes = [r for r in bal if r < primero]
        ini_ops = (max(bal_antes) if bal_antes else self.d0 - 1) + 1
        formato_actual = self.raw(5, 7) == "Cambio General"
        return dict(cierres=cier, primer_cierre=primero, ini_ops=ini_ops, ini_pend=ini_pend,
                    ult_cierre_ops=ult_ops, fin_pend=fin_pend, cierre_final=fin_cierre,
                    formato_actual=formato_actual)


class Registro:
    def __init__(self, ruta, cfg):
        self.cfg = cfg
        self.wf = openpyxl.load_workbook(ruta)
        self.wv = openpyxl.load_workbook(ruta, data_only=True)
        nombres = [ws.title for ws in self.wf.worksheets if SEMANA.match(ws.title)]
        self.semanas = [Semana(n, self.wf[n], self.wv[n], cfg["anio"], i)
                        for i, n in enumerate(nombres, 1)]
        self.actual = self.semanas[-1]

    # ------------------------------------------------------------------
    def operaciones(self):
        """Operaciones finalizadas de cada semana (sin bloques de pendientes)."""
        out = []
        for s in self.semanas:
            e = s.estructura()
            fin = s.maxr + 1 if s is self.actual else e["ini_pend"]
            fechas = self._fechas_cierres(s, e)
            for r in range(e["ini_ops"], fin):
                G, F = s.raw(r, 7), s.raw(r, 6)
                if not G or F in ("Cierre", "Balance"):
                    continue
                d = s.raw(r, 4)
                es_op = (isinstance(d, str) and d.startswith("=")) or (isinstance(d, (int, float)) and r > e["primer_cierre"])
                if not es_op:
                    continue
                fin_, pen, can = s.raw(r, 1) is True, s.raw(r, 2) is True, s.raw(r, 3) is True
                op = s.etiqueta(r, 8)
                op = {"coco": "Coco"}.get(op, op) or "Sin operador"
                imp = s.imputaciones(r)
                out.append(dict(
                    semana_n=s.idx, semana=s.nombre, fila=r, ope=_num(s.v.cell(r, 4).value),
                    fecha=self._fecha_fila(r, fechas, s), fin=fin_, pen=pen, can=can,
                    detalle=F or "", cliente=str(G).strip(), operador=op,
                    debe=s.val(r, 9) if s.val(r, 9) is not None else _num(s.v.cell(r, 9).value),
                    caja_debe=(s.etiqueta(r, 10) or "").upper() or None,
                    cotizacion=_num(s.v.cell(r, 11).value),
                    haber=s.val(r, 12) if s.val(r, 12) is not None else _num(s.v.cell(r, 12).value),
                    caja_haber=(s.etiqueta(r, 13) or "").upper() or None,
                    imputado=imp,
                ))
        df = pd.DataFrame(out)
        df["fecha"] = pd.to_datetime(df["fecha"])
        return df

    @staticmethod
    def _fechas_cierres(s, e):
        """Fecha de cada Cierre diario: la escrita en la columna Q si cae dentro de la
        semana; si no, se infiere por orden (día siguiente al cierre anterior)."""
        res, prev = {}, None
        diarios = [r for r in e["cierres"] if r > e["ini_ops"] and (e["ini_pend"] is None or r <= e["ini_pend"])]
        for i, r in enumerate(diarios):
            q = s.v.cell(r, 17).value
            if isinstance(q, dt.datetime) and s.inicio <= q.date() <= s.fin and (prev is None or q.date() >= prev):
                d = q.date()
            elif prev is None:
                d = s.inicio
            else:
                d = min(prev + dt.timedelta(days=1), s.fin)
            res[r] = d
            prev = d
        return res

    def paridad_usdt(self, ops, ars):
        """USD billete por cada USDT, por semana: cotización en pesos del USDT (filas USDT General)
        dividida la cotización del USD billete. Si config fija un valor, se usa ese."""
        fijo = self.cfg["cotizaciones"].get("usdt_en_usd")
        lo, hi = self.cfg["rango_cotizacion_ars"]
        u = ops[ops.fin & (ops.cliente == "USDT General") & ops.cotizacion.between(lo, hi)]
        u = u[[{a, b} == {"TRANSFER", "USDT"} for a, b in zip(u.caja_debe, u.caja_haber)]]
        med = u.groupby("semana_n").cotizacion.median()
        res = {}
        for s in self.semanas:
            if fijo:
                res[s.idx] = float(fijo)
            elif s.idx in med.index:
                res[s.idx] = float(med[s.idx] / ars[s.idx])
            else:
                res[s.idx] = res.get(s.idx - 1, 1.0)
        return res

    @staticmethod
    def _fecha_fila(r, fechas, s):
        sig = [c for c in fechas if c > r]
        if sig:
            return fechas[min(sig)]
        return (max(fechas.values()) + dt.timedelta(days=1)) if fechas else s.inicio

    # ------------------------------------------------------------------
    def saldos_semanales(self):
        """Saldo real (Balance) y caja real (Balance + Apertura Pendientes) al inicio
        de cada semana con el formato actual, por caja."""
        out = []
        for s in self.semanas:
            if not s.estructura()["formato_actual"]:
                continue
            for c, h in s.hdr.items():
                b = s.val(5, c) or 0
                a = s.val(6, c) or 0
                out.append(dict(semana_n=s.idx, semana=s.nombre, inicio=pd.Timestamp(s.inicio),
                                caja=h.upper(), saldo_real=b, apertura_pend=a, caja_real=b + a))
        return pd.DataFrame(out)

    def pendientes_actuales(self, ops):
        """Bloque de pendientes de arriba de la semana actual, con antigüedad por N° de Ope."""
        s = self.actual
        e = s.estructura()
        cp = [r for r in s.filas("Balance") if "cierre" in _low(s.raw(r, 7)) and r < e["primer_cierre"]]
        fin = cp[0] if cp else e["primer_cierre"]
        con_ope = ops[ops.ope.notna()].sort_values("semana_n")
        sem_por_ope = dict(zip(con_ope.ope.astype(int)[::-1], con_ope.semana_n[::-1]))  # primera aparición
        out = []
        for r in range(7, fin):
            G, F = s.raw(r, 7), s.raw(r, 6)
            if not G or F in ("Cierre", "Balance"):
                continue
            ope = _num(s.v.cell(r, 4).value)
            sn = sem_por_ope.get(int(ope)) if ope else None
            imp = s.imputaciones(r)
            out.append(dict(fila=r, codigo=s.raw(r, 5), detalle=F, cliente=str(G).strip(), ope=ope,
                            semana_origen_n=sn,
                            semanas_abierto=(s.idx - sn) if sn else None,
                            con_signo_pregunta=any(str(s.v.cell(r, c).value).strip() == "?" for c in (9, 11)),
                            debe=_num(s.v.cell(r, 9).value), caja_debe=s.etiqueta(r, 10),
                            haber=_num(s.v.cell(r, 12).value), caja_haber=s.etiqueta(r, 13),
                            imputado=imp))
        return pd.DataFrame(out)

    # ------------------------------------------------------------------
    def cheques(self):
        """Cartera de cheques de las hojas CQ, Donato - Poligono y CQ - Hipoteca."""
        out = []
        for hoja in ("CQ", "Donato - Poligono"):
            if hoja not in self.wv.sheetnames:
                continue
            ws = self.wv[hoja]
            hdr_r = [r for r in range(1, 12) if ws.cell(r, 1).value == "COBRADO"][0]
            for r in range(hdr_r + 1, ws.max_row + 1):
                monto = _num(ws.cell(r, 6).value)
                if not monto or not isinstance(ws.cell(r, 5).value, dt.datetime):
                    continue
                out.append(dict(hoja=hoja, cobrado=ws.cell(r, 1).value is True, colocado=ws.cell(r, 2).value is True,
                                fecha=ws.cell(r, 4).value, vencimiento=ws.cell(r, 5).value, monto=monto,
                                titular=str(ws.cell(r, 7).value or "").strip().upper(), cliente=ws.cell(r, 8).value,
                                dias=_num(ws.cell(r, 10).value), tasa_mensual=_num(ws.cell(r, 11).value),
                                comision=_num(ws.cell(r, 14).value), pagado=_num(ws.cell(r, 15).value),
                                destino=ws.cell(r, 16).value))
        df = pd.DataFrame(out)
        if not df.empty:
            # los mismos cheques aparecen en CQ y en Donato - Poligono: queda la primera aparición (CQ)
            df = df.drop_duplicates(subset=["titular", "monto", "vencimiento"], keep="first")
            # la columna Comisión solo es comisión cuando la fila tiene tasa y el valor es razonable
            ok = df.tasa_mensual.notna() & df.comision.notna() & (df.comision <= df.monto * 0.6)
            df.loc[~ok, "comision"] = None
        resumen = {}
        if "CQ" in self.wv.sheetnames:
            ws = self.wv["CQ"]
            celdas = {"total_cheques": "C2", "total_entregado": "C3", "total_comision": "C4", "total_recibido": "H2",
                      "ganancia_recibida": "H3", "total_a_cobrar": "M2", "ganancia_a_cobrar": "M3",
                      "comisiones_pagadas": "T2"}
            for k, c in celdas.items():
                resumen[k] = _num(ws[c].value)
        return df, resumen

    def inversores(self):
        if "Inversores" not in self.wv.sheetnames:
            return pd.DataFrame()
        ws = self.wv["Inversores"]
        out = []
        for r in range(3, 13):
            inv = ws.cell(r, 5).value
            if not inv:
                continue
            out.append(dict(plazo=ws.cell(r, 2).value, destino=ws.cell(r, 4).value, inversor=inv,
                            monto_usd=_num(ws.cell(r, 6).value), detalle=ws.cell(r, 7).value,
                            retiro=ws.cell(r, 8).value, tasa_mensual_pct=_num(ws.cell(r, 9).value),
                            interes_mensual_usd=_num(ws.cell(r, 10).value)))
        return pd.DataFrame(out)

    # ------------------------------------------------------------------
    def cotizaciones(self, ops):
        """Pesos por USD para cada semana (config o mediana observada)."""
        cz = self.cfg["cotizaciones"]
        lo, hi = self.cfg["rango_cotizacion_ars"]
        mon = self.cfg["moneda_por_caja"]
        obs = defaultdict(list)
        sub = ops[(ops.detalle == "Cajas") & ops.cotizacion.between(lo, hi)]
        for _, x in sub.iterrows():
            m = {mon.get(x.caja_debe or ""), mon.get(x.caja_haber or "")}
            if m == {"USD", "ARS"}:
                obs[x.semana_n].append(x.cotizacion)
        res = {}
        for s in self.semanas:
            if cz.get("ars_unica"):
                res[s.idx] = float(cz["ars_unica"])
            elif str(s.idx) in cz.get("ars_por_semana", {}):
                res[s.idx] = float(cz["ars_por_semana"][str(s.idx)])
            elif obs.get(s.idx):
                res[s.idx] = float(statistics.median(obs[s.idx]))
            else:
                res[s.idx] = res.get(s.idx - 1, 1500.0)
        return res
