# Akıllı Atık Ayrıştırma Kutusu

Kameraya gösterilen atığın türünü (plastik, kağıt, cam, metal, diğer) görüntüden tespit edip servo motorlarla ilgili kutuya döken bir sistem. Raspberry Pi üzerinde çalışıyor.

TEKNOFEST 2026 için geliştirdiğimiz projenin yazılım kısmı, takım kaptanıyım. Proje devam ediyor.

## Nasıl çalışıyor

1. Raspberry Pi kamerası atığın fotoğrafını çekiyor.
2. Görüntü sınıflandırılıyor (şu an Gemini API, ileride yerel YOLO modeli).
3. Platform servo motoru, tespit edilen sınıfın kutusunun üzerine dönüyor.
4. Kapak servo motoru açılıyor, atık kutuya düşüyor, kapak kapanıyor.
5. Platform ortaya geri dönüp yeni atığı bekliyor.

## Donanım

| Parça | Bağlantı |
|---|---|
| Raspberry Pi | ana kart |
| Raspberry Pi kamera modülü | `rpicam-still` ile fotoğraf |
| Servo 1 – platform | GPIO 18 |
| Servo 2 – kapak | GPIO 17 |

Kutuların platformdaki konumları (servo değeri -1 ile 1 arası):

| Sınıf | Konum |
|---|---|
| Plastik | -0.8 |
| Kağıt | -0.4 |
| Cam | 0.0 |
| Metal | 0.4 |
| Diğer | 0.7 |

Konumlar -0.8 ile 0.7 arasında tutuldu, platformun mekanik sınırlarını aşmasın diye.

## İki sürüm

| | `gemini_ile.py` (şu an kullanılan) | `yolo_ile.py` (hazırlanıyor) |
|---|---|---|
| Model | Gemini API (`gemini-3-flash-preview`) | kendi eğiteceğimiz YOLO modeli (`best.pt`) |
| İnternet | gerekiyor | gerekmiyor |
| Gecikme | API cevabına bağlı | düşük, Pi üzerinde çalışacak |

Sistemi şu an Gemini ile çalıştırıyoruz, hazır bir model olduğu için atık tanımayı hızlıca deneyebildik. Kalıcı çözüm olarak internetsiz ve daha düşük gecikmeyle çalışması için kendi YOLO modelimizi eğitmeyi planlıyoruz. `yolo_ile.py` bunun için hazır: model eğitilip `best.pt` olarak klasöre konunca aynı mekanik kodla çalışacak.

## Dikkat ettiğim noktalar

- **Yumuşak hareket:** Servo hedefe birden dönerse dişliler zarar görebiliyor. Platform hedefe 0.012'lik adımlarla, her adımda 8 ms bekleyerek gidiyor.
- **Titreme:** Hareket bitince servoya giden sinyal kesiliyor (`value = None`), yoksa servo yerinde titriyor.
- **Güven eşiği (YOLO sürümü):** Model %50'nin altında emin olduğu tespitlerde hiçbir şey yapmıyor. Fotoğrafta birden fazla nesne varsa en emin olduğu tespiti alıyor.
- **Eski fotoğraf:** Her döngüde eski fotoğraf silinip yenisi çekiliyor. Kamera hata verirse eski fotoğraf tekrar analiz edilmiyor.
- **Gemini yanıtı:** Modelden sadece rakam isteniyor. Yine de "3." gibi fazladan karakter gelirse ilk rakama bakılıyor, anlaşılmayan yanıtta platform hareket etmiyor.
- **API anahtarı:** Koda yazılmıyor, `GEMINI_API_KEY` ortam değişkeninden okunuyor.
- Pi terminalinde Türkçe karakter sorunu çıkmasın diye konsol çıktıları ASCII.

## Dosyalar

| Dosya | Ne işe yarıyor |
|---|---|
| `donanim.py` | servo ayarları, kutu konumları, platform ve kapak hareketleri |
| `kamera.py` | `rpicam-still` ile fotoğraf çekme |
| `yolo_ile.py` | yerel model sürümü |
| `gemini_ile.py` | Gemini API sürümü |

## Çalıştırma

Gemini sürümü:

```
pip install -r requirements-gemini.txt
export GEMINI_API_KEY="..."
python gemini_ile.py
```

YOLO sürümü (eğitilmiş `best.pt` model dosyası aynı klasörde olmalı):

```
pip install -r requirements.txt
python yolo_ile.py
```

Her iki sürümde de ENTER ile atık işleniyor, `q` ile çıkılıyor.

## Eksikler

- YOLO modeli henüz eğitilmedi; bunun için 5 sınıflı bir atık veri seti toplanıp etiketlenecek.
- Atık şu an ENTER'a basınca işleniyor. Kutuya atık konduğunu algılayan bir sensör (ör. kızılötesi) eklenince sistem tamamen otomatik olacak.
- Kutuların doluluk durumu takip edilmiyor.
