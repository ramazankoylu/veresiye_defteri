import sqlite3

# Veritabanı bağlantısı oluşturma
def veritabani_baglan():
    conn = sqlite3.connect('veresiye_defteri.db')
    return conn

# Yeni müşteri ekleme fonksiyonu
def musteri_ekle(isim, soyisim, borc, urun):
    conn = veritabani_baglan()
    c = conn.cursor()

    # musteriler tablosunu oluşturma
    c.execute('''
        CREATE TABLE IF NOT EXISTS musteriler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT,
            soyisim TEXT,
            toplam_borc REAL DEFAULT 0
        )
    ''')

    # borclar tablosunu oluşturma
    c.execute('''
        CREATE TABLE IF NOT EXISTS borclar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musteri_id INTEGER,
            borc REAL,
            urun TEXT,
            FOREIGN KEY (musteri_id) REFERENCES musteriler(id) ON DELETE CASCADE
        )
    ''')

    # musteriler tablosuna müşteri ekleme
    c.execute("INSERT INTO musteriler (isim, soyisim, toplam_borc) VALUES (?, ?, ?)", 
              (isim, soyisim, borc))

    # Eklenen müşteriye ait borcu borclar tablosuna ekleme
    musteri_id = c.lastrowid
    c.execute("INSERT INTO borclar (musteri_id, borc, urun) VALUES (?, ?, ?)", (musteri_id, borc, urun))
    conn.commit()
    conn.close()

# Müşteriye borç ekleme fonksiyonu
def borc_ekle(musteri_id, borc, urun):
    conn = veritabani_baglan()
    c = conn.cursor()

    # Borclar tablosunun var olduğundan emin olalım
    c.execute('''
        CREATE TABLE IF NOT EXISTS borclar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            musteri_id INTEGER,
            borc REAL,
            urun TEXT,
            FOREIGN KEY (musteri_id) REFERENCES musteriler(id) ON DELETE CASCADE
        )
    ''')

    # Borç ekleme işlemi
    c.execute("INSERT INTO borclar (musteri_id, borc, urun) VALUES (?, ?, ?)", (musteri_id, borc, urun))
    c.execute("UPDATE musteriler SET toplam_borc = toplam_borc + ? WHERE id = ?", (borc, musteri_id))
    conn.commit()
    conn.close()

# Müşteri borçlarını getirme fonksiyonu
def musteri_borclarini_getir(musteri_id):
    conn = veritabani_baglan()
    c = conn.cursor()
    c.execute("SELECT borc, urun FROM borclar WHERE musteri_id = ?", (musteri_id,))
    borclar = c.fetchall()
    conn.close()
    return borclar

# Müşteri silme fonksiyonu
def musteri_sil(musteri_id):
    conn = veritabani_baglan()
    c = conn.cursor()
    c.execute("DELETE FROM musteriler WHERE id = ?", (musteri_id,))
    c.execute("DELETE FROM borclar WHERE musteri_id = ?", (musteri_id,))
    conn.commit()
    conn.close()

# Müşteri borçlarını silme fonksiyonu
def borc_sil(musteri_id, borc):
    conn = veritabani_baglan()
    c = conn.cursor()
    c.execute("UPDATE musteriler SET toplam_borc = toplam_borc - ? WHERE id = ?", (borc, musteri_id))
    c.execute("DELETE FROM borclar WHERE musteri_id = ? AND borc = ?", (musteri_id, borc))
    conn.commit()
    conn.close()

# Tüm müşterileri getirme fonksiyonu
def tum_musterileri_getir():
    conn = veritabani_baglan()
    c = conn.cursor()
    c.execute("SELECT * FROM musteriler")
    musteriler = c.fetchall()
    conn.close()
    return musteriler
