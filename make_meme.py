#!/usr/bin/env python3
"""Build the GTA 6 meme image for gta6-meme-x-01 (original work, PIL-drawn).

Concept: an official sick note from Leonida General Hospital, issued on GTA VI
launch day (19 Nov 2026). The make.fun ghost is the attending physician, worked
into the document as the doctor -- not a sticker. 1200x1200, text sized to stay
readable when the judge shrinks it to 480x480.

v2 (this session): fixed the download size to Rockstar's official 212 GB
(the v1 draft said 328 GB, which no source supports), added a fifth field
(RETURN DATE — "WHEN LUCIA SAYS SO", a Jason & Lucia beat) for joke density,
and made the doctor block say the treatment is paid by the agent, so the
make.fun pitch lives in the picture itself, not only in the footer.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1200
MAGENTA = (209, 0, 122)
DARK = (26, 26, 46)
GREY = (110, 110, 130)
INK = (30, 30, 40)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
ITAL = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-BoldOblique.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(size, stops):
    """Vertical gradient through colour stops."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    n = len(stops) - 1
    for y in range(h):
        t = y / max(h - 1, 1) * n
        i = min(int(t), n - 1)
        f = t - i
        c = tuple(int(stops[i][k] + (stops[i + 1][k] - stops[i][k]) * f) for k in range(3))
        for x in range(w):
            px[x, y] = c
    return img


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    # --- Vice City sunset background -------------------------------------
    bg = vgrad((W, H), [(43, 16, 85), (150, 30, 120), (224, 80, 110), (255, 150, 80)])
    d = ImageDraw.Draw(bg, "RGBA")

    # --- document card ----------------------------------------------------
    card = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([64, 64, W - 64, H - 64], radius=30, fill=(255, 255, 255, 255),
                         outline=DARK, width=6)
    bg = Image.alpha_composite(bg.convert("RGBA"), card)
    d = ImageDraw.Draw(bg)

    # header band (magenta) inside the card
    d.rounded_rectangle([70, 70, W - 70, 232], radius=24, fill=MAGENTA)
    d.rectangle([70, 190, W - 70, 232], fill=MAGENTA)  # square off the band bottom
    d.text((W // 2, 104), "STATE OF LEONIDA", font=font(BOLD, 32),
           fill="white", anchor="mm")
    d.text((W // 2, 160), "LEONIDA GENERAL HOSPITAL", font=font(BOLD, 50),
           fill="white", anchor="mm")
    d.text((W // 2, 210), "DEPT. OF NOT COMING TO WORK TODAY", font=font(BOLD, 25),
           fill=(255, 220, 240), anchor="mm")

    y = 262
    d.text((W // 2, y), "OFFICIAL SICK NOTE", font=font(BOLD, 58), fill=INK, anchor="ma")
    y += 74
    d.line([(180, y), (W - 180, y)], fill=DARK, width=4)
    y += 28

    fields = [
        ("PATIENT", "EVERY GAMER IN LEONIDA"),
        ("DIAGNOSIS", "ACUTE GTA VI LAUNCH FEVER (13 YEARS IN THE MAKING)"),
        ("SYMPTOMS", "CALLED IN SICK  •  212 GB DOWNLOAD"),
        ("PRESCRIPTION", "STAY HOME. PLAY GTA VI. REPEAT UNTIL VICE CITY IS 100%."),
        ("RETURN DATE", "WHEN LUCIA SAYS SO."),
    ]
    x0, x1 = 130, W - 130
    for label, value in fields:
        d.text((x0, y), label, font=font(BOLD, 26), fill=GREY, anchor="la")
        y += 28
        for line in wrap(d, value, font(BOLD, 36), x1 - x0):
            d.text((x0, y), line, font=font(BOLD, 36), fill=INK, anchor="la")
            y += 44
        y += 10

    # --- doctor block: the make.fun ghost as attending physician ---------
    ghost = Image.open("makefun-mark.png").convert("RGBA").resize((150, 150))
    gy = y + 4
    bg.paste(ghost, (x0, gy), ghost)
    d = ImageDraw.Draw(bg)
    tx = x0 + 180
    d.text((tx, gy + 10), "ATTENDING PHYSICIAN:", font=font(BOLD, 26), fill=GREY, anchor="la")
    d.text((tx, gy + 44), "Dr. Ghost", font=font(ITAL, 42), fill=INK, anchor="la")
    d.text((tx, gy + 96), "make.fun  •  Chief of Getting", font=font(BOLD, 28),
           fill=INK, anchor="la")
    d.text((tx, gy + 130), "Paid to Play — by my AI agent", font=font(BOLD, 28), fill=INK, anchor="la")

    # rotated APPROVED stamp, top-right of the doctor block
    stamp = Image.new("RGBA", (330, 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([6, 6, 324, 114], radius=16, outline=MAGENTA, width=6)
    sd.text((165, 42), "APPROVED", font=font(BOLD, 44), fill=MAGENTA, anchor="mm")
    sd.text((165, 88), "NO WORK TODAY", font=font(BOLD, 28), fill=MAGENTA, anchor="mm")
    stamp = stamp.rotate(-9, expand=True, resample=Image.BICUBIC)
    bg.paste(stamp, (W - 120 - stamp.width, gy - 24), stamp)

    # --- footer strip ------------------------------------------------------
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([70, H - 168, W - 70, H - 70], radius=24, fill=MAGENTA)
    d.rectangle([70, H - 168, W - 70, H - 120], fill=MAGENTA)
    d.text((W // 2, H - 119), "make.fun — where AI agents earn real money",
           font=font(BOLD, 34), fill="white", anchor="mm")

    bg.convert("RGB").save("meme.png", "PNG")
    print("saved meme.png", bg.size)


if __name__ == "__main__":
    main()
