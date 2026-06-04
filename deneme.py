import pandas as pd
import ollama

# --- 1. ADIM: FABRİKA VERİLERİNİ HESAPLAMA VE EXCEL OLUŞTURMA ---
imalat_verisi = {
    'Urun_Adi': ['Çelik Kapı (Model-A)', 'Yangın Kapısı', 'Lazer Kesim Sac', 'Ferforje Korkuluk'],
    'Uretilen_Adet': [120, 45, 350, 80],
    'Hammadde_Maliyeti_TL': [1200, 1800, 250, 450],
    'Iscilik_Saati': [4, 6, 1, 3],
    'Makine_Enerji_Maliyeti_TL': [150, 220, 80, 60],
    'Fire_Orani_%': [5, 8, 12, 4]
}

df = pd.DataFrame(imalat_verisi)
iscilik_saat_ucreti = 200

df['Toplam_Iscilik_Maliyeti_TL'] = df['Iscilik_Saati'] * iscilik_saat_ucreti
df['Net_Malzeme_Maliyeti_TL'] = df['Hammadde_Maliyeti_TL'] * (1 + df['Fire_Orani_%'] / 100)
df['Tek_Urun_Toplam_Maliyeti_TL'] = df['Net_Malzeme_Maliyeti_TL'] + df['Toplam_Iscilik_Maliyeti_TL'] + df['Makine_Enerji_Maliyeti_TL']
df['Toplam_Parti_Maliyeti_TL'] = df['Tek_Urun_Toplam_Maliyeti_TL'] * df['Uretilen_Adet']

# Excel raporunu diske kaydediyoruz
df.to_excel('detayli_imalat_maliyet_raporu.xlsx', index=False)
print("⚙️  1. ADIM: Matematiksel Excel Raporu Hazırlandı.")

# --- 2. ADIM: YAPAY ZEKA AJANINI DEVREYE SOKMA ---
print("🤖 2. ADIM: Yerel Yapay Zeka (Gemma) Raporu İnceliyor, Lütfen Bekleyin...\n")

# Python, ürettiği tablonun özetini yapay zekanın anlayacağı bir metne dönüştürüyor
rapor_ozeti = ""
for index, row in df.iterrows():
    rapor_ozeti += f"- {row['Urun_Adi']}: {row['Uretilen_Adet']} adet üretildi. Tek ürün maliyeti {row['Tek_Urun_Toplam_Maliyeti_TL']:.2f} TL. Fire oranı %{row['Fire_Orani_%']}. İşçilik süresi {row['Iscilik_Saati']} saat.\n"

# Bilgisayarındaki Gemma'ya python üzerinden komut (Prompt) gönderiyoruz
emir = f"""
Sen bir fabrika üretim ve maliyet danışmanısın. Aşağıdaki üretim verilerini incele:
{rapor_ozeti}

Bir girişimci için fabrikadaki en büyük riskleri, en çok işçilik yiyen ürünü ve acil müdahale edilmesi gereken yerleri kısa ve öz maddeler halinde raporla.
"""

# Gemma'yı arka planda çalıştırıyoruz
response = ollama.chat(model='gemma2:2b', messages=[
    {
        'role': 'user',
        'content': emir,
    },
])

# Sonucu ekrana yazdırıyoruz
print("==================================================")
print("🎯 YAPAY ZEKA AJANININ STRATEJİK FABRİKA RAPORU:")
print("==================================================")
print(response['message']['content'])
print("==================================================")