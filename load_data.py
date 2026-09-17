"""
Script de carga de datos
Lee el CSV de Kaggle (creditcard.csv) y lo inserta en la tabla
`transactions` de SQL Server.
Ajusta la cadena de conexión (SERVER y DATABASE) según mi instalación
de SQL Server Management Studio.
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# 1. CONFIGURACIÓN - las credenciales se leen desde el archivo .env

load_dotenv()  # carga las variables definidas en .env

SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DRIVER = "ODBC+Driver+17+for+SQL+Server"  

CSV_PATH = "data/raw/creditcard.csv"   # ruta al CSV descargado de Kaggle

# Cadena de conexión con autenticación de SQL Server (usuario y contraseña)
connection_string = (
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"
    f"?driver={DRIVER}"
)


# 2. LEER EL CSV

print("Leyendo el archivo CSV...")
df = pd.read_csv(CSV_PATH)
print(f"Filas leídas: {len(df):,}")
print(f"Columnas: {list(df.columns)}")

# Verificación rápida antes de insertar
print("\nVerificaciones previas a la carga:")
print(f"- Valores nulos por columna:\n{df.isnull().sum().sum()} nulos en total")
print(f"- Duplicados: {df.duplicated().sum()} filas duplicadas")
print(f"- Proporción de fraude: {df['Class'].mean() * 100:.3f}%")


# 3. INSERTAR EN SQL SERVER

print("\nConectando a SQL Server...")
engine = create_engine(connection_string)

print("Insertando datos en la tabla 'transactions' (esto puede tardar unos minutos)...")
df.to_sql(
    "transactions",
    con=engine,
    if_exists="append",   # la tabla ya existe (creada por 01_create_tables.sql)
    index=False,
    chunksize=5000         # inserta por lotes para no saturar la conexión
)

print("¡Carga completada!")

# 4. VALIDACIÓN FINAL 
#__________________________________________________________________
with engine.connect() as conn:
    result = conn.exec_driver_sql("SELECT COUNT(*) FROM transactions").scalar()
    print(f"\nFilas ahora en la tabla 'transactions': {result:,}")
    print("Verifica que este número coincida con el de filas leídas del CSV arriba.")