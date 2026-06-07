import json
import requests
import re
import os

# Ayarlar
DATA_FILE = "data.json"
REPO_SOURCE_URL = "https://raw.githubusercontent.com/mooncrown04/TestPlugins/master"
OUTPUT_DIR = "m3u_cikti"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def get_m3u_from_kt(plugin_name):
    """Kaynak .kt dosyasını indir ve mainUrl'i regex ile bul."""
    # Eklenti ismine göre .kt dosyasının GitHub ham linkini oluştur
    kt_url = f"{REPO_SOURCE_URL}/{plugin_name}.kt"
    try:
        response = requests.get(kt_url, timeout=10)
        if response.status_code == 200:
            # İçerikte mainUrl = "..." kısmını ara
            match = re.search(r'mainUrl\s*=\s*"(.*?)"', response.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Hata: {plugin_name} kaynak kodu çekilemedi: {e}")
    return None

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        name = item.get("name")
        print(f"İşleniyor: {name}")
        
        m3u_url = get_m3u_from_kt(name)
        if m3u_url:
            print(f"  -> Bulunan Link: {m3u_url}")
            # M3U içeriğini çek ve dosyaya yaz
            try:
                m3u_res = requests.get(m3u_url, timeout=10)
                if m3u_res.status_code == 200:
                    output_path = os.path.join(OUTPUT_DIR, f"{name}.m3u")
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(m3u_res.text)
                    print(f"  -> Kaydedildi: {output_path}")
            except Exception as e:
                print(f"  -> M3U indirme hatası: {e}")
        else:
            print(f"  -> Uyarı: {name} için link bulunamadı.")

if __name__ == "__main__":
    main()
