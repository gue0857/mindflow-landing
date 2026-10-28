"""產生首頁 OG 圖 src/static/assets/og.png（1200x630）。字型用 Windows 微軟正黑體。"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1200, 630
img = Image.new("RGB", (W, H), "#0D1B2A")
glow = Image.new("RGB", (W, H), "#0D1B2A")
g = ImageDraw.Draw(glow)
g.ellipse((700, -250, 1500, 450), fill="#1B3F8F")
g.ellipse((-300, 380, 500, 1000), fill="#0F4E5C")
img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(120)), 0.9)
d = ImageDraw.Draw(img)
B = "C:/Windows/Fonts/msjhbd.ttc"; R = "C:/Windows/Fonts/msjh.ttc"
f = lambda p, s: ImageFont.truetype(p, s)
# logo mark
def wave(y, dy, color):
    pts = []
    for i in range(0, 101):
        x = 80 + i * 0.7
        t = min(max((x - 112) / 22, 0), 1)
        s = t * t * (3 - 2 * t)
        pts.append((x, y - dy * s))
    d.line(pts, fill=color, width=8, joint="curve")
wave(84, 12, "#FFFFFF"); wave(108, 5, "#2563FF"); wave(134, 10, "#FFFFFF")
d.text((172, 78), "MIND FLOW", font=f(B, 34), fill="#FFFFFF")
d.text((174, 120), "思  維  流", font=f(R, 20), fill="#9DB0C8")
d.text((80, 205), "企業流程 AI 代理人", font=f(B, 30), fill="#7FA6FF")
d.text((80, 255), "一句話交辦，", font=f(B, 76), fill="#FFFFFF")
d.text((80, 350), "AI 自動執行、主動匯報。", font=f(B, 76), fill="#FFFFFF")
chips = ["下指令", "排程自動執行", "例外請人核准", "定期主動匯報"]
x = 80
for c in chips:
    w = d.textlength(c, font=f(R, 24)) + 40
    d.rounded_rectangle((x, 500, x + w, 548), 24, outline="#3A5578", width=2, fill="#13263B")
    d.text((x + 20, 508), c, font=f(R, 24), fill="#D5DFEC")
    x += w + 14
d.text((80, 575), "mindflow.tw", font=f(R, 20), fill="#6E84A1")
img.save("src/static/assets/og.png", optimize=True)
print("ok")
