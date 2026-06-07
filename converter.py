import json
import requests
import os
import zipfile
import io
import re

DATA_FILE = "data.json"
OUTPUT_DIR = "m3u_cikti"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def extract_main_url_from_cs3(cs3_url):
    print(f"  [DEBUG] İndiriliyor: {cs3_url}")
    try:
        response = requests.get(cs3_url, timeout=20)
        if response.status_code != 200:
            print(f"  [HATA] İndirme başarısız, kod: {response.status_code}")
            return None
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for file_name in z.namelist():
                # Sadece metin tabanlı dosyaları incele
                if file_name.endswith(('.kt', '.java', '.json', '.txt', '.dex')):
                    try:
                        with z.open(file_name) as f:
                            content = f.read().decode('utf-8', errors='ignore')
                            # Daha geniş bir arama yapalım
                            match = re.search(r'mainUrl\s*=\s*["\'](https?://[^"\']+)["\']', content)
                            if match:
                                return match.group(1)
                    except:
                        continue
        print("  [UYARI] Zip içinde mainUrl bulunamadı.")
    except Exception as e:
        print(f"  [HATA] İstisna oluştu: {str(e)}")
    return None

def convert_to_m3u(data):
    if not data:
        print("Data dosyası boş!")
        return

    for item in data:
        name = item.get("name")
        cs3_url = item.get("url")
        print(f"\nİşleniyor: {name}")
        
        m3u_link = extract_main_url_from_cs3(cs3_url)
        
        if m3u_link:
            print(f"  -> Bulundu: {m3u_link}")
            try:
                m3u_response = requests.get(m3u_link, timeout=15)
                output_path = os.path.join(OUTPUT_DIR, f"{name}.m3u")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(m3u_response.text)
                print(f"  -> BAŞARILI: {output_path}")
            except Exception as e:
                print(f"  -> M3U İndirme Hatası: {e}")
        else:
            print(f"  -> BAŞARISIZ: Link çıkarılamadı.")

if __name__ == "__main__":
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        convert_to_m3u(data)
    else:
        print(f"{DATA_FILE} dosyası bulunamadı!")
