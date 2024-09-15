import re
import time

import requests
from bs4 import BeautifulSoup
from loguru import logger

from app.models_benefit import remove_duplicates_benefit, add_user_benefit, ProductLinkBenefit, \
    get_all_product_links_benefit, add_product_benefit

# URL начальной страницы
base_url = 'https://belbazar24.by'


def get_html_benefit(url):
    """Получить HTML-код страницы по URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        logger.info(f"Не удалось получить страницу {url}. Код состояния: {response.status_code}")
        return None


def extract_product_benefit(soup):
    """Извлечь ссылки на товары со страницы."""
    product_links = []
    links = soup.find_all('a', class_='product_item_image')  # Поиск всех тегов <a> с классом 'product_item_image'
    for link in links:
        href = link.get('href')
        if href:
            full_url = base_url + href  # Дополняем URL до полного
            product_links.append(full_url)
    return product_links


def find_max_page_benefit(soup):
    """Найти наибольший номер страницы из навигации."""
    max_page = 1
    page_numbers = soup.select(
        '.navigation_content a')  # Поиск всех ссылок на страницы в элементе с классом 'navigation_content'
    for page_number in page_numbers:
        try:
            number = int(page_number.text.strip())  # Попытка получить номер страницы как целое число
            if number > max_page:
                max_page = number
        except ValueError:
            continue
    return max_page


def scrape_all_pages_benefit(start_url):
    """Собирать ссылки на товары со всех страниц с пагинацией."""

    remove_duplicates_benefit()  # Удаление дубликатов из базы данных

    try:
        html_content = get_html_benefit(start_url)  # Получаем HTML начальной страницы
        if not html_content:
            return []
        soup = BeautifulSoup(html_content, 'html.parser')
        max_page = find_max_page_benefit(soup)  # Определяем максимальное количество страниц
        logger.info(f"Наибольшая страница: {max_page}")
        for page in range(1, max_page + 1):  # Цикл по всем страницам
            current_url = f"{start_url}&page={page}"
            time.sleep(0.4)  # Пауза в 0.4 секунды, меньше не ставить, так как на сайте присутствует защита
            logger.info(f"Обрабатывается страница: {current_url}")
            html_content = get_html_benefit(current_url)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                product_links = extract_product_benefit(soup)  # Извлечение ссылок на товары
                logger.info(f"Найдено {len(product_links)} товаров")
                for product_links_benefit in product_links:
                    logger.info(f"Ссылки на товары: {product_links_benefit}")
                    add_user_benefit(product_links_benefit)

                    remove_duplicates_benefit()  # Удаление дубликатов из базы данных
            else:
                logger.info(f"Ошибка при получении страницы {current_url}")
    except Exception as e:
        logger.exception(e)

        remove_duplicates_benefit()  # Удаление дубликатов из базы данных


def remove_product_link_benefit(link):
    """Функция для удаления записи из таблицы `Product_Link` по значению `product_links`."""
    try:
        query = ProductLinkBenefit.get(ProductLinkBenefit.product_links_benefit == link)
        query.delete_instance()
        logger.info(f"Ссылка удалена: {link}")
    except ProductLinkBenefit.DoesNotExist:
        logger.warning(f"Ссылка не найдена в базе данных: {link}")
    except Exception as e:
        logger.error(f"Ошибка при удалении ссылки: {e}")


def parsing_products_via_links_benefit():
    """Парсинг данных из ссылок по базе данных"""

    all_links = get_all_product_links_benefit()  # Пример использования функции для чтения данных
    for link in all_links:
        try:

            html_content = get_html_benefit(link)  # Получаем HTML начальной страницы
            # Парсинг HTML с использованием BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Извлечение артикула из блока 'prod_top_title'
            prod_top_title = soup.find('div', class_='prod_top_title')
            if prod_top_title:
                article_text = prod_top_title.get_text(strip=True)
                # Использование регулярного выражения для извлечения текста после 'Арт.'
                match = re.search(r'Арт\.\s*([^\s\(\)]+)', article_text)
                if match:
                    article = match.group(1)
                else:
                    article = 'Не указан'
            else:
                article = 'Не указан'

            # Извлечение всех элементов с классом 'prod_param_item'
            params = soup.find_all('div', class_='prod_param_item')
            result = {}
            for param in params:
                key = param.find('b').get_text(strip=True).rstrip(':')
                value = param.get_text(strip=True).replace(key + ':', '').strip()
                result[key] = value

            # Извлечение необходимых данных
            material = result.get('Состав', 'Не указан')
            color = result.get('Цвет', 'Не указан')
            name = article  # Если название равно артикулу

            # Извлечение всех размеров с классом 'prod_size_item'
            sizes = soup.find_all('div', class_='prod_size_item')
            size_list = [size.get_text(strip=True) for size in sizes]
            size_output = ', '.join(size_list) if size_list else 'Не указано'

            # Логирование и сохранение
            logger.info(f"Ссылка {link}, Данные: Тип одежды: {result.get('Тип одежды', 'Не указано')}; Цвет: {color}; "
                        f"Состав: {material}; Рост: {result.get('Рост', 'Не указан')}, Размеры: {size_output}")

            # Добавление в базу данных
            add_product_benefit(
                link=link,  # Ссылка
                name=name,  # Название
                article=article,  # Артикул
                material=material,  # Тип одежды
                color=color,  # Цвет
                size=size_output  # Размеры
            )

            remove_product_link_benefit(link)  # Удаление ссылки после парсинга и добавления в базу данных

            remove_duplicates_benefit()  # Удаление дубликатов из базы данных
        except TypeError:  # Не рабочая ссылка
            logger.error(f"Ошибка при парсинге ссылки {link}: неверная ссылка")
        except requests.exceptions.ConnectionError:
            logger.error(f"Ошибка при парсинге ссылки {link}: не удалось подключиться к серверу или попытка сарвера "
                         f"разорвать соединения")
        except Exception as e:
            logger.exception(f"Ошибка при парсинге ссылки {link}: {e}")


if __name__ == '__main__':
    parsing_products_via_links_benefit()
