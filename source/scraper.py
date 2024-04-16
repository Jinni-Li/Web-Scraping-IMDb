import re
import urllib.request
import urllib.error
from urllib.parse import urljoin
import logging
from bs4 import BeautifulSoup
import pandas as pd

logging.basicConfig(level=logging.INFO)  # Configurar el nivel de registro


def download(url, user_agent='*', num_retries=2):
    """
    Descarga el contenido de una URL.

    Args:
        url (str): La URL para descargar.
        user_agent (str): El agente de usuario para enviar en el encabezado de la solicitud.
        num_retries (int): El número de reintentos en caso de error.

    Returns:
        str or None: El contenido de la URL, o None si no se puede descargar.
    """
    logging.info('Downloading: %s', url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read().decode('utf-8')
        return html
    except (urllib.error.URLError, UnicodeDecodeError) as e:
        logging.error('Download error: %s', e)
        if num_retries > 0:
            logging.info('Retrying (%d attempts left)...', num_retries)
            return download(url, user_agent, num_retries - 1)
    return None


def get_links(html):
    """
    Extrae los enlaces de una página HTML.

    Args:
        html (str): El contenido HTML de la página.

    Returns:
        list: Una lista de enlaces encontrados en la página.
    """
    if html:
        # Expresión regular para encontrar enlaces en el HTML
        webpage_regex = re.compile(r'<a[^>]+href=["\'](/title/tt\d+/\?ref_=chtmvm_t_\d+)["\']', re.IGNORECASE)
        # Encontrar todos los enlaces que coincidan con la expresión regular
        return webpage_regex.findall(html)
    return []

def extract_movie_info(html):
    """
    Extrae una lista que contiene el título, el título original, el rating, lo géneros y el director para cada película

        Args:
            html (str): El contenido HTML de la página.

        Returns:
            list: Una lista que contiene el título, el título original, el rating, lo géneros y el director de la película
    """
    soup = BeautifulSoup(html, "html.parser")

    # Título original
    original_title_tag = soup.find('div', class_='sc-d8941411-1 fTeJrK')
    raw_original_title = original_title_tag.text.strip() if original_title_tag else None
    regex = r'Original title: (.+)'
    match = re.search(regex, raw_original_title) if original_title_tag else None
    original_title = match.group(1) if original_title_tag else None

    # Título en español
    title_tag = soup.find('span', class_='hero__primary-text')
    title = title_tag.text.strip() if title_tag else None

    # Rating
    movie_rating_tag = soup.find('span', class_='sc-bde20123-1 cMEQkK')
    movie_rating = movie_rating_tag.text.strip() if movie_rating_tag else None

    # Géneros
    genres_container = soup.find('div', class_='ipc-chip-list__scroller')
    genres = [link.span.text.strip() for link in genres_container.find_all('a', class_='ipc-chip')] if genres_container else []
    # Divide los géneros en hasta tres variables diferentes
    genre1 = genres[0] if len(genres) > 0 else None
    genre2 = genres[1] if len(genres) > 1 else None
    genre3 = genres[2] if len(genres) > 2 else None

    # Director
    director_tag = soup.find('a', class_='ipc-metadata-list-item__list-content-item')
    director = director_tag.text.strip() if director_tag else None

    return original_title, title, movie_rating, genre1, genre2, genre3, director

def link_crawler(seed_url):
    """
    Rastrea enlaces en una página web a partir de una URL semilla.

    Args:
        seed_url (str): La URL semilla para iniciar el rastreo.

    Returns:
        list: Una lista de tuplas que contienen información de películas y los números de enlaces.
    """
    crawl_queue = [seed_url]
    crawled_links = set()  # Conjunto para almacenar los enlaces rastreados
    movie_data = []
    while crawl_queue:
        url = crawl_queue.pop()
        if url not in crawled_links:
            html = download(url)
            if html:
                crawled_links.add(url)  # Agregar el enlace actual al conjunto de enlaces rastreados
                # Extraer información de cada película
                original_title, title, movie_rating, genre1, genre2, genre3, director = extract_movie_info(html)
                movie_data.append((original_title, title, movie_rating, genre1, genre2, genre3, director))
                # Obtener los enlaces
                links = get_links(html)
                # Agregar las entradas al movie_data
                for link in links:
                    # Recorrer los enlaces encontrados en la página y agregarlos a la cola de rastreo
                    absolute_link = urljoin(seed_url, link)  # Construir la URL absoluta
                    crawl_queue.append(absolute_link)

    return movie_data


def extract_movie_data(seed_url):
    """
    Extrae una lista que contiene el título, el ranking, el año de estreno, la clasificación y la duración
    para cada película que se encuentra en la página web

        Args:
            seed_url (str): La URL para descargar.

        Returns:
            list: una lista que contiene el título, el ranking, el año de estreno, la clasificación y la duración
            para cada película que se encuentra en la página web
    """
    # Descargar la página web
    response = download(seed_url)
    soup = BeautifulSoup(response, "html.parser")
    movie_data = []

    # Buscar todos los nombres de películas dentro de etiquetas 'h3' con una clase específica
    movie_names = soup.find_all('h3', class_='ipc-title__text')[1:]

    # Buscar todos los metadatos de las películas dentro de etiquetas 'div' con una clase específica
    movie_metadata = soup.find_all('div', class_='sc-b189961a-7 feoqjK cli-title-metadata')

    # Buscar todas las etiquetas de clasificación dentro de etiquetas 'div' con una clase específica
    ranking_tags = soup.find_all('div',
                                 class_='sc-b8b74125-0 eukXAN meter-const-ranking sc-b189961a-6 fabIxY cli-meter-title-header')

    # Recorrer cada nombre, metadato y etiqueta de clasificación, extraer y almacenar la información
    for name, metadata, ranking_tag in zip(movie_names, movie_metadata, ranking_tags):
        # Extraer el nombre de la película
        movie_name = name.text.strip()

        # Extraer metadatos para cada película
        metadata_items = metadata.find_all('span', class_='sc-b189961a-8 kLaxqf cli-title-metadata-item')
        if len(metadata_items) == 3:
            movie_year = metadata_items[0].text.strip()
            movie_duration = metadata_items[1].text.strip()
            movie_classification = metadata_items[2].text.strip()
        else:
            movie_year, movie_duration, movie_classification = None, None, None

        # Extraer clasificación para cada película
        ranking_text = ranking_tag.get('aria-label', None)
        ranking_number = ranking_text.split(':')[-1].strip() if ranking_text else None

        # Agregar los datos de la película a la lista
        movie_data.append((movie_name, movie_year, movie_duration, movie_classification, ranking_number))

    return movie_data


def scraper():
    """
    Ejecuta todas las funciones y con el resultado crea una dataframe que después es guardado con formato csv

        Returns:
            df1: dataframe con todos los datos extracto del las páginas de detalle
            df2: dataframe con los datos extracto en la seed_page (películas populares)
            df_merge: combinación de df1 y df2 cuya indentificador es la variable 'title'
            csv_file: archivo csv que contiene todos los datos extractos.
    """
    seed_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    data = link_crawler(seed_url)
    print(data)

    df1 = pd.DataFrame(data, columns=['original_title', 'title', 'rating', 'genre1', 'genre2', 'genre3', 'director'])
    print("Dataframe from extract_movie_info:")
    print(df1)

    movie_data = extract_movie_data(seed_url)
    df2 = pd.DataFrame(movie_data, columns=['title', 'year', 'duration', 'classification', 'ranking'])
    print("\nDataframe from extract_movie_data:")
    print(df2)

    # Combinar df1 con df2 a través de 'title'
    merged_df = pd.merge(df1, df2, on='title', how='inner')
    print("\nMerged dataframe:")
    print(merged_df)

    merged_df.to_csv('dataset/dataset.csv', index=False)