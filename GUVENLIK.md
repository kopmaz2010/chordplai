# Güvenlik Denetimi — 31 Temmuz 2026

Bütün site tarandı: veritabanı yetkileri, sırlar, XSS yüzeyleri, HTTP
başlıkları, dosya erişimi. Aşağıdaki her madde **test edilerek** bulundu ve
düzeltmeler **canlıda doğrulandı**.

---

## 🔴 KRİTİK — senin yapman gereken (tek adım kaldı)

### 553 üyenin e-postası dışarıdan listelenebiliyor

`profiles` tablosundaki politika `for select using (true)` idi. `anon`
anahtarı sitede herkese açık olduğu için (bu normaldir, koruma RLS'ten gelir)
internetteki herkes tek istekle tüm üye listesini çekebiliyor.

Doğrulandı: 553 satır, 553 e-posta, ad ve avatar okunabiliyor.

**Kök neden:** RLS *satır* bazlıdır, *sütun* bazlı değildir. Liderlik tablosu
için takma adı açmak istenmiş, aynı politika e-postayı da açmış.

**Düzeltme hazır:** `supabase/fix-profiles-rls.sql` — panelde çalıştır:

```
https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/sql/new
```

Tabloyu kendi satırına kilitler, herkese açık alanları (`display_name`,
`avatar_url`) ayrı bir `public_profiles` görünümüyle verir. Uygulamayı
kırmaz: kod `profiles`'ı yalnızca kendi satırını yazmak için kullanıyor,
üye sayacı `security definer` olduğu için etkilenmiyor.

> Bunu ben çalıştıramıyorum: proje `minortakvim` hesabında, bağlayıcım
> göremiyor. KVKK açısından bugün kapatılmalı.

---

## ✅ KAPATILDI — canlıda doğrulandı

### 1. Clickjacking / kamera hırsızlığı
Hiçbir çerçeveleme koruması yoktu. Site kamera ve mikrofon izni istediği için
kötü niyetli bir sayfa ChordPlai'ı görünmez bir iframe'e alıp kullanıcıyı
kendi kamerasını açmaya kandırabilirdi.
→ `frame-ancestors 'none'` + `X-Frame-Options: DENY`

### 2. İzin sızıntısı
→ `Permissions-Policy`: kamera/mikrofon yalnız `self`; konum, ödeme, USB ve
tüm hareket sensörleri **tamamen kapalı**.

### 3. Content-Security-Policy yoktu
→ Gerçek kullanım listesinden türetilmiş CSP: `connect-src` yalnız Supabase +
jsDelivr + model deposu, `object-src 'none'`, `base-uri`/`form-action 'self'`,
`frame-src` yalnız Google girişi.

### 4. Kaynak dosyalar canlıda servis ediliyordu
`/supabase/schema.sql` (tablo yapısı **ve RLS politikaları**), `/build.py`,
`/HANDOFF.md` (hesap adları, proje kimlikleri, mimari, bilinen tuzaklar) —
hepsi 200 dönüyordu. Saldırgan için hazır yol haritası.
→ `.vercelignore` ile yayından çıkarıldı, hepsi artık **404**.

### 5. Diğer başlıklar
`X-Content-Type-Options: nosniff` · `Referrer-Policy:
strict-origin-when-cross-origin` · `Cross-Origin-Opener-Policy` ·
DNS-prefetch kapalı.

---

## ✅ DENETLENDİ — sorun bulunmadı

| Alan | Sonuç |
|---|---|
| **Yazma yetkisi** | anon anahtarla sahte profil ve sahte skor yazma denendi → ikisi de RLS ile **reddedildi** |
| **XSS** | Liderlik tabloları `esc()`, prompter satırları `&<>` kaçırılıyor, preset adları temizleniyor, özel akor değerleri öznitelik bağlamında kaçırılıyor, profil adları `textContent` |
| **Tehlikeli kalıplar** | `eval` 0 · `new Function` 0 · `document.write` 0 |
| **Depoda sır** | `service_role` yok, `client_secret` yok, `.env` yok — git geçmişindeki eşleşmeler yalnızca uyarı yorumları |
| **Açık yönlendirme** | OAuth `redirectTo` sabit `https://chordplai.com` |
| **`.git` erişimi** | 404 |

---

## ⚠️ Bilinen sınırlar (dürüstçe)

**`script-src` içinde `'unsafe-inline'` var.** Uygulamanın tamamı satır içi
script olduğu için zorunlu; bu, CSP'nin XSS'e karşı koruma gücünü ciddi
biçimde azaltır. Asıl koruma kaçırma katmanında ve o denetlendi. Nonce tabanlı
CSP'ye geçmek ayrı bir yeniden yapılandırma işi — ileride yapılmalı.

**Oturum jetonu `localStorage`'da.** Supabase'in tarayıcı varsayılanı; statik
sitede httpOnly çerezine geçmek sunucu katmanı ister. Bir XSS olursa jeton
çalınabilir — bu yüzden yukarıdaki XSS denetimi ve CSP önemli.

**`wasm-unsafe-eval` gerekli.** MediaPipe'ın WebAssembly'si olmadan
çalışmıyor (yayın öncesi test edilerek bulundu). Tam `unsafe-eval`'den çok
daha dar bir izin.

---

## Regresyon (CSP altında, canlı)

8 görünümün hepsi açılıyor · MediaPipe el **ve** beden modelleri yükleniyor ·
yılan + metronom çalışıyor · akapella 13/13 nota buluyor · 34 görsel yükleniyor
· jsDelivr, Supabase ve model deposu erişilebilir · **0 CSP ihlali** · konsol
temiz.
