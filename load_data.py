"""
Proyecto: Deteccion de Fraude con Tarjetas de Credito
Archivo unico de Python: crea la base de datos y las tablas (si no
existen), carga los datos historicos del CSV (si la tabla esta vacia),
y permite registrar consultas nuevas en tiempo real.
Las credenciales se leen desde el archivo .env (no se escriben aqui
directamente, por seguridad).
"""
 
import os
import random
import pyodbc
import pandas as pd
from dotenv import load_dotenv
 
load_dotenv()
 

# 1. Configuracion de conexion

SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_DATABASE")
USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
 
CSV_PATH = "data/raw/creditcard.csv"
 
CONNECTION_STRING_MASTER = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    "DATABASE=master;"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)
 
CONNECTION_STRING_DB = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
)
 

# 2. Crear la base de datos (si no existe)

print(f"Verificando/creando base de datos '{DATABASE}'...")
 
conexion_master = pyodbc.connect(CONNECTION_STRING_MASTER, autocommit=True)
cursor_master = conexion_master.cursor()
 
cursor_master.execute(f"""
    IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{DATABASE}')
    BEGIN
        CREATE DATABASE {DATABASE};
    END
""")
 
conexion_master.close()
print("Base de datos lista.")
 

# 3. Crear las tablas (si no existen)

conexion = pyodbc.connect(CONNECTION_STRING_DB, autocommit=True)
cursor = conexion.cursor()
 
print("Verificando/creando tablas...")
 
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'transactions')
    BEGIN
        CREATE TABLE transactions (
            id INT IDENTITY(1,1) PRIMARY KEY,
            [Time] FLOAT,
            V1 FLOAT, V2 FLOAT, V3 FLOAT, V4 FLOAT, V5 FLOAT,
            V6 FLOAT, V7 FLOAT, V8 FLOAT, V9 FLOAT, V10 FLOAT,
            V11 FLOAT, V12 FLOAT, V13 FLOAT, V14 FLOAT, V15 FLOAT,
            V16 FLOAT, V17 FLOAT, V18 FLOAT, V19 FLOAT, V20 FLOAT,
            V21 FLOAT, V22 FLOAT, V23 FLOAT, V24 FLOAT, V25 FLOAT,
            V26 FLOAT, V27 FLOAT, V28 FLOAT,
            Amount FLOAT,
            Class INT
        );
    END
""")
 
cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'consultas_predicciones')
    BEGIN
        CREATE TABLE consultas_predicciones (
            id INT IDENTITY(1,1) PRIMARY KEY,
            fecha_hora DATETIME DEFAULT GETDATE(),
            amount FLOAT,
            prediccion INT,
            probabilidad FLOAT,
            origen VARCHAR(50) DEFAULT 'VS Code'
        );
    END
""")
 
print("Tablas listas.")
 

# 4. Cargar los datos historicos (solo si la tabla esta vacia)

cursor.execute("SELECT COUNT(*) FROM transactions")
total_actual = cursor.fetchone()[0]
 
if total_actual == 0:
    print("La tabla esta vacia. Cargando datos del CSV...")
    data = pd.read_csv(CSV_PATH)
    print(f"Filas leidas del CSV: {len(data):,}")
 
    query_insertar_transaccion = """
        INSERT INTO transactions (
            [Time], V1, V2, V3, V4, V5, V6, V7, V8, V9, V10,
            V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
            V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
 
    contador = 0
    for indice, fila in data.iterrows():
        cursor.execute(query_insertar_transaccion, tuple(fila))
        contador = contador + 1
        if contador % 20000 == 0:
            print(f"  {contador:,} filas insertadas hasta ahora...")
 
    conexion.commit()
    print(f"Carga completada: {contador:,} filas insertadas.")
else:
    print(f"La tabla ya tiene {total_actual:,} filas, no se vuelve a cargar.")
 

# 5. Consulta en tiempo real (registrar una prediccion nueva)

print("\n" + "=" * 50)
print(" Registro de consulta en tiempo real")
print("=" * 50)
 
seguir_consultando = "s"
 
while seguir_consultando == "s":
    monto_texto = input("\nIngresa el monto de la transaccion a consultar: ")
 
    try:
        monto = float(monto_texto)
    except ValueError:
        print("Monto invalido, se usara 100.00 por defecto.")
        monto = 100.00
 
    # NOTA: por ahora la prediccion se simula de forma aleatoria.
    # Cuando el modelo de Machine Learning este entrenado se realizará ahí el proceso.
    probabilidad = round(random.uniform(0, 1), 4)
    if probabilidad >= 0.5:
        prediccion = 1
    else:
        prediccion = 0
 
    print(f"Monto consultado: {monto}")
    if prediccion == 1:
        print("Resultado: FRAUDE PROBABLE")
    else:
        print("Resultado: LEGITIMA")
    print(f"Probabilidad de fraude: {probabilidad * 100:.2f}%")
 
    cursor.execute(
        """
        INSERT INTO consultas_predicciones (amount, prediccion, probabilidad, origen)
        VALUES (?, ?, ?, ?)
        """,
        (monto, prediccion, probabilidad, "VS Code")
    )
    conexion.commit()
    print("Consulta guardada en la base de datos.")
 
    seguir_consultando = input("\nQuieres registrar otra consulta? (s/n): ").lower()
 

# 6. Cerrar conexion

cursor.close()
conexion.close()
print("\nProceso finalizado.")