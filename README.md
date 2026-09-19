# Detección de Fraude con Tarjetas de Crédito

## Contexto y pregunta de negocio

> ¿Cómo se comporta el fraude, y qué tan bien se puede anticipar y controlar?

Este proyecto responde la pregunta en 3 niveles:

1. **Descriptivo/Diagnóstico** — ¿cuándo y en qué montos se concentra el fraude?
2. **Predictivo** — ¿se puede anticipar si una transacción nueva es fraudulenta?
3. **Prescriptivo** — ¿qué umbral de sensibilidad minimiza el riesgo sin afectar a clientes legítimos?

*Nota de transparencia: la "consulta en tiempo real" del script de Python
genera por ahora una probabilidad de forma simulada, mientras se integra
el modelo de Machine Learning entrenado en Google Colab. Esto se
documentará y actualizará una vez completado.*

## Fuente de datos

- **Dataset:** Credit Card Fraud Detection (Machine Learning Group – ULB)
- **Link:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- 284,807 transacciones de tarjetahabientes europeos (septiembre 2013), 492 fraudes (0.17%).
- Variables V1–V28 anonimizadas por PCA por confidencialidad bancaria (no representan
  características de negocio interpretables directamente).
- Tras la limpieza (eliminación de 1,081 duplicados), la base de datos final
  contiene **283,726 transacciones**.

## Stack tecnológico

| Herramienta | Uso en el proyecto |
|---|---|
| SQL Server Management Studio | Base de datos `FraudDetectionDB`, tablas `transactions` y `consultas_predicciones` |
| Python (VS Code) | Un solo archivo (`load_data.py`) que crea la BD, limpia los datos, los carga, y permite consultas en tiempo real |
| Google Colab | Limpieza adicional, análisis exploratorio y modelo de Machine Learning |
| Power BI | Dashboard de 3 páginas: Análisis, Modelo, Simulador |

## Estructura del repositorio

data/raw/ -> CSV original de Kaggle
data/processed/ -> Datos exportados para Colab
sql/ -> Scripts de verificación (nulos, duplicados, atípicos, consultas básicas)
notebooks/ -> Notebook de Colab (EDA y modelo de Machine Learning)
models/ -> Modelo entrenado (.pkl)
dashboards/ -> Archivo .pbix de Power BI
load_data.py -> Archivo único de Python (BD, limpieza, carga, consulta en tiempo real)
tema_deteccion_fraude.json -> Tema personalizado de Power BI


## Resumen técnico

- Base de datos `FraudDetectionDB` creada en SQL Server, con las tablas
  `transactions` (283,726 filas limpias) y `consultas_predicciones`.
- `load_data.py` se conecta a la base de datos y realiza ambas acciones:
  **inserta** (carga inicial + consultas en tiempo real) y **consulta**
  (lectura de las primeras filas y conteo de consultas registradas).
- Limpieza de nulos y duplicados aplicada con `pandas` antes de insertar,
  y verificada de forma independiente con scripts SQL.
- Dashboard de Power BI con 3 páginas (Análisis descriptivo, Modelo,
  Simulador), tema visual personalizado, KPIs, gráficos y slicers
  interactivos.
- Modelo de Machine Learning en Google Colab para clasificar
  transacciones como fraude/legítima (en desarrollo).

## Resultados clave

*(completar con los hallazgos del EDA y las métricas del modelo, al
finalizar el notebook de Colab)*

## Limitaciones y trabajo futuro

- Las variables V1–V28 están anonimizadas por PCA; el análisis de negocio
  se apoya en `Amount`, `Time` y `Class`, que sí son interpretables.
- El dataset corresponde a transacciones de 2013; el análisis es
  metodológico, no una recomendación operativa actual.
- La "consulta en tiempo real" usa una probabilidad simulada hasta que el
  modelo de Machine Learning esté entrenado e integrado.