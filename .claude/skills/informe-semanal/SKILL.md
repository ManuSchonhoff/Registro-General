---
name: informe-semanal
description: Rutina semanal completa sobre el Registro General. Procesa en un paso los Excel de datos/ con actualizar.py (análisis, tableros v1 y v2, chequeos de control, notas), republica los tableros como Artifacts y, si lo piden, corre el agente asesor-financiero para el informe. Usar cuando suban un Registro General o una actualización nueva, o pidan "actualizar el tablero", "correr el análisis" o "el informe de la semana".
---

# Rutina semanal

Todo sale de `actualizar.py` (detalle en el README, sección "Actualización semanal (un paso)", y en
`docs/tablero_v2_spec.md`, sección 7). Los tableros se publican **sin clave**: el Artifact ya es privado. `--clave`
queda solo para mandar el HTML por fuera, si lo piden.

1. **Guardar lo que subieron.** Copiá cada Excel a `datos/AAAA-MM-DD_<nombre>.xlsx`, con la fecha de hoy adelante y
   sin borrar lo anterior: `actualizar.py` usa la fecha del nombre para ordenar los archivos y elige solo qué archivo
   aporta cada semana. Alcanza con la hoja de la semana nueva **si `datos/` ya tiene un Registro General completo**; el
   Registro completo hace falta si cambiaron los cheques (hoja CQ) o los inversores (hoja Inversores) y siempre que
   `datos/` esté vacío (no está en git: en una sesión nueva puede no haber nada). Con una hoja suelta y sin base, el plan
   bloquea por C05: pedí el Registro completo.
2. **Cotizaciones.** Si el usuario pasó cotizaciones, cargalas en `config.json` (`cotizaciones.ars_unica` o
   `ars_por_semana`, `eur_en_usd`, `usdt_en_usd`) antes de correr.
3. **Si la sesión arrancó sin `salidas/`** (no está en git): si falta `salidas/notas_manuales.json` y no hay ningún
   `salidas/*/tablero_v2_datos.json`, recuperá las notas del último v2 publicado antes de procesar. Buscalo con
   `Artifact list` por título ("Tablero semanal"), leelo con `Artifact read` (el resultado dice en qué archivo quedó la
   página) y pasá ese archivo con `--notas-desde <archivo>` en los pasos 4 y 5 (también en el `--dry-run`, así el plan
   muestra las notas que se van a recuperar). Así no se pierden las filas ya revisadas ni los hallazgos.
4. **Ver el plan:** `python3 actualizar.py --dry-run` (no escribe nada). Mostrale al usuario en dos o tres líneas
   qué archivo es la base, cuáles son actualizaciones o se ignoran, la última semana (cerrada o en curso) y la fecha de
   corte. Si aparece algo **BLOQUEANTE** (código de salida 2), frená y preguntá antes de seguir.
5. **Procesar:** `python3 actualizar.py` (tarda alrededor de un minuto).
   - La primera vez, con `--sembrar-revisadas`: da por revisadas todas las diferencias de carga graves y menores (Alta
     y Media en el JSON) hasta la última semana cerrada, como mucho hasta la del 18/10/2026, y resuelve los hallazgos
     existentes (el 19/10/2026 el dueño confirmó que esos errores de carga ya están corregidos). Si ya se hizo, el script
     lo avisa y no lo repite.
   - Si el script avisa que suma notas escritas a mano en `salidas/<fecha>/notas_tablero.json`, mostrale al usuario los
     textos que imprime.
   - Código 0: listo para publicar. Código 2: hay bloqueantes; las salidas con fecha se escribieron (no corras el asesor
     sobre esa carpeta hasta reprocesar sin bloqueantes), pero las rutas fijas no cambiaron. Explicá cuáles son y preguntá: se corrige la planilla o, si el dueño decide publicar igual,
     `--forzar`. Código 1: error (mirá el detalle).
6. **Resumir el control** en una línea, desde `salidas/<fecha>/validaciones.json` (por ejemplo: "12–18 oct cerrada ·
   38 semanas · 0 bloqueantes · 1 aviso: una caja sin moneda asignada").
7. **Lo que el dueño da por resuelto** se anota en `salidas/notas_manuales.json` (una entrada por línea) y se vuelve a
   correr `python3 actualizar.py`:
   - Una fila ("la fila 120 del 12/10 ya está"): buscá en `revisar` de `salidas/<fecha>/tablero_v2_datos.json` la
     semana que incluye esa fecha y la fila; su `clave` es `<inicio>#<fila>#<N° de Ope>` (por ejemplo
     `2026-10-12#120#15001`). Agregá a `revisadas` `{"clave": "...", "fecha": "<hoy>", "nota": "<lo que dijo>"}`.
   - Un aviso de control ("lo de la caja sin moneda"): sus claves están en `claves` del chequeo en `validaciones.json`
     (`control:C12:<caja>`); agregá cada una a `revisadas`. Los bloqueantes no se dan por revisados.
   - Un hallazgo resuelto: `estado` "resuelta" y `fecha_estado` de hoy. Una pregunta respondida: `estado`
     "respondida", y la respuesta va a `docs/notas_duenos.md` **sin nombres de clientes ni montos** (ese archivo se
     versiona); si la respuesta los necesita, agregala como campo `respuesta` de la pregunta en `notas_manuales.json`
     (los campos extra se conservan). Un hallazgo o una pregunta nueva: al final de su lista,
     con el id siguiente (`h12`, `p9`), `estado` "abierta", `fecha` de hoy y, si es de una semana, `semana` con su
     inicio (`AAAA-MM-DD`).
   - No edites `salidas/<fecha>/notas_tablero.json`: es la copia de las notas abiertas para el v1 y se regenera.
8. **Publicar** a partir de `salidas/estado_publicacion.json`, primero el v2 (`salidas/tablero_v2_artifact.html`) y
   después el v1 (`salidas/tablero_v1_artifact.html`):
   - Leé el archivo completo antes de publicarlo (pesa menos de 800 KB).
   - Si el tablero ya tiene `url`: primero `Artifact read` de esa URL y después publicá la ruta fija con ese `url`.
   - Si no tiene `url`, antes de crear uno nuevo buscalo con `Artifact list` por título: "Tablero semanal" (v2) y
     "Tablero Registro General" (v1). Si aparece, guardalo con `python3 actualizar.py --guardar-url v2 <URL>` (o
     `v1`) y republicá ahí. Si no aparece, publicá un Artifact **nuevo** (el v2 nunca pisa al v1) y guardá su URL con
     `--guardar-url`.
9. **Informe del asesor (opcional):** solo si piden "el informe". Lanzá el agente `asesor-financiero` sobre
   `salidas/<fecha>/` (si la sesión no lo tiene registrado, usá un agente general con el contenido de
   `.claude/agents/asesor-financiero.md` como instrucciones). Antes, revisá el "Resultado estimado mensual" y
   `metricas.json`: si algo es absurdo (por ejemplo, un mes 10 veces mayor que el resto), buscá la causa en los CSV.
   Ese chequeo es del informe; el tablero no muestra ganancia ni resultado.
10. **Entregar:** los links de los tableros y el resumen de una línea del paso 6. Si hubo informe, también
    `informe_asesor.md` y `Analisis_Registro_General.xlsx`, con un resumen corto.

Los datos y las salidas tienen nombres y montos de clientes: **no se suben al repositorio**
(`datos/` y `salidas/` están en `.gitignore`).
