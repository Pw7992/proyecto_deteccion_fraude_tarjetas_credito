-- Consultas varias

USE FraudDetectionDB;
GO

-- 1. Ver las primeras 10 transacciones
SELECT TOP 10 * FROM transactions;
GO

-- 2. Contar el total de transacciones
SELECT COUNT(*) AS total_transacciones FROM transactions;
GO

-- 3. Ver solo las transacciones marcadas como fraude
SELECT TOP 10 id, Amount, Class
FROM transactions
WHERE Class = 1;
GO

-- 4. Monto promedio de todas las transacciones
SELECT AVG(Amount) AS monto_promedio FROM transactions;
GO

-- 5. Monto maximo y minimo registrado
SELECT MAX(Amount) AS monto_maximo, MIN(Amount) AS monto_minimo
FROM transactions;
GO

-- 6. Ver el contenido de la tabla de consultas en tiempo real
SELECT * FROM consultas_predicciones;
GO

-- 7. Contar cuantas transacciones son fraude vs legitimas
SELECT Class, COUNT(*) AS cantidad
FROM transactions
GROUP BY Class;
GO
