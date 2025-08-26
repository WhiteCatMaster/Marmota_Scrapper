import os
import csv

# Nombre del archivo para guardar los enlaces.
URL_FILE_NAME = "comic_urls.csv"

def read_urls_from_file():
    """
    Lee los enlaces existentes del archivo CSV y los devuelve.
    """
    urls = []
    if os.path.exists(URL_FILE_NAME):
        with open(URL_FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    urls.append((row[0], row[1])) # Almacena tuplas de (nombre, url)
    return urls

def append_to_file(comic_name, url):
    """
    Añade un nuevo enlace al final del archivo CSV si no existe ya.
    """
    urls_in_file = read_urls_from_file()
    existing_urls_only = [url_item[1] for url_item in urls_in_file]

    if url in existing_urls_only:
        print(f"⚠️ ¡URL ya existente! '{url}' no se añadirá de nuevo.")
        return False
    else:
        with open(URL_FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([comic_name, url])
        print(f"✅ Añadido: {comic_name} -> {url}")
        return True

if __name__ == "__main__":
    
    print("--- 📚 Añadir URLs de cómics a un archivo CSV ---")
    
    # Define el nombre del cómic
    comic_name = input("¿Cuál es el nombre del cómic?: ")

    if not comic_name:
        print("❗ El nombre del cómic no puede estar vacío. Saliendo.")
    else:
        print("\nPor favor, introduce las URLs de los capítulos (una por una).")
        print("Cuando termines, escribe 'fin' y presiona Enter.")
        
        urls_added_count = 0
        while True:
            link = input(f"Ingresa la URL del capítulo #{urls_added_count + 1}: ")
            if link.lower() == 'fin':
                break
            if link:
                if append_to_file(comic_name, link):
                    urls_added_count += 1
        
        print(f"\n--- Proceso completado. Se añadieron {urls_added_count} URL(s) nuevas a '{URL_FILE_NAME}'. ---")

