# db_config.py
import mysql.connector

def get_db_connection():
    """Fungsi untuk connect ke MySQL database"""
    try:
        conn = mysql.connector.connect(
            # host="103.191.76.189",      # atau "localhost"
            # user="kpdkvdsa_25ue-labkpd",           # ← TUKAR INI
            # password=".@5gBul0h#!",           # ← TUKAR INI
            # database="kpdkvdsa_25e-labkpd"   # nama database
            host="localhost",      # atau "localhost"
            user="root",           # ← TUKAR INI
            password="",           # ← TUKAR INI
            database="elabkpd"   # nama database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None