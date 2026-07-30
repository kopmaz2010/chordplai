# Nano Banana 2 — Beden Pozları Görseli (7 poz + sus)

## Ana prompt (16:9 tek görsel, çerçeveli 8 kare)

```
A single 16:9 instructional poster on a very dark charcoal-black background (#0a0a07),
divided into 8 equal rounded rectangular panels arranged in a 4x2 grid, each panel
separated by thin warm-amber hairline borders (#f5c264, 1px, subtle glow).

Inside every panel: the SAME young adult person, full upper body from mid-thigh up,
centered, facing the camera straight on, photographed from the front at chest height.
Neutral confident expression, relaxed shoulders. Plain fitted dark charcoal t-shirt,
dark trousers. Warm amber key light from the upper left, soft teal rim light from the
back right, dark vignette. Cinematic studio photography, shallow depth of field,
crisp focus on the body, 85mm lens look.

The eight panels show these EXACT arm positions, in this order, left to right, top row first:

1. Both arms raised straight up above the head, forming a wide V, palms open facing forward, fingers together.
2. RIGHT arm raised straight up above the head; LEFT arm extended straight out to the side at exact shoulder height, palm down.
3. LEFT arm raised straight up above the head; RIGHT arm extended straight out to the side at exact shoulder height, palm down.
4. Both arms extended straight out to the sides at exact shoulder height, forming a perfect horizontal T, palms down.
5. RIGHT arm raised straight up above the head; LEFT arm hanging straight down along the body, close to the hip.
6. LEFT arm raised straight up above the head; RIGHT arm hanging straight down along the body, close to the hip.
7. Both arms raised above the head with the WRISTS CROSSED over each other, forming a clear X shape above the head.
8. Both arms hanging relaxed straight down along the body, hands beside the thighs, resting stance.

Each panel has a large amber roman numeral in its top-left corner: I, II, III, IV, V, VI, VII
for panels 1 to 7, and a small amber mute icon for panel 8.

Silhouettes must be unmistakably readable: high contrast between the body and the
background, arms fully extended, no bent elbows unless specified, no motion blur, no
overlap between the arms and the head except in panel 7. Same person, same clothing,
same framing, same lighting in all eight panels. Photorealistic, high detail, 16:9.
```

## Negatif prompt

```
text, letters, words, watermark, logo, extra limbs, deformed hands, blurry, motion blur,
low contrast, cluttered background, props, instruments, multiple people, different people
per panel, inconsistent clothing, side view, three-quarter view, cropped arms, arms out of
frame, bent elbows, drooping arms, mirrored duplicates, cartoon, illustration, 3d render
```

## Tek tek export için (şeffaf arka plan, 200×200)

El işaretlerinde yaptığımız gibi tek tek de gerekiyorsa, her poz için ayrı istek:

```
Full upper body of a young adult on a fully TRANSPARENT background (alpha channel, PNG).
[POZ TARİFİ buraya — yukarıdaki listeden bir madde]
Front view, centered, warm amber key light from upper left, soft teal rim light from back
right. Plain dark charcoal t-shirt. Photorealistic, crisp edges, clean alpha cutout, no
shadow on the ground, square 1:1 composition with even margins on all sides.
```

Dosya adları (siteye entegre ederken bu adları bekliyorum):

| Dosya | Poz | Derece |
|---|---|---|
| `tasarim/pose/1.webp` | İki kol yukarı (V) | I |
| `tasarim/pose/2.webp` | Sağ yukarı · sol yanda | II |
| `tasarim/pose/3.webp` | Sol yukarı · sağ yanda | III |
| `tasarim/pose/4.webp` | İki kol yana (T) | IV |
| `tasarim/pose/5.webp` | Sağ yukarı · sol aşağı | V |
| `tasarim/pose/6.webp` | Sol yukarı · sağ aşağı | VI |
| `tasarim/pose/7.webp` | Bilekler üstte çapraz (X) | VII |
| `tasarim/pose/0.webp` | İki kol aşağı | Sus |

## Neden bu tarifler böyle yazıldı

Sınıflandırıcı kararını **bilek yüksekliğine** göre veriyor, kola değil:

- **"yukarı"** = bilek burun hizasının üstünde
- **"yanda"** = bilek omuz yüksekliğinde ± gövde boyunun %35'i, ve omuzdan yatayda omuz genişliğinin %55'inden uzakta
- **"aşağı"** = bilek omuzun gövde boyu × %55 altında
- **"çapraz"** = iki bilek de yukarıda ve x ekseninde yer değiştirmiş (ya da omuz genişliğinin %40'ından yakın)

Bu yüzden promptta "straight up above the head", "exact shoulder height", "hanging
straight down" gibi net ifadeler var — yarım kalmış kollar hem görselde hem gerçek
kullanımda belirsiz kalıyor. Görselde de kullanıcıya öğrettiğimiz duruş, kameranın
tanıdığı duruşla birebir aynı olmalı.
