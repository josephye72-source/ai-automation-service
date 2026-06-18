from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "workflow-preview.png"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def rounded(draw: ImageDraw.ImageDraw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start, end, color):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=3)
    draw.polygon([(x2, y2), (x2 - 8, y2 - 5), (x2 - 8, y2 + 5)], fill=color)


def multiline(draw, xy, text, fill, fnt, line_gap=5):
    x, y = xy
    for line in text.split("\n"):
        draw.text((x, y), line, fill=fill, font=fnt)
        y += fnt.size + line_gap


def build():
    img = Image.new("RGB", (1400, 820), "#f8faf9")
    d = ImageDraw.Draw(img)

    title_font = font(44, True)
    label_font = font(22, True)
    body_font = font(19)
    small_font = font(16)

    d.text((70, 55), "P0 AI Workflow Loop", fill="#10201f", font=title_font)
    d.text((72, 113), "From internal question to reviewable answer and traceable log", fill="#4b5d5b", font=body_font)

    nodes = [
        ("Message\nInput", "Lark Bot / webhook", 70, 220, "#e8f7f3", "#0f766e"),
        ("RAG\nRetrieval", "RAGFlow sources", 330, 220, "#eef6ff", "#2563eb"),
        ("AI Draft", "Dify / LLM route", 590, 220, "#fff7ed", "#d97706"),
        ("Call Log", "Lark Base record", 850, 220, "#f0fdf4", "#16a34a"),
        ("Human\nReview", "approve / revise", 1110, 220, "#f5f3ff", "#7c3aed"),
    ]

    for title, desc, x, y, bg, accent in nodes:
        rounded(d, (x, y, x + 210, y + 170), 14, bg, "#d6dedb", 2)
        d.rectangle((x, y, x + 210, y + 8), fill=accent)
        multiline(d, (x + 22, y + 32), title, "#10201f", label_font, 4)
        d.text((x + 22, y + 122), desc, fill="#50615f", font=small_font)

    for x in [280, 540, 800, 1060]:
        arrow(d, (x, 305), (x + 38, 305), "#6b7d7a")

    rounded(d, (90, 470, 665, 715), 16, "#ffffff", "#d8e1de", 2)
    d.text((125, 505), "Sample output", fill="#0f766e", font=label_font)
    sample = (
        "Question: low-budget GCC creator campaign?\n"
        "Sources: case-2026-001, rule-pricing-003\n"
        "Draft: offer paid diagnostic first; clarify market,\n"
        "creator tier, deliverables, and payment risk.\n"
        "Status: pending human review"
    )
    multiline(d, (125, 550), sample, "#1d2d2b", body_font, 7)

    rounded(d, (725, 470, 1310, 715), 16, "#10201f", "#10201f", 2)
    d.text((760, 505), "Engineering boundaries", fill="#7dd3c7", font=label_font)
    boundaries = (
        "• secrets stay in environment variables\n"
        "• every call produces a reviewable log row\n"
        "• failures return explicit retry states\n"
        "• no CAPTCHA bypass or gray-market automation"
    )
    multiline(d, (760, 550), boundaries, "#e7f3f1", body_font, 9)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    build()

