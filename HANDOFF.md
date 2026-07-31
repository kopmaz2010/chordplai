# ChordPlai — Devir Dokümanı

> Bu dosya, projeyi devralan kişinin (ya da başka bir bilgisayardaki sen'in)
> hiçbir şey sormadan devam edebilmesi için yazıldı.
> **Son güncelleme:** 29 Temmuz 2026

---

## 1. Proje nedir?

**ChordPlai** — tarayıcıda çalışan Türkçe/çok dilli müzik uygulaması.
Ana özelliği **Air Chord**: web kamerasına el işareti göstererek akor çalarsın,
üzerine şarkı söylersin. Enstrüman gerekmez.

**Canlı:** https://chordplai.com
**Depo:** https://github.com/kopmaz2010/chordplai (public)

Yan modüller (ikinci kategori): akor egzersizi, nota oyunu, porte okuma,
Akor Ninja (mikrofonla akor tanıma), Akor Tetris.

---

## 2. Beş dakikada çalıştırma

```bash
git clone https://github.com/kopmaz2010/chordplai.git
cd chordplai
python3 -m http.server 8000     # tarayıcıda http://localhost:8000
```

> ⚠️ `file://` ile açma — localStorage ve kamera izinleri farklı davranır,
> giriş/otomatik başlatma akışları yanıltıcı sonuç verir. Hep HTTP kullan.
> Air Chord'un el-takip modeli CDN'den indiği için **internet gerekir**.

**Yayına alma:**

```bash
npx vercel deploy --prod --yes
```

İlk kez o makinede çalışıyorsan önce `npx vercel login` (hesap: `kopmaz2010`)
ve `npx vercel link` (takım `kopmaz2010s-projects`, proje `akor-antrenoru`).

> Vercel–GitHub bağlantısı **kurulu değil**; `git push` tek başına yayınlamaz.
> Deploy'u ayrıca çalıştırmalısın. (Bağlamak istersen: Vercel → proje →
> Settings → Git → Connect Git Repository. `vercel git connect` komutu
> GitHub App kurulu olmadığı için hata veriyor.)

---

## 3. Dosya haritası

| Yol | Ne |
|---|---|
| `index.html` | **Uygulamanın tamamı** (284 KB, 14 ayrı `<script>` IIFE modülü) |
| `build.py` | İçerik üreteci — blog HTML'i, i18n sözlükleri, sitemap |
| `content/blog.<dil>.json` | Blog içeriği (8 yazı × 6 dil) — **kaynak budur** |
| `content/ui.<dil>.json` | Arayüz sözlüğü (277 dize) |
| `content/ui.delta.<dil>.json` | Sonradan eklenen etiketler — build'de birleşir |
| `blog/` | **ÜRETİLMİŞ** 54 sayfa — elle düzenleme, build ezer |
| `i18n/<dil>.json` | **ÜRETİLMİŞ** çalışma-anı sözlükleri |
| `tasarim/sign/1..7.webp` | El işareti fotoğrafları (derece başına) |
| `tasarim/air-signs.webp` | 7 işaretin birlikte olduğu 16:9 görsel |
| `samples/` | Ritim sample'ları (kick/snare/hihat) + analogwaves |
| `supabase/schema.sql` | Üyelik veritabanı şeması |
| `sitemap.xml`, `robots.txt`, `llms.txt`, `og.png` | SEO varlıkları (sitemap üretilir) |

### İçerik değiştirdiysen

```bash
python3 build.py     # ZORUNLU — blog, i18n ve sitemap yeniden yazılır
```

---

## 4. Mimari — index.html nasıl kurulu?

Tek dosya, 14 bağımsız IIFE modülü. Aralarında `window.*` üzerinden konuşurlar.

**Yükleme sırası önemli:**
1. `<head>` → `CP_SUPA` (üyelik ayarı), `CP_LANG` + sözlük fetch'i başlar
2. `<body>` → görünümler, sonra modüller
3. En sonda → şarkı asistanı, not defteri, çeviri motoru, analytics

**Paylaşılan API'ler:** `window.AkorTheory` (gam/akor teorisi), `window.AkorPools`
(havuz kurucu), `window.AkorEngine` (mikrofon akor tanıma), `window.AkorPreview`
(hover akor önizleme), `window.CP_T(s)` (tek dize çevir).

**Test kancaları** (tarayıcı konsolundan): `__air`, `__np`, `__sa`, `__aiSet`,
`__nj`, `__tt`, `__sf`, `__ng`, `__acap`, `__airPose`. Örnek:

```js
window.__air.state()            // Air Chord durumu
window.__air.simPlay(1, 0, null)// 1. dereceyi kamerasız çal
window.__np.state()             // not defteri / prompter
window.__aiSet.parse("Ton = A · Gam/Makam = Kürdi")
window.__acap.load(f32, 44100)  // Akapella'ya sentetik ses ver (mikrofonsuz test)
window.__airPose.classify(lm)   // 33 noktalı sentetik iskelet → 0-7 poz
window.__airPose.step(1)        // pozu derece boru hattına sok (4× kararlılıkta çalar)
```

**Akapella (`#view-acap`)**: kayıt → otokorelasyon pitch analizi →
granüler pitch-shift ile 2-6 diyatonik ses → 6'lı video ızgara → WebM.
Demo melodi butonu mikrofonsuz uçtan uca test sağlar. Ton tahmini
son/ilk nota tonik sezgisi kullanır (C/G ayrımı için şart).

**Beden pozu modu**: Air Chord üst barındaki "🖐️ El / 🧍 Beden" butonu;
`akorAirBody` localStorage'da. PoseLandmarker lite tembel yüklenir
(~5 MB). 7 poz = 7 derece, iki kol aşağı = sus, poz kararlılığı 4 kare
(el işaretinden yavaş — kol hareketi büyük).

### Air Chord çalışma mantığı

- **Sol el** = gam derecesi (1–7 parmak işareti). Dik = gamın akoru,
  içe yatık = majör, dışa yatık = minör. ✊ = sustur.
- **Sağ el** = YALNIZ efekt. Sola eğ → distorsiyon, sağa çevir → dalga morph.
  Akora/gama dokunmaz (bilinçli tasarım kararı, değiştirme).
- El takibi MediaPipe `tasks-vision@0.10.14`, jsDelivr CDN'den dinamik import.
- Ses zinciri: osilatörler → bus → filtre → (kuru | reverb) → kompresör → çıkış.

---

## 5. Çok dillilik (6 dil: TR EN ES DE FR PT)

**Blog:** her dil ayrı URL, ayrı slug, hreflang'li. `/blog` (TR kök),
`/blog/en/...` vb. `build.py` üretir.

**Uygulama:** çalışma anı çevirisi. `CP_LANG` seçilir (`?lang=` → localStorage
→ tarayıcı dili → bilinmiyorsa `en`), `/i18n/<dil>.json` indirilir, DOM metin
düğümleri ve `placeholder/aria-label/title` öznitelikleri değiştirilir.
MutationObserver sonradan oluşan metinleri de yakalar.

**Yeni metin eklerken:**
1. Türkçesini HTML/JS'e yaz
2. `content/ui.delta.<dil>.json` dosyalarına 5 dilin karşılığını ekle
3. `python3 build.py`
4. `?lang=de` ile doğrula

> JS ile kurulan ve çevrilmiş etiket kullanan arayüzler (ör. akor tipi
> `<option>`'ları) `document.addEventListener("cp:i18n", ...)` olayına abone
> olup kendini yeniden kurmalı. `CP_DICT.then` ile beklemek **işe yaramaz** —
> modüller çeviri script'inden önce abone olur, sözlük daha dolmamıştır.

---

## 6. Üyelik (Supabase + Google)

- Proje: `cnpfhcjxxtboylvvqbfz` — **minortakvim hesabında**, `ChordPlai` org'u,
  Seul bölgesi. (Claude'un Supabase bağlayıcısı `kopmaz2010` hesabına bağlı,
  bu projeyi **göremez**; SQL/ayar işleri panelden yapılır.)
- Google OAuth istemcisi: GCP projesi `chordplai`,
  redirect `https://cnpfhcjxxtboylvvqbfz.supabase.co/auth/v1/callback`,
  origin `https://chordplai.com`.
- Giriş **yalnız Google** (takma ad yolu sadece Google'a erişilemezse yedek).
- Şu an **7 kayıtlı üye**. Liste: Supabase → Authentication → Users.

**Sağlık kontrolü:**

```bash
BASE=https://cnpfhcjxxtboylvvqbfz.supabase.co
ANON=<index.html içindeki CP_SUPA.anon>
curl -s "$BASE/auth/v1/settings" -H "apikey: $ANON" | grep -o '"google":[a-z]*'
curl -s -X POST "$BASE/rest/v1/rpc/user_count" -H "apikey: $ANON" \
     -H "Content-Type: application/json" -d '{}'
```

> `anon` anahtarın tarayıcıda olması **normaldir**. Güvenlik `schema.sql`'deki
> RLS politikalarındadır. `service_role` anahtarı ASLA istemciye koyma.

---

## 7. Kullanıcı akışı (tasarımın özü)

```
Siteye gir → Google ile giriş → kamera izni → Air Chord tam ekran
                                                    ↓
   Şarkı Asistanı: akorlu sözleri yapıştır → yapay zekâya gönder
                                                    ↓
   Dönen "ChordPlai AYARI: Ton = A · Gam = Kürdi" → ayar kutusuna yapıştır
   Dönen işaretli sözler → 📝 Notlar paneline yapıştır
                                                    ↓
              🎬 Prompter'ı başlat → elini kaldır → söyle
```

Prompter'da emojiler **otomatik olarak el fotoğraflarına** dönüşür; gamın
kendi akoru olmayanlarda işaretin sağında **▸** (içe yatır/majör) veya
**◂** (dışa yatır/minör) oku çıkar.

---

## 8. ⚠️ Tuzaklar — buraya bak, zaman kaybetme

**CSS**

- `display:flex/grid` verilen bir öğede `hidden` özniteliği **ezilir**.
  Her overlay için `[hidden] { display: none }` yaz. (`.air-idle`, `.np-body`
  ve `#gateFallback`'te üçü de bu yüzden bozulmuştu.)
- Genel sınıf adlarından kaçın: dizgeç hücrelerine `.beat` demek metronom
  noktalarının stiliyle çakıştı, `.bt`'ye çevrildi.
- `calc()` içinde kullanılan özel değişkenler geçişte **bir kare geriden**
  gelir. Çözüm: `@property { syntax: "<number>" }` ile kaydet
  (`--cam`, `--dock-op`, `--np-op` böyle). Boyut değişimlerinde ayrıca
  `transition` koyma — tuval yeniden ölçümü kaçıyor.
- `input[type=range]` dolgusu `--fill` değişkeninden gelir; global bir script
  her `input` olayında günceller. Yeni fader eklersen otomatik çalışır.
- Prompter satırlarında `white-space: pre-wrap` + monospace **şart** —
  HTML ardışık boşlukları eziyor, yapay zekânın hizalaması bozuluyor.

**JavaScript**

- `requestAnimationFrame` arka planda/önizlemede **kısılıyor**. Oyun döngüleri
  ve tuval yeniden ölçümü `setInterval` ya da doğrudan çağrı kullanır.
- Modül IIFE'lerinde kablolama bloğu `const` tanımlarından önce çalışırsa
  TDZ hatası modülü **sessizce** öldürür (konsolda görünmez). Kablolamayı
  hep tanımların sonrasına koy.
- `document` üzerindeki keydown dinleyicilerinde `e.target instanceof Element`
  guard'ı olmadan `.matches()` patlar.
- Akor eki araması **büyük/küçük harfe duyarlı** olmalı: `M13` majör,
  `m13` minör. Küçük harfe indirgeyen tek harita `Dm13 → Dmaj13` hatası verdi.
- **localStorage değerini modül kapsamında önbelleğe alma.** Modüller
  bağımsız IIFE; biri yazınca diğerinin değişkeni bayat kalır ve hata
  yalnızca "sayfayı yenileyince düzeliyor" şeklinde görünür. Nota oyunu
  `PLAYER`'ı yüklemede okuyordu, üyelik modülü girişte `akorPlayer`'ı
  yazıyordu → Başla → kapı → giriş → Başla → kapı döngüsü. Çözüm:
  yazan taraf `document.dispatchEvent(new CustomEvent("cp:player"))`,
  okuyan taraf dinleyip tazeliyor (`cp:i18n` ile aynı desen). Ya her
  kullanımda localStorage'dan oku, ya da olayla tazele — ikisinin arası yok.
- Girişin bir eylemi bölmesi gerekiyorsa niyeti sakla (`pendingStart`) ve
  giriş bitince sürdür; yoksa kullanıcı butona ikinci kez basmak zorunda
  kalır ve bunu hata sanar.
- `window.__airAutoStart` gibi otomatik başlatıcıları çağırmadan önce
  **o görünüm açık mı** diye bak. Nota oyunundan giriş yapan kullanıcının
  karşısına kamera izni çıkıyordu.
- **Beden pozu görselleri AYNALANMIŞ tutulur.** Kamera `scaleX(-1)` ile ayna
  görünümünde: kullanıcının sağ kolu ekranın sağında görünür. Model fotoğrafı
  aynalanmazsa (karşıdan çekilmiş fotoğrafta modelin sağ kolu solda görünür)
  kullanıcı gördüğü kolu taklit edip **ters kolu** kaldırır ve yanlış akor
  çalar. Yeni poz görseli eklerken `Image.FLIP_LEFT_RIGHT` uygulanmalı;
  metin tarifleri ise anatomik kalır ("sağ kol yukarı").
- Kanvas öğesine **açık CSS yüksekliği** ver. Yoksa öğe yüksekliği kanvasın
  `dpr`'li iç yüksekliğine oturur, fare koordinatı ölçeği ikiye katlanır.
  Ölçeği daima `getBoundingClientRect()`'ten hesapla, `dpr` varsayma.
- Gizli öğede `clientWidth` **0**'dır; o anda kanvas çizmek boş kare bırakır
  (akapella piano-roll'u böyle boş kalıyordu). Önce göster, sonra çiz.
- JS'te birleştirilen cümleler i18n TreeWalker'ına yakalanmaz (anahtar tam
  metindir). Parçaları `window.CP_T()` ile tek tek çevir.
- Yerel sunucuda `i18n/<dil>.json` **tarayıcı önbelleğinde** kalır; çeviri
  gelmiyorsa önce sayfayı tazele, koda dokunma.
- **Oyun kokpiti ortak**: Yılan/Ninja/Tetris aynı `.snk-cockpit` iskeletini
  kullanır (sol kamera+parametre sütunu, sağ sahne+HUD, `.gk-full` ile tam
  ekran, `.snk-page-only` sayfa-modu blokları). `snk-` öneki tarihsel —
  yılanda doğdu, üçü de kullanıyor. Yeni oyun eklerken bu iskeleti kopyala.
- **Kamera önizlemesi `CP_camPreview.attach(video)` ile alınır** — motor
  akışına güvenme: AkorEngine daha önce ses-yalnız başladıysa
  (`ENG.running` kısa devresi) akışta video hiç olmaz; yardımcı gerekirse
  bağımsız video akışı açar ve `play()` çağırır. Çıkışta `release()`.

**Türkçe/i18n**

- `text-transform: uppercase` + Türkçe locale "i"yi "İ" yapar. Marka
  başlıklarında `lang="en"` + `text-transform: none` şart, yoksa "CHORDPLAİ".
- Yapay zekâya giden promtta emoji **kalmalı** (metin olarak gidiyor);
  arayüzde el fotoğrafı kullanılır. Çevrilmiş cümlelerin içindeki emojilere
  dokunma — i18n anahtarları kırılır.

**Test ortamı**

- Claude'un önizleme paneli sık sık bozuluyor: `innerWidth` 0'a düşüyor,
  `getComputedStyle` bayat değer döndürüyor (`!important` bile değiştirmiyor),
  ekran görüntüsü beyaz çıkıyor. **Ölçüme değil ekran görüntüsüne güven**;
  gerekirse yeni sekme aç + `resize_window`.

---

## 9. Yapılmayanlar / sıradakiler

| Konu | Durum | Kim yapabilir |
|---|---|---|
| **Vercel Web Analytics** | Kod ekli, panelden **açılmadı** (`/_vercel/insights/script.js` 404) | Vercel → proje → Analytics → Enable (1 tık) |
| **Google Search Console** | Site eklenmedi, sitemap gönderilmedi | Google hesabı gerekir |
| **GCP OAuth consent screen** | "Testing"te kalmış olabilir → sadece test kullanıcıları girebilir | PUBLISH APP (kapsamlar hassas değil, anında) |
| **Vercel–GitHub bağlantısı** | Yok; deploy elle | Vercel panelinden bağlanabilir |
| **Cihazlar arası liderlik tablosu** | `scores` tablosu hazır, uygulamaya bağlanmadı | geliştirme |
| **Supabase bölgesi** | Seul — TR'den ~250 ms | taşımak isterse yeniden kurulum |

**Kaldırılan özellikler** (geri isteme ihtimaline karşı): sampler pad,
video kaydı (Reels/YouTube) ve vokal harmonizer 29 Tem'de kullanıcı isteğiyle
tamamen silindi. Git geçmişinde `f886126` öncesinde duruyor.

---

## 10. Kimde ne var?

| Şey | Hesap / yer |
|---|---|
| Alan adı | Hostinger (`kopmaz2015@gmail.com`), DNS de orada |
| Hosting | Vercel — `kopmaz2010s-projects` / `akor-antrenoru` |
| Depo | GitHub — `kopmaz2010/chordplai` |
| Veritabanı + auth | Supabase — **minortakvim** hesabı, `ChordPlai` org |
| Google OAuth | GCP projesi `chordplai` |
| Marka/logo | `tasarim/` + Masaüstü `chordplai-logo/` (SVG varyantları) |

DNS: `A @ → 76.76.21.21`, `CNAME www → cname.vercel-dns.com`.
`www` ve `http` → `https://chordplai.com`'a 308 ile yönlenir (`vercel.json`).

---

## 11. Hızlı sağlık kontrolü

```bash
# sayfalar
for u in "" blog blog/en sitemap.xml robots.txt llms.txt og.png \
         tasarim/sign/1.webp i18n/en.json; do
  printf "%-24s %s\n" "/$u" "$(curl -s -o /dev/null -w '%{http_code}' https://chordplai.com/$u)"
done

# yönlendirmeler (308 beklenir)
curl -sI https://www.chordplai.com/ | head -1

# JS sözdizimi (dosyayı elle düzenlediysen)
node --input-type=module -e '
const fs=await import("fs"); const h=fs.readFileSync("index.html","utf8");
const re=/<script([^>]*)>([\s\S]*?)<\/script>/g; let m,i=0,bad=0;
while((m=re.exec(h))){ if(/src=|ld\+json/.test(m[1]||"")) continue; i++;
  try{ new Function(m[2]); }catch(e){ bad++; console.log("HATA",i,e.message); } }
console.log(i+" blok, "+bad+" hatalı");'
```

---

## 12. Çalışma alışkanlığı

Her anlamlı değişiklikten sonra:

```bash
python3 build.py                          # içerik değiştiyse
npx vercel deploy --prod --yes            # canlıya
git add -A && git commit -m "..." && git push
```

Değişikliği **canlıda doğrula** — bu projede pek çok hata yalnız gerçek
tarayıcıda ortaya çıktı (kamera izinleri, localStorage, CSS geçişleri).
