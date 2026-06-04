import pandas as pd

# Örnek veri oluştur
veri = {
    'Ürün': ['Cıvata', 'Pul', 'Somun'],
    'Birim_Maliyeti': [0.5, 0.2, 0.8],
    'Miktar': [1000, 5000, 500]
}

# DataFrame oluştur
df = pd.DataFrame(veri)

# Excel'e kaydet
df.to_excel('uretim_maliyeti.xlsx', index=False)

print("✅ uretim_maliyeti.xlsx oluşturuldu!")
print(df)