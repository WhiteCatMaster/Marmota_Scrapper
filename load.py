import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import zipfile
import csv

# Ruta absoluta donde Kavita guarda la librería
LIBRARY_PATH = "/home/ubuntu/comics/kavita/data"
# Nombre del archivo para guardar los enlaces
URL_FILE_NAME = "comic_urls.csv"

def scrape_chapter(url, output_name):
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"📥 Descargando desde: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la URL {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img", {"data-src": True})
    images = []

    print(f"🔎 Encontradas {len(img_tags)} imágenes en la página...")

    for i, img in enumerate(img_tags):
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

    for f in images:
        os.remove(f)
    os.rmdir(temp_dir)
    print("🧹 Archivos temporales eliminados.")

def scrape_multiple(urls, comic_name, comic_year):
    if not urls:
        print("❗ No se han proporcionado URLs. Saliendo.")
        return
    for idx, url in enumerate(urls, start=1):
        chapter_name = f"{comic_name} ({comic_year}) - #{idx}"
        scrape_chapter(url, chapter_name)
        print("-" * 40)

def read_urls_from_file():
    urls = []
    if os.path.exists(URL_FILE_NAME):
        with open(URL_FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    urls.append((row[0], row[1])) # Almacena tuplas de (nombre, url)
    return urls

def append_to_file(comic_name, url):
    with open(URL_FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([comic_name, url])

if __name__ == "__main__":
    
    # 1. Lee los enlaces existentes del archivo CSV
    urls_from_file = read_urls_from_file()
    if urls_from_file:
        print(f"✅ Se encontraron {len(urls_from_file)} URL(s) en '{URL_FILE_NAME}'.")
        
        # Procesa los cómics del archivo
        # Asume que todos los cómics del archivo son de la misma serie
        comic_name, _ = urls_from_file[0]
        comic_urls_only = [url for _, url in urls_from_file]
        print("Iniciando descarga de cómics desde el archivo...")
        scrape_multiple(comic_urls_only, comic_name, "2024")

    # 2. Pide nuevos enlaces al usuario y los añade al archivo y a la lista de descargas
    print("\nPor favor, introduce nuevas URLs para descargar.")
    print("Cuando termines, escribe 'fin' y presiona Enter.")
    
    urls_to_scrape = []
    comic_name_input = input("¿Cuál es el nombre del cómic?: ")
    
    while True:
        link = input(f"Ingresa la URL del capítulo #{len(urls_to_scrape) + 1}: ")
        if link.lower() == 'fin':
            break
        if link:
            urls_to_scrape.append(link)
            append_to_file(comic_name_input, link)
            
    # Procesa las nuevas URLs introducidas
    if urls_to_scrape:
        print("\nIniciando descarga de los nuevos cómics...")
        scrape_multiple(urls_to_scrape, comic_name_input, "2024")

    print("\nProceso de scraping finalizado.")