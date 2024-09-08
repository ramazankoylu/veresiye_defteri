# -------------------------------
# License: This software is developed by Ramazan Köylü and all rights are reserved.
# Unauthorized copying, distribution, or use of this software for commercial purposes is prohibited.
# This software may only be used by individuals authorized by the developer.
#
# Developer: Ramazan Köylü
# Date: [09.09.2024]
# Signature: The owner of this software is Ramazan Köylü.
# -------------------------------





import tkinter as tk
from tkinter import ttk, messagebox
from veresiye_defteri import yeni_musteri_ekle, musteri_borc_ekle, musteri_silme, musteri_borc_silme
from veritabani import tum_musterileri_getir, musteri_borclarini_getir
from datetime import datetime

# Ana Tkinter penceresi
root = tk.Tk()
root.title("Market Veresiye Defteri")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Modern Buton Stilleri
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Arial", 12), padding=10, foreground="#ffffff", background="#4CAF50", borderwidth=0)
style.map("TButton", background=[('active', '#45a049'), ('pressed', '#3e8e41')], foreground=[('active', '#ffffff')])

# Müşteri arama fonksiyonu
def musteri_arama(ara_entry, tree):
    search_text = ara_entry.get().strip().lower()
    for item in tree.get_children():
        tree.delete(item)

    musteriler = tum_musterileri_getir()
    for musteri in musteriler:
        if search_text in musteri[1].lower() or search_text in musteri[2].lower():
            borc = f"{musteri[3]:.2f}"
            tree.insert("", "end", values=(musteri[0], musteri[1], musteri[2], borc))

# Müşteri borçlarını gösterme fonksiyonu (raporlarla birlikte)
def musteri_borclari_goster(musteri_id):
    borclar = musteri_borclarini_getir(musteri_id)

    borc_pencere = tk.Toplevel()
    borc_pencere.title("Müşteri Borçları")
    borc_pencere.geometry("400x300")

    tree = ttk.Treeview(borc_pencere, columns=("Borç", "Ürün"), show="headings")
    tree.heading("Borç", text="Borç (TL)")
    tree.heading("Ürün", text="Aldığı Ürün")

    for borc, urun in borclar:
        tree.insert("", "end", values=(borc, urun))

    tree.pack(fill=tk.BOTH, expand=True)

    # Raporları gösterme
    rapor_label = ttk.Label(borc_pencere, text="Borç Düşüş Raporları:")
    rapor_label.pack(pady=10)

    rapor_text = tk.Text(borc_pencere, height=8)
    rapor_text.pack(fill=tk.BOTH, expand=True)

    try:
        with open(f"musteri_{musteri_id}_rapor.txt", "r") as file:
            raporlar = file.readlines()
    except FileNotFoundError:
        raporlar = []

    if raporlar:
        for rapor in raporlar:
            rapor_text.insert(tk.END, rapor)
    else:
        rapor_text.insert(tk.END, "Bu müşteri için borç düşüş raporu bulunmamaktadır.")

# Müşteri ekleme arayüzü
def musteri_ekle_ekrani():
    def ekle():
        isim = isim_entry.get().strip()
        soyisim = soyisim_entry.get().strip()
        borc_str = borc_entry.get().strip()
        aldigi_urun = urun_entry.get().strip()

        if not isim or not soyisim or not borc_str or not aldigi_urun:
            messagebox.showwarning("Uyarı", "Tüm alanları doldurun!")
            return

        try:
            borc = float(borc_str)
        except ValueError:
            messagebox.showwarning("Uyarı", "Borç alanına geçerli bir sayı girin!")
            return

        yeni_musteri_ekle(isim, soyisim, borc, aldigi_urun)
        messagebox.showinfo("Başarılı", f"{isim} {soyisim} başarıyla eklendi!")
        ekle_pencere.destroy()

    ekle_pencere = tk.Toplevel()
    ekle_pencere.title("Yeni Müşteri Ekle")
    ekle_pencere.geometry("400x300")
    ekle_pencere.configure(bg="#f0f0f0")

    ttk.Label(ekle_pencere, text="İsim:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
    isim_entry = ttk.Entry(ekle_pencere, width=30)
    isim_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(ekle_pencere, text="Soyisim:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10, sticky='e')
    soyisim_entry = ttk.Entry(ekle_pencere, width=30)
    soyisim_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(ekle_pencere, text="Borç (TL):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10, sticky='e')
    borc_entry = ttk.Entry(ekle_pencere, width=30)
    borc_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(ekle_pencere, text="Aldığı Ürün:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=10, sticky='e')
    urun_entry = ttk.Entry(ekle_pencere, width=30)
    urun_entry.grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(ekle_pencere, text="Ekle", command=ekle).grid(row=4, column=0, columnspan=2, pady=20)

# Borç ekleme arayüzü
def borc_ekle_ekrani():
    def ekle_borc():
        musteri_id = musteri_id_entry.get().strip()
        borc_str = borc_entry.get().strip()
        urun = urun_entry.get().strip()

        if not musteri_id or not borc_str or not urun:
            messagebox.showwarning("Uyarı", "Tüm alanları doldurun!")
            return

        try:
            musteri_id = int(musteri_id)
            borc = float(borc_str)
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçerli bir Müşteri ID ve Borç girin!")
            return

        musteri_borc_ekle(musteri_id, borc, urun)
        messagebox.showinfo("Başarılı", f"{borc} TL borç başarıyla eklendi.")
        borc_pencere.destroy()

    borc_pencere = tk.Toplevel()
    borc_pencere.title("Borç Ekle")
    borc_pencere.geometry("400x300")
    borc_pencere.configure(bg="#f0f0f0")

    ttk.Label(borc_pencere, text="Müşteri ID:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10)
    musteri_id_entry = ttk.Entry(borc_pencere, width=30)
    musteri_id_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(borc_pencere, text="Borç (TL):", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10)
    borc_entry = ttk.Entry(borc_pencere, width=30)
    borc_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(borc_pencere, text="Aldığı Ürün:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10)
    urun_entry = ttk.Entry(borc_pencere, width=30)
    urun_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Button(borc_pencere, text="Borç Ekle", command=ekle_borc).grid(row=3, column=0, columnspan=2, pady=20)

# Borç silme arayüzü
def sil_borc_ekrani():
    def sil_borc():
        musteri_id_str = musteri_id_entry.get().strip()
        borc_str = borc_entry.get().strip()

        if not musteri_id_str or not borc_str:
            messagebox.showwarning("Uyarı", "Tüm alanları doldurun!")
            return

        try:
            musteri_id = int(musteri_id_str)
            borc = float(borc_str)
        except ValueError:
            messagebox.showwarning("Uyarı", "Geçerli bir Müşteri ID ve Borç girin!")
            return

        musteri_borc_silme(musteri_id, borc)
        messagebox.showinfo("Başarılı", f"{borc} TL borç başarıyla silindi.")
        
        # Raporu dosyaya kaydet
        rapor = f"Borç Düşüş Raporu: {musteri_id} ID'li müşterinin {borc} TL borcu silindi - {datetime.now()}\n"
        with open(f"musteri_{musteri_id}_rapor.txt", "a") as file:
            file.write(rapor)

        sil_pencere.destroy()

    sil_pencere = tk.Toplevel()
    sil_pencere.title("Borç Sil")
    sil_pencere.geometry("300x200")
    sil_pencere.configure(bg="#f0f0f0")

    ttk.Label(sil_pencere, text="Müşteri ID:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10)
    musteri_id_entry = ttk.Entry(sil_pencere, width=30)
    musteri_id_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(sil_pencere, text="Silinecek Borç (TL):", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10)
    borc_entry = ttk.Entry(sil_pencere, width=30)
    borc_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Button(sil_pencere, text="Borç Sil", command=sil_borc).grid(row=2, column=0, columnspan=2, pady=20)

# Müşteri listesini gösterme (modernleştirilmiş tablo)
def musteri_listesi_goster():
    musteriler = tum_musterileri_getir()

    liste_pencere = tk.Toplevel()
    liste_pencere.title("Müşteri Listesi")
    liste_pencere.geometry("800x600")
    liste_pencere.configure(bg="#f0f0f0")

    scrollbar = ttk.Scrollbar(liste_pencere)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree = ttk.Treeview(liste_pencere, columns=("ID", "İsim", "Soyisim", "Toplam Borç"), show="headings", height=20, yscrollcommand=scrollbar.set)
    tree.heading("ID", text="ID")
    tree.heading("İsim", text="İsim")
    tree.heading("Soyisim", text="Soyisim")
    tree.heading("Toplam Borç", text="Toplam Borç (TL)")

    tree.column("ID", width=50, anchor='center')
    tree.column("İsim", width=150, anchor='center')
    tree.column("Soyisim", width=150, anchor='center')
    tree.column("Toplam Borç", width=150, anchor='center')

    scrollbar.config(command=tree.yview)

    tree.tag_configure('low_debt', background='#dff0d8')      # Yeşil tonları
    tree.tag_configure('medium_debt', background='#fcf8e3')   # Sarı tonları
    tree.tag_configure('high_debt', background='#f2dede')     # Kırmızı tonları

    for musteri in musteriler:
        borc = musteri[3]
        if borc < 500:
            tag = 'low_debt'
        elif 500 <= borc < 2000:
            tag = 'medium_debt'
        else:
            tag = 'high_debt'
        tree.insert("", "end", values=(musteri[0], musteri[1], musteri[2], f"{borc:.2f}"), tags=(tag,))

    tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    arama_frame = ttk.Frame(liste_pencere)
    arama_frame.pack(pady=10)

    ttk.Label(arama_frame, text="Müşteri Ara:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
    ara_entry = ttk.Entry(arama_frame, width=30)
    ara_entry.pack(side=tk.LEFT, padx=5)
    ttk.Button(arama_frame, text="Ara", command=lambda: musteri_arama(ara_entry, tree)).pack(side=tk.LEFT, padx=5)

    def on_double_click(event):
        selected_item = tree.selection()
        if selected_item:
            musteri_id = tree.item(selected_item[0])['values'][0]
            musteri_borclari_goster(musteri_id)

    tree.bind("<Double-1>", on_double_click)

# Ana menü
def ana_menu():
    menu_frame = ttk.Frame(root, padding=20)
    menu_frame.pack(expand=True)

    ttk.Button(menu_frame, text="Yeni Müşteri Ekle", command=musteri_ekle_ekrani, width=25).pack(pady=10)
    ttk.Button(menu_frame, text="Müşteriyi Sil", command=sil_borc_ekrani, width=25).pack(pady=10)
    ttk.Button(menu_frame, text="Müşteriye Borç Ekle", command=borc_ekle_ekrani, width=25).pack(pady=10)
    ttk.Button(menu_frame, text="Müşteriden Borç Sil", command=sil_borc_ekrani, width=25).pack(pady=10)
    ttk.Button(menu_frame, text="Müşteri Listesi", command=musteri_listesi_goster, width=25).pack(pady=10)

ana_menu()
root.mainloop()
