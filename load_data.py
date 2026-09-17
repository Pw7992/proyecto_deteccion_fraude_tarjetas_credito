"""
Script de carga de datos
Lee el CSV de Kaggle (creditcard.csv) e inserta los datos en la tabla
`transactions` de SQL Server, usando pyodbc y cursor.
Conexión (SERVER y DATABASE)
"""

import os
import pandas as pd
from conexion_bd import conectar_bd

CSV_PATH = "data/raw/creditcard.csv"

# 1. Se lee el archivo csv
print("Leyendo el archivo CSV...")
data = pd.read_csv(CSV_PATH)
print(f"Filas leidas: {len(data):,}")
print(f"Columnas: {list(data.columns)}")


# 2. Verificaciones previas a cargar los datos

print("\nVerificaciones previas a la carga:")
print(f"- Valores nulos por columna:\n{data.isnull().sum().sum()} nulos en total")
print(f"- Duplicados: {data.duplicated().sum()} filas duplicadas")
print(f"- Proporcion de fraude: {data['Class'].mean() * 100:.3f}%")


# 3. Conexion a la base de datos
conexion, cursor = conectar_bd()

if conexion:
    try:
        # Arma la lista de columnas dinamicamente (Time, V1..V28, Amount, Class)
        columnas = list(data.columns)
        columnas_sql = ", ".join([f"[{c}]" for c in columnas])
        placeholders = ", ".join(["?"] * len(columnas))

        query_insert = f"INSERT INTO transactions ({columnas_sql}) VALUES ({placeholders})"

        # fast_executemany acelera mucho la insercion de miles de filas
        cursor.fast_executemany = True

        print("\nInsertando datos en la tabla 'transactions' (esto puede tardar unos minutos)...")
        datos_a_insertar = [tuple(fila) for fila in data.to_numpy()]
        cursor.executemany(query_insert, datos_a_insertar)
        conexion.commit()

        print("¡Carga completada!")


        # 4. Validación final
        cursor.execute("SELECT COUNT(*) FROM transactions")
        total_filas = cursor.fetchone()[0]
        print(f"\nFilas ahora en la tabla 'transactions': {total_filas:,}")
        print("Verifica que este numero coincida con el de filas leidas del CSV arriba.")

    except Exception as error:
        print("Ocurrio un error durante la insercion:", error)

    finally:
        cursor.close()
        conexion.close()