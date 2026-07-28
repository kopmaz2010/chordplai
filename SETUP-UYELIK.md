# ChordPlai Üyelik Kurulumu (Google ile Giriş)

Kod tarafı **hazır** — site, aşağıdaki iki değer doldurulunca üyeliği kendiliğinden açar:

```js
// index.html'in en altında:
window.CP_SUPA = {
  url:  "",   // ← Supabase Project URL
  anon: "",   // ← Supabase anon/publishable key
};
```

Doldurulmadığı sürece üyelik UI'ları gizli kalır, site bugünkü gibi çalışır.

## 1. Supabase'te yer aç (tek engel bu!)

Hesabın (kopmaz2010) **2 aktif ücretsiz proje limitine** takılı. Admin olduğun
diğer organizasyondaki projelerden birini **Pause** et (Dashboard → o proje →
Settings → General → Pause project) ya da sil. Sonra:

- https://supabase.com/dashboard → **New project** → isim: `chordplai`,
  bölge: `eu-central-1 (Frankfurt)` (Türkiye'ye en yakın).
- (İstersen bunun yerine mevcut "kopmaz2010's Project"i **Restore** da edebilirsin.)

## 2. Anahtarları al

Proje açılınca: **Settings → API**
- `Project URL` → `CP_SUPA.url`
- `anon public` key → `CP_SUPA.anon`

Bu iki değeri `index.html` en altındaki `CP_SUPA`'ya yapıştır, deploy et.
(anon key tarayıcıya konması **normaldir**; güvenlik RLS politikalarında.)

## 3. Veritabanı şemasını kur

Dashboard → **SQL Editor** → bu repodaki `supabase/schema.sql` dosyasının
içeriğini yapıştır → **Run**. (Profiller, otomatik profil tetikleyicisi,
üye sayacı ve gelecekteki liderlik tablosu kurulur.)

## 4. Google ile girişi aç

1. https://console.cloud.google.com → proje oluştur (`chordplai`).
2. **APIs & Services → OAuth consent screen** → External → uygulama adı
   "ChordPlai", destek e-postası seç → kaydet.
3. **Credentials → Create credentials → OAuth client ID** → Web application:
   - Authorized JavaScript origins: `https://chordplai.com`
   - Authorized redirect URIs: `https://<PROJE-REF>.supabase.co/auth/v1/callback`
     (Supabase → Authentication → Providers → Google sayfası bu URI'yi aynen gösterir, oradan kopyala)
4. Çıkan **Client ID** ve **Client Secret**'ı Supabase → **Authentication →
   Providers → Google**'a yapıştır, **Enable** et.
5. Supabase → **Authentication → URL Configuration** → Site URL:
   `https://chordplai.com`

## 5. Deploy

```bash
cd ~/akor-antrenoru && npx vercel deploy --prod --yes
```

## Sonuç — neler açılır?

- Giriş kapısında beyaz **"Google ile giriş yap"** butonu (takma adla devam da kalır).
- Sağ üstte **profil çipi**: Google avatarı + isim; tıklayınca profil kartı
  (e-posta, bu cihazdaki oyun sayısı, çıkış).
- Footer'da **"👥 N üye"** sayacı — kaç kullanıcın olduğunu herkes görür;
  detaylar Supabase Dashboard → Authentication → Users'da.
- `scores` tablosu hazır: istediğinde cihazlar-arası liderlik tablosunu bağlarız.

## Kaç kişi siteyi ziyaret ediyor? (üyelikten bağımsız)

Vercel Web Analytics kodu siteye eklendi ama Vercel tarafında bir kez elle
açman gerekiyor: https://vercel.com/kopmaz2010s-projects/akor-antrenoru →
**Analytics** sekmesi → **Enable**. Açtığın andan itibaren ziyaretçi/sayfa
görüntüleme sayıları o sekmede birikir (Hobby planda ücretsiz).
