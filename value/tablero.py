"""Tablero Value · Cambio General: inserta el contrato de datos en la plantilla HTML.

La plantilla (value/tablero_plantilla.html) no tiene datos: trae la marca MARCA, que se reemplaza por el JSON del
contrato. La versión para publicar como Artifact es la plantilla tal cual (el visor le agrega el esqueleto del
documento); la versión para abrir en el navegador se envuelve en un documento completo.
"""
import json
import os

MARCA = "/*__DATOS_VALUE__*/null"
PLANTILLA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tablero_plantilla.html")


def serializar(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")


def generar(contrato, plantilla=PLANTILLA):
    """Devuelve (html_artifact, html_documento)."""
    html = open(plantilla, encoding="utf-8").read()
    if html.count(MARCA) != 1:
        raise ValueError(f"la plantilla tiene que traer una sola marca {MARCA}")
    artifact = html.replace(MARCA, serializar(contrato), 1)
    documento = ("<!doctype html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
                 "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
                 "</head>\n<body>\n" + artifact + "\n</body>\n</html>\n")
    return artifact, documento
