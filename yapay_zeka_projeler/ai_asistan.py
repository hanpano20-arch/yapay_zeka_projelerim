import requests
import json

# Ollama'ya bağlan (localhost:11434)
def ai_sorusoru(soru):
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'mistral',
            'prompt': soru,
            'stream': False
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['response']
    else:
        return "Hata: AI yanıt veremedi"

# Test et
print("🤖 YEREL AI ASISTAN")
print("=" * 50)

soru = "Türkçe olarak: Bir fabrika için maliyet analizi nasıl yapılır? Kısaca açıkla."
print(f"Soru: {soru}\n")

cevap = ai_sorusoru(soru)
print(f"Cevap:\n{cevap}")