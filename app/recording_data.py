import csv
from peewee import *
from loguru import logger

db = SqliteDatabase('database.db')  # Настройка подключения к базе данных


class BaseModel(Model):
    """Определение модели"""

    class Meta:
        database = db


class Product(BaseModel):
    """Модель для хранения информации о продуктах"""
    link = CharField(unique=True)  # Ссылка на товар
    name = CharField()  # Название товара (равно артикулу)
    article = CharField()  # Артикул
    material = CharField()  # Материал
    color = CharField()  # Цвет
    size = CharField()  # Размер


def export_products_to_csv(file_path):
    """
    Функция для экспорта данных из таблицы `Product` в CSV файл.
    :param file_path: Путь к файлу
    """
    try:
        # Открытие файла для записи
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            # Определение полей для CSV
            fieldnames = ['link', 'name', 'article', 'material', 'color', 'size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Запись заголовков
            writer.writeheader()

            # Извлечение всех записей из таблицы `Product`
            products = Product.select()

            # Запись данных в CSV
            for product in products:
                writer.writerow({
                    'link': product.link,
                    'name': product.name,
                    'article': product.article,
                    'material': product.material,
                    'color': product.color,
                    'size': product.size
                })

        logger.info(f"Данные успешно экспортированы в файл: {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при экспорте данных в CSV: {e}")


class ProductBenefit(BaseModel):
    """Модель для хранения информации о продуктах"""
    link = CharField(unique=True)  # Ссылка на товар
    name = CharField()  # Название товара (равно артикулу)
    article = CharField()  # Артикул
    material = CharField()  # Материал
    color = CharField()  # Цвет
    size = CharField()  # Размер


def export_products_to_csv_benefit(file_path):
    """
    Функция для экспорта данных из таблицы `Product` в CSV файл.
    :param file_path: Путь к файлу
    """
    try:
        # Открытие файла для записи
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            # Определение полей для CSV
            fieldnames = ['link', 'name', 'article', 'material', 'color', 'size']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Запись заголовков
            writer.writeheader()

            # Извлечение всех записей из таблицы `Product`
            products = ProductBenefit.select()

            # Запись данных в CSV
            for product in products:
                writer.writerow({
                    'link': product.link,
                    'name': product.name,
                    'article': product.article,
                    'material': product.material,
                    'color': product.color,
                    'size': product.size
                })

        logger.info(f"Данные успешно экспортированы в файл: {file_path}")
    except Exception as e:
        logger.error(f"Ошибка при экспорте данных в CSV: {e}")
