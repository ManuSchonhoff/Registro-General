# Registro General: análisis y asesor financiero

Herramientas para analizar el Registro General de la financiera (Excel exportado de Google Sheets)
y generar cada semana un informe del agente asesor.

## Estructura

```
config.json                      cotizaciones y criterios (editable)
correr.py                        corre todo: lee el Excel → análisis → salidas
registro/
  leer.py                        lectura de hojas semanales, pendientes, saldos, cheques, inversores
  analisis.py                    los 15 análisis + resultado estimado
  exportar.py                    Excel, metricas.json y resumen para el asesor
docs/
  contexto_negocio.md            cómo funciona el negocio y la planilla
  metodologia.md                 cómo se calcula cada número y sus límites
  notas_duenos.md                (opcional) respuestas de los dueños a preguntas del asesor
.claude/agents/asesor-financiero.md   definición del agente asesor
.claude/skills/informe-semanal/       rutina semanal (pipeline + asesor)
datos/      (no se versiona)     Excels del registro
salidas/    (no se versiona)     resultados por fecha
```

## Uso

```bash
pip install openpyxl pandas
python3 correr.py datos/Registro_General_2026.xlsx --fecha 2026-10-02
```

Después, pedile a Claude Code "el informe de la semana" (skill `informe-semanal`) o lanzá el agente
`asesor-financiero` sobre la carpeta de salida.

## Análisis incluidos

1. Ranking de clientes · 2. Altas, recurrentes y perdidos · 3. Cliente ↔ operador ·
4. Spread de USD billete · 5. Margen del circuito Transfer → USDT · 6. Comisiones ·
7. Cheques · 8. Evolución por producto · 9. Día de la semana · 10. Tamaño de operaciones ·
11. Calidad de carga por operador · 12. Posición por moneda y efecto del tipo de cambio ·
13. Pendientes y cuentas corrientes · 14. Costo del fondeo · 15. Gastos ·
y el resultado estimado mensual.
