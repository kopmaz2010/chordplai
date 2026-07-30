# ChordPlai — Proje Analizi ve 20 Fikir

*30 Temmuz 2026 · kod tabanı ölçülerek hazırlandı*

---

## Bölüm 1 — Projenin bugünkü hali

### Rakamlar

| | |
|---|---|
| `index.html` | 334 KB · 6.986 satır · **4.984 satır JS** |
| Modüller | 14 bağımsız IIFE, `window.*` üzerinden konuşuyor |
| Diller | 6 (TR·EN·ES·DE·FR·PT), 431 dize/dil |
| İçerik | 8 blog × 6 dil = 48 sayfa, 57 URL'lik sitemap |
| Depo | 21 MB, 32 commit |
| Sunucu maliyeti | **0** — her şey tarayıcıda çalışıyor |

### Mimari özet

Tek dosyalık istemci uygulaması. Build adımı yok, framework yok, bağımlılık yok.
Dışarıdan çekilen tek şey MediaPipe modelleri (el 7,8 MB · beden 5,8 MB, CDN'den
tembel yükleniyor) ve Supabase/Google giriş kitaplıkları.

Sekiz bölüm: Air Chord (bayrak gemisi), Akapella, Akorlar, Nota Oyunu, Porte,
Ninja, Tetris + not defteri/prompter paneli.

### Zaten kurulu olan teknoloji yığını

**Görü:** HandLandmarker (21 nokta × 2 el) · PoseLandmarker (33 nokta)

**Ses:** Oscillator katmanlama, ConvolverNode (reverb), DynamicsCompressor,
BiquadFilter, WaveShaper (distorsiyon), StereoPanner, AnalyserNode,
MediaStreamDestination

**DSP (kendi yazdığımız):** otokorelasyon perde tespiti, **TD-PSOLA perde
kaydırma** (formant koruyan), diyatonik armoni üretimi

**Çıktı:** MediaRecorder + canvas `captureStream` → WebM/MP4 dışa aktarma

**Teori motoru:** 13 gam/makam, 33 akor tipi (JGuitar tabanlı), derece/roma
rakamı çevirimi, gam-göreli aralık matematiği

**Altyapı:** Supabase (auth + profiles + **scores tablosu**), statik içerik
üreteci (`build.py`), çalışma-anı i18n, hreflang sitemap

**Sıfır maliyetli AI köprüsü:** "ChordPlai AYARI: Ton = A · Gam = Kürdi"
satırı — kullanıcı promtu kendi AI'ına yapıştırıyor, dönen satırı bize
veriyor. API faturası yok, kota yok.

### En önemli bulgu: ham verinin ~%8'ini kullanıyoruz

```
HandLandmarker : 21 nokta × 2 el × 3 eksen = 126 sayı/kare
PoseLandmarker : 33 nokta × 3 eksen        =  99 sayı/kare
─────────────────────────────────────────────────────────
Çıkarılan      : parmak(4 bit) · başparmak · yatış · avuç yönü · poz
                 ≈ 10 sayı
```

**Hiç kullanılmayanlar:**

- **z ekseni (derinlik)** — kodda tek referans var, o da veri kopyalarken
- **Hız/ivme** — hareket türevi yok; el hareketleri "olay" üretmiyor
- **İki el arası mesafe** — el başına ayrı işleniyor, aralarındaki ilişki yok
- **Çimdik mesafesi (baş–işaret parmağı)** — sürekli kontrolcü, bedava duruyor
- **Mutlak x/y konumu** — sadece "sol yarı / sağ yarı" olarak kullanılıyor
- **El boyutu** — kameraya uzaklığın vekili
- **MediaPipe'ın kendi handedness çıktısı** — biz ekran konumundan tahmin ediyoruz
- **Çoklu kişi** — `numPoses: 1`
- **Yüz (FaceLandmarker)** — aynı kitaplıkta, 478 nokta + blendshape, hiç açılmadı

**Atıl varlıklar:** `scores` tablosu şemada var ama liderlik tablosu cihazda
kalıyor · `SpeechRecognition` sadece nota oyununda · Air Chord'da sağ el
yalnızca efekt yapıyor.

### Stratejik değerlendirme

Güçlü yanlar: her şey cihazda çalıştığı için **gizlilik doğal olarak
çözülmüş** (kamera görüntüsü hiç çıkmıyor) ve **sunucu maliyeti sıfır**.
Kurulum yok, tarayıcı yeter. 6 dil ve SEO hattı hazır. Türk makamları hiçbir
rakipte yok.

Zayıf yanlar: tek dosya 334 KB'a ulaştı (modülerleşme baskısı yakın), sinyal
çeşitliliği düşük (her şey ayrık, sürekli kontrol yok), sosyal/çok oyunculu
katman yok, kullanıcı sayısı ölçülemiyor (Analytics hâlâ kapalı).

---

## Bölüm 2 — 10 müzik fikri

### 1. Çimdik = sürekli kontrolcü 🔥
Baş parmak ile işaret parmağı arasındaki mesafe (landmark 4↔8) sürekli bir
değer üretir: pitch bend, filtre kesimi, vibrato derinliği, ses şişirme.
Şu an her şey ayrık (parmak say, poz tut); tek bir sürekli eksen enstrümanı
**ifade edilebilir** kılar. *Yeniden kullanım: landmarklar zaten elde.
Zorluk: düşük. Etki: çok yüksek.*

### 2. İki elli enstrüman — sol akor, sağ melodi
Sol el dereceyi tutar (mevcut), sağ elin **yüksekliği** gamdaki notayı seçer.
Kendi akorunun üstüne solo çalarsın. Sağ el şu an sadece efekt yapıyor, yani
elin yarısı boşta duruyor. *Zorluk: orta. Etki: ürünü oyuncaktan enstrümana
taşır.*

### 3. Hayalet el — ritim oyunu modu
Prompter'daki sıradaki akorun el fotoğrafı kameranın üstünde yarı saydam
belirir, doğru anda o işareti yapman istenir; isabet puanlanır. Guitar Hero
mantığı ama el işaretiyle. *Yeniden kullanım: prompter + `tasarim/sign/*` +
`scores` tablosu. Zorluk: orta. Etki: elde tutma ve paylaşılabilirlik.*

### 4. Beden perküsyonu
El hızındaki ani sıçramalar vuruş üretir: alkış (iki el birleşiyor), diz
şapırtısı (el kalça landmarkına iniyor), göğüs vuruşu. Kendi ritmini bedenle
çalarsın. *Kullanılmayan sinyal: hız. Zorluk: orta (eşik ayarı iş ister).*

### 5. Orkestra şefliği
El yüksekliği = gürlük, el hızı = tempo. Metronomu ve arpeji canlı yönetirsin.
Klasik müzik eğitiminde şeflik jestleri öğretilebilir. *Zorluk: düşük-orta.
Etki: eğitim kurumlarına açılım.*

### 6. Canlı armoni — Akapella + Air Chord birleşimi 🔥
Mikrofona söylerken elinle akoru gösteriyorsun, sesin **anlık olarak** o akora
harmonize ediliyor. İki bayrak gemisi özelliğin tek deneyimde birleşiyor.
PSOLA zaten yazıldı; mesele gecikmeyi 30 ms altına indirmek. *Zorluk: yüksek.
Etki: dünyada eşi az olan bir demo.*

### 7. Makam koması — mikrotonal eğitim
Türk makamları eşit olmayan aralıklar kullanır. El yatışı koma seviyesinde
detune kontrol etsin; öğrenci segah ile buselik farkını **eliyle hissetsin**.
Batı yazılımlarında olmayan, kültürel olarak sana ait bir alan. *Yeniden
kullanım: makam gamları + yatış sinyali. Zorluk: orta. Etki: farklılaşma.*

### 8. Air DJ / döngü istasyonu
Jestlerle katman kaydet, üstüne bindir, kanal sustur/aç. Bir şarkıyı canlı
canlı katmanlayarak kurarsın. *Yeniden kullanım: Akapella'nın kanal aç/kapa
mimarisi birebir uyar. Zorluk: orta.*

### 9. Gerçek enstrüman koçu
Kamera **gerçek gitarındaki** parmaklarına bakar, bastığın akoru şekilden
tanır: "Am basıyorsun ama 2. tel boşta kalmış." Air Chord'un tersi — sanal
değil gerçek enstrümanı düzeltir. *Zorluk: yüksek (perde tespiti gerekir).
Etki: en büyük eğitim pazarı burası.*

### 10. Düello modu — iki kişi tek kamera
`numHands: 2` zaten var; iki kişi karşılıklı oynar, biri akor diğeri melodi,
ya da sırayla akor yarışı. Video çıktısı hazır olduğu için doğrudan Reels
malzemesi. *Zorluk: orta. Etki: viral döngü.*

---

## Bölüm 3 — 10 ölçeklenebilir global fikir

### 11. İşaret dili alfabesi öğreticisi 🔥🔥
Aynı teknoloji, bambaşka bir amaç: TİD/ASL parmak alfabesini kameraya
gösterirsin, doğru yaptın mı anında geri bildirim alırsın. Her ülkenin kendi
işaret dili var → doğal olarak ölçeklenir, ve senin i18n hattın hazır.
Duolingo'nun yapamadığı şey bu: **elini görmesi gerekiyor.**
*Yeniden kullanım: el sınıflandırıcı mimarisi birebir. Etki: en yüksek sosyal
değer + en net global pazar.*

### 12. Erişilebilirlik — elle imleç
Fare kullanamayan insanlar için el ile imleç sürme ve bekleyerek tıklama.
Tarayıcıda, ücretsiz, özel donanım gerektirmeden. Piyasadaki çözümler
binlerce dolarlık cihazlar. *Zorluk: orta. Etki: hayat değiştiren erişim.*

### 13. Fizik tedavi hareket takibi
PoseLandmarker omuz/kol açıklığını ölçer, tekrar sayar, haftalar boyunca
ilerlemeyi grafikler. Yaşlanan nüfus + uzaktan sağlık. Tıbbi teşhis iddiası
olmadan "egzersiz takibi" olarak konumlandırılırsa düzenleme riski düşük.
*Zorluk: orta. Etki: gerçek ödeme isteği olan pazar.*

### 14. Sunum kumandası
Jestle slayt ilerlet, işaret parmağıyla lazer imleci, avuçla yakınlaştır.
Tarayıcıda çalışır, donanım yok. Kurumsal satışa uygun, küçük ve net bir ürün.
*Zorluk: düşük. Etki: hızlı gelir denemesi.*

### 15. Dans/koreografi eşleştirme
Bir dansı öğren, kamera duruş dizini referansla karşılaştırıp puan versin.
TikTok dansları = hazır viral döngü. *Yeniden kullanım: poz sınıflandırıcı +
video dışa aktarma. Zorluk: orta-yüksek (zaman hizalama).*

### 16. Sınıfta hareket molası
Öğretmen açar, ekrandaki pozları çocuklar taklit eder, sınıf birlikte hareket
eder. Okullara kurulum gerektirmeden girer, kelime öğretimiyle birleştirilirse
(pozu yap + kelimeyi söyle) dil eğitimine bağlanır. *Zorluk: düşük.
Etki: kurumsal dağıtım kanalı.*

### 17. Dokunmasız kontrol — mutfak, laboratuvar, atölye
Elleri kirli/eldivenli insanlar için tarif, kontrol listesi, teknik şema
sayfasını jestle çevirme. Hijyen zorunluluğu olan yerlerde gerçek ihtiyaç ve
ödeme isteği var. *Zorluk: düşük. Etki: B2B niş, yüksek marj.*

### 18. Egzersiz formu koçu
Şınav/squat sayarken diz açısı, sırt hizası gibi form hatalarını uyarır.
Ev sporunun en büyük sorunu yanlış form. *Zorluk: orta. Etki: devasa pazar,
ama rekabet de yoğun.*

### 19. Jestle sınıf katılımı / anket
Uzaktan derste "1-4 parmak göster" ile oylama, el kaldırma tespiti, yoklama.
Zoom/Meet yanında ikinci ekran olarak çalışır. *Yeniden kullanım: parmak
sayma zaten var. Zorluk: düşük.*

### 20. Yaşlı bakımında düşme ve hareketsizlik uyarısı
Poz verisi cihazda işlenir, **görüntü hiç çıkmaz** — bu senin mimarinin
doğal üstünlüğü, çünkü rakiplerin çoğu buluta video gönderiyor ve aileler
bundan çekiniyor. Yalnızca "düştü" olayı bildirilir. *Zorluk: yüksek
(yanlış alarm yönetimi + sorumluluk). Etki: en yüksek toplumsal fayda.*

---

## Bölüm 4 — Nereden başlamalı

**Bu hafta (küçük, yüksek getiri):** #1 çimdik kontrolcüsü ve #2 iki elli
enstrüman. İkisi de mevcut landmark verisiyle, yeni model indirmeden yapılır
ve Air Chord'u anında derinleştirir.

**Bu ay (ürünü büyütür):** #3 hayalet el ritim modu — `scores` tablosunu da
nihayet devreye sokar ve paylaşılabilir çıktı üretir.

**Ayrı ürün olarak düşün:** #11 işaret dili. ChordPlai'ın içine sıkıştırma;
aynı motoru kullanan kardeş site yap. Sosyal değeri, basın ilgisi ve global
ölçeklenmesi müzikten daha büyük olabilir.

**Önce şunu yap:** Vercel Analytics hâlâ kapalı. 20 fikirden hangisinin
tutacağını tahmin etmek yerine ölçerek öğrenmek varken, kaç kişinin hangi
bölümde vakit geçirdiğini bilmiyoruz.
