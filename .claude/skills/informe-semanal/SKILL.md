---
name: informe-semanal
description: Rutina semanal completa sobre el Registro General. Corre el pipeline de análisis sobre el Excel nuevo y después el agente asesor-financiero, que escribe el informe. Usar cuando pidan "el informe de la semana", "correr el análisis" o suban un Registro General nuevo.
---

# Informe semanal

1. **Ubicar el Excel.** Si el usuario subió uno, copialo a `datos/` (carpeta fuera de git). Si no,
   usá el más reciente de `datos/`.
2. **Revisar cotizaciones.** Si el usuario pasó cotizaciones, cargalas en `config.json`
   (`cotizaciones.ars_unica` o `ars_por_semana`, `eur_en_usd`, `usdt_en_usd`) antes de correr.
3. **Correr el pipeline:**
   ```bash
   python3 correr.py datos/<archivo>.xlsx --fecha AAAA-MM-DD
   ```
   Genera `salidas/AAAA-MM-DD/` con el Excel de análisis, `metricas.json`,
   `resumen_para_asesor.md` y `datos/*.csv`. Tarda alrededor de 1 minuto.
4. **Revisar antes de seguir.** Mirá el "Resultado estimado mensual" y las métricas de
   `metricas.json`. Si algo es absurdo (por ejemplo, un mes con un valor 10 veces mayor al resto),
   buscá la causa en los CSV antes de pasárselo al asesor.
5. **Correr el asesor.** Lanzá el agente `asesor-financiero` indicándole la carpeta
   `salidas/AAAA-MM-DD/`. Si la sesión no lo tiene registrado, usá un agente general con el
   contenido de `.claude/agents/asesor-financiero.md` como instrucciones.
6. **Tablero para compartir (opcional):** si piden algo para mandarle a un socio, agregá
   `--tablero --clave "<contraseña>"` a `correr.py`. Genera `Tablero_Financiera_<fecha>.html` cifrado.
   La contraseña se comunica por un canal distinto al del archivo. El tablero no incluye estimaciones
   de ganancia.
7. **Entregar** al usuario `informe_asesor.md` y `Analisis_Registro_General.xlsx`, con un resumen
   corto. Las respuestas de los dueños a las "Preguntas" del informe se guardan en
   `docs/notas_duenos.md` para la próxima corrida.

Los datos y las salidas tienen nombres y montos de clientes: **no se suben al repositorio**
(`datos/` y `salidas/` están en `.gitignore`).
