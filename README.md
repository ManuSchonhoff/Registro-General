# Registro General: análisis y asesor financiero

Herramientas para analizar el Registro General de la financiera (Excel exportado de Google Sheets)
y generar cada semana un informe del agente asesor.

## Estructura

```
config.json                      cotizaciones y criterios (editable); el bloque tablero_v2 tiene umbrales y opciones del v2
actualizar.py                    actualización semanal en un paso: plan → notas → análisis y tableros v1 y v2 → rutas fijas
correr.py                        corre todo: lee el Excel → análisis → salidas (pipeline que usa actualizar.py)
registro/
  leer.py                        lectura de hojas semanales, pendientes, saldos, cheques, inversores
  analisis.py                    los 15 análisis + resultado estimado
  exportar.py                    Excel, metricas.json y resumen para el asesor
  tablero.py                     tablero v1: HTML cifrado (AES-256-GCM + PBKDF2) o en claro
  tablero_plantilla.html         interfaz del tablero v1 (sin datos)
  tablero_v2.py                  tablero v2: contrato JSON, alertas, chequeos de control y notas
  tablero_v2_plantilla.html      interfaz del tablero v2 (sin datos)
  actualizacion.py               plan de archivos, fecha de corte, notas y publicación (lo usa actualizar.py)
docs/
  contexto_negocio.md            cómo funciona el negocio y la planilla
  metodologia.md                 cómo se calcula cada número y sus límites
  tablero_v2_spec.md             especificación del tablero v2 y del flujo semanal
  notas_duenos.md                (opcional) respuestas de los dueños a preguntas del asesor
value.py                         tablero Value · Cambio General (patrimonio y ganancia) desde la Calculadora Semanal
value/
  leer.py                        lectura de la Calculadora: evalúa las fórmulas del bloque caja por caja
  modelo.py                      ganancia, retiros, ajustes a mano, grupos, meses, marcas y chequeos
  tablero.py                     inserta los datos en la plantilla
  tablero_plantilla.html         interfaz del tablero Value (sin datos)
analisis/                        inventario, informes de interpretación y SPEC del tablero Value
.claude/agents/asesor-financiero.md   definición del agente asesor
.claude/skills/informe-semanal/       rutina semanal (pipeline + asesor)
datos/      (no se versiona)     Excels del registro
salidas/    (no se versiona)     resultados por fecha
```

## Actualización semanal (un paso)

Cada semana, después de copiar a `datos/` lo que mandaron (con la fecha adelante: `datos/AAAA-MM-DD_<nombre>.xlsx`, sin
borrar lo anterior):

```bash
pip install openpyxl pandas cryptography
python3 actualizar.py --dry-run     # muestra el plan y los chequeos; no escribe nada
python3 actualizar.py               # procesa y deja los tableros listos para publicar
```

- **Plan.** Toma todos los `.xlsx` de `datos/`. La **base** es el más reciente que tiene las hojas CQ e Inversores (de
  ahí salen cheques e inversores) y va primero; las **actualizaciones** son los posteriores a la base, en orden de fecha
  (la `AAAA-MM-DD` del nombre; si el nombre no tiene fecha, el fin de su última hoja semanal). Cada hoja semanal sale
  del último archivo que la trae. Los archivos anteriores a la base se ignoran.
- **Fecha de corte.** El domingo de la última semana si está cerrada; si no, la fecha del último Cierre con fecha.
- **Salidas con fecha** (`salidas/<fecha>/`): lo de `correr.py` más `Tablero_Financiera_<fecha>.html` y
  `tablero_artifact_<fecha>.html` (v1), `Tablero_v2_<fecha>.html`, `tablero_v2_artifact_<fecha>.html`,
  `tablero_v2_datos.json` (los datos del v2, en claro) y `validaciones.json` (los chequeos de control).
- **Rutas fijas** para republicar siempre el mismo Artifact: `salidas/tablero_v2_artifact.html` y
  `salidas/tablero_v1_artifact.html`. Se copian solo si no hay chequeos bloqueantes (o con `--forzar`).
- **`salidas/estado_publicacion.json`:** por tablero (`v1`, `v2`), la `url` del Artifact publicado, la fecha de corte,
  la última semana, la cantidad de semanas, el `sha256` de la ruta fija y cuándo se generó. Python nunca borra la `url`;
  se graba con `python3 actualizar.py --guardar-url v2 <URL>`. Con menos semanas que en la última publicación, el
  chequeo C06 bloquea (falta alguna hoja).
- **`salidas/notas_manuales.json`:** la única fuente de las notas. `hallazgos` (abierta / resuelta), `preguntas`
  (abierta / respondida) y `revisadas` (`{"clave", "fecha", "nota"}`): las filas y avisos que el dueño ya revisó y no
  tienen que volver a aparecer como nuevos. La clave de una fila es `<inicio de la semana>#<fila>#<N° de Ope>` (por
  ejemplo `2026-10-12#120#15001`) y se ve en el detalle de cada fila del tablero; la de un aviso de control,
  `control:<id>:<contenido>`. Hay una entrada por línea para poder editarlo a mano. Si falta, `actualizar.py` lo
  reconstruye desde el último `salidas/*/tablero_v2_datos.json` o, si no hay, desde el último `notas_tablero.json`.
  Las notas abiertas se copian a `salidas/<fecha>/notas_tablero.json` para el v1 (ese archivo no se edita: se
  regenera). Si en esa carpeta había uno escrito a mano, sus textos se suman como abiertos solo si es posterior al
  último guardado de `notas_manuales.json`; uno anterior se guarda como `notas_tablero_original.json` sin sumar nada
  (así no se reabren notas ya resueltas).
- **Código de salida:** 0 si está todo bien; 2 si hay bloqueantes (las salidas con fecha se escriben igual, pero no
  las rutas fijas); 1 si hubo un error.

Opciones:

| Opción | Qué hace |
|---|---|
| `--dry-run` | Muestra el plan (base, actualizaciones, ignorados, qué archivo aporta cada semana, la última semana y si está cerrada) y los chequeos que ya se pueden evaluar. No escribe nada |
| `--fecha AAAA-MM-DD` | Fecha de corte (por defecto, la calculada) |
| `--datos carpeta/` | Carpeta con los Excel (por defecto, `datos/`) |
| `--archivos A.xlsx B.xlsx …` | Usa solo esos archivos, en cualquier orden, en lugar de todos los de `--datos` |
| `--salidas carpeta/` | Raíz de las salidas, las notas y las rutas fijas (por defecto, `salidas/`; sirve para pruebas) |
| `--clave X` | Tableros con contraseña (por defecto van sin clave: el Artifact ya es privado) |
| `--sin-v1` | No genera ni publica el v1 |
| `--forzar` | Copia a las rutas fijas aunque haya bloqueantes |
| `--sembrar-revisadas` | Una sola vez: da por revisadas las diferencias de carga graves y menores (Alta y Media) hasta la última semana cerrada, como mucho hasta la del 18/10/2026 (`tablero_v2.sembrar_revisadas_hasta`), y resuelve los hallazgos existentes. Si ya se hizo, no se repite |
| `--guardar-url {v1,v2} URL` | Graba la URL del Artifact en `estado_publicacion.json` y termina |
| `--notas-desde ARCHIVO` | Si falta `notas_manuales.json`, lo reconstruye desde un tablero v2 sin clave guardado localmente (el HTML del Artifact o un `tablero_v2_datos.json`) |
| `--excluir-hoja "DDMM - DDMM"` | Todavía no disponible |

El detalle de cada módulo, alerta y chequeo del v2 está en `docs/tablero_v2_spec.md`.

## Tablero Value · Cambio General (patrimonio y ganancia)

Lee la **Calculadora Semanal** (una hoja por semana, `DDMM - DDMM`) y arma un tablero interactivo para los socios:
patrimonio neto, ganancia de la semana y del mes (con y sin ajustes a mano), dónde está la plata, gastos, la parte de
cada socio y los chequeos de los datos. Las definiciones y las decisiones están en `analisis/SPEC.md`.

```bash
python3 value.py                     # lee datos/value/ y escribe salidas/value/
python3 value.py --guardar-url <URL> # recuerda la URL del Artifact publicado
```

- **Datos:** los Excel van en `datos/value/` (no en `datos/`, que es del Registro), con la fecha adelante
  (`AAAA-MM-DD_<nombre>.xlsx`). Puede ser la Calculadora completa o una hoja suelta: cada hoja semanal sale del archivo
  más nuevo (por nombre) que la trae; el prefijo «Copia de» de una hoja copiada se ignora. El Value CG va en la misma
  carpeta: de su hoja Tenencia sale el capital de cada socio.
- **Salidas:** `salidas/value/<fecha>/tablero_value.html` (abrir en el navegador), `tablero_value_datos.json` (todos
  los números) y la ruta fija `salidas/value/tablero_value_artifact.html` para republicar el mismo Artifact. La URL
  queda en `salidas/value/estado_publicacion.json`.
- **Lo que la planilla no tiene** va en `config.json` → `value`: grupos de cajas, alias de encabezados, retiros que no
  están en la columna DIVIDENDOS (por ejemplo, los cargados dentro de INTERESES), semanas a revisar con su
  explicación, socios y la regla del dividendo. Cuando el dueño explica una semana, se borra de `semanas_a_revisar`.
- **Control:** el patrimonio se recalcula evaluando las fórmulas de cada hoja y se compara con el valor guardado. Si
  alguna hoja no cierra, el código de salida es 2 y el tablero lo muestra en "¿Le creo a estos números?".
- `analisis/inventario.py` regenera `analisis/00_inventario.md` (inventario factual de las planillas, sin nombres de
  clientes; los nombres de terceros a ocultar van en `datos/value/nombres_a_ocultar.txt`).

## Uso de `correr.py` (paso a paso)

```bash
pip install openpyxl pandas
python3 correr.py datos/Registro_General_2026.xlsx --fecha 2026-10-02
```

Si llega una actualización con hojas sueltas (por ejemplo "Copia de 0510 - 1110"), se pasa después del Registro
completo: sus hojas semanales reemplazan a las del mismo nombre o se agregan (el prefijo "Copia de" se ignora).

```bash
python3 correr.py datos/Registro_General_2026.xlsx datos/Actualizacion_2026-10-15.xlsx --fecha 2026-10-15
```

Tablero interactivo cifrado para compartir (un solo HTML, se abre con contraseña en cualquier navegador):

```bash
python3 correr.py datos/Registro_General_2026.xlsx --fecha 2026-10-02 --tablero --clave "<contraseña>"
```

Si no se pasa `--clave` (ni la variable `CLAVE_TABLERO`), se genera una contraseña aleatoria y se muestra una sola vez
(`--sin-clave` lo genera en claro). El v1 lee los hallazgos y las preguntas de `salidas/<fecha>/notas_tablero.json`
(`{"hallazgos": [...], "preguntas": [...]}`); con `actualizar.py` ese archivo se regenera desde
`salidas/notas_manuales.json`, que es donde se editan. Con `--tablero-v2` se genera además el tablero v2
(`tablero_v2_datos.json`, `validaciones.json` y el HTML); lee `salidas/notas_manuales.json` si existe. Ninguno de los
dos tableros incluye estimaciones de ganancia.

Después, pedile a Claude Code "el informe de la semana" (skill `informe-semanal`) o lanzá el agente
`asesor-financiero` sobre la carpeta de salida.

## Análisis incluidos

1. Ranking de clientes · 2. Altas, recurrentes y perdidos · 3. Cliente ↔ operador ·
4. Spread de USD billete · 5. Margen del circuito Transfer → USDT · 6. Comisiones ·
7. Cheques · 8. Evolución por producto · 9. Día de la semana · 10. Tamaño de operaciones ·
11. Calidad de carga por operador · 12. Posición por moneda y efecto del tipo de cambio ·
13. Pendientes y cuentas corrientes · 14. Costo del fondeo · 15. Gastos ·
y el resultado estimado mensual.
