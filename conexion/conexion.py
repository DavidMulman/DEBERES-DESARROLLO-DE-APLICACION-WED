import mysql.connector
import os


def conectar_mysql():
    conexion = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE", "proyecto_tic"),
        port=int(os.getenv("MYSQL_PORT", "3306"))
    )

    return conexion