-- ============================================================
--Eliminación de duplicados
--Proyecto: Detección de Fraude con Tarjetas de Crédito
-- ============================================================

USE FraudDetectionDB;
GO

-- 1. Confirmar cuántos duplicados hay ANTES de borrar
--    (dos filas se consideran duplicadas si TODAS sus columnas,
--    excepto el id autonumérico, son idénticas)
WITH duplicados AS (
    SELECT
        id,
        ROW_NUMBER() OVER (
            PARTITION BY
                [Time], V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
                V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
                V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class
            ORDER BY id
        ) AS rn
    FROM transactions
)
SELECT COUNT(*) AS filas_duplicadas_a_eliminar
FROM duplicados
WHERE rn > 1;
GO

-- 2. Eliminar los duplicados, conservando solo la primera aparición (rn = 1)
WITH duplicados AS (
    SELECT
        id,
        ROW_NUMBER() OVER (
            PARTITION BY
                [Time], V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
                V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
                V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class
            ORDER BY id
        ) AS rn
    FROM transactions
)
DELETE FROM duplicados
WHERE rn > 1;
GO

-- 3. Verificación final: el conteo debe bajar de 284,807 a ~283,726
SELECT COUNT(*) AS filas_despues_de_limpiar FROM transactions;
GO
