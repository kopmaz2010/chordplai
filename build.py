#!/usr/bin/env python3
"""ChordPlai blog üreteci — content/blog.<lang>.json → blog/ altında statik HTML.

Kullanım:  python3 build.py
Üretilenler:
  blog/index.html               (TR blog dizini)
  blog/<slug>.html              (TR yazılar — mevcut URL'ler korunur)
  blog/<lang>/index.html        (diğer diller)
  blog/<lang>/<slug>.html
  blog/blog.css                 (ortak stil)
  sitemap.xml                   (tüm diller + hreflang)
"""
import json, os, re, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
OUT = os.path.join(ROOT, "blog")
SITE = "https://chordplai.com"
BASE_LANG = "tr"                       # kök dilde /blog, diğerlerinde /blog/<lang>
LANGS = ["tr", "en", "es", "de", "fr", "pt"]

MARK = ('<svg viewBox="0 0 120 120" aria-hidden="true">'
        '<path d="M74 30 A28 28 0 1 0 74 90" fill="none" stroke="#efe6d2" stroke-width="11" stroke-linecap="round"/>'
        '<g stroke="#f5c264" stroke-width="11" stroke-linecap="round" fill="none">'
        '<line x1="74" y1="26" x2="74" y2="98"/><path d="M74 30 h10 a17 17 0 0 1 0 34 h-10"/></g>'
        '<circle cx="46" cy="60" r="6" fill="#ffd98a"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'%3E"
           "%3Crect width='120' height='120' rx='26' fill='%2314110b'/%3E"
           "%3Cpath d='M74 30 A28 28 0 1 0 74 90' fill='none' stroke='%23efe6d2' stroke-width='11' stroke-linecap='round'/%3E"
           "%3Cg stroke='%23f5c264' stroke-width='11' stroke-linecap='round' fill='none'%3E"
           "%3Cline x1='74' y1='26' x2='74' y2='98'/%3E%3Cpath d='M74 30 h10 a17 17 0 0 1 0 34 h-10'/%3E%3C/g%3E"
           "%3Ccircle cx='46' cy='60' r='6' fill='%23ffd98a'/%3E%3C/svg%3E")

CSS = """
:root { --bg:#14110b; --panel:#241d13; --line:#3a3020; --amber:#f5c264; --amber-hot:#ffd98a; --cream:#efe6d2; --muted:#b8ab90; }
* { box-sizing: border-box; margin: 0; }
body { background: var(--bg); color: var(--cream); font: 16px/1.75 -apple-system, "Segoe UI", Roboto, sans-serif; -webkit-text-size-adjust: 100%; }
.wrap { max-width: 720px; margin: 0 auto; padding: 24px 20px 60px; }
header.site { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; padding-bottom: 16px; border-bottom: 1px solid var(--line); margin-bottom: 26px; }
header.site svg { width: 34px; height: 34px; flex: 0 0 auto; }
header.site .home { color: var(--cream); text-decoration: none; font-weight: 700; letter-spacing: .22em; }
header.site .home b { color: var(--amber-hot); font-weight: 700; }
header.site .crumb { margin-left: auto; font-size: .8rem; }
header.site .crumb a { color: var(--amber); text-decoration: none; }
a { color: var(--amber); }
h1 { font-size: clamp(1.4rem, 4.4vw, 1.7rem); line-height: 1.3; margin-bottom: 10px; }
.lead { color: var(--muted); margin-bottom: 26px; }
.meta { font-size: .78rem; color: var(--muted); letter-spacing: .06em; margin-bottom: 24px; }
.post { display: block; background: var(--panel); border: 1px solid var(--line); border-radius: 14px; padding: 18px 20px; margin-bottom: 14px; text-decoration: none; transition: border-color .15s, transform .15s; }
.post:hover { border-color: var(--amber); transform: translateY(-1px); }
.post h2 { color: var(--amber-hot); font-size: 1.12rem; margin-bottom: 6px; line-height: 1.35; }
.post p { color: var(--muted); font-size: .92rem; }
.post .date { font-size: .72rem; color: var(--muted); opacity: .65; letter-spacing: .08em; }
article h2 { color: var(--amber-hot); font-size: 1.18rem; margin: 30px 0 10px; line-height: 1.35; }
article p { margin-bottom: 14px; }
article ul, article ol { margin: 0 0 14px 22px; }
article li { margin-bottom: 6px; }
.box { background: var(--panel); border: 1px solid var(--line); border-left: 3px solid var(--amber); border-radius: 10px; padding: 14px 16px; margin: 18px 0; font-size: .95rem; }
.tw { overflow-x: auto; margin: 14px 0; }
table { border-collapse: collapse; width: 100%; min-width: 380px; font-size: .9rem; }
th, td { border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top; }
th { color: var(--amber-hot); background: var(--panel); }
.cta { margin-top: 34px; text-align: center; }
.cta a { display: inline-block; background: linear-gradient(180deg, #f8d488, #eab04c); color: #241a06; font-weight: 700; text-decoration: none; padding: 13px 26px; border-radius: 12px; }
.langs { display: flex; gap: 6px; flex-wrap: wrap; margin: 26px 0 0; padding-top: 16px; border-top: 1px solid var(--line); }
.langs a, .langs span { font-size: .74rem; padding: 5px 10px; border-radius: 8px; border: 1px solid var(--line); text-decoration: none; color: var(--muted); }
.langs a:hover { border-color: var(--amber); color: var(--cream); }
.langs .on { border-color: var(--amber); color: var(--amber-hot); }
footer { margin-top: 26px; padding-top: 16px; border-top: 1px solid var(--line); font-size: .8rem; color: var(--muted); }
""".strip()


def load():
    data = {}
    for lg in LANGS:
        p = os.path.join(CONTENT, "blog.%s.json" % lg)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                data[lg] = json.load(f)
    return data


def post_url(lg, slug):
    return "/blog/%s" % slug if lg == BASE_LANG else "/blog/%s/%s" % (lg, slug)


def index_url(lg):
    return "/blog" if lg == BASE_LANG else "/blog/%s" % lg


def out_path(lg, name):
    d = OUT if lg == BASE_LANG else os.path.join(OUT, lg)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, name)


def head(lg, data, title, desc, canonical, alts, jsonld, og_type="website"):
    """alts: {lang: url} — hreflang seti."""
    L = []
    A = L.append
    A('<!doctype html>')
    A('<html lang="%s">' % lg)
    A('<head>')
    A('<meta charset="utf-8">')
    A('<meta name="viewport" content="width=device-width, initial-scale=1">')
    A('<meta name="theme-color" content="#14110b">')
    A('<title>%s</title>' % html.escape(title))
    A('<meta name="description" content="%s">' % html.escape(desc, quote=True))
    A('<link rel="canonical" href="%s%s">' % (SITE, canonical))
    for l2, u2 in alts.items():
        A('<link rel="alternate" hreflang="%s" href="%s%s">' % (l2, SITE, u2))
    if BASE_LANG in alts:
        A('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, alts.get("en", alts[BASE_LANG])))
    A('<meta property="og:type" content="%s">' % og_type)
    A('<meta property="og:site_name" content="ChordPlai">')
    A('<meta property="og:title" content="%s">' % html.escape(title, quote=True))
    A('<meta property="og:description" content="%s">' % html.escape(desc, quote=True))
    A('<meta property="og:url" content="%s%s">' % (SITE, canonical))
    A('<meta property="og:image" content="%s/og.png">' % SITE)
    A('<meta property="og:locale" content="%s">' % data.get("locale", "tr_TR"))
    A('<meta name="twitter:card" content="summary_large_image">')
    A('<meta name="twitter:title" content="%s">' % html.escape(title, quote=True))
    A('<meta name="twitter:description" content="%s">' % html.escape(desc, quote=True))
    A('<meta name="twitter:image" content="%s/og.png">' % SITE)
    A('<link rel="icon" href="%s">' % FAVICON)
    A('<link rel="stylesheet" href="/blog/blog.css">')
    if jsonld:
        A('<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False))
    A('</head>')
    A('<body>')
    return "\n".join(L)


def site_header(lg, data, crumb_html):
    return ('<div class="wrap">\n<header class="site">\n%s\n'
            '<a class="home" href="/?lang=%s" lang="en">CHORD<b>PLAI</b></a>\n'
            '<span class="crumb">%s</span>\n</header>' % (MARK, lg, crumb_html))


def lang_bar(cur, alts, names):
    if len(alts) < 2:
        return ""
    parts = []
    for l2, u2 in alts.items():
        nm = html.escape(names.get(l2, l2.upper()))
        if l2 == cur:
            parts.append('<span class="on">%s</span>' % nm)
        else:
            parts.append('<a href="%s" hreflang="%s" lang="%s">%s</a>' % (u2, l2, l2, nm))
    return '<nav class="langs" aria-label="Language">%s</nav>' % "".join(parts)


def render_body(blocks, lg, by_id, slug_index):
    """İçerik bloklarını HTML'e çevirir. 'link' alanı başka bir yazıya çapraz bağ kurar."""
    out = []
    for b in blocks:
        link_html = ""
        ref = b.get("link")
        if ref:
            target = by_id.get(ref) or slug_index.get(ref)
            if target:
                t_slug = target["posts_by_lang"].get(lg)
                if t_slug:
                    link_html = ' <a href="%s">→ %s</a>' % (post_url(lg, t_slug[0]), html.escape(t_slug[1]))
        if "h2" in b:
            out.append("<h2>%s</h2>" % b["h2"])
        elif "p" in b:
            out.append("<p>%s%s</p>" % (b["p"], link_html))
        elif "box" in b:
            out.append('<div class="box">%s%s</div>' % (b["box"], link_html))
        elif "ul" in b:
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in b["ul"]))
        elif "ol" in b:
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % x for x in b["ol"]))
        elif "table" in b:
            t = b["table"]
            rows = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in t["rows"])
            hd = "<tr>%s</tr>" % "".join("<th>%s</th>" % c for c in t["head"])
            out.append('<div class="tw"><table>%s%s</table></div>' % (hd, rows))
    return "\n".join(out)


def main():
    data = load()
    if BASE_LANG not in data:
        raise SystemExit("blog.%s.json bulunamadı" % BASE_LANG)
    langs = [l for l in LANGS if l in data]
    names = {l: data[l].get("name", l.upper()) for l in langs}

    # id → { lang: (slug, title) }  — hreflang ve çapraz bağlar için
    by_id, slug_index = {}, {}
    for pid in [p["id"] for p in data[BASE_LANG]["posts"]]:
        entry = {"posts_by_lang": {}}
        for l in langs:
            for p in data[l]["posts"]:
                if p["id"] == pid:
                    entry["posts_by_lang"][l] = (p["slug"], p["title"])
        by_id[pid] = entry
    # eski TR slug'larıyla da referans verilebilsin
    for p in data[BASE_LANG]["posts"]:
        slug_index[p["slug"]] = by_id[p["id"]]

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "blog.css"), "w", encoding="utf-8") as f:
        f.write(CSS)

    # sayfa başlığı/açıklaması (çeviri motoru bunları document.title ve meta'ya yazar)
    META = {
        "en": ("ChordPlai — Air Chord: Play Chords With Your Hands",
               "Make music without an instrument: show your hands to the camera and Air Chord plays the chords while you sing over them. Plus guitar & piano drills, note games and chord-controlled mini games. Free, in your browser."),
        "es": ("ChordPlai — Air Chord: toca acordes con las manos",
               "Haz música sin instrumento: muestra las manos a la cámara y Air Chord toca los acordes mientras cantas encima. Además, ejercicios de guitarra y piano, juegos de notas y minijuegos con acordes. Gratis, en tu navegador."),
        "de": ("ChordPlai — Air Chord: Akkorde mit den Händen spielen",
               "Musik ohne Instrument: Zeig deine Hände in die Kamera, Air Chord spielt die Akkorde und du singst darüber. Dazu Gitarren- und Klavierübungen, Notenspiele und Minispiele mit Akkorden. Kostenlos im Browser."),
        "fr": ("ChordPlai — Air Chord : jouer des accords avec les mains",
               "Faites de la musique sans instrument : montrez vos mains à la caméra, Air Chord joue les accords et vous chantez par-dessus. Plus des exercices guitare et piano, des jeux de notes et des mini-jeux d'accords. Gratuit, dans le navigateur."),
        "pt": ("ChordPlai — Air Chord: toque acordes com as mãos",
               "Faça música sem instrumento: mostre as mãos para a câmera e o Air Chord toca os acordes enquanto você canta. Além de exercícios de violão e piano, jogos de notas e minijogos com acordes. Grátis, no navegador."),
    }

    # uygulama arayüzü sözlükleri: content/ui.<lang>.json → /i18n/<lang>.json
    i18n_dir = os.path.join(ROOT, "i18n")
    os.makedirs(i18n_dir, exist_ok=True)
    for lg in langs:
        if lg == BASE_LANG:
            continue
        src = os.path.join(CONTENT, "ui.%s.json" % lg)
        if not os.path.exists(src):
            continue
        with open(src, encoding="utf-8") as f:
            d = json.load(f)
        # ikinci çıkarma turunda bulunan etiketler
        extra = os.path.join(CONTENT, "ui.delta.%s.json" % lg)
        if os.path.exists(extra):
            with open(extra, encoding="utf-8") as f:
                d.update(json.load(f))
        if lg in META:
            d["__title"], d["__desc"] = META[lg]
        with open(os.path.join(i18n_dir, "%s.json" % lg), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
        print("  i18n/%s.json  %d dize" % (lg, len(d)))

    urls = []   # sitemap için (loc, alts)

    for lg in langs:
        d = data[lg]
        ui = d["ui"]
        posts = d["posts"]

        # ---- dizin sayfası ----
        idx_alts = {l: index_url(l) for l in langs}
        cards = []
        for p in posts:
            cards.append(
                '<a class="post" href="%s"><h2>%s</h2><p>%s</p><span class="date">%s</span></a>'
                % (post_url(lg, p["slug"]), html.escape(p["title"]), p["excerpt"], p["date"]))
        jl = {"@context": "https://schema.org", "@type": "Blog",
              "name": ui["blogTitle"], "url": SITE + index_url(lg), "inLanguage": lg,
              "publisher": {"@type": "Organization", "name": "ChordPlai", "url": SITE + "/"}}
        idx_title = ui["blogTitle"] if "ChordPlai" in ui["blogTitle"] else "%s — ChordPlai" % ui["blogTitle"]
        page = [head(lg, d, idx_title, ui["blogDesc"], index_url(lg), idx_alts, jl),
                site_header(lg, d, html.escape(ui["blogCrumb"])),
                "<h1>%s</h1>" % html.escape(ui["blogTitle"]),
                '<p class="lead">%s</p>' % ui["blogLead"],
                "\n".join(cards),
                '<div class="cta"><a href="/?lang=%s">%s</a></div>' % (lg, html.escape(ui["cta"])),
                lang_bar(lg, idx_alts, names),
                '<footer>© 2026 ChordPlai · <a href="/?lang=%s">chordplai.com</a> — %s</footer>' % (lg, html.escape(ui["footer"])),
                "</div>\n</body>\n</html>"]
        with open(out_path(lg, "index.html"), "w", encoding="utf-8") as f:
            f.write("\n".join(page))
        urls.append((index_url(lg), idx_alts))

        # ---- yazı sayfaları ----
        for i, p in enumerate(posts):
            alts = {}
            for l2 in langs:
                t = by_id[p["id"]]["posts_by_lang"].get(l2)
                if t:
                    alts[l2] = post_url(l2, t[0])
            nxt = posts[(i + 1) % len(posts)]
            jl = {"@context": "https://schema.org", "@type": "Article",
                  "headline": p["title"], "description": p["desc"],
                  "datePublished": p["date"], "dateModified": p["date"], "inLanguage": lg,
                  "author": {"@type": "Organization", "name": "ChordPlai"},
                  "publisher": {"@type": "Organization", "name": "ChordPlai",
                                "logo": {"@type": "ImageObject", "url": SITE + "/og.png"}},
                  "image": SITE + "/og.png",
                  "mainEntityOfPage": SITE + post_url(lg, p["slug"])}
            crumb = '<a href="%s">%s</a>' % (index_url(lg), html.escape(ui["backToBlog"]))
            page = [head(lg, d, "%s · ChordPlai" % p["title"], p["desc"], post_url(lg, p["slug"]), alts, jl, "article"),
                    site_header(lg, d, crumb),
                    "<article>",
                    "<h1>%s</h1>" % html.escape(p["title"]),
                    '<p class="meta">%s · ChordPlai</p>' % p["date"],
                    render_body(p["body"], lg, by_id, slug_index),
                    '<div class="cta"><a href="/?lang=%s">%s</a></div>' % (lg, html.escape(ui["ctaPost"])),
                    "</article>",
                    lang_bar(lg, alts, names),
                    '<footer>© 2026 ChordPlai · <a href="/?lang=%s">chordplai.com</a> · '
                    '<a href="%s">%s</a> · %s: <a href="%s">%s</a></footer>'
                    % (lg, index_url(lg), html.escape(ui["blogCrumb"]), html.escape(ui["next"]),
                       post_url(lg, nxt["slug"]), html.escape(nxt["title"])),
                    "</div>\n</body>\n</html>"]
            with open(out_path(lg, p["slug"] + ".html"), "w", encoding="utf-8") as f:
                f.write("\n".join(page))
            urls.append((post_url(lg, p["slug"]), alts))

    # ---- sitemap ----
    home_alts = {l: ("/" if l == BASE_LANG else "/?lang=%s" % l) for l in langs}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    def entry(loc, alts, prio, freq):
        e = ["  <url>", "    <loc>%s%s</loc>" % (SITE, loc)]
        for l2, u2 in alts.items():
            e.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l2, SITE, u2))
        e += ["    <lastmod>2026-07-29</lastmod>",
              "    <changefreq>%s</changefreq>" % freq,
              "    <priority>%s</priority>" % prio, "  </url>"]
        return e
    sm += entry("/", home_alts, "1.0", "weekly")
    # elle yazılan statik sayfalar (üretilmez, kökte durur)
    for static in ("/gizlilik", "/kosullar"):
        sm += entry(static, {}, "0.3", "yearly")
    for loc, alts in urls:
        is_index = loc.rstrip("/").endswith("blog") or re.match(r"^/blog/[a-z]{2}$", loc)
        sm += entry(loc, alts, "0.8" if is_index else "0.7", "weekly" if is_index else "monthly")
    sm.append("</urlset>")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sm) + "\n")

    print("diller     :", ", ".join(langs))
    print("yazı sayfa :", sum(len(data[l]["posts"]) for l in langs))
    print("toplam URL :", len(urls) + 1)


if __name__ == "__main__":
    main()
