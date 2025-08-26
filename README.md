📖 Lector de Cómics Automático - Scraper de Marmota
Este proyecto te permite gestionar y descargar cómics de la página marmota.me de una forma sencilla y organizada, ideal para ser utilizado con tu propio servidor de cómics, como Kavita.

🚀 Cómo Usar el Script
El flujo de trabajo se divide en dos pasos clave para que puedas añadir y descargar cómics de forma eficiente:

1. Añadir los Enlaces (Script de Python)
Utiliza el script comic_url_adder.py para añadir los enlaces de los capítulos que quieres descargar a un archivo CSV. Este paso te permite gestionar tu lista de cómics de forma manual y evitar duplicados.

Ejecuta el script de Python:

python3 comic_url_adder.py

El script te guiará para que introduzcas el nombre del cómic y las URLs de los capítulos que deseas añadir. La información se guardará en un archivo llamado comic_urls.csv.

2. Descargar los Cómics (Script de Shell)
Una vez que hayas añadido los enlaces al archivo CSV, el script de shell se encargará de todo el proceso de descarga y la construcción del contenedor de Docker.

Ejecuta el script de shell:

sudo docker compose -d --build

Este comando hará lo siguiente automáticamente:

Lee las URLs del archivo CSV que generaste en el paso anterior.

Descarga cada capítulo y lo convierte en un archivo .cbz.

Coloca los archivos .cbz en la carpeta de tu servidor de cómics (montada como un volumen en el contenedor de Docker).

Se asegura de que tu servidor de cómics esté actualizado y funcionando en segundo plano.