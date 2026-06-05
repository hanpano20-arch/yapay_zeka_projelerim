import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

print("📊 PDF RAPOR AJANI BAŞLATILIYOR...\n")

# Türkçe font
font_path = r"C:\Windows\Fonts\arial.ttf"
pdfmetrics.registerFont(TTFont("arial", font_path))

# Excel oku
print("1️⃣ Excel okunuyor...")
df = pd.read_excel("uretim_maliyeti.xlsx")

# Analiz
df["Toplam_Maliyet"] = df["Birim_Maliyeti"] * df["Miktar"]

toplam = df["Toplam_Maliyet"].sum()

en_pahali_satir = df.loc[df["Toplam_Maliyet"].idxmax()]
en_ucuz_satir = df.loc[df["Toplam_Maliyet"].idxmin()]

en_pahali = en_pahali_satir["Ürün"]
en_ucuz = en_ucuz_satir["Ürün"]

print(f"✅ Toplam maliyet: {toplam:.2f} TL")

# AI yerine otomatik rapor
rapor = f"""
Bu rapor otomatik olarak oluşturulmuştur.

Toplam maliyet: {toplam:.2f} TL

En yüksek maliyetli ürün:
{en_pahali}

En düşük maliyetli ürün:
{en_ucuz}

Maliyet dağılımı incelendiğinde üretim giderlerinin büyük kısmının yüksek maliyetli ürünlerde toplandığı görülmektedir.
"""

# PDF oluştur
print("2️⃣ PDF oluşturuluyor...")

pdf_path = "MALIYET_RAPORU.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter
)

elements = []

title_style = ParagraphStyle(
    "Title",
    fontName="arial",
    fontSize=18,
    alignment=1,
    spaceAfter=20
)

body_style = ParagraphStyle(
    "Body",
    fontName="arial",
    fontSize=11,
    leading=18
)

elements.append(
    Paragraph("ÜRÜN MALİYET RAPORU", title_style)
)

elements.append(Spacer(1, 10))

elements.append(
    Paragraph(rapor.replace("\n", "<br/>"), body_style)
)

elements.append(Spacer(1, 20))

# Tablo
table_data = [
    ["Ürün", "Birim Maliyet", "Miktar", "Toplam Maliyet"]
]

for _, row in df.iterrows():
    table_data.append([
        str(row["Ürün"]),
        f"{row['Birim_Maliyeti']:.2f} TL",
        str(int(row["Miktar"])),
        f"{row['Toplam_Maliyet']:.2f} TL"
    ])

table = Table(
    table_data,
    colWidths=[2.2*inch, 1.3*inch, 1*inch, 1.5*inch]
)

table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ("FONTNAME", (0, 0), (-1, -1), "arial"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
]))

elements.append(table)

doc.build(elements)

print(f"✅ PDF oluşturuldu: {pdf_path}")
print("🎉 İŞLEM TAMAMLANDI!")