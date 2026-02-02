# admin.py
import mysql.connector
from db_config import get_db_connection
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance
from datetime import datetime

# Global variable untuk simpan nama admin yang login
logged_in_admin = None

def login_admin():
    global logged_in_admin
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
        cur.execute("SELECT * FROM guru WHERE id_guru=%s AND password=%s", (int(user), pwd))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            logged_in_admin = result[1]  # Simpan nama admin
            lbl_msg.config(text="Log masuk berjaya! Membuka paparan rekod...", bg="white", fg="green")
            root.update()  # Update UI untuk tengok mesej
            # Tutup login window dan buka rekod page
            root.after(500, lambda: open_records_page(logged_in_admin))
        else:
            lbl_msg.config(text="ID/Kata laluan salah!", bg="white", fg="red")
    except ValueError:
        lbl_msg.config(text="ID mesti nombor!", bg="white", fg="red")
    except Exception as err:
        lbl_msg.config(text=f"Error: {str(err)}", bg="white", fg="red")
        print(f"Error: {err}")  # Print untuk debugging
        if conn:
            conn.close()

def open_records_page(admin_name):
    """Function untuk buka rekod page selepas tutup login window"""
    root.destroy()
    try:
        import rekod_pelajar
        rekod_pelajar.show_records_page(admin_name)
    except Exception as e:
        print(f"Error opening records page: {e}")
        import traceback
        traceback.print_exc()  # Print full error untuk debugging
        # Jika error, buka window error
        error_win = Tk()
        error_win.title("Error")
        Label(error_win, text=f"Error membuka paparan rekod:\n{e}", fg="red", font=("Arial", 10)).pack(padx=20, pady=20)
        Button(error_win, text="OK", command=error_win.destroy).pack(pady=10)
        error_win.mainloop()

def show_login_page():
    """Page login untuk admin"""
    global root, entry_user, entry_pwd, lbl_msg, style_color
    
    root = Tk()
    root.title("e-LabKPD - Admin Login")
    root.geometry("1300x750")
    root.resizable(False, False)

    try:
        bg_img = Image.open("background.jpg").resize((1300, 750))
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

    # ID Admin Section
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

    # Kata Laluan Section
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

    # Button
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

    # Message Label
    lbl_msg = Label(
        overlay,
        text="",
        font=("Segoe UI", 10),
        bg="white",
        fg="red"
    )
    lbl_msg.pack()

    root.mainloop()

# Start dengan login page
if __name__ == "__main__":
    show_login_page()