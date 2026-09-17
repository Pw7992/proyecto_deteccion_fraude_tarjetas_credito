# -*- coding: utf-8 -*-
"""
Herramienta de DEMO EN VIVO para la exposicion.
Permite ingresar un monto nuevo en tiempo real, generar una prediccion
y guardarla en la tabla `consultas_predicciones` de SQL Server, sin
depender de internet ni de Streamlit Cloud. Mismo estilo de conexion
(pyodbc + cursor) visto en clase.

Uso durante la exposicion:
    python demo_en_vivo.py

Nota: hasta que el modelo real (Fase 4, modelo_fraude.pkl) este
entrenado, este script SIMULA la prediccion de forma aleatoria.
En cuanto el modelo exista, se reemplaza la funcion generar_prediccion
por la prediccion real; el resto del script no cambia.
"""

import os
import random
import pickle
import pandas as pd
from datetime import datetime
from conexion_bd import conectar_bd

CSV_PATH = "data/raw/creditcard.csv"
MODEL_PATH = "models/modelo_fraude.pkl"


def cargar_transaccion_base():
    """Toma una fila real y aleatoria del dataset para usar sus
    valores V1-V28 (anonimizados), que no tiene sentido escribir a mano."""
    data = pd.read_csv(CSV_PATH)
    fila = data.sample(1).iloc[0]
    return fila


def generar_prediccion(fila, nuevo_amount):
    """
    Genera la prediccion de fraude.
    - Si ya existe un modelo entrenado (Fase 4), lo usa de verdad.
    - Si todavia no existe, simula un resultado aleatorio (solo para
      probar la mecanica de la demo antes de tener el modelo real).
    """
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            modelo = pickle.load(f)

        entrada = fila.drop(labels=["Time", "Amount", "Class"]).to_dict()
        entrada["Amount"] = nuevo_amount
        entrada_df = pd.DataFrame([entrada])

        probabilidad = modelo.predict_proba(entrada_df)[0][1]
        prediccion = 1 if probabilidad >= 0.5 else 0
        return prediccion, round(probabilidad, 4)
    else:
        print("\n[Aviso] Todavia no existe el modelo entrenado (models/modelo_fraude.pkl).")
        print("Se genera un resultado SIMULADO solo para probar la demo.\n")
        probabilidad = round(random.uniform(0, 1), 4)
        prediccion = 1 if probabilidad >= 0.5 else 0
        return prediccion, probabilidad


def insertar_en_sql(cursor, conexion, amount, prediccion, probabilidad):
    query_insert = """
        INSERT INTO consultas_predicciones (fecha_hora, amount, prediccion, probabilidad, origen)
        VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(
        query_insert,
        (datetime.now(), amount, prediccion, probabilidad, "Demo en vivo (VS Code)")
    )
    conexion.commit()


def main():
    print("=" * 55)
    print(" DEMO EN VIVO: Deteccion de Fraude")
    print("=" * 55)

    monto_input = input("\nIngresa el monto de la transaccion a consultar (ej. 150.50): ")
    try:
        nuevo_amount = float(monto_input)
    except ValueError:
        print("Monto invalido, se usara 100.00 por defecto.")
        nuevo_amount = 100.00

    fila_base = cargar_transaccion_base()
    prediccion, probabilidad = generar_prediccion(fila_base, nuevo_amount)

    print("\n" + "-" * 55)
    print(f"Monto consultado:       €{nuevo_amount:,.2f}")
    print(f"Resultado del modelo:   {'FRAUDE PROBABLE' if prediccion == 1 else 'LEGITIMA'}")
    print(f"Probabilidad de fraude: {probabilidad * 100:.2f}%")
    print("-" * 55)

    conexion, cursor = conectar_bd()
    if conexion:
        try:
            insertar_en_sql(cursor, conexion, nuevo_amount, prediccion, probabilidad)
            print("\nConsulta guardada en la base de datos (tabla consultas_predicciones).")
            print("Ve a Power BI y presiona 'Actualizar' para verla reflejada en la Pagina 4.\n")
        except Exception as error:
            print("Ocurrio un error al guardar la consulta:", error)
        finally:
            cursor.close()
            conexion.close()


if __name__ == "__main__":
    main()
