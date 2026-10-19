"""Actualización semanal en un paso: plan → notas → análisis y tableros v1 y v2 → rutas fijas para publicar.

Uso:
    python3 actualizar.py [--dry-run] [--fecha AAAA-MM-DD] [--datos datos/] [--archivos A.xlsx …] [--clave X] [--sin-v1]
                          [--forzar] [--sembrar-revisadas] [--guardar-url {v1,v2} URL] [--salidas salidas/]
                          [--notas-desde ARCHIVO] [--excluir-hoja "DDMM - DDMM"]…

1. Plan: toma todos los .xlsx de datos/ (o los de --archivos, en cualquier orden). La base es el más reciente con las
   hojas CQ e Inversores; las actualizaciones, los posteriores a la base en orden de fecha (la AAAA-MM-DD del nombre).
2. Fecha de corte: el domingo de la última semana si está cerrada; si no, el último Cierre con fecha (--fecha manda).
3. Notas: salidas/notas_manuales.json (si falta, se reconstruye desde el último tablero v2 o desde el último
   notas_tablero.json) y copia de las notas abiertas en salidas/<fecha>/notas_tablero.json para el v1.
4. Proceso: correr.pipeline con el v1, el v2 y sus artifacts (sin clave salvo --clave), con una sola lectura del Excel.
5. Publicación: sin bloqueantes (o con --forzar) copia los artifacts a salidas/tablero_v1_artifact.html y
   salidas/tablero_v2_artifact.html y actualiza salidas/estado_publicacion.json.

--dry-run muestra el plan y los chequeos que ya se pueden evaluar, sin escribir nada.
--sembrar-revisadas (una sola vez): marca como revisadas todas las filas Altas y Medias hasta la última semana cerrada y
resuelve los hallazgos existentes (los errores de carga que el dueño dio por resueltos el 19/10/2026).
--guardar-url v2 URL: graba la URL del Artifact publicado en estado_publicacion.json (no procesa nada).
--notas-desde ARCHIVO: si falta notas_manuales.json, lo reconstruye desde un tablero v2 sin clave guardado localmente
(el HTML del Artifact o un tablero_v2_datos.json).

Código de salida: 0 si está todo bien (o si se publicó con --forzar); 2 si hay bloqueantes (las salidas con fecha se
escriben igual, pero no las rutas fijas); 1 si hubo un error.
Especificación: docs/tablero_v2_spec.md, sección 7.
"""
import argparse
import datetime as dt
import json
import os
import sys
import traceback

sys.dont_write_bytecode = True  # --dry-run no escribe nada, tampoco cachés de Python
RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)

from registro import actualizacion as AC  # noqa: E402

NIVEL_TXT = {"bloqueante": "BLOQUEANTE", "aviso": "AVISO", "info": "INFO", "ok": "OK", "no_evaluado": "SIN EVALUAR"}
ROL_TXT = {"base": "base", "actualizacion": "actualización", "ignorado": "ignorado"}
FECHA_TXT = {"nombre": "del nombre", "hojas": "por su última hoja", "modificación": "por la fecha de modificación"}


def _rel(p):
    if p is None:
        return "—"
    r = os.path.relpath(p)
    return p if r.startswith("..") else r


def _plural(n, uno, varios):
    return f"{n} {uno if n == 1 else varios}"


def argumentos(argv=None):
    ap = argparse.ArgumentParser(description="Actualización semanal en un paso (tablero v1 y v2).")
    ap.add_argument("--dry-run", action="store_true", help="muestra el plan y los chequeos, sin escribir nada")
    ap.add_argument("--fecha", help="fecha de corte AAAA-MM-DD (por defecto, la de la última semana)")
    ap.add_argument("--datos", default=os.path.join(RAIZ, "datos"), help="carpeta con los Excel (por defecto, datos/)")
    ap.add_argument("--archivos", nargs="+", help="Excel a usar, en cualquier orden (en lugar de todos los de --datos)")
    ap.add_argument("--salidas", default=os.path.join(RAIZ, "salidas"),
                    help="carpeta raíz de las salidas, las notas y las rutas fijas (por defecto, salidas/)")
    ap.add_argument("--clave", help="contraseña de los tableros (por defecto, sin clave: el Artifact ya es privado)")
    ap.add_argument("--sin-v1", action="store_true", help="no genera ni publica el tablero v1")
    ap.add_argument("--forzar", action="store_true", help="publica en las rutas fijas aunque haya bloqueantes")
    ap.add_argument("--excluir-hoja", action="append", default=[], metavar="'DDMM - DDMM'",
                    help="saltea una hoja (todavía no disponible: requiere excluir en registro/leer.py)")
    ap.add_argument("--sembrar-revisadas", action="store_true",
                    help="una sola vez: da por revisadas las filas Altas y Medias hasta la última semana cerrada y "
                         "resuelve los hallazgos existentes")
    ap.add_argument("--guardar-url", nargs=2, action="append", metavar=("{v1,v2}", "URL"),
                    help="graba la URL del Artifact publicado en estado_publicacion.json y termina")
    ap.add_argument("--notas-desde", metavar="ARCHIVO",
                    help="si falta notas_manuales.json, lo reconstruye desde este tablero v2 (HTML sin clave o JSON)")
    ap.add_argument("--config", default=os.path.join(RAIZ, "config.json"))
    return ap.parse_args(argv)


def imprimir_plan(plan, ult, fecha, motivo, salida, checks):
    anio = plan["anio"]
    print("Plan")
    for d in plan["archivos"]:
        n = len(d["semanas"])
        partes = [f"fecha {d['fecha']} ({FECHA_TXT[d['fecha_origen']]})"]
        if d["rol"] == "base":
            partes.append(_plural(n, "hoja semanal", "hojas semanales"))
            partes.append("con CQ e Inversores" if d["cq"] and d["inversores"] else
                          "SIN " + " ni ".join(h for h, ok in (("CQ", d["cq"]), ("Inversores", d["inversores"])) if not ok))
        else:
            lista = ", ".join(h for _, h in d["semanas"][-6:])
            partes.append(_plural(n, "hoja semanal", "hojas semanales") + (f": {lista}" if n else "")
                          + (" …" if n > 6 else ""))
        if d["motivo"]:
            partes.append(d["motivo"])
        print(f"  {ROL_TXT[d['rol']]:<14} {d['archivo']} · " + " · ".join(partes))
    print("Orden de lectura: " + " → ".join(os.path.basename(r) for r in plan["rutas"]))
    sem = plan["semanas"]
    print(f"Semanas: {len(sem)} ({AC.etiqueta(sem[0], anio)} a {AC.etiqueta(sem[-1], anio)})")
    base = os.path.basename(plan["base"])
    otras = [x for x in AC.escanear(plan) if x["archivo"] != base]
    if otras:
        print("Semanas que salen de una actualización: "
              + "; ".join(f"{AC.etiqueta(x['semana'], anio)} ← {x['archivo']}" for x in otras))
    print(f"Última semana: {AC.etiqueta(ult['nombre'], anio)} (hoja «{plan['semana_hoja'][ult['nombre']]}» de "
          f"{ult['archivo']}): {'cerrada' if ult['cerrada'] else 'en curso'}"
          + ("" if ult["cerrada"] else f", último Cierre con fecha: {ult['ultimo_cierre'] or 'ninguno'}"))
    print(f"Fecha de corte: {fecha} ({motivo})")
    print(f"Salida: {_rel(salida)}/")
    print("Chequeos que ya se pueden evaluar:")
    for c in sorted(checks, key=lambda c: (["bloqueante", "aviso", "info", "ok", "no_evaluado"].index(c["nivel"]), c["id"])):
        print(f"  {NIVEL_TXT[c['nivel']]:<11} {c['id']} {c['titulo']}: {c['detalle']}")


def _resumen_notas(notas):
    ha = sum(h["estado"] == "abierta" for h in notas["hallazgos"])
    pa = sum(p["estado"] == "abierta" for p in notas["preguntas"])
    return (f"{_plural(len(notas['hallazgos']), 'hallazgo', 'hallazgos')} ({ha} abiertos), "
            f"{_plural(len(notas['preguntas']), 'pregunta', 'preguntas')} ({pa} abiertas), "
            f"{_plural(len(notas['revisadas']), 'fila o aviso revisado', 'filas o avisos revisados')}")


def actualizar(a):
    cfg = json.load(open(a.config, encoding="utf-8"))
    raiz = os.path.abspath(a.salidas)

    if a.guardar_url:
        for tablero, url in a.guardar_url:
            AC.guardar_url(raiz, tablero, url)
            print(f"URL del {tablero} guardada en {_rel(os.path.join(raiz, AC.ESTADO))}: {url}")
        return 0
    if a.excluir_hoja:
        print("--excluir-hoja todavía no está disponible: requiere el cambio P1 de registro/leer.py (excluir).",
              file=sys.stderr)
        return 1
    if a.fecha:
        try:
            dt.date.fromisoformat(a.fecha)
        except ValueError:
            raise AC.ErrorUsuario(f"La fecha {a.fecha!r} no es válida: tiene que ser AAAA-MM-DD") from None
    if a.notas_desde and not os.path.exists(a.notas_desde):
        raise AC.ErrorUsuario(f"No existe {a.notas_desde}")

    if a.archivos:
        faltan = [x for x in a.archivos if not os.path.isfile(x)]
        if faltan:
            raise AC.ErrorUsuario("No existe " + ", ".join(faltan))
    archivos = [os.path.abspath(x) for x in a.archivos] if a.archivos else AC.listar_excels(a.datos)
    plan = AC.planificar(archivos, cfg)
    ult = AC.ultima_semana(plan)
    fecha, motivo = (a.fecha, "indicada con --fecha") if a.fecha else AC.fecha_corte(ult)
    salida = os.path.join(raiz, fecha)
    estado_path = os.path.join(raiz, AC.ESTADO)
    previo = AC._leer_json(estado_path) if os.path.exists(estado_path) else None
    checks = AC.chequeos_plan(plan, previo, fecha, cfg)
    semanas = [AC.fechas_semana(n, plan["anio"]) for n in plan["semanas"]]
    hasta = AC.tope_sembrado(cfg, AC.ultima_cerrada_ini(plan, ult))
    hasta_txt = next((AC.etiqueta(n, plan["anio"]) for n, (i, _) in zip(plan["semanas"], semanas) if i.isoformat() == hasta),
                     hasta or "—")
    imprimir_plan(plan, ult, fecha, motivo, salida, checks)

    # notas (en memoria; se escriben solo si no es --dry-run)
    notas, origen = AC.cargar(raiz, semanas, desde=a.notas_desde)
    if origen["tipo"] == "manuales":
        if a.notas_desde:
            print(f"Ya existe {_rel(origen['archivo'])}: se ignora --notas-desde.")
        print(f"Notas: {_rel(origen['archivo'])} ({_resumen_notas(notas)})")
    elif origen["tipo"] == "migradas":
        print(f"Notas: no hay {_rel(os.path.join(raiz, AC.NOTAS))}; se "
              f"{'reconstruiría' if a.dry_run else 'reconstruye'} desde {_rel(origen['archivo'])} ({_resumen_notas(notas)})")
    else:
        print("Notas: no hay notas anteriores; se empieza con una lista vacía.")
    absorbidas, motivo_abs = AC.absorber_v1(notas, salida, fecha, semanas, origen=origen, raiz=raiz)
    p_v1 = _rel(os.path.join(salida, AC.NOTAS_V1))
    if absorbidas:
        print(f"  {p_v1} tiene {_plural(len(absorbidas), 'nota escrita', 'notas escritas')} a mano después del último "
              f"guardado de las notas: {'se sumarían' if a.dry_run else 'se suman'} como abiertas:")
        for t in absorbidas:
            print(f"    · {t if len(t) <= 160 else t[:157] + '…'}")
    elif motivo_abs == "viejo":
        print(f"  {p_v1} fue escrito a mano antes del último guardado de las notas: no se suma nada (sus notas ya pasaron "
              f"por {AC.NOTAS}); {'se guardaría' if a.dry_run else 'se guarda'} como {AC.NOTAS_V1_ORIGINAL} y se "
              "reemplaza por la copia de las notas abiertas.")
    hoy = dt.date.today().isoformat()
    sembrar = False
    if a.sembrar_revisadas:
        previo_s = AC.ya_sembrado(notas)
        if previo_s:
            print(f"--sembrar-revisadas: ya se sembró el {previo_s}; no se repite.")
        elif a.dry_run:
            n = sum(h["estado"] == "abierta" and (h.get("semana") is None or (hasta and h["semana"] <= hasta))
                    for h in notas["hallazgos"])
            print(f"--sembrar-revisadas: resolvería {_plural(n, 'hallazgo', 'hallazgos')} y daría por revisadas las filas "
                  f"Altas y Medias hasta {hasta_txt} (se cuentan al procesar).")
        else:
            sembrar = True
            n = AC.sembrar_hallazgos(notas, hasta, hoy)
            print(f"--sembrar-revisadas: {_plural(n, 'hallazgo pasa', 'hallazgos pasan')} a resuelto ({hoy}).")

    nb_plan = sum(c["nivel"] == "bloqueante" for c in checks)
    if a.dry_run:
        print("No se escribió nada (--dry-run).")
        return 2 if nb_plan else 0

    AC.guardar_notas(raiz, notas)
    narr, escrito = AC.arrastrar_v1(notas, salida)
    print(f"Notas para el v1: {_plural(narr, 'nota abierta', 'notas abiertas')} en {_rel(os.path.join(salida, AC.NOTAS_V1))}"
          + ("" if escrito else " (sin cambios)"))

    plan["control"] = AC.chequeos_escaneo(plan)
    plan["origen_notas"] = dict(origen, arrastradas=narr)
    sembradas = {}
    if sembrar:
        def antes_v2(R, b, T, M):
            sembradas["filas"] = AC.sembrar_filas(notas, AC.claves_revisar(R, b, T, hasta), hoy)
            AC.guardar_notas(raiz, notas)
        plan["antes_v2"] = antes_v2
    if a.clave:
        print("Aviso: el modo con clave del v2 todavía no está terminado; sin --clave los dos tableros abren directo.")

    import correr
    try:
        out = correr.pipeline(plan["rutas"], fecha, salida, cfg, tablero=not a.sin_v1, tablero_v2=True, artifact=True,
                              clave=a.clave, plan=plan)
    except Exception as e:  # noqa: BLE001
        if not nb_plan:
            raise
        # con un bloqueante del plan (por ejemplo, una hoja suelta sin la base) el análisis puede no tener con qué
        # trabajar: se informa el bloqueante, no el error interno
        print(f"\nNo se pudo procesar ({type(e).__name__}: {e}). Hay bloqueantes en el plan:", file=sys.stderr)
        for c in checks:
            if c["nivel"] == "bloqueante":
                print(f"  BLOQUEANTE {c['id']} {c['titulo']}: {c['detalle']}", file=sys.stderr)
        print("Las rutas fijas no cambiaron. Si falta la base, pedí el Registro General completo.", file=sys.stderr)
        return 2
    if sembrar:
        print(f"--sembrar-revisadas: {_plural(sembradas.get('filas', 0), 'fila Alta o Media queda', 'filas Altas o Medias quedan')} "
              f"como revisadas ({hoy}).")

    d2 = out["datos_v2"]
    nb = out["bloqueantes"]
    cs = d2["semanas"]["c"]
    meta = dict(fecha_corte=fecha, semana=d2["semanas"]["f"][-1][cs.index("ini")], semanas=len(d2["semanas"]["f"]),
                generado=d2["generado"])
    publicados = {}
    if nb == 0 or a.forzar:
        if out.get("artifact_v2"):
            publicados["v2"] = AC.publicar_fijo(raiz, "v2", out["artifact_v2"], meta)
        else:
            print("No hay plantilla del v2 (registro/tablero_v2_plantilla.html): el v2 no se copió a la ruta fija.")
        if out.get("artifact"):
            publicados["v1"] = AC.publicar_fijo(raiz, "v1", out["artifact"], meta)

    print()
    if nb and not a.forzar:
        cola = "no se publica: hay bloqueantes (ver validaciones.json)"
    elif nb:
        cola = "publicado con --forzar a pesar de los bloqueantes"
    else:
        cola = "listo para publicar"
    print(f"{d2['control']['resumen']} · {cola}")
    for c in d2["control"]["checks"]:
        if c["nivel"] == "bloqueante" or (c["nivel"] == "aviso" and not c["revisada"]):
            print(f"  {NIVEL_TXT[c['nivel']]} {c['id']} {c['titulo']}: {c['detalle']}")
    estado = AC.estado_publicacion(raiz)
    for t in ("v2", "v1"):
        if t in publicados:
            ruta, _ = publicados[t]
            url = estado[t].get("url")
            print(f"  {t}: {_rel(ruta)} → " + (f"republicar en {url}" if url else
                                                   f"sin URL: publicar como Artifact nuevo y guardar la URL con "
                                                   f"--guardar-url {t} URL"))
        elif t == "v1" and a.sin_v1:
            continue
        else:
            print(f"  {t}: la ruta fija {_rel(AC.ruta_fija(raiz, t))} no cambió")
    return 2 if (nb and not a.forzar) else 0


def main(argv=None):
    a = argumentos(argv)
    try:
        return actualizar(a)
    except AC.ErrorUsuario as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Cancelado.", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001 (código 1 ante cualquier error, con el detalle)
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
