import time

import requests
from bs4 import BeautifulSoup
from loguru import logger

from database import add_user, remove_duplicates, get_all_product_links

# URL начальной страницы
base_url = 'https://belbazar24.by'

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
    links = soup.find_all('a', class_='product_item_image') # Поиск всех тегов <a> с классом 'product_item_image'
    for link in links:
        href = link.get('href')
        if href:
            full_url = base_url + href  # Дополняем URL до полного
            product_links.append(full_url)
    return product_links


def find_max_page(soup):
    """Найти наибольший номер страницы из навигации."""
    max_page = 1
    page_numbers = soup.select('.navigation_content a')# Поиск всех ссылок на страницы в элементе с классом 'navigation_content'
    for page_number in page_numbers:
        try:
            number = int(page_number.text.strip())# Попытка получить номер страницы как целое число
            if number > max_page:
                max_page = number
        except ValueError:
            continue
    return max_page


def scrape_all_pages(start_url):
    """Собирать ссылки на товары со всех страниц с пагинацией."""
    try:
        html_content = get_html(start_url) # Получаем HTML начальной страницы
        if not html_content:
            return []
        soup = BeautifulSoup(html_content, 'html.parser')
        max_page = find_max_page(soup)# Определяем максимальное количество страниц
        logger.info(f"Наибольшая страница: {max_page}")
        for page in range(1, max_page + 1):# Цикл по всем страницам
            current_url = f"{start_url}&page={page}"
            time.sleep(0.4) # Пауза в 0.4 секунды, меньше не ставить, так как на сайте присутствует защита
            logger.info(f"Обрабатывается страница: {current_url}")
            html_content = get_html(current_url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                product_links = extract_product_links(soup)# Извлечение ссылок на товары
                logger.info(f"Найдено {len(product_links)} товаров")
                for product_link in product_links:
                    logger.info(f"Ссылки на товары: {product_link}")
                    add_user(product_link)
                remove_duplicates() # Удаление дубликатов из базы данных
            else:
                logger.info(f"Ошибка при получении страницы {current_url}")
    except Exception as e:
        logger.exception(e)

def parsing_products_via_links():
    """Парсинг данных из ссылок по базе данных"""
    all_links = get_all_product_links()  # Пример использования функции для чтения данных

    for link in all_links:
        logger.info(link)  # Вывод всех ссылок из базы данных

if __name__ == '__main__':
    parsing_products_via_links()