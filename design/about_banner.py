"""About page banner: the founder photo, widened with its own sky colors so it fills any screen.

Usage: python3 design/about_banner.py [photo]   (default: Photo/iCloud Photos/IMG_5999.JPG; Photo/ is not in git)
Writes static/images/hero-about-sergei.webp (the page) and .jpg (link previews). Needs Pillow.
"""
import sys
from PIL import Image, ImageEnhance, ImageFilter

TOP_CROP = 170   # px of empty sky cut from the top, so the face fills more of the banner with the head still whole
FACE_X = 0.78    # the face's center, across the photo
FACE_AT = 0.55   # where the face lands across the banner; the page shows the banner's center
H, W = 1000, 6000  # 6:1, so the 460px-tall banner still covers a 2560px screen

src = Image.open(sys.argv[1] if len(sys.argv) > 1 else "Photo/iCloud Photos/IMG_5999.JPG").convert("RGB")
src = ImageEnhance.Brightness(src.crop((0, TOP_CROP, src.width, src.height))).enhance(1.12)
ph = src.resize((round(src.width * H / src.height), H), Image.LANCZOS)
pw = ph.width

# Fill each row with the photo's left-edge color, blurred down the rows, on both sides of the photo
edge = ph.crop((0, 0, 6, H)).resize((1, H), Image.BOX).resize((200, H)).filter(ImageFilter.GaussianBlur(60)).crop((100, 0, 101, H))
canvas = ImageEnhance.Brightness(edge.resize((W, H))).enhance(.85)

# Long fades on both photo edges, so it melts into the fill with no visible border
ramp = Image.linear_gradient("L").rotate(90)  # 0 at the left, 255 at the right
mask = Image.new("L", (pw, H), 255)
mask.paste(ramp.resize((320, H)), (0, 0))
mask.paste(ramp.resize((200, H)).transpose(Image.FLIP_LEFT_RIGHT), (pw - 200, 0))
canvas.paste(ph, (round(W * FACE_AT - FACE_X * pw), 0), mask.filter(ImageFilter.GaussianBlur(20)))

canvas.save("static/images/hero-about-sergei.jpg", quality=84, optimize=True, progressive=True)
canvas.save("static/images/hero-about-sergei.webp", quality=82, method=6)
print("static/images/hero-about-sergei.webp, .jpg")
