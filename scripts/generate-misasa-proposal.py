from __future__ import annotations

from pathlib import Path
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "misasa-onsen-hospital-web-proposal.pdf"
QR_OUTPUT = ROOT / "misasa-demo" / "assets" / "misasa-demo-qr.png"
SOCIAL_IMAGE = ROOT / "misasa-demo" / "assets" / "misasa-demo-social.png"
DEMO_URL = "https://ldmvworks.github.io/misasa-demo/"
PAGE_W, PAGE_H = landscape(A4)


COLORS = {
    "ink": colors.HexColor("#17312c"),
    "muted": colors.HexColor("#64766f"),
    "paper": colors.HexColor("#f7faf7"),
    "white": colors.white,
    "line": colors.HexColor("#d9e5df"),
    "green": colors.HexColor("#2d7668"),
    "green_dark": colors.HexColor("#174f47"),
    "mint": colors.HexColor("#dff1e9"),
    "aqua": colors.HexColor("#bce2de"),
    "amber": colors.HexColor("#e7ad52"),
}


DEMOS = [
    {
        "number": "01",
        "title": "病院総合トップ",
        "subtitle": "3つの情報設計を、その場で切り替えて比較。",
        "summary": "情報整理型のブルー、写真・体験型のオレンジ、スタイリッシュなグリーン。導線設計まで異なる3案を体験できます。",
        "features": ["ブルー・オレンジ・グリーンの3案切替", "各案に最適化した目的別導線", "スマートフォン対応とURL共有"],
        "value": "見た目だけでなく、情報の届け方と回遊性を比較・検討できる",
        "color": "#2d7668",
        "tint": "#e4f1eb",
    },
    {
        "number": "02",
        "title": "外来・受診案内",
        "subtitle": "来院前の「わからない」を減らす。",
        "summary": "初診・再診・急な症状・健診など、状況を選ぶだけで必要な手続きや持ち物へ進める受診ガイド。",
        "features": ["状況別のナビゲーション", "診療科タブと外来予定表", "持ち物・受付場所の事前確認"],
        "value": "患者さまの不安と、電話での定型問い合わせを軽減",
        "color": "#b27a21",
        "tint": "#fff8e9",
    },
    {
        "number": "03",
        "title": "温泉リハビリ",
        "subtitle": "この場所ならではの医療を、物語で伝える。",
        "summary": "温泉資源、多職種チーム、暮らしへの復帰支援を、回復までのストーリーとして紹介する特色ページ。",
        "features": ["回復プロセスの可視化", "PT・OT・STの役割紹介", "温泉活用の誠実な情報発信"],
        "value": "選ばれる理由をわかりやすく伝え、紹介・相談につなげる",
        "color": "#207a82",
        "tint": "#deeff1",
    },
    {
        "number": "04",
        "title": "入院・退院支援",
        "subtitle": "入院前から在宅復帰まで、見通しのある安心を。",
        "summary": "入院準備、病棟での支援、退院調整、在宅支援を一本の流れとして示す患者さま・ご家族向けガイド。",
        "features": ["患者ジャーニーの見える化", "病棟の役割を平易に説明", "FAQと相談窓口の整理"],
        "value": "支援の全体像を共有し、ご本人・ご家族の安心を高める",
        "color": "#79644e",
        "tint": "#f2ece5",
    },
    {
        "number": "05",
        "title": "採用・働く人",
        "subtitle": "仕事内容だけでなく、働く意味を届ける。",
        "summary": "チーム医療、成長、地域で働く価値を、職員の声や職種別の情報とともに伝える採用コミュニケーション。",
        "features": ["職員インタビュー", "制度を利用場面から紹介", "職種別募集と見学申込み"],
        "value": "応募前の理解を深め、病院との相性が良い人材に届ける",
        "color": "#bb604d",
        "tint": "#f6e8e3",
    },
    {
        "number": "06",
        "title": "地域医療連携",
        "subtitle": "地域の医療を、情報でつなぐ。",
        "summary": "紹介・入院相談・退院支援・様式ダウンロードを一か所へ集約する、医療・介護関係者向けポータル。",
        "features": ["相談目的別の最短導線", "受け入れ情報の表示", "最新様式の一元管理"],
        "value": "連携先と病院双方の確認時間・更新負担を減らす",
        "color": "#575487",
        "tint": "#e9e8f3",
    },
]


def register_fonts() -> None:
    regular = Path(r"C:\Windows\Fonts\YuGothM.ttc")
    bold = Path(r"C:\Windows\Fonts\YuGothB.ttc")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ProposalJP", str(regular), subfontIndex=0))
        pdfmetrics.registerFont(TTFont("ProposalJPBold", str(bold), subfontIndex=0))
        return
    pdfmetrics.registerFont(TTFont("ProposalJP", r"C:\Windows\Fonts\meiryo.ttc", subfontIndex=0))
    pdfmetrics.registerFont(TTFont("ProposalJPBold", r"C:\Windows\Fonts\meiryob.ttc", subfontIndex=0))


def split_lines(text: str, font: str, size: float, width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for paragraph in text.split("\n"):
        for char in paragraph:
            candidate = current + char
            if current and pdfmetrics.stringWidth(candidate, font, size) > width:
                lines.append(current)
                current = char
            else:
                current = candidate
        lines.append(current)
        current = ""
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def draw_text(
    c: canvas.Canvas,
    text: str,
    x: float,
    y: float,
    width: float,
    font: str = "ProposalJP",
    size: float = 12,
    color=COLORS["ink"],
    leading: float | None = None,
    max_lines: int | None = None,
) -> float:
    leading = leading or size * 1.55
    lines = split_lines(text, font, size, width)
    if max_lines:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    cursor = y
    for line in lines:
        c.drawString(x, cursor, line)
        cursor -= leading
    return cursor


def draw_footer(c: canvas.Canvas, page: int, dark: bool = False) -> None:
    color = colors.Color(1, 1, 1, alpha=0.58) if dark else COLORS["muted"]
    c.setFillColor(color)
    c.setFont("ProposalJP", 7.5)
    c.drawString(42, 22, "三朝温泉病院様 Webリニューアル提案 / 非公式・提案用")
    c.drawRightString(PAGE_W - 42, 22, f"{page:02d}")


def generate_qr() -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=18,
        border=4,
    )
    qr.add_data(DEMO_URL)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#174f47", back_color="white")
    QR_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(QR_OUTPUT)


def draw_cover(c: canvas.Canvas) -> None:
    image = ImageReader(str(SOCIAL_IMAGE))
    image_w, image_h = image.getSize()
    scale = max(PAGE_W / image_w, PAGE_H / image_h)
    draw_w, draw_h = image_w * scale, image_h * scale
    c.drawImage(image, (PAGE_W - draw_w) / 2, (PAGE_H - draw_h) / 2, draw_w, draw_h, mask="auto")
    c.setFillColor(colors.Color(0.05, 0.16, 0.14, alpha=0.72))
    c.roundRect(54, 36, 240, 30, 8, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("ProposalJPBold", 9)
    c.drawString(68, 46, "SALES DEMONSTRATION / 6 EXPERIENCES")
    draw_footer(c, 1, dark=True)
    c.showPage()


def draw_strategy(c: canvas.Canvas) -> None:
    c.setFillColor(COLORS["paper"])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(COLORS["green_dark"])
    c.roundRect(PAGE_W - 254, PAGE_H - 222, 290, 260, 42, fill=1, stroke=0)
    c.setFillColor(COLORS["aqua"])
    c.circle(PAGE_W - 80, PAGE_H - 54, 72, fill=1, stroke=0)
    c.setFillColor(COLORS["green"])
    c.setFont("ProposalJPBold", 9)
    c.drawString(48, PAGE_H - 56, "PROPOSAL FRAME")
    draw_text(c, "6つの体験で、\n病院の価値を伝え分ける。", 48, PAGE_H - 98, 500, "ProposalJPBold", 28, COLORS["ink"], 40)
    draw_text(c, "ひとつのサイトに情報を詰め込むのではなく、見る人の目的ごとに最短の体験を設計します。", 48, PAGE_H - 190, 510, size=12, color=COLORS["muted"], leading=20)

    audiences = [
        ("患者さま・ご家族", "受診・入院・退院後まで、迷わず安心できる情報"),
        ("未来の職員", "仕事の意義、働く人、成長できる環境の実感"),
        ("地域の関係者", "紹介・相談・様式確認を短時間で完了できる導線"),
    ]
    start_y = PAGE_H - 296
    for i, (title, body) in enumerate(audiences):
        x = 48 + i * 250
        c.setFillColor(colors.white)
        c.roundRect(x, start_y - 162, 224, 158, 22, fill=1, stroke=0)
        c.setFillColor(COLORS["mint"])
        c.circle(x + 28, start_y - 32, 13, fill=1, stroke=0)
        c.setFillColor(COLORS["green_dark"])
        c.setFont("ProposalJPBold", 14)
        c.drawString(x + 20, start_y - 72, title)
        draw_text(c, body, x + 20, start_y - 100, 180, size=9.5, color=COLORS["muted"], leading=15)

    c.setFillColor(COLORS["ink"])
    c.setFont("ProposalJPBold", 10)
    c.drawString(48, 70, "期待する変化")
    c.setFont("ProposalJP", 9)
    c.setFillColor(COLORS["muted"])
    c.drawString(142, 70, "探しやすさ / 信頼形成 / 問い合わせ負担の軽減 / 採用力 / 地域連携の効率")
    draw_footer(c, 2)
    c.showPage()


def draw_demo_page(c: canvas.Canvas, demo: dict[str, object], page: int) -> None:
    accent = colors.HexColor(str(demo["color"]))
    tint = colors.HexColor(str(demo["tint"]))
    c.setFillColor(COLORS["paper"])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setFillColor(tint)
    c.roundRect(PAGE_W - 330, 36, 350, PAGE_H - 72, 36, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("ProposalJPBold", 10)
    c.drawString(48, PAGE_H - 54, f"DEMO {demo['number']}")
    c.setFillColor(COLORS["ink"])
    c.setFont("ProposalJPBold", 32)
    c.drawString(48, PAGE_H - 104, str(demo["title"]))
    draw_text(c, str(demo["subtitle"]), 48, PAGE_H - 142, 430, "ProposalJPBold", 16, accent, 24)
    draw_text(c, str(demo["summary"]), 48, PAGE_H - 202, 430, size=11.5, color=COLORS["muted"], leading=19)

    c.setFillColor(COLORS["ink"])
    c.setFont("ProposalJPBold", 9)
    c.drawString(48, PAGE_H - 300, "DEMONSTRATED FEATURES")
    y = PAGE_H - 334
    for feature in demo["features"]:  # type: ignore[index]
        c.setFillColor(accent)
        c.circle(56, y + 3, 4, fill=1, stroke=0)
        c.setFillColor(COLORS["ink"])
        c.setFont("ProposalJPBold", 11)
        c.drawString(70, y, str(feature))
        y -= 33

    c.setFillColor(colors.white)
    c.roundRect(48, 76, 410, 86, 18, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("ProposalJPBold", 8)
    c.drawString(66, 132, "BUSINESS VALUE")
    draw_text(c, str(demo["value"]), 66, 108, 360, "ProposalJPBold", 12, COLORS["ink"], 18)

    # Abstract browser mockup to represent the corresponding live demo.
    mock_x, mock_y, mock_w, mock_h = PAGE_W - 304, 95, 270, 395
    c.setFillColor(colors.white)
    c.roundRect(mock_x, mock_y, mock_w, mock_h, 24, fill=1, stroke=0)
    c.setFillColor(COLORS["line"])
    c.roundRect(mock_x + 16, mock_y + mock_h - 32, 106, 6, 3, fill=1, stroke=0)
    c.circle(mock_x + mock_w - 25, mock_y + mock_h - 29, 5, fill=1, stroke=0)
    c.setFillColor(accent)
    c.roundRect(mock_x + 16, mock_y + 195, mock_w - 32, 155, 22, fill=1, stroke=0)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.95))
    c.roundRect(mock_x + 34, mock_y + 305, 92, 7, 3, fill=1, stroke=0)
    c.roundRect(mock_x + 34, mock_y + 283, 155, 12, 5, fill=1, stroke=0)
    c.roundRect(mock_x + 34, mock_y + 262, 122, 12, 5, fill=1, stroke=0)
    c.setFillColor(tint)
    for row in range(2):
        for col in range(2):
            c.roundRect(mock_x + 16 + col * 121, mock_y + 102 - row * 90, 109, 76, 14, fill=1, stroke=0)
    c.setFillColor(accent)
    c.setFont("ProposalJPBold", 42)
    c.drawRightString(PAGE_W - 52, 54, str(demo["number"]))

    draw_footer(c, page)
    c.showPage()


def draw_qr_page(c: canvas.Canvas, page: int) -> None:
    c.setFillColor(COLORS["green_dark"])
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(colors.Color(1, 1, 1, alpha=0.08))
    c.circle(PAGE_W - 35, PAGE_H - 30, 175, fill=1, stroke=0)
    c.circle(PAGE_W - 35, PAGE_H - 30, 125, fill=1, stroke=0)

    c.setFillColor(COLORS["aqua"])
    c.setFont("ProposalJPBold", 9)
    c.drawString(54, PAGE_H - 62, "LIVE DEMONSTRATION")
    draw_text(c, "その場で、\n6つのデモを体験。", 54, PAGE_H - 112, 410, "ProposalJPBold", 31, colors.white, 43)
    draw_text(c, "スマートフォンのカメラでQRコードを読み取り、\nパスワードを入力してください。", 54, PAGE_H - 220, 390, size=12, color=colors.Color(1, 1, 1, alpha=0.72), leading=21)

    c.setFillColor(colors.white)
    c.roundRect(PAGE_W - 338, 72, 270, 450, 28, fill=1, stroke=0)
    c.drawImage(ImageReader(str(QR_OUTPUT)), PAGE_W - 309, 224, 212, 212, mask="auto")
    c.setFillColor(COLORS["green_dark"])
    c.setFont("ProposalJPBold", 10)
    c.drawCentredString(PAGE_W - 203, 184, "ACCESS PASSWORD")
    c.setFont("Helvetica-Bold", 23)
    c.drawCentredString(PAGE_W - 203, 150, "misasa")
    c.setFillColor(COLORS["muted"])
    c.setFont("Helvetica", 7.2)
    c.drawCentredString(PAGE_W - 203, 115, DEMO_URL)

    c.setFillColor(colors.Color(1, 1, 1, alpha=0.12))
    c.roundRect(54, 94, 382, 92, 18, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("ProposalJPBold", 9)
    c.drawString(72, 158, "DEMO NOTE")
    draw_text(c, "本資料およびデモは提案イメージです。病院公式サイトではなく、診療予定・募集状況・受け入れ情報などの表示は実データではありません。", 72, 136, 340, size=8.5, color=colors.Color(1, 1, 1, alpha=0.72), leading=14)

    c.setFillColor(colors.Color(1, 1, 1, alpha=0.48))
    c.setFont("ProposalJP", 7)
    c.drawString(54, 56, "Content basis: misasa-hp.jp/recruit/ / chuubu.tottori.med.or.jp  (checked 2026-07-10)")
    draw_footer(c, page, dark=True)
    c.showPage()


def main() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    generate_qr()
    c = canvas.Canvas(str(OUTPUT), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("三朝温泉病院 Webリニューアル提案デモ")
    c.setAuthor("LDMV Works")
    c.setSubject("非公式・営業提案用デモ")
    draw_cover(c)
    draw_strategy(c)
    for page, demo in enumerate(DEMOS, start=3):
        draw_demo_page(c, demo, page)
    draw_qr_page(c, 9)
    c.save()
    print(OUTPUT)
    print(QR_OUTPUT)


if __name__ == "__main__":
    main()
