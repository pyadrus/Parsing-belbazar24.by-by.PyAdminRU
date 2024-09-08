from peewee import *
from loguru import logger

# Настройка подключения к базе данных
db = SqliteDatabase('database.db')


# Определение модели
class BaseModel(Model):
    class Meta:
        database = db


class Product_Link(BaseModel):
    product_links = CharField()


# Модель для хранения информации о продуктах
class Product(BaseModel):
    link = CharField(unique=True)  # Ссылка на товар
    name = CharField()  # Название товара (равно артикулу)
    article = CharField()  # Артикул
    material = CharField()  # Материал
    color = CharField()  # Цвет
    size = CharField()  # Размер


db.connect()  # Создание таблиц, если они не существуют

# Проверка и создание таблиц, если они не существуют
if not Product_Link.table_exists():
    db.create_tables([Product_Link])
if not Product.table_exists():
    db.create_tables([Product])


def add_product(link, name, article, material, color, size):
    """Функция для добавления данных о продукте в базу данных"""
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
    """ Функция для записи данных в базу данных """
    try:
        Product_Link.create(product_links=product_links)
    except IntegrityError:
        return None


def remove_duplicates():
    """Функция для удаления дубликатов из таблицы `product_link` по полю `product_links`."""
    # Найти дубликаты по полю `product_links`
    duplicates = (Product_Link
                  .select(Product_Link.product_links, fn.COUNT(Product_Link.id).alias('count'))
                  .group_by(Product_Link.product_links)
                  .having(fn.COUNT(Product_Link.id) > 1))

    # Для каждого дубликата сохранить одно значение, а остальные удалить
    for duplicate in duplicates:
        # Получаем все записи с текущим значением `product_links`
        records = Product_Link.select().where(Product_Link.product_links == duplicate.product_links)

        # Пропускаем первую запись, а остальные удаляем
        for record in records[1:]:
            record.delete_instance()


def get_all_product_links():
    """Функция для получения всех записей из таблицы `product_link`."""
    try:
        product_links = Product_Link.select()
        # Преобразуем записи в список строк
        return [record.product_links for record in product_links]
    except Exception as e:
        logger.error(f"Ошибка при получении данных: {e}")
        return []


if __name__ == '__main__':
    remove_duplicates()
    get_all_product_links()
