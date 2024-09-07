from peewee import *
from loguru import logger
logger.add("log/log.log", rotation="1 MB", compression="zip")  # Логирование программы

# Настройка подключения к базе данных
db = SqliteDatabase('my_database.db')

# Определение модели
class BaseModel(Model):
    class Meta:
        database = db

class product_link(BaseModel):
    product_links = CharField()


db.connect()# Создание таблиц, если они не существуют
db.create_tables([product_link])

def add_user(product_links):
    """ Функция для записи данных в базу данных """
    try:
        product_link.create(product_links=product_links)
    except IntegrityError:
        return None

def remove_duplicates():
    """Функция для удаления дубликатов из таблицы `product_link` по полю `product_links`."""
    # Найти дубликаты по полю `product_links`
    duplicates = (product_link
                  .select(product_link.product_links, fn.COUNT(product_link.id).alias('count'))
                  .group_by(product_link.product_links)
                  .having(fn.COUNT(product_link.id) > 1))

    # Для каждого дубликата сохранить одно значение, а остальные удалить
    for duplicate in duplicates:
        # Получаем все записи с текущим значением `product_links`
        records = product_link.select().where(product_link.product_links == duplicate.product_links)

        # Пропускаем первую запись, а остальные удаляем
        for record in records[1:]:
            record.delete_instance()


if __name__ == '__main__':
    remove_duplicates()
