# pelajar.py
import mysql.connector
from db_config import get_db_connection
from tkinter import *
from datetime import datetime
from PIL import Image, ImageTk

def login_pelajar():
    id_pelajar = entry_id.get()
    nama_pelajar = entry_nama.get()
    no_pc = entry_pc.get()

    if not id_pelajar or not nama_pelajar or not no_pc:
        lbl_msg.config(text="Sila isi semua medan!", bg="white", fg="red")
        return

    conn = get_db_connection()
    if not conn:
        lbl_msg.config(text="Gagal connect ke database!", bg="white", fg="red")
        return
    
    try:
        cur = conn.cursor()
        
        # Insert atau update pelajar
        cur.execute("INSERT INTO pelajar (id_pelajar, nama, masa, no_komputer) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE nama=%s, masa=%s, no_komputer=%s",
                    (id_pelajar, nama_pelajar, 0, no_pc, nama_pelajar, 0, no_pc))
        
        # Jika ada jadual Penggunaan, tambah rekod
        try:
            cur.execute("INSERT INTO Penggunaan (id_pelajar, tarikh, masa_masuk, no_komputer) VALUES (%s, %s, %s, %s)",
                        (id_pelajar, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), no_pc))
        except mysql.connector.Error:
            # Jika jadual Penggunaan belum wujud, skip
            pass
        
        conn.commit()
        cur.close()
        conn.close()
        
        lbl_msg.config(text=f"Log masuk berjaya: {nama_pelajar}", bg="white", fg="green")
        
        # Clear input fields
        entry_id.delete(0, END)
        entry_nama.delete(0, END)
        entry_pc.delete(0, END)

        # Tutup window selepas 1.5 saat untuk user tengok mesej
        root.after(1500, root.destroy)
        
    except mysql.connector.Error as err:
        lbl_msg.config(text=f"Error: {err}", bg="white", fg="red")
        if conn:
            conn.close()

# === GUI CODE ===
root = Tk()
root.title("e-LabKPD - Log Masuk Pelajar")
root.geometry("800x500")
root.resizable(False, False)

# === Tambah Background ===
try:
    bg_img = Image.open("background.jpg")
    bg_img = bg_img.resize((800, 500))
    bg_photo = ImageTk.PhotoImage(bg_img)
    
    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    # Jika gambar tak jumpa, guna warna background
    root.config(bg="#E8F4F8")

# === Frame untuk form supaya tulisan jelas ===
frame = Frame(root, bg="white", padx=30, pady=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

Label(frame, text="Log Masuk Pelajar", font=("Segoe UI", 18, "bold"), bg="white", fg="#1F6AA5").pack(pady=(0, 20))

Label(frame, text="ID Pelajar", font=("Segoe UI", 11), bg="white", fg="#333333").pack(anchor="w")
entry_id = Entry(frame, font=("Segoe UI", 11), relief="flat", bg="#F4F6FA", fg="#222222", width=25)
entry_id.pack(pady=(5, 15), ipady=5, ipadx=10)

Label(frame, text="Nama Pelajar", font=("Segoe UI", 11), bg="white", fg="#333333").pack(anchor="w")
entry_nama = Entry(frame, font=("Segoe UI", 11), relief="flat", bg="#F4F6FA", fg="#222222", width=25)
entry_nama.pack(pady=(5, 15), ipady=5, ipadx=10)

Label(frame, text="No Komputer", font=("Segoe UI", 11), bg="white", fg="#333333").pack(anchor="w")
entry_pc = Entry(frame, font=("Segoe UI", 11), relief="flat", bg="#F4F6FA", fg="#222222", width=25)
entry_pc.pack(pady=(5, 15), ipady=5, ipadx=10)

Button(
    frame, 
    text="Log Masuk", 
    font=("Segoe UI", 11, "bold"),
    bg="#1F6AA5",
    fg="white",
    relief="flat",
    padx=30,
    pady=8,
    cursor="hand2",
    command=login_pelajar
).pack(pady=(10, 10))

lbl_msg = Label(frame, text="", font=("Segoe UI", 10), bg="white", fg="red")
lbl_msg.pack()

root.mainloop()