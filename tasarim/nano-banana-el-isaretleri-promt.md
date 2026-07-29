# Nano Banana 2 — Air Chord el işaretleri görseli (16:9)

Air Chord boş ekranını (idle) emoji yerine gerçek bir görselle değiştirmek için.
**En:boy 16:9** · dosya adı önerisi: `air-signs.webp` → `/tasarim/` klasörüne koy,
`.air-idle` içine `<img>` olarak ekleyeceğiz.

---

## ANA PROMPT (kopyala–yapıştır)

```
A premium 16:9 instructional poster for a music app called ChordPlai, showing seven
distinct hand gestures inside seven separate framed panels.

LAYOUT: A precise grid on a single 16:9 canvas — top row has 4 panels, bottom row has 3
panels centred beneath them. Each panel is a rounded-rectangle card (18px radius) with a
1px warm amber border and a soft inner vignette, separated by generous dark gutters.

IN EACH PANEL: one adult hand, palm facing the camera, photographed from the front,
cropped at the wrist, floating centred in the frame. Same hand, same person, same
lighting in all seven panels for perfect consistency. Anatomically correct, exactly five
fingers, natural skin, clean short nails, no jewellery, no watch, no sleeves.

THE SEVEN GESTURES, in reading order:
1. Index finger extended straight up; thumb, middle, ring and little finger folded down
   into the palm.
2. Index and middle fingers extended straight up in a V, clearly separated; thumb, ring
   and little finger folded down.
3. Index, middle and ring fingers extended straight up, evenly spread; thumb and little
   finger folded down.
4. Index, middle, ring and little finger all extended straight up and slightly spread;
   thumb folded across the palm.
5. All five fingers fully extended and spread wide — an open palm.
6. Index finger and little finger extended straight up; middle and ring fingers folded
   down; thumb folded across them (a rock-horns sign).
7. Thumb, index finger and little finger all extended; middle and ring fingers folded
   down (an "I love you" sign).

NUMBER BADGE: in the lower-left corner of each panel, a small circular badge containing
the roman numeral of that panel — I, II, III, IV, V, VI, VII — in warm amber on a dark
disc. No other text anywhere in the image.

COLOUR & LIGHT: very dark warm-charcoal background (#14110b) with a faint radial glow at
the top centre. Hands are lit by a soft key light from the upper left plus a warm amber
rim light (#f5c264) tracing the finger edges, giving a subtle studio-equipment glow. Deep
shadows, high contrast, cinematic and premium — like a boutique guitar-pedal advertisement.
Overall palette: near-black background, warm cream skin highlights, amber accents only.

STYLE: clean product photography, shallow depth of field on the background only, hands
tack sharp. Minimal, elegant, professional. No clutter, no props, no instruments, no
watermark, no logo, no captions.

Aspect ratio 16:9, high resolution.
```

---

## VARYANT A — tek sıra şerit (dar alanlar için)

Aynı prompt'ta `LAYOUT` paragrafını şununla değiştir:

```
LAYOUT: A single horizontal row of seven equal panels spanning the full width of a 16:9
canvas, like frames on a film strip, separated by thin dark gutters. Each panel is a tall
rounded rectangle with a 1px warm amber border.
```

## VARYANT B — çizim/illüstrasyon (eller zor çıkarsa)

Fotoğrafik eller yapay çıkarsa bu satırı `STYLE` yerine koy:

```
STYLE: elegant minimal line illustration — hands drawn with clean 3px warm amber outlines
on a near-black background, no fill, subtle cream highlights on the fingertips. Technical
yet beautiful, like a premium instruction manual. Consistent line weight across all seven
panels.
```

---

## KULLANIM NOTLARI

- **Eller yapay çıkarsa:** Modeller çok parmaklı el üretmeye eğilimlidir. Panelleri
  **teker teker** üretip (her seferinde tek el, kare kadraj, aynı ışık tarifiyle) sonra
  yan yana dizmek en garantili yol. Yukarıdaki gesture tarifleri tek tek de kullanılabilir.
- **Tutarlılık için:** Nano Banana 2'de ilk iyi sonucu referans görsel olarak verip
  "same hand, same lighting, now showing gesture #N" diye devam et.
- **Kontrol listesi:** her panelde tam 5 parmak var mı · katlanan parmaklar gerçekten
  avuç içine giriyor mu · 6. ve 7. işaretlerde başparmak konumu doğru mu.
- **Siteye eklerken:** WebP'ye çevir (~150 KB altı), `loading="lazy"` verme (ilk ekran),
  `alt="Air Chord el işaretleri: 1'den 7'ye gam dereceleri"` yaz.
