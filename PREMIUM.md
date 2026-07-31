# ChordPlai Premium — Gelir Sistemi ve 20 Özellik

*31 Temmuz 2026 · mevcut yapı sabit tutularak tasarlandı*

---

## 0. Başlangıç durumu (ölçüldü)

| | |
|---|---|
| Kayıtlı üye | **532** (`profiles` tablosu) |
| Ödeme/abonelik izi | **0** — sıfırdan kuruluyor |
| `scores` tablosu | şemada var, **hiç kullanılmıyor** |
| Kullanıcı verisi | **tamamı localStorage** — bulut senkronu yok, cihaz değişince her şey kaybolur |
| Analytics | **kapalı** — kimin neyi kullandığını bilmiyoruz |

Bu tablo iki şeyi söylüyor: (1) satacak gerçek bir eksik var — **bulut**, (2) ne
satacağımızı tahmin ediyoruz çünkü ölçmüyoruz.

---

## 1. Temel ilke: ücretsiz sürüm bozulmayacak

Bugün ücretsiz olan **hiçbir şey** paralı olmayacak. 532 kişi mevcut deneyimle
geldi; onu kısmak güveni yakar ve huniyi kurutur. Premium yalnızca **yeni**
yeteneklerle satılır.

Tek istisna, yeni gelen kapasite sınırlarıdır (bulut kaydı, uzun kayıt gibi) —
bunlar zaten bugün var olmayan şeyler.

---

## 2. Gerçek koruma vs. görüntüde koruma

Uygulamanın tamamı tarayıcıda çalışıyor. **İstemci tarafındaki kilit her zaman
kırılabilir.** Bunu kabul edip ona göre kurgulamak lazım:

- **Sunucu tarafında gerçekten korunabilenler** (Supabase RLS + Edge Function):
  bulut kütüphanesi, global sıralama, yerleşik AI, şarkı kütüphanesi, öğretmen
  paneli, e-posta raporları. → **Değerin ağırlığı buraya konmalı.**
- **Yalnızca istemcide olanlar** (uzun kayıt, filigransız dışa aktarma, ek
  kanallar, oyun modları): teknik olarak kırılabilir. Bunları "kırılırsa
  kaybederiz" diye değil, "çoğunluk zaten kırmaz, kırana da kızmayız" diye
  koyuyoruz. Kimseyi suçlayıcı uyarı/DRM eklemeyeceğiz.

---

## 3. Fiyatlandırma

| Plan | Türkiye | Global |
|---|---|---|
| Aylık | ₺149 | $5.99 |
| Yıllık | ₺1.190 (2 ay bedava) | $49 |
| Ömür boyu (ilk 500 kişi) | ₺2.490 | $99 |
| Öğretmen/Sınıf | ₺449/ay (30 öğrenci) | $19/ay |

**Kurucu Üye kampanyası:** mevcut 532 kişiye ömür boyu planı **₺999**'a, 14 gün
süreyle. Amaç gelirden çok **doğrulama**: kaç kişi para veriyor, hangi özellik
için? Bu veri olmadan yıllık fiyat körlemesine belirlenir.

---

## 4. Ödeme altyapısı

Türkiye'den global dijital satış için en pratik yol **Merchant of Record**
(Paddle veya Lemon Squeezy): KDV/vergi beyanını onlar üstlenir, sen tek
sözleşmeyle dünyaya satarsın. Yerel kart/taksit için **iyzico** veya **PayTR**
ikinci kanal olarak eklenir.

> ⚠️ Sağlayıcı seçimi öncesi güncel komisyon, Türkiye'ye ödeme (payout) ve
> şahıs şirketi/limited şartlarını **doğrulaman** gerekir; bu koşullar sık
> değişiyor ve tavsiye niteliğinde bir liste veriyorum, teyit senin.

**Akış:** Ödeme sağlayıcısı → webhook → Supabase Edge Function → `subscriptions`
tablosu → istemci oturumda `is_premium` görür.

```sql
create table public.subscriptions (
  user_id     uuid primary key references public.profiles(id) on delete cascade,
  plan        text not null,           -- 'monthly' | 'yearly' | 'lifetime' | 'teacher'
  status      text not null,           -- 'active' | 'past_due' | 'canceled'
  provider    text not null,
  provider_id text,
  renews_at   timestamptz,
  created_at  timestamptz not null default now()
);
alter table public.subscriptions enable row level security;
create policy "kendi aboneliğini görür" on public.subscriptions
  for select using (auth.uid() = user_id);

create or replace function public.is_premium()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.subscriptions
    where user_id = auth.uid() and status = 'active'
      and (renews_at is null or renews_at > now())
  )
$$;
```

Diğer tabloların RLS politikaları `is_premium()` çağırır — böylece bulut
özellikleri **gerçekten** korunur.

---

## 5. Hukuki gereklilik (satış başlayınca devreye girer)

Defensible kontrol listesinde **9. madde** ("ön bilgilendirme, cayma, iade")
"satış yok" diye atlanmıştı. Satış başlayınca **zorunlu** hale gelir:

- **Ön Bilgilendirme Formu** ve **Mesafeli Satış Sözleşmesi** (ödeme öncesi onay)
- **Cayma hakkı**: dijital içerikte, kullanıcı "hemen teslim" onayı verirse
  cayma hakkı düşer — bu onayı ödeme ekranında **açık kutucukla** almak gerekir
- İade politikası ve faturalandırma bilgisi
- `/kosullar` sayfasına ücretli plan maddeleri eklenmeli

Bunlar hazır olmadan ödeme almaya başlama.

---

# 20 Premium Özellik

Her özellikte: **[S]** = sunucu tarafında gerçekten korunur · **[İ]** = istemci
tarafı (kırılabilir) · Zorluk: 🟢 kolay · 🟡 orta · 🔴 zor

---

## A · Bulut ve Hesap (en güçlü satış argümanı)

### 1. Bulut Kütüphanesi **[S]** 🟢
Özel akorlar, presetler, not defteri içeriği, ayarlar — hepsi hesaba bağlı.
Telefondan başla, bilgisayarda devam et. *Bugün her şey localStorage'da: cihaz
değişince tamamı gidiyor. Kullanıcının en somut acısı bu.*

### 2. Sınırsız Şarkı Kaydı **[S]** 🟢
Ücretsiz: 3 şarkı bulutta. Premium: sınırsız + klasörleme + arama.

### 3. Global Sıralama ve Profil Sayfası **[S]** 🟡
`scores` tablosu şemada duruyor ama hiç kullanılmıyor. Ücretsiz: cihaz içi
skor. Premium: dünya sıralaması, ülke sıralaması, herkese açık profil
(`chordplai.com/u/ismail`), rozet vitrini.

### 4. Şarkı Geçmişi ve Sürümler **[S]** 🟡
Bir şarkının önceki hallerine dön, iki sürümü karşılaştır. Prova ederken
"dün daha iyiydi" durumunun çözümü.

---

## B · Akapella Pro (bayrak gemisinin derinleşmesi)

### 5. Uzun Kayıt **[İ]** 🟢
Ücretsiz 45 sn → Premium **5 dakika**. Tam bir şarkı kaydedilebilir hale gelir.

### 6. Stem Dışa Aktarma **[İ]** 🟡
Her ses ayrı **WAV** dosyası olarak iner. Logic/Ableton'a taşıyıp gerçek prodüksiyona
sokulabilir — bunu isteyen kitle zaten para ödemeye alışkın.

### 7. Filigransız ve Dikey Video **[İ]** 🟢
Ücretsiz sürümde köşede küçük "chordplai.com" filigranı (viral etki için
faydalı), Premium'da yok. Ayrıca **9:16 dikey** ve 1080p seçenekleri — Reels
için doğrudan hazır çıktı.

### 8. 12 Kanala Kadar Koro **[İ]** 🟡
6 → 12 ses. Kanal başına formant kaydırma (kadın/erkek ses rengi), ayrı reverb
gönderimi, kanal solo.

### 9. Akıllı Armoni Şablonları **[İ]** 🟡
"Gospel", "Barbershop", "Bulgar korosu", "Türk çoksesli", "Beach Boys" gibi
hazır aralık dizilimleri — tek tıkla 6 kanalı o stile kurar. *Aralık motoru
zaten var; bu yalnızca akıllı ön ayar.*

---

## C · Air Chord Pro

### 10. MIDI Dışa Aktarma **[İ]** 🟡
Air Chord performansını **.mid** olarak indir, DAW'a sürükle. Elinle çaldığın
akorlar gerçek bir MIDI parçasına dönüşür. *Prodüktör kitlesini açan kapı.*

### 11. Canlı MIDI Kontrolcü (WebMIDI) **[İ]** 🔴
ChordPlai'ı bir MIDI enstrümanı gibi kullan: Logic, Ableton, Kontakt'ı
elinle çal. Piyasada dengi az; teknik olarak en gösterişli özellik.

### 12. Özel Gam ve Makam Oluşturucu **[İ]** 🟡
13 hazır gamın dışına çık: kendi aralıklarını tanımla, adlandır, kaydet,
paylaş. Makam meraklıları ve deneysel müzisyenler için.

### 13. Performans Stüdyosu **[İ]** 🔴
Air Chord performansını kamera + ses miksiyle 1080p kaydet; çoklu çekim, en
iyi çekimi seç, basit kırpma. *Daha önce kaldırılan "video kaydı" özelliğinin
premium ve olgun hali.*

### 14. Ses Tasarımı Kiti **[İ]** 🟡
Ek synth tonları (yaylı pad, org, koro, sitar), kendi örneğini yükleyip
enstrüman yapma, efekt zinciri ön ayarları.

---

## D · Yapay Zekâ ve İçerik

### 15. Yerleşik Şarkı Asistanı **[S]** 🟡
Kopyala-yapıştır yok: şarkı sözünü yapıştır, akorlar ve el işaretleri
**doğrudan uygulamada** oluşsun. *Gerçek API maliyeti doğurur → aboneliği
doğrudan haklı çıkarır. Aylık adil kullanım kotasıyla.*

### 16. Hazır Şarkı Kütüphanesi **[S]** 🟡
El işaretleriyle hazırlanmış 100+ şarkı; Türkçe pop/rock ağırlıklı, aranabilir,
zorluk etiketli. *İçerik hendeği: kopyalanması en zor değer. Telif için
kullanıcı-üretimi + kamuya açık eserlerle başlanmalı.*

### 17. Otomatik Transpoze ve Ses Aralığı **[İ]** 🟢
"Bu şarkı sesime yüksek geliyor" → sesini bir kez ölçeriz, her şarkıyı sana
uygun tona çeviririz; gitarda kapo önerisi de verir.

---

## E · Öğrenme ve Öğretmen

### 18. İlerleme Takibi ve Haftalık Rapor **[S]** 🟡
Hangi akorda yanılıyorsun, hangi geçiş yavaş, seri kaç gün — oyunlardan gelen
veriyle. Haftalık e-posta özeti. *Verinin zaten üretildiği ama hiç
saklanmadığı yer burası.*

### 19. Kişisel Egzersiz Planı **[S]** 🔴
Zayıf olduğun akorları/geçişleri tespit edip her gün 10 dakikalık uyarlanabilir
alıştırma üretir. Aralıklı tekrar mantığıyla.

### 20. Öğretmen Paneli / Sınıf **[S]** 🔴
Öğretmen sınıf açar, öğrenci davet eder, ödev atar, ilerlemeyi tablo halinde
görür. **En yüksek fiyatlı katman** — bir öğretmen 30 öğrenciye ulaşır,
birim gelir en yüksek buradadır.

---

## 6. Uygulama sırası

**1. aşama — temel (bunlar olmadan satış yok):**
`subscriptions` tablosu + `is_premium()` + ödeme sağlayıcısı + webhook +
`/premium` sayfası + hukuki metinler.

**2. aşama — ilk paket (satılabilir en küçük set):**
#1 Bulut Kütüphanesi · #5 Uzun Kayıt · #7 Filigransız/dikey video ·
#10 MIDI dışa aktarma · #3 Global sıralama.
Beşi de mevcut altyapıya en yakın olanlar; ikisi gerçekten sunucu korumalı.

**3. aşama — derinlik:** #6, #8, #9, #15, #17
**4. aşama — yeni pazar:** #16, #18, #19, #20 (öğretmen katmanı)

## 7. Satıştan önce yapılması gereken tek şey

**Vercel Analytics'i aç.** 532 kişi var ama hangi bölümde vakit geçirdiklerini
bilmiyoruz. Yukarıdaki 20 özelliğin sıralaması şu an *mantıklı tahmin*;
iki haftalık kullanım verisiyle bu sıralama *bilgi* olur. Yanlış özelliği
önce yapmanın maliyeti, ölçmenin maliyetinden çok daha yüksek.
