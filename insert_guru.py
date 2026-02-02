# insert_guru.py
from db_config import get_db_connection

conn = get_db_connection()
if conn:
    cur = conn.cursor()
    
    # Insert data admin ke table guru
    # Format: (id_guru, nama, password)
    # id_guru mesti 12 digit nombor
    # password maksimum 6 aksara
    
    cur.execute("""
        INSERT INTO guru (id_guru, nama, password) 
        VALUES (%s, %s, %s)
    """, (202245, 'admin', 'admin01'))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Data admin berjaya ditambah ke table guru!")
    print("   ID: 202245")
    print("   Nama: admin")
    print("   Password: admin01")
else:
    print("❌ Gagal connect ke database!")