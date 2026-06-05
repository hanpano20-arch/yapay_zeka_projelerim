import pandas as pd
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

print("📊 PDF RAPOR AJANI BAŞLATILIYOR...\n")

# 1. Excel'i oku
print("1️⃣  Excel okunuyor...")
df = pd.read_excel('uretim_maliyeti.xlsx')

# 2. Veriler analiz ediliyor
df['Toplam_Maliyet'] = df['Birim_Maliyeti'] * df['Miktar']
toplam = df['Toplam_Maliyet'].sum()
en_pahali = df.loc[df['Toplam_Maliyet'].idxmax(), 'Ürün']
en_ucuz = df.loc[df['Toplam_Maliyet'].idxmin(), 'Ürün']

print(f"   ✅ Toplam Maliyet: {toplam:.2f} TL")
print(f"   ✅ En Pahalı: {en_pahali}")
print(f"   ✅ En Ucuz: {en_ucuz}\n")

# 3. AI'dan rapor taslağı iste
print("2️⃣  AI rapor hazırlıyor...")
prompt = f"""
Türkçe olarak, profesyonel bir fabrika maliyet raporu yaz.
Veriler:
- Toplam Maliyet: {toplam:.2f} TL
- En Pahalı Ürün: {en_pahali}
- En Ucuz Ürün: {en_ucuz}

Kısa ve net ol. 3 paragraf.
"""

response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'mistral',
        'prompt': prompt,
        'stream': False
    }
)

ai_rapor = response.json()['response']
print("   ✅ AI rapor hazır\n")

# 4. PDF'e kaydet
print("3️⃣  PDF oluşturuluyor...")
pdf_path = "MALIYET_RAPORU.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
elements = []

# Başlık
title_style = ParagraphStyle(
    'CustomTitle',
    parent=getSampleStyleSheet()['Heading1'],
    fontSize=20,
    textColor=colors.HexColor('#1a1a1a'),
    spaceAfter=30
)
elements.append(Paragraph("📊 ÜRÜN MALİYET RAPORU", title_style))
elements.append(Spacer(1, 0.2*inch))

# AI Raporu
elements.append(Paragraph(ai_rapor, getSampleStyleSheet()['BodyText']))
elements.append(Spacer(1, 0.3*inch))

# Tablo
table_data = [['Ürün', 'Birim Maliyeti', 'Miktar', 'Toplam Maliyet']]
for idx, row in df.iterrows():
    table_data.append([
        row['Ürün'],
        f"${row['Birim_Maliyeti']:.2f}",
        f"{row['Miktar']}",
        f"${row['Toplam_Maliyet']:.2f}"
    ])

t = Table(table_data)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(t)

doc.build(elements)
print(f"   ✅ Rapor oluşturuldu: {pdf_path}\n")

print("🎉 AJANI İŞİ BİTTİ! PDF hazır.")