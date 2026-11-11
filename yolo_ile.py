# -*- coding: utf-8 -*-
# yerel model surumu: kendi egitecegimiz yolo modeliyle internetsiz calisacak
# model egitilip best.pt olarak bu klasore konunca kullanilabilir
import sys
from ultralytics import YOLO
import donanim
from kamera import foto_cek

MODEL_YOLU = "best.pt"
GUVEN_ESIGI = 0.5

# modeli egitirken kullanilacak sinif sirasi
SINIFLAR = {0: "PLASTIK", 1: "KAGIT", 2: "CAM", 3: "METAL", 4: "DIGER"}

try:
    model = YOLO(MODEL_YOLU)
    print("[SISTEM] Model yuklendi.")
except Exception as e:
    print(f"[HATA] Model yuklenemedi, '{MODEL_YOLU}' dosyasini kontrol edin: {e}")
    sys.exit(1)


def tespit_et(foto):
    sonuc = model(foto, verbose=False)[0]
    if len(sonuc.boxes) == 0:
        print("[YOLO] Nesne bulunamadi.")
        return None

    # birden fazla kutu varsa en emin oldugunu aliyorum
    en_iyi = int(sonuc.boxes.conf.argmax())
    sinif_id = int(sonuc.boxes.cls[en_iyi])
    guven = float(sonuc.boxes.conf[en_iyi])

    if guven < GUVEN_ESIGI:
        print(f"[YOLO] Tespit guveni yetersiz: %{guven * 100:.1f}")
        return None
    if sinif_id not in SINIFLAR:
        print(f"[YOLO] Bilinmeyen sinif numarasi: {sinif_id}")
        return None

    print(f"--- YOLO SONUCU: {SINIFLAR[sinif_id]} (Guven: %{guven * 100:.1f}) ---")
    return SINIFLAR[sinif_id]


def sistem_dongusu():
    foto = foto_cek()
    if foto is None:
        return
    print("[YOLO] Goruntu analiz ediliyor...")
    sinif = tespit_et(foto)
    if sinif:
        donanim.atik_isleme(sinif)


if __name__ == "__main__":
    print("=========================================")
    print("   AKILLI ATIK AYRISTIRMA SISTEMI        ")
    print("   Model: YOLO (best.pt)                ")
    print("=========================================")
    donanim.baslat()
    try:
        while True:
            komut = input("\n>> Baslatmak icin ENTER, cikis icin 'q': ")
            if komut.strip().lower() == "q":
                break
            sistem_dongusu()
    except KeyboardInterrupt:
        pass
    finally:
        print("\n[SISTEM] Kapatiliyor...")
        donanim.kapat()
