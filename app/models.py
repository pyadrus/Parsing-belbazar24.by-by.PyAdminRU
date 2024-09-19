from peewee import *
from loguru import logger

# Настройка подключения к базе данных
db = SqliteDatabase('database.db')


# Определение модели
class BaseModel(Model):
    class Meta:
        database = db


class ProductLink(BaseModel):
    product_links = CharField()


class Product(BaseModel):
    """Модель для хранения информации о продуктах"""
    link = CharField(unique=True)  # Ссылка на товар
    name = CharField()  # Название товара (равно артикулу)
    article = CharField()  # Артикул
    material = CharField()  # Материал
    color = CharField()  # Цвет
    size = CharField()  # Размер


db.connect()  # Создание таблиц, если они не существуют

# Проверка и создание таблиц, если они не существуют

if not ProductLink.table_exists():
    db.create_tables([ProductLink])
if not Product.table_exists():
    db.create_tables([Product])


def add_product(link, name, article, material, color, size):
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
        Product.create(
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


def add_user(product_links):
    """
    Функция для записи данных в базу данных
    :param product_links: Ссылка на товар
    """
    try:
        ProductLink.create(product_links=product_links)
    except IntegrityError:
        return None


def remove_duplicates_product():
    """Функция для удаления дубликатов из таблицы `product_link` по полю `product_links`."""
    # Найти дубликаты по полю `product_links`
    duplicates = (Product
                  .select(Product.article, fn.COUNT(Product.id).alias('count'))
                  .group_by(Product.article)
                  .having(fn.COUNT(Product.id) > 1))

    # Для каждого дубликата сохранить одно значение, а остальные удалить
    for duplicate in duplicates:
        # Получаем все записи с текущим значением `product_links`
        records = Product.select().where(Product.article == duplicate.article)

        # Пропускаем первую запись, а остальные удаляем
        for record in records[1:]:
            record.delete_instance()


def remove_duplicates():
    """Функция для удаления дубликатов из таблицы `product_link` по полю `product_links`."""
    # Найти дубликаты по полю `product_links`
    duplicates = (ProductLink
                  .select(ProductLink.product_links, fn.COUNT(ProductLink.id).alias('count'))
                  .group_by(ProductLink.product_links)
                  .having(fn.COUNT(ProductLink.id) > 1))

    # Для каждого дубликата сохранить одно значение, а остальные удалить
    for duplicate in duplicates:
        # Получаем все записи с текущим значением `product_links`
        records = ProductLink.select().where(ProductLink.product_links == duplicate.product_links)

        # Пропускаем первую запись, а остальные удаляем
        for record in records[1:]:
            record.delete_instance()


def get_all_product_links():
    """Функция для получения всех записей из таблицы `product_link`."""
    try:
        product_links = ProductLink.select()
        # Преобразуем записи в список строк
        return [record.product_links for record in product_links]
    except Exception as e:
        logger.error(f"Ошибка при получении данных: {e}")
        return []


if __name__ == '__main__':
    remove_duplicates()
    get_all_product_links()
    remove_duplicates_product()
