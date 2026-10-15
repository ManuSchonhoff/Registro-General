# Registro General

Análisis del registro de operaciones de una financiera / casa de cambio (Excel semanal) y agente
asesor que escribe un informe para los dueños.

- Antes de tocar el análisis, leé `docs/contexto_negocio.md` y `docs/metodologia.md`.
- Pipeline: `python3 correr.py datos/<excel>.xlsx --fecha AAAA-MM-DD` → `salidas/AAAA-MM-DD/`.
- Cotizaciones y criterios en `config.json`, nunca hardcodeados en el código.
- Rutina semanal: skill `informe-semanal`. Agente: `.claude/agents/asesor-financiero.md`.
- `datos/` y `salidas/` tienen información de clientes: nunca se suben a git.
- Respuestas en castellano rioplatense; montos en USD salvo que se indique otra moneda.
- Consultas puntuales (liquidaciones de cuentas, búsqueda de pagos, saldos de un cliente): responder con una
  tabla en el chat (semana, fila, Ope, movimiento, monto, saldo acumulado). Generar archivo solo si lo piden.
- Para actualizar los datos conviene recibir el Registro General completo (un solo Excel), no hojas sueltas.
