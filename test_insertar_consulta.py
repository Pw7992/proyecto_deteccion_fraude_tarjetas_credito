# -*- coding: utf-8 -*-
"""
Script de PRUEBA (no es la app final de Streamlit).
Verifica que la conexion de escritura hacia la tabla
`consultas_predicciones` funciona correctamente, simulando
una prediccion antes de tener el modelo real entrenado.
Mismo estilo de conexion (pyodbc + cursor) visto en clase.
"""

import random
from datetime import datetime
from conexion_bd import conectar_bd

conexion, cursor = conectar_bd()

if conexion:
    try:
        # ------------------------------------------------------------
        # SIMULACION de una "consulta nueva" (luego lo hara el modelo real)
        # ------------------------------------------------------------
        amount_simulado = round(random.uniform(1, 500), 2)
        prediccion_simulada = random.choice([0, 1])  # 0 = legitima, 1 = fraude
        probabilidad_simulada = round(random.uniform(0, 1), 4)

        print("Simulando una consulta nueva:")
        print(f"- Monto: {amount_simulado}")
        print(f"- Prediccion: {'Fraude' if prediccion_simulada == 1 else 'Legitima'}")
        print(f"- Probabilidad: {probabilidad_simulada}")

        # ------------------------------------------------------------
        # INSERTAR en la tabla consultas_predicciones
        # ------------------------------------------------------------
        query_insert = """
            INSERT INTO consultas_predicciones (fecha_hora, amount, prediccion, probabilidad, origen)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(
            query_insert,
            (datetime.now(), amount_simulado, prediccion_simulada, probabilidad_simulada,
             "Prueba desde VS Code (sin modelo real aun)")
        )
        conexion.commit()
        print("\n¡Insercion de prueba completada!")

        # ------------------------------------------------------------
        # VERIFICACION: mostrar las ultimas 5 consultas registradas
        # ------------------------------------------------------------
        cursor.execute("SELECT TOP 5 * FROM consultas_predicciones ORDER BY id DESC")
        print("\nUltimas consultas registradas en la tabla:")
        for fila in cursor.fetchall():
            print(fila)

    except Exception as error:
        print("Ocurrio un error durante la insercion:", error)

    finally:
        cursor.close()
        conexion.close()
