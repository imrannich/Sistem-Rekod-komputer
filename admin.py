# admin.py
import mysql.connector
from db_config import get_db_connection
from tkinter import *
from PIL import Image, ImageTk, ImageEnhance

def login_admin():
    user = entry_user.get()
    pwd = entry_pwd.get()

    if not user or not pwd:
        lbl_msg.config(text="Sila isi semua medan!", bg="white", fg="red")
        return

    conn = get_db_connection()
    if not conn:
        lbl_msg.config(text="Gagal connect ke database!", bg="white", fg="red")
        return
    
    try:
        cur = conn.cursor()
        # Guna table "guru" dengan column "id_guru" dan "password"
        # Convert user ke integer sebab id_guru adalah int(12)
        cur.execute("SELECT * FROM guru WHERE id_guru=%s AND password=%s", (int(user), pwd))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            lbl_msg.config(text="", bg="white")
            show_records()
        else:
            lbl_msg.config(text="ID/Kata laluan salah!", bg="white", fg="red")
    except ValueError:
        lbl_msg.config(text="ID mesti nombor!", bg="white", fg="red")
    except mysql.connector.Error as err:
        lbl_msg.config(text=f"Error: {err}", bg="white", fg="red")
        if conn:
            conn.close()

def show_records():
    records_win = Toplevel(root)
    records_win.title("Rekod Penggunaan Komputer")
    records_win.geometry("800x500")
    records_win.resizable(False, False)

    try:
        bg_img2 = Image.open("background.jpg").resize((800, 500))
        bg_img2 = ImageEnhance.Brightness(bg_img2).enhance(0.65)
        bg_photo2 = ImageTk.PhotoImage(bg_img2)
        
        bg_label2 = Label(records_win, image=bg_photo2)
        bg_label2.image = bg_photo2
        bg_label2.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        records_win.config(bg="#E8F4F8")

    overlay2 = Frame(records_win, bg="#FFFFFF", bd=0, highlightthickness=0)
    overlay2.place(relx=0.5, rely=0.5, anchor="center", width=520, height=360)

    try:
        logo_img2 = Image.open("logo.jpeg").resize((110, 110))
        logo_photo2 = ImageTk.PhotoImage(logo_img2)
        logo_label2 = Label(overlay2, image=logo_photo2, bg="white")
        logo_label2.image = logo_photo2
        logo_label2.pack(pady=(20, 12))
    except:
        pass

    Label(
        overlay2,
        text="Rekod Penggunaan Makmal Komputer",
        font=("Segoe UI", 16, "bold"),
        bg="white",
        fg=style_color,
    ).pack(pady=(0, 12))

    records_frame = Frame(overlay2, bg="white")
    records_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    scrollbar = Scrollbar(records_frame)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox = Listbox(
        records_frame,
        font=("Segoe UI", 10),
        bg="#F4F6FA",
        fg="#222222",
        relief="flat",
        activestyle="none",
        yscrollcommand=scrollbar.set,
        width=60,
        height=10,
    )
    listbox.pack(side=LEFT, fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    conn = get_db_connection()
    if not conn:
        listbox.insert(END, "Gagal connect ke database!")
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT p.nama, g.tarikh, g.masa_masuk, g.no_komputer
            FROM Penggunaan g
            JOIN pelajar p ON g.id_pelajar = p.id_pelajar
            ORDER BY g.id DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if rows:
            for row in rows:
                nama, tarikh, masa_masuk, no_pc = row
                listbox.insert(END, f"{nama} | {tarikh} | {masa_masuk} | Komputer {no_pc}")
        else:
            listbox.insert(END, "Tiada rekod ditemui.")
    except mysql.connector.Error as err:
        listbox.insert(END, f"Error: {err}")
        if conn:
            conn.close()

# === MAIN WINDOW ===
root = Tk()
root.title("e-LabKPD - Admin")
root.geometry("800x500")
root.resizable(False, False)

try:
    bg_img = Image.open("background.jpg").resize((800, 500))
    bg_img = ImageEnhance.Brightness(bg_img).enhance(0.65)
    bg_photo = ImageTk.PhotoImage(bg_img)
    
    bg_label = Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.config(bg="#E8F4F8")

overlay = Frame(root, bg="#FFFFFF", bd=0, highlightthickness=0)
overlay.place(relx=0.5, rely=0.48, anchor="center", width=380, height=400)

try:
    logo_img = Image.open("logo.jpeg").resize((130, 130))
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = Label(overlay, image=logo_photo, bg="white")
    logo_label.image = logo_photo
    logo_label.pack(pady=(20, 10))
except:
    pass

style_color = "#1F6AA5"

Label(
    overlay,
    text="Log Masuk Admin",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg=style_color,
).pack(pady=(0, 15))

# === ID Admin Section ===
Label(
    overlay,
    text="ID Admin",
    font=("Segoe UI", 11),
    bg="white",
    fg="#333333",
).pack(anchor="w", padx=36)

entry_user = Entry(
    overlay,
    font=("Segoe UI", 11),
    relief="flat",
    bg="#F4F6FA",
    fg="#222222"
)
entry_user.pack(pady=(5, 10), padx=36, ipady=5, ipadx=10, fill="x")

# === Kata Laluan Section ===
Label(
    overlay,
    text="Kata Laluan",
    font=("Segoe UI", 11),
    bg="white",
    fg="#333333",
).pack(anchor="w", padx=36)

entry_pwd = Entry(
    overlay,
    font=("Segoe UI", 11),
    relief="flat",
    bg="#F4F6FA",
    fg="#222222",
    show="*"
)
entry_pwd.pack(pady=(5, 15), padx=36, ipady=5, ipadx=10, fill="x")

# === Button ===
Button(
    overlay,
    text="Log Masuk",
    font=("Segoe UI", 11, "bold"),
    bg=style_color,
    fg="white",
    relief="flat",
    padx=30,
    pady=8,
    cursor="hand2",
    command=login_admin
).pack(pady=(0, 10))

# === Message Label ===
lbl_msg = Label(
    overlay,
    text="",
    font=("Segoe UI", 10),
    bg="white",
    fg="red"
)
lbl_msg.pack()

root.mainloop()