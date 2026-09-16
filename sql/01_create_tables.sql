-- ============================================================
-- Fase 1: Creación de base de datos y tablas
-- Proyecto: Detección de Fraude con Tarjetas de Crédito
-- ============================================================

-- 1. Crear la base de datos (ejecutar una sola vez)
CREATE DATABASE FraudDetectionDB;
GO

USE FraudDetectionDB;
GO

-- 2. Tabla principal: transacciones originales del dataset de Kaggle
CREATE TABLE transactions (
    id          INT IDENTITY(1,1) PRIMARY KEY,  -- llave primaria autonumérica
    [Time]      FLOAT,          -- segundos desde la primera transacción
    V1 FLOAT, V2 FLOAT, V3 FLOAT, V4 FLOAT, V5 FLOAT,
    V6 FLOAT, V7 FLOAT, V8 FLOAT, V9 FLOAT, V10 FLOAT,
    V11 FLOAT, V12 FLOAT, V13 FLOAT, V14 FLOAT, V15 FLOAT,
    V16 FLOAT, V17 FLOAT, V18 FLOAT, V19 FLOAT, V20 FLOAT,
    V21 FLOAT, V22 FLOAT, V23 FLOAT, V24 FLOAT, V25 FLOAT,
    V26 FLOAT, V27 FLOAT, V28 FLOAT,
    Amount      FLOAT,          -- monto de la transacción
    Class       INT             -- 1 = fraude, 0 = legítima
);
GO

-- 3. Tabla de consultas: se llenará desde Streamlit (Fase 6)
--    Queda vacía por ahora, pero la creamos ya para no tocar
--    el modelo de datos más adelante.
CREATE TABLE consultas_predicciones (
    id              INT IDENTITY(1,1) PRIMARY KEY,
    fecha_hora      DATETIME DEFAULT GETDATE(),
    amount          FLOAT,
    prediccion      INT,            -- 0 = legítima, 1 = fraude (predicho por el modelo)
    probabilidad    FLOAT,          -- probabilidad de fraude según el modelo (0 a 1)
    origen          VARCHAR(50) DEFAULT 'Streamlit demo'
);
GO

-- 4. Verificación rápida (deben aparecer las 2 tablas, ambas en 0 filas)
SELECT 'transactions' AS tabla, COUNT(*) AS filas FROM transactions
UNION ALL
SELECT 'consultas_predicciones', COUNT(*) FROM consultas_predicciones;
GO
