"""Logo, favicons and social share image for Tourney Finder (writes brand/)."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(ROOT, "brand")
NAVY, GOLD, GOLD2, CREAM = (7, 11, 31), (201, 165, 76), (230, 201, 122), (243, 239, 228)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def shield(d, cx, top, w, stroke):
    h = w * 1.12
    pts = [(cx, top), (cx + w / 2, top + h * .15), (cx + w / 2, top + h * .5), (cx + w * .38, top + h * .78), (cx, top + h), (cx - w * .38, top + h * .78), (cx - w / 2, top + h * .5), (cx - w / 2, top + h * .15)]
    d.polygon(pts, fill=(24, 30, 66), outline=GOLD, width=stroke)
    return h

def icon(size):
    im = Image.new("RGB", (size * 4, size * 4), NAVY); d = ImageDraw.Draw(im); S = size * 4
    h = shield(d, S / 2, S * .1, S * .7, max(4, S // 28))
    f = ImageFont.truetype(BOLD, int(S * .3))
    d.text((S / 2, S * .1 + h * .48), "TF", font=f, fill=GOLD2, anchor="mm")
    return im.resize((size, size), Image.LANCZOS)

def og():
    im = Image.new("RGB", (1200, 630), NAVY); d = ImageDraw.Draw(im)
    for x in range(-630, 1200, 28):
        d.line([(x, 630), (x + 300, 0)], fill=(16, 22, 48), width=1)
    im.paste(icon(220), (90, 205))
    d.text((360, 230), "TOURNEY FINDER", font=ImageFont.truetype(BOLD, 64), fill=CREAM)
    d.text((362, 320), "Every tournament. One calendar.", font=ImageFont.truetype(BOLD, 40), fill=GOLD2)
    d.text((362, 390), "Football · futsal · cricket · basketball · AFL", font=ImageFont.truetype(BOLD, 28), fill=(170, 178, 205))
    d.text((362, 432), "Junior & community tournaments · NSW + QLD", font=ImageFont.truetype(BOLD, 28), fill=(170, 178, 205))
    return im

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    icon(512).save(os.path.join(OUT, "logo-512.png"))
    icon(192).save(os.path.join(OUT, "icon-192.png"))
    icon(180).save(os.path.join(OUT, "apple-touch-icon.png"))
    icon(48).save(os.path.join(OUT, "favicon-48.png"))
    icon(64).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    og().save(os.path.join(OUT, "og-image.png"))
    print("ok")
