from peewee import *
from loguru import logger

db = SqliteDatabase('database.db')  # Настройка подключения к базе данных


class BaseModel(Model):
    """Определение модели"""

    class Meta:
        database = db


class ProductLinkBenefit(BaseModel):
    """Таблица для ссылок раздела 'Купи выгодно'"""
    product_links_benefit = CharField()


class ProductBenefit(BaseModel):
    """Модель для хранения информации о продуктах"""
    link = CharField(unique=True)  # Ссылка на товар
    name = CharField()  # Название товара (равно артикулу)
    article = CharField()  # Артикул
    material = CharField()  # Материал
    color = CharField()  # Цвет
    size = CharField()  # Размер


db.connect()  # Создание таблиц, если они не существуют

# Проверка и создание таблиц, если они не существуют
if not ProductLinkBenefit.table_exists():
    db.create_tables([ProductLinkBenefit])
if not ProductBenefit.table_exists():
    db.create_tables([ProductBenefit])


def add_product_benefit(link, name, article, material, color, size):
    """
    Функция для добавления данных о продукте в базу данных
    :param link: Ссылка на товар
    :param name: Название товара (равно артикулу)
    :param article: Артикул
    :param material: Материал
    :param color: Цвет
    :param size: Размер
    """
    try:
        ProductBenefit.create(
            link=link,
            name=name,
            article=article,
            material=material,
            color=color,
            size=size
        )
        logger.info(f"Продукт добавлен: {name} ({article})")
    except IntegrityError:
        logger.warning(f"Продукт с ссылкой {link} уже существует.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении продукта: {e}")


def add_user_benefit(product_links_benefit):
    """
    Функция для записи данных в базу данных
    :param product_links_benefit: Ссылка на товар
    :return: None
    """
    try:
        logger.info(f"Продукт добавлен: {product_links_benefit}")
        ProductLinkBenefit.create(product_links_benefit=product_links_benefit)  # Здесь нужно исправить
    except IntegrityError:
        return None


def remove_duplicates_product_benefit():
    """Функция для удаления дубликатов из таблицы `product_link` по полю `product_links`."""
    # Найти дубликаты по полю `product_links`
    duplicates = (ProductBenefit
                  .select(ProductBenefit.article, fn.COUNT(ProductBenefit.id).alias('count'))
                  .group_by(ProductBenefit.article)
                  .having(fn.COUNT(ProductBenefit.id) > 1))

    # Для каждого дубликата сохранить одно значение, а остальные удалить
    for duplicate in duplicates:
        # Получаем все записи с текущим значением `product_links`
        records = ProductBenefit.select().where(ProductBenefit.article == duplicate.article)

        # Пропускаем первую запись, а остальные удаляем
        for record in records[1:]:
            record.delete_instance()


def remove_duplicates_benefit():
    """Функция для удаления дубликатов из таблицы `product_link` по полю `product_links`."""
    # Найти дубликаты по полю `product_links`
    duplicates = (ProductLinkBenefit
                  .select(ProductLinkBenefit.product_links_benefit, fn.COUNT(ProductLinkBenefit.id).alias('count'))
                  .group_by(ProductLinkBenefit.product_links_benefit)
                  .having(fn.COUNT(ProductLinkBenefit.id) > 1))

    # Для каждого дубликата сохранить одно значение, а остальные удалить
    for duplicate in duplicates:
        # Получаем все записи с текущим значением `product_links`
        records = ProductLinkBenefit.select().where(
            ProductLinkBenefit.product_links_benefit == duplicate.product_links_benefit)

        # Пропускаем первую запись, а остальные удаляем
        for record in records[1:]:
            record.delete_instance()


def get_all_product_links_benefit():
    """Функция для получения всех записей из таблицы `product_link`."""
    try:
        product_links_benefit = ProductLinkBenefit.select()
        # Преобразуем записи в список строк
        return [record.product_links_benefit for record in product_links_benefit]
    except Exception as e:
        logger.error(f"Ошибка при получении данных: {e}")
        return []


if __name__ == '__main__':
    get_all_product_links_benefit()
    remove_duplicates_benefit()
    remove_duplicates_product_benefit()
