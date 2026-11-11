# -*- coding: utf-8 -*-
# bulut surumu: siniflandirmayi gemini api'ye yaptiriyor (internet gerekiyor)
# su an sistemi bu surumle calistiriyoruz
import os
import sys
import PIL.Image
from google import genai
import donanim
from kamera import foto_cek

MODEL_ADI = "gemini-3-flash-preview"

# api anahtari koda yazilmiyor, ortam degiskeninden okunuyor:
#   export GEMINI_API_KEY="..."
api_anahtari = os.environ.get("GEMINI_API_KEY")
if not api_anahtari:
    print("[HATA] GEMINI_API_KEY ortam degiskeni tanimli degil.")
    sys.exit(1)

client = genai.Client(api_key=api_anahtari)

NUMARA_SINIF = {"1": "PLASTIK", "2": "KAGIT", "3": "CAM", "4": "METAL", "5": "DIGER"}

PROMPT = """Sen bir atik ayristirma sistemisin. Goruntudeki atigi siniflandir.
1 = PLASTIK, 2 = KAGIT, 3 = CAM, 4 = METAL, 5 = DIGER
Cevap olarak sadece tek bir rakam yaz."""


def siniflandir(foto):
    img = PIL.Image.open(foto)
    try:
        cevap = client.models.generate_content(model=MODEL_ADI, contents=[PROMPT, img])
        metin = (cevap.text or "").strip()
    except Exception as e:
        print(f"[AI] API hatasi: {e}")
        return None

    print(f"--- AI YANITI: {metin} ---")
    # model bazen "3." gibi fazladan karakter ekleyebiliyor, sadece ilk rakama bakiyorum
    for karakter in metin:
        if karakter in NUMARA_SINIF:
            return NUMARA_SINIF[karakter]
    print("[AI] Yanit anlasilamadi, islem yapilmadi.")
    return None


def sistem_dongusu():
    foto = foto_cek()
    if foto is None:
        return
    print("[AI] Gemini goruntuyu analiz ediyor...")
    sinif = siniflandir(foto)
    if sinif:
        donanim.atik_isleme(sinif)


if __name__ == "__main__":
    print("--- GEMINI KONTROLLU AYRISTIRMA SISTEMI ---")
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
