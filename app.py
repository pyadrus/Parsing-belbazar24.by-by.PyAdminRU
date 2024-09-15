from flask import Flask, render_template, request, redirect, url_for

from app.parsing import scrape_all_pages, parsing_products_via_links
from app.parsing_benefit import scrape_all_pages_benefit, parsing_products_via_links_benefit
from app.recording_data import export_products_to_csv, export_products_to_csv_benefit

# Фильтр "Материал и цвет"
start_url = 'https://belbazar24.by/women/dress/?filtr=3:33;3:34;3:35;3:36;3:37;3:38;3:39;3:40;3:41;3:42;3:43;3:44;3:45;3:46;3:47;3:48;3:49;3:50;3:51;3:52;3:53;3:54;3:55;3:56;3:57;3:58;3:59;3:60;3:61;6:73;6:74;6:75;6:76;6:77;6:78;6:79;6:80;6:81;6:82;6:83;6:84;6:85;6:86;6:87;6:88'

start_urls = 'https://belbazar24.by/women/dress/?filtr=999:last-size'

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/action', methods=['POST'])
def action():
    user_input = int(request.form['user_input'])

    # Фильтр "Материал и цвет"
    if user_input == 1:
        scrape_all_pages(start_url)  # Запуск сбора данных
    elif user_input == 2:
        parsing_products_via_links()
        return redirect(url_for('loading_pars'))
    elif user_input == 3:
        export_products_to_csv(file_path='products.csv')
        return redirect(url_for('loading'))

    # Фильтр "Купи выгодно"
    elif user_input == 4:
        scrape_all_pages_benefit(start_urls)  # Запуск сбора данных "Купить выгодно"
    elif user_input == 5:
        parsing_products_via_links_benefit()
        return redirect(url_for('loading_pars'))
    elif user_input == 6:
        export_products_to_csv_benefit(file_path='products_benefit.csv')
        return redirect(url_for('loading'))

    return redirect(url_for('index'))


@app.route('/loading_pars')
def loading_pars():
    """Показывает страницу загрузки"""
    return render_template('loading_pars.html')


@app.route('/loading')
def loading():
    """Показывает страницу загрузки"""
    return render_template('loading.html')


if __name__ == '__main__':
    app.run(debug=True)
