# Akıllı Atık Ayrıştırma Kutusu

*Raspberry Pi smart recycling bin: a camera image is classified (Gemini API, or my offline YOLOv8n-cls model trained on TrashNet) and two servo motors drop the item into one of 5 compartments.*

Kameraya gösterilen atığın türünü (plastik, kağıt, cam, metal, diğer) görüntüden tespit edip servo motorlarla ilgili kutuya döken bir sistem. Raspberry Pi üzerinde çalışıyor.

Takım kaptanı olduğum bir ekip projesi, bu repoda sistemin yazılım kısmı var. Proje devam ediyor.

## Nasıl çalışıyor

1. Raspberry Pi kamerası atığın fotoğrafını çekiyor.
2. Görüntü sınıflandırılıyor (Gemini API ya da internetsiz çalışan yerel model).
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

## Üç sürüm

| | `gemini_ile.py` (şu an kullanılan) | `siniflandirici_ile.py` | `yolo_ile.py` (hazırlanıyor) |
|---|---|---|---|
| Model | Gemini API (`gemini-3-flash-preview`) | TrashNet ile eğittiğim YOLOv8n-cls | kendi verimizle eğitilecek YOLO tespit modeli (`best.pt`) |
| İnternet | gerekiyor | gerekmiyor | gerekmiyor |
| Durum | kutuda çalışıyor | model hazır, kutuda henüz denenmedi | model eğitilmedi |

Sistemi şu an Gemini ile çalıştırıyoruz, hazır bir model olduğu için atık tanımayı hızlıca deneyebildik. İnternetsiz çalışması için açık bir veri seti olan TrashNet ile bir sınıflandırma modeli eğittim: test kümesinde kutudaki 5 bölmeye göre %91,56 doğruluk. Eğitim, karşılaştırma ve sonuçlar ayrı repoda: **[atik-siniflandirma-modeli](https://github.com/UBKc/atik-siniflandirma-modeli)**. TrashNet fotoğrafları beyaz zeminde çekildiği için kutunun kamerasında başarı daha düşük çıkabilir. Kalıcı çözüm olarak kendi kutumuzdan fotoğraf toplayıp YOLO modeli eğitmeyi planlıyoruz, `yolo_ile.py` bunun için hazır.

## Dikkat ettiğim noktalar

- **Yumuşak hareket:** Servo hedefe birden dönerse dişliler zarar görebiliyor. Platform hedefe 0.012'lik adımlarla, her adımda 8 ms bekleyerek gidiyor.
- **Titreme:** Hareket bitince servoya giden sinyal kesiliyor (`value = None`), yoksa servo yerinde titriyor.
- **Güven eşiği (yerel modeller):** Model %50'nin altında emin olduğu tahminlerde hiçbir şey yapmıyor. YOLO sürümünde fotoğrafta birden fazla nesne varsa en emin olduğu tespit alınıyor.
- **Eski fotoğraf:** Her döngüde eski fotoğraf silinip yenisi çekiliyor. Kamera hata verirse eski fotoğraf tekrar analiz edilmiyor.
- **Gemini yanıtı:** Modelden sadece rakam isteniyor. Yine de "3." gibi fazladan karakter gelirse ilk rakama bakılıyor, anlaşılmayan yanıtta platform hareket etmiyor.
- **API anahtarı:** Koda yazılmıyor, `GEMINI_API_KEY` ortam değişkeninden okunuyor.
- Pi terminalinde Türkçe karakter sorunu çıkmasın diye konsol çıktıları ASCII.

## Dosyalar

| Dosya | Ne işe yarıyor |
|---|---|
| `donanim.py` | servo ayarları, kutu konumları, platform ve kapak hareketleri |
| `kamera.py` | `rpicam-still` ile fotoğraf çekme |
| `siniflandirici_ile.py` | TrashNet ile eğitilmiş sınıflandırma modeli sürümü |
| `yolo_ile.py` | kendi verimizle eğitilecek YOLO modeli sürümü |
| `gemini_ile.py` | Gemini API sürümü |

## Çalıştırma

Gemini sürümü:

```
pip install -r requirements-gemini.txt
export GEMINI_API_KEY="..."
python gemini_ile.py
```

Sınıflandırma modeli sürümü ([atik-siniflandirma-modeli](https://github.com/UBKc/atik-siniflandirma-modeli) reposundaki `model/atik_yolov8n_cls.pt` dosyası bu klasöre konmalı):

```
pip install -r requirements.txt
python siniflandirici_ile.py
```

YOLO sürümü (eğitilmiş `best.pt` model dosyası aynı klasörde olmalı):

```
pip install -r requirements.txt
python yolo_ile.py
```

Hepsinde ENTER ile atık işleniyor, `q` ile çıkılıyor.

## Eksikler

- Sınıflandırma modeli kutunun kamerasıyla henüz denenmedi.
- Kendi verimizle YOLO modeli henüz eğitilmedi; bunun için kutunun kamerasından 5 sınıflı bir atık veri seti toplanıp etiketlenecek.
- Atık şu an ENTER'a basınca işleniyor. Kutuya atık konduğunu algılayan bir sensör (ör. kızılötesi) eklenince sistem tamamen otomatik olacak.
- Kutuların doluluk durumu takip edilmiyor.
