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

