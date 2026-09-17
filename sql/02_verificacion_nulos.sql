
-- Verificación de nulos por columna

USE FraudDetectionDB;
GO

-- El script de Python ya confirmó "0 nulos en total", pero aquí lo
-- verificamos columna por columna directamente en SQL, como respaldo
-- y para tener el query documentado en el repositorio.

SELECT
    SUM(CASE WHEN [Time] IS NULL THEN 1 ELSE 0 END) AS nulos_Time,
    SUM(CASE WHEN V1 IS NULL THEN 1 ELSE 0 END)     AS nulos_V1,
    SUM(CASE WHEN V2 IS NULL THEN 1 ELSE 0 END)     AS nulos_V2,
    SUM(CASE WHEN V3 IS NULL THEN 1 ELSE 0 END)     AS nulos_V3,
    SUM(CASE WHEN V4 IS NULL THEN 1 ELSE 0 END)     AS nulos_V4,
    SUM(CASE WHEN V5 IS NULL THEN 1 ELSE 0 END)     AS nulos_V5,
    SUM(CASE WHEN V6 IS NULL THEN 1 ELSE 0 END)     AS nulos_V6,
    SUM(CASE WHEN V7 IS NULL THEN 1 ELSE 0 END)     AS nulos_V7,
    SUM(CASE WHEN V8 IS NULL THEN 1 ELSE 0 END)     AS nulos_V8,
    SUM(CASE WHEN V9 IS NULL THEN 1 ELSE 0 END)     AS nulos_V9,
    SUM(CASE WHEN V10 IS NULL THEN 1 ELSE 0 END)    AS nulos_V10,
    SUM(CASE WHEN V11 IS NULL THEN 1 ELSE 0 END)    AS nulos_V11,
    SUM(CASE WHEN V12 IS NULL THEN 1 ELSE 0 END)    AS nulos_V12,
    SUM(CASE WHEN V13 IS NULL THEN 1 ELSE 0 END)    AS nulos_V13,
    SUM(CASE WHEN V14 IS NULL THEN 1 ELSE 0 END)    AS nulos_V14,
    SUM(CASE WHEN V15 IS NULL THEN 1 ELSE 0 END)    AS nulos_V15,
    SUM(CASE WHEN V16 IS NULL THEN 1 ELSE 0 END)    AS nulos_V16,
    SUM(CASE WHEN V17 IS NULL THEN 1 ELSE 0 END)    AS nulos_V17,
    SUM(CASE WHEN V18 IS NULL THEN 1 ELSE 0 END)    AS nulos_V18,
    SUM(CASE WHEN V19 IS NULL THEN 1 ELSE 0 END)    AS nulos_V19,
    SUM(CASE WHEN V20 IS NULL THEN 1 ELSE 0 END)    AS nulos_V20,
    SUM(CASE WHEN V21 IS NULL THEN 1 ELSE 0 END)    AS nulos_V21,
    SUM(CASE WHEN V22 IS NULL THEN 1 ELSE 0 END)    AS nulos_V22,
    SUM(CASE WHEN V23 IS NULL THEN 1 ELSE 0 END)    AS nulos_V23,
    SUM(CASE WHEN V24 IS NULL THEN 1 ELSE 0 END)    AS nulos_V24,
    SUM(CASE WHEN V25 IS NULL THEN 1 ELSE 0 END)    AS nulos_V25,
    SUM(CASE WHEN V26 IS NULL THEN 1 ELSE 0 END)    AS nulos_V26,
    SUM(CASE WHEN V27 IS NULL THEN 1 ELSE 0 END)    AS nulos_V27,
    SUM(CASE WHEN V28 IS NULL THEN 1 ELSE 0 END)    AS nulos_V28,
    SUM(CASE WHEN Amount IS NULL THEN 1 ELSE 0 END) AS nulos_Amount,
    SUM(CASE WHEN Class IS NULL THEN 1 ELSE 0 END)  AS nulos_Class
FROM transactions;
GO

-- Si todas las columnas dan 0, se confirma formalmente (con evidencia en SQL,
-- no solo en el log de Python) que el dataset no requiere imputación de nulos.
