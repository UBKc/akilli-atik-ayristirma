# -*- coding: utf-8 -*-
# servo motorlar ve mekanik hareketler (yolo ve gemini surumu ortak kullaniyor)
from time import sleep
from gpiozero import Servo

# servolarin darbe genisligi araligi (0.45 ms - 2.45 ms), kendi servolarimiza gore ayarlandi
PLATFORM_PIN = 18   # platformu kutularin uzerine dondurur
KAPAK_PIN = 17      # kapagi acip copu kutuya dokuyor

m_platform = Servo(PLATFORM_PIN, min_pulse_width=0.45 / 1000, max_pulse_width=2.45 / 1000)
m_kapak = Servo(KAPAK_PIN, min_pulse_width=0.45 / 1000, max_pulse_width=2.45 / 1000)

KAPAK_ACIK = -0.65
KAPAK_KAPALI = 0.0

# her sinifin kutusu platformda hangi konumda (-1 ile 1 arasi)
# -0.8 ile 0.7 arasinda tutuldu, platform mekanik sinirlari asmasin diye
KUTU_KONUMLARI = {
    "PLASTIK": -0.8,
    "KAGIT": -0.4,
    "CAM": 0.0,
    "METAL": 0.4,
    "DIGER": 0.7,
}

ADIM = 0.012        # her seferde ne kadar donsun
ADIM_BEKLEME = 0.008

current_pos = 0.0


def baslat():
    # acilista platform ortada, kapak kapali
    global current_pos
    current_pos = 0.0
    m_platform.value = current_pos
    m_kapak.value = KAPAK_KAPALI
    sleep(0.5)
    m_platform.value = None
    m_kapak.value = None


def platform_hareket(hedef_konum):
    # servo hedefe birden gitmesin diye kucuk adimlarla ilerliyor,
    # birden donerse disliler zarar gorebiliyor
    global current_pos
    print(f"   [MOTOR] Platform konumlaniyor: {hedef_konum}...")

    while current_pos != hedef_konum:
        if hedef_konum > current_pos:
            current_pos = min(current_pos + ADIM, hedef_konum)
        else:
            current_pos = max(current_pos - ADIM, hedef_konum)
        m_platform.value = current_pos
        sleep(ADIM_BEKLEME)

    sleep(0.1)
    m_platform.value = None   # sinyali kesince servo titremiyor


def kapak_tahliye():
    print("   [MEKANIK] Kapak aciliyor...")
    m_kapak.value = KAPAK_ACIK
    sleep(0.5)
    m_kapak.value = None

    # copun kutuya dusmesi icin bekleme
    print("   [MEKANIK] Tahliye icin bekleniyor (1.0 sn)...")
    sleep(1.0)

    print("   [MEKANIK] Kapak kapaniyor...")
    m_kapak.value = KAPAK_KAPALI
    sleep(0.4)
    m_kapak.value = None


def atik_isleme(sinif_adi):
    if sinif_adi not in KUTU_KONUMLARI:
        print(f"[SISTEM] Bilinmeyen sinif: {sinif_adi}")
        return

    print(f"\n--- TESPIT EDILEN SINIF: {sinif_adi} ---")
    platform_hareket(KUTU_KONUMLARI[sinif_adi])
    kapak_tahliye()
    print("   [SISTEM] Merkeze donuluyor...")
    platform_hareket(0.0)


def kapat():
    m_platform.value = None
    m_kapak.value = None
    m_platform.close()
    m_kapak.close()
