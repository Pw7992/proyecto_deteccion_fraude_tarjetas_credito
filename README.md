# Detección de Fraude con Tarjetas de Crédito

## Contexto y pregunta de negocio

¿Cómo se comporta el fraude, se puede anticipar, y qué tan sensible debe ser
el sistema que lo detecta?

Este proyecto responde esa pregunta en 3 capas:

1. **Descriptivo/Diagnóstico:** ¿cuándo y en qué montos se concentra el fraude?
2. **Predictivo:** ¿se puede predecir si una transacción es fraudulenta?
3. **Prescriptivo:** ¿qué umbral de sensibilidad minimiza el riesgo sin
   afectar a clientes legítimos?

## Fuente de datos

- **Dataset:** Credit Card Fraud Detection (Machine Learning Group – ULB)
- **Link:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- 284,807 transacciones de tarjetahabientes europeos (septiembre 2013),
  492 fraudes (0.17%). Variables V1–V28 anonimizadas por PCA por
  confidencialidad bancaria.

## Stack tecnológico

| Herramienta | Uso en el proyecto |
|---|---|
| SQL Server Management Studio | Base de datos, tablas `transactions` y `consultas_predicciones` |
| Python | Carga de datos a SQL, y motor de la app de Streamlit |
| Google Colab | Limpieza, análisis exploratorio y modelo de Machine Learning |
| Power BI | Dashboard de 4 páginas: Panorama, Modelo, Simulador, Consultas en Vivo |
| Streamlit | Aplicación pública para predicción de nuevas transacciones |

## Estructura del repositorio

```
data/raw/              -> CSV original de Kaggle
data/processed/        -> Datos limpios y predicciones exportadas
sql/                   -> Scripts de creación y carga de la base de datos
notebooks/             -> Notebooks de Colab (EDA, feature engineering, modelo)
models/                -> Modelo entrenado (.pkl)
dashboards/            -> Archivo .pbix de Power BI
app/                   -> Código de la aplicación Streamlit
```

## Resultados clave

*(completar al finalizar la Fase 2 y 4, con los hallazgos del EDA y las
métricas del modelo)*

## Enlaces

- App en Streamlit: *(completar en la Fase 6)*
- Dashboard de Power BI: *(adjuntar archivo o captura)*

## Limitaciones y trabajo futuro

- Las variables V1–V28 están anonimizadas por PCA; no representan
  características de negocio interpretables directamente.
- El dataset corresponde a transacciones de 2013; el análisis es
  metodológico, no una recomendación operativa actual.
# proyecto_deteccion_fraude_tarjetas_credito
Detección de fraude en transacciones con tarjetas de crédito usando SQL Server, Python y Machine Learning, con dashboard interactivo en Power BI y app de predicción en vivo desplegada con Streamlit.
