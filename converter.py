import json
import requests
import os
import zipfile
import io
import re

DATA_FILE = "data.json"
OUTPUT_DIR = "m3u_cikti"

# Hata ayıklama için çalışma dizinini yazdıralım
print(f"Çalışma dizini: {os.getcwd()}")
print(f"Dosyalar: {os.listdir('.')}")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"{OUTPUT_DIR} klasörü oluşturuldu.")

def convert_to_m3u():
    if not os.path.exists(DATA_FILE):
        print(f"HATA: {DATA_FILE} dosyası bulunamadı!")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        name = item.get("name")
        cs3_url = item.get("url")
        print(f"\n--- İşleniyor: {name} ---")
        
        # Link çekme (Basitleştirilmiş)
        try:
            response = requests.get(cs3_url, timeout=20)
            if response.status_code != 200:
                print(f"HATA: {cs3_url} erişilemedi. Kod: {response.status_code}")
                continue
                
            # Zip içeriğini bellekte tara
            found_url = None
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                for file_name in z.namelist():
                    if file_name.endswith(('.kt', '.java')):
                        content = z.open(file_name).read().decode('utf-8', errors='ignore')
                        match = re.search(r'mainUrl\s*=\s*["\'](https?://[^"\']+)["\']', content)
                        if match:
                            found_url = match.group(1)
                            print(f"URL bulundu: {found_url}")
                            break
            
            if found_url:
                m3u_res = requests.get(found_url, timeout=20)
                output_path = os.path.join(OUTPUT_DIR, f"{name}.m3u")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(m3u_res.text)
                print(f"BAŞARILI: {output_path} yazıldı.")
            else:
                print("URL bulunamadı.")
        except Exception as e:
            print(f"HATA: {e}")

if __name__ == "__main__":
    convert_to_m3u()
