# -*- coding: utf-8 -*-
# siniflandirma modeli surumu: TrashNet ile egittigim YOLOv8n-cls modeliyle internetsiz calisiyor
# model ve egitim: https://github.com/UBKc/atik-siniflandirma-modeli
# atik_yolov8n_cls.pt dosyasi bu klasore konunca kullanilabilir
import sys
from ultralytics import YOLO
import donanim
from kamera import foto_cek

MODEL_YOLU = "atik_yolov8n_cls.pt"
GUVEN_ESIGI = 0.5

# modelin 6 sinifi kutudaki 5 bolmeye eslesiyor, karton kagit bolmesine gidiyor
KUTU = {
    "plastik": "PLASTIK",
    "kagit": "KAGIT",
    "karton": "KAGIT",
    "cam": "CAM",
    "metal": "METAL",
    "cop": "DIGER",
}

try:
    model = YOLO(MODEL_YOLU)
    print("[SISTEM] Model yuklendi.")
except Exception as e:
    print(f"[HATA] Model yuklenemedi, '{MODEL_YOLU}' dosyasini kontrol edin: {e}")
    sys.exit(1)


def siniflandir(foto):
    sonuc = model(foto, imgsz=224, verbose=False)[0]
    sinif_id = int(sonuc.probs.top1)
    guven = float(sonuc.probs.top1conf)
    sinif = model.names[sinif_id]

    if guven < GUVEN_ESIGI:
        print(f"[MODEL] Tahmin guveni yetersiz: {sinif} %{guven * 100:.1f}")
        return None
    if sinif not in KUTU:
        print(f"[MODEL] Bilinmeyen sinif: {sinif}")
        return None

    print(f"--- MODEL SONUCU: {sinif} -> {KUTU[sinif]} (Guven: %{guven * 100:.1f}) ---")
    return KUTU[sinif]


def sistem_dongusu():
    foto = foto_cek()
    if foto is None:
        return
    print("[MODEL] Goruntu analiz ediliyor...")
    kutu = siniflandir(foto)
    if kutu:
        donanim.atik_isleme(kutu)


if __name__ == "__main__":
    print("=========================================")
    print("   AKILLI ATIK AYRISTIRMA SISTEMI        ")
    print("   Model: YOLOv8n-cls (atik_yolov8n_cls) ")
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
