import mysql.connector
import os

from dotenv import load_dotenv
load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME", "railway"),
    )


def get_cursor(conn):
    return conn.cursor(dictionary=True)
