# -*- coding: utf-8 -*-
"""
Modulo de conexion a la base de datos.
"""

import os
import pyodbc as db
from dotenv import load_dotenv

load_dotenv()

SERVIDOR = os.getenv("DB_SERVER")
BASE_DE_DATOS = os.getenv("DB_DATABASE")
DRIVER = "{ODBC Driver 17 for SQL Server}"
USUARIO = os.getenv("DB_USERNAME")
CONTRASENA = os.getenv("DB_PASSWORD")


def driver_seguro(servidor, base_datos):
    return f"DRIVER={DRIVER};SERVER={servidor};DATABASE={base_datos};"


def conectar_bd(servidor=SERVIDOR, base_datos=BASE_DE_DATOS, usuario=USUARIO, contrasena=CONTRASENA):
    if usuario and contrasena:
        cadena_conexion = (
            f"{driver_seguro(servidor, base_datos)}"
            f"UID={usuario};PWD={contrasena};"
        )
    else:
        cadena_conexion = (
            f"{driver_seguro(servidor, base_datos)}"
            f"Trusted_Connection=yes;TrustServerCertificate=yes;"
        )

    try:
        conexion = db.connect(cadena_conexion)
        cursor = conexion.cursor()
        print("Conexion Exitosa")
        return conexion, cursor
    except db.Error as error:
        print("No se pudo conectar a la Base de datos:", error)
        return None, None
