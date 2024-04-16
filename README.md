# Web Sraping IMDb: Películas Populares de IMDb en abril 2024
## Este proyecto está realizado únicamente por Jinni Li
Proyecto realizado como tarea de la asignatura "Tipología y ciclo de vida de datos" en la "Universitat Oberta de Catalunya"
Consiste en un proyecto de web scraping para extrer informaciones relevanes de las películas valoradas como más populares en el abril del año 2024 en IMDb.com
## Contenido
El proyecto contiene 2 carpetas: `dataset` y `resource`.
En `resource` se encuentra todos los módulos python que compone proceso de web scraping, que sonincluye los siguientes módulos y archivos:
- `background_research.py`: Contiene las funciones para obtener el robot.txt, el propietario y la tecnología usada en una website
- `scraper.py`: Contiene todas las funciones para extraer los datos de la web IMDb.com y convertirlos en dataset.csv
- `main.py`: la ejecución

En `dataset` se encuentran los archivos generados por los scripts en `resource`:
-`dataset.csv`: archivo csv que contiene todos los datos extraídos del IMDb
-`background_researc_output`: archivo que contiene el robot.txt, las tecnologías usadas y la "ownership" de IMDb.com

Fuera de las carpeta se encuentra:
- `README.md`: Este archivo, proporcionando información sobre el proyecto y su ejecución.
- `requirements.txt`: Contiene todas las librerías usadas en el proyecto
- `LICENSE`: Archivo que contiene la licencia bajo la cual se distribuye el código.

## Ejecución
Para ejecutar el proyecto, ejecuta el script principal: `main.py`

## Licencia

Este proyecto está bajo la licencia CC BY-SA 4.0. Puedes utilizar, compartir y modificar libremente este código, siempre y cuando des crédito al autor original y compartas tus modificaciones bajo la misma licencia.
