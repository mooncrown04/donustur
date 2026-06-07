import json

def generate_m3u(input_json, output_file):
    # JSON dosyasını oku
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # M3U dosyasını yaz
    with open(output_file, 'w', encoding='utf-8') as m3u:
        m3u.write("#EXTM3U\n")
        for item in data:
            name = item.get("name", "Bilinmeyen")
            url = item.get("url", "#")
            # mkvod formatına uygun M3U satırı
            m3u.write(f"#EXTINF:-1, {name}\n{url}\n")
    
    print(f"Bitti! {output_file} dosyası oluşturuldu.")

# Çalıştır
if __name__ == "__main__":
    generate_m3u("data.json", "liste.m3u")
