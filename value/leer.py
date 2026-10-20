"""Lectura de la Calculadora Semanal (Value · Cambio General).

Cada hoja semanal ("DDMM - DDMM") tiene una fila por caja (fila 1: nombre; filas 2 y 3: saldo y pendientes; una fila
de sumas) y debajo un bloque de cálculo (Dólares, Pesos, Euros, Deuda, USDT, Egresos, Neto, Bruto...). Las fórmulas
del bloque cambian de hoja en hoja (rangos que se corren, cotización escrita dentro de la fórmula, filas que entran y
salen del Neto), así que no se suponen posiciones: cada fórmula se evalúa como una combinación lineal de las celdas de
las cajas. Eso da el valor de cada fila del bloque y cuánto aporta cada caja al Neto, y permite verificar que el Neto
recalculado coincida con el que guardó la planilla.
"""
import datetime as dt
import os
import re

import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

SEMANAL = re.compile(r"^(\d{2})(\d{2}) - (\d{2})(\d{2})(.*)$")
REF = r"\$?([A-Z]{1,3})\$?(\d+)"
TOKEN = re.compile(rf"\s*(?:(?P<rango>{REF}:{REF})|(?P<ref>{REF})|(?P<num>\d+(?:\.\d+)?)|(?P<fn>[A-Z]+)\(|(?P<op>[-+*/(),]))")
MONEDAS = ("USD", "ARS", "EUR", "REAL")
TOL = 0.05


class ErrorFormula(Exception):
    pass


# ----------------------------------------------------------------------------------------------- álgebra lineal mínima
def _lin(c=0.0, **_):
    return {"": float(c)}


def _sumar(a, b, k=1.0):
    r = dict(a)
    for x, v in b.items():
        r[x] = r.get(x, 0.0) + k * v
    return r


def _escalar(a, k):
    return {x: v * k for x, v in a.items()}


def _const(a):
    return all(abs(v) < 1e-12 for x, v in a.items() if x)


class Hoja:
    """Evalúa fórmulas de una hoja como combinaciones lineales de las celdas de caja (filas 1 a 5)."""

    def __init__(self, wsf, wsv, fila_suma):
        self.wsf, self.wsv, self.fila_suma = wsf, wsv, fila_suma
        self.cache = {}

    def valor(self, celda):
        v = self.wsv[celda].value
        return v if isinstance(v, (int, float)) and not isinstance(v, bool) else 0.0

    def celda(self, col, fila):
        """Expresión lineal de una celda. Las de las filas 2 a 5 son variables (las cajas); el resto se evalúa."""
        clave = f"{col}{fila}"
        if clave in self.cache:
            return self.cache[clave]
        f = self.wsf[clave].value
        if fila <= 5:
            # una celda de caja: la fila de sumas se descompone en filas 2 y 3 si es =SUM(x2:x3)
            if fila == self.fila_suma and isinstance(f, str) and f.startswith("="):
                r = self.evaluar(f[1:])
            else:
                r = {clave: 1.0}
        elif isinstance(f, str) and f.startswith("="):
            self.cache[clave] = None   # corta ciclos
            try:
                r = self.evaluar(f[1:])
            except ErrorFormula:
                del self.cache[clave]
                raise
        elif isinstance(f, (int, float)) and not isinstance(f, bool):
            r = _lin(f)
        else:
            r = _lin(0)
        self.cache[clave] = r
        return r

    def evaluar(self, texto):
        return _Parser(self, texto).resultado()


class _Parser:
    """Parser recursivo de una fórmula (uno por fórmula: las celdas referenciadas se evalúan con su propio parser).
    expr := term (('+'|'-') term)* ; term := factor (('*'|'/') factor)* ; factor := num | ref | SUM(...) | (expr) | -factor"""

    def __init__(self, hoja, texto):
        self.h, self.texto = hoja, texto.strip()
        self.toks, pos = [], 0
        while pos < len(self.texto):
            m = TOKEN.match(self.texto, pos)
            if not m or m.end() == pos:
                raise ErrorFormula(f"no entiendo '{self.texto[pos:pos + 15]}' en ={self.texto}")
            self.toks.append(m)
            pos = m.end()
        self.i = 0

    def resultado(self):
        r = self._expr()
        if self.i != len(self.toks):
            raise ErrorFormula(f"sobra texto en ={self.texto}")
        return r

    def _ver(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def _op(self, o):
        t = self._ver()
        if t is not None and t.group("op") == o:
            self.i += 1
            return True
        return False

    def _ref(self, col, fila):
        r = self.h.celda(col, fila)
        if r is None:
            raise ErrorFormula("referencia circular")
        return r

    def _expr(self):
        r = self._term()
        while True:
            if self._op("+"):
                r = _sumar(r, self._term())
            elif self._op("-"):
                r = _sumar(r, self._term(), -1)
            else:
                return r

    def _term(self):
        r = self._factor()
        while True:
            if self._op("*"):
                b = self._factor()
                if _const(b):
                    r = _escalar(r, b[""])
                elif _const(r):
                    r = _escalar(b, r[""])
                else:
                    raise ErrorFormula("producto de dos celdas de caja")
            elif self._op("/"):
                b = self._factor()
                if not _const(b) or abs(b[""]) < 1e-12:
                    raise ErrorFormula("división por una caja o por cero")
                r = _escalar(r, 1 / b[""])
            else:
                return r

    def _factor(self):
        t = self._ver()
        if t is None:
            raise ErrorFormula("fórmula incompleta")
        if self._op("-"):
            return _escalar(self._factor(), -1)
        if self._op("+"):
            return self._factor()
        if self._op("("):
            r = self._expr()
            if not self._op(")"):
                raise ErrorFormula("falta ')'")
            return r
        self.i += 1
        if t.group("num"):
            return _lin(float(t.group("num")))
        if t.group("ref"):
            col, fila = re.match(REF, t.group("ref")).groups()
            return self._ref(col, int(fila))
        if t.group("fn"):
            if t.group("fn") != "SUM":
                raise ErrorFormula(f"función {t.group('fn')} no soportada")
            r = _lin(0)
            if self._op(")"):
                return r
            while True:
                s = self._ver()
                if s is not None and s.group("rango"):
                    self.i += 1
                    c1, f1, c2, f2 = re.match(f"{REF}:{REF}", s.group("rango")).groups()
                    for ci in range(column_index_from_string(c1), column_index_from_string(c2) + 1):
                        for fi in range(int(f1), int(f2) + 1):
                            r = _sumar(r, self._ref(get_column_letter(ci), fi))
                else:
                    r = _sumar(r, self._expr())
                if self._op(")"):
                    return r
                if not self._op(","):
                    raise ErrorFormula("se esperaba ',' o ')'")
        raise ErrorFormula(f"token inesperado {t.group(0)}")


# ----------------------------------------------------------------------------------------------- utilidades de hoja
def fechas_hoja(nombre, anio):
    """'1008 - 2308 (Dos Semanas)' → (2026-08-10, 2026-08-23, ' (Dos Semanas)')."""
    m = SEMANAL.match(nombre)
    if not m:
        return None
    d1, m1, d2, m2, resto = m.groups()
    ini = dt.date(anio, int(m1), int(d1))
    fin = dt.date(anio + (1 if int(m2) < int(m1) else 0), int(m2), int(d2))
    return ini, fin, resto.strip()


def _fila_con(ws, prueba, desde=3, hasta=7):
    for r in range(desde, hasta + 1):
        n = sum(1 for c in range(1, ws.max_column + 1) if prueba(ws.cell(r, c).value))
        if n >= 5:
            return r
    return None


def fila_suma(ws):
    return _fila_con(ws, lambda v: isinstance(v, str) and v.upper().startswith("=SUM("))


def fila_moneda(ws):
    return _fila_con(ws, lambda v: v in MONEDAS)


def _num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def leer_hoja(wsf, wsv, origen, anio):
    """Lee una hoja semanal. Devuelve un dict con cajas, bloque, aportes por caja y chequeos."""
    ini, fin, sufijo = fechas_hoja(wsf.title, anio)
    fs = fila_suma(wsf)
    fm = fila_moneda(wsf)
    h = Hoja(wsf, wsv, fs)

    # cajas: una por columna con encabezado o con números en las filas 2-3
    cajas = []
    for c in range(1, wsf.max_column + 1):
        col = get_column_letter(c)
        nombre = wsf.cell(1, c).value
        saldo, pend = _num(wsv.cell(2, c).value), _num(wsv.cell(3, c).value)
        if nombre is None and saldo is None and pend is None:
            continue
        cajas.append({
            "col": col,
            "nombre": str(nombre).strip() if nombre is not None else None,
            "moneda": wsf.cell(fm, c).value if fm else None,
            "saldo": saldo or 0.0,
            "pendiente": pend or 0.0,
            "total": (saldo or 0.0) + (pend or 0.0),
        })

    # bloque de cálculo: etiquetas de la columna A desde la fila 6
    bloque, errores = {}, []
    for r in range(6, min(wsf.max_row, 40) + 1):
        a = wsf.cell(r, 1).value
        if not isinstance(a, str) or not a.strip() or a.startswith("="):
            continue
        etiqueta = a.strip()
        if etiqueta in bloque:          # 'Ganancia Neta' aparece dos veces: la primera es la del cálculo
            continue
        f = wsf.cell(r, 2).value
        guardado = wsv.cell(r, 2).value
        item = {"fila": r, "formula": f if isinstance(f, str) and f.startswith("=") else None,
                "guardado": _num(guardado), "error_guardado": guardado if isinstance(guardado, str) and guardado.startswith("#") else None,
                "otra_hoja": bool(isinstance(f, str) and "!" in f)}
        if item["formula"] and not item["otra_hoja"]:
            try:
                item["lin"] = h.celda("B", r)
            except ErrorFormula as e:
                errores.append(f"B{r} ({etiqueta}): {e}")
        elif item["formula"] is None and _num(f) is not None:
            item["lin"] = _lin(f)
        bloque[etiqueta] = item

    # cotización y factor del euro: C8/C9 si son números; si no, el divisor escrito en la fórmula de Pesos
    fp = bloque.get("Pesos", {}).get("formula") or ""
    cot = _num(wsv["C8"].value) if (wsf["C7"].value == "Cotizacion" or re.search(r"/\s*\$?C\$?8\b", fp)) else None
    if cot is None and fp:
        m = re.search(r"/\s*(\d+(?:\.\d+)?)\s*$", bloque["Pesos"]["formula"])
        if m:
            cot = float(m.group(1))
    eur = _num(wsv["C9"].value) if isinstance(_num(wsv["C9"].value), float) and (wsv["C9"].value or 0) < 5 else None
    for k in ("Euros", "euros"):
        if eur is None and k in bloque and bloque[k]["formula"]:
            m = re.search(r"\*\s*(\d+(?:\.\d+)?)\s*$", bloque[k]["formula"])
            if m:
                eur = float(m.group(1))

    def val(lin):
        return sum(v * (1.0 if x == "" else (_num(wsv[x].value) or 0.0)) for x, v in lin.items())

    for it in bloque.values():
        if "lin" in it:
            it["calculado"] = val(it["lin"])

    # aporte de cada caja al Neto (y al Bruto) en USD; las constantes (Deuda, USDT) quedan como filas propias
    neto = bloque.get("Neto", {})
    aportes = {}
    if "lin" in neto:
        for x, coef in neto["lin"].items():
            if x == "":
                continue
            col = re.match(r"([A-Z]+)", x).group(1)
            v = _num(wsv[x].value) or 0.0
            aportes[col] = aportes.get(col, 0.0) + coef * v
    # filas del bloque que suman al Neto (por fila): se arma desde la fórmula del Neto (SUM sobre la columna B)
    filas_neto = []
    if neto.get("formula"):
        for rango in re.findall(r"B(\d+):B(\d+)|B(\d+)", neto["formula"]):
            if rango[0]:
                filas_neto += list(range(int(rango[0]), int(rango[1]) + 1))
            else:
                filas_neto.append(int(rango[2]))
    por_fila = {}
    for et, it in bloque.items():
        if it["fila"] in filas_neto and "calculado" in it:
            por_fila[et] = it["calculado"]

    chequeos = []
    for et in ("Dolares", "Pesos", "Euros", "Egresos", "Neto", "Bruto"):
        it = bloque.get(et)
        if it and "calculado" in it and it["guardado"] is not None and abs(it["calculado"] - it["guardado"]) > TOL:
            chequeos.append(f"{et}: recalculado {it['calculado']:.2f} ≠ guardado {it['guardado']:.2f}")
    if "Neto" in bloque and "calculado" in bloque["Neto"] and aportes:
        const = bloque["Neto"]["lin"].get("", 0.0)
        if abs(sum(aportes.values()) + const - bloque["Neto"]["calculado"]) > TOL:
            chequeos.append("los aportes por caja no suman el Neto")

    return {
        "hoja": wsf.title, "origen": os.path.basename(origen), "inicio": ini, "fin": fin, "sufijo": sufijo,
        "dias": (fin - ini).days + 1, "fila_suma": fs, "fila_moneda": fm, "cotizacion": cot, "eur_usd": eur,
        "cajas": cajas, "bloque": bloque, "aportes_neto": aportes, "por_fila": por_fila,
        "errores_formula": errores, "chequeos": chequeos,
    }


def leer_carpeta(carpeta, anio=2026):
    """Lee todos los .xlsx de la carpeta en orden de nombre; cada hoja semanal sale del último archivo que la trae.
    Devuelve (hojas semanales en orden cronológico, archivos leídos, libros abiertos por archivo)."""
    archivos = sorted(os.path.join(carpeta, f) for f in os.listdir(carpeta)
                      if f.lower().endswith(".xlsx") and not f.startswith("~$"))
    elegidas, libros = {}, {}
    for p in archivos:
        wf = openpyxl.load_workbook(p)
        wv = openpyxl.load_workbook(p, data_only=True)
        libros[p] = (wf, wv)
        for ws in wf.worksheets:
            if SEMANAL.match(ws.title):
                elegidas[ws.title] = (p, ws, wv[ws.title])
    hojas = [leer_hoja(ws, wsv, p, anio) for p, ws, wsv in elegidas.values()]
    hojas.sort(key=lambda h: h["inicio"])
    return hojas, archivos, libros
