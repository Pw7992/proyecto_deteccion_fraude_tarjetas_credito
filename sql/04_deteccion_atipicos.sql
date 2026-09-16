-- ============================================================
-- Fase 1 (ampliada): Detección de valores atípicos (outliers)
-- Proyecto: Detección de Fraude con Tarjetas de Crédito
-- ============================================================
 
USE FraudDetectionDB;
GO
 
-- Método: regla de 3 desviaciones estándar sobre la media.
-- Cualquier transacción cuyo Amount esté a más de 3 desviaciones
-- estándar de la media se marca como atípica.
-- (Funciona en cualquier versión de SQL Server; PERCENTILE_CONT/DISC
-- solo está disponible desde SQL Server 2022 en adelante.)
 
-- Variables para guardar el conteo y los límites del umbral
DECLARE @total_atipicos INT;
DECLARE @media FLOAT, @desviacion FLOAT;
DECLARE @limite_superior FLOAT, @limite_inferior FLOAT;
 
SELECT
    @media = AVG(Amount),
    @desviacion = STDEV(Amount)
FROM transactions;
 
SET @limite_superior = @media + 3 * @desviacion;
SET @limite_inferior = @media - 3 * @desviacion;
 
SELECT @total_atipicos = COUNT(*)
FROM transactions
WHERE Amount > @limite_superior OR Amount < @limite_inferior;
 
-- Mensaje condicional según el resultado
IF @total_atipicos = 0
BEGIN
    PRINT 'No se encontraron valores atipicos en la columna Amount (umbral: media +/- 3 desviaciones estandar).';
END
ELSE
BEGIN
    PRINT CONCAT('Se encontraron ', @total_atipicos, ' transacciones atipicas en el monto (Amount), fuera del rango [',
                  ROUND(@limite_inferior, 2), ' , ', ROUND(@limite_superior, 2), ']. Detalle de las 20 mas extremas a continuacion:');
 
    SELECT TOP 20
        id, Amount, Class,
        @media AS media_general,
        @desviacion AS desviacion_general
    FROM transactions
    WHERE Amount > @limite_superior OR Amount < @limite_inferior
    ORDER BY Amount DESC;
END
GO
 
-- Nota importante para tu documentación/presentación:
-- NO se eliminan estos atípicos. En detección de fraude, los montos
-- inusualmente altos (o inusualmente bajos, típicos de "pruebas" de
-- tarjetas robadas) suelen ser justamente la señal de interés, no ruido
-- a descartar. Eliminarlos podría borrar parte del fraude real.