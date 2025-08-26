import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import zipfile

# Ruta absoluta donde Kavita guarda la librería
# Reemplaza la línea existente con la ruta absoluta
LIBRARY_PATH = "/home/ubuntu/comics/kavita/data"

def scrape_chapter(url, output_name):
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"📥 Descargando desde: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la solicitud falla
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la URL {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    # Busca todas las etiquetas <img> que tienen el atributo 'data-src'
    img_tags = soup.find_all("img", {"data-src": True})
    images = []

    print(f"🔎 Encontradas {len(img_tags)} imágenes en la página...")

    for i, img in enumerate(img_tags):
        # La URL real de la imagen está en el atributo 'data-src'
        src = img.get("data-src", "").strip()
        if not src:
            continue
        try:
            r = requests.get(src)
            r.raise_for_status()
            image = Image.open(BytesIO(r.content)).convert("RGB")
            filename = os.path.join(temp_dir, f"{i:03}.jpg")
            image.save(filename, "JPEG")
            images.append(filename)
            print(f"   ✅ Descargada la página {i}: {filename}")
        except Exception as e:
            print(f"   ⚠️ Error con {src}: {e}")

    if not images:
        print("🤷‍♂️ No se encontraron imágenes válidas para descargar.")
        return

    os.makedirs(LIBRARY_PATH, exist_ok=True)

    output_path = os.path.join(LIBRARY_PATH, f"{output_name}.cbz")
    with zipfile.ZipFile(output_path, 'w') as cbz:
        for img in sorted(images):
            cbz.write(img, os.path.basename(img))

    print(f"📚 Archivo CBZ creado con éxito: {output_path}")

    # Limpiar
    for f in images:
        os.remove(f)
    os.rmdir(temp_dir)
    print("🧹 Archivos temporales eliminados.")

def scrape_multiple(urls, comic_name, comic_year):
    if not urls:
        print("❗ No se han proporcionado URLs. Saliendo.")
        return
    for idx, url in enumerate(urls, start=1):
        # Formato de nombre: "Nombre del Cómic (Año) - #Número del capítulo"
        chapter_name = f"{comic_name} ({comic_year}) - #{idx}"
        scrape_chapter(url, chapter_name)
        print("-" * 40)

if __name__ == "__main__":
    urls = []
    
    # Define el nombre del cómic y el año aquí
    comic_name = input("Cual es el nombre?: ")
    comic_year = "2024"

    print("Por favor, introduce las URLs de los capítulos (una por una).")
    print("Cuando termines, escribe 'fin' y presiona Enter.")
    
    while True:
        link = input(f"Ingresa la URL del capítulo #{len(urls) + 1}: ")
        if link.lower() == 'fin':
            break
        if link:
            urls.append(link)
    
    scrape_multiple(urls, comic_name, comic_year)