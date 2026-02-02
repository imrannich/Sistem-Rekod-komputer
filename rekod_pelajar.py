# rekod_pelajar.py
import mysql.connector
from db_config import get_db_connection
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance

def show_records_page(admin_name=None):
    """Page utama untuk paparan rekod pelajar - hanya boleh akses selepas login"""
    
    records_win = Tk()
    records_win.title("e-LabKPD - Rekod Penggunaan Komputer")
    records_win.geometry("2000x750")
    records_win.resizable(True, True)

    # Background
    try:
        bg_img2 = Image.open("background.jpg").resize((2000, 750))
        bg_img2 = ImageEnhance.Brightness(bg_img2).enhance(0.65)
        bg_photo2 = ImageTk.PhotoImage(bg_img2)
        
        bg_label2 = Label(records_win, image=bg_photo2)
        bg_label2.image = bg_photo2
        bg_label2.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        records_win.config(bg="#E8F4F8")

    # Header frame
    header_frame = Frame(records_win, bg="#1F6AA5", height=80)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    try:
        logo_img2 = Image.open("logo.jpeg").resize((60, 60))
        logo_photo2 = ImageTk.PhotoImage(logo_img2)
        logo_label2 = Label(header_frame, image=logo_photo2, bg="#1F6AA5")
        logo_label2.image = logo_photo2
        logo_label2.pack(side="left", padx=20, pady=10)
    except:
        pass

    title_frame = Frame(header_frame, bg="#1F6AA5")
    title_frame.pack(side="left", fill="y", padx=10)

    Label(
        title_frame,
        text="Rekod Penggunaan Makmal Komputer",
        font=("Segoe UI", 18, "bold"),
        bg="#1F6AA5",
        fg="white",
    ).pack(anchor="w")

    if admin_name:
        Label(
            title_frame,
            text=f"Admin: {admin_name}",
            font=("Segoe UI", 10),
            bg="#1F6AA5",
            fg="#E0E0E0",
        ).pack(anchor="w")

    # Logout button
    Button(
        header_frame,
        text="Log Keluar",
        font=("Segoe UI", 10),
        bg="#D32F2F",
        fg="white",
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2",
        command=lambda: logout(records_win)
    ).pack(side="right", padx=20, pady=20)

        # Main content frame
    main_frame = Frame(records_win, bg="white")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Search frame untuk pilih tarikh
    search_frame = Frame(main_frame, bg="white", pady=10)
    search_frame.pack(fill="x", pady=(0, 10))
    
    Label(
        search_frame,
        text="Cari Rekod Mengikut Tarikh:",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        fg="#333333"
    ).pack(side="left", padx=(0, 10))
    
    # Dropdown untuk hari
    Label(search_frame, text="Hari:", font=("Segoe UI", 10), bg="white").pack(side="left", padx=5)
    hari_var = StringVar(value="")
    hari_combo = ttk.Combobox(search_frame, textvariable=hari_var, width=5, state="readonly")
    hari_combo['values'] = [""] + [str(i).zfill(2) for i in range(1, 32)]
    hari_combo.pack(side="left", padx=5)
    
    # Dropdown untuk bulan
    Label(search_frame, text="Bulan:", font=("Segoe UI", 10), bg="white").pack(side="left", padx=5)
    bulan_var = StringVar(value="")
    bulan_combo = ttk.Combobox(search_frame, textvariable=bulan_var, width=5, state="readonly")
    bulan_combo['values'] = [""] + [str(i).zfill(2) for i in range(1, 13)]
    bulan_combo.pack(side="left", padx=5)
    
    # Dropdown untuk tahun
    Label(search_frame, text="Tahun:", font=("Segoe UI", 10), bg="white").pack(side="left", padx=5)
    tahun_var = StringVar(value="")
    tahun_combo = ttk.Combobox(search_frame, textvariable=tahun_var, width=8, state="readonly")
    tahun_combo['values'] = [""] + [str(i) for i in range(2020, 2030)]
    tahun_combo.pack(side="left", padx=5)
    
    # Button Cari
    search_btn = Button(
        search_frame,
        text="🔍 Cari",
        font=("Segoe UI", 10, "bold"),
        bg="#1F6AA5",
        fg="white",
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2",
        command=lambda: load_records(tree, hari_var.get(), bulan_var.get(), tahun_var.get())
    )
    search_btn.pack(side="left", padx=10)
    
    # Button Reset
    reset_btn = Button(
        search_frame,
        text="🔄 Reset",
        font=("Segoe UI", 10),
        bg="#757575",
        fg="white",
        relief="flat",
        padx=15,
        pady=5,
        cursor="hand2",
        command=lambda: reset_search(hari_var, bulan_var, tahun_var, tree)
    )
    reset_btn.pack(side="left", padx=5)

    # Table untuk paparan rekod
    table_frame = Frame(main_frame, bg="white")
    table_frame.pack(fill="both", expand=True)

    # Create Treeview (table)
    columns = ("ID Pelajar", "Nama Pelajar", "Masa (24jam)", "Tarikh", "No Komputer")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

    # Configure column headings
    tree.heading("ID Pelajar", text="ID Pelajar")
    tree.heading("Nama Pelajar", text="Nama Pelajar")
    tree.heading("Masa (24jam)", text="Masa (24jam)")
    tree.heading("Tarikh", text="Tarikh")
    tree.heading("No Komputer", text="No Komputer")

    # Configure column widths
    tree.column("ID Pelajar", width=120, anchor="center")
    tree.column("Nama Pelajar", width=200, anchor="w")
    tree.column("Masa (24jam)", width=100, anchor="center")
    tree.column("Tarikh", width=120, anchor="center")
    tree.column("No Komputer", width=120, anchor="center")

    # Scrollbar
    scrollbar_y = Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar_x = Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # Pack scrollbars and tree
    tree.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")
    scrollbar_x.pack(side="bottom", fill="x")

    # Load data
    load_records(tree)

    # Refresh button
    refresh_btn = Button(
        main_frame,
        text="🔄 Muat Semula",
        font=("Segoe UI", 11, "bold"),
        bg="#1F6AA5",
        fg="white",
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
        command=lambda: load_records(tree)
    )
    refresh_btn.pack(pady=10)

    records_win.mainloop()

def load_records(tree, hari="", bulan="", tahun=""):
    """Load rekod pelajar dari database dengan filter tarikh"""
    # Clear existing data
    for item in tree.get_children():
        tree.delete(item)
    
    conn = get_db_connection()
    if not conn:
        tree.insert("", "end", values=("Gagal connect ke database!", "", "", "", ""))
        return
    
    try:
        cur = conn.cursor()
        from datetime import datetime as dt
        
                # Build query dengan filter tarikh
        if hari and bulan and tahun:
            # Filter mengikut tarikh yang dipilih
            tarikh_filter = f"{tahun}-{bulan}-{hari}"
            cur.execute("""
                SELECT id_pelajar, nama, masa, no_komputer, tarikh
                FROM pelajar
                WHERE DATE(tarikh) = %s
                ORDER BY id_pelajar DESC
            """, (tarikh_filter,))
        else:
            # Papar semua rekod
            cur.execute("""
                SELECT id_pelajar, nama, masa, no_komputer, tarikh
                FROM pelajar
                ORDER BY id_pelajar DESC
            """)
        
        rows = cur.fetchall()
        
        if rows:
            for row in rows:
                id_pelajar, nama, masa, no_pc, tarikh = row
                
                # Format tarikh untuk paparan (DD-MM-YYYY)
                if tarikh:
                    if isinstance(tarikh, str):
                        try:
                            parts = tarikh.split('-')
                            if len(parts) == 3:
                                tarikh_formatted = f"{parts[2]}-{parts[1]}-{parts[0]}"
                            else:
                                tarikh_formatted = tarikh
                        except:
                            tarikh_formatted = tarikh
                    elif hasattr(tarikh, 'strftime'):
                        tarikh_formatted = tarikh.strftime('%d-%m-%Y')
                    else:
                        tarikh_formatted = str(tarikh)
                else:
                    tarikh_formatted = "-"
                
                tree.insert("", "end", values=(
                    id_pelajar, 
                    nama, 
                    f"{masa} jam", 
                    tarikh_formatted,  # Tarikh dari database
                    f"Komputer {no_pc}"
                ))
        else:
            tree.insert("", "end", values=("Tiada rekod ditemui.", "", "", "", ""))
        
        cur.close()
        conn.close()
        
    except mysql.connector.Error as err:
        tree.insert("", "end", values=(f"Error: {err}", "", "", "", ""))
        if conn:
            conn.close()

def reset_search(hari_var, bulan_var, tahun_var, tree):
    """Reset search dan papar semua rekod"""
    hari_var.set("")
    bulan_var.set("")
    tahun_var.set("")
    load_records(tree, "", "", "")

def logout(win):
    """Logout dan kembali ke login page - connect dengan sistem admin"""
    win.destroy()
    # Import admin selepas destroy window untuk elak circular import
    try:
        import admin
        admin.show_login_page()
    except Exception as e:
        print(f"Error: {e}")
        # Jika error, buka window baru untuk login
        error_win = Tk()
        error_win.title("Error")
        Label(error_win, text=f"Error: {e}\nSila run admin.py", fg="red").pack(padx=20, pady=20)
        Button(error_win, text="OK", command=error_win.destroy).pack(pady=10)
        error_win.mainloop()