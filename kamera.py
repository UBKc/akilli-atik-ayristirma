# -*- coding: utf-8 -*-
import os
import subprocess

DOSYA = "atik.jpg"


def foto_cek():
    # her seferinde eski fotoyu silip yenisini cekiyorum,
    # yoksa kamera hata verdiginde eski foto tekrar analiz ediliyordu
    if os.path.exists(DOSYA):
        os.remove(DOSYA)

    print("\n[KAMERA] Goruntu aliniyor...")
    sonuc = subprocess.run(
        ["rpicam-still", "-o", DOSYA, "--immediate", "--nopreview"],
        capture_output=True,
    )
    if sonuc.returncode != 0 or not os.path.exists(DOSYA):
        print("[KAMERA] Fotograf cekilemedi, kamera baglantisini kontrol edin.")
        return None
    return DOSYA
