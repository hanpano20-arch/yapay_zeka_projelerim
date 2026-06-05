import pandas as pd

# Excel'i oku
df = pd.read_excel('uretim_maliyeti.xlsx')

# Toplam maliyeti hesapla
df['Toplam_Maliyet'] = df['Birim_Maliyeti'] * df['Miktar']

print("=" * 50)
print("📊 ÜRÜN MALİYET ANALİZİ")
print("=" * 50)
print(df)
print("\n")
print(f"💰 Toplam Maliyet: {df['Toplam_Maliyet'].sum():.2f} TL")
print(f"📈 En Pahalı Ürün: {df.loc[df['Toplam_Maliyet'].idxmax(), 'Ürün']}")
print(f"⚡ En Ucuz Ürün: {df.loc[df['Toplam_Maliyet'].idxmin(), 'Ürün']}")