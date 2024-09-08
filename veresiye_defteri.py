from veritabani import musteri_ekle, borc_ekle, musteri_sil, borc_sil

# Yeni müşteri ekleme işlevi
def yeni_musteri_ekle(isim, soyisim, borc, urun):
    musteri_ekle(isim, soyisim, borc, urun)

# Müşteriye yeni borç ekleme işlevi
def musteri_borc_ekle(musteri_id, borc, urun):
    borc_ekle(musteri_id, borc, urun)

# Müşteri silme işlevi
def musteri_silme(musteri_id):
    musteri_sil(musteri_id)

# Müşteri borcunu silme işlevi
def musteri_borc_silme(musteri_id, borc):
    borc_sil(musteri_id, borc)
