import pandas as pd

# 1. Adım: Az önce ürettiğimiz Excel dosyasını bilgisayarın hafızasına okuyoruz
df = pd.read_excel('uretim_verileri.xlsx')

# 2. Adım: Matematiksel analizleri yapıyoruz
toplam_uretim = df['Uretim_Adedi'].sum()

# Her ürünün toplam maliyetini hesaplayıp yeni bir sütun olarak ekliyoruz
df['Toplam_Maliyet_TL'] = df['Uretim_Adedi'] * df['Birim_Maliyet_TL']
genel_toplam_maliyet = df['Toplam_Maliyet_TL'].sum()

# Hata oranını hesaplıyoruz (Hatalı Ürün / Toplam Üretim)
df['Hata_Orani_%'] = (df['Hatalı_Urun'] / df['Uretim_Adedi']) * 100

# En yüksek hata oranına sahip ürünü buluyoruz
en_hatali_urun_index = df['Hata_Orani_%'].idxmax()
en_hatali_urun = df.loc[en_hatali_urun_index, 'Urun_Adi']
en_yuksek_oran = df.loc[en_hatali_urun_index, 'Hata_Orani_%']

# 3. Adım: Sonuçları ekrana şık bir rapor olarak yazdırıyoruz
print("==============================")
print("     FABRİKA ANALİZ RAPORU    ")
print("==============================")
print(f"Toplam Üretilen Ürün Adedi: {toplam_uretim} adet")
print(f"Toplam Üretim Maliyeti: {genel_toplam_maliyet:,.2f} TL")
print(f"En Yüksek Hata Oranı: {en_hatali_urun} (%{en_yuksek_oran:.2f})")
print("==============================")