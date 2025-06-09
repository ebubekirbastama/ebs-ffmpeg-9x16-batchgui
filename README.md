# 🎬 9:16 / 16:9 Blur Video İşleyici

📱 Dikey (9:16) ya da 🖥️ Yatay (16:9) video formatına uygun hale getirilmiş videolar mı istiyorsun?<br>
🎞️ Bu araç, videolarını seçtiğin orana göre dönüştürür, arka planı bulanıklaştırır ve çoklu dosyayı aynı anda işler!

---

## 🚀 Özellikler

✅ Dikey veya yatay video formatı seçimi  
✅ Çoklu video seçimi  
✅ Her video için ilerleme çubuğu ve durum bildirimi  
✅ Blur arka plan efekti (YouTube Shorts, Reels, TikTok ve YouTube için ideal)  
✅ FFmpeg ile yüksek performanslı işleme  
✅ Modern ve kullanıcı dostu PyQt5 arayüzü  
✅ 📁 Çıktılar output_videos klasörüne otomatik kaydedilir 

---

## 📸 Önizleme

| 📂 Seçim | ⏳ İşlem | ✅ Tamam |
|---------|---------|---------|
| ![select](https://placehold.co/100x20?text=📂) | ![progress](https://placehold.co/100x20?text=🔄) | ![done](https://placehold.co/100x20?text=✔️) |

---

## 🛠 Gereksinimler

- Python 3.7+  
- `ffmpeg` sisteminizde kurulu ve `PATH`'e eklenmiş olmalı  
- Gerekli Python kütüphaneleri:

```bash
pip install PyQt5
```

---

## 🔧 Kurulum ve Kullanım

1️⃣ Depoyu klonlayın:
```bash
git clone https://github.com/kullaniciadi/9-16-blur-video.git
cd 9-16-blur-video
```

2️⃣ Python bağımlılıklarını kurun:
```bash
pip install PyQt5
```

3️⃣ `ffmpeg` yüklü değilse yükleyin:

**Windows:**  
[https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) — ve `bin` klasörünü `PATH`'e ekleyin.

**Linux:**  
```bash
sudo apt install ffmpeg
```

**macOS:**  
```bash
brew install ffmpeg
```

4️⃣ Uygulamayı başlatın:
```bash
python app.py
```

---

## 📁 Çıktı Yapısı

İşlenmiş videolar aşağıdaki klasöre kaydedilir:

```
/output_videos/
├── video1.mp4
├── video2.mp4
└── ...
```

---

## 🎥 Video İşleme Mantığı

FFmpeg filtreleri:

- 📏 Oran: 1080x1920 (9:16)
- 🎨 Arka plan: Bulanıklaştırılmış orijinal video
- 🎯 Ön plan: Orijinal video ortalanarak yerleştirilir
- 💾 Codec: `libx264` + `copy audio`

```bash
ffmpeg -i input.mp4 -filter_complex "[0:v]scale=...blur...overlay..." ...
```

---

## 🧠 Geliştirici Notları

- PyQt5 ile geliştirilmiş modern ve sade bir arayüz
- Her video için ayrı bir thread kullanılır: UI donmaz
- Emoji destekli statü güncellemeleri: ⏳ ✅ ❌

---

## 💡 Katkıda Bulun

Pull request’ler, bug raporları ve önerileriniz memnuniyetle karşılanır.  
Fork'la, geliştir ve katkıda bulun! 🚀

---

## 🪪 Lisans

MIT Lisansı – Dilediğiniz gibi ✅ kullanın, ✅ geliştirin,  ✅paylaşın ❌satışını yapmayın.

---

## 👨‍💻 Geliştirici

📛 **Ebubekir Bastama**  


---

## 📌 Not

Bu uygulama GUI üzerinden işlemleri basitleştirmek amacıyla geliştirilmiştir. Arka planda güçlü bir `ffmpeg` altyapısı kullanır.  

🧪 Daha fazla özellik için:  
- 🎨 Tema desteği  
- 📁 Çıktı klasörünü otomatik açma  
- 🛑 Durdurma/sıfırlama butonları  
...yakında!  

---

✨ **İyi işlenmiş videolar, daha çok izlenme demektir. Bu uygulama ile içeriklerinizi profesyonelleştirin!**
