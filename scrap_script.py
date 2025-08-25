import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import zipfile

# Ruta absoluta donde Kavita guarda la librería
LIBRARY_PATH = "/home/wcMaster/projects/comics/kavita/data"

def scrape_chapter(url, output_name):
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"📥 Descargando desde: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    img_tags = soup.find_all("img")
    images = []

    for i, img in enumerate(img_tags):
        src = img.get("src")
        if not src:
            continue
        try:
            r = requests.get(src)
            image = Image.open(BytesIO(r.content)).convert("RGB")
            filename = os.path.join(temp_dir, f"{i:03}.jpg")
            image.save(filename, "JPEG")
            images.append(filename)
            print(f"   ✅ {filename}")
        except Exception as e:
            print(f"   ⚠️ Error con {src}: {e}")

    os.makedirs(LIBRARY_PATH, exist_ok=True)

    output_path = os.path.join(LIBRARY_PATH, f"{output_name}.cbz")
    with zipfile.ZipFile(output_path, 'w') as cbz:
        for img in sorted(images):
            cbz.write(img, os.path.basename(img))

    print(f"📚 Archivo creado: {output_path}")

    # Limpiar
    for f in images:
        os.remove(f)
    os.rmdir(temp_dir)


def scrape_multiple(urls, prefix="Comic"):
    for idx, url in enumerate(urls, start=1):
        chapter_name = f"{prefix} - Capítulo {idx}"
        scrape_chapter(url, chapter_name)


if __name__ == "__main__":
    urls = [
        "https://ejemplo.com/capitulo1",
        "https://ejemplo.com/capitulo2",
        "https://ejemplo.com/capitulo3"
    ]
    scrape_multiple(urls, prefix="MiSerie")
