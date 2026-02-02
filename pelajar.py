# pelajar.py
import mysql.connector
from db_config import get_db_connection
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk

def login_pelajar():
    id_pelajar = entry_id.get()
    nama_pelajar = entry_nama.get()
    no_pc = entry_pc.get()
    masa_val = entry_masa.get()

    if not id_pelajar or not nama_pelajar or not no_pc or not masa_val:
        lbl_msg.config(text="Sila isi semua medan!", bg="white", fg="red")
        messagebox.showwarning("Amaran", "Sila isi semua medan!", parent=root)
        return

    try:
        masa_int = int(masa_val)
        if masa_int < 0:
            raise ValueError("Masa negatif")
    except ValueError:
        lbl_msg.config(text="Masa mesti nombor (24jam)!", bg="white", fg="red")
        messagebox.showerror("Error", "Masa mesti nombor (24jam)!", parent=root)
        return

    conn = get_db_connection()
    if not conn:
        lbl_msg.config(text="Gagal connect ke database!", bg="white", fg="red")
        messagebox.showerror("Error", "Gagal connect ke database!", parent=root)
        return
    
    try:
        cur = conn.cursor()
        
                # Dapatkan tarikh semasa
        tarikh_sekarang = datetime.now().strftime('%Y-%m-%d')
        
        # Insert atau update pelajar dengan masa dan tarikh
        cur.execute(
            "INSERT INTO pelajar (id_pelajar, nama, masa, no_komputer, tarikh) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE nama=%s, masa=%s, no_komputer=%s, tarikh=%s",
            (id_pelajar, nama_pelajar, masa_int, no_pc, tarikh_sekarang,
             nama_pelajar, masa_int, no_pc, tarikh_sekarang)
        )

        conn.commit()
        cur.close()
        conn.close()

        # Clear input fields
        entry_id.delete(0, END)
        entry_nama.delete(0, END)
        entry_pc.delete(0, END)
        entry_masa.delete(0, END)

        # Tunjukkan mesej dalam form
        lbl_msg.config(text=f"Log masuk berjaya: {nama_pelajar}", bg="white", fg="green")
        
        # Tunjukkan popup "Berjaya masukkan rekod"
        messagebox.showinfo(
            "Berjaya", 
            f"Berjaya masukkan rekod!\n\nNama: {nama_pelajar}\nID: {id_pelajar}\nNo Komputer: {no_pc}\nMasa: {masa_int} jam\nTarikh: {tarikh_sekarang}",
            parent=root
        )
        
        # Tutup window selepas 1.5 saat
        root.after(1500, root.destroy)
        
    except mysql.connector.Error as err:
        lbl_msg.config(text=f"Error: {err}", bg="white", fg="red")
        messagebox.showerror("Error", f"Gagal masukkan rekod:\n{err}", parent=root)
        if conn:
            conn.close()

# === GUI CODE ===
root = Tk()
root.title("e-LabKPD - Log Masuk Pelajar")
root.geometry("1300x750")
root.resizable(False, False)

# === Tambah Background ===
try:
    bg_img = Image.open("background.jpg")
    bg_img = bg_img.resize((1300, 750))
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

Label(frame, text="ID Pelajar(Angka Giliran)", font=("Segoe UI", 11), bg="white", fg="#333333").pack(anchor="w")
entry_id = Entry(frame, font=("Segoe UI", 11), relief="flat", bg="#F4F6FA", fg="#222222", width=25)
entry_id.pack(pady=(5, 15), ipady=5, ipadx=10)

Label(frame, text="Nama Pelajar", font=("Segoe UI", 11), bg="white", fg="#333333").pack(anchor="w")
entry_nama = Entry(frame, font=("Segoe UI", 11), relief="flat", bg="#F4F6FA", fg="#222222", width=25)
entry_nama.pack(pady=(5, 15), ipady=5, ipadx=10)

Label(frame, text="Masa (24jam)", font=("Segoe UI", 11), bg="white", fg="#333333").pack(anchor="w")
entry_masa = Entry(frame, font=("Segoe UI", 11), relief="flat", bg="#F4F6FA", fg="#222222", width=25)
entry_masa.pack(pady=(5, 15), ipady=5, ipadx=10)

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