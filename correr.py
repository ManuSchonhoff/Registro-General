"""Corre el pipeline completo sobre un Registro General.

Uso:
    python correr.py datos/Registro_General_2026.xlsx [--salida salidas/AAAA-MM-DD] [--fecha AAAA-MM-DD]

Genera en la carpeta de salida:
    Analisis_Registro_General.xlsx   15 análisis + resultado estimado
    metricas.json                    números clave
    resumen_para_asesor.md           lo que lee el agente asesor
    datos/*.csv                      tablas base (operaciones, saldos, pendientes, cheques)
"""
import argparse
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from registro import analisis as A  # noqa: E402
from registro import exportar as X  # noqa: E402
from registro.leer import Registro  # noqa: E402


METODOLOGIA = [
    "Operaciones consideradas: filas con Fin marcado dentro del bloque de operaciones de cada semana. Quedan afuera los pendientes y las cuentas corrientes.",
    "Volumen: solo Detalle = Cajas y Recaudadora, sin las filas de USDT General (la cobertura de las transferencias; sumarlas duplicaría el volumen) ni Cambio General, y sin filas de garantías.",
    "Promedio neto = (Debe + Haber) / 2, pasado a USD. Una operación de 1.000 USD contra pesos cuenta 1.000.",
    "Pesos: cotización mediana de las operaciones USD/Pesos de cada semana. USDT: paridad semanal observada (cotización del USDT en pesos / cotización del billete). EUR y BRL: valores fijos de referencia.",
    "Clientes: se agrupan quitando lo que va entre paréntesis y normalizando acentos.",
    "La fecha de cada operación se infiere de los Cierre diarios (no todas las hojas tienen fecha): el análisis por día es aproximado.",
    "Saldos: fila Balance (saldo real) y Balance + Apertura Pendientes (caja real) al inicio de cada semana, desde el 11/05.",
    "Este tablero no incluye estimaciones de ganancia ni de resultado.",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("excel")
    ap.add_argument("--salida")
    ap.add_argument("--fecha", help="fecha de corte (por defecto, la del archivo)")
    ap.add_argument("--tablero", action="store_true", help="genera además el tablero HTML cifrado")
    ap.add_argument("--clave", help="contraseña del tablero (si falta, usa CLAVE_TABLERO o genera una)")
    ap.add_argument("--config", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    fecha = a.fecha or dt.date.fromtimestamp(os.path.getmtime(a.excel)).isoformat()
    salida = a.salida or os.path.join("salidas", fecha)
    os.makedirs(os.path.join(salida, "datos"), exist_ok=True)

    print("Leyendo", a.excel)
    R = Registro(a.excel, cfg)
    ops = R.operaciones()
    cz = R.cotizaciones(ops)
    cz_usdt = R.paridad_usdt(ops, cz)
    pend = R.pendientes_actuales(ops)
    saldos = R.saldos_semanales()
    ch, ch_res = R.cheques()
    inv = R.inversores()
    act = R.actual.idx

    b = A.Base(ops, cz, cfg, act, cz_usdt)
    cot_mes = defaultdict(list)
    for s in R.semanas:
        cot_mes[s.inicio.strftime("%Y-%m")].append(cz[s.idx])
    cot_mes = {m: sum(v) / len(v) for m, v in cot_mes.items()}

    T, M = {}, {}
    pasos = [
        ("01_ranking_clientes", lambda: A.ranking_clientes(b)),
        ("02_altas_bajas", lambda: A.altas_bajas(b, cfg["semanas_cliente_perdido"])),
        ("03_cliente_operador", lambda: A.cliente_operador(b)),
        ("04_spread_billete", lambda: A.spread_billete(b)),
        ("05_circuito_usdt", lambda: A.circuito_usdt(b)),
        ("06_comisiones", lambda: A.comisiones(b)),
        ("07_cheques", lambda: A.cheques(ch, ch_res, cz[act], fecha, cot_mes)),
        ("08_evolucion", lambda: A.evolucion(b)),
        ("09_dia_semana", lambda: A.dia_semana(b)),
        ("10_tamano", lambda: A.tamano(b)),
        ("11_calidad_carga", lambda: A.calidad_carga(b)),
        ("12_posicion", lambda: A.posicion(saldos, cfg, cz, cz_usdt)),
        ("13_pendientes", lambda: A.pendientes(pend, b)),
        ("15_gastos", lambda: A.gastos(b)),
    ]
    for nombre, f in pasos:
        print(" ·", nombre)
        t, m = f()
        T.update(t)
        M[nombre] = m
    res = A.resultado_estimado(M["04_spread_billete"], M["05_circuito_usdt"], M["06_comisiones"], M["07_cheques"],
                               M["15_gastos"], {})
    t, m = A.fondeo(inv, b, dict(zip(res.mes, res.ingresos_operativos_usd)))
    T.update(t)
    M["14_fondeo"] = m
    res = A.resultado_estimado(M["04_spread_billete"], M["05_circuito_usdt"], M["06_comisiones"], M["07_cheques"],
                               M["15_gastos"], M["14_fondeo"])
    T = {"Resultado estimado mensual": res, **T}
    M["resultado_estimado"] = dict(
        ingresos_operativos_usd=float(res.ingresos_operativos_usd.sum()),
        gastos_usd=float(res.gastos_usd.sum()), intereses_usd=float(res.intereses_inversores_usd.sum()),
        resultado_usd=float(res.resultado_estimado_usd.sum()),
        nota="Estimación desde el registro: spread de billete + margen del circuito USDT + comisiones + descuento de cheques "
             "− gastos (Detalle=Gastos) − intereses comprometidos con inversores. No incluye resultados de inversiones "
             "(Polígono, Carbox, etc.), diferencias de cambio ni ajustes. Compararlo con la ganancia semanal del análisis de patrimonio.")
    M["contexto"] = dict(
        archivo=os.path.basename(a.excel), fecha_corte=fecha, semanas=len(R.semanas),
        primera_semana=R.semanas[0].nombre, semana_actual=R.actual.nombre + " (incompleta)",
        operaciones_finalizadas=int(ops.fin.sum()), operaciones_en_volumen=int(len(b.vol)),
        cotizacion_ars_actual=cz[act], paridad_usdt_actual=round(cz_usdt[act], 4),
        cotizaciones=cfg["cotizaciones"])

    notas = {
        "Archivo": a.excel, "Fecha de corte": fecha,
        "Volumen": "Promedio neto = (Debe + Haber)/2 en USD. Solo operaciones finalizadas de Cajas y Recaudadora, sin pendientes, "
                   "sin USDT General ni Cambio General, sin filas de garantías.",
        "Cotizaciones": f"ARS por semana (mediana operada o config.json). USDT: paridad semanal observada vs. billete "
                        f"(hoy {cz_usdt[act]:.3f}). EUR {cfg['cotizaciones']['eur_en_usd']}, BRL {cfg['cotizaciones']['brl_por_usd']}.",
        "Spread billete": "Por día y canal: cotización promedio de venta − de compra × USD calzados (mín. entre comprado y vendido).",
        "Circuito USDT": "Par cliente + fila USDT General con la misma transferencia: USD del cliente − USDT pagados (valuados a la paridad).",
        "Comisiones": "Operaciones con cotización expresada en % (0-15): valor que entra − valor que sale, en USD.",
        "Pendientes": "Signo: positivo = la contraparte nos entregó valor (lo debemos); negativo = nos debe. A confirmar.",
        "Resultado estimado": M["resultado_estimado"]["nota"],
    }
    X.excel(T, notas, os.path.join(salida, "Analisis_Registro_General.xlsx"))
    X.metricas_json(M, os.path.join(salida, "metricas.json"))
    X.resumen_md(T, M, M["contexto"], os.path.join(salida, "resumen_para_asesor.md"))
    cols = [c for c in b.ops.columns if c != "imputado"]
    b.ops[cols].to_csv(os.path.join(salida, "datos", "operaciones.csv"), index=False)
    saldos.to_csv(os.path.join(salida, "datos", "saldos_semanales.csv"), index=False)
    pend.drop(columns=["imputado"]).assign(imputado=pend.imputado.map(json.dumps)).to_csv(
        os.path.join(salida, "datos", "pendientes.csv"), index=False)
    ch.to_csv(os.path.join(salida, "datos", "cheques.csv"), index=False)
    pd.DataFrame({"semana_n": list(cz), "ars_por_usd": list(cz.values()), "usd_por_usdt": [cz_usdt[k] for k in cz]}).to_csv(
        os.path.join(salida, "datos", "cotizaciones.csv"), index=False)
    if a.tablero:
        from registro import tablero as TB
        notas_path = os.path.join(salida, "notas_tablero.json")
        notas = json.load(open(notas_path, encoding="utf-8")) if os.path.exists(notas_path) else {}
        notas.setdefault("metodologia", METODOLOGIA)
        datos = TB.construir_datos(R, b, T, M, cz, cz_usdt, fecha, notas)
        clave = a.clave or os.environ.get("CLAVE_TABLERO") or TB.clave_aleatoria()
        ruta = TB.generar(datos, clave, os.path.join(salida, f"Tablero_Financiera_{fecha}.html"))
        print("Tablero:", ruta)
        if not (a.clave or os.environ.get("CLAVE_TABLERO")):
            print("Contraseña generada (guardala, no se vuelve a mostrar):", clave)
    print("Listo:", salida)


if __name__ == "__main__":
    main()
