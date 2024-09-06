import requests
from bs4 import BeautifulSoup

url = 'https://belbazar24.by/women/dress/?filtr=3:33;3:34;3:35;3:36;3:37;3:38;3:39;3:40;3:41;3:42;3:43;3:44;3:45;3:46;3:47;3:48;3:49;3:50;3:51;3:52;3:53;3:54;3:55;3:56;3:57;3:58;3:59;3:60;3:61;6:73;6:74;6:75;6:76;6:77;6:78;6:79;6:80;6:81;6:82;6:83;6:84;6:85;6:86;6:87;6:88'

response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    html_content = response.text

    # Создание объекта BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Поиск всех элементов с классом, содержащим 'product_item_art'
    # Поиск всех тегов <a> с классом 'product_item_image'
    links = soup.find_all('a', class_='product_item_image')
    # Вывод всех найденных ссылок
    for link in links:
        href = link.get('href')
        if href:
            full_url = 'https://belbazar24.by' + href  # Дополняем URL до полного
            print(full_url)
    # product_item_size = soup.find_all(class_='product_item_size')
    # product_item_price = soup.find_all(class_='product_item_price')
    # Вывод всех найденных элементов
    # for item in product_item_image:
    #     print(item.get_text(strip=True))

    # for size in product_item_size:
    #     print(size.get_text(strip=True))

    # for price in product_item_price:
    #     print(price.get_text(strip=True))


else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

"""
Собираем данные из html 

Товар: ноче мио 6865-2 
Размер: 44; 46; 48; 50
Материал «акрил»

"""