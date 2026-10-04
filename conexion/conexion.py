import os
import psycopg2
from psycopg2.extras import RealDictCursor


def conectar_postgresql():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(
            database_url,
            cursor_factory=RealDictCursor
        )

    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "proyecto_tic"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "7777"),
        cursor_factory=RealDictCursor
    )