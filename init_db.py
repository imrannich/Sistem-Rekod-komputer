import sqlite3

# Sambung ke DB (akan auto cipta kalau tak wujud)
conn = sqlite3.connect("elabkpd.db")
cur = conn.cursor()

# Jadual Pelajar
cur.execute("""
CREATE TABLE IF NOT EXISTS Pelajar (
    id_pelajar TEXT PRIMARY KEY,
    nama TEXT NOT NULL
)
""")

# Jadual Rekod Penggunaan
cur.execute("""
CREATE TABLE IF NOT EXISTS Penggunaan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pelajar TEXT,
    tarikh TEXT,
    masa_masuk TEXT,
    masa_keluar TEXT,
    no_komputer TEXT,
    FOREIGN KEY(id_pelajar) REFERENCES Pelajar(id_pelajar)
)
""")

# Jadual Admin
cur.execute("""
CREATE TABLE IF NOT EXISTS Admin (
    id_admin TEXT PRIMARY KEY,
    nama TEXT,
    kata_laluan TEXT
)
""")

# Tambah contoh admin
cur.execute("INSERT OR IGNORE INTO Admin VALUES (?,?,?)", ("admin01", "Guru Besar", "12345"))

conn.commit()
# Line 37 - selepas create table Admin (atau selepas create table guru)
# Tambah contoh guru
cur.execute("INSERT IGNORE INTO guru (id_guru, nama, password) VALUES (%s, %s, %s)", 
            (202245, 'admin', 'admin01'))
conn.close()
print("Database berjaya dicipta!")
