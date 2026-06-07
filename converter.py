import json
import requests
import os
import re

# Eklenti verilerinin olduğu JSON dosyan
DATA_FILE = "data.json"
OUTPUT_DIR = "m3u_cikti"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_m3u_content(url):
    try:
        # Eklentinin içindeki M3U linkine gidip içeriği çekiyoruz
        response = requests.get(url, timeout=10)
        return response.text
    except Exception as e:
        print(f"Hata: {url} çekilemedi. {e}")
        return None

def convert_to_m3u(data):
    for item in data:
        name = item.get("name")
        # .cs3 dosyası içinde aslında M3U linki saklıdır
        # Gerçek uygulamada o linki bulmak için URL'yi parse ediyoruz
        # Sen şimdi o eklentilerin beslendiği asıl M3U linklerini buraya ekle
        target_m3u_url = item.get("url") # Eğer URL bir M3U ise direkt alır
        
        print(f"İşleniyor: {name} -> {target_m3u_url}")
        
        content = get_m3u_content(target_m3u_url)
        if content:
            # M3U standartlarına göre dosyayı kaydet
            output_path = os.path.join(OUTPUT_DIR, f"{name}.m3u")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Kaydedildi: {output_path}")

if __name__ == "__main__":
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    convert_to_m3u(data)
