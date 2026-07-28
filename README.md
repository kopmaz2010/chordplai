# ChordPlai 🖐️🎸

**https://chordplai.com** — kamerayla elinle akor çal (Air Chord), üzerine söyle,
Reels/YouTube videonu kaydet. Ayrıca gitar & piyano akor egzersizleri, nota oyunu,
porte okuma, Akor Ninja ve Akor Tetris.

Tek dosyalık istemci uygulaması: `index.html` (MediaPipe el takibi + Web Audio).
Statik ekler: `blog/`, `og.png`, `sitemap.xml`, `robots.txt`, `llms.txt`,
`samples/` (kullanıcı ritim sample'ları), `supabase/schema.sql` (üyelik şeması).

## Yayınlama (deploy)

Vercel projesi: `kopmaz2010s-projects/akor-antrenoru` → `chordplai.com` alias'lı.

```bash
cd akor-antrenoru
npx vercel deploy --prod --yes
```

## Başka bilgisayardan çalışmak

İlk kurulum (bir kez):

```bash
git clone https://github.com/kopmaz2010/chordplai.git
cd chordplai
npx vercel login          # kopmaz2010 hesabıyla
npx vercel link           # takım: kopmaz2010s-projects, proje: akor-antrenoru
```

Günlük akış:

```bash
git pull                  # son hali al
# ... düzenle ...
git add -A && git commit -m "değişiklik"
git push                  # GitHub'a yolla
npx vercel deploy --prod --yes   # canlıya al
```

> 💡 İstersen Vercel'i GitHub'a bağla, `git push` tek başına yayınlasın:
> vercel.com → Dashboard → akor-antrenoru → Settings → Git → **Connect Git
> Repository** → GitHub'da Vercel uygulamasını kur → `kopmaz2010/chordplai` seç.
> Bağlandıktan sonra `main`'e her push otomatik production deploy olur ve
> `npx vercel deploy` adımına gerek kalmaz.

## Üyelik (Google ile giriş)

Kod hazır, tek eksik Supabase yapılandırması — adım adım: **SETUP-UYELIK.md**.

## Ziyaretçi istatistikleri

Vercel Web Analytics script'i ekli; Vercel panelinde **Analytics → Enable**
yapınca saymaya başlar (SETUP-UYELIK.md sonunda anlatıldı).
