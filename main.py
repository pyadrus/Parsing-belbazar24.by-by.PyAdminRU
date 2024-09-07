import time

import requests
from bs4 import BeautifulSoup
from loguru import logger

# URL начальной страницы
base_url = 'https://belbazar24.by'
start_url = 'https://belbazar24.by/women/dress/?filtr=3:33;3:34;3:35;3:36;3:37;3:38;3:39;3:40;3:41;3:42;3:43;3:44;3:45;3:46;3:47;3:48;3:49;3:50;3:51;3:52;3:53;3:54;3:55;3:56;3:57;3:58;3:59;3:60;3:61;6:73;6:74;6:75;6:76;6:77;6:78;6:79;6:80;6:81;6:82;6:83;6:84;6:85;6:86;6:87;6:88'

logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы


def get_html(url):
    """Получить HTML-код страницы по URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        logger.info(f"Не удалось получить страницу {url}. Код состояния: {response.status_code}")
        return None


def extract_product_links(soup):
    """Извлечь ссылки на товары со страницы."""
    product_links = []
    # Поиск всех тегов <a> с классом 'product_item_image'
    links = soup.find_all('a', class_='product_item_image')
    for link in links:
        href = link.get('href')
        if href:
            full_url = base_url + href  # Дополняем URL до полного
            product_links.append(full_url)
    return product_links


def find_max_page(soup):
    """Найти наибольший номер страницы из навигации."""
    max_page = 1
    # Поиск всех ссылок на страницы в элементе с классом 'navigation_content'
    page_numbers = soup.select('.navigation_content a')
    for page_number in page_numbers:
        try:
            # Попытка получить номер страницы как целое число
            number = int(page_number.text.strip())
            if number > max_page:
                max_page = number
        except ValueError:
            continue
    return max_page


def scrape_all_pages(start_url):
    """Собирать ссылки на товары со всех страниц с пагинацией."""
    # Получаем HTML начальной страницы
    html_content = get_html(start_url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')

    # Определяем максимальное количество страниц
    max_page = find_max_page(soup)
    logger.info(f"Наибольшая страница: {max_page}")

    all_product_links = []

    # Цикл по всем страницам
    for page in range(1, max_page + 1):
        current_url = f"{start_url}&page={page}"
        time.sleep(0.2)
        logger.info(f"Обрабатывается страница: {current_url}")
        html_content = get_html(current_url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Извлечение ссылок на товары
            product_links = extract_product_links(soup)
            logger.info(f"Ссылки на товары: {product_links}")
            logger.info(f"Найдено {len(product_links)} товаров")
            all_product_links.extend(product_links)
        else:
            logger.info(f"Ошибка при получении страницы {current_url}")

    return all_product_links



all_product_links = scrape_all_pages(start_url)# Запуск сбора данных


logger.info("\nВсе ссылки на товары:")# Вывод всех найденных ссылок на товары
for link in all_product_links:
    logger.info(link)
