# 🌾 Módulo de Producción – ERP Infopalm

## 🎯 Objetivo
Registrar, analizar y reportar la **producción de fruta fresca (RFF)** por lote, proyecto o plantación, integrando la información con tasas de extracción, precios del mercado (FEP) y tasas de cambio para obtener una **visión económica y productiva diaria, mensual y anual**.

---

## 🔑 Funciones principales

1. **Registro de producción diaria**
   - Captura por fecha, lote, bloque o frente de cosecha.
   - Campos: fecha, lote, kg de fruto, número de racimos, cuadrilla, transporte, observaciones.
   - Integración con la estructura de plantación (`LandParcelModel`, `LandProjectModel`).

2. **Cálculo de rendimiento y eficiencia**
   - Rendimiento (kg/ha) y racimos/palma.
   - Comparativo con metas históricas y promedio de la finca.
   - Análisis por lote, supervisor o zona productiva.

3. **Conversión económica**
   - Conversión de producción a valor económico mediante:
     - **Tasa de extracción (% aceite del fruto).**
     - **Precio FEP (COP/kg de aceite).**
     - **Tasa de cambio COP/USD.**
   - Cálculo automático de:
     - Aceite equivalente (kg).
     - Valor en COP y USD.
     - Ingreso estimado por hectárea.

4. **Boletín informativo diario**
   - Reporte automático tipo “boletín gerencial” con:
     - Datos del día anterior.  
     - Producción total por lote o proyecto.  
     - Valor económico estimado.  
     - Tendencias frente a promedio semanal o mensual.  
   - Exportable a Excel, PDF o Power BI.

5. **Análisis histórico**
   - Acumulados por día, mes, trimestre o año.
   - Comparativo entre lotes, proyectos o fincas.
   - Visualización gráfica mediante dashboards Power BI.

6. **Validación de datos**
   - Detección automática de inconsistencias (fechas, valores fuera de rango).
   - Registro de errores o advertencias antes de consolidar datos.

---

## 🧩 Estructura de datos

| Tabla | Descripción |
|-------|--------------|
| `ProductionTable` | Registro de producción diaria: fecha, lote, kg, racimos, cuadrilla. |
| `WeightTicketTable`| Registro de movimientos de bascula diarios recibidos de Entrepalmas|
| `ExtractionRateTable` | Tasa de extracción mensual (% aceite). |
| `FEPPriceTable` | Precio FEP (COP/kg aceite) con vigencia mensual. |
| `ExchangeRateTable` | Tasa representativa del mercado (COP/USD). |
| `ProductionSummaryView` | Vista agregada con indicadores productivos y económicos. |

---

## 🧮 Fórmulas clave

```text
Aceite equivalente (kg) = Producción fruta × (Tasa de extracción / 100)
Valor COP = Aceite equivalente × Precio FEP
Valor USD = Valor COP / Tasa de cambio
Rendimiento = kg fruta / ha
```