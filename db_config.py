# db_config.py
import mysql.connector

def get_db_connection():
    """Fungsi untuk connect ke MySQL database"""
    try:
        conn = mysql.connector.connect(
            host="localhost",      # atau "localhost"
            user="root",           # ← TUKAR INI
            password="",           # ← TUKAR INI
            database="elabkpd"     # nama database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None