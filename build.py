from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import json, os

BASE = r'c:\Users\Teja\OneDrive\MS office\Working\Kiran Birthday_spe'

img = Image.open(os.path.join(BASE, 'Kiran Ph.jpeg')).convert('L')
w, h = img.size

# 70-char ramp: densest(dark) -> lightest(bright)
RAMP = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`. '
RL = len(RAMP)

# Tuned preprocessing for best face/hair accuracy
i2 = ImageOps.autocontrast(img, cutoff=2)
i2 = i2.point([int((v/255)**0.62*255) for v in range(256)])
i2 = ImageEnhance.Contrast(i2).enhance(2.4)
i2 = ImageEnhance.Sharpness(i2).enhance(3.0)
i2 = i2.filter(ImageFilter.UnsharpMask(radius=1, percent=180, threshold=2))

TW = 150
TH = int((h/w)*TW*0.44)
i2 = i2.resize((TW, TH), Image.Resampling.LANCZOS)

rows = []
for y in range(TH):
    row = ''
    for x in range(TW):
        b = i2.getpixel((x, y))
        row += RAMP[int(b/255*(RL-1))]
    rows.append(row)

rows_js = json.dumps(rows)
print(f'Grid {TW}x{TH}, {len(rows)} rows')

out = os.path.join(BASE, 'birthday.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write('PLACEHOLDER')
print('build.py ready, rows_js length:', len(rows_js))

# Save rows_js to a temp file so we can read it in the next step
with open(os.path.join(BASE, '_rows.json'), 'w', encoding='utf-8') as f:
    f.write(rows_js)
print('_rows.json written')
