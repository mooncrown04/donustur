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
    """CS3 dosyasını indir, içindeki metin dosyalarını tara ve mainUrl'i bul."""
    try:
        response = requests.get(cs3_url, timeout=15)
        # CS3 paketini bellekte bir zip olarak aç
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for file_name in z.namelist():
                # Genelde kodlar .class veya .kt (eğer kaynak varsa) uzantılıdır
                # .dex veya .class dosyaları binarydir, bunları decode etmeye çalışacağız
                try:
                    with z.open(file_name) as f:
                        content = f.read().decode('utf-8', errors='ignore')
                        # mainUrl = "..." kısmını ara
                        match = re.search(r'mainUrl\s*=\s*["\'](https?://.*?)["\']', content)
                        if match:
                            return match.group(1)
                except:
                    continue
    except Exception as e:
        print(f"CS3 işleme hatası: {e}")
    return None

def convert_to_m3u(data):
    for item in data:
        name = item.get("name")
        cs3_url = item.get("url")
        
        print(f"İşleniyor: {name}...")
        
        # 1. Adım: CS3'ün içinden asıl M3U linkini bul
        m3u_link = extract_main_url_from_cs3(cs3_url)
        
        if m3u_link:
            print(f"  -> Bulunan M3U: {m3u_link}")
            # 2. Adım: O M3U linkine git ve içeriği çek
            m3u_response = requests.get(m3u_link, timeout=15)
            if m3u_response.status_code == 200:
                output_path = os.path.join(OUTPUT_DIR, f"{name}.m3u")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(m3u_response.text)
                print(f"  -> Kaydedildi: {output_path}")
        else:
            print(f"  -> Uyarı: {name} içinde mainUrl bulunamadı!")

if __name__ == "__main__":
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    convert_to_m3u(data)
