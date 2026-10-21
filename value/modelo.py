"""Modelo del tablero Value · Cambio General: de las hojas leídas (value/leer.py) al contrato de datos del tablero.

Las definiciones están en analisis/SPEC.md (sección 3). Resumen:
- var  = neto(t) − neto(t−1)
- ret  = retiros de socios: columna DIVIDENDOS (lo que resta Egresos) + config.value.retiros
- aj   = ajustes a mano: variación de los renglones fijos del bloque (USDT General, Deuda)
- gan  = var + ret − aj   (ganancia de la semana, "sin ajustes")
- gas  = egresos del negocio (gastos, comisiones, intereses sin los retiros reclasificados, inversión)
- antes de gastos = gan + gas
"""
import datetime as dt
import itertools
import re
import statistics
from collections import defaultdict

from openpyxl.utils import get_column_letter

GRUPOS_PATRIMONIO = ["proyectos", "pesos", "billete", "cripto", "exterior", "usdt_general", "deuda", "otros"]
DISPONIBLE = ("pesos", "billete", "cripto", "exterior", "otros")
FIJOS = ("usdt_general", "deuda")
TIPOS_EGRESO = ("gastos", "comisiones", "intereses", "inversion", "otros")
MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre",
         "noviembre", "diciembre")


def r2(x):
    return None if x is None else round(float(x), 2)


def norm(nombre):
    """Encabezado normalizado: mayúsculas, espacios simples; los números como enteros ('1.0' → '1')."""
    if nombre is None:
        return None
    if isinstance(nombre, (int, float)):
        nombre = str(int(nombre)) if float(nombre).is_integer() else str(nombre)
    t = re.sub(r"\s+", " ", str(nombre)).strip().upper()
    if re.fullmatch(r"\d+(\.0+)?", t):
        t = str(int(float(t)))
    return t or None


def jueves(ini, dias):
    """Jueves que define el mes de la hoja (el de la última semana si la hoja abarca más de una)."""
    return ini + dt.timedelta(days=dias - 4)


def jueves_del_mes(anio, mes):
    d = dt.date(anio, mes, 1)
    out = []
    while d.month == mes:
        if d.weekday() == 3:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def fmt_usd(x):
    s = f"{abs(x):,.0f}".replace(",", ".")
    return ("−" if x < 0 else "") + s


def fmt_dm(d):
    return d.strftime("%d/%m")


def rango_txt(ini, fin):
    m = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic")
    if ini.month == fin.month:
        return f"{ini.day}–{fin.day} {m[fin.month - 1]}"
    return f"{ini.day} {m[ini.month - 1]}–{fin.day} {m[fin.month - 1]}"


class Modelo:
    def __init__(self, hojas, archivos, cfg, tenencia=None, signo_pendientes_confirmado=False, moneda_por_caja=None):
        self.hojas, self.archivos, self.cfg = hojas, archivos, cfg
        # moneda de cada caja cuando la hoja no tiene fila de monedas (config.json → moneda_por_caja)
        abrev = {"USD": "USD", "USD EXTERIOR": "USD", "USDT": "USDT", "ARS": "ARS", "EUR": "EUR", "BRL": "REAL", "GBP": "GBP"}
        self.moneda_de = {norm(k): abrev.get(norm(v), v) for k, v in (moneda_por_caja or {}).items()}
        self.tenencia = tenencia
        self.signo_ok = signo_pendientes_confirmado
        self.grupo_de = {}
        for g, nombres in cfg["grupos"].items():
            for n in nombres:
                self.grupo_de[norm(n)] = g
        self.alias = {norm(k): norm(v) for k, v in cfg.get("alias", {}).items()}
        self.tipo_egreso = {norm(k): v for k, v in cfg.get("tipo_egreso", {}).items()}
        self.fijos = {norm(k): v for k, v in cfg.get("renglones_fijos", {}).items()}
        self.chequeos = []
        self.semanas = []

    # ------------------------------------------------------------------------------------------- cajas por hoja
    def _cajas(self, h, prev_nombres):
        """Nombre normalizado, grupo y heredados para cada columna de la hoja."""
        cols = {}
        for c in h["cajas"]:
            n = norm(c["nombre"])
            n = self.alias.get(n, n)
            heredado = False
            if n is None:
                n = prev_nombres.get(c["col"])
                heredado = n is not None
                if n is None:
                    n = f"SIN NOMBRE ({c['col']})"
            g = self.grupo_de.get(n, "otros")
            moneda = c["moneda"] or self.moneda_de.get(n) or {"pesos": "ARS", "billete": "USD", "cripto": "USD", "proyectos": "USD",
                                                              "flujos": "USD"}.get(g)
            # un euro que la fórmula del Neto suma 1 a 1 se muestra como USD (así lo cuenta esa hoja)
            coef = h["coef_neto"].get(c["col"] + "2")
            eur_1a1 = moneda == "EUR" and coef is not None and abs(coef - 1) < 1e-9
            if eur_1a1:
                moneda = "USD"
            cols[c["col"]] = dict(c, n=n, g=g, heredado=heredado, moneda=moneda, eur_1a1=eur_1a1, coef=coef)
        return cols

    # ------------------------------------------------------------------------------------------- semanas
    def armar(self):
        cfg = self.cfg
        retiros_cfg = defaultdict(list)
        for r in cfg.get("retiros", []):
            retiros_cfg[r["semana"]].append(r)
        a_revisar = cfg.get("semanas_a_revisar", {})
        prev = None
        prev_nombres = {}
        prev_cajas_usd = {}
        prev_coef = {}
        prev_eur, prev_eur_tot = None, 0.0
        for h in self.hojas:
            cols = self._cajas(h, prev_nombres)
            b = h["bloque"]
            neto = b["Neto"].get("calculado")
            bruto = b.get("Bruto", {}).get("calculado")
            egr_planilla = -(b.get("Egresos", {}).get("calculado") or 0.0)
            sid = h["inicio"].isoformat()

            # aportes al Neto por grupo, separando saldo (fila 2) y pendientes (fila 3)
            grupos = defaultdict(float)
            pend = defaultdict(float)
            caja_usd = defaultdict(float)
            for celda, usd in h["aportes_neto"].items():
                col, fila = re.match(r"([A-Z]+)(\d+)", celda).groups()
                info = cols.get(col)
                g = info["g"] if info else "otros"
                grupos[g] += usd
                if int(fila) == 3:
                    pend[g] += usd
                nombre = info["n"] if info else f"SIN NOMBRE ({col})"
                caja_usd[nombre] += usd
            fijos_val = {}
            for et, val in h["constantes"].items():
                g = self.fijos.get(norm(et), "otros")
                grupos[g] += val
                fijos_val[norm(et)] = val
            # garantías y flujos netean 0 en el Neto: lo que quede (si queda) va a "otros"
            for g in ("garantias", "flujos"):
                if abs(grupos.get(g, 0.0)) > 0.005:
                    grupos["otros"] += grupos[g]
                    pend["otros"] += pend.get(g, 0.0)
                grupos.pop(g, None)
                pend.pop(g, None)
            suma_grupos = sum(grupos.values())

            # egresos por tipo (lo que resta el renglón Egresos de cada columna)
            egr = defaultdict(float)
            for celda, v in h["egresos_por_celda"].items():
                col = re.match(r"([A-Z]+)", celda).group(1)
                info = cols.get(col)
                tipo = self.tipo_egreso.get(info["n"] if info else None, "otros")
                egr[tipo] += v
            ret_col = egr.pop("retiros", 0.0)
            ingresos = -egr.pop("ingresos", 0.0)   # alquileres: la planilla los resta en Egresos con signo
            ret_det = []
            if ret_col > 0.005:
                ret_det.append({"monto": r2(ret_col), "detalle": "Columna DIVIDENDOS de la hoja", "confirmado": True})
            ret_cfg = 0.0
            for r in retiros_cfg.get(sid, []):
                dentro = norm(r.get("dentro_de"))
                if dentro:
                    tipo = self.tipo_egreso.get(dentro, "otros")
                    egr[tipo] -= r["monto"]
                ret_cfg += r["monto"]
                ret_det.append({"monto": r2(r["monto"]), "detalle": r["detalle"], "confirmado": bool(r.get("confirmado"))})
            ret = ret_col + ret_cfg
            gas = sum(egr.get(t, 0.0) for t in TIPOS_EGRESO) - ingresos

            # ajustes a mano: variación de los renglones fijos
            aj_det = []
            if prev is not None:
                for k in sorted(set(fijos_val) | set(prev["_fijos"])):
                    d = fijos_val.get(k, 0.0) - prev["_fijos"].get(k, 0.0)
                    if abs(d) > 0.005:
                        aj_det.append({"renglon": k, "grupo": self.fijos.get(k, "otros"), "monto": r2(d)})
            aj = sum(a["monto"] for a in aj_det)

            var = None if prev is None else neto - prev["neto"]
            gan = None if var is None else var + ret - aj
            sem = h["dias"] / 7
            cot = h["cotizacion"]
            ars = grupos.get("pesos", 0.0) * cot if cot else None
            efecto = None
            if prev is not None and cot and prev["cot"] and prev["ars"] is not None:
                efecto = prev["ars"] * (1 / cot - 1 / prev["cot"])
            sens10 = (ars / cot - ars / (cot + 10)) if ars is not None and cot else None
            vol = None
            for et in ("Volumen Prom", "Promedio"):
                if et in b and b[et]["guardado"] is not None:
                    vol = b[et]["guardado"]
                    break
            gp = b.get("Ganancia Neta", {})
            g_otra = b.get("Ganancia") if not gp else None

            # cajas para el detalle
            lista = []
            en_neto = {re.match(r"([A-Z]+)", x).group(1) for x in h["aportes_neto"]}
            for col, c in cols.items():
                n = c["n"]
                usd = caja_usd.get(n, 0.0) if col in en_neto and (c["con_suma"] or c["g"] == "flujos") else None
                lista.append({
                    "n": n, "col": col, "g": c["g"], "mon": c["moneda"], "s": r2(c["saldo"]), "p": r2(c["pendiente"]),
                    "t": r2(c["total"]), "usd": r2(usd) if usd is not None else None,
                    "usd_prev": None if prev is None else r2(prev_cajas_usd.get(n, 0.0)),
                    "suma": usd is not None, "heredado": c["heredado"], "eur_1a1": c["eur_1a1"],
                })

            s = {
                "id": sid, "hoja": h["hoja"], "origen": h["origen"], "ini": h["inicio"].isoformat(),
                "fin": h["fin"].isoformat(), "txt": rango_txt(h["inicio"], h["fin"]) + (" (2 sem.)" if h["dias"] == 14 else ""),
                "dias": h["dias"], "mes": jueves(h["inicio"], h["dias"]).strftime("%Y-%m"),
                "cot": cot, "eur": h["eur_usd"], "neto": r2(neto), "bruto": r2(bruto), "egr_planilla": r2(egr_planilla),
                "neto_guardado": r2(b["Neto"].get("guardado")), "var": r2(var), "ret": r2(ret), "ret_det": ret_det,
                "aj": r2(aj), "aj_det": aj_det, "gan": r2(gan), "gan_con": r2(None if var is None else var + ret),
                "gas": r2(gas), "gas_det": {t: r2(egr.get(t, 0.0)) for t in TIPOS_EGRESO}, "ingresos": r2(ingresos),
                "antes": r2(None if gan is None else gan + gas),
                "antes_con": r2(None if var is None else var + ret + gas),
                "gan_planilla": r2(gp.get("guardado")), "gan_planilla_error": gp.get("error_guardado"),
                "gan_bruta_planilla": r2(b.get("Ganancia Bruta", {}).get("guardado")),
                "grupos": {g: r2(grupos.get(g, 0.0)) for g in GRUPOS_PATRIMONIO},
                "pend": {g: r2(pend.get(g, 0.0)) for g in GRUPOS_PATRIMONIO},
                "disponible": r2(sum(grupos.get(g, 0.0) for g in DISPONIBLE)),
                "fijos": r2(sum(grupos.get(g, 0.0) for g in FIJOS)),
                "ars": r2(ars), "efecto": r2(efecto), "sens10": r2(sens10), "volumen": r2(vol),
                "refs": [r2(x) for x in h["referencias"]] if h.get("referencias") else None,
                "por_semana": r2(None if gan is None else gan / sem),
                "cierre_ok": abs(suma_grupos - neto) <= 0.05,
                "cajas": sorted(lista, key=lambda x: (GRUPOS_PATRIMONIO.index(x["g"]) if x["g"] in GRUPOS_PATRIMONIO else 99, -(abs(x["usd"] or 0)))),
                "notas": h["notas"], "a_revisar": a_revisar.get(sid),
                "celda_neto": f"B{b['Neto']['fila']}", "celda_gan": f"B{gp['fila']}" if gp else None,
                "celda_gan_otra": {"celda": f"B{g_otra['fila']}", "valor": r2(g_otra.get("guardado"))} if g_otra else None,
                "_fijos": fijos_val,
            }
            self.semanas.append(s)
            prev = dict(s, neto=neto, cot=cot, ars=ars)
            prev_nombres = {c["col"]: c["n"] for c in cols.values() if not c["n"].startswith("SIN NOMBRE")}
            prev_cajas_usd = dict(caja_usd)
            criterio = []
            for c in cols.values():
                cp = prev_coef.get(c["n"])
                uno, uno_p = c["coef"] is not None and abs(c["coef"] - 1) < 1e-9, cp is not None and abs(cp - 1) < 1e-9
                if cp and c["coef"] and uno != uno_p and abs(c["total"]) > 0.005:
                    como = "1 a 1 como dólar" if uno else "como euro (× " + f"{c['coef']:.2f}".replace(".", ",") + ")"
                    d = c["total"] * (c["coef"] - cp)
                    criterio.append(f"{c['n'].capitalize()} pasa a contarse {como}: {'+' if d > 0 else ''}{fmt_usd(d)} que no son movimiento de plata")
            # cambio de la cotización del euro: revalúa los euros que había (no es movimiento de plata)
            eur_tot = sum(c["total"] for c in cols.values() if c["moneda"] == "EUR" and c["coef"] and abs(c["coef"] - 1) > 1e-9)
            if prev_eur and h["eur_usd"] and abs(h["eur_usd"] - prev_eur) > 1e-9 and abs(prev_eur_tot) > 0.005:
                d = prev_eur_tot * (h["eur_usd"] - prev_eur)
                criterio.append(f"el euro pasa de {prev_eur:.2f} a {h['eur_usd']:.2f}".replace(".", ",")
                                + f": {'+' if d > 0 else ''}{fmt_usd(d)} sobre los euros de la semana anterior, que no son movimiento de plata")
            prev_eur, prev_eur_tot = h["eur_usd"], eur_tot
            if criterio:
                s["_criterio"] = criterio
            prev_coef = {c["n"]: c["coef"] for c in cols.values() if c["coef"] is not None and (c["eur_1a1"] or c["moneda"] == "EUR")}
            self._chequeos_hoja(h, s, cols)

        self._tipica_y_marcas()
        self.meses = self._meses()
        self._chequeos_globales()
        for s in self.semanas:
            s.pop("_fijos", None)
        return self

    # ------------------------------------------------------------------------------------------- marcas
    def _tipica_y_marcas(self):
        n = self.cfg.get("semanas_tipicas", 8)
        vals = [s["por_semana"] for s in self.semanas if s["por_semana"] is not None]
        med = statistics.median(vals)
        mad = statistics.median(abs(v - med) for v in vals) * 1.4826 or 1.0
        umbral = self.cfg.get("umbral_desvio_revisar", 2.5)
        cots = [s["cot"] for s in self.semanas]
        for i, s in enumerate(self.semanas):
            previas = [x["por_semana"] for x in self.semanas[max(0, i - n):i] if x["por_semana"] is not None]
            s["tipica"] = r2(statistics.median(previas)) if len(previas) >= 3 else None
            s["tipica_n"] = len(previas)
            m = []
            if s["dias"] == 14:
                m.append({"k": "doble", "t": f"La hoja abarca dos semanas ({s['txt']}). Para comparar se cuenta como dos semanas de USD {fmt_usd(s['por_semana'] or 0)}."})
            if s["ret"] and s["ret"] > 0.005:
                det = "; ".join(f"{fmt_usd(r['monto'])} {r['detalle'].lower()}" + ("" if r["confirmado"] else " (a confirmar)") for r in s["ret_det"])
                m.append({"k": "ret", "t": f"Retiros de socios por USD {fmt_usd(s['ret'])}: {det}. No es una pérdida: se suman de vuelta a la ganancia."})
            if s["aj_det"]:
                det = "; ".join(f"{'USDT General' if a['grupo'] == 'usdt_general' else 'Deuda a cobrar' if a['grupo'] == 'deuda' else a['renglon']} {'+' if a['monto'] > 0 else ''}{fmt_usd(a['monto'])}" for a in s["aj_det"])
                m.append({"k": "aj", "t": f"Cambió lo cargado a mano en la planilla: {det}. Se muestra aparte de la ganancia de la semana."})
            z = None if s["por_semana"] is None else (s["por_semana"] - med) / mad
            if s["a_revisar"]:
                m.append({"k": "rev", "t": s["a_revisar"]})
            elif z is not None and abs(z) > umbral:
                m.append({"k": "rev", "t": f"Ganancia de USD {fmt_usd(s['gan'])}, muy lejos de lo habitual (mediana USD {fmt_usd(med)} por semana) y sin explicación cargada."})
            dud, arreglar = [], []
            if i > 0 and cots[i] is not None and cots[i] == cots[i - 1]:
                dud.append(f"cotización igual a la de la semana anterior ($ {cots[i]:,.0f})".replace(",", "."))
            if s.get("gan_planilla_error"):
                arreglar.append(f"la celda de ganancia de la planilla da error ({s['gan_planilla_error']}); el tablero la calcula con el patrimonio de las dos semanas, así que el número está bien")
            if len(getattr(self, "archivos_por_hoja", {}).get(s["hoja"], [])) > 1:
                arreglar.append(f"la hoja llegó en {len(self.archivos_por_hoja[s['hoja']])} archivos y se usó el más nuevo")
            if any(c["heredado"] for c in s["cajas"]):
                arreglar.append("una columna no tiene título y se le puso el de la hoja anterior (" + ", ".join(c["n"].capitalize().replace("Poligono", "Polígono") for c in s["cajas"] if c["heredado"]) + "): conviene ponérselo en la planilla")
            if s.get("_sin_suma"):
                dud.append("valores que no entran en la fórmula: " + ", ".join(s["_sin_suma"]))
            if s.get("_criterio"):
                dud.append("; ".join(s["_criterio"]))
            if s["notas"]:
                dud.append("notas en la hoja: " + "; ".join(s["notas"]))
            if dud:
                m.append({"k": "dudoso", "t": "Puede cambiar los números: " + "; ".join(dud) + "."})
            s["planilla"] = [x[0].upper() + x[1:] + "." for x in arreglar]
            if (s["gas_det"]["gastos"] or 0) >= self.cfg.get("umbral_gastos_grandes", 5000):
                m.append({"k": "gastos", "t": f"Semana de costos fijos: se pagaron USD {fmt_usd(s['gas_det']['gastos'])} de gastos. Conviene mirar el mes completo."})
            s["marcas"] = m
            s.pop("_sin_suma", None)
            s.pop("_criterio", None)
        self.mediana_global = r2(med)

    # ------------------------------------------------------------------------------------------- meses
    def _meses(self):
        por_mes = defaultdict(list)
        for s in self.semanas:
            por_mes[s["mes"]].append(s)
        ultimo_fin = dt.date.fromisoformat(self.semanas[-1]["fin"])
        primero_ini = dt.date.fromisoformat(self.semanas[0]["ini"])
        out = []
        for mes, ss in sorted(por_mes.items()):
            a, m = map(int, mes.split("-"))
            jj = jueves_del_mes(a, m)
            completo = ultimo_fin >= jj[-1] and primero_ini <= jj[0]
            con_gan = [s for s in ss if s["gan"] is not None]
            out.append({
                "id": mes, "nombre": f"{MESES[m - 1]} {a}", "esperadas": len(jj),
                "semanas": round(sum(s["dias"] for s in ss) / 7, 2), "hojas": [s["id"] for s in ss],
                "completo": completo, "con_ganancia": len(con_gan) == len(ss),
                "gan": r2(sum(s["gan"] for s in con_gan)) if con_gan else None,
                "gan_con": r2(sum(s["gan_con"] for s in con_gan)) if con_gan else None,
                "gas": r2(sum(s["gas"] for s in ss)),
                "ret": r2(sum(s["ret"] for s in ss)), "aj": r2(sum(s["aj"] for s in ss)),
                "neto_fin": ss[-1]["neto"],
            })
        return out

    # ------------------------------------------------------------------------------------------- chequeos
    def _chequeos_hoja(self, h, s, cols):
        # columnas con valores en filas 2-3 que no entran en ninguna fórmula (p. ej. sin la fila de sumas)
        # (las garantías netean 0; reales y libras no se suman a propósito)
        en_formula = {re.match(r"([A-Z]+)", x).group(1) for x in h["coef_neto"]}
        sin_suma = []
        for col, c in cols.items():
            if abs(c["total"]) <= 0.005 or c["g"] == "garantias" or c["n"] in ("REALES", "LIBRAS"):
                continue
            if col not in en_formula or not c["con_suma"]:
                sin_suma.append(f"{c['n']} {fmt_usd(c['total'])} ({'sin fórmula de suma' if not c['con_suma'] else 'fuera de la fórmula'})")
        if sin_suma:
            s["_sin_suma"] = sin_suma
        for e in h["chequeos"]:
            self.chequeos.append({"nivel": "revisar", "titulo": f"Hoja {h['hoja']}: {e}", "semanas": [s["id"]]})
        for e in h["errores_formula"]:
            if "Neto" in e or "Bruto" in e or "Egresos" in e:
                self.chequeos.append({"nivel": "revisar", "titulo": f"Hoja {h['hoja']}: no se pudo evaluar {e}", "semanas": [s["id"]]})
        if not s["cierre_ok"]:
            self.chequeos.append({"nivel": "revisar", "titulo": f"Hoja {h['hoja']}: los grupos no suman el patrimonio", "semanas": [s["id"]]})

    def _chequeos_globales(self):
        ss = self.semanas
        ch = self.chequeos
        n_ok = sum(1 for s in ss if s["neto_guardado"] is None or abs(s["neto"] - s["neto_guardado"]) <= 0.05)
        ch.insert(0, {"nivel": "ok" if n_ok == len(ss) else "revisar",
                      "titulo": f"El patrimonio recalculado coincide con el de la planilla en {n_ok} de {len(ss)} hojas",
                      "texto": "Cada fórmula del bloque se recalculó desde las cajas y se comparó con el valor guardado.",
                      "semanas": []})
        # hojas repetidas entre archivos
        for hoja, archivos in getattr(self, "archivos_por_hoja", {}).items():
            if len(archivos) > 1:
                s = next(x for x in ss if x["hoja"] == hoja)
                txt = f"La hoja {hoja} está en {len(archivos)} archivos; se usó la del más nuevo ({s['origen']})."
                if s["gan_planilla_error"]:
                    txt += f" Su celda de ganancia tiene {s['gan_planilla_error']}: se recalculó contra la hoja anterior."
                ch.append({"nivel": "info", "titulo": f"Hoja {hoja} corregida", "texto": txt, "semanas": [s["id"]]})
        rep_cot = [s["id"] for s in ss if any("cotización igual" in m["t"] for m in s["marcas"] if m["k"] == "dudoso")]
        if rep_cot:
            ch.append({"nivel": "revisar", "titulo": f"Cotización repetida en {len(rep_cot)} semanas",
                       "texto": "La cotización del dólar quedó igual a la de la semana anterior. Si quedó vieja, la ganancia de esas semanas está mal en proporción a los pesos que había.",
                       "semanas": rep_cot})
        her = sorted({c["n"] for s in ss for c in s["cajas"] if c["heredado"]})
        if her:
            sem = [s["id"] for s in ss if any(c["heredado"] for c in s["cajas"])]
            monto = next(c["usd"] for c in reversed(ss[-1]["cajas"]) if c["heredado"]) if any(c["heredado"] for c in ss[-1]["cajas"]) else None
            ch.append({"nivel": "revisar", "titulo": "Columna sin título",
                       "texto": f"Desde {next(x['txt'] for x in ss if x['id'] == sem[0])} una columna con saldo no tiene título ({len(sem)} hojas); se le dio el nombre que tenía antes ({', '.join(her)})"
                                + (f". Hoy suma USD {fmt_usd(monto)} al patrimonio." if monto else "."),
                       "semanas": sem})
        rev = [s for s in ss if any(m["k"] == "rev" for m in s["marcas"])]
        for s in rev:
            ch.append({"nivel": "revisar", "titulo": f"Semana {s['txt']} a revisar",
                       "texto": next(m["t"] for m in s["marcas"] if m["k"] == "rev"), "semanas": [s["id"]]})
        # reales y libras: la planilla nunca los suma al Neto (el detalle de cada semana los muestra como «no suma»)
        for nom, sim in (("REALES", "R$"), ("LIBRAS", "£")):
            con = [(s, c["t"]) for s in ss for c in s["cajas"] if c["n"] == nom and not c["suma"] and abs(c["t"] or 0) > 0.005]
            if con:
                s_max, t_max = max(con, key=lambda x: abs(x[1]))
                ch.append({"nivel": "revisar", "titulo": f"{nom.capitalize()}: la planilla nunca los suma al patrimonio",
                           "texto": f"Hay saldo en {len(con)} hojas, hasta {sim} {fmt_usd(t_max)} en {s_max['txt']}. No están en el patrimonio ni en la ganancia; "
                                    "si son de la financiera, falta sumarlos en la fórmula del Neto.",
                           "semanas": [s_max["id"]]})
        aj = [s for s in ss if s["aj_det"]]
        if aj:
            ch.append({"nivel": "info", "titulo": f"Ajustes a mano en {len(aj)} semanas",
                       "texto": "Cambios en los valores fijos del bloque (USDT General y Deuda): " + "; ".join(
                           f"{s['txt']} {'+' if s['aj'] > 0 else ''}{fmt_usd(s['aj'])}" for s in aj) + ". Por defecto no cuentan como ganancia de la semana.",
                       "semanas": [s["id"] for s in aj]})
        sin_conf = [(s, r) for s in ss for r in s["ret_det"] if not r["confirmado"]]
        if sin_conf:
            ch.append({"nivel": "revisar", "titulo": "Retiros a confirmar",
                       "texto": "; ".join(f"{s['txt']}: USD {fmt_usd(r['monto'])} ({r['detalle'].lower()})" for s, r in sin_conf)
                                + ". Se tratan como retiros de socios porque coinciden con los dividendos del Value CG.",
                       "semanas": [s["id"] for s, _ in sin_conf]})
        con_ret = [s for s in ss if s["ret"] > 0.005]
        if con_ret:
            ultimo = con_ret[-1]
            if dt.date.fromisoformat(ultimo["fin"]) < dt.date.fromisoformat(ss[-1]["fin"]) - dt.timedelta(days=45):
                ch.append({"nivel": "revisar", "titulo": f"No hay retiros de socios registrados desde {ultimo['txt']}",
                           "texto": "Si se pagaron dividendos después, no están en la planilla o están cargados en otra columna.",
                           "semanas": []})
        if self.tenencia and self.tenencia.get("mes"):
            ch.append({"nivel": "revisar", "titulo": f"Tenencia de socios cargada hasta {MESES[self.tenencia['mes'] - 1]}",
                       "texto": "El capital de cada socio sale de la hoja Tenencia del Value CG, que no se actualizó después.",
                       "semanas": []})
        if not self.signo_ok:
            ch.append({"nivel": "info", "titulo": "Signo de los pendientes sin confirmar",
                       "texto": "Los pendientes (fila 3 de cada caja) se suman al patrimonio tal como vienen del cierre del Registro General.",
                       "semanas": []})
        # renglones del bloque que leen una columna con otro nombre
        corridas = set()
        for h in self.hojas:
            nombres = {c["col"]: norm(c["nombre"]) for c in h["cajas"]}
            for et, it in h["bloque"].items():
                f = it.get("formula") or ""
                m = re.fullmatch(r"=\$?([A-Z]+)\$?\d+", f.replace(" ", ""))
                leida = nombres.get(m.group(1)) if m else None
                if m and leida and norm(et) and not norm(et).startswith(leida) and not leida.startswith(norm(et)):
                    corridas.add(f"«{et}» lee la columna {nombres[m.group(1)].title()}")
        if corridas:
            ch.append({"nivel": "info", "titulo": "Renglones del bloque que leen otra columna",
                       "texto": "; ".join(sorted(corridas)) + ". No cambia el patrimonio (esas columnas netean 0); el tablero arma los grupos por el nombre de cada caja.",
                       "semanas": []})
        ops = [h["bloque"].get("Operaciones", {}).get("guardado") for h in self.hojas]
        racha = max((sum(1 for _ in g) for k, g in itertools.groupby(ops) if k is not None), default=0)
        if racha >= 4:
            ch.append({"nivel": "info", "titulo": "«Operaciones» copiado de semana en semana",
                       "texto": f"El mismo número se repite en {racha} hojas seguidas. El tablero no lo usa.", "semanas": []})

    # ------------------------------------------------------------------------------------------- contrato
    def contrato(self, generado, corte=None):
        ss = self.semanas
        ult = ss[-1]
        socios = []
        for so in self.cfg.get("socios", []):
            cap = (self.tenencia or {}).get("capital", {}).get(so["nombre"])
            socios.append({"nombre": so["nombre"], "pct": so["pct"], "aporte": so["aporte"], "capital": r2(cap)})
        ten_al = None
        if self.tenencia and self.tenencia.get("mes"):
            a = self.cfg.get("anio", 2026)
            m = self.tenencia["mes"]
            ten_al = (dt.date(a, m % 12 + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(a, 12, 31)).isoformat()
        aportes = sum(s["aporte"] for s in self.cfg.get("socios", []))
        avisos = []
        rev = [s for s in reversed(ss) if any(m["k"] == "rev" for m in s["marcas"])]
        if rev:
            det = " y ".join(f"{s['txt']} {'+' if (s['var'] or 0) > 0 else ''}{fmt_usd(s['var'] or 0)}" for s in rev)
            avisos.append({"k": "rev", "semanas": [s["id"] for s in rev],
                           "t": f"{'Semana' if len(rev) == 1 else str(len(rev)) + ' semanas'} con saltos sin explicar: {det}. Conviene aclararlas antes de repartir."})
        # el resto de lo que hay que revisar va en una sola franja que abre la lista de «¿Le creo a estos números?»
        todos = [c["titulo"] for c in self.chequeos if c["nivel"] == "revisar"]
        otros = [x for x in todos if not x.startswith("Semana ")]
        if todos:
            ej = " y ".join(x[0].lower() + x[1:] for x in otros[:2])
            avisos.append({"k": "dudoso", "semana": None, "ancla": "revisar",
                           "t": f"Para el que arma la planilla: {len(todos)} {'punto' if len(todos) == 1 else 'puntos'} para revisar"
                                + (f": {'las semanas de arriba y ' if len(todos) > len(otros) else ''}{len(otros)} más, por ejemplo {ej}." if otros else ".")})
        return {
            "meta": {
                "generado": generado, "corte": corte or ult["fin"], "ultima": ult["id"], "hojas": len(ss),
                "archivos": [a.split("/")[-1] for a in self.archivos], "tenencia_al": ten_al,
                "tenencia_archivo": (self.tenencia or {}).get("archivo"), "anio": self.cfg.get("anio"),
                "mediana_global": self.mediana_global,
                "estado": "avisos" if any(c["nivel"] == "revisar" and ("no se pudo" in c["titulo"] or "no suman" in c["titulo"])
                                          for c in self.chequeos) else "ok",
            },
            "config": {"umbral_gastos": self.cfg.get("umbral_gastos_grandes", 5000),
                       "semanas_tipicas": self.cfg.get("semanas_tipicas", 8),
                       "regla_dividendo": self.cfg.get("regla_dividendo", 0.10)},
            "socios": {"lista": socios, "tenencia_al": ten_al, "aportes": r2(aportes),
                       "suma_pct": r2(sum(s["pct"] for s in socios))},
            "semanas": ss, "meses": self.meses, "chequeos": self.chequeos, "avisos": avisos,
        }
