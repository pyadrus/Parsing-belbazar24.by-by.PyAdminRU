import requests
from bs4 import BeautifulSoup

# URL начальной страницы
base_url = 'https://belbazar24.by'
start_url = 'https://belbazar24.by/women/dress/?filtr=3:33;3:34;3:35;3:36;3:37;3:38;3:39;3:40;3:41;3:42;3:43;3:44;3:45;3:46;3:47;3:48;3:49;3:50;3:51;3:52;3:53;3:54;3:55;3:56;3:57;3:58;3:59;3:60;3:61;6:73;6:74;6:75;6:76;6:77;6:78;6:79;6:80;6:81;6:82;6:83;6:84;6:85;6:86;6:87;6:88'


def get_html(url):
    """Получить HTML-код страницы по URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Не удалось получить страницу {url}. Код состояния: {response.status_code}")
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


def find_next_page(soup):
    """Найти ссылку на следующую страницу."""
    next_page_link = soup.find('a', class_='navigation_link_right')
    if next_page_link and next_page_link.get('href'):
        return base_url + next_page_link.get('href')
    return None


def scrape_all_pages(start_url):
    """Собирать ссылки на товары со всех страниц с пагинацией."""
    current_url = start_url
    all_product_links = []

    while current_url:
        print(f"Обрабатывается страница: {current_url}")
        html_content = get_html(current_url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            # Извлечение ссылок на товары
            product_links = extract_product_links(soup)
            all_product_links.extend(product_links)

            # Поиск следующей страницы
            current_url = find_next_page(soup)
        else:
            break

    return all_product_links


# Запуск сбора данных
all_product_links = scrape_all_pages(start_url)

# Вывод всех найденных ссылок на товары
print("\nВсе ссылки на товары:")
for link in all_product_links:
    print(link)
