# ChordPlai Üyelik Kurulumu — Kalan 2 Adım

Proje: **chordplai** · `cnpfhcjxxtboylvvqbfz` · bölge: Seul

| Durum | Adım |
|---|---|
| ✅ | Supabase projesi açıldı |
| ✅ | Anon key siteye yazıldı, bağlantı çalışıyor (canlıda doğrulandı) |
| ✅ | Google giriş butonu + profil kartı + üye sayacı kodu canlıda |
| ⬜ | **1. Veritabanı şeması** — aşağıda |
| ⬜ | **2. Google ile giriş** — aşağıda |

---

## 1️⃣ Veritabanı şeması (2 dakika)

Bu adım olmadan giriş yapılsa bile profil kaydedilmez ve üye sayacı görünmez.

1. Şunu aç: **https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/sql/new**
2. Bu repodaki **`supabase/schema.sql`** dosyasının tamamını kopyala, editöre yapıştır.
3. Sağ alttaki **Run**'a bas. "Success" yazmalı.

Kurulanlar: `profiles` tablosu (RLS'li), yeni kayıt olunca profili otomatik oluşturan
tetikleyici, footer'daki üye sayacını besleyen `user_count` fonksiyonu ve ileride
cihazlar-arası liderlik tablosu için `scores` tablosu.

> 🔒 **RLS neden önemli:** anon anahtarı tarayıcıya gider (tasarımı böyle, normaldir).
> Verini koruyan şey bu SQL'deki RLS politikalarıdır — herkes isim/avatar okuyabilir,
> ama kimse başkasının satırını değiştiremez. Bu yüzden bu adımı atlama.

---

## 2️⃣ Google ile giriş (10 dakika)

Şu an kapalı — butona basınca "Google girişi şu an kapalı" uyarısı çıkar.

**a) Google tarafı** — https://console.cloud.google.com

1. Yeni proje oluştur: `chordplai`
2. **APIs & Services → OAuth consent screen** → **External** → uygulama adı "ChordPlai",
   destek e-postası ve geliştirici e-postası: `kopmaz2015@gmail.com` → Save
3. **Credentials → Create credentials → OAuth client ID → Web application**:
   - **Authorized JavaScript origins:**
     ```
     https://chordplai.com
     ```
   - **Authorized redirect URIs:**
     ```
     https://cnpfhcjxxtboylvvqbfz.supabase.co/auth/v1/callback
     ```
4. Çıkan **Client ID** ve **Client Secret**'ı kopyala.

**b) Supabase tarafı**

1. **https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/auth/providers**
   → **Google** → Client ID + Secret yapıştır → **Enable** → Save
2. **https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/auth/url-configuration**
   → **Site URL:** `https://chordplai.com`

Bitince https://chordplai.com'da giriş kapısındaki beyaz butondan Google'la girilir;
sağ üstte avatarın çıkar, footer'da "👥 N üye" görünür.

---

## 📊 Ziyaretçi sayısı (üyelikten bağımsız, 1 tık)

Vercel Web Analytics kodu sitede kurulu ama panelden açılması gerekiyor:
**https://vercel.com/kopmaz2010s-projects/akor-antrenoru** → **Analytics** → **Enable**.
Açtığın andan itibaren günlük ziyaretçi ve sayfa görüntüleme sayıları orada birikir
(Hobby planda ücretsiz).

---

## Kaç üyem var, nereden bakarım?

- **Sitede:** ana sayfa footer'ında "👥 N üye" (1. adımdan sonra görünür)
- **Detaylı:** https://supabase.com/dashboard/project/cnpfhcjxxtboylvvqbfz/auth/users
  — kim, hangi e-posta, ne zaman katıldı, en son ne zaman girdi
