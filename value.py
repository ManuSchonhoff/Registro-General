"""Tablero Value · Cambio General (patrimonio y ganancia semanal) a partir de la Calculadora Semanal.

Uso:
    python3 value.py                      # lee datos/value/, escribe salidas/value/
    python3 value.py --datos carpeta/ --salidas carpeta/ --fecha AAAA-MM-DD
    python3 value.py --guardar-url <URL>  # recuerda la URL del Artifact publicado

Lee todos los .xlsx de la carpeta (cada hoja semanal sale del archivo más nuevo, por nombre, que la trae), aplica
config.json → value y escribe:
    salidas/value/<fecha>/tablero_value.html        (para abrir en el navegador)
    salidas/value/<fecha>/tablero_value_datos.json  (todos los números, para auditar)
    salidas/value/tablero_value_artifact.html       (ruta fija para republicar el mismo Artifact)
Código de salida: 0 bien; 2 si alguna hoja no cierra (el Neto recalculado no coincide con el guardado o una fórmula no
se pudo evaluar; igual escribe, con el aviso adentro); 1 si hubo un error.
Definiciones: analisis/SPEC.md.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys

from value.leer import leer_carpeta, leer_tenencia, nombre_hoja
from value.modelo import Modelo
from value.tablero import generar

RAIZ = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--datos", help="carpeta con los Excel (por defecto config.json → value.carpeta)")
    ap.add_argument("--salidas", default=os.path.join(RAIZ, "salidas"), help="raíz de las salidas (por defecto salidas/)")
    ap.add_argument("--fecha", help="fecha de corte AAAA-MM-DD (por defecto, el domingo de la última hoja)")
    ap.add_argument("--config", default=os.path.join(RAIZ, "config.json"))
    ap.add_argument("--guardar-url", metavar="URL", help="guarda la URL del Artifact publicado y termina")
    a = ap.parse_args()

    cfg_total = json.load(open(a.config, encoding="utf-8"))
    cfg = cfg_total["value"]
    base = os.path.join(a.salidas, "value")
    estado_path = os.path.join(base, "estado_publicacion.json")
    os.makedirs(base, exist_ok=True)
    estado = json.load(open(estado_path, encoding="utf-8")) if os.path.exists(estado_path) else {}
    if a.guardar_url:
        estado["url"] = a.guardar_url
        json.dump(estado, open(estado_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"URL guardada en {estado_path}")
        return 0

    carpeta = a.datos or os.path.join(RAIZ, cfg.get("carpeta", "datos/value"))
    hojas, archivos, libros = leer_carpeta(carpeta, cfg.get("anio", 2026))
    if not hojas:
        print(f"No hay hojas semanales en {carpeta}", file=sys.stderr)
        return 1
    tenencia = leer_tenencia(libros, [s["nombre"] for s in cfg.get("socios", [])])
    signo_ok = cfg_total.get("tablero_v2", {}).get("signo_pendientes_confirmado", False)

    m = Modelo(hojas, archivos, cfg, tenencia, signo_ok, cfg_total.get("moneda_por_caja"))
    m.archivos_por_hoja = {}
    for p, (wf, _) in libros.items():
        for ws in wf.worksheets:
            m.archivos_por_hoja.setdefault(nombre_hoja(ws.title), []).append(os.path.basename(p))
    m.armar()
    corte = a.fecha or m.semanas[-1]["fin"]
    generado = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    contrato = m.contrato(generado, corte)

    artifact, documento = generar(contrato)
    carpeta_fecha = os.path.join(base, corte)
    os.makedirs(carpeta_fecha, exist_ok=True)
    open(os.path.join(carpeta_fecha, "tablero_value.html"), "w", encoding="utf-8").write(documento)
    json.dump(contrato, open(os.path.join(carpeta_fecha, "tablero_value_datos.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    fija = os.path.join(base, "tablero_value_artifact.html")
    open(fija, "w", encoding="utf-8").write(artifact)
    estado.update({"corte": corte, "ultima_semana": contrato["meta"]["ultima"], "hojas": len(m.semanas),
                   "sha256": hashlib.sha256(artifact.encode("utf-8")).hexdigest(), "generado": generado})
    json.dump(estado, open(estado_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    ult = m.semanas[-1]
    malas = [c for c in contrato["chequeos"] if c["nivel"] == "revisar" and ("no se pudo" in c["titulo"] or "no suman" in c["titulo"])]
    ok_neto = contrato["chequeos"][0]["titulo"]
    print(f"{len(m.semanas)} hojas · última {ult['txt']} · patrimonio USD {ult['neto']:,.2f} · {ok_neto}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"Tablero: {fija}")
    print(f"Datos:   {os.path.join(carpeta_fecha, 'tablero_value_datos.json')}")
    if estado.get("url"):
        print(f"Artifact publicado: {estado['url']} (republicar ahí)")
    for c in malas:
        print(f"BLOQUEANTE: {c['titulo']}", file=sys.stderr)
    return 2 if malas else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e}", file=sys.stderr)
        raise
