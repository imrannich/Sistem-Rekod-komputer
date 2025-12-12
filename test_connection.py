# test_connection.py
from db_config import get_db_connection

print("Sedang test connection ke MySQL...")
print("-" * 40)

conn = get_db_connection()

if conn:
    print("✅ Berjaya connect ke MySQL!")
    print(f"✅ Database: elabkpd")
    
    # Test query untuk check jadual
    try:
        cur = conn.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        
        if tables:
            print(f"✅ Jadual yang wujud: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("⚠️  Tiada jadual dalam database")
        
        cur.close()
        conn.close()
        print("\n✅ Connection test berjaya!")
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.close()
else:
    print("❌ Gagal connect ke MySQL!")
    print("\nSila check:")
    print("1. MySQL service running dalam XAMPP?")
    print("2. Username/password dalam db_config.py betul?")
    print("3. Database 'elabkpd' sudah wujud?")